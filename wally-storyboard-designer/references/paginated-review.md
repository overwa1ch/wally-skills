# 裁切与图文成品

只有用户已确认裁切或成品制作时读取。普通生图在原图交付处结束；生成步骤见 [按场景生成](chatgpt-web-visual-test-workflow.md)。

## 确认后的交付

1. 核对用户确认的范围、所选原图及文字依据。导演脚本与表演设计均可直接使用；格式按当次需求确定。
2. 按实际画格边界逐镜裁切，保持画面比例和内容；不拉伸、重画或补造镜头。必要的留白仅用于排版。核对每张切图的原场景、镜号和来源，排除重复、缺失及错配。
3. 只要求切图时，交付该范围的切图。要求完整成品时，按原场景与镜头顺序，在每个镜头文字旁附对应分镜，保留有效字段及适用的全局、场景说明。
4. 交付一个可用的完整产物，文件形式与版式按当前要求确定。镜头图片、正文和衔接须齐全；仅拼图或只列镜号的审查 PDF 不算图文成品。复核文字可读性、图文对应和翻页／滚动效果。

## 可选本地工具

[scripts/visual_test_pipeline.py](../scripts/visual_test_pipeline.py) 提供运行记录、原图登记、切图及自包含 HTML 图文成品，也保留仅图片的审查 PDF。它支持规则 3×3 故事板、2×2 分镜表的默认分页；这只是工具支持范围，不限制用户输入或交付。

从 skill 目录运行，路径用绝对路径，Python 需 Pillow；仅审查 PDF 需要 ReportLab。Codex 中可用 `load_workspace_dependencies` 返回的运行环境。

### 准备与记录

`init` 可在生成前使用，仅准备文件和记录，不上传、生图或切图。自动解析支持数字场景标题、分镜块、Shot 标题及镜号表格；表格数据行之间仅支持空白，其他插入说明需保留原稿并使用适合其结构的工具。逐场核对解析清单与原稿；不支持的结构改用适合现有材料的处理方式，不重写原稿来凑解析器。末尾的全局说明应明确提供为 `--context`，该文件亦可承载人工选定的适用全局内容。每场输入包含完整场景和上下文，不按页删减。

```bash
python3 scripts/visual_test_pipeline.py init --source SOURCE.md --output RUN_DIR --mode storyboard --run-id RUN_ID --work WORK_NAME --versions 1
python3 scripts/visual_test_pipeline.py init --source SOURCE.md --output RUN_DIR --mode shot-table --run-id RUN_ID --work WORK_NAME --assets-json ASSETS.json --versions 1
```

资产 JSON 按源场景编号映射，例如 `S01`；每项含 `id`、`name`、`path`。工具合并为一次上传清单和一个基础聊天，仍记录各场使用哪些资产。分页只增加生成任务，同场任务共享场景输入与聊天位置。

```bash
python3 scripts/visual_test_pipeline.py set-asset-base --manifest RUN_DIR/manifest.json --url ASSET_BASE_CHAT_URL
python3 scripts/visual_test_pipeline.py set-scene --manifest RUN_DIR/manifest.json --scene S01 --url SCENE_CHAT_OR_BRANCH_URL
python3 scripts/visual_test_pipeline.py record-native --manifest RUN_DIR/manifest.json --job JOB_ID --version V01 --file ORIGINAL.png --chat-url SCENE_URL --native-card-evidence EVIDENCE
python3 scripts/visual_test_pipeline.py status --manifest RUN_DIR/manifest.json
```

项目 URL 可用 `set-project` 记录，创建新 Project 不是必要步骤。`record-native` 保存原始字节与 SHA-256。`reject` 记录不可用原图；`block` 记录失败位置与原因。

### 裁切与输出

执行前确认授权范围。`--approval-note` 记录用户真实的裁切／成品授权，不由 Agent 编造；它只记录已有确认，不替代确认。

```bash
python3 scripts/visual_test_pipeline.py assemble --manifest RUN_DIR/manifest.json --format html --approval-note '用户已明确确认的裁切与图文成品要求'
```

`--format panels` 仅裁切；`html` 在每镜原文旁嵌入切图，形成一个自包含文件；`review-pdf` 输出仅图片的审查拼图与 PDF，只有用户明确要该形式时使用。其他格式由相应文档工具完成，沿用已核对的切图、原文和镜头对应关系。

工具在切图前检查原图、来源、文件完整性、镜头覆盖和同场聊天一致性。自动边界检测仍需视觉复核，合成测试不能代替真实生成图的审查。
