# Wally Skills

Wally 是一套面向 AI 视频生产的模块化 Codex skills。用户说“wally”后，`wally-helper` 会加载 Wally 助手身份，记录和应用跨模块制作经验，整理材料、判断下一步并检查专业产物之间是否衔接。它知道每个专业 skill 的用途，但不能替用户调用；专业工作必须由用户明确调用对应 skill。

专业 skills 是可独立、随时取用的工具，直接承接当前材料并交付指定产物。Helper 根据具体问题提供流程与测试建议，用户可直接调用任何工具。

## 当前模块

| Skill | 当前版本 | 职责 |
| --- | --- | --- |
| `story-idea-generator` | V1.2 | 生成故事支点（灵感／创意），再以事件数轴与八要素展开万字纲；两阶段方法、案例和矩阵按需读取。 |
| `wally-helper` | V4.6 | 整理材料、记录制作经验、判断流程与测试需要、检查跨产物兼容性，并提供专业工具的可复制调用请求；按需返回固定 BGM 制作请求。 |
| `wally-screenplay-writer` | V2.4 | 按任务需要选择作品定义和创作方法，负责故事、人物、结构、场景、对白和剧本诊断；有依据、有作用才写，不确定时写得更少，分步开发细则按需读取。 |
| `wally-storyboard-designer` | V4.1 | 按需设计或修订分镜、制作或修订白模视频、绘制场景布局及检查提示词污染。各功能分别取用；新分镜沿用先听用户讲述关键画面的设计方法。 |
| `wally-asset-designer` | V3.11 | 按当前范围与数量提供图片资产、可选人物动态参考或白模视频参考；动态参考以 Cxx 提供造型，左格展示动作与局部，右格展示表情与声音，可结合已有对白作简短表演。图片保留类型合同，逐条独立提交并归档，由人审查；不自动扩成候选包。 |
| `wally-camera-designer` | V1.5 | 设计镜头、时间线、参考绑定、摄影、灯光、成像和声音空间，组装十段完整视频提示词。 |
| `wally-performance-designer` | V1.0 | 设计人物任务、策略、倾听、互动与逐拍表演；按复杂程度分简单、标准和完整三档。 |
| `higgsfield-fight-scene` | V2.4 | 按需点名的近身打斗入口，保留原作者技能及知识库，分拍交给摄影与成像组装。 |
| `wally-visual-style-extractor` | V1.7 | 检索既有风格并提取有证据的 style layer；普通解释直接回答，结构化任务只读对应模板章节。 |

## 故事、剧本与脚本

`story-idea-generator` 提供故事支点（灵感／创意）与万字纲，`wally-screenplay-writer` 提供剧本创作、修订与诊断，`wally-storyboard-designer` 提供分镜等镜头产物。按当前需求明确调用，各自接受已有材料。

## 安装

```bash
git clone https://github.com/overwa1ch/wally-skills.git
mkdir -p /path/to/repository/.agents/skills
cp -R wally-skills/wally-* wally-skills/story-idea-generator wally-skills/higgsfield-fight-scene /path/to/repository/.agents/skills/
```

在该 repository 内新建 Codex 任务，让 Codex 只在这个项目作用域发现这些 skills。Wally 不再推荐安装到全局 user skill 目录。

从旧版升级时，用 `wally-asset-designer/` 替换项目安装目录中的 `wally-static-asset-designer/`，调用名称同步改为 `$wally-asset-designer`；避免同时保留两个入口。

从旧版升级时，清除安装目录中的 `wally-action-designer/`、`wally-action-designer-v329/` 和 `wally-action-designer-v354/`。以后只使用 `$wally-camera-designer` 与 `$wally-performance-designer` 这一套拆分版；需要近身打斗时明确点名 `$higgsfield-fight-scene`。

升级已安装的 skill 时完整替换对应目录，清除新版已经移除的资源；项目自行修改过的副本先核对差异。

