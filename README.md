# Wally Skills

Wally 是一套面向 AI 视频生产的模块化 Codex skills。用户说“wally”后，`wally-helper` 会加载 Wally 助手身份，记录和应用跨模块制作经验，整理材料、判断下一步并检查专业产物之间是否衔接。它知道每个专业 skill 的用途，但不能替用户调用；专业工作必须由用户明确调用对应 skill。

## 当前模块

| Skill | 当前版本 | 职责 |
| --- | --- | --- |
| `story-idea-generator` | V1.2 | 生成故事支点（灵感／创意），再以事件数轴与八要素展开万字纲；两阶段方法、案例和矩阵按需读取。 |
| `wally-helper` | V4.3 | 整理材料、记录制作经验、建议下一步、检查跨产物兼容性，并提供专业 skill 的可复制调用请求；按需返回固定 BGM 制作请求。 |
| `wally-screenplay-writer` | V2.2 | 按任务需要选择作品定义和创作方法，负责故事、人物、结构、场景、对白和剧本诊断；有依据、有作用才写，不确定时写得更少，分步开发细则按需读取。 |
| `wally-storyboard-designer` | V3.20 | 按场景生成故事板或分镜表：故事板每场独立聊天；分镜表一次上传全部资产后逐场分支，同场多页共用聊天。先交付原图，确认后按逐页选定版本裁切并制作逐镜图文成品。 |
| `wally-static-asset-designer` | V2.11 | 提示词请求交付文本；需要图片时通过内置 Browser 建立命名聊天，每项资产独立聊天；Preview 至少 8 套不同风格提示词与图像，各项资产至少 4 套不同提示词与图像，逐版生成供用户选择，并继承已选全局效果。 |
| `wally-action-designer` | V3.25 | 按场景完成整场表演与视听设计，沿用英文标签与 Shot 连续正文，字段按需选用；保留原镜号，场景时间从 0.0s 接续。 |
| `wally-visual-style-extractor` | V1.7 | 检索既有风格并提取有证据的 style layer；普通解释直接回答，结构化任务只读对应模板章节。 |

## 故事、剧本与脚本

`story-idea-generator` 负责故事支点（灵感／创意）与万字纲两个阶段；万字纲用具体事件、行动和因果展开故事，随后由 `wally-screenplay-writer` 写成剧本，再由 `wally-storyboard-designer` 设计分镜脚本。各阶段都需用户明确调用；已有材料可直接进入对应阶段。

## 安装

```bash
git clone https://github.com/overwa1ch/wally-skills.git
mkdir -p /path/to/repository/.agents/skills
cp -R wally-skills/wally-* wally-skills/story-idea-generator /path/to/repository/.agents/skills/
```

在该 repository 内新建 Codex 任务，让 Codex 只在这个项目作用域发现这些 skills。Wally 不再推荐安装到全局 user skill 目录。

全部七个 skill 都采用明确点名调用：只有用户点名对应 skill 并要求使用时才启用，普通故事、分镜、动作、资产或风格请求按常规任务处理。七份 `agents/openai.yaml` 均设置 `policy.allow_implicit_invocation: false`，关闭 Codex 的隐式调用；使用 `$wally-screenplay-writer` 等完整名称可显式加载对应 skill。

用户明确要求使用 `wally` / `wally-helper` 时加载 Helper；点名专业 skill 只启用被点名的 skill。Helper 可推荐专业 skill 并给出可复制的调用请求，由用户明确调用。

## 输出结构

