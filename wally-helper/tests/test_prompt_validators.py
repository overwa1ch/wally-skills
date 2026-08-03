#!/usr/bin/env python3
"""Basic cross-contract tests for the staged Helper validators."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from prompt_validation_common import ExpectedBinding, load_binding_schema, validate_audio  # noqa: E402
from validate_route_a_prompt import CONTROL_SENTENCE, validate as validate_route_a  # noqa: E402
from validate_route_b_prompt import validate as validate_route_b  # noqa: E402


DEFAULT_BODY = """Subject: 雨伞
Action: 雨伞张开。
Audio: 无BGM。持续雨声和伞面摩擦声。
Constraints: 保持动作连续。"""

ROUTE_B_SCHEMA = {
    "SEG01": [
        ExpectedBinding(
            segment="SEG01",
            identity="红伞",
            handle="@图片1",
            kind="static",
            role="P03 prop_reference；身份与外观",
            source_aliases=("雨伞",),
        )
    ]
}

ROUTE_B_PROMPT = """SEG01

Asset List:
“红伞” = @图片1 - P03 prop_reference；身份与外观。

Prompt:
Subject: “红伞”
Action: “红伞”张开。
Audio: 无BGM。持续雨声和伞面摩擦声。
Constraints: 保持动作连续。

Constraints:
只使用本SEG Asset List中的成品资产；不得把参考板内部局部或状态拆成独立资产。
无旁白、无画外解说。"""


class AudioContractTests(unittest.TestCase):
    def test_all_three_audio_branches(self) -> None:
        cases = {
            "default": "Action: 门打开。\nAudio: 无BGM。只有房间底噪和门轴摩擦声。",
            "music": "Action: 门打开。\nAudio: 低沉钢琴配乐进入，压低于环境声。",
            "silence": "Action: 门打开。\nAudio: 全程绝对静音。",
        }
        for mode, body in cases.items():
            with self.subTest(mode=mode):
                errors, detected = validate_audio(body, mode)
                self.assertEqual([], errors)
                self.assertEqual(mode, detected)

    def test_missing_audio_fails(self) -> None:
        errors, _mode = validate_audio("Action: 门打开。", "default")
        self.assertTrue(errors)


class BindingSchemaTests(unittest.TestCase):
    def test_six_field_object_schema(self) -> None:
        payload = {
            "schema_version": "wally-reference-bindings/v1",
            "bindings": [
                {
                    "segment": "SEG01",
                    "identity": "红伞",
                    "handle": "@图片1",
                    "kind": "static",
                    "role": "身份与外观",
                    "source_aliases": ["雨伞"],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bindings.json"
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            parsed = load_binding_schema(path)
        self.assertEqual("红伞", parsed["SEG01"][0].identity)

    def test_unknown_field_fails(self) -> None:
        payload = {
            "schema_version": "wally-reference-bindings/v1",
            "bindings": [
                {
                    "segment": "SEG01",
                    "identity": "红伞",
                    "handle": "@图片1",
                    "kind": "static",
                    "role": "身份与外观",
                    "source_aliases": [],
                    "asset_form": "forbidden-extra",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bindings.json"
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_binding_schema(path)


class RouteValidatorTests(unittest.TestCase):
    def test_route_b_permitted_identity_replacement(self) -> None:
        errors, bindings, citations, modes = validate_route_b(
            ROUTE_B_PROMPT,
            audio_mode="default",
            binding_schema=ROUTE_B_SCHEMA,
            approved_bodies={"SEG01": DEFAULT_BODY},
        )
        self.assertEqual([], errors)
        self.assertEqual((1, 2, ["default"]), (bindings, citations, modes))

    def test_route_b_rejects_other_body_change(self) -> None:
        changed = ROUTE_B_PROMPT.replace("张开。", "突然张开。")
        errors, *_rest = validate_route_b(
            changed,
            audio_mode="default",
            binding_schema=ROUTE_B_SCHEMA,
            approved_bodies={"SEG01": DEFAULT_BODY},
        )
        self.assertTrue(any("changes content beyond" in error for error in errors))

    def test_route_b_extracts_only_trailing_avoid(self) -> None:
        approved = DEFAULT_BODY + "\nAvoid: 额外文字。"
        prompt = ROUTE_B_PROMPT + "\n禁止出现：额外文字。"
        errors, *_rest = validate_route_b(
            prompt,
            audio_mode="default",
            binding_schema=ROUTE_B_SCHEMA,
            approved_bodies={"SEG01": approved},
        )
        self.assertEqual([], errors)

    def test_route_b_normalizes_declared_alias_in_trailing_avoid(self) -> None:
        approved = DEFAULT_BODY + "\nAvoid: 不要雨伞变色。"
        prompt = ROUTE_B_PROMPT + "\n禁止出现：不要“红伞”变色。"
        errors, *_rest = validate_route_b(
            prompt,
            audio_mode="default",
            binding_schema=ROUTE_B_SCHEMA,
            approved_bodies={"SEG01": approved},
        )
        self.assertEqual([], errors)

    def test_route_b_rejects_storyboard_inventory(self) -> None:
        schema = {
            "SEG01": [
                ExpectedBinding(
                    segment="SEG01",
                    identity="SEG01故事板",
                    handle="@图片2",
                    kind="storyboard",
                    role="故事板",
                    source_aliases=(),
                )
            ]
        }
        errors, *_rest = validate_route_b(
            ROUTE_B_PROMPT,
            audio_mode="default",
            binding_schema=schema,
            approved_bodies={"SEG01": DEFAULT_BODY},
        )
        self.assertTrue(any("globally forbids storyboard" in error for error in errors))

    def test_route_a_preserves_body_exactly(self) -> None:
        body = "Action: 红伞张开。\nAudio: 无BGM。持续雨声和伞面摩擦声。"
        prompt = f"""SEG01

