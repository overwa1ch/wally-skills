# Changelog

## 2026-09-08

- Wally Helper 升级为 V4.1：在用户请求时原样返回已批准的一句话 BGM 制作请求，其余流程、专业边界与 Route A/B 组装合同保持不变。
- Action 升级为 V3.21：清理旧示例，入口收束为任务路由与职责交接；导演正文合同、制作方法与回片审查按需读取，已批准台词、Shot 与 Audio 合同保持不变。
- Static Asset 升级为 V2.9：删除七类资产中重复模板、偏向同一写实年代设定的完整旧示例，保留正式字段和全部固定几何 / 呈现块；通用写法仅保留两个局部短例。肤质与造型审查按所选媒介和风格判断，不再把漫画化本身当成错误。
- 规划文件只维护资产取舍与类型路由，具体依赖归各类型文件，共用契约只维护跨类型提示词规则；视觉方案模板区分剧本硬约束、Preview 待探索范围和已有选定风格。画幅、上传与权重控件的核实统一进入浏览器流程，按实际能力操作并记录，不假定平台存在固定控件。
- V2.9 保留 Preview 至少 8 版、各资产至少 4 版、独立命名聊天、逐版生成、用户选择和原图验收；九宫格 / 四宫格固定基础句逐字节不变，校验器与测试改从类型文件检查相应路由。
- Static Asset 升级为 V2.8：Preview 至少 8 套不同完整提示词与独立图像方向，均符合剧本整体调性；用户看图选择后再锁定全局 `style_aesthetic`，不先锁唯一风格再只出一张 Preview。
- 每项正式资产及九宫格 / 四宫格至少 4 套不同提示词与独立图像，继承已选全局效果与基础参考，依次生成整组供用户选择；重复提示词、技术重试及合并多版本的单张图不充数。
- ChatGPT Web 按制作批次新建命名 Project，Preview 与每项资产分别新建命名聊天，衍生资产显式上传选定基础图；新候选轮次单独留档，中断恢复复用原项目和进度。
- 浏览器流程补齐逐版原图验收、一次技术重试、候选不足的停止条件与用户选图记录；移除固定旧 Browser skill 名称依赖。技术评审与用户选择分开，不自动批准或越过选图步骤。
- Preview 模板改为逐方向填写；九宫格 / 四宫格保留原固定基础句，新增每版覆盖重点以支持不同完整提示词。入口按任务路由，具体规则留在对应参考文件，新增候选生成记录模板。
- Storyboard 升级为 V3.17：按渐进式披露整理入口，只保留职责、共用约束与按任务读取表；作品定义细则归入导演脚本合同，历史版本记录合并至本日志。
- 两套模板只维护固定正文与使用边界；网页发送方式统一由 ChatGPT Web 流程维护，短任务与生成模版在同一条消息中按顺序提交。四个固定正文块逐字节不变。
- Web 流程补齐脚本实际支持的场景标题、镜头块、表格行和资产映射格式，以及完整性核对、格式不匹配处理和生成文件的使用位置；脚本功能与原图门禁不变。

## 2026-09-02

- Storyboard 升级为 V3.16：把 ChatGPT Web 视觉测试完整落进 skill；新增可复用的运行初始化、场景原样切片、3×3 / 2×2 分页、场景资产底座登记、原生图片证据与 SHA-256、严格切格、按镜号重组、长图和审查 PDF 脚本。
- Storyboard V3.15 加入内置 Browser 的 ChatGPT Web 测试流程：故事板与分镜表每个生图回合只生成一个独立版本，后续版本用固定追发语句触发，避免多个版本被合并进同一张图或被代码生成文件替代；下载原图后只允许裁切与重组。
- 拼接门禁只接受与可见原生生图卡一致的下载原图；缺图、拒收、证据不足、哈希变化、错误网格或非 16:9 画格均停止组装，不再用截图或代码绘图补位。

## 2026-08-30

- Storyboard V3.14 将固定机位设为默认；每镜不再强制填写运镜，只在需要时写明摄影机运动。

## 2026-08-29

- Storyboard 升级为 V3.13：固定分镜表提示词替换为用户确认的新版本，先输出【短任务提示词】，再单独输出【分镜表生成模版】；删除场景标题占位符与运行时替换。
- 分镜表短任务明确以导演脚本为分镜的唯一依据、以静态资产为视觉效果的唯一依据；生成模版只要求数字镜头序号、无文字描述和逐格 16:9。
- Storyboard 升级为 V3.12：固定故事板提示词替换为用户确认的新版本，先输出【短任务提示词】，再单独输出【故事板生成模版】；短任务不再包含场景标题占位符，运行时逐字照发，不做任何替换。
- 新故事板模版明确采用粗略导演分镜手稿、简单 2D 草图、红色取景框与关键动作 / 运镜箭头、逐格中文说明和逐格 16:9；分镜表提示词及其源场景标题替换规则保持不变。

