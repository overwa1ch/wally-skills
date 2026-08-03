"""Anonymous, standard-library regression fixtures for the six Wally skills."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
HELPER_SCRIPTS = REPO / "wally-helper" / "scripts"


class RouteValidatorTests(unittest.TestCase):
    maxDiff = None

    def run_validator(
        self,
        route: str,
        prompt: str,
        body: str,
        bindings: dict,
        mode: str,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prompt_path = root / "prompt.txt"
            body_path = root / "body.txt"
            bindings_path = root / "bindings.json"
            prompt_path.write_text(prompt, encoding="utf-8")
            body_path.write_text(body, encoding="utf-8")
            bindings_path.write_text(
                json.dumps(bindings, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            return subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(HELPER_SCRIPTS / f"validate_route_{route.lower()}_prompt.py"),
                    str(prompt_path),
                    "--director-body",
                    str(body_path),
                    "--bindings",
                    str(bindings_path),
                    "--audio-mode",
                    mode,
                ],
                check=False,
                capture_output=True,
                text=True,
            )

    @staticmethod
    def route_a_prompt(body: str) -> str:
        return (
            "SEG01\n\n"
            "Reference List:\n"
            "“红色保温壶” = @image1 - Pxx 道具身份。\n"
            "“SEG01镜头板” = @image2 - 故事板。\n\n"
            "影片调性：内容类型为产品短片。\n\n"
            "Prompt:\n"
            "请根据以上参考生成本段视频。故事板控制镜头顺序、运镜、人物动作、空间关系和道具关系。\n\n"
            f"{body.rstrip()}\n\n"
            "Constraints:\n"
            "无旁白、无画外解说。\n"
        )

    @staticmethod
    def route_b_prompt(rendered_body: str, avoid: str | None = None) -> str:
        constraints = (
            "只使用本SEG Asset List中的成品资产；不得把参考板内部局部或状态拆成独立资产。\n"
            "无旁白、无画外解说。"
        )
        if avoid is not None:
            constraints += f"\n禁止出现：{avoid}"
        return (
            "SEG01\n\n"
            "Asset List:\n"
            "“红色保温壶” = @image1 - Pxx 道具身份。\n\n"
            "Prompt:\n"
            f"{rendered_body.rstrip()}\n\n"
            "Constraints:\n"
            f"{constraints}\n"
        )

    @staticmethod
    def body(audio_line: str, *, legacy: bool = False, avoid: bool = False) -> str:
        label = "SFX" if legacy else "Audio"
        text = (
            "Subject: 主道具。\n"
            "Action: 主道具在灰色桌面上静止展示。\n"
            f"{label}: {audio_line}\n"
            "Constraints: 道具外形和颜色保持稳定。"
        )
        if avoid:
            text += "\nAvoid: 额外文字和水印。"
        return text

    @staticmethod
    def rendered(source: str) -> str:
        without_avoid = re.sub(r"\nAvoid:.*\Z", "", source)
        return without_avoid.replace("主道具", "“红色保温壶”")

    def setUp(self) -> None:
        self.bindings_a = json.loads(
            (FIXTURES / "bindings-route-a.json").read_text(encoding="utf-8")
        )
        self.bindings_b = json.loads(
            (FIXTURES / "bindings-route-b.json").read_text(encoding="utf-8")
        )

    def assertPass(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS:", result.stdout)

    def assertFail(self, result: subprocess.CompletedProcess[str], phrase: str) -> None:
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(phrase, result.stderr)

    def test_frozen_default_route_a_fixture_passes(self) -> None:
        result = self.run_validator(
            "a",
            (FIXTURES / "route-a-default.prompt").read_text(encoding="utf-8"),
            (FIXTURES / "route-a-default.body").read_text(encoding="utf-8"),
            self.bindings_a,
            "default",
        )
        self.assertPass(result)

    def test_frozen_default_route_b_fixture_passes(self) -> None:
        result = self.run_validator(
            "b",
            (FIXTURES / "route-b-default.prompt").read_text(encoding="utf-8"),
            (FIXTURES / "route-b-default.body").read_text(encoding="utf-8"),
            self.bindings_b,
            "default",
        )
        self.assertPass(result)

    def test_audio_three_branches_and_legacy_pass_on_both_routes(self) -> None:
        cases = (
            ("default", "无BGM。轻微室内房间音与壶底摩擦声。", False),
            ("music", "低声部弦乐缓慢持续，室内声压低。", False),
            ("silence", "全程绝对静音。", False),
            ("default", "无BGM。轻微室内房间音与壶底摩擦声。", True),
        )
        for mode, audio, legacy in cases:
            with self.subTest(route="A", mode=mode, legacy=legacy):
                source = self.body(audio, legacy=legacy)
                route_a_source = source.replace("主道具", "红色保温壶")
                self.assertPass(
                    self.run_validator(
                        "a", self.route_a_prompt(route_a_source), route_a_source,
                        self.bindings_a, mode,
                    )
                )
            with self.subTest(route="B", mode=mode, legacy=legacy):
                source = self.body(audio, legacy=legacy, avoid=True)
                self.assertPass(
                    self.run_validator(
                        "b", self.route_b_prompt(self.rendered(source), "额外文字和水印。"),
                        source, self.bindings_b, mode,
                    )
                )

    def test_missing_audio_and_wrong_audio_branch_fail(self) -> None:
        body = "Subject: 红色保温壶。\nAction: 红色保温壶静止展示。"
        self.assertFail(
            self.run_validator("a", self.route_a_prompt(body), body, self.bindings_a, "default"),
            "must contain exactly one Audio field",
        )
        music = "Subject: 红色保温壶。\nAction: 红色保温壶静止展示。\nAudio: 柔和弦乐持续。"
        self.assertFail(
            self.run_validator("a", self.route_a_prompt(music), music, self.bindings_a, "default"),
            "must start with `无BGM。`",
        )
        bad_silence = "Subject: 红色保温壶。\nAction: 红色保温壶静止展示。\nAudio: 全程绝对静音，但保留房间音。"
        self.assertFail(
            self.run_validator("a", self.route_a_prompt(bad_silence), bad_silence, self.bindings_a, "silence"),
            "must not add ambience",
        )

    def test_route_a_rejects_body_mutation_raw_handle_placeholder_and_bad_binding(self) -> None:
        body = (FIXTURES / "route-a-default.body").read_text(encoding="utf-8").rstrip()
        mutated_prompt = self.route_a_prompt(body.replace("静止展示", "缓慢旋转"))
        self.assertFail(
            self.run_validator("a", mutated_prompt, body, self.bindings_a, "default"),
            "differs from approved body",
        )
        raw = body.replace("红色保温壶。", "红色保温壶 @image1。", 1)
        self.assertFail(
            self.run_validator("a", self.route_a_prompt(raw), raw, self.bindings_a, "default"),
            "raw platform handle",
        )
        self.assertFail(
            self.run_validator("a", self.route_a_prompt(body) + "SEGXX\n", body, self.bindings_a, "default"),
            "unresolved template placeholder",
        )
        mismatch = json.loads(json.dumps(self.bindings_a, ensure_ascii=False))
        mismatch["bindings"][0]["handle"] = "@image9"
        self.assertFail(
            self.run_validator("a", self.route_a_prompt(body), body, mismatch, "default"),
            "missing approved binding",
        )

    def test_route_b_allows_only_declared_identity_and_trailing_avoid_changes(self) -> None:
        source = self.body("无BGM。轻微室内房间音与壶底摩擦声。", avoid=True)
        rendered = self.rendered(source).replace("静止展示", "快速旋转")
        self.assertFail(
            self.run_validator(
                "b", self.route_b_prompt(rendered, "额外文字和水印。"), source,
                self.bindings_b, "default",
            ),
            "changes content beyond declared identity",
        )
        wrong_avoid = self.route_b_prompt(self.rendered(source), "另一条限制。")
        self.assertFail(
            self.run_validator("b", wrong_avoid, source, self.bindings_b, "default"),
            "trailing Avoid must appear exactly once",
        )

    def test_route_b_rejects_storyboard_duplicate_binding_and_continuity_only_use(self) -> None:
        storyboard = json.loads(json.dumps(self.bindings_b, ensure_ascii=False))
        storyboard["bindings"].append(
            {
                "segment": "SEG01",
                "identity": "SEG01镜头板",
                "handle": "@image2",
                "kind": "storyboard",
                "role": "故事板",
                "source_aliases": [],
            }
        )
        source = self.body("无BGM。轻微室内房间音。")
        self.assertFail(
            self.run_validator("b", self.route_b_prompt(self.rendered(source)), source, storyboard, "default"),
            "globally forbids storyboard",
        )

        duplicate = json.loads(json.dumps(self.bindings_b, ensure_ascii=False))
        extra = dict(duplicate["bindings"][0])
        extra["handle"] = "@image2"
        duplicate["bindings"].append(extra)
        self.assertFail(
            self.run_validator("b", self.route_b_prompt(self.rendered(source)), source, duplicate, "default"),
            "duplicated",
        )

        continuity_source = (
            "Continuity: 主道具外形和颜色保持。\n"
            "Action: 画面保持静止。\n"
            "Audio: 无BGM。轻微室内房间音。"
        )
        continuity_rendered = continuity_source.replace("主道具", "“红色保温壶”")
        self.assertFail(
            self.run_validator(
                "b", self.route_b_prompt(continuity_rendered), continuity_source,
                self.bindings_b, "default",
            ),
            "Continuity-only",
        )


class SkillContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (REPO / relative).read_text(encoding="utf-8")

    def test_screenplay_dialogue_triggers_eight_steps_and_single_menu_owner(self) -> None:
        skill = self.read("wally-screenplay-writer/SKILL.md")
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
        self.assertIsNotNone(frontmatter)
        for phrase in ("原创对白", "台词写作", "对白改写", "对白诊断"):
            self.assertIn(phrase, frontmatter.group(1))
        expected = (
            "1. 破题与核心动作\n2. 梗概草稿\n3. 人物深度与弧光\n"
            "4. 前史与世界观\n5. 结构大纲\n6. 场景拆解\n"
            "7. 场景写作\n8. 剧本医生"
        )
        self.assertIn(expected, skill)
        for label in ("[通过]", "[修改]", "[自检]", "[通过并锁定]"):
            self.assertIn(label, skill)
        canonical = re.search(
            r"## Workflow\n\n((?:[1-8]\. .+\n){8})", skill
        )
        self.assertIsNotNone(canonical)
        canonical_names = [
            line.split(". ", 1)[1]
            for line in canonical.group(1).strip().splitlines()
        ]
        short = self.read("wally-screenplay-writer/references/format-short.md")
        short_names = re.findall(
            r"(?m)^### 第[一二三四五六七八]步：(.+)$", short
        )
        short_names = [
            re.sub(r"（短片精简版）$", "", name) for name in short_names
        ]
        self.assertEqual(short_names, canonical_names)
        references = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((REPO / "wally-screenplay-writer/references").glob("*.md"))
        )
        self.assertNotIn("请选择：回复", references)
        self.assertNotIn("通过并锁定", references)
        self.assertIn("## Define the work", skill)
        self.assertIn("## 作品定义", skill)
        self.assertIn(
            "叙事超短片聚焦1-2个中心人物，不强制完整Want/Need/Arc",
            short,
        )
        self.assertIn(
            "叙事超短片至少呈现一次可见的选择、让步或关系变化",
            short,
        )
        self.assertIn(
            "叙事超短片采用“建立处境—形成压力—做出选择—落到可见结果”",
            short,
        )
        self.assertIn(
            "叙事短片使用1-2个主角和完整Want/Need/Arc",
            short,
        )
        self.assertIn("叙事短片完成一次A→B变化", short)

    def test_storyboard_open_input_svg_and_fixed_prompt_routes(self) -> None:
        skill = self.read("wally-storyboard-designer/SKILL.md")
        svg = self.read("wally-storyboard-designer/references/scene-layout-svg-rules.md")
        tree = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((REPO / "wally-storyboard-designer").rglob("*.md"))
        )
        for phrase in ("prose", "tables", "images", "partial", "conflicting"):
            self.assertIn(phrase, skill)
        for phrase in (
            "Create one SVG per supplied scene immediately",
            "do not require another storyboard-domain product first",
        ):
            self.assertIn(phrase, svg)
        self.assertIn("Leave `SEGXX` unchanged for a generic reusable prompt", skill)
        self.assertIn("exact current SEG identifier", skill)
        self.assertNotIn("READY_FOR_FIXED_STORYBOARD_PROMPT", tree)
        self.assertNotIn("handoff-to-storyboard.md", tree)
        self.assertIsNone(
            re.search(r"(?i)full[- ]chain|WAITING_FOR_|## Output gates", tree)
        )
        self.assertIn("Provide on-demand storyboard-domain functions", skill)
        self.assertIn(
            "Copy the source screenplay's `## 作品定义` block verbatim",
            skill,
        )
        self.assertIn(
            "Keep the fixed storyboard and shot-table prompt templates verbatim",
            skill,
        )
        director_contract = self.read(
            "wally-storyboard-designer/references/director-script-output-contract.md"
        )
        self.assertIn("状态：DIRECTOR_SCRIPT_READY", director_contract)
        self.assertIn("## 作品定义", director_contract)
        design = self.read(
            "wally-storyboard-designer/references/storyboard-design.md"
        )
        self.assertIn("## Carry the work definition", design)
        self.assertIn(
            "Begin every complete storyboard or shot-sequence design",
            design,
        )

    def test_helper_routes_storyboard_revisions_to_the_storyboard_specialist(self) -> None:
        helper = self.read("wally-helper/SKILL.md")
        workflow = self.read("wally-helper/references/workflow-guide.md")
        self.assertIn(
            "wally-helper@2026-08-03-v3.12-wally-project-scope-cutover",
            helper,
        )
        self.assertIn(
            "hand those revisions to `wally-storyboard-designer` for integration",
            workflow,
        )
        self.assertIn(
            "When the updated director script returns",
            workflow,
        )
        self.assertIn(
            "Do not author or revise any specialist product.",
            helper,
        )
        self.assertNotIn("integrate every named shot-design revision", workflow)

    def test_static_four_grid_and_prop_state_contracts(self) -> None:
        four = self.read("wally-static-asset-designer/types/multi-angle-2x2.md")
        fixed_blocks = re.findall(r"```text\n(.*?)```", four, re.DOTALL)
        self.assertEqual(
            fixed_blocks[0].strip(),
            "参考场景资产图，生成这个XX场景不同角度不同景别的2×2四宫格场景图。",
        )
        self.assertEqual(fixed_blocks[0].count("XX"), 1)
        static_skill = self.read("wally-static-asset-designer/SKILL.md")
        self.assertIn("This nine-grid remains the default", static_skill)
        self.assertIn("do not append the fallback prompt", static_skill)
        state = self.read("wally-static-asset-designer/types/pxx-state.md")
        labels = (
            "**基础道具参考**", "**目标状态**", "**状态变化**",
            "**保持不变**", "**材质与物理表现**", "**状态一致性**",
        )
        positions = [state.index(label) for label in labels]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("缺图时指出缺失并停止", state)
        self.assertIn("只有用户明确要求草案", state)
        self.assertIn("不生成基准状态或前后对比", state)

    def test_visual_evidence_owner_sources_and_json_boundaries(self) -> None:
        skill = self.read("wally-visual-style-extractor/SKILL.md")
        templates = self.read(
            "wally-visual-style-extractor/references/style-extraction-templates.md"
        )
        for phrase in (
            "Do not design static-asset identities",
            "Do not design a shot sequence",
            "dialogue, or audio",
            "final image-to-video or text-to-video prompts",
        ):
            self.assertIn(phrase, skill)
        analysis = templates.split("## Analysis Card", 1)[1].split("## Three-Stage Brief", 1)[0]
        block = re.findall(r"```text\n(.*?)```", analysis, re.DOTALL)[0]
        self.assertEqual(len(re.findall(r"(?m)^Evidence strength:\s*$", block)), 1)
        self.assertIn("Canonical match: none confirmed", templates)
        self.assertIn('"term": "<canonical or supporting established term>"', templates)
        self.assertIn('"camera": "<user-supplied camera value, or reusable placeholder>"', templates)
        self.assertNotIn("repeated style tendency", templates)

    def test_action_owns_only_approved_dialogue_execution_and_three_audio_modes(self) -> None:
        skill = self.read("wally-action-designer/SKILL.md")
        craft = self.read("wally-action-designer/references/craft.md")
        contract = self.read("wally-action-designer/references/contract.md")
        self.assertIn("已批准台词的表演与口型执行", skill)
        self.assertIn("do not trigger for original dialogue writing or rewrite", skill)
        self.assertIn("never propose alternatives here", craft)
        self.assertIn("Music unspecified: start with `无BGM。`", contract)
        self.assertIn("Music explicitly supplied or requested", contract)
        self.assertIn("Absolute silence explicitly required", contract)


if __name__ == "__main__":
    unittest.main()
