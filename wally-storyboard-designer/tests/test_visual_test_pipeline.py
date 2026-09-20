from __future__ import annotations

import importlib.util
import base64
import html
from html.parser import HTMLParser
from io import BytesIO
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

from PIL import Image, ImageChops, ImageDraw


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "visual_test_pipeline.py"
SPEC = importlib.util.spec_from_file_location("visual_test_pipeline", SCRIPT)
pipeline = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(pipeline)


SOURCE_TEXT = """## 作品定义
测试。

## 场景1：院子 / 清晨

### 分镜1｜第一镜
画面内容：一。

### 分镜2｜第二镜
画面内容：二。
"""


class VisualTestPipelineTests(unittest.TestCase):
    def init_storyboard(self, root: Path, versions: int = 2) -> Path:
        source = root / "director.md"
        source.write_text(SOURCE_TEXT, encoding="utf-8")
        output = root / "run"
        pipeline.init_run(SimpleNamespace(
            source=source, output=output, mode="storyboard", run_id="test-r01",
            work="测试作品", versions=versions, project_name=None, assets_json=None,
        ))
        manifest_path = output / "manifest.json"
        pipeline.set_project(SimpleNamespace(manifest=manifest_path, url="https://chatgpt.com/g/test-project"))
        return manifest_path

    def test_init_preserves_scene_and_shot_order(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            manifest_path = self.init_storyboard(Path(temporary))
            manifest = pipeline.load_manifest(manifest_path)
            self.assertEqual(manifest["grid"], {"columns": 3, "rows": 3, "panel_aspect": "16:9"})
            self.assertEqual(manifest["jobs"][0]["shot_ids"], [1, 2])
            packet = (manifest_path.parent / manifest["jobs"][0]["packet"]).read_text(encoding="utf-8")
            self.assertEqual(packet, SOURCE_TEXT)
            self.assertEqual(manifest["jobs"][0]["packet_sha256"], manifest["source"]["sha256"])

    def test_scene_packets_keep_context_and_all_pages_share_one_scene_chat(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "director.md"
            preamble = "Style: 胶片。\r\nLighting/mood: 日光。\r\n"
            first = "## 场景1：院子 / 日\r\n场景说明：保持红门。\r\n"
            first += "".join(f"### 分镜{n}｜镜头\r\n画面内容：动作{n}。\r\n" for n in range(1, 11))
            first += "## 声音与衔接\r\nAudio: 警铃延续至下一场。\r\n"
            second = "## 场景2：门口 / 夜\r\n**Shot 11 [0.0-3.0s]**\r\nDialogue: 原台词。"
            source.write_bytes((preamble + first + second).encode())
            context = root / "global.md"
            context.write_text("参考绑定：C01。", encoding="utf-8")
            output = root / "run"
            pipeline.init_run(SimpleNamespace(
                source=source, output=output, mode="storyboard", run_id="scenes",
                work="测试作品", versions=1, project_name=None, assets_json=None, context=context,
            ))
            path = output / "manifest.json"
            manifest = pipeline.load_manifest(path)
            self.assertEqual([j["shot_ids"] for j in manifest["jobs"]], [list(range(1, 10)), [10], [11]])
            self.assertEqual(len({j["packet"] for j in manifest["jobs"]}), 2)
            self.assertEqual((output / manifest["source"]["copy"]).read_bytes(), source.read_bytes())
            for job in manifest["jobs"]:
                expected = preamble + "参考绑定：C01。\n\n" + (first if job["scene_id"] == "S01" else second)
                self.assertEqual((output / job["packet"]).read_bytes(), expected.encode())
            pipeline.set_scene(SimpleNamespace(manifest=path, scene="S01", url="https://chatgpt.com/c/scene-1"))
            updated = pipeline.load_manifest(path)
            self.assertEqual([j["chat_url"] for j in updated["jobs"]],
                             ["https://chatgpt.com/c/scene-1", "https://chatgpt.com/c/scene-1", None])
            self.assertIn("场景1：院子", updated["scenes"][0]["chat_name"])
            packet = output / updated["jobs"][0]["packet"]
            packet.write_text("删减后的内容", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "packet missing or changed"):
                pipeline.validate_ready(path, updated)

    def test_mixed_shot_formats_fail_before_writing_a_partial_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "director.md"
            source.write_text(SOURCE_TEXT + "\n| 03 | 表格镜头 |\n", encoding="utf-8")
            output = root / "run"
            with self.assertRaisesRegex(ValueError, "mixes shot blocks and table rows"):
                pipeline.init_run(SimpleNamespace(
                    source=source, output=output, mode="storyboard", run_id="mixed",
                    work="作品", versions=1, project_name=None, assets_json=None,
                ))
            self.assertFalse(output.exists())
            source.write_text("## 场景1：门口 / 日\n| 1 | 动作一 |\nAudio: 敲门。\n| 2 | 动作二 |\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "interleaved table text"):
                pipeline.init_run(SimpleNamespace(
                    source=source, output=output, mode="storyboard", run_id="mixed",
                    work="作品", versions=1, project_name=None, assets_json=None,
                ))
            self.assertFalse(output.exists())

    def test_table_director_script_is_paginated_without_rewriting_rows(self) -> None:
        text = """# 表格分镜\n\n## 场景1：院子 / 日\n\n| 镜 | 内容 |\n| --- | --- |\n| 01 | 动作一 |\n| 02 | 动作二 |\n\n## 场景2：门口 / 夜\n\n| 镜 | 内容 |\n| --- | --- |\n| 03 | 动作三 |\n"""
        preamble, scenes = pipeline.scene_records(text)
        self.assertEqual(preamble, "# 表格分镜\n\n")
        self.assertEqual([scene["shot_ids"] for scene in scenes], [[1, 2], [3]])
        self.assertEqual(scenes[0]["source_format"], "table")
        self.assertEqual("".join(scenes[0]["shot_blocks"]), "| 01 | 动作一 |\n| 02 | 动作二 |\n")

    def test_shot_table_uploads_assets_once_and_branches_by_scene(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "director.md"
            source.write_text(SOURCE_TEXT + "\n## 场景2：门口 / 夜\n**Shot 3 [0.0-2.0s]**\n抬头。\n", encoding="utf-8")
            asset = root / "person.png"
            Image.new("RGB", (64, 64), "gray").save(asset)
            assets_json = root / "assets.json"
            assets_json.write_text(json.dumps({scene: [{"id": "C01", "name": "人物", "path": "person.png"}] for scene in ("S01", "S02")}), encoding="utf-8")
            output = root / "run"
            pipeline.init_run(SimpleNamespace(
                source=source, output=output, mode="shot-table", run_id="shot-table-test",
                work="测试作品", versions=2, project_name=None, assets_json=assets_json,
            ))
            manifest = pipeline.load_manifest(output / "manifest.json")
            self.assertEqual(manifest["grid"]["columns"], 2)
            self.assertEqual(len(manifest["asset_bases"]), 1)
            self.assertEqual(len(manifest["asset_bases"][0]["upload_files"]), 1)
            self.assertEqual(len(manifest["scenes"]), 2)
            self.assertEqual(manifest["assets_by_scene"]["S01"][0]["sha256"], pipeline.sha256(asset))
            self.assertTrue((output / manifest["asset_bases"][0]["mapping_prompt"]).is_file())

            with self.assertRaisesRegex(ValueError, "asset base is not confirmed"):
                pipeline.validate_ready(output / "manifest.json", manifest)

            pipeline.set_asset_base(SimpleNamespace(manifest=output / "manifest.json", url="https://chatgpt.com/c/assets"))
            for number in (1, 2):
                pipeline.set_scene(SimpleNamespace(manifest=output / "manifest.json", scene=f"S{number:02d}", url=f"https://chatgpt.com/c/branch-{number}"))
            updated = pipeline.load_manifest(output / "manifest.json")
            self.assertEqual([j["branch_url"] for j in updated["jobs"]],
                             ["https://chatgpt.com/c/branch-1", "https://chatgpt.com/c/branch-2"])

    def test_unrecorded_or_rejected_versions_block_assembly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            manifest_path = self.init_storyboard(Path(temporary), versions=1)
            manifest = pipeline.load_manifest(manifest_path)
            with self.assertRaisesRegex(ValueError, "status=pending"):
                pipeline.validate_ready(manifest_path, manifest)
            version = manifest["jobs"][0]["versions"][0]
            version.update({"status": "rejected", "artifact_origin": "code-or-file-substitute"})
            with self.assertRaisesRegex(ValueError, "non-native origin"):
                pipeline.validate_ready(manifest_path, manifest)

    def test_visible_grid_detection_skips_full_sheet_header(self) -> None:
        image = Image.new("RGB", (1600, 900), "white")
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 1599, 39), fill="black")
        for y in (50, 330, 610):
            draw.rectangle((0, y, 1599, y + 19), fill="black")
        for x in (10, 540, 1070, 1590):
            draw.line((x, 50, x, 899), fill="black", width=2)
        boxes = pipeline.detected_grid_boxes(image, 3, 3)
        self.assertEqual(boxes[0], (10, 50, 540, 330))
        self.assertEqual(boxes[3], (10, 330, 540, 610))
        self.assertEqual(boxes[6], (10, 610, 540, 900))

    def test_run_level_block_is_recorded_without_rejecting_versions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            manifest_path = self.init_storyboard(Path(temporary), versions=1)
            pipeline.block_run(SimpleNamespace(
                manifest=manifest_path, stage="browser-automation",
                reason="in-app Browser control is unavailable",
            ))
            manifest = pipeline.load_manifest(manifest_path)
            self.assertEqual(manifest["status"], "blocked")
            self.assertEqual(manifest["errors"][-1]["stage"], "browser-automation")
            self.assertIn("control is unavailable", manifest["errors"][-1]["reason"])
            self.assertEqual(manifest["jobs"][0]["versions"][0]["status"], "pending")

    def test_no_confirmation_means_no_cropping_or_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = self.init_storyboard(root, versions=1)
            before = path.read_bytes()
            with self.assertRaisesRegex(ValueError, "user confirmation required"):
                pipeline.assemble_run(SimpleNamespace(manifest=path, format="html", approval_note=""))
            self.assertEqual(before, path.read_bytes())
            self.assertFalse((path.parent / "panels").exists())
            self.assertFalse((path.parent / "assembled").exists())
            original = root / "native.png"
            Image.new("RGB", (1600, 900), "white").save(original)
            pipeline.record_native(SimpleNamespace(manifest=path, job="SB-S01-P01", version="V01", file=original,
                chat_url="https://chatgpt.com/c/scene-1", native_card_evidence="synthetic fixture",
                download_url=None, replace=False))
            pipeline.assemble_run(SimpleNamespace(manifest=path, format="panels", approval_note="测试夹具仅授权切图"))
            finished = pipeline.load_manifest(path)
            self.assertEqual(set(finished["deliverables"]), {"panels"})
            self.assertEqual(len(finished["deliverables"]["panels"]), 2)
            self.assertFalse((path.parent / "assembled/review.pdf").exists())
            self.assertFalse((path.parent / "assembled/storyboard.html").exists())

    def test_html_pairs_original_text_with_each_panel_in_source_order(self) -> None:
        class Rows(HTMLParser):
            def __init__(self):
                super().__init__()
                self.rows = []
                self.current = None
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == "article":
                    self.current = {"scene": attrs["data-scene"], "shot": int(attrs["data-shot"]), "text": ""}
                    self.rows.append(self.current)
                if tag == "img" and self.current is not None:
                    self.current["src"] = attrs["src"]
            def handle_data(self, data):
                if self.current is not None:
                    self.current["text"] += data
            def handle_endtag(self, tag):
                if tag == "article":
                    self.current = None
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "performance.md"
            text = "Style: 胶片。\n## 场景1：院子 / 日\nLighting/mood: 柔光。\n"
            text += "**Shot 7 [0.0-2.0s]**\n人物看向对方。\n**Shot 4 [2.0-3.0s]**\n对白：<原文&保留>。\n"
            text += "## 场景2：门口 / 夜\n**Shot 23 [0.0-3.0s]**\nAudio: 门响。\n"
            source.write_text(text, encoding="utf-8")
            output = root / "run"
            pipeline.init_run(SimpleNamespace(source=source, output=output, mode="storyboard", run_id="html",
                                             work="表演图文", versions=1, project_name=None, assets_json=None))
            path = output / "manifest.json"
            manifest = pipeline.load_manifest(path)
            expected_colors = {}
            for job in manifest["jobs"]:
                img = Image.new("RGB", (1600, 900), "white")
                draw = ImageDraw.Draw(img)
                for index, (shot_id, box) in enumerate(zip(job["shot_ids"], pipeline.grid_boxes(img.size, 3, 3))):
                    color = (180 + index * 20, 210, 230)
                    draw.rectangle((box[0], box[1], box[2] - 1, box[3] - 1), fill=color)
                    expected_colors[(job["scene_id"], shot_id)] = color
                image_path = root / f"{job['scene_id']}.png"
                img.save(image_path)
                pipeline.record_native(SimpleNamespace(manifest=path, job=job["job_id"], version="V01", file=image_path,
                    chat_url=f"https://chatgpt.com/c/{job['scene_id']}", native_card_evidence="synthetic fixture",
                    download_url=None, replace=False))
            pipeline.assemble_run(SimpleNamespace(manifest=path, format="html", approval_note="测试夹具授权图文成品"))
            result = pipeline.load_manifest(path)
            body = (output / result["deliverables"]["document"]).read_text(encoding="utf-8")
            rows = Rows()
            rows.feed(body)
            self.assertEqual([(r["scene"], r["shot"]) for r in rows.rows], [("S01", 7), ("S01", 4), ("S02", 23)])
            for row in rows.rows:
                self.assertTrue(row["src"].startswith("data:image/png;base64,"))
                with Image.open(BytesIO(base64.b64decode(row["src"].split(",", 1)[1]))) as img:
                    self.assertEqual(img.getpixel((img.width // 2, img.height // 2)), expected_colors[(row["scene"], row["shot"])])
            self.assertIn("对白：<原文&保留>。", rows.rows[1]["text"])
            self.assertIn("**Shot 23 [0.0-3.0s]**", rows.rows[2]["text"])
            self.assertIn("Style: 胶片。", html.unescape(body))
            self.assertIn("Lighting/mood: 柔光。", html.unescape(body))
            self.assertFalse((output / "assembled/review.pdf").exists())
            # Moving a page into another chat must fail before replacing its source image.
            before = path.read_bytes()
            job = manifest["jobs"][0]
            with self.assertRaisesRegex(ValueError, "another scene chat"):
                pipeline.record_native(SimpleNamespace(manifest=path, job=job["job_id"], version="V01", file=image_path,
                    chat_url="https://chatgpt.com/c/a-new-page-chat", native_card_evidence="fixture",
                    download_url=None, replace=True))
            self.assertEqual(before, path.read_bytes())

    def test_selected_candidates_make_one_complete_document(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "director.md"
            source.write_text("Style: 日光。\n## 场景1：院子 / 日\n" + "".join(
                f"### 分镜{n}｜原镜\n动作：保持原文{n}。\n" for n in range(1, 11)
            ) + "## 场景2：门口 / 日\n### 分镜11｜原镜\n动作：走出门。\n", encoding="utf-8")
            pipeline.init_run(SimpleNamespace(source=source, output=root / "run", mode="storyboard",
                run_id="selection", work="选定图文", versions=2, project_name=None, assets_json=None))
            path = root / "run/manifest.json"
            manifest = pipeline.load_manifest(path)
            choices = {}
            for index, job in enumerate(manifest["jobs"]):
                version = "V02" if index == 1 else "V01"
                choices[job["job_id"]] = version
                original = root / f"candidate-{index}.png"
                Image.new("RGB", (960, 540), (50 + index * 60, 100, 150)).save(original)
                pipeline.record_native(SimpleNamespace(manifest=path, job=job["job_id"], version=version,
                    file=original, chat_url=f"https://chatgpt.com/c/{job['scene_id']}",
                    native_card_evidence="synthetic fixture", download_url=None, replace=False))
            # The rejected alternative and other pending alternatives are not selected.
            pipeline.reject_version(SimpleNamespace(manifest=path, job=manifest["jobs"][1]["job_id"],
                version="V01", origin="chatgpt-native-image-card", reason="用户未采用此候选"))
            pipeline.assemble_run(SimpleNamespace(manifest=path, format="html",
                select=[f"{job}={version}" for job, version in choices.items()],
                approval_note="合成测试：按逐页选择制作完整图文"))
            report = json.loads((path.parent / "assembled/assembly-report.json").read_text())
            self.assertEqual(report["selected_versions"], choices)
            self.assertEqual(report["panel_count"], 11)
            self.assertEqual([r["shot_id"] for r in report["panels"]], list(range(1, 12)))
            self.assertEqual([r["version"] for r in report["panels"]], ["V01"] * 9 + ["V02", "V01"])
            document = (path.parent / "assembled/storyboard.html").read_text()
            self.assertEqual(document.count("<article "), 11)
            self.assertEqual(document.count("<img "), 11)
            for record in report["panels"]:
                with Image.open(pipeline.run_path(path, record["source_raw"])) as original, Image.open(pipeline.run_path(path, record["panel"])) as panel:
                    self.assertIsNone(ImageChops.difference(original.crop(record["crop_box"]), panel).getbbox())
            self.assertFalse((path.parent / "panels/S01/P02/V01").exists())
            self.assertEqual(pipeline.load_manifest(path)["jobs"][1]["versions"][0]["status"], "rejected")

    def test_ambiguous_or_invalid_selection_does_not_write_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = self.init_storyboard(Path(temporary), versions=2)
            before = path.read_bytes()
            cases = [([], False), (["unknown=V01"], False), (["SB-S01-P01=V99"], False),
                     (["SB-S01-P01=V01", "SB-S01-P01=V02"], False), (["SB-S01-P01=V01"], True)]
            for choices, all_versions in cases:
                with self.subTest(choices=choices, all_versions=all_versions), self.assertRaises(ValueError):
                    pipeline.assemble_run(SimpleNamespace(manifest=path, format="html", select=choices,
                        all_versions=all_versions, approval_note="合成测试：制作图文"))
                self.assertEqual(path.read_bytes(), before)
                self.assertFalse((path.parent / "assembled").exists())
                self.assertFalse((path.parent / "panels").exists())

    def test_selected_rejected_or_corrupt_original_still_blocks_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = self.init_storyboard(root, versions=2)
            original = root / "original.png"
            Image.new("RGB", (960, 540), "white").save(original)
            pipeline.record_native(SimpleNamespace(manifest=path, job="SB-S01-P01", version="V01",
                file=original, chat_url="https://chatgpt.com/c/scene-1", native_card_evidence="fixture",
                download_url=None, replace=False))
            args = SimpleNamespace(manifest=path, format="panels", select=["SB-S01-P01=V01"],
                approval_note="合成测试：只采用 V01")
            manifest = pipeline.load_manifest(path)
            raw = pipeline.run_path(path, manifest["jobs"][0]["versions"][0]["raw_image"])
            raw.write_bytes(b"corrupted image")
            before = path.read_bytes()
            with self.assertRaisesRegex(ValueError, "raw hash mismatch"):
                pipeline.assemble_run(args)
            self.assertEqual(path.read_bytes(), before)
            pipeline.reject_version(SimpleNamespace(manifest=path, job="SB-S01-P01", version="V01",
                origin="chatgpt-native-image-card", reason="不可用"))
            with self.assertRaisesRegex(ValueError, "status=rejected"):
                pipeline.assemble_run(args)
            self.assertFalse((path.parent / "assembled").exists())
            self.assertFalse((path.parent / "panels").exists())

    def test_native_record_split_and_pdf_are_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest_path = self.init_storyboard(root)
            originals = []
            for number, color in ((1, "#cce0ff"), (2, "#ffe1cc")):
                source = Image.new("RGB", (1600, 900), color)
                image_path = root / f"native-{number}.png"
                source.save(image_path)
                originals.append(image_path)
                pipeline.record_native(SimpleNamespace(
                    manifest=manifest_path, job="SB-S01-P01", version=f"V{number:02d}", file=image_path,
                    chat_url="https://chatgpt.com/c/test-scene-1", native_card_evidence=f"native-card-{number}",
                    download_url=None, replace=False,
                ))
            manifest = pipeline.load_manifest(manifest_path)
            pipeline.validate_ready(manifest_path, manifest)
            pipeline.assemble_run(SimpleNamespace(manifest=manifest_path, format="review-pdf", all_versions=True, approval_note="测试夹具授权比较全部版本的审查 PDF"))
            finished = pipeline.load_manifest(manifest_path)
            self.assertEqual(finished["status"], "assembled-awaiting-human-review")
            self.assertTrue((manifest_path.parent / finished["deliverables"]["V01"]).is_file())
            self.assertTrue((manifest_path.parent / finished["deliverables"]["review_pdf"]).is_file())
            report = json.loads((manifest_path.parent / "assembled/assembly-report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["panel_count"], 4)
            self.assertEqual([record["shot_id"] for record in report["panels"]], [1, 2, 1, 2])
            for record in report["panels"]:
                with Image.open(pipeline.run_path(manifest_path, record["source_raw"])) as source, Image.open(pipeline.run_path(manifest_path, record["panel"])) as panel:
                    self.assertIsNone(ImageChops.difference(source.convert("RGB").crop(record["crop_box"]), panel.convert("RGB")).getbbox())


if __name__ == "__main__":
    unittest.main()