## 2026-08-22

- Static Asset V2.7 将 Preview、正式资产与场景参考图的默认执行入口改为内置 Browser 中的 ChatGPT Web，提示词内部保存，生成图下载、审查并归档；此版本原记录由 skill 入口迁入本日志。
- Storyboard 升级为 V3.11：把 `画面内容` 从一句提示升级为正式字段合同。默认只写一个主要主体和一个核心可见动作或状态；第二主体、前景、背景和道具仅在承担镜头任务时加入；所有名词必须落在景别与正向取景边界内；抽象解释归入 `任务`，摄影控制归入 `拍摄手法`；运动镜头只补必要的可见内容变化，并以删词测试收口。
- 固定故事板与分镜表提示词保持逐字节不变；公共校验器、匿名合同测试和 README 版本同步为 V3.11。

## 2026-08-19

- Storyboard 升级为 V3.10：新增按需的提示词污染检查——由干净上下文 agent（subagent，或用户新开对话粘贴固定检查提示词）只看镜头块，逐镜判断越框与过密，只回删词建议；默认不触发，用户提出才生效；写分镜的 agent 不得自查，修改走定向修订。
- Storyboard 升级为 V3.9：场景布局 SVG 合同收敛为四条规则——使用显式源场景、只画初始状态、只画活跃交互内容、保持真实俯视几何；删除机位连续性构造与视觉层级指令。SVG 只在用户明确发起新的空间规划任务时创建，已停止或删除的 SVG 请求不延续到后续轮次。
- Storyboard V3.1 将场景布局收敛为人物起始位置和正在物理交互的环境、物件，省略被动背景与地点说明锚点；同日后续版本在此基础上形成四条规则。
- Storyboard 分镜脚本合同精简为三字段镜头块 `拍摄手法（景别 + 机位 + 按需焦段/光学 + 运镜） / 画面内容 / 任务`，拍摄角度并入机位，删除 `动作`、`锚点` 字段与逐项运镜细则；顶部并列两条原则「一切为了讲故事，内容是优先级最高的评判标准」与「如果你不确定，就写得更少，而不是更多」，并写明分镜思路：先找关键画面并各写成一个镜头（主镜），再衔接、用同一格式把分镜设计完。
- 校验器、匿名合同测试与 README 随 V3.9 同步：版本串、SVG 四条规则钉句、README 表。
- 删除冗余的 `storyboard-style-contract.md`：canonical 15 行样式块的唯一权威回到冻结的固定故事板模板本身，校验器改为直接从模板内提取样式块校验 hash，模板逐字节不变。

## 2026-08-18（第二次）

- Storyboard 升级为 V3.0，定位收敛为测试层：设计分镜脚本（处理版导演脚本），再给出固定故事板 / 分镜表提示词供用户快速看图判断是否符合预期；用户看图后的观察作为分镜脚本定向修订的输入交回。
- Storyboard 删除视觉优化、分镜设计、多 agent 主镜对抗裁决、回图审查、内部连续性校验五项功能及其指南文件（`visual-optimization-rules.md`、`storyboard-design.md`、`main-shot-adjudication.md`、`storyboard-review.md`、`continuity-validation-rules.md`）；`ai-video-composition-rules.md` 的首帧层次与锚点并入镜头格式后删除。
- Storyboard 分镜脚本立原则「一切为了讲故事，内容是优先级最高的评判标准」，原则置于导演脚本合同顶部，选镜只依据该原则；SKILL.md 改为流程口吻（设计分镜脚本 → 固定测试提示词 → 用户看图 → 定向修订）；导演脚本合同收缩为镜头格式合同：取消固定文档骨架与状态行，镜头块为 `拍摄手法 / 画面内容 / 任务`，另立核心原则「如果你不确定，就写得更少，而不是更多」，时长仅在用户给预算时写，另含根据回板观察做定向修订的规则。
- Storyboard 样式合同文件收缩为 canonical 样式块的唯一权威来源，15 行样式块逐字节不变，固定故事板与分镜表模板逐字节不变；校验器与匿名合同测试同步改为检查已退役指南零残留。
- Helper 仅同步 Storyboard 功能菜单与测试说明措辞（去掉视觉优化、分镜设计、回板审查与文字连续性校验，回板由用户看图判断），版本保持 V4.0。

