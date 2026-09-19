"""Standard-library contract regressions for the Wally skill collection."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


REPO = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (REPO / relative).read_text(encoding="utf-8")

    def test_screenplay_v2_four_format_routes_and_dialogue_triggers(self) -> None:
        skill = self.read("wally-screenplay-writer/SKILL.md")
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
        self.assertIsNotNone(frontmatter)
        self.assertIn(
            "wally-screenplay-writer@2026-09-12-v2.1-adaptive-writing",
            skill,
        )
        for phrase in ("原创对白", "台词写作", "对白改写", "对白诊断"):
            self.assertIn(phrase, frontmatter.group(1))
        self.assertTrue(any(label in skill for label in ("四格式", "四种格式")))
        for pattern in (
            r"(?:概念超短片.{0,40}1\s*[-–]\s*3\s*分钟|1\s*[-–]\s*3\s*分钟.{0,40}概念超短片)",
            r"(?:叙事短片.{0,40}5\s*[-–]\s*10\s*分钟|5\s*[-–]\s*10\s*分钟.{0,40}叙事短片)",
            r"(?:长片.{0,20}90\s*分钟|90\s*分钟.{0,20}长片)",
            r"(?:剧集.{0,40}(?:连续剧|多集内容)|多集剧集)",
        ):
            self.assertRegex(skill, pattern)
        for phrase in (
            "四种格式是创作方法路由",
            "实际体量偏离默认值",
            "已有材料的定向对白",
        ):
            self.assertIn(phrase, skill)

        tree = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((REPO / "wally-screenplay-writer").rglob("*.md"))
        )
        self.assertNotIn("叙事超短片", tree)

        clarification_contexts = [
            skill[max(0, match.start() - 100):match.end() + 320]
            for match in re.finditer("完整叙事", skill)
        ]
        self.assertTrue(
            any(
                re.search(r"1\s*[-–]\s*3\s*分钟", context)
                and re.search(r"3\s*[-–]\s*5\s*分钟", context)
                and "概念超短片" in context
                and re.search(r"5\s*[-–]\s*10\s*分钟", context)
                and any(word in context for word in ("确认", "澄清", "选择", "询问", "问"))
                for context in clarification_contexts
            )
        )

    def test_screenplay_narrative_eight_steps_and_concept_three_step_exception(self) -> None:
        skill = self.read("wally-screenplay-writer/SKILL.md")
        canonical = re.search(
            r"(?ms)^#{2,3} (?:(?:叙事类)?通用八步流程|Workflow)\s*\n(?P<body>.*?)(?=^#{2,3} |^---\s*$|\Z)",
            skill,
        )
        self.assertIsNotNone(canonical)
        parsed_names = []
        for raw_name in re.findall(r"(?m)^[1-8]\.\s+(.+)$", canonical.group("body")):
            bold_name = re.match(r"\*\*(.+?)\*\*", raw_name)
            parsed_names.append(
                bold_name.group(1) if bold_name else raw_name.split(" —", 1)[0].strip()
            )
        canonical_names = tuple(parsed_names)
        expected = (
            "破题与核心动作",
            "梗概草稿",
            "人物深度与弧光",
            "前史与世界观",
            "结构大纲",
            "场景拆解",
            "场景写作",
            "剧本医生",
        )
        self.assertEqual(canonical_names, expected)
        for phrase in (
            "### 八步基础交付合同",
            "目标 → 阻碍 → 结果或失败代价",
            "用户要求改写时同时给可直接替换的改写稿",
        ):
            self.assertIn(phrase, skill)

        short = self.read("wally-screenplay-writer/references/format-short.md")
        short_names = tuple(
            re.findall(r"(?m)^### 第[一二三四五六七八]步：(.+)$", short)
        )
        self.assertEqual(short_names, expected)
        for phrase in (
            "用户要求改写时",
            "可直接替换的改写稿",
            "不回滚范围外已通过的决定",
            "只保留用户本轮范围内的适用项",
            "该步未全部完成时",
        ):
            self.assertIn(phrase, short)

        series = self.read("wally-screenplay-writer/references/format-series.md")
        for heading in (
            "### 阶段 A：季度规划",
            "### 阶段 B：分集大纲",
            "### 阶段 C：逐集剧本（通用八步流程）",
        ):
            self.assertIn(heading, series)
        self.assertIn("配置不是独立审批阶段", series)
        self.assertIn("以下内容只增加剧集单集要求，不替换基础交付", series)
        for phrase in (
            "第二步的单集梗概来自阶段 B",
            "第四步的前史与世界观来自阶段 A",
            "引用并确认对应既有产物即满足八步基础交付",
            "不扩成整集或全季审计",
            "整集场景全部通过后才进入第八步",
        ):
            self.assertIn(phrase, series)

        feature = self.read("wally-screenplay-writer/references/format-feature.md")
        self.assertIn("不要求读取短片格式来补全输出", feature)
        self.assertIn("不扩成全片审计", feature)
        self.assertIn("全部 Sequence 通过后才进入第八步", feature)

        concept = self.read("wally-screenplay-writer/references/format-ultrashort.md")
        what_if_workflow = concept.split("## What-If工作流", 1)[-1].split("# Part B", 1)[0]
        concept_steps = tuple(
            re.findall(r"(?m)^### 第[一二三]步：(.+)$", what_if_workflow)
        )
        self.assertEqual(concept_steps, ("概念锻造", "结构与视听设计", "全片剧本"))
        how_to_workflow = concept.split("## How-to-Tell工作流", 1)[-1].split("# Part C", 1)[0]
        how_to_steps = tuple(
            re.findall(r"(?m)^### 第[一二三]步：(.+)$", how_to_workflow)
        )
        self.assertEqual(how_to_steps, ("形式发现", "结构与视听设计", "全片剧本"))
        self.assertIn("不套用 What-If 的 A-E 结构", how_to_workflow)
        self.assertIn("不强制设置 What-If 式翻转", how_to_workflow)
        self.assertIn(
            "所有“3分钟”与“1-3分钟”检查均改用作品定义中的真实目标时长",
            concept,
        )
        self.assertIn("按作品定义中的真实目标时长等比调整", short)
        self.assertIsNotNone(
            re.search(r"概念超短片.{0,100}三步|三步.{0,100}概念超短片", skill, re.DOTALL)
        )

        tree = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((REPO / "wally-screenplay-writer").rglob("*.md"))
        )
        for phrase in (
            "结构大纲（第三步）",
            "剧本写作（第五步）",
            "场景拆解（第四步）",
            "短片第二步（人物深度）",
            "长片第四步（场景拆解）",
            "长片第三步（结构大纲）",
            "逐集进入六步工作流",
            "完整六步工作流",
        ):
            self.assertNotIn(phrase, tree)

    def test_screenplay_current_stage_work_definition_dialogue_owner_and_single_menu(self) -> None:
        skill = self.read("wally-screenplay-writer/SKILL.md")
        self.assertIn("已有材料", skill)
        self.assertTrue(
            any(
                phrase in skill
                for phrase in ("最新可用", "当前可用", "匹配步骤", "当前阶段")
            )
        )
        for phrase in (
            "自检只覆盖当前步骤、用户本轮范围及其必要上下文",
            "该步尚未完成时",
            "锁定只作用于本轮明确交付的范围",
            "无需完整格式路由的独立定向对白",
        ):
            self.assertIn(phrase, skill)
        core = self.read("wally-screenplay-writer/references/core-methodology.md")
        self.assertIn("这不是内容审批或正式锁定", core)

        self.assertIn("## 作品定义", skill)
        for field in (
            "作品形态：",
            "目标体量：",
            "题材类型：",
            "商业属性 / 内容功能：",
            "叙事方式：",
            "视听定位：",
        ):
            self.assertIn(field, skill)
        self.assertIn("题材类别自动当成视听定位", skill)

        self.assertIn("wally-action-designer", skill)
        self.assertIn("已批准", skill)

        intermediate_menu = (
            "[通过]：接受当前交付并继续\n"
            "[修改]：留在当前步骤修改\n"
            "[自检]：查看当前步骤检查结果"
        )
        final_menu = (
            "[通过并锁定]：完成并锁定当前交付范围\n"
            "[修改]：继续精修当前交付范围\n"
            "[自检]：查看当前步骤检查结果"
        )
        self.assertEqual(skill.count(intermediate_menu), 1)
        self.assertEqual(skill.count(final_menu), 1)
        self.assertNotIn("[通过]：进入下一步", skill)
        self.assertNotIn("[通过并锁定]：完成并锁定当前剧本", skill)

        references = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((REPO / "wally-screenplay-writer/references").glob("*.md"))
        )
        for phrase in (
            "请选择：回复",
            '请回复"通过"',
            "请回复“通过”",
            "进入[自检环节]",
            "[通过并锁定]",
        ):
            self.assertNotIn(phrase, references)

    def test_storyboard_open_input_svg_and_fixed_prompt_routes(self) -> None:
        skill = self.read("wally-storyboard-designer/SKILL.md")
        svg = self.read("wally-storyboard-designer/references/scene-layout-svg-rules.md")
        storyboard_template = self.read(
            "wally-storyboard-designer/templates/storyboard-prompt-template.md"
        )
        shot_table_template = self.read(
            "wally-storyboard-designer/templates/shot-table-prompt-template.md"
        )
        tree = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((REPO / "wally-storyboard-designer").rglob("*.md"))
        )
        for phrase in ("scene-divided", "tables", "images", "partial", "conflicting"):
            self.assertIn(phrase, skill)
        for phrase in (
            "Use explicit source scenes.",
            "Show only the initial state.",
            "Include only active interaction content.",
            "Preserve true top-down geometry.",
        ):
            self.assertIn(phrase, svg)
        self.assertIn(
            "Do not insert a scene title or make any other runtime substitution",
            skill,
        )
        self.assertNotIn("【源场景标题】", storyboard_template)
        self.assertNotIn("【源场景标题】", shot_table_template)
        storyboard_blocks = re.findall(
            r"```text\n(.*?)```", storyboard_template, re.DOTALL
        )
        self.assertEqual(
            [block.strip() for block in storyboard_blocks],
            [
                """【短任务提示词】