全部九个入口都采用明确点名调用：只有用户点名对应 skill 并要求使用时才启用，普通故事、分镜、动作、资产或风格请求按常规任务处理。九份入口 `agents/openai.yaml` 均设置 `policy.allow_implicit_invocation: false`，关闭 Codex 的隐式调用；使用 `$wally-screenplay-writer` 等完整名称可显式加载对应 skill。

用户明确要求使用 `wally` / `wally-helper` 时加载 Helper；点名专业 skill 只启用被点名的 skill。Helper 可推荐专业 skill 并给出可复制的调用请求，由用户明确调用。

## 输出结构

- 专业产物保留所属 skill 的模板或输出合同结构。
- `story-idea-generator` 按任务交付故事支点或万字纲。灵感默认十条；万字纲以四幕组织十个事件序列，把八要素填入十序列矩阵，用能勾勒画面的事件说明人物与主题；结局单列在四幕之外。
- `wally-screenplay-writer` 按当前任务选择内容与方法；作品定义只写有依据且影响创作的项，缺项省略，整块无用时省略。四种格式按用户真实体量缩放，不强制改片长；已有稿整理和局部修改直接交付，只有用户选择分步开发或要求锁定时才使用审批菜单。原则：如果你不确定，就写得更少，而不是更多。
- `wally-storyboard-designer` 继承已有作品定义、场景与镜号，按请求交付分镜脚本、白模视频或布局等指定产物；用户反馈后定向修订。白模定义沿用 Asset，具体表演由视频模型补全。
- `wally-asset-designer` 的单幅效果图使用“整体风格＋构图描述”，保留当前图片所需的图片类型、文化信息、视觉要求与构图；风格参考按用户说明绑定，实际效果由人审查。
- `wally-asset-designer` 根据文字材料、用户说明和已选记录绑定参考图；正式提示词保留字段名和相对顺序，不显示数字或字母序号，只补目标变化、布局、身份锚点与有依据的漂移风险。Agent 核对任务回执、文件关联与元数据，图像内容和效果由人判断。
- `wally-asset-designer` 的 Cxx 使用16:9整页，左侧为包含完整头部的正背面全身视图，传达已确认的头身比；右侧为面部特写，每个候选以完整提示词一次生成；Cxx 按实际附件用途选择参考绑定，无参考图时依据文字设定创作；服装写具体可见形态，姿态与神态按角色需要填写。Sxx 采用 Higgsfield 场景提示词组织方式：场景正文＋CAMERA／LIGHTING／COLOR／STYLE，文化信息融入建筑、材料与陈设，NEGATIVE 放在末尾；不适用项省略。基础 Pxx 与 Pxx-state 均为16:9单一主视图，每个目标状态独立一图并使用已选基础道具参考。Cxx-Lxx 场景角色状态模板已弃用。场景覆盖默认九宫格，九格一致性不足或用户明确要求时可改用 `2×2` 四宫格。
- `wally-asset-designer` 的白模定义与几何体约定见[白模视频参考](wally-asset-designer/types/whitebox-video.md)。
- `wally-asset-designer` 的[动态角色参考](wally-asset-designer/types/dynamic-character-video.md)是可选项，不作为后续制作的前置条件，也不在静态角色页后自动追加；已有图片参考或文字设定足够时直接继续。选择制作时默认10秒、左右双格。静态 Cxx 页提供人物造型，视频重新组织画面；左格开头约2–3秒展示动作及正背面，其余时间切换具体局部，右格以可自然转头、切近的正面近景展示表情、声音与同步口型。双格位置保持，格内景别和内容可变化，两格独立展示。沿用已有对白与实际声音素材；[通用提示词](wally-asset-designer/templates/dynamic-character-reference-10s.txt)独立保存。
- `wally-camera-designer` 采用 REFERENCE、FORMAT、STYLE、CAMERA、ACTING TASKS、THE SHOT、SPOKEN LINE、LIGHT、AUDIO、NEGATIVE 十段格式，不适用项省略。每场从 `0.0s` 起算，保留原镜号、机位、景别和朝向，具体动作与摄影执行进入 THE SHOT。场景参考决定空间、材质、陈设与光照特征，机位与构图以提示词为准；默认一个地点一张参考，另一面有戏时才增补。
- `wally-performance-designer` 保留完整动作粒度，融合场景事件、动机、目标、阻碍、策略和反馈。简单、标准、完整三档按任务选择；完整档先交设计说明供用户确认。ACTING TASKS 写意图层，逐拍表演只写入 THE SHOT；台词原文、声音身份与已确认调度保持。
- 未指定画幅与成像方向时，Camera 与 Asset 的 Sxx 使用 2.39:1 和变形宽银幕 35mm 胶片观感；平台没有该比例时选 21:9。用户指定、项目当前风格、风格参考和已确认稿件优先。视频画面有明亮实际光源时才写轻微横向光条，并明确光源；场景参考图默认不带光条。
- `higgsfield-fight-scene` 只在用户点名时使用，提供近身接触动作及受击反应。截拳道／咏春套路仅在选定时采用；枪战、追逐和普通推搡由对应专业工具处理。第三方源文件及归属见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
- Camera 和 Shot 只按任务需要选择 capture physics、光学、稳定性、运动动机、剪辑语法、视点、前景、焦点、空间层次与时长预算；这些控制不得覆盖已批准的镜头权威。
- 原创或改写对白属于 `wally-screenplay-writer`；`wally-performance-designer` 设计已批准措辞的表演、口型与停顿，`wally-camera-designer` 负责时序、声音位置和声学执行。
- `wally-visual-style-extractor` 普通解释直接回答；结构化请求按需选择 Style Lookup、Analysis Card、Three-Stage Brief、Reusable JSON Prompt 或 Transfer Validation。`subject`、`scene`、`camera` 只接受用户已有值或复用占位符。
- `wally-helper` 接受各专业产物的现有格式，按需指出材料冲突、缺件和下一步；剧情镜头的视频提示词及参考绑定交给 `wally-camera-designer`，人物表演由 `wally-performance-designer` 设计，动态角色参考由 `wally-asset-designer` 承接。