## 2026-08-18

- Screenplay 升级为 V2.0，正式收敛为四种格式：1–3 分钟概念超短片、5–10 分钟叙事短片、约 90 分钟长片和多集剧集；1–3 分钟完整人物 / 事件叙事或 3–5 分钟叙事必须先确认概念化或扩展路线。
- Screenplay 统一为叙事类八步、概念超短片三步；剧集按阶段 A 季度规划、阶段 B 分集大纲、阶段 C 逐集八步推进。已有材料从当前可用阶段继续，所有步骤号与参考资料重新对齐。
- Screenplay 继续保存六字段作品定义、持有原创 / 改写对白与诊断职责，并由入口文件唯一维护中间审批和最终锁定菜单。
- Screenplay 的统一菜单改为按当前交付范围批准：分批场景写作在本步骤内继续，定向改写只锁定指定段落；格式外实际体量复用最接近的方法路线，不增加第五条流程。
- Helper 升级为 V4.0，Storyboard 升级为 V2.1；剧本已有场景结构与源场景标题或编号成为唯一分镜叙事边界，分镜流程不再创建另一层故事分段。
- Storyboard V2.0 将场景布局、导演脚本、分镜设计、固定故事板提示词和固定分镜表提示词统一为继承源场景边界、原始标题和顺序；当时的固定提示词以源场景标题占位符定位，执行时保留原始标题或编号。
- Storyboard V2.1 在源场景内部增加盲选、多 agent 对抗质询与删除 / 合并检验，以证据裁定主镜集合；该流程不创建新的场景层级。
- Helper 的 Route A/B 组装改为单一当前生成范围，binding 合同升级为 `wally-reference-bindings/v2`；每项只保留五个资产字段，不保留范围字段，并拒绝旧格式。
- 固定提示词、冻结面、验证器、匿名 fixtures 与合同测试随场景权威迁移同步更新，并新增旧概念零残留检查。
- Action 与 Static Asset 仅清理旧边界措辞，专业职责和现有版本保持不变；Visual Style 的场景和镜头职责不变。

## 2026-08-03

- Deco 系列正式更名为 Wally Skills；六个 skill 的目录名、frontmatter、内部 handoff、验证脚本、测试和 CI job 统一使用 `wally-*`。
- Helper 升级为 V3.12，显式身份触发词从 `deco` 切换为 `wally`，并继续维持 specialist 必须由用户明确调用的边界。
- 默认安装方式从全局 user skills 调整为 repository 内的 `.agents/skills`，避免无关项目加载整套 Wally metadata。
- 为六个 skill 补齐 `agents/openai.yaml` UI metadata，并保留原有合同、冻结模板和专业职责。
- 合并全局安装中尚未发布的 Action V3.9：Camera 按 capture physics、光学、稳定性、运动动机与剪辑语法自适应组装；Shot 按视点、轴线、前景、焦点、空间层次、动作落点和时长预算选择必要控制，且不覆盖已批准镜头权威。

## 2026-07-28

- Helper V3.11、Screenplay V1.7 与 Storyboard V1.19 完成跨模块合同修复；Static Asset V2.6、Action V3.8 与 Visual Style V1.6 保持不变。
- Helper 保存故事板对整体节奏和粗镜头设计的验证状态，并把板测暴露的镜头修改明确交回 `wally-storyboard-designer`，再根据返回的更新版导演脚本推进最终批准。
- Screenplay 新增作品定义与 1–3 分钟叙事超短片路线；叙事超短片使用可见选择、让步或关系变化，不强制完整 Want / Need / Arc，3–10 分钟叙事短片继续完成完整 A→B 弧光。
- Storyboard 保持按需专业功能，继承上游作品定义，不持有跨模块 full-chain 生命周期或批准 Gate；canonical storyboard style、固定故事板模板与固定分镜表模板逐字节不变。
- 公共健康检查和匿名合同测试覆盖 specialist handoff、叙事超短片缩放、作品定义继承、Storyboard 生命周期边界和既有冻结面。

## 2026-07-22