- 专业产物保留所属 skill 的模板或输出合同结构。
- `story-idea-generator` 按任务交付故事支点或万字纲。灵感默认十条；万字纲以四幕组织十个事件序列，把八要素填入十序列矩阵，用能勾勒画面的事件说明人物与主题；结局单列在四幕之外。
- `wally-screenplay-writer` 按当前任务选择内容与方法；作品定义只写有依据且影响创作的项，缺项省略，整块无用时省略。四种格式按用户真实体量缩放，不强制改片长；已有稿整理和局部修改直接交付，只有用户选择分步开发或要求锁定时才使用审批菜单。原则：如果你不确定，就写得更少，而不是更多。
- `wally-storyboard-designer` 继承上游已有作品定义与场景结构，保留源场景标题或编号；按请求设计分镜脚本、交付固定绘图提示词或生成故事板／分镜表原图，确认后裁切及制作成品。用户审查创作结果，`wally-helper` 记录测试证据和批准状态。
- `wally-static-asset-designer` 的 Preview 提示词先定义图片类型，写明具体年代与地域，以精简的一段话探索明确调色或已有定义的艺术风格；艺术参照不附创作年代，不堆叠纹理与暗部细节。
- `wally-static-asset-designer` 以用户提供的参考图承载已清楚可见的规格；正式提示词保留字段名和相对顺序，不显示数字或字母序号，只补目标变化、布局、身份锚点与真实漂移风险。
- `wally-static-asset-designer` 为一个已批准基础 Pxx 的单一关键改变态提供 `Pxx-state`；场景覆盖默认九宫格，九格一致性不足或用户明确要求时可改用 `2×2` 四宫格。
- `wally-action-designer` 按已有场景拆分，一个场景完整做一场戏；每场从 `0.0s` 起算，场内接续计时，原镜号保留。沿用 `Style:`、`Reference:`、`Camera:`、`Acting:` 等英文标签与 Shot 连续正文，字段按需选用；单镜测试与合并按用户要求执行。表演设计在分镜表生成中等同于导演脚本。
- Camera 和 Shot 只按任务需要选择 capture physics、光学、稳定性、运动动机、剪辑语法、视点、前景、焦点、空间层次与时长预算；这些控制不得覆盖已批准的镜头权威。
- 原创或改写对白属于 `wally-screenplay-writer`；`wally-action-designer` 只保留已批准措辞并设计其表演、口型、停顿、声音与镜头内执行。
- `wally-visual-style-extractor` 普通解释直接回答；结构化请求按需选择 Style Lookup、Analysis Card、Three-Stage Brief、Reusable JSON Prompt 或 Transfer Validation。`subject`、`scene`、`camera` 只接受用户已有值或复用占位符。
- `wally-helper` 接受各专业产物的现有格式，按需指出材料冲突、缺件和下一步；视频提示词及参考绑定交给 `wally-action-designer`，直接使用其产物。

## 新手使用方式

直接说“wally”，然后描述想做的视频，或上传任意已有材料。Helper 会整理信息、判断下一步，并给出对应 skill 名称和可以直接复制的调用请求；用户复制请求并明确调用该 skill，再把产物带回 Wally。

## 当前推荐经验

需要挑选故事支点，或把选定方向展开成万字纲时，明确调用 `story-idea-generator`；已有万字纲或剧本时从对应阶段继续。

1. `wally-screenplay-writer` 完成可用的剧本初稿。
2. `wally-storyboard-designer` 根据完整剧本和用户指定范围制作简单故事板草稿，低成本测试景别、运镜、动作和镜头顺序；故事问题交回 Screenplay，镜头问题交回 Storyboard，Helper 记录测试与批准状态。
3. `wally-static-asset-designer` 先生成符合剧本整体调性的 Preview 候选，由用户选择全局效果；再生成各项资产候选，由用户逐项选定。场景九宫格一致性不足时，建议用户选择 `2×2` 四宫格。
4. `wally-storyboard-designer` 用导演脚本／表演设计和静态资产生成分镜表：一次上传全部静态资产后，每场建一个分支。按当次图数与版本要求交付原图供用户审查；裁切与完整图文成品经确认后执行。
5. `wally-action-designer` 设计动作、表演、摄影、光影和声音执行。
6. 需要复核材料衔接或判断下一步时，返回 `wally-helper`。

`wally-helper` 从开始到结束持续陪同；上面的顺序是当前经验建议，不是专业 skill 的调用前提。`wally-visual-style-extractor` 可在任何需要锁定或复核视觉风格的阶段按需使用。实际顺序以当前材料和交付目标为准。

## 健康检查

仓库的 `validate-wally-skills` GitHub Actions job 会检查七项 frontmatter、引用完整性、跨模块合同、公开安全和冻结提示词 hash。也可在本地运行：

```bash
python -m pip install Pillow reportlab
python scripts/validate_wally_skills.py --skills-root .
python -m unittest discover -s tests -p 'test_*.py' -v
python -m unittest discover -s wally-storyboard-designer/tests -p 'test_*.py' -v
```

## 仓库迁移

原独立仓库已分别更名为 `overwa1ch/deco-helper-deprecated` 和 `overwa1ch/deco-helper-storyboard-deprecated`，并转为 Private，从公开列表隐藏。它们只保留历史内容，不再作为当前版本来源。本仓库是 Wally 系列唯一公开的主发布仓库。

这里的 `wally-helper/` 仍是 Wally 系列中的有效协调模块；废弃并隐藏的是原先单独发布它的旧 GitHub 仓库。

## License

[MIT](LICENSE)
