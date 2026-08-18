#!/usr/bin/env python3
"""Shared parsing and cross-contract checks for Wally Route A/B prompts."""

from __future__ import annotations

from dataclasses import dataclass
from collections import Counter
import json
from pathlib import Path
import re
from typing import Iterable


ASSET_BINDING = re.compile(r"^“([^”]+)”\s*=\s*(@[^\s]+)\s+-\s+(.+?)。?$")
SHOT_HEADING = re.compile(r"(?m)^\*{0,2}Shot\s+\d+.*$")
FIELD_HEADING = re.compile(
    r"(?m)^\*{0,2}(?P<label>"
    r"Use case|Primary request|Scene/background|Subject|Style/format|"
    r"Lighting/mood|Color palette|Camera|Acting|Continuity|Physics|"
    r"Action|Timing/beats|Audio|SFX|Text \(verbatim\)|Dialogue|Voiceover|"
    r"Constraints|Avoid|Style|Lighting|Color"
    r"):\*{0,2}\s*"
)
EXECUTION_FIELDS = {"Subject", "Action", "Timing/beats"}
WRAPPER_HEADING = re.compile(
    r"(?mi)^[ \t]*\*{0,2}(?:Reference(?: List)?|Asset List)\s*:\*{0,2}\s*"
)
RAW_HANDLE = re.compile(r"(?<![\w@])@[^\s，。；、]+")

PLACEHOLDER_MARKERS = (
    "[资产名称]",
    "[平台引用]",
    "[用途]",
    "[可选：",
    "[Preview名称]",
    "[内容类型]",
    "[原样粘贴",
    "[导演正文含",
    "[出现台词时加入",
    "[可直接指代画面对象的身份名]",
    "[已确认平台引用",
    "[资产类型；控制内容]",
    "[粘贴完整 Director 正文",
    "[命名唯一性：",
    "[含已批准的Voiceover",
    "[含Voiceover、Dialogue",
    "[正文含 Avoid:",
    "[原字段内容。]",
)

AUDIO_MODES = ("default", "music", "silence")
ABSOLUTE_SILENCE_TERMS = (
    "绝对静音",
    "全程静音",
    "完全静音",
    "全段静音",
    "完全无声",
)
MUSIC_TERMS = (
    "BGM",
    "配乐",
    "音乐",
    "乐曲",
    "旋律",
    "钢琴",
    "弦乐",
    "鼓点",
    "音轨",
    "乐器",
)
NON_MUSICAL_SOUND_TERMS = (
    "环境声",
    "底噪",
    "房间音",
    "室内音",
    "风声",
    "雨声",
    "脚步",
    "呼吸",
    "摩擦",
    "碰撞",
    "回声",
    "混响",
    "音效",
    "foley",
    "ambience",
    "room tone",
)

BINDING_SCHEMA_VERSION = "wally-reference-bindings/v2"
BINDING_KINDS = {"static", "storyboard", "preview"}


@dataclass(frozen=True)
class Binding:
    name: str
    handle: str
    description: str


@dataclass(frozen=True)
class ExpectedBinding:
    identity: str
    handle: str
    kind: str
    role: str
    source_aliases: tuple[str, ...]


def parse_bindings(text: str, list_name: str) -> tuple[list[Binding], list[str]]:
    """Parse a rendered Reference/Asset List and report grammar failures."""
    bindings: list[Binding] = []
    errors: list[str] = []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line_number, line in enumerate(lines, start=1):
        match = ASSET_BINDING.fullmatch(line)
        if not match:
            errors.append(
                f"{list_name} line {line_number}: expected "
                "“referable object name” = @handle - asset form and role"
            )
            continue
        name, handle, description = match.groups()
        bindings.append(Binding(name, handle, description.rstrip("。")))

    names = [binding.name for binding in bindings]
    handles = [binding.handle for binding in bindings]
    if len(names) != len(set(names)):
        errors.append(f"duplicate quoted identity name in {list_name}")
    if len(handles) != len(set(handles)):
        errors.append(f"duplicate platform handle in {list_name}")
    return bindings, errors


def execution_scope(prompt: str) -> tuple[str, list[str]]:
    """Return only Subject/Action/Timing or Shot chunks that may carry assets."""
    markers: list[tuple[int, int, str, str]] = []
    for match in FIELD_HEADING.finditer(prompt):
        markers.append((match.start(), match.end(), "field", match.group("label")))
    for match in SHOT_HEADING.finditer(prompt):
        markers.append((match.start(), match.end(), "shot", "Shot"))
    markers.sort(key=lambda item: item[0])

    chunks: list[str] = []
    carriers: list[str] = []
    for index, (start, _end, kind, label) in enumerate(markers):
        end = markers[index + 1][0] if index + 1 < len(markers) else len(prompt)
        if kind == "shot" or label in EXECUTION_FIELDS:
            chunks.append(prompt[start:end])
            carriers.append(label)
    return "\n".join(chunks), carriers