- 六项 skill 完成协调健康修复：Helper V3.9、Screenplay V1.5、Storyboard V1.16、Static Asset V2.6、Action V3.8 与 Visual Style V1.6。
- Helper 对齐 Action 的无BGM、明确音乐、绝对静音三分支，新增 Route A validator 并补全 Route B 的正文保护、故事板排除、占位符、Audio 和资产清单检查；Route A/B 固定模板逐字节不变。
- Screenplay 统一八步名称与编号，允许已有材料直接进入对应产品，明确拥有原创 / 改写对白，并把审批菜单收口为单一来源。Action 只负责已批准台词的表演、口型、停顿、声音和镜头执行。
- Storyboard 接受任意阶段与混合材料，区分单产品 / full-chain Scene SVG 路由，删除失效 handoff 与冗余 READY Gate，并统一固定故事板 / 分镜表的旧分段占位符运行时替换；canonical style 和两个固定模板未改。
- Static Asset 新增 `Pxx-state` 与 `2×2` 四宫格场景 fallback；现有 Preview、视觉方向和九宫格固定提示词未改。Visual Style 收紧为 style layer，Established style 必须有来源与匹配强度，Analysis Card 只保留一个 Evidence strength owner。
- 新增无第三方依赖的公共健康检查、匿名合同 fixtures 与 `validate-wally-skills` GitHub Actions status check。
- `wally-action-designer` 升级为 V3.7，包含 V3.6–V3.7 累积更新：多镜头或既有镜头权威仍使用全片时间的 `Shot N [start-end s]` 标题；Shot 内动作改为从 `0.0s` 起算的直接局部时间码行，统一格式为 `0.2-0.6s: 动作描述`。
- Shot 内不再输出 `Action:`、`beat N`、圆括号、方括号或项目符号包装；无阶段变化的镜头使用一条覆盖完整镜长的局部时间码，有阶段变化时使用最少量的连续时间码行。
- Action V3.5 的弹性字段选择、Sora 字段原义、全局与 Shot 双向一致性、完整自适应 Audio、单一 `Constraints`、首帧场景状态和 Reference / Route 禁止项全部保留。
- Helper Route B 已验证可在 Shot 执行载体中消费直接局部时间码；Helper V3.8、Screenplay Writer V1.4、Storyboard Designer V1.15、Static Asset Designer V2.5 与 Visual Style Extractor V1.5 保持不变，冻结提示词表面逐字节不变。

## 2026-07-21

- `wally-static-asset-designer` 升级为 V2.5，包含 V2.4–V2.5 累积更新：正式资产提示词保留字段名与相对顺序但移除可见数字 / 字母序号；用户提供参考图时，以图像作为可见身份、结构、材质、颜色、标记和状态的主要规格，只补目标变化、布局、关键身份锚点与真实漂移风险。
- Static Asset 的几何契约、呈现契约与用户指定状态 / 布局继续完整输出；Preview、视觉方向、九宫格固定提示词逐字节不变。
- `wally-action-designer` 升级为 V3.5，包含 V3.1–V3.5 累积更新：Shot 内局部 Action 时间从 `0.0s` 起算；吸收 Sora 的平台无关提示知识并保持借用字段原义；全局字段与每个 Shot 双向校验；正向不变量与独立失败风险合并为唯一 `Constraints` 字段，不再输出单独 `Avoid`。
- 清洁、修复、整理、损伤消除、前后对比与产品功效 Shot 必须在动作前写明可生成的场景初态，包括污物 / 损伤 / 乱序的类型、数量或密度、分布与位置；展示和收纳 Shot 写明干净、空置或整齐基线。
- Action 的默认声音分支仍为无BGM加完整环境声 / SFX；用户或锁定材料明确提供音乐时准确保留音乐，明确要求绝对静音时不添加任何声音。
- Helper V3.8、Screenplay Writer V1.4、Storyboard Designer V1.15 与 Visual Style Extractor V1.5 保持不变；Helper Route B 已验证兼容新 Action 正文内部的单一 `Constraints` 与 Subject / Action / Timing / Shot 四类资产执行载体。

## 2026-07-20

- `wally-helper` 升级为 V3.8，包含 V3.7–V3.8 累积更新：保留各专业产物的模板结构；兼容旧 V2 固定导演正文与新 V3 弹性正文；用语义充分性检查代替固定字段组合检查；Route B 可在 `Subject`、`Action`、`Timing/beats` 或 Shot 中绑定资产，无 Avoid 时省略空限制。
- `wally-static-asset-designer` 升级为 V2.3：六类生产资产提示词保留编号、字段名、层级和字段顺序；Preview、视觉方向、九宫格固定提示词和资产几何定义保持不变。
- `wally-action-designer` 升级为 V3.0：字段只在承担独立控制信息时出现；单一连续动作、精确单镜和多镜头分别使用 `Action`、`Action + Timing/beats` 或 Shot；删除剧情总述与 Shot 的重复层；继续提供完整无BGM声音设计。
- `wally-visual-style-extractor` 升级为 V1.5，包含 V1.4–V1.5 累积更新：交付物使用匹配的结构化模板；按请求选择 Style Lookup、Analysis Card、Three-Stage Brief、Reusable JSON Prompt 或 Transfer Validation；模板内部省略空字段和无证据字段。
- Screenplay Writer V1.4 与 Storyboard Designer V1.15 保持不变。Helper Route A、Static Asset 固定提示词、Storyboard canonical style、固定故事板提示词和固定分镜表提示词通过冻结面校验。
- 六项 skill 通过结构校验、fresh-process 前向测试、Route A/B 兼容检查、live/repository 树一致性和公开发布安全检查。

