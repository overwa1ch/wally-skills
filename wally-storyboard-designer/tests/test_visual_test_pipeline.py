from __future__ import annotations

import importlib.util
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
            self.assertEqual(packet, SOURCE_TEXT[SOURCE_TEXT.index("## 场景1") :])
            self.assertNotIn("作品定义", packet)
            self.assertIn("每次回复只调用一次原生生图", (manifest_path.parent / "browser/project-instructions.txt").read_text(encoding="utf-8"))
            self.assertIn("只绘制渲染包内实际存在的镜头块", (manifest_path.parent / "browser/project-instructions.txt").read_text(encoding="utf-8"))

    def test_table_director_script_is_paginated_without_rewriting_rows(self) -> None:
        text = """# 表格分镜\n\n## 场景1：院子 / 日\n\n| 镜 | 内容 |\n| --- | --- |\n| 01 | 动作一 |\n| 02 | 动作二 |\n\n## 场景2：门口 / 夜\n\n| 镜 | 内容 |\n| --- | --- |\n| 03 | 动作三 |\n"""
        preamble, scenes = pipeline.scene_records(text)
        self.assertEqual(preamble, "# 表格分镜\n\n")
        self.assertEqual([scene["shot_ids"] for scene in scenes], [[1, 2], [3]])
        self.assertEqual(scenes[0]["source_format"], "table")
        self.assertEqual("".join(scenes[0]["shot_blocks"]), "| 01 | 动作一 |\n| 02 | 动作二 |\n")

    def test_shot_table_init_records_scene_asset_base(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "director.md"
            source.write_text(SOURCE_TEXT, encoding="utf-8")
            asset = root / "person.png"
            Image.new("RGB", (64, 64), "gray").save(asset)
            assets_json = root / "assets.json"
            assets_json.write_text(json.dumps({"S01": [{"id": "C01", "name": "人物", "path": "person.png"}]}), encoding="utf-8")
            output = root / "run"
            pipeline.init_run(SimpleNamespace(
                source=source, output=output, mode="shot-table", run_id="shot-table-test",
                work="测试作品", versions=2, project_name=None, assets_json=assets_json,
            ))
            manifest = pipeline.load_manifest(output / "manifest.json")
            self.assertEqual(manifest["grid"]["columns"], 2)
            self.assertEqual(manifest["asset_bases"][0]["scene_id"], "S01")
            self.assertEqual(manifest["assets_by_scene"]["S01"][0]["sha256"], pipeline.sha256(asset))
            self.assertTrue((output / manifest["asset_bases"][0]["mapping_prompt"]).is_file())

            with self.assertRaisesRegex(ValueError, "project: missing URL"):
                pipeline.validate_ready(output / "manifest.json", manifest)

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
                    chat_url=f"https://chatgpt.com/c/test-{number}", native_card_evidence=f"native-card-{number}",
                    download_url=None, replace=False,
                ))
            manifest = pipeline.load_manifest(manifest_path)
            pipeline.validate_ready(manifest_path, manifest)
            pipeline.assemble_run(SimpleNamespace(manifest=manifest_path))
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