def field_blocks(text: str, labels: Iterable[str]) -> list[tuple[str, str]]:
    """Extract complete adaptive-field blocks without assuming a fixed body."""
    wanted = set(labels)
    markers: list[tuple[int, int, str]] = [
        (match.start(), match.end(), match.group("label"))
        for match in FIELD_HEADING.finditer(text)
    ]
    markers.extend(
        (match.start(), match.end(), "Shot") for match in SHOT_HEADING.finditer(text)
    )
    markers.sort(key=lambda item: item[0])

    blocks: list[tuple[str, str]] = []
    for index, (_start, value_start, label) in enumerate(markers):
        if label not in wanted:
            continue
        value_end = markers[index + 1][0] if index + 1 < len(markers) else len(text)
        blocks.append((label, text[value_start:value_end].strip()))
    return blocks


def _positive_non_musical_sound(value: str) -> bool:
    """Require a positive sound state after removing simple negative clauses."""
    remainder = re.sub(r"(?:无|没有|不含|不得添加|不要|不使用)[^。；，,\n]*", "", value)
    lowered = remainder.lower()
    return any(term.lower() in lowered for term in NON_MUSICAL_SOUND_TERMS)


def _positive_music(value: str) -> bool:
    remainder = re.sub(r"(?:无|没有|不含|不得添加|不要|不使用)[^。；，,\n]*", "", value)
    lowered = remainder.lower()
    return any(term.lower() in lowered for term in MUSIC_TERMS)


def validate_audio(text: str, expected_mode: str) -> tuple[list[str], str | None]:
    """Validate the Action Designer's three-branch Audio/SFX contract."""
    if expected_mode not in AUDIO_MODES:
        return [f"unsupported audio mode: {expected_mode}"], None

    blocks = field_blocks(text, {"Audio", "SFX"})
    if len(blocks) != 1:
        return [f"director body must contain exactly one Audio field (legacy SFX accepted); found {len(blocks)}"], None

    _label, value = blocks[0]
    if not value:
        return ["Audio field is empty"], None

    has_no_bgm = value.lstrip().startswith("无BGM。")
    has_silence = any(term in value for term in ABSOLUTE_SILENCE_TERMS)

    mode = expected_mode

    errors: list[str] = []
    if mode == "default":
        if not has_no_bgm:
            errors.append("default Audio must start with `无BGM。`")
        if has_silence:
            errors.append("default Audio conflicts with an absolute-silence declaration")
        if not _positive_non_musical_sound(value):
            errors.append("default Audio must supply a substantive positive non-musical sound state")
        if _positive_music(value):
            errors.append("default Audio must not add music")
    elif mode == "music":
        if has_no_bgm:
            errors.append("explicit-music Audio must omit `无BGM。`")
        if has_silence:
            errors.append("explicit-music Audio conflicts with absolute silence")
        if not _positive_music(value):
            errors.append("explicit-music Audio must describe the supplied or requested music")
    elif mode == "silence":
        if not has_silence:
            errors.append("absolute-silence Audio must state full-scope absolute silence")
        if has_no_bgm:
            errors.append("absolute-silence Audio must not use the default `无BGM。` branch")
        if field_blocks(text, {"Dialogue", "Voiceover"}) or re.search(r"「[^」]+」", text):
            errors.append("absolute-silence scope must not contain dialogue or voiceover")
        if _positive_non_musical_sound(value) or _positive_music(value):
            errors.append("absolute-silence Audio must not add ambience, foley, or music")

    return errors, mode


def placeholder_errors(text: str) -> list[str]:
    return [f"unresolved template placeholder remains: {marker}" for marker in PLACEHOLDER_MARKERS if marker in text]


def director_reference_errors(prompt: str) -> list[str]:
    errors: list[str] = []
    if WRAPPER_HEADING.search(prompt):
        errors.append("director body contains a forbidden Reference/Reference List/Asset List heading")
    handles = sorted(set(RAW_HANDLE.findall(prompt)))
    for handle in handles:
        errors.append(f"director body contains raw platform handle {handle}")
    return errors


