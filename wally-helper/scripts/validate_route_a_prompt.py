#!/usr/bin/env python3
"""Validate a finished Route A prompt and its byte-preserved approved BODY."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

from prompt_validation_common import (
    AUDIO_MODES,
    Binding,
    approved_body_map,
    director_reference_errors,
    load_binding_schema,
    parse_bindings,
    placeholder_errors,
    schema_binding_errors,
    split_segments,
    validate_audio,
)


SECTIONS = re.compile(
    r"\AReference List:\s*\n(?P<references>.*?)\n\s*\n"
    r"影片调性：(?P<tone>[^\n]+)\n\s*\nPrompt:\s*\n(?P<prompt>.*)"
    r"\n\s*\nConstraints:\s*\n(?P<constraints>.*)\Z",
    re.DOTALL,
)
CONTROL_SENTENCE = (
    "请根据以上参考生成本段视频。故事板控制镜头顺序、运镜、人物动作、空间关系和道具关系。"
)
STORYBOARD_DESCRIPTION = re.compile(r"故事板|storyboard", re.IGNORECASE)
PREVIEW_DESCRIPTION = re.compile(r"preview", re.IGNORECASE)


def _route_a_binding_errors(heading: str, bindings: list[Binding]) -> list[str]:
    errors: list[str] = []
    storyboards = [item for item in bindings if STORYBOARD_DESCRIPTION.search(item.description)]
    previews = [item for item in bindings if PREVIEW_DESCRIPTION.search(item.description)]
    if len(storyboards) != 1:
        errors.append(f"{heading}: Route A Reference List must contain exactly one storyboard")
    if len(previews) > 1:
        errors.append(f"{heading}: Route A Reference List may contain at most one Preview")
    return errors


def _extract_director_body(prompt: str) -> tuple[str | None, list[str]]:
    if not prompt.startswith(CONTROL_SENTENCE):
        return None, ["Prompt must begin with the frozen Route A storyboard-control sentence"]
    remainder = prompt[len(CONTROL_SENTENCE) :]
    if remainder.startswith("\n\n"):
        remainder = remainder[2:]
    elif remainder.startswith("\n"):
        remainder = remainder[1:]
    else:
        return None, ["director body must begin on the line after the Route A control sentence"]
    if not remainder:
        return None, ["director body is missing after the Route A control sentence"]
    return remainder, []


def validate(
    text: str,
    *,
    audio_mode: str,
    binding_schema: dict,
    approved_bodies: dict[str, str],
) -> tuple[list[str], int, list[str]]:
    errors = placeholder_errors(text)
    binding_count = 0
    modes: list[str] = []

    if "Asset List:" in text:
        errors.append("Route A must not contain an Asset List")
    segments = split_segments(text)
    if not segments:
        return errors + ["no numbered SEG block found"], 0, modes
    for heading, block in segments:
        section_match = SECTIONS.fullmatch(block)
        if not section_match:
            errors.append(
                f"{heading}: expected exact Reference List / 影片调性 / Prompt / Constraints order"
            )
            continue

        bindings, binding_errors = parse_bindings(
            section_match.group("references").strip(), heading, "Reference List"
        )
        errors.extend(binding_errors)
        errors.extend(_route_a_binding_errors(heading, bindings))
        binding_count += len(bindings)
        errors.extend(schema_binding_errors(heading, bindings, binding_schema, "A"))

        director_body, body_errors = _extract_director_body(section_match.group("prompt"))
        errors.extend(f"{heading}: {error}" for error in body_errors)
        if director_body is None:
            continue
        errors.extend(f"{heading}: {error}" for error in director_reference_errors(director_body))
        audio_errors, detected_mode = validate_audio(director_body, audio_mode)
        errors.extend(f"{heading}: {error}" for error in audio_errors)
        if detected_mode:
            modes.append(detected_mode)

        approved = approved_bodies.get(heading)
        if approved is None:
            errors.append(f"{heading}: approved BODY is missing this segment")
        elif director_body != approved.rstrip("\n"):
            errors.append(
                f"{heading}: pasted director body differs from approved body "
                "(comparison ignores only the approved file's terminal newline)"
            )

    rendered = {heading for heading, _body in segments}
    for extra_heading in sorted(set(binding_schema) - rendered):
        errors.append(f"binding inventory contains unrendered segment {extra_heading}")
    return errors, binding_count, modes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt_file", metavar="PROMPT", type=Path)
    parser.add_argument(
        "--director-body",
        dest="director_body",
        required=True,
        type=Path,
        metavar="BODY",
        help="Approved BODY; for multi-SEG prompts, include matching SEG blocks.",
    )
    parser.add_argument(
        "--bindings",
        dest="bindings",
        required=True,
        type=Path,
        metavar="BINDINGS.json",
        help="BINDINGS.json using wally-reference-bindings/v1.",
    )
    parser.add_argument("--audio-mode", choices=AUDIO_MODES, required=True)
    args = parser.parse_args()

    try:
        text = args.prompt_file.read_text(encoding="utf-8")
        binding_schema = load_binding_schema(args.bindings)
        source_text = args.director_body.read_text(encoding="utf-8")
        prompt_segments = split_segments(text)
        approved_bodies = approved_body_map(
            source_text, [heading for heading, _body in prompt_segments]
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors, bindings, modes = validate(
        text,
        audio_mode=args.audio_mode,
        binding_schema=binding_schema,
        approved_bodies=approved_bodies,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {bindings} Reference List bindings; Audio branches: {', '.join(modes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