Reference List:
“红伞” = @图片1 - 身份与外观。
“SEG01故事板” = @图片2 - 故事板。

影片调性：内容类型为叙事短片。

Prompt:
{CONTROL_SENTENCE}

{body}

Constraints:
无旁白、无画外解说。
画面里不要出现故事板边框、镜头编号、中文标注、红色箭头或线稿风格。"""
        schema = {
            "SEG01": [
                ExpectedBinding("SEG01", "红伞", "@图片1", "static", "身份与外观", ()),
                ExpectedBinding("SEG01", "SEG01故事板", "@图片2", "storyboard", "故事板", ()),
            ]
        }
        errors, bindings, modes = validate_route_a(
            prompt,
            audio_mode="default",
            binding_schema=schema,
            approved_bodies={"SEG01": body},
        )
        self.assertEqual([], errors)
        self.assertEqual((2, ["default"]), (bindings, modes))


class CliContractTests(unittest.TestCase):
    def test_exact_route_b_cli_and_public_audio_choices(self) -> None:
        payload = {
            "schema_version": "wally-reference-bindings/v1",
            "bindings": [
                {
                    "segment": "SEG01",
                    "identity": "红伞",
                    "handle": "@图片1",
                    "kind": "static",
                    "role": "P03 prop_reference；身份与外观",
                    "source_aliases": ["雨伞"],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prompt = root / "prompt.txt"
            body = root / "body.txt"
            bindings = root / "bindings.json"
            prompt.write_text(ROUTE_B_PROMPT, encoding="utf-8")
            body.write_text(DEFAULT_BODY, encoding="utf-8")
            bindings.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            command = [
                sys.executable,
                str(SCRIPT_DIR / "validate_route_b_prompt.py"),
                str(prompt),
                "--director-body",
                str(body),
                "--bindings",
                str(bindings),
                "--audio-mode",
                "default",
            ]
            passed = subprocess.run(command, capture_output=True, text=True, check=False)
            rejected = subprocess.run(
                command[:-1] + ["auto"], capture_output=True, text=True, check=False
            )
        self.assertEqual(0, passed.returncode, passed.stderr)
        self.assertIn("PASS:", passed.stdout)
        self.assertEqual(2, rejected.returncode)
        self.assertIn("invalid choice", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