def load_binding_schema(path: Path) -> list[ExpectedBinding]:
    """Load and strictly validate wally-reference-bindings/v2 JSON."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read binding schema: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("binding schema root must be the versioned object")
    if set(payload) != {"schema_version", "bindings"}:
        raise ValueError("binding schema root must contain exactly `schema_version` and `bindings`")
    if payload.get("schema_version") != BINDING_SCHEMA_VERSION:
        raise ValueError(f"schema_version must equal {BINDING_SCHEMA_VERSION}")
    entries = payload.get("bindings")
    if not isinstance(entries, list):
        raise ValueError("binding schema `bindings` must be an array")

    parsed: list[ExpectedBinding] = []
    required = {"identity", "handle", "kind", "role", "source_aliases"}
    semantic_owner: dict[str, str] = {}
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict) or set(entry) != required:
            raise ValueError(f"binding entry {index} must contain exactly {sorted(required)}")
        scalar_fields = required - {"source_aliases"}
        if not all(isinstance(entry[key], str) and entry[key].strip() for key in scalar_fields):
            raise ValueError(f"binding entry {index} scalar fields must be non-empty strings")
        aliases = entry["source_aliases"]
        if not isinstance(aliases, list) or not all(isinstance(alias, str) and alias.strip() for alias in aliases):
            raise ValueError(f"binding entry {index} source_aliases must be an array of non-empty strings")
        if len(aliases) != len(set(aliases)):
            raise ValueError(f"binding entry {index} contains duplicate source_aliases")
        if entry["identity"] in aliases:
            raise ValueError(f"binding entry {index} repeats identity in source_aliases")
        if not entry["handle"].startswith("@") or re.search(r"\s", entry["handle"]):
            raise ValueError(f"binding entry {index} has invalid platform handle")
        if entry["kind"] not in BINDING_KINDS:
            raise ValueError(f"binding entry {index} has unsupported kind {entry['kind']!r}")
        item = ExpectedBinding(
            identity=entry["identity"],
            handle=entry["handle"],
            kind=entry["kind"],
            role=entry["role"],
            source_aliases=tuple(aliases),
        )
        for semantic in (item.identity, *item.source_aliases):
            semantic_key = semantic.casefold()
            owner = semantic_owner.get(semantic_key)
            if owner is not None:
                raise ValueError(
                    f"semantic {semantic!r} is duplicated by identities/aliases "
                    f"for {owner!r} and {item.identity!r}"
                )
            semantic_owner[semantic_key] = item.identity
        parsed.append(item)

    identities = [item.identity for item in parsed]
    handles = [item.handle for item in parsed]
    if len(identities) != len(set(identities)):
        raise ValueError("binding inventory contains duplicate identities")
    if len(handles) != len(set(handles)):
        raise ValueError("binding inventory contains duplicate handles")
    return parsed


def schema_binding_errors(
    actual: list[Binding],
    expected: list[ExpectedBinding],
    route: str,
) -> list[str]:
    """Prove rendered bindings equal the approved current-scope inventory."""
    errors: list[str] = []
    if route == "A":
        storyboards = [item for item in expected if item.kind == "storyboard"]
        previews = [item for item in expected if item.kind == "preview"]
        if len(storyboards) != 1:
            errors.append("Route A inventory must contain exactly one storyboard")
        if len(previews) > 1:
            errors.append("Route A inventory may contain at most one Preview")

    actual_map = {(item.name, item.handle): item for item in actual}
    expected_map = {(item.identity, item.handle): item for item in expected}
    missing = expected_map.keys() - actual_map.keys()
    extra = actual_map.keys() - expected_map.keys()
    for name, handle in sorted(missing):
        errors.append(f"rendered list is missing approved binding “{name}” = {handle}")
    for name, handle in sorted(extra):
        errors.append(f"rendered list contains unapproved binding “{name}” = {handle}")

    for key in actual_map.keys() & expected_map.keys():
        rendered = actual_map[key].description
        item = expected_map[key]
        if item.role not in rendered:
            errors.append(f"“{item.identity}” description omits role `{item.role}`")
        if item.kind == "storyboard" and "故事板" not in rendered:
            errors.append(f"storyboard binding “{item.identity}” is not labeled 故事板")
        elif item.kind == "preview" and "preview" not in rendered.lower():
            errors.append(f"Preview binding “{item.identity}” is not labeled Preview")
    return errors


TRAILING_AVOID = re.compile(
    r"(?s)(?P<prefix>.*?)(?:\n+)(?:\*{0,2}Avoid:\*{0,2}\s*|避免：\s*)(?P<content>.+?)\s*\Z"
)


def extract_trailing_avoid(text: str) -> tuple[str, str | None]:
    """Extract only a terminal legacy Avoid/避免 field."""
    match = TRAILING_AVOID.fullmatch(text.rstrip("\n"))
    if not match:
        return text.rstrip("\n"), None
    if FIELD_HEADING.search(match.group("content")) or SHOT_HEADING.search(match.group("content")):
        return text.rstrip("\n"), None
    return match.group("prefix").rstrip("\n"), match.group("content").strip()


def normalize_declared_identities(value: str, bindings: list[ExpectedBinding]) -> str:
    """Normalize declared aliases/bare identities to exact quoted identities."""
    replacements: dict[str, str] = {}
    for item in bindings:
        quoted = f"“{item.identity}”"
        replacements[quoted] = quoted
        replacements[item.identity] = quoted
        for alias in item.source_aliases:
            replacements[alias] = quoted
    if not replacements:
        return value
    alternatives = sorted(replacements, key=len, reverse=True)
    pattern = re.compile("|".join(re.escape(term) for term in alternatives))
    return pattern.sub(lambda match: replacements[match.group(0)], value)


def identity_transform_errors(
    approved_body: str,
    rendered_body: str,
    bindings: list[ExpectedBinding],
) -> tuple[list[str], str | None]:
    """Prove Route B changed only declared aliases/identity insertions and trailing Avoid.

    The proof turns declared source identities/aliases and rendered quoted
    identities into stable markers. The non-identity skeleton must remain
    byte-identical, every source marker must remain at the same skeleton offset,
    and the rendered body may add only extra declared markers. Horizontal
    whitespace immediately touching a marker belongs to that permitted edit.
    """
    errors: list[str] = []
    approved_base, avoid_content = extract_trailing_avoid(approved_body)

    masked_rendered = re.sub(r"“[^”]*”", "", rendered_body)
    source_terms: list[tuple[str, str]] = []
    rendered_terms: list[tuple[str, str]] = []
    marker_ids: list[str] = []
    for index, item in enumerate(bindings):
        marker = f"\x00B{index}\x00"
        marker_ids.append(marker)
        quoted = f"“{item.identity}”"
        if quoted not in rendered_body:
            errors.append(f"rendered body does not use declared identity {quoted}")
        if item.identity in masked_rendered:
            errors.append(
                f"identity {item.identity!r} appears outside its exact quoted form"
            )
        source_terms.extend(((quoted, marker), (item.identity, marker)))
        rendered_terms.append((quoted, marker))
        for alias in item.source_aliases:
            if alias in masked_rendered:
                errors.append(
                    f"source alias {alias!r} remains outside a quoted identity"
                )
            source_terms.append((alias, marker))

    def canonicalize(value: str, terms: list[tuple[str, str]]) -> str:
        lookup = {term: marker for term, marker in terms}
        alternatives = sorted(lookup, key=len, reverse=True)
        if alternatives:
            pattern = re.compile("|".join(re.escape(term) for term in alternatives))
            value = pattern.sub(lambda match: lookup[match.group(0)], value)
        if marker_ids:
            marker_pattern = "|".join(re.escape(marker) for marker in marker_ids)
            value = re.sub(rf"[ \t]*({marker_pattern})[ \t]*", r"\1", value)
        return value

    if not marker_ids:
        if approved_base != rendered_body:
            errors.append(
                "rendered director body changes content beyond terminal Avoid extraction"
            )
        return errors, avoid_content

    marker_re = re.compile("(" + "|".join(re.escape(marker) for marker in marker_ids) + ")")

    def skeleton_and_anchors(value: str) -> tuple[str, Counter[tuple[int, str]]]:
        offset = 0
        skeleton: list[str] = []
        anchors: Counter[tuple[int, str]] = Counter()
        for part in marker_re.split(value):
            if part in marker_ids:
                anchors[(offset, part)] += 1
            else:
                skeleton.append(part)
                offset += len(part)
        return "".join(skeleton), anchors

    source = canonicalize(approved_base, source_terms)
    rendered = canonicalize(rendered_body, rendered_terms)
    source_skeleton, required_anchors = skeleton_and_anchors(source)
    rendered_skeleton, rendered_anchors = skeleton_and_anchors(rendered)
    missing_anchors = required_anchors - rendered_anchors

    if source_skeleton != rendered_skeleton or missing_anchors:
        errors.append(
            "rendered director body changes content beyond declared identity "
            "replacement/insertion and terminal Avoid extraction"
        )
    return errors, avoid_content