## 新手使用方式

直接说“wally”，然后描述想做的视频，或上传任意已有材料。Helper 会整理信息、判断下一步，并给出对应 skill 名称和可以直接复制的调用请求；用户复制请求并明确调用该 skill，再把产物带回 Wally。

## 流程与测试建议

制作顺序、视觉质感确认及其他测试判断统一维护在 [Helper 指南](wally-helper/references/workflow-guide.md)。专业工具保留各自的方法、真实素材依赖和交付范围；用户可随时取用，无需先完成其他工具的工作。

## 健康检查

仓库的 `validate-wally-skills` GitHub Actions job 会检查八项 Wally 模块及近身打斗入口的 frontmatter、引用完整性、跨模块合同、公开安全和冻结提示词 hash。也可在本地运行：

```bash
python scripts/validate_wally_skills.py --skills-root .
python -m unittest discover -s tests -p 'test_*.py' -v
node --test wally-asset-designer/tests/test_cua_payload.cjs
```

## 仓库迁移

原独立仓库已分别更名为 `overwa1ch/deco-helper-deprecated` 和 `overwa1ch/deco-helper-storyboard-deprecated`，并转为 Private，从公开列表隐藏。它们只保留历史内容，不再作为当前版本来源。本仓库是 Wally 系列唯一公开的主发布仓库。

这里的 `wally-helper/` 仍是 Wally 系列中的有效协调模块；废弃并隐藏的是原先单独发布它的旧 GitHub 仓库。

## License

Wally 原创部分采用 [MIT](LICENSE)。第三方来源与适用范围见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)，第三方归档原文不纳入 Wally 的 MIT 授权。