你绘制故事板，我来审查。请读取我上传的材料，作为当前故事板生成依据。不要拆分、改写、补全、总结、修复或判断我上传的故事 / 剧本 / 导演脚本等材料；不要新增剧情。
[每次只生成1个版本；我会另行要求下一个版本。每个版本必须是一张独立的故事板图像。]""",
                """【故事板生成模版】
粗略的导演分镜手稿，不是概念艺术：
- 原则：如果你不确定，就画得更少，而不是更多。
- 使用极其简单的 2D 预览草图风格
- 黑色松散的草图线条
- 用红色方框表示镜头(摄像机)取景框
- 箭头表示运动/力/呼吸/方向
- 只有人物/人偶的造型
- 没有面部细节，没有服装细节，没有解剖细节
- 没有纹理，没有阴影，没有抛光的渲染

红色箭头表示"关键"人物动作、运镜(取景框移动)，箭头标记上写简短的中文说明。
把关键过程尽可能详细地画出来。
每一格下方添加简短中文说明，景别、运镜、人物动作。
将每一格的宽高比设为 16:9。""",
            ],
        )
        shot_table_blocks = re.findall(
            r"```text\n(.*?)```", shot_table_template, re.DOTALL
        )
        self.assertEqual(
            [block.strip() for block in shot_table_blocks],
            [
                """【短任务提示词】