## 2026-07-19

- `wally-helper` 升级为 V3.6：明确承担 Wally 系列的用法与跨模块制作经验层；新增“剧本初稿 → 故事板草稿测试 → 静态资产 → 资产支持的分镜表复核 → 动作设计 → 最终组装”推荐路线，同时保留用户独立调用任一专业功能的选择。
- 场景多角度参考默认先使用九宫格；九格无法保持场景身份、拓扑、家具、设备或风格一致时，推荐降低信息密度并改用 `2×2` 四宫格。
- `wally-storyboard-designer` 升级为 V1.15：按用户授权，只修改故事板和分镜表固定短任务的分图措辞，分别明确故事板之间、分镜表之间不要拼成一张图；canonical 故事板样式和其余模板内容不变。
- `wally-action-designer` 升级为 V2.9，包含 V2.7–V2.9 累积更新：删除会诱发多余动作编排的 connected-motion-consequences / follow-through 规则；采用单一主动作、单一主导摄影行为和按需顺序节拍的动作经济；画面中需要逐字生成的文字统一使用中文双引号“……”，对白继续使用「……」。
- Screenplay Writer V1.4、Static Asset Designer V2.2、Visual Style Extractor V1.3 保持不变；六项 skill 通过结构校验、边界扫描和公开发布安全检查。

## 2026-07-16

- `wally-helper` 升级为 V3.5：身份提示词改用第一人称，Wally 以“我是 Wally”介绍自己，不再把内部第二人称指令原样展示给用户。
- `wally-helper` 升级为 V3.4：身份层收口为一段用户确认的精简提示词，列出五个专业 skill 及其核心功能。
- 明确 Wally 不能调用或代替专业 skill；需要专业工作时，只推荐对应 skill 并提供由用户复制执行的调用请求。
- `wally-helper` 升级为 V3.3 助手身份：用户说“wally”后，默认按零基础用户接待，从目标或现有材料开始，一次推进一个步骤。
- 新增固定新手引导循环与可复制的专业交接格式；交接会说明当前状态、下一步、所需材料、预期产物和完成标准。
- 修正 Helper 内残留的旧技术名，统一使用 `wally-screenplay-writer` 与 `wally-action-designer`；Route A/B 组装结构未改。
- 将两个退役独立仓库更名为 `deco-helper-deprecated` 与 `deco-helper-storyboard-deprecated`，并转为 Private；当前主仓库保持公开。
- 修正触发边界：只有 `wally-helper` 要求用户明确呼叫 Wally；编剧、故事板、静态资产、动作设计和视觉风格五个专业 skill 按各自专业意图正常触发。
- 专业 skill 版本更新为 Screenplay Writer V1.4、Storyboard Designer V1.14、Static Asset Designer V2.2、Action Designer V2.6、Visual Style Extractor V1.3。
- 建立 `overwa1ch/wally-skills`，作为 Wally 系列唯一的主发布仓库。
- 首次统一发布六个当前模块：`wally-helper`、`wally-screenplay-writer`、`wally-storyboard-designer`、`wally-static-asset-designer`、`wally-action-designer`、`wally-visual-style-extractor`。
- 正式采用 `wally-screenplay-writer` 和 `wally-action-designer` 两个新技术名。
- 宣布原独立仓库 `overwa1ch/deco-helper` 与 `overwa1ch/deco-helper-storyboard` 退役。
- 六个 skill 均通过 Codex skill 结构校验和公开发布安全扫描。

## 未标日期的早期版本

- Storyboard V1.18 将专业功能设为按用户请求独立交付。
- Static Asset V2.0 建立过程、知识、共用合同与自包含类型文件的分层；V2.1 将专业功能设为按需菜单，仅在用户明确要求时运行完整流程。两项原入口记录未标日期。
