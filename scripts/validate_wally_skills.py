#!/usr/bin/env python3
"""Deterministic health checks for the six public Wally skills."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


SKILLS = {
    "wally-helper": "wally-helper@2026-08-18-v4.0-single-scope-bindings-v2",
    "wally-screenplay-writer": "wally-screenplay-writer@2026-08-18-v2.0-four-format-workflow-unification",
    "wally-storyboard-designer": "wally-storyboard-designer@2026-08-19-v3.9-four-rule-layout",
    "wally-static-asset-designer": "wally-static-asset-designer@2026-07-22-v2.6-prop-state-four-grid",
    "wally-action-designer": "wally-action-designer@2026-07-29-v3.9-adaptive-camera-shot-grammar",
    "wally-visual-style-extractor": "wally-visual-style-extractor@2026-07-22-v1.6-boundary-evidence-ownership",
}

README_VERSIONS = {
    "wally-helper": "V4.0",
    "wally-screenplay-writer": "V2.0",
    "wally-storyboard-designer": "V3.9",
    "wally-static-asset-designer": "V2.6",
    "wally-action-designer": "V3.9",
    "wally-visual-style-extractor": "V1.6",
}

FROZEN_HASHES = {
    "wally-helper/templates/route-a-final-prompt.md": "9dc2b8ced5b8b4276c291d1b268ed546f0ee53fe08f2d6fe0e5a8b1d3d3b5188",
    "wally-helper/templates/route-b-final-prompt.md": "96ef1ffed75ab5bfc204f2f2ef4205cfe0e71c13a9671133d152a3e34d089ca6",
    "wally-storyboard-designer/references/storyboard-style-contract.md": "b26e28e64fc7a94430e1ebdf6dadccbeb6df5efd218b301b957ad7db03caf186",
    "wally-storyboard-designer/templates/storyboard-prompt-template.md": "2164c752ddd8086b4afd9429f76814bd358b959970ea06b9199dda98463bdcc4",
    "wally-storyboard-designer/templates/shot-table-prompt-template.md": "a3708139bb78491b415fc40d1cd16b9ca8b349e5bda4c3a0c5736ab66379c1d6",
    "wally-static-asset-designer/templates/preview-prompt.md": "cc1cf4dadc4a29a9f14eeb78244ae57327e8dca3fdcd7699d6d5bdaffba0b145",
    "wally-static-asset-designer/templates/visual-direction-proposal.md": "125f3b1fdb2f56c510bd35a920a5de573f6e06bb04a51f49af2cce3a8e90619d",
    "wally-static-asset-designer/types/multi-angle.md": "90203837a5ec2dd836f7fa6bd04c4f73b8f0b12930a990160510d4f7f439cfa7",
}

CANONICAL_STYLE_HASH = "7b09eff252af0861472ad7111eb1ff887950f22c345bdd39b0a3c0f885dc630d"
IGNORED_NAMES = {".DS_Store", ".git", "__pycache__"}
RETIRED_UNIT_FRAGMENT = "".join(("s", "e", "g"))
TEXT_SUFFIXES = {
    ".body",
    ".cfg",
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".prompt",
    ".py",
    ".sh",
    ".svg",
    ".toml",
    ".ts",
    ".tsv",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
TEXT_FILENAMES = {".gitignore", "LICENSE"}
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CODE_MD = re.compile(r"`([^`\n]+\.md(?:#[^`\n]+)?)`")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def skill_root(candidate: Path) -> Path:
    for nested in (
        candidate,
        candidate / "repository",
        candidate / "live",
        candidate / "repository" / "skills",
        candidate / "skills",
    ):
        if all((nested / name).is_dir() for name in SKILLS):
            return nested
    raise FileNotFoundError(f"cannot locate all six skill directories under {candidate}")


def iter_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in IGNORED_NAMES for part in path.parts) or path.suffix == ".pyc":
            continue
        yield path


def iter_skill_files(root: Path):
    """Yield only the six managed skill trees from a collection or repo root."""
    for name in SKILLS:
        yield from iter_files(root / name)


def tree_hash(root: Path) -> str:
    lines = [f"{sha256(path)}  {path.relative_to(root).as_posix()}\n" for path in iter_files(root)]
    return hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()


def parse_frontmatter(path: Path, errors: list[str]) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(?P<frontmatter>.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(errors, f"{path}: frontmatter requires exact opening and closing delimiters")
        return "", ""
    frontmatter = match.group("frontmatter")
    name_match = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", frontmatter)
    desc_match = re.search(r"(?m)^description:\s*(\S.*)$", frontmatter)
    if not name_match or not desc_match or not desc_match.group(1).strip(" \"'"):
        fail(errors, f"{path}: frontmatter requires non-empty name and description")
        return "", ""
    return name_match.group(1).strip(), frontmatter


def check_links(skills: Path, errors: list[str]) -> None:
    for path in iter_skill_files(skills):
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        if any(line.rstrip("\n").endswith((" ", "\t")) for line in text.splitlines(keepends=True)):
            fail(errors, f"{path}: trailing whitespace")
        candidates = [m.group(1) for m in MARKDOWN_LINK.finditer(text)]
        candidates.extend(m.group(1) for m in CODE_MD.finditer(text))
        for raw in candidates:
            raw = raw.split("#", 1)[0].strip()
            if not raw or raw.startswith(("http://", "https://", "mailto:", "/")):
                continue
            if any(token in raw for token in ("<", ">", "*", "[", "]")):
                continue
            relative = path.relative_to(skills)
            owner = (
                skills / relative.parts[0]
                if relative.parts[0] in SKILLS
                else skills
            )
            possible = (
                path.parent / raw,
                owner / raw,
                owner / "references" / raw,
                owner / "templates" / raw,
                owner / "types" / raw,
            )
            resolved_owner = owner.resolve()
            valid = False
            for target in possible:
                resolved = target.resolve()
                if resolved == resolved_owner or resolved_owner in resolved.parents:
                    valid = valid or resolved.exists()
            if not valid:
                fail(errors, f"{path}: missing reference {raw}")


def check_public_safety(root: Path, errors: list[str], *, skills_only: bool = False) -> None:
    # Build these tokens from harmless pieces so the validator can scan its own
    # source without treating the policy definitions as leaked content.
    forbidden = (
        "/" + "Users" + "/",
        "BEGIN " + "OPENSSH PRIVATE KEY",
        "BEGIN " + "PRIVATE KEY",
        ".codex/" + "sessions/",
        "build-perfect-" + "ai-video-skill",
    )
    files = iter_skill_files(root) if skills_only else iter_files(root)
    for path in files:
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in TEXT_FILENAMES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in forbidden:
            if token in text:
                fail(errors, f"{path}: public-safety token {token!r}")


def check_retired_unit_absent(
    root: Path, errors: list[str], *, skills_only: bool = False
) -> None:
    """Prevent the removed intermediate story-unit vocabulary from returning."""
    files = iter_skill_files(root) if skills_only else iter_files(root)
    for path in files:
        relative = path.relative_to(root).as_posix()
        if RETIRED_UNIT_FRAGMENT in relative.casefold():
            fail(errors, f"retired story-unit token remains in path: {relative}")
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in TEXT_FILENAMES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if RETIRED_UNIT_FRAGMENT in text.casefold():
            fail(errors, f"retired story-unit token remains in file: {relative}")


def check_frozen(skills: Path, errors: list[str]) -> None:
    for relative, expected in FROZEN_HASHES.items():
        path = skills / relative
        if not path.is_file():
            fail(errors, f"missing frozen surface {relative}")
        elif sha256(path) != expected:
            fail(errors, f"frozen surface changed: {relative}")

    style = (skills / "wally-storyboard-designer/references/storyboard-style-contract.md").read_text(encoding="utf-8")
    match = re.search(r"```text\n(.*?)```", style, re.DOTALL)
    if not match:
        fail(errors, "canonical storyboard style block not found")
    else:
        block_hash = hashlib.sha256((match.group(1)).encode("utf-8")).hexdigest()
        if block_hash != CANONICAL_STYLE_HASH:
            fail(errors, "canonical storyboard 15-line block changed")


def check_module_contracts(skills: Path, errors: list[str]) -> None:
    helper = (skills / "wally-helper/SKILL.md").read_text(encoding="utf-8")
    helper_contract = (skills / "wally-helper/references/artifact-compatibility.md").read_text(encoding="utf-8")
    helper_workflow = (skills / "wally-helper/references/workflow-guide.md").read_text(encoding="utf-8")
    helper_parser = (skills / "wally-helper/scripts/prompt_validation_common.py").read_text(encoding="utf-8")
    for relative in (
        "wally-helper/scripts/prompt_validation_common.py",
        "wally-helper/scripts/validate_route_a_prompt.py",
        "wally-helper/scripts/validate_route_b_prompt.py",
    ):
        if not (skills / relative).is_file():
            fail(errors, f"missing Helper validator {relative}")
    if "default|music|silence" not in helper and "default / music / silence" not in helper:
        fail(errors, "Helper does not declare all three Audio modes")
    if "Confirm that `Audio: 无BGM。` exists" in helper_contract:
        fail(errors, "Helper retains unconditional no-BGM compatibility rule")
    if "hand those revisions to `wally-storyboard-designer` for integration" not in helper_workflow:
        fail(errors, "Helper does not hand storyboard-exposed shot revisions to Storyboard Designer")
    if "When the updated director script returns" not in helper_workflow:
        fail(errors, "Helper can approve before the specialist returns an updated director script")
    if "Do not author or revise any specialist product." not in helper:
        fail(errors, "Helper specialist-product boundary is missing")
    if "integrate every named shot-design revision" in helper_workflow:
        fail(errors, "Helper still claims specialist shot-design revision work")
    for phrase in (
        "exactly one current generation scope",
        "wally-reference-bindings/v2",
        "all five entry fields",
    ):
        if phrase not in f"{helper}\n{helper_contract}\n{helper_parser}":
            fail(errors, f"Helper single-scope binding contract is missing: {phrase}")

    screenplay_root = skills / "wally-screenplay-writer"
    screenplay = (screenplay_root / "SKILL.md").read_text(encoding="utf-8")
    screenplay_frontmatter = re.match(r"\A---\n(.*?)\n---\n", screenplay, re.DOTALL)
    frontmatter_text = screenplay_frontmatter.group(1) if screenplay_frontmatter else ""
    for trigger in ("原创对白", "台词写作", "对白改写", "对白诊断"):
        if trigger not in frontmatter_text:
            fail(errors, f"Screenplay frontmatter is missing dialogue trigger {trigger}")

    four_format_patterns = {
        "1-3 minute concept ultrashort": (
            r"(?:概念超短片.{0,40}1\s*[-–]\s*3\s*分钟|"
            r"1\s*[-–]\s*3\s*分钟.{0,40}概念超短片)"
        ),
        "5-10 minute narrative short": (
            r"(?:叙事短片.{0,40}5\s*[-–]\s*10\s*分钟|"
            r"5\s*[-–]\s*10\s*分钟.{0,40}叙事短片)"
        ),
        "feature": r"(?:长片.{0,20}90\s*分钟|90\s*分钟.{0,20}长片)",
        "series": r"(?:剧集.{0,40}(?:连续剧|多集内容)|多集剧集)",
    }
    if not any(label in screenplay for label in ("四格式", "四种格式")):
        fail(errors, "Screenplay does not declare the four-format contract")
    for label, pattern in four_format_patterns.items():
        if not re.search(pattern, screenplay, re.DOTALL):
            fail(errors, f"Screenplay four-format route is missing: {label}")
    for phrase in (
        "四种格式是创作方法路由",
        "实际体量偏离默认值",
        "已有材料的定向对白",
    ):
        if phrase not in screenplay:
            fail(errors, f"Screenplay four-format scaling or scoped-task rule is missing: {phrase}")

    screenplay_markdown = [
        path.read_text(encoding="utf-8")
        for path in iter_files(screenplay_root)
        if path.suffix == ".md"
    ]
    all_screenplay = "\n".join(screenplay_markdown)
    if "叙事超短片" in all_screenplay:
        fail(errors, "Screenplay active tree retains the retired narrative-ultrashort route")

    workflow_match = re.search(
        r"(?ms)^#{2,3} (?:(?:叙事类)?通用八步流程|Workflow)\s*\n(?P<body>.*?)(?=^#{2,3} |^---\s*$|\Z)",
        screenplay,
    )
    expected_workflow = (
        "破题与核心动作",
        "梗概草稿",
        "人物深度与弧光",
        "前史与世界观",
        "结构大纲",
        "场景拆解",
        "场景写作",
        "剧本医生",
    )
    workflow_names: tuple[str, ...] = ()
    if workflow_match:
        parsed_names: list[str] = []
        for raw_name in re.findall(r"(?m)^[1-8]\.\s+(.+)$", workflow_match.group("body")):
            bold_name = re.match(r"\*\*(.+?)\*\*", raw_name)
            parsed_names.append(
                bold_name.group(1) if bold_name else raw_name.split(" —", 1)[0].strip()
            )
        workflow_names = tuple(parsed_names)
    if workflow_names != expected_workflow:
        fail(errors, "Screenplay narrative eight-step source of truth is missing or reordered")
    for phrase in (
        "### 八步基础交付合同",
        "目标 → 阻碍 → 结果或失败代价",
        "用户要求改写时同时给可直接替换的改写稿",
    ):
        if phrase not in screenplay:
            fail(errors, f"Screenplay narrative base deliverable contract is missing: {phrase}")

    concept_format = (screenplay_root / "references/format-ultrashort.md").read_text(encoding="utf-8")
    concept_workflow = concept_format.split("## What-If工作流", 1)[-1].split("# Part B", 1)[0]
    concept_steps = tuple(
        re.findall(r"(?m)^### 第[一二三]步：(.+)$", concept_workflow)
    )
    if concept_steps != ("概念锻造", "结构与视听设计", "全片剧本"):
        fail(errors, "Screenplay concept-ultrashort three-step workflow is missing or reordered")
    how_to_workflow = concept_format.split("## How-to-Tell工作流", 1)[-1].split("# Part C", 1)[0]
    how_to_steps = tuple(
        re.findall(r"(?m)^### 第[一二三]步：(.+)$", how_to_workflow)
    )
    if how_to_steps != ("形式发现", "结构与视听设计", "全片剧本"):
        fail(errors, "Screenplay How-to-Tell three-step workflow is missing or reordered")
    for phrase in (
        "不套用 What-If 的 A-E 结构",
        "不强制设置 What-If 式翻转",
    ):
        if phrase not in how_to_workflow:
            fail(errors, f"Screenplay How-to-Tell retains a What-If conflict: {phrase}")
    if "所有“3分钟”与“1-3分钟”检查均改用作品定义中的真实目标时长" not in concept_format:
        fail(errors, "Screenplay concept route declares scaling but its reference retains hard duration checks")
    if not re.search(r"概念超短片.{0,100}三步|三步.{0,100}概念超短片", screenplay, re.DOTALL):
        fail(errors, "Screenplay entry does not declare the concept-ultrashort three-step exception")

    intermediate_menu = "\n".join(
        (
            "[通过]：接受当前交付并继续",
            "[修改]：留在当前步骤修改",
            "[自检]：查看当前步骤检查结果",
        )
    )
    final_menu = "\n".join(
        (
            "[通过并锁定]：完成并锁定当前交付范围",
            "[修改]：继续精修当前交付范围",
            "[自检]：查看当前步骤检查结果",
        )
    )
    if screenplay.count(intermediate_menu) != 1:
        fail(errors, "Screenplay must define the exact intermediate approval menu once")
    if screenplay.count(final_menu) != 1:
        fail(errors, "Screenplay must define the exact final approval menu once")

    stale_phrases = (
        "结构大纲（第三步）", "剧本写作（第五步）", "场景拆解（第四步）",
        "短片第二步（人物深度）", "长片第四步（场景拆解）",
        "长片第三步（结构大纲）", "逐集进入六步工作流",
        "完整六步工作流", "[通过]：进入下一步",
        "[通过并锁定]：完成并锁定当前剧本",
    )
    for phrase in stale_phrases:
        if phrase in all_screenplay:
            fail(errors, f"Screenplay stale workflow phrase: {phrase}")
    screenplay_references = "\n".join(
        path.read_text(encoding="utf-8")
        for path in iter_files(screenplay_root / "references")
        if path.suffix == ".md"
    )
    for phrase in (
        "请选择：回复",
        '请回复"通过"',
        "请回复“通过”",
        "进入[自检环节]",
        "[通过并锁定]",
    ):
        if phrase in screenplay_references:
            fail(errors, f"Screenplay format reference retains a local approval-menu variant: {phrase}")

    short_format = (screenplay_root / "references/format-short.md").read_text(encoding="utf-8")
    short_steps = tuple(
        re.findall(r"(?m)^### 第[一二三四五六七八]步：(.+)$", short_format)
    )
    if short_steps != expected_workflow:
        fail(errors, "Screenplay short-format headings do not match the narrative eight-step source")
    if not all(
        phrase in short_format
        for phrase in (
            "用户要求改写时",
            "可直接替换的改写稿",
            "不回滚范围外已通过的决定",
            "只保留用户本轮范围内的适用项",
            "该步未全部完成时",
        )
    ):
        fail(errors, "Screenplay doctor does not deliver scoped, directly usable rewrites")
    if "按作品定义中的真实目标时长等比调整" not in short_format:
        fail(errors, "Screenplay short route declares scaling but its reference lacks the scale rule")

    series_format = (screenplay_root / "references/format-series.md").read_text(encoding="utf-8")
    for heading in (
        "### 阶段 A：季度规划",
        "### 阶段 B：分集大纲",
        "### 阶段 C：逐集剧本（通用八步流程）",
    ):
        if heading not in series_format:
            fail(errors, f"Screenplay series workflow is missing: {heading}")
    if "配置不是独立审批阶段" not in series_format:
        fail(errors, "Screenplay series configuration creates an ambiguous extra gate")
    feature_format = (screenplay_root / "references/format-feature.md").read_text(encoding="utf-8")
    if "不要求读取短片格式来补全输出" not in feature_format:
        fail(errors, "Screenplay feature workflow has an implicit short-format dependency")
    if "以下内容只增加剧集单集要求，不替换基础交付" not in series_format:
        fail(errors, "Screenplay series episode workflow does not inherit the base deliverables")
    for phrase in (
        "第二步的单集梗概来自阶段 B",
        "第四步的前史与世界观来自阶段 A",
        "引用并确认对应既有产物即满足八步基础交付",
        "不扩成整集或全季审计",
        "整集场景全部通过后才进入第八步",
    ):
        if phrase not in series_format:
            fail(errors, f"Screenplay series overlay conflict remains: {phrase}")
    for phrase in (
        "不扩成全片审计",
        "全部 Sequence 通过后才进入第八步",
    ):
        if phrase not in feature_format:
            fail(errors, f"Screenplay feature overlay conflict remains: {phrase}")

    if "已有材料" not in screenplay or not any(
        phrase in screenplay for phrase in ("最新可用", "当前可用", "匹配步骤", "当前阶段")
    ):
        fail(errors, "Screenplay does not resume supplied material from its current usable stage")
    for phrase in (
        "自检只覆盖当前步骤、用户本轮范围及其必要上下文",
        "该步尚未完成时",
        "锁定只作用于本轮明确交付的范围",
        "无需完整格式路由的独立定向对白",
    ):
        if phrase not in screenplay:
            fail(errors, f"Screenplay scoped continuation contract is missing: {phrase}")
    if "这不是内容审批或正式锁定" not in (
        screenplay_root / "references/core-methodology.md"
    ).read_text(encoding="utf-8"):
        fail(errors, "Screenplay memory checkpoint is ambiguous with approval locking")

    work_definition_fields = (
        "作品形态：",
        "目标体量：",
        "题材类型：",
        "商业属性 / 内容功能：",
        "叙事方式：",
        "视听定位：",
    )
    if "## 作品定义" not in screenplay:
        fail(errors, "Screenplay work-definition block is missing")
    for field in work_definition_fields:
        if field not in screenplay:
            fail(errors, f"Screenplay work-definition field is missing: {field}")
    if "题材类别自动当成视听定位" not in screenplay:
        fail(errors, "Screenplay work definition permits unsupported visual-style inference")

    if not all(token in screenplay for token in ("wally-action-designer", "已批准")):
        fail(errors, "Screenplay dialogue ownership boundary with Action Designer is missing")

    clarification_contexts = [
        screenplay[max(0, match.start() - 100):match.end() + 320]
        for match in re.finditer("完整叙事", screenplay)
    ]
    if not any(
        re.search(r"1\s*[-–]\s*3\s*分钟", context)
        and re.search(r"3\s*[-–]\s*5\s*分钟", context)
        and "概念超短片" in context
        and re.search(r"5\s*[-–]\s*10\s*分钟", context)
        and any(word in context for word in ("确认", "澄清", "选择", "询问", "问"))
        for context in clarification_contexts
    ):
        fail(errors, "Screenplay lacks the 1-3 / 3-5 minute narrative clarification rule")

    action = (skills / "wally-action-designer/SKILL.md").read_text(encoding="utf-8")
    action_craft = (skills / "wally-action-designer/references/craft.md").read_text(encoding="utf-8")
    if "已批准台词" not in action:
        fail(errors, "Action frontmatter/body does not limit dialogue to approved wording")
    if "Propose new wording" in action_craft:
        fail(errors, "Action still proposes original dialogue wording")
    for phrase in (
        "compose Camera and each Shot from only the conditional controls the task needs",
        "Capture physics",
        "Fit the action, camera response, contact, settling, dialogue, and listener registration",
    ):
        if phrase not in f"{action}\n{action_craft}":
            fail(errors, f"Action V3.9 adaptive camera/Shot contract is missing: {phrase}")

    storyboard_root = skills / "wally-storyboard-designer"
    storyboard = (storyboard_root / "SKILL.md").read_text(encoding="utf-8")
    storyboard_tree = "\n".join(path.read_text(encoding="utf-8") for path in iter_files(storyboard_root) if path.suffix == ".md")
    if "handoff-to-storyboard.md" in storyboard_tree:
        fail(errors, "Storyboard retains dead handoff reference")
    if "READY_FOR_FIXED_STORYBOARD_PROMPT" in storyboard_tree:
        fail(errors, "Storyboard retains obsolete READY gate")
    if "storyboard-style-contract.md" not in storyboard:
        fail(errors, "Storyboard entry does not load canonical style contract")
    for token in ("scene-divided", "tables", "images", "partial", "conflicting", "mixture"):
        if token not in storyboard:
            fail(errors, f"Storyboard open-input contract is missing {token!r}")
    svg_rules = (storyboard_root / "references/scene-layout-svg-rules.md").read_text(encoding="utf-8")
    for phrase in (
        "Use explicit source scenes.",
        "Show only the initial state.",
        "Include only active interaction content.",
        "Preserve true top-down geometry.",
        "name only what is missing and stop",
    ):
        if phrase not in svg_rules:
            fail(errors, f"Storyboard Scene SVG route is missing: {phrase}")
    if re.search(r"(?i)full[- ]chain|WAITING_FOR_|## Output gates", storyboard_tree):
        fail(errors, "Storyboard retains a cross-module lifecycle or approval gate")
    for phrase in (
        "Provide on-demand storyboard-domain functions",
        "Preserve the latest explicit or approved `作品定义`",
        "Copy the source screenplay's `## 作品定义` block verbatim",
        "Keep the fixed storyboard and shot-table prompt templates verbatim",
    ):
        if phrase not in storyboard:
            fail(errors, f"Storyboard work-definition inheritance is missing: {phrase}")
    director_contract = (storyboard_root / "references/director-script-output-contract.md").read_text(encoding="utf-8")
    for phrase in ("## 作品定义", "## Targeted Revision", "## Shot format"):
        if phrase not in director_contract:
            fail(errors, f"Storyboard director-script contract is missing: {phrase}")
    for retired in (
        "references/visual-optimization-rules.md",
        "references/storyboard-design.md",
        "references/storyboard-review.md",
        "references/main-shot-adjudication.md",
        "references/continuity-validation-rules.md",
        "references/ai-video-composition-rules.md",
    ):
        if (storyboard_root / retired).exists():
            fail(errors, f"Storyboard retains retired guide {retired}")
    for phrase in ("visual-optimization-rules.md", "storyboard-design.md", "storyboard-review.md", "main-shot-adjudication.md", "continuity-validation-rules.md", "ai-video-composition-rules.md"):
        if phrase in storyboard_tree:
            fail(errors, f"Storyboard still references retired guide {phrase}")
    for phrase in (
        "This skill is the test layer",
        "### 分镜脚本 (processed director script)",
        "Do not offer returned-board review as a product",
    ):
        if phrase not in storyboard:
            fail(errors, f"Storyboard test-layer contract is missing: {phrase}")
    for phrase in (
        "Leave `【源场景标题】` unchanged for a generic reusable prompt",
        "exact original source scene heading",
        "Never split, merge, rename, normalize, or renumber",
        "output only its stored, labeled",
        "There is no rough/formal grade",
    ):
        if phrase not in storyboard:
            fail(errors, f"Storyboard fixed-prompt contract is missing: {phrase}")

    four_grid = skills / "wally-static-asset-designer/types/multi-angle-2x2.md"
    prop_state = skills / "wally-static-asset-designer/types/pxx-state.md"
    if not four_grid.is_file():
        fail(errors, "Static 2x2 fixed prompt is missing")
    else:
        four_text = four_grid.read_text(encoding="utf-8")
        blocks = re.findall(r"```text\n(.*?)```", four_text, re.DOTALL)
        fixed = "参考场景资产图，生成这个XX场景不同角度不同景别的2×2四宫格场景图。"
        if not blocks or blocks[0].strip() != fixed or blocks[0].count("XX") != 1:
            fail(errors, "Static 2x2 fixed block must contain only the exact one-XX sentence")
        for phrase in ("九宫格", "用户可以直接点名", "无法保持场景身份", "不附标题"):
            if phrase not in four_text:
                fail(errors, f"Static 2x2 routing/output contract is missing: {phrase}")
    static_skill = (skills / "wally-static-asset-designer/SKILL.md").read_text(encoding="utf-8")
    for phrase in ("This nine-grid remains the default", "explicitly requests a 2x2 four-grid", "do not append the fallback prompt"):
        if phrase not in static_skill:
            fail(errors, f"Static nine-grid/fallback contract is missing: {phrase}")
    if not prop_state.is_file():
        fail(errors, "Static Pxx-state contract is missing")
    else:
        state_text = prop_state.read_text(encoding="utf-8")
        labels = (
            "**基础道具参考**", "**目标状态**", "**状态变化**",
            "**保持不变**", "**材质与物理表现**", "**状态一致性**",
        )
        positions = [state_text.find(label) for label in labels]
        if any(position < 0 for position in positions) or positions != sorted(positions):
            fail(errors, "Static Pxx-state core fields are missing or out of order")
        for phrase in (
            "一个已批准基础 `Pxx`", "缺图时指出缺失并停止",
            "只有用户明确要求草案", "不生成基准状态或前后对比",
            "同一个目标状态",
        ):
            if phrase not in state_text:
                fail(errors, f"Static Pxx-state contract is missing: {phrase}")

    visual_skill = (skills / "wally-visual-style-extractor/SKILL.md").read_text(encoding="utf-8")
    visual_templates = (skills / "wally-visual-style-extractor/references/style-extraction-templates.md").read_text(encoding="utf-8")
    if "## Boundaries" not in visual_skill:
        fail(errors, "Visual Style boundaries section is missing")
    for phrase in (
        "Do not design static-asset identities",
        "Do not design a shot sequence",
        "dialogue, or audio",
        "final image-to-video or text-to-video prompts",
    ):
        if phrase not in visual_skill:
            fail(errors, f"Visual Style boundary is missing: {phrase}")
    if "does not authorize filling those three JSON keys" not in visual_skill:
        fail(errors, "Visual Style does not protect subject/scene/camera JSON ownership")
    analysis_section = visual_templates.split("## Analysis Card", 1)[-1].split("## Three-Stage Brief", 1)[0]
    analysis_blocks = re.findall(r"```text\n(.*?)```", analysis_section, re.DOTALL)
    if not analysis_blocks or len(re.findall(r"(?m)^Evidence strength:\s*$", analysis_blocks[0])) != 1:
        fail(errors, "Analysis Card must have exactly one top-level Evidence strength owner")
    for phrase in (
        "Canonical match: none confirmed",
        "direct source URL or a precise offline source note",
        "state match strength",
        '"term": "<canonical or supporting established term>"',
        '"camera": "<user-supplied camera value, or reusable placeholder>"',
    ):
        if phrase not in visual_templates and phrase not in visual_skill:
            fail(errors, f"Visual Style evidence/JSON contract is missing: {phrase}")
    if "repeated style tendency" in visual_templates:
        fail(errors, "Visual Style JSON camera still permits inferred style tendency")


def check_machine_files(skills: Path, errors: list[str]) -> None:
    for path in iter_skill_files(skills):
        try:
            if path.suffix == ".json":
                json.loads(path.read_text(encoding="utf-8"))
            elif path.suffix == ".svg":
                ET.parse(path)
            elif path.suffix == ".py":
                compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except Exception as exc:  # noqa: BLE001 - aggregate all deterministic failures
            fail(errors, f"{path}: {exc}")


def check_repository_metadata(root: Path, errors: list[str]) -> None:
    """Check public-repository declarations when the supplied root is a repo."""
    readme_path = root / "README.md"
    changelog_path = root / "CHANGELOG.md"
    workflow_path = root / ".github/workflows/validate-wally-skills.yml"
    test_path = root / "tests/test_wally_contracts.py"
    fixtures = root / "tests/fixtures"
    if not readme_path.is_file():
        return

    readme = readme_path.read_text(encoding="utf-8")
    changelog = changelog_path.read_text(encoding="utf-8") if changelog_path.is_file() else ""
    for name, version in README_VERSIONS.items():
        if f"| `{name}` | {version} |" not in readme:
            fail(errors, f"README version table is inconsistent for {name} {version}")
    if "六项 skill 完成协调健康修复" not in changelog:
        fail(errors, "CHANGELOG lacks the coordinated 2026-07-22 release entry")
    if "Helper V3.11、Screenplay V1.7 与 Storyboard V1.19" not in changelog:
        fail(errors, "CHANGELOG lacks the coordinated 2026-07-28 contract repair entry")
    if "Helper 升级为 V3.12" not in changelog or ".agents/skills" not in changelog:
        fail(errors, "CHANGELOG lacks the 2026-08-03 Wally project-scope cutover entry")
    if "Helper 升级为 V4.0" not in changelog or "Storyboard 升级为 V2.1" not in changelog:
        fail(errors, "CHANGELOG lacks the 2026-08-18 source-scene migration entry")
    if "Storyboard 升级为 V3.0" not in changelog or "测试层" not in changelog:
        fail(errors, "CHANGELOG lacks the 2026-08-18 Storyboard V3.0 test-layer entry")
    if "Storyboard 升级为 V3.9" not in changelog or "四条规则" not in changelog:
        fail(errors, "CHANGELOG lacks the 2026-08-19 Storyboard V3.9 four-rule layout entry")
    if "Screenplay 升级为 V2.0" not in changelog or "正式收敛为四种格式" not in changelog:
        fail(errors, "CHANGELOG lacks the 2026-08-18 Screenplay V2.0 entry")
    if not workflow_path.is_file() or "validate-wally-skills:" not in workflow_path.read_text(encoding="utf-8"):
        fail(errors, "validate-wally-skills GitHub Actions job is missing")
    if not test_path.is_file():
        fail(errors, "anonymous contract unittest module is missing")
    if not fixtures.is_dir() or not any(path.is_file() for path in fixtures.rglob("*")):
        fail(errors, "anonymous contract fixtures are missing")


def compare_trees(left: Path, right: Path, label: str, errors: list[str]) -> None:
    for name in SKILLS:
        a = tree_hash(left / name)
        b = tree_hash(right / name)
        if a != b:
            fail(errors, f"{label}: {name} tree mismatch ({a} != {b})")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--snapshot-root", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    supplied_root = args.skills_root.resolve()
    skills = skill_root(supplied_root)

    for directory, version in SKILLS.items():
        root = skills / directory
        skill_file = root / "SKILL.md"
        if not skill_file.is_file():
            fail(errors, f"{directory}: missing SKILL.md")
            continue
        name, _frontmatter = parse_frontmatter(skill_file, errors)
        if name != directory:
            fail(errors, f"{directory}: frontmatter name is {name!r}")
        if version not in skill_file.read_text(encoding="utf-8"):
            fail(errors, f"{directory}: target version {version} not found")

    check_links(skills, errors)
    if (supplied_root / "README.md").is_file():
        check_retired_unit_absent(supplied_root, errors)
    else:
        check_retired_unit_absent(skills, errors, skills_only=True)
    check_frozen(skills, errors)
    check_module_contracts(skills, errors)
    check_machine_files(skills, errors)
    check_repository_metadata(supplied_root, errors)

    if args.repo_root:
        compare_trees(skills, skill_root(args.repo_root.resolve()), "repository", errors)
    if args.snapshot_root:
        compare_trees(skills, skill_root(args.snapshot_root.resolve()), "snapshot", errors)

    if args.repo_root:
        check_public_safety(args.repo_root.resolve(), errors)
    elif (supplied_root / "README.md").is_file():
        check_public_safety(supplied_root, errors)
    else:
        check_public_safety(skills, errors, skills_only=True)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAIL: {len(errors)} issue(s)", file=sys.stderr)
        return 1

    print(f"PASS: six Wally skills healthy at {skills}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
