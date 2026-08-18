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
    "wally-screenplay-writer": "wally-screenplay-writer@2026-07-28-v1.7-narrative-ultrashort-arc-closure",
    "wally-storyboard-designer": "wally-storyboard-designer@2026-08-18-v2.1-adversarial-main-shot",
    "wally-static-asset-designer": "wally-static-asset-designer@2026-07-22-v2.6-prop-state-four-grid",
    "wally-action-designer": "wally-action-designer@2026-07-29-v3.9-adaptive-camera-shot-grammar",
    "wally-visual-style-extractor": "wally-visual-style-extractor@2026-07-22-v1.6-boundary-evidence-ownership",
}

README_VERSIONS = {
    "wally-helper": "V4.0",
    "wally-screenplay-writer": "V1.7",
    "wally-storyboard-designer": "V2.1",
    "wally-static-asset-designer": "V2.6",
    "wally-action-designer": "V3.9",
    "wally-visual-style-extractor": "V1.6",
}

FROZEN_HASHES = {
    "wally-helper/templates/route-a-final-prompt.md": "9dc2b8ced5b8b4276c291d1b268ed546f0ee53fe08f2d6fe0e5a8b1d3d3b5188",
    "wally-helper/templates/route-b-final-prompt.md": "96ef1ffed75ab5bfc204f2f2ef4205cfe0e71c13a9671133d152a3e34d089ca6",
    "wally-storyboard-designer/references/storyboard-style-contract.md": "b2daf11298d50845ae2644f7444bd992078ae55df8edf66b4aa1d95a7fd77d69",
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
    workflow_match = re.search(r"## Workflow\n\n(.*?)\n\n", screenplay, re.DOTALL)
    expected_workflow = "\n".join(
        (
            "1. 破题与核心动作",
            "2. 梗概草稿",
            "3. 人物深度与弧光",
            "4. 前史与世界观",
            "5. 结构大纲",
            "6. 场景拆解",
            "7. 场景写作",
            "8. 剧本医生",
        )
    )
    if not workflow_match or workflow_match.group(1).strip() != expected_workflow:
        fail(errors, "Screenplay eight-step source of truth is missing or reordered")
    for menu_label in ("[通过]", "[修改]", "[自检]", "[通过并锁定]"):
        if menu_label not in screenplay:
            fail(errors, f"Screenplay unified approval menu is missing {menu_label}")
    stale_phrases = (
        "结构大纲（第三步）", "剧本写作（第五步）", "场景拆解（第四步）",
        "短片第二步（人物深度）", "长片第四步（场景拆解）",
        "长片第三步（结构大纲）", "逐集进入六步工作流",
    )
    all_screenplay = "\n".join(path.read_text(encoding="utf-8") for path in iter_files(screenplay_root) if path.suffix == ".md")
    for phrase in stale_phrases:
        if phrase in all_screenplay:
            fail(errors, f"Screenplay stale workflow phrase: {phrase}")
    screenplay_references = "\n".join(
        path.read_text(encoding="utf-8")
        for path in iter_files(screenplay_root / "references")
        if path.suffix == ".md"
    )
    if "请选择：回复" in screenplay_references or "通过并锁定" in screenplay_references:
        fail(errors, "Screenplay format reference retains a local approval-menu variant")
    short_format = (screenplay_root / "references/format-short.md").read_text(encoding="utf-8")
    for phrase in (
        "叙事超短片聚焦1-2个中心人物，不强制完整Want/Need/Arc",
        "叙事超短片至少呈现一次可见的选择、让步或关系变化",
        "叙事短片完成一次A→B变化",
    ):
        if phrase not in short_format:
            fail(errors, f"Screenplay narrative-ultrashort scaling contract is missing: {phrase}")
    if "## 作品定义" not in screenplay or "Define the work" not in screenplay:
        fail(errors, "Screenplay work-definition contract is missing")

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
        "Create one SVG per supplied scene immediately",
        "do not require another storyboard-domain product first",
        "name only the missing facts and stop",
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
    storyboard_design = (storyboard_root / "references/storyboard-design.md").read_text(encoding="utf-8")
    for phrase in ("状态：DIRECTOR_SCRIPT_READY", "## 作品定义"):
        if phrase not in director_contract:
            fail(errors, f"Storyboard director-script contract is missing: {phrase}")
    for phrase in ("## Carry the work definition", "Begin every complete storyboard or shot-sequence design"):
        if phrase not in storyboard_design:
            fail(errors, f"Storyboard design work-definition carrier is missing: {phrase}")
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
