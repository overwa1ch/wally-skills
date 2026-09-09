# ChatGPT Web Visual Test Workflow

Use this only when the user asks the skill to execute a storyboard or shot-table test on ChatGPT Web. Use the in-app Browser and the existing signed-in ChatGPT session. Do not switch to Chrome.

Run the packaged [visual_test_pipeline.py](../scripts/visual_test_pipeline.py) for initialization, native-image registration, strict assembly, and status reporting; do not recreate these mechanics in a project-local script. Set the command working directory to the directory that contains this skill's `SKILL.md`; pass absolute source, asset, output, and manifest paths. Use a Python environment that provides Pillow and ReportLab. In the Codex app, use the Python path returned by `load_workspace_dependencies` when the default `python3` lacks them.

## 脚本输入要求

这些是本流程的解析要求，仅执行网页测试时检查。只索要固定提示词的请求不经过此检查。

| 输入 | 当前脚本可直接读取的形式 |
| --- | --- |
| 导演脚本 | UTF-8 Markdown；场景标题单独成行，如 `## 场景1：院子 / 清晨`，编号为数字，冒号可为 `：` 或 `:`，冒号后有标题。 |
| 镜头块 | 如 `分镜1｜镜头类型：主镜`，也接受前缀 `### `；数字后使用全角 `｜`，镜头正文持续到下一镜或该场景结束。 |
| 表格镜头 | 如 `\| 01 \| 动作一 \|` 或 `\| 镜01 \| 动作一 \|`；每个镜头独占一行，首列是数字镜号；分页只保留数据行，不携带表头。 |
| 分镜表资产 | JSON 以场景编号映射为键，如 `S01` 对应源场景1；每个场景须有非空数组，每项包含 `id`、`name`、`path`，且文件真实存在。故事板模式无需资产 JSON。 |

每场至少有一个可识别镜头；场景数字编号须唯一，同场镜号须唯一（`1` 与 `01` 按同一数字处理）。标题行和表格行须以换行结束。`S01` 等仅用于运行清单及资产映射，不替换原场景标题。

初始化前核对当前材料的全部场景与镜头：同场混用镜头块和表格时，脚本只取镜头块；不匹配的标题或行可能被跳过，场景内另一个二级标题会截断该场景的读取。不能用“命令未报错”代替完整性检查。初始化后将 manifest 中的场景顺序、镜号和分页包逐项对回源材料，确认无遗漏再上传。

格式不匹配时，指出具体标题、镜号或表格位置以及解析限制，暂停依赖它的执行；不得改写标题、重编号、补造场景或镜头来适配脚本。已有明确结构但解析器不支持时，向用户请求扩展解析支持或提供兼容材料的处理方向；真正缺少场景边界或镜头内容时，只报告缺失输入，创作工作另按用户请求处理。不要把执行请求悄悄降级为让用户自行去网页粘贴提示词。

## Prepare

1. Initialize the run with the packaged script. It mechanically reads existing scene headings and paginates shots in source order: storyboard `3×3` (up to 9 shots), shot table `2×2` (up to 4 shots). Each page packet contains the original scene heading plus only that page's original shot blocks. Do not copy a work preamble or scene-level metadata into a partial page packet, because total-shot declarations can make the image model add off-page shots. Do not form, split, rename, rewrite, or reorder source scenes or shot blocks.

   ```bash
   python3 scripts/visual_test_pipeline.py init --source DIRECTOR.md --output RUN_DIR --mode storyboard --run-id RUN_ID --work WORK_NAME
   python3 scripts/visual_test_pipeline.py init --source DIRECTOR.md --output RUN_DIR --mode shot-table --run-id RUN_ID --work WORK_NAME --assets-json ASSETS.json
   ```

   路径占位符须换成真实绝对路径；`RUN_DIR` 使用新的运行目录，已有 manifest 时脚本拒绝覆盖。按用户要求用 `--versions N` 指定每页版本数，`N` 为正整数；未指定时脚本默认两版。
2. Create one identifiable ChatGPT Project for the selected mode and apply the generated `browser/project-instructions.txt` as its Project instructions. For storyboard, create one chat per page packet and upload only that packet. For shot table, first create one asset-base chat per scene, upload the scene's static assets, state the exact name-to-file mapping using the generated scene mapping file, then branch once per page packet from the confirmed asset base.
3. Work in parallel only across independent page chats or branches. Once the user has authorized the materials, mode, and destination, continue through upload, generation, download, crop, and assembly without step-by-step confirmation.

Record the corresponding Web locations as soon as they exist:

