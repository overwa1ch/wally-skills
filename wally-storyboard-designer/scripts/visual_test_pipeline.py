#!/usr/bin/env python3
"""Prepare, record, validate, split, and assemble Wally visual tests."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date, datetime
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import tempfile

from PIL import Image, ImageDraw, ImageFont


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASPECT = 16 / 9
TOLERANCE = 0.01
MODE = {
    "storyboard": {"columns": 3, "rows": 3, "label": "故事板"},
    "shot-table": {"columns": 2, "rows": 2, "label": "分镜表"},
}
SCENE_RE = re.compile(r"(?m)^## 场景(\d+)[：:]([^\n]+)\n")
SHOT_RE = re.compile(r"(?m)^(?:### )?分镜(\d+)｜[^\n]*\n")
TABLE_SHOT_RE = re.compile(r"(?m)^\|\s*(?:镜)?(\d+)\s*\|[^\n]*\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    temporary.replace(path)


def load_manifest(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != "wally-visual-test-run/v1":
        raise ValueError("unsupported manifest schema")
    return payload


def relative_to_run(path: Path, run_root: Path) -> str:
    return path.resolve().relative_to(run_root.resolve()).as_posix()


def run_path(manifest_path: Path, recorded: str) -> Path:
    path = Path(recorded)
    return path if path.is_absolute() else manifest_path.parent / path


def prompt_blocks(mode: str) -> list[str]:
    filename = "storyboard-prompt-template.md" if mode == "storyboard" else "shot-table-prompt-template.md"
    text = (SKILL_ROOT / "templates" / filename).read_text(encoding="utf-8")
    blocks = re.findall(r"```text\n(.*?)```", text, re.DOTALL)
    if len(blocks) != 2:
        raise ValueError(f"expected two prompt blocks in {filename}")
    return [block.rstrip() + "\n" for block in blocks]


def scene_records(source_text: str) -> tuple[str, list[dict]]:
    scenes = list(SCENE_RE.finditer(source_text))
    if not scenes:
        raise ValueError("source requires explicit headings such as '## 场景1：地点 / 时间'")
    preamble = source_text[: scenes[0].start()]
    records = []
    seen_scene_ids: set[str] = set()
    for index, scene in enumerate(scenes):
        end = scenes[index + 1].start() if index + 1 < len(scenes) else len(source_text)
        region = source_text[scene.start():end]
        trailing_h2 = re.search(r"(?m)^## (?!场景\d+[：:])", region[scene.end() - scene.start():])
        if trailing_h2:
            region = region[: scene.end() - scene.start() + trailing_h2.start()]
        shots = list(SHOT_RE.finditer(region))
        source_format = "blocks"
        if not shots:
            shots = list(TABLE_SHOT_RE.finditer(region))
            source_format = "table"
        if not shots:
            raise ValueError(f"场景{scene.group(1)} has no recognized shot blocks or table rows")
        scene_id = f"S{int(scene.group(1)):02d}"
        if scene_id in seen_scene_ids:
            raise ValueError(f"duplicate scene: {scene_id}")
        seen_scene_ids.add(scene_id)
        shot_blocks = []
        shot_ids = []
        for shot_index, shot in enumerate(shots):
            if source_format == "table":
                shot_end = shot.end()
            else:
                shot_end = shots[shot_index + 1].start() if shot_index + 1 < len(shots) else len(region)
            shot_id = int(shot.group(1))
            if shot_id in shot_ids:
                raise ValueError(f"duplicate shot {shot_id} in {scene_id}")
            shot_ids.append(shot_id)
            shot_blocks.append(region[shot.start():shot_end])
        records.append({
            "scene_id": scene_id,
            "scene_order": index + 1,
            "scene_title": scene.group(2).strip(),
            "scene_heading": region[: scene.end() - scene.start()],
            "source_format": source_format,
            "prefix": region[: shots[0].start()],
            "shot_ids": shot_ids,
            "shot_blocks": shot_blocks,
        })
    return preamble, records


def load_assets(path: Path | None, scenes: list[dict], mode: str) -> dict:
    if mode == "storyboard":
        return {}
    if path is None:
        raise ValueError("shot-table init requires --assets-json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    result = {}
    for scene in scenes:
        scene_id = scene["scene_id"]
        assets = payload.get(scene_id)
        if not isinstance(assets, list) or not assets:
            raise ValueError(f"missing asset list for {scene_id}")
        normalized = []
        for asset in assets:
            if not all(asset.get(key) for key in ("id", "name", "path")):
                raise ValueError(f"asset in {scene_id} requires id, name, and path")
            asset_path = Path(asset["path"]).expanduser()
            if not asset_path.is_absolute():
                asset_path = path.parent / asset_path
            asset_path = asset_path.resolve()
            if not asset_path.is_file():
                raise FileNotFoundError(asset_path)
            normalized.append({"id": asset["id"], "name": asset["name"], "path": str(asset_path), "sha256": sha256(asset_path)})
        result[scene_id] = normalized
    return result


def project_instructions(mode: str, versions: int) -> str:
    grid = "3×3" if mode == "storyboard" else "2×2"
    return (
        f"只使用当前聊天或分支明确上传的材料。每张图使用规则{grid}，一个镜头对应一个画格，按原镜号排列；不足一页的格子留白。\n"
        "只绘制渲染包内实际存在的镜头块，不根据其他元数据补画镜头。整张成图使用16:9横版画布，等分网格后每格仍为16:9。\n"
        f"本渲染包需要{versions}个版本。每次回复只调用一次原生生图并生成1张独立图像；后续版本等待下一条消息，不得把多个版本拼在一张图里。\n"
        "不要使用Python、代码解释器、SVG、canvas或普通文件附件制作替代图。\n"
    )


def init_run(args: argparse.Namespace) -> None:
    source = args.source.expanduser().resolve()
    output = args.output.expanduser().resolve()
    manifest_path = output / "manifest.json"
    if manifest_path.exists():
        raise FileExistsError(f"refusing to overwrite existing run: {manifest_path}")
    text = source.read_text(encoding="utf-8")
    preamble, scenes = scene_records(text)
    assets = load_assets(args.assets_json, scenes, args.mode)
    spec = MODE[args.mode]
    capacity = spec["columns"] * spec["rows"]
    output.mkdir(parents=True, exist_ok=True)
    prompts_dir = output / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    for label, content in zip(("short", "template"), prompt_blocks(args.mode)):
        (prompts_dir / f"{label}.txt").write_text(content, encoding="utf-8")
    browser_dir = output / "browser"
    browser_dir.mkdir(parents=True, exist_ok=True)
    (browser_dir / "project-instructions.txt").write_text(project_instructions(args.mode, args.versions), encoding="utf-8")
    jobs = []
    for scene in scenes:
        scene_assets = assets.get(scene["scene_id"], [])
        if scene_assets:
            lines = ["请确认以下名称与上传文件一一对应，不要开始绘制：", ""]
            lines.extend(f"{a['id']}｜{a['name']} → {Path(a['path']).name}" for a in scene_assets)
            (browser_dir / f"asset-mapping-{scene['scene_id']}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        for page_index, offset in enumerate(range(0, len(scene["shot_ids"]), capacity), start=1):
            ids = scene["shot_ids"][offset:offset + capacity]
            blocks = scene["shot_blocks"][offset:offset + capacity]
            packet_dir = output / "packets" / scene["scene_id"]
            packet_dir.mkdir(parents=True, exist_ok=True)
            packet = packet_dir / f"P{page_index:02d}-SH{ids[0]:03d}-{ids[-1]:03d}.md"
            # A page packet contains only the exact source scene heading and the
            # exact shot blocks assigned to that page. Full-work preambles and
            # scene-level metadata often mention the scene's total shot count;
            # carrying those lines into a partial page makes image models invent
            # off-page panels. Removing them is mechanical packaging, not a
            # rewrite of the authoritative scene or shot text.
            packet.write_text(scene["scene_heading"].rstrip("\n") + "\n\n" + "".join(blocks), encoding="utf-8")
            job_id = f"{'SB' if args.mode == 'storyboard' else 'ST'}-{scene['scene_id']}-P{page_index:02d}"
            jobs.append({
                "job_id": job_id,
                "mode": args.mode,
                "scene_id": scene["scene_id"],
                "scene_order": scene["scene_order"],
                "scene_title": scene["scene_title"],
                "page": page_index,
                "shot_ids": ids,
                "packet": relative_to_run(packet, output),
                "packet_sha256": sha256(packet),
                "chat_url": None,
                "branch_url": None,
                "status": "prepared",
                "versions": [{
                    "version": f"V{version:02d}", "status": "pending", "artifact_origin": None,
                    "native_card_evidence": None, "chat_url": None, "download_url": None,
                    "raw_image": None, "raw_sha256": None, "panel_files": [],
                } for version in range(1, args.versions + 1)],
            })
    manifest = {
        "schema": "wally-visual-test-run/v1", "run_id": args.run_id, "work": args.work,
        "created": date.today().isoformat(), "mode": args.mode, "status": "prepared",
        "source": {"path": str(source), "sha256": sha256(source)},
        "grid": {"columns": spec["columns"], "rows": spec["rows"], "panel_aspect": "16:9"},
        "versions_per_page": args.versions,
        "project": {"name": args.project_name or f"WALLY｜{args.work}｜{spec['label']}测试｜{args.run_id}", "url": None},
        "assets_by_scene": assets,
        "asset_bases": [{
            "scene_id": scene["scene_id"], "chat_name": f"ASSET-{scene['scene_id']}",
            "chat_url": None, "mapping_prompt": f"browser/asset-mapping-{scene['scene_id']}.txt",
            "status": "pending",
        } for scene in scenes if args.mode == "shot-table"],
        "prompts": {name: {"path": f"prompts/{name}.txt", "sha256": sha256(prompts_dir / f"{name}.txt")} for name in ("short", "template")},
        "project_instructions": {"path": "browser/project-instructions.txt", "sha256": sha256(browser_dir / "project-instructions.txt")},
        "jobs": jobs, "errors": [], "deliverables": {},
    }
    atomic_json(manifest_path, manifest)
    print(f"created {manifest_path}")
    print(f"scenes={len(scenes)} jobs={len(jobs)} versions={sum(len(j['versions']) for j in jobs)}")


def find_job(manifest: dict, job_id: str) -> dict:
    matches = [job for job in manifest["jobs"] if job["job_id"] == job_id]
    if len(matches) != 1:
        raise ValueError(f"expected one job {job_id}, found {len(matches)}")
    return matches[0]


def find_version(job: dict, version: str) -> dict:
    matches = [record for record in job["versions"] if record["version"] == version]
    if len(matches) != 1:
        raise ValueError(f"expected one version {version}, found {len(matches)}")
    return matches[0]


def record_native(args: argparse.Namespace) -> None:
    manifest_path = args.manifest.expanduser().resolve()
    manifest = load_manifest(manifest_path)
    job = find_job(manifest, args.job)
    version = find_version(job, args.version)
    if version["status"] != "pending" and not args.replace:
        raise ValueError(f"{args.job}/{args.version} is {version['status']}; use --replace only after reviewing the prior record")
    source = args.file.expanduser().resolve()
    with Image.open(source) as image:
        image.verify()
    suffix = source.suffix.lower() or ".png"
    target = manifest_path.parent / "raw" / job["scene_id"] / f"P{int(job['page']):02d}" / args.version / f"native{suffix}"
    target.parent.mkdir(parents=True, exist_ok=True)
    if source != target:
        shutil.copy2(source, target)
    version.update({
        "status": "recorded-native", "artifact_origin": "chatgpt-native-image-card",
        "native_card_evidence": args.native_card_evidence, "chat_url": args.chat_url,
        "download_url": args.download_url, "raw_image": relative_to_run(target, manifest_path.parent),
        "raw_sha256": sha256(target), "panel_files": [],
    })
    location_key = "chat_url" if manifest["mode"] == "storyboard" else "branch_url"
    job[location_key] = job[location_key] or args.chat_url
    job["status"] = "recording"
    manifest["status"] = "recording"
    atomic_json(manifest_path, manifest)
    print(f"recorded native image: {args.job}/{args.version} {version['raw_sha256']}")


def reject_version(args: argparse.Namespace) -> None:
    manifest_path = args.manifest.expanduser().resolve()
    manifest = load_manifest(manifest_path)
    job = find_job(manifest, args.job)
    version = find_version(job, args.version)
    version.update({
        "status": "rejected", "artifact_origin": args.origin, "rejection_reason": args.reason,
        "native_card_evidence": None, "chat_url": None, "download_url": None,
        "raw_image": None, "raw_sha256": None, "panel_files": [],
    })
    job["status"] = "incomplete"
    manifest["status"] = "incomplete"
    atomic_json(manifest_path, manifest)
    print(f"rejected: {args.job}/{args.version}")


def set_project(args: argparse.Namespace) -> None:
    manifest_path = args.manifest.expanduser().resolve()
    manifest = load_manifest(manifest_path)
    manifest["project"]["url"] = args.url
    atomic_json(manifest_path, manifest)


def set_job(args: argparse.Namespace) -> None:
    manifest_path = args.manifest.expanduser().resolve()
    manifest = load_manifest(manifest_path)
    job = find_job(manifest, args.job)
    if args.chat_url:
        job["chat_url"] = args.chat_url
    if args.branch_url:
        job["branch_url"] = args.branch_url
    atomic_json(manifest_path, manifest)


def set_asset_base(args: argparse.Namespace) -> None:
    manifest_path = args.manifest.expanduser().resolve()
    manifest = load_manifest(manifest_path)
    matches = [base for base in manifest.get("asset_bases", []) if base["scene_id"] == args.scene]
    if len(matches) != 1:
        raise ValueError(f"expected one asset base for {args.scene}, found {len(matches)}")
    matches[0].update({"chat_url": args.url, "status": "confirmed"})
    atomic_json(manifest_path, manifest)


def block_run(args: argparse.Namespace) -> None:
    manifest_path = args.manifest.expanduser().resolve()
    manifest = load_manifest(manifest_path)
    event = {
        "at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "stage": args.stage,
        "reason": args.reason,
    }
    manifest.setdefault("errors", []).append(event)
    manifest["status"] = "blocked"
    atomic_json(manifest_path, manifest)
    print(f"blocked at {args.stage}: {args.reason}")


def grid_boxes(size: tuple[int, int], columns: int, rows: int) -> list[tuple[int, int, int, int]]:
    width, height = size
    xs = [round(i * width / columns) for i in range(columns + 1)]
    ys = [round(i * height / rows) for i in range(rows + 1)]
    return [(xs[x], ys[y], xs[x + 1], ys[y + 1]) for y in range(rows) for x in range(columns)]


def projection_clusters(image: Image.Image, axis: str, fraction: float, threshold: int = 120) -> list[tuple[int, int, float]]:
    gray = image.convert("L")
    pixels = gray.load()
    width, height = gray.size
    positions = []
    limit = width if axis == "y" else height
    length = height if axis == "y" else width
    for position in range(length):
        dark = 0
        if axis == "y":
            for x in range(width):
                dark += pixels[x, position] < threshold
        else:
            for y in range(height):
                dark += pixels[position, y] < threshold
        score = dark / limit
        if score >= fraction:
            positions.append((position, score))
    clusters: list[list[tuple[int, float]]] = []
    for position, score in positions:
        if not clusters or position > clusters[-1][-1][0] + 1:
            clusters.append([])
        clusters[-1].append((position, score))
    return [(cluster[0][0], cluster[-1][0], max(score for _, score in cluster)) for cluster in clusters]


def strongest_position(image: Image.Image, axis: str, start: int, end: int, threshold: int = 120) -> int:
    gray = image.convert("L")
    pixels = gray.load()
    width, height = gray.size
    best_position, best_score = start, -1
    for position in range(max(0, start), min(end, width if axis == "x" else height)):
        if axis == "x":
            score = sum(pixels[position, y] < threshold for y in range(height)) / height
        else:
            score = sum(pixels[x, position] < threshold for x in range(width)) / width
        if score > best_score:
            best_position, best_score = position, score
    return best_position


def detected_grid_boxes(image: Image.Image, columns: int, rows: int) -> list[tuple[int, int, int, int]]:
    """Locate visible cell boundaries while retaining an equal-grid fallback.

    Native image cards often add a work header or gutters around an otherwise
    regular grid. Dividing the whole canvas blindly then cuts captions and title
    bars across adjacent shots. This detector uses only full-row/full-column
    boundary evidence; it never interprets or changes depicted content.
    """
    width, height = image.size
    ratio = width / height
    if abs(ratio / ASPECT - 1) > TOLERANCE:
        raise ValueError(f"native image ratio {ratio:.4f} is outside 1% of 16:9")

    horizontal = projection_clusters(image, "y", 0.90)
    # A dark title band contains white lettering, so its per-row score can dip
    # below the thin-border threshold. Use a looser projection only to identify
    # multi-pixel bands; keep 0.90 for border-line pairing.
    horizontal_bands = projection_clusters(image, "y", 0.50)
    bands = [cluster for cluster in horizontal_bands if cluster[1] - cluster[0] + 1 >= 8]
    if len(bands) >= rows:
        if len(bands) >= rows + 1 and bands[0][0] <= 2:
            bands = bands[1:]
        row_starts = [cluster[0] for cluster in bands[:rows]]
        if len(row_starts) == rows:
            y_ranges = [
                (row_starts[index], row_starts[index + 1] if index + 1 < rows else height)
                for index in range(rows)
            ]
        else:
            y_ranges = []
    else:
        thin_horizontal = [cluster for cluster in horizontal if cluster[1] - cluster[0] + 1 <= 5]
        y_ranges = [
            (thin_horizontal[index][0], thin_horizontal[index + 1][1] + 1)
            for index in range(0, min(len(thin_horizontal), 2 * rows), 2)
            if index + 1 < len(thin_horizontal)
        ]

    vertical = projection_clusters(image, "x", 0.55)
    thin_vertical = [cluster for cluster in vertical if cluster[1] - cluster[0] + 1 <= 5]
    if len(thin_vertical) >= 2 * columns:
        x_ranges = [
            (thin_vertical[index][0], thin_vertical[index + 1][1] + 1)
            for index in range(0, 2 * columns, 2)
        ]
    else:
        boundaries = []
        for index in range(columns + 1):
            if index == columns:
                boundaries.append(width)
                continue
            expected = index * width / columns
            radius = width * (0.08 if index == 0 else 0.04)
            boundaries.append(strongest_position(image, "x", round(expected - radius), round(expected + radius) + 1, threshold=160))
        x_ranges = list(zip(boundaries[:-1], boundaries[1:]))

    if len(x_ranges) != columns or len(y_ranges) != rows:
        return grid_boxes(image.size, columns, rows)
    boxes = [(left, top, right, bottom) for top, bottom in y_ranges for left, right in x_ranges]
    if any(right - left < 32 or bottom - top < 32 for left, top, right, bottom in boxes):
        return grid_boxes(image.size, columns, rows)
    return boxes


def pad_to_aspect(image: Image.Image) -> tuple[Image.Image, tuple[int, int]]:
    width, height = image.size
    if width / height > ASPECT:
        target_width, target_height = width, math.ceil(width / ASPECT)
    else:
        target_width, target_height = math.ceil(height * ASPECT), height
    canvas = Image.new("RGB", (target_width, target_height), "white")
    offset = ((target_width - width) // 2, (target_height - height) // 2)
    canvas.paste(image.convert("RGB"), offset)
    return canvas, offset


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = (
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    )
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def validate_ready(manifest_path: Path, manifest: dict) -> None:
    failures = []
    if not manifest.get("project", {}).get("url"):
        failures.append("project: missing URL")
    if manifest["mode"] == "shot-table":
        for base in manifest.get("asset_bases", []):
            if base.get("status") != "confirmed" or not base.get("chat_url"):
                failures.append(f"{base['scene_id']}: asset base is not confirmed with a URL")
        for scene_id, assets in manifest.get("assets_by_scene", {}).items():
            for asset in assets:
                path = Path(asset["path"])
                if not path.is_file():
                    failures.append(f"{scene_id}/{asset['id']}: asset file is missing")
                elif sha256(path) != asset["sha256"]:
                    failures.append(f"{scene_id}/{asset['id']}: asset hash mismatch")
    for job in manifest["jobs"]:
        location_key = "chat_url" if manifest["mode"] == "storyboard" else "branch_url"
        if not job.get(location_key):
            failures.append(f"{job['job_id']}: missing {location_key}")
        if len(job["versions"]) != manifest["versions_per_page"]:
            failures.append(f"{job['job_id']}: wrong version count")
        for version in job["versions"]:
            label = f"{job['job_id']}/{version['version']}"
            if version.get("status") not in {"recorded-native", "split"}:
                failures.append(f"{label}: status={version.get('status')}")
            if version.get("artifact_origin") != "chatgpt-native-image-card":
                failures.append(f"{label}: non-native origin")
            if not version.get("native_card_evidence"):
                failures.append(f"{label}: missing native-card evidence")
            if not version.get("raw_image") or not run_path(manifest_path, version["raw_image"]).is_file():
                failures.append(f"{label}: missing raw image")
            elif version.get("raw_sha256") != sha256(run_path(manifest_path, version["raw_image"])):
                failures.append(f"{label}: raw hash mismatch")
    if failures:
        raise ValueError("run is not ready:\n- " + "\n- ".join(failures))


def split_native(manifest_path: Path, manifest: dict) -> list[dict]:
    records = []
    columns, rows = manifest["grid"]["columns"], manifest["grid"]["rows"]
    for job in manifest["jobs"]:
        for version in job["versions"]:
            raw = run_path(manifest_path, version["raw_image"])
            with Image.open(raw) as source:
                boxes = detected_grid_boxes(source, columns, rows)
            if len(job["shot_ids"]) > len(boxes):
                raise ValueError(f"{job['job_id']} has more shots than cells")
    for job in manifest["jobs"]:
        for version in job["versions"]:
            raw = run_path(manifest_path, version["raw_image"])
            with Image.open(raw) as source:
                image = source.convert("RGB")
                boxes = detected_grid_boxes(image, columns, rows)
                panel_files = []
                for shot_id, box in zip(job["shot_ids"], boxes):
                    target = manifest_path.parent / "panels" / job["scene_id"] / f"P{int(job['page']):02d}" / version["version"] / f"SH{int(shot_id):03d}.png"
                    target.parent.mkdir(parents=True, exist_ok=True)
                    content = image.crop(box)
                    panel, paste_offset = pad_to_aspect(content)
                    panel.save(target, format="PNG")
                    recorded = relative_to_run(target, manifest_path.parent)
                    panel_files.append(recorded)
                    records.append({
                        "scene_id": job["scene_id"], "scene_order": job["scene_order"],
                        "scene_title": job["scene_title"], "page": job["page"], "shot_id": shot_id,
                        "version": version["version"], "panel": recorded, "source_raw": version["raw_image"],
                        "source_sha256": version["raw_sha256"], "crop_box": box,
                        "content_size": content.size, "paste_offset": paste_offset,
                    })
            version["panel_files"] = panel_files
            version["status"] = "split"
        job["status"] = "split"
    return records


def grouped_scenes(records: list[dict]) -> list[list[dict]]:
    groups: dict[str, list[dict]] = {}
    for record in sorted(records, key=lambda r: (r["scene_order"], r["shot_id"])):
        groups.setdefault(record["scene_id"], []).append(record)
    return list(groups.values())


def assemble_long(manifest_path: Path, manifest: dict, records: list[dict], version: str, target: Path) -> None:
    columns = manifest["grid"]["columns"]
    scenes = grouped_scenes(records)
    sizes = []
    for record in records:
        with Image.open(run_path(manifest_path, record["panel"])) as panel:
            sizes.append(panel.size)
    panel_w = max(size[0] for size in sizes)
    panel_h = max(size[1] for size in sizes)
    label_h, scene_h = 52, 80
    margin, gap, header = 36, 18, 126
    rows = sum(math.ceil(len(scene) / columns) for scene in scenes)
    width = 2 * margin + columns * panel_w + (columns - 1) * gap
    height = header + 2 * margin + rows * (panel_h + label_h + gap) + len(scenes) * (scene_h + margin)
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((margin, 24), f"{manifest['work']}｜{MODE[manifest['mode']]['label']}｜{version}", fill="black", font=load_font(38))
    draw.text((margin, 76), "原生图片无损切格后重组｜待人工审查", fill="#555555", font=load_font(25))
    y = header + margin
    for scene in scenes:
        draw.rectangle((margin, y, width - margin, y + 60), fill="#edf0f2")
        draw.text((margin + 14, y + 9), f"{scene[0]['scene_id']}｜{scene[0]['scene_title']}", fill="#273540", font=load_font(31))
        for index, record in enumerate(scene):
            row, column = divmod(index, columns)
            x = margin + column * (panel_w + gap)
            cell_y = y + scene_h + row * (label_h + panel_h + gap)
            draw.text((x, cell_y + 8), f"镜 {int(record['shot_id']):03d}", fill="black", font=load_font(25))
            with Image.open(run_path(manifest_path, record["panel"])) as panel:
                original = panel.convert("RGB")
            offset_x = x + (panel_w - original.width) // 2
            offset_y = cell_y + label_h + (panel_h - original.height) // 2
            canvas.paste(original, (offset_x, offset_y))
        y += scene_h + math.ceil(len(scene) / columns) * (label_h + panel_h + gap) + margin
    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(target, format="PNG")


def pdf_font():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    candidates = (
        Path("/System/Library/Fonts/STHeiti Light.ttc"),
        Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    )
    font = next((path for path in candidates if path.is_file()), None)
    if font is None:
        raise RuntimeError("Chinese TrueType font required for review PDF")
    pdfmetrics.registerFont(TTFont("WallyChinese", str(font), subfontIndex=0))
    return "WallyChinese"


def assemble_pdf(manifest_path: Path, manifest: dict, by_version: dict[str, list[dict]], target: Path) -> None:
    from reportlab.lib.pagesizes import A3, landscape
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas
    font = pdf_font()
    width, height = landscape(A3)
    doc = canvas.Canvas(str(target), pagesize=(width, height))
    page_number = 0
    columns, rows = manifest["grid"]["columns"], manifest["grid"]["rows"]
    capacity = columns * rows
    for version in sorted(by_version):
        for scene in grouped_scenes(by_version[version]):
            for offset in range(0, len(scene), capacity):
                page_number += 1
                page = scene[offset:offset + capacity]
                doc.setFont(font, 18)
                doc.drawString(36, height - 36, f"{manifest['work']}｜{MODE[manifest['mode']]['label']}｜{version}")
                doc.setFont(font, 11)
                doc.drawString(36, height - 58, f"{page[0]['scene_id']}｜{page[0]['scene_title']}")
                margin_x, top, bottom, gx, gy, label_h = 36, height - 76, 34, 12, 16, 18
                cell_w = (width - 2 * margin_x - (columns - 1) * gx) / columns
                image_h = cell_w / ASPECT
                if rows * (label_h + image_h) + (rows - 1) * gy > top - bottom:
                    image_h = (top - bottom - rows * label_h - (rows - 1) * gy) / rows
                    cell_w = image_h * ASPECT
                for index, record in enumerate(page):
                    row, column = divmod(index, columns)
                    x = margin_x + column * (cell_w + gx)
                    y_top = top - row * (label_h + image_h + gy)
                    doc.setFont(font, 10)
                    doc.drawString(x, y_top - 12, f"镜 {int(record['shot_id']):03d}")
                    doc.drawImage(ImageReader(str(run_path(manifest_path, record["panel"]))), x, y_top - label_h - image_h, width=cell_w, height=image_h, preserveAspectRatio=True, mask="auto")
                doc.setFont(font, 9)
                doc.drawString(36, 18, "原生图片无损切格后重组；内容待人工审查。")
                doc.drawRightString(width - 36, 18, f"第 {page_number} 页")
                doc.showPage()
    doc.save()


def assemble_run(args: argparse.Namespace) -> None:
    manifest_path = args.manifest.expanduser().resolve()
    manifest = load_manifest(manifest_path)
    validate_ready(manifest_path, manifest)
    records = split_native(manifest_path, manifest)
    by_version = defaultdict(list)
    for record in records:
        by_version[record["version"]].append(record)
    output = manifest_path.parent / "assembled"
    deliverables = {}
    for version, version_records in sorted(by_version.items()):
        target = output / f"{manifest['mode']}-{version}.png"
        assemble_long(manifest_path, manifest, version_records, version, target)
        deliverables[version] = relative_to_run(target, manifest_path.parent)
    pdf = output / "review.pdf"
    output.mkdir(parents=True, exist_ok=True)
    assemble_pdf(manifest_path, manifest, by_version, pdf)
    deliverables["review_pdf"] = relative_to_run(pdf, manifest_path.parent)
    report = {
        "run_id": manifest["run_id"], "status": "assembled-awaiting-human-review",
        "source_manifest_sha256_before_assembly": sha256(manifest_path),
        "validation_scope": "Native provenance, file hashes, version count, shot order, and equal-cell 16:9 proportions. Content approval remains human.",
        "panel_count": len(records), "panels": records, "deliverables": deliverables,
    }
    atomic_json(output / "assembly-report.json", report)
    manifest["deliverables"] = deliverables
    manifest["status"] = "assembled-awaiting-human-review"
    atomic_json(manifest_path, manifest)
    print(f"assembled panels={len(records)} versions={len(by_version)} pdf={pdf}")


def show_status(args: argparse.Namespace) -> None:
    manifest = load_manifest(args.manifest.expanduser().resolve())
    counts = defaultdict(int)
    for job in manifest["jobs"]:
        for version in job["versions"]:
            counts[version["status"]] += 1
    errors = manifest.get("errors", [])
    print(json.dumps({
        "run_id": manifest["run_id"], "mode": manifest["mode"], "status": manifest["status"],
        "jobs": len(manifest["jobs"]), "versions": dict(counts),
        "latest_error": errors[-1] if errors else None, "deliverables": manifest["deliverables"],
    }, ensure_ascii=False, indent=2))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--source", type=Path, required=True)
    init.add_argument("--output", type=Path, required=True)
    init.add_argument("--mode", choices=tuple(MODE), required=True)
    init.add_argument("--run-id", required=True)
    init.add_argument("--work", required=True)
    init.add_argument("--versions", type=int, default=2)
    init.add_argument("--project-name")
    init.add_argument("--assets-json", type=Path)
    init.set_defaults(function=init_run)

    record = commands.add_parser("record-native")
    record.add_argument("--manifest", type=Path, required=True)
    record.add_argument("--job", required=True)
    record.add_argument("--version", required=True)
    record.add_argument("--file", type=Path, required=True)
    record.add_argument("--chat-url", required=True)
    record.add_argument("--native-card-evidence", required=True)
    record.add_argument("--download-url")
    record.add_argument("--replace", action="store_true")
    record.set_defaults(function=record_native)

    reject = commands.add_parser("reject")
    reject.add_argument("--manifest", type=Path, required=True)
    reject.add_argument("--job", required=True)
    reject.add_argument("--version", required=True)
    reject.add_argument("--origin", default="code-or-file-substitute")
    reject.add_argument("--reason", required=True)
    reject.set_defaults(function=reject_version)

    project = commands.add_parser("set-project")
    project.add_argument("--manifest", type=Path, required=True)
    project.add_argument("--url", required=True)
    project.set_defaults(function=set_project)

    job = commands.add_parser("set-job")
    job.add_argument("--manifest", type=Path, required=True)
    job.add_argument("--job", required=True)
    job.add_argument("--chat-url")
    job.add_argument("--branch-url")
    job.set_defaults(function=set_job)

    asset = commands.add_parser("set-asset-base")
    asset.add_argument("--manifest", type=Path, required=True)
    asset.add_argument("--scene", required=True)
    asset.add_argument("--url", required=True)
    asset.set_defaults(function=set_asset_base)

    blocked = commands.add_parser("block")
    blocked.add_argument("--manifest", type=Path, required=True)
    blocked.add_argument("--stage", required=True)
    blocked.add_argument("--reason", required=True)
    blocked.set_defaults(function=block_run)

    assemble = commands.add_parser("assemble")
    assemble.add_argument("--manifest", type=Path, required=True)
    assemble.set_defaults(function=assemble_run)

    status = commands.add_parser("status")
    status.add_argument("--manifest", type=Path, required=True)
    status.set_defaults(function=show_status)
    return root


def main() -> None:
    args = parser().parse_args()
    if getattr(args, "versions", 1) < 1:
        raise ValueError("--versions must be positive")
    args.function(args)


if __name__ == "__main__":
    main()