你绘制分镜，制作分镜表，我来审查。请读取我上传的导演脚本、静态资产，以导演脚本为分镜的唯一依据，以静态资产为视觉效果的唯一依据。不要拆分、改写、补全、总结、修复或判断我上传的故事 / 剧本 / 导演脚本等材料；不要新增剧情。
[每次只生成1个版本；我会另行要求下一个版本。每个版本必须是一张独立的分镜表图像。]""",
                """【分镜表生成模版】
1.用数字标出镜头序号，不需要文字描述。
2.每一格分镜的宽高比为 16:9。""",
            ],
        )
        self.assertNotIn("READY_FOR_FIXED_STORYBOARD_PROMPT", tree)
        self.assertNotIn("handoff-to-storyboard.md", tree)
        self.assertIsNone(
            re.search(r"(?i)full[- ]chain|WAITING_FOR_|## Output gates", tree)
        )
        self.assertIn("Provide on-demand storyboard-domain functions", skill)
        self.assertIn(
            "Keep the fixed storyboard and shot-table prompt templates verbatim",
            skill,
        )
        director_contract = self.read(
            "wally-storyboard-designer/references/director-script-output-contract.md"
        )
        self.assertIn(
            "Copy the source screenplay's `## 作品定义` block verbatim",
            director_contract,
        )
        self.assertIn("## 作品定义", director_contract)
        self.assertIn("## Targeted Revision", director_contract)
        self.assertIn("## Shot format", director_contract)
        self.assertIn("## 画面内容合同", director_contract)
        self.assertIn(
            "默认只写一个主要主体和一个核心可见动作或状态",
            director_contract,
        )
        self.assertIn("前景、背景和道具都不是必填项", director_contract)
        self.assertIn(
            "把心理、象征、关系解释、剧情意义和镜头理由留在 `任务`",
            director_contract,
        )
        for retired in (
            "references/visual-optimization-rules.md",
            "references/storyboard-design.md",
            "references/storyboard-review.md",
            "references/main-shot-adjudication.md",
            "references/continuity-validation-rules.md",
            "references/ai-video-composition-rules.md",
            "references/storyboard-style-contract.md",
        ):
            self.assertFalse(
                (REPO / "wally-storyboard-designer" / retired).exists(),
                retired,
            )
        for phrase in (
            "visual-optimization-rules.md",
            "storyboard-design.md",
            "storyboard-review.md",
            "main-shot-adjudication.md",
            "continuity-validation-rules.md",
            "ai-video-composition-rules.md",
            "storyboard-style-contract.md",
        ):
            self.assertNotIn(phrase, tree)
        self.assertIn("This skill is the test layer", skill)
        self.assertIn("Do not offer returned-board review as a product", skill)

    def test_helper_routes_storyboard_revisions_to_the_storyboard_specialist(self) -> None:
        helper = self.read("wally-helper/SKILL.md")
        workflow = self.read("wally-helper/references/workflow-guide.md")
        self.assertIn(
            "wally-helper@2026-09-19-v4.3-workflow-guidance",
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
        nine = self.read("wally-static-asset-designer/types/multi-angle.md")
        nine_blocks = re.findall(r"```text\n(.*?)```", nine, re.DOTALL)
        self.assertEqual(
            nine_blocks[0].strip(),
            "参考场景资产图，生成这个XX场景不同角度不同景别的九宫格场景图。",
        )
        self.assertEqual(nine_blocks[0].count("XX"), 1)
        self.assertIn("九宫格是地点多角度参考的默认产物", nine)
        self.assertIn("用户可以直接点名", four)
        self.assertIn("用户选择后再执行", four)
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



if __name__ == "__main__":
    unittest.main()