```bash
python3 scripts/visual_test_pipeline.py set-project --manifest RUN_DIR/manifest.json --url PROJECT_URL
python3 scripts/visual_test_pipeline.py set-asset-base --manifest RUN_DIR/manifest.json --scene S01 --url ASSET_BASE_CHAT_URL
python3 scripts/visual_test_pipeline.py set-job --manifest RUN_DIR/manifest.json --job JOB_ID --chat-url STORYBOARD_CHAT_URL
python3 scripts/visual_test_pipeline.py set-job --manifest RUN_DIR/manifest.json --job JOB_ID --branch-url SHOT_TABLE_BRANCH_URL
```

Use `--chat-url` for a storyboard page chat. Use `set-asset-base` for the shot-table asset-base chat and `--branch-url` for a shot-table page branch. `record-native` also fills the page chat or branch URL from `--chat-url` when it has not already been recorded.

## Generate versions

1. After the page packet is attached, place `prompts/short.txt` first and `prompts/template.txt` immediately after it in one composer submission. These are extracted from the selected fixed template; keep both labeled payloads verbatim and in their stored order. Do not include the template file's explanatory prose or submit the short-task payload by itself: it can trigger an image before the style template arrives.
2. The first response produces `V01`. For each later version, send: `按相同材料和相同模版再生成1个独立版本。本次只生成1张图像，不要把多个版本拼在一张图里。`
3. A version is valid only when ChatGPT returns one native generated-image card for that turn and the card itself contains exactly one requested grid. If several versions appear inside one image, retry that version once in a clean chat or branch.

## Native-image gate

- Download only through the native generated-image card (`Edit image` / `Share this image` context). The downloaded image must be the same depicted image shown on that card.
- Reject every PNG, PDF, SVG, canvas, or other file supplied through a normal file/download button after Python, code interpreter, shell, or another document-building tool ran. Correct dimensions, labels, or grid geometry do not make such a substitute acceptable.
- If a response contains both a native generated-image card and separate downloadable files, ignore the separate files. If the native card cannot be downloaded as the original image, mark the version incomplete; do not substitute a screenshot or code-generated file.
- Before accepting a version, compare the downloaded image with the visible native card. The shot drawings, poses, props, arrows, and overall line character must be the same. Record the chat URL, version, native-card evidence, downloaded filename, and SHA-256.
- For storyboard, reject a surface that has changed from loose black sketch lines into uniform geometric diagrams. For shot table, reject a surface that does not use the uploaded static assets as its visual source. These are technical intake checks; the user still judges storytelling and visual quality.

Register each accepted native original immediately; the command copies the original bytes into the run and records its SHA-256:

```bash
python3 scripts/visual_test_pipeline.py record-native --manifest RUN_DIR/manifest.json --job JOB_ID --version V01 --file DOWNLOADED_IMAGE --chat-url CHAT_URL --native-card-evidence EVIDENCE
```

For a rejected substitute, record the rejection instead of downloading it into the accepted source set:

```bash
python3 scripts/visual_test_pipeline.py reject --manifest RUN_DIR/manifest.json --job JOB_ID --version V01 --reason REASON
```

## Crop and assemble

1. After the native-image gate passes, local code may only locate visible grid boundaries, crop the cells, add white padding when needed to normalize each extracted cell to 16:9, add review-page labels outside the cells, and assemble them in original scene/shot order. Never stretch a cell.
2. Local code must not redraw, trace, simplify, replace, retouch, or regenerate any person, action, prop, location, arrow, caption, or shot content.
3. Keep storyboard and shot-table outputs separate. Missing versions or shots remain explicit missing slots and keep the run incomplete.
4. Deliver original native images, assembled review images, the manifest/provenance report, and the review PDF. No step automatically approves a storyboard, shot table, director script, or static asset.

After every expected version is registered, run strict assembly. It fails before cutting when the Project URL, required chat or branch URL, confirmed asset base, version, native-card evidence, asset hash, or image hash is missing or invalid.

```bash
python3 scripts/visual_test_pipeline.py assemble --manifest RUN_DIR/manifest.json
python3 scripts/visual_test_pipeline.py status --manifest RUN_DIR/manifest.json
```

## Failure handling

- Suspected benign safety false positive: click the original response's Retry without changing the supplied story material. If it still fails or no retry exists, record the stop point.
- Wrong grid, combined versions, extra/missing shots, or wrong canvas ratio: retry the affected version once in the same page chat when the materials are still clean; otherwise retry from a clean chat or the confirmed asset-base branch. State only the violated mechanical constraint and keep the fixed prompt payloads unchanged.
- Code/file substitute, inaccessible native original, login, quota, or changed page structure: stop that version and report the exact failure. Never silently replace the required native image.

Record a run-level stop that occurs before a specific version can be accepted or rejected:

```bash
python3 scripts/visual_test_pipeline.py block --manifest RUN_DIR/manifest.json --stage STAGE --reason REASON
```
