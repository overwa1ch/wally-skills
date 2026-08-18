#!/usr/bin/env python3
"""Validate a finished Route B prompt against bindings and shared contracts."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

from prompt_validation_common import (
    AUDIO_MODES,
    Binding,
    ExpectedBinding,
    director_reference_errors,
    execution_scope,
    identity_transform_errors,
    load_binding_schema,
    normalize_declared_identities,
    parse_bindings,
    placeholder_errors,
    schema_binding_errors,
    validate_audio,
)


SECTIONS = re.compile(
    r"\AAsset List:\s*\n(?P<assets>.*?)\n\s*\nPrompt:\s*\n(?P<prompt>.*)"
    r"\n\s*\nConstraints:\s*\n(?P<constraints>.*)\Z",
    re.DOTALL,
)
INVALID_IDENTITY_NAMES = {
    "人物三视图",
    "场景九宫格",
    "对比产品",
    "自家产品",
    "人物参考资产",
    "场景参考资产",
    "对比产品参考资产",
    "自家产品参考资产",
}
ASSET_FORM_SUFFIX = re.compile(
    r"(?:三视图|九宫格|四宫格|参考图|参考资产|素材图|资产图|人物图|场景图|产品图)$"
)
STORYBOARD_DESCRIPTION = re.compile(r"故事板|storyboard", re.IGNORECASE)
AVOID_HEADING = re.compile(r"(?m)^(?:\*{0,2}Avoid:\*{0,2}\s*|避免：\s*)")
EMPTY_AVOID_CONSTRAINT = re.compile(r"(?m)^禁止出现：\s*$")
GENERIC_ALIAS_TOKENS = ("对比产品", "自家产品", "折叠体", "商品", "人物", "产品")
ALIAS_EXEMPT_TERMS = ("产品演示", "产品反转", "纸就产品", "成品资产")


def _binding_semantics(bindings: list[Binding]) -> list[str]:
    errors: list[str] = []
    for binding in bindings:
        if binding.name in INVALID_IDENTITY_NAMES or ASSET_FORM_SUFFIX.search(binding.name):
            errors.append(
                f"“{binding.name}” describes an asset form or role, not a referable screen object"
            )
        if STORYBOARD_DESCRIPTION.search(binding.description):
            errors.append(f"Route B Asset List must not contain storyboard binding “{binding.name}”")
    return errors


def validate(
    text: str,
    *,
    audio_mode: str,
    binding_schema: list[ExpectedBinding],
    approved_body: str,
) -> tuple[list[str], int, int, list[str]]:
    errors = placeholder_errors(text)
    binding_count = 0
    citation_count = 0
    modes: list[str] = []

    if "Reference List:" in text:
        errors.append("Route B must not contain an outer Reference List")
    if "Asset Use:" in text:
        errors.append("Route B must not contain an Asset Use section")
    if "影片调性" in text:
        errors.append("Route B must not contain a separate 影片调性 line")
    if STORYBOARD_DESCRIPTION.search(text):
        errors.append("Route B globally forbids storyboard content")
    for item in binding_schema:
        if item.kind == "storyboard":
            errors.append(
                f"Route B globally forbids storyboard binding “{item.identity}”"
            )

    section_match = SECTIONS.fullmatch(text.rstrip("\n"))
    if not section_match:
        return errors + [
            "expected exact Asset List / Prompt / Constraints section order"
        ], 0, 0, modes

    asset_text = section_match.group("assets").strip()
    prompt = section_match.group("prompt")
    constraints = section_match.group("constraints")
    bindings, binding_errors = parse_bindings(asset_text, "Asset List")
    errors.extend(binding_errors)
    errors.extend(_binding_semantics(bindings))
    binding_count += len(bindings)

    errors.extend(schema_binding_errors(bindings, binding_schema, "B"))

    carrier_text, carriers = execution_scope(prompt)
    if not carriers:
        errors.append("Prompt has no Subject, Action, Timing/beats, or Shot execution carrier")
    errors.extend(director_reference_errors(prompt))
    audio_errors, detected_mode = validate_audio(prompt, audio_mode)
    errors.extend(audio_errors)
    if detected_mode:
        modes.append(detected_mode)

    if AVOID_HEADING.search(prompt):
        errors.append("Prompt retains Avoid/避免; move its content to outer Constraints")
    if EMPTY_AVOID_CONSTRAINT.search(constraints):
        errors.append("empty 禁止出现 line must be omitted")

    transform_errors, avoid_content = identity_transform_errors(
        approved_body, prompt, binding_schema
    )
    errors.extend(transform_errors)
    avoid_lines = constraints.count("禁止出现：")
    if avoid_content is None:
        if avoid_lines:
            errors.append(
                "outer Constraints contains 禁止出现 without a trailing Avoid in BODY"
            )
    else:
        expected_avoid = (
            "禁止出现："
            + normalize_declared_identities(avoid_content, binding_schema)
        )
        if constraints.count(expected_avoid) != 1 or avoid_lines != 1:
            errors.append(
                f"trailing Avoid must appear exactly once as `{expected_avoid}`"
            )

    masked_constraints = re.sub(r"“[^”]*”", "", constraints)
    for item in binding_schema:
        if item.identity in masked_constraints:
            errors.append(
                f"outer Constraints uses identity {item.identity!r} outside its quoted form"
            )
        for alias in item.source_aliases:
            if alias in masked_constraints:
                errors.append(
                    f"source alias {alias!r} remains in outer Constraints"
                )

    for binding in bindings:
        citation = f"“{binding.name}”"
        count = prompt.count(citation)
        if count == 0:
            errors.append(f"Prompt does not cite {citation}")
        else:
            citation_count += count
        if citation not in carrier_text:
            errors.append(
                f"Subject/Action/Timing/Shot execution does not cite {citation}; "
                "Continuity-only or summary-only citation is insufficient"
            )

    alias_scope = prompt + "\n" + constraints
    masked = re.sub(r"“[^”]*”", "", alias_scope)
    for term in ALIAS_EXEMPT_TERMS:
        masked = masked.replace(term, "")
    for token in GENERIC_ALIAS_TOKENS:
        if token in masked:
            errors.append(
                f"generic alias “{token}” appears outside a quoted identity; "
                "use the exact bound identity name for the asset"
            )
            masked = masked.replace(token, "")

    return errors, binding_count, citation_count, modes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt_file", metavar="PROMPT", type=Path)
    parser.add_argument(
        "--director-body",
        dest="director_body",
        required=True,
        type=Path,
        metavar="BODY",
        help="Approved BODY for the current generation scope.",
    )
    parser.add_argument(
        "--bindings",
        dest="bindings",
        required=True,
        type=Path,
        metavar="BINDINGS.json",
        help="BINDINGS.json using wally-reference-bindings/v2.",
    )
    parser.add_argument("--audio-mode", choices=AUDIO_MODES, required=True)
    args = parser.parse_args()

    try:
        text = args.prompt_file.read_text(encoding="utf-8")
        binding_schema = load_binding_schema(args.bindings)
        source_text = args.director_body.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors, bindings, citations, modes = validate(
        text,
        audio_mode=args.audio_mode,
        binding_schema=binding_schema,
        approved_body=source_text,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    mode_summary = ", ".join(modes)
    print(
        f"PASS: {bindings} Asset List bindings, {citations} exact quoted Prompt citations; "
        f"Audio branches: {mode_summary}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
