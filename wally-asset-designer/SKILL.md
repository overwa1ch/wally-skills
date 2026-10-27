---
name: wally-asset-designer
description: Use only when the user explicitly requests wally-asset-designer or $wally-asset-designer by name. Prepare reusable image assets, character video references or whitebox video references from current materials. For character video references, preserve the selected Cxx page and use existing screenplay dialogue and context for a brief performance. Generate requested images through ChatGPT Web for human review. Original screenplay, dialogue rewriting, scene shot design and final scene-video prompts remain with their specialists.
---

# Wally Asset Designer

规划可复用的图片资产、动态角色参考与白模视频参考，按用户请求交付定义、提示词或资产。

Version: `wally-asset-designer@2026-10-27-v3.4-targeted-image-revision`

## 共用边界

- 接受剧本、文字、表格、图像、故事板、参考板、已有资产、部分材料和混合输入。只处理会影响当前产物的缺失与矛盾，不要求用户从固定起点重做。
- 保留剧本事实、整体调性与用户已确认的视觉约束。故事板只作为状态、构图、空间与道具的证据，不修改镜头序列。
- Agent 根据文字材料、用户说明和已选关系准备输入，直接绑定所需参考图，不查看或评判图像内容。图片用途不清楚且影响输入时，只补问必要的用途说明。具体生产依赖由所选类型文件维护。
- 图片和参考视频的内容、整体观感、风格差异和资产可用性统一由人审查。Agent 只核对提交回执、任务状态、文件关联及尺寸等元数据；类型清单用于起草提示词和供人审查，不作为 Agent 审图任务。
- 只交付用户点名的定义、提示词或资产，直接使用已有材料；不要求先完成资产规划、风格选择或其他项目阶段。
- 沿用用户已有的剧本、分镜、表演与时序。动态角色参考可选取剧本原句，并依据其情境编写角色参考页的短表演提示词；原创剧情、对白改写、剧情镜头的具体表演与声音设计，以及最终场景视频提示词继续由对应专业工具负责。
- 不再规划或生成场景角色状态资产页。角色的霜冻、污渍、伤口等外观状态留给后期制作。

## 图片版本与交付

- 按本次要求的范围和数量交付；未指定数量时，只准备完成当前任务所需的版本，不自动扩成候选包。已有定稿输入直接执行，定向修改只处理指定版本。
- 用户要求多个设计方案时，每套使用独立完整输入，并说明实际设计差异；重复输入、只改编号或随机重画不计作不同设计。用户明确要求同一输入多次生成时，记录为重复采样。
- 全部生成结果交给人审查，说明输入意图及执行状态，不自行筛选、评分、视觉修正或追加生成。只整理反馈、解释或归档时不触发生图。
- 用户指定采用的版本与原图如实记录。仅在当前衍生产物实际依赖某张基础图时核对该引用；已指定的外部素材同样可以直接使用，不要求在本 skill 内重新生成或选定。

## 按任务读取

只读当前任务对应入口，按表中触发条件读取其引用；历史版本留在 Changelog，不默认加载。用户只要定义或提示词时交付文本；要图时默认内部准备输入，通过内置 Browser 操作 ChatGPT Web 提交、收集本次结果并交人审图。

**图片定稿执行**：核对范围、数量和实际参考依赖，逐字沿用完整输入，加载浏览器操作与生成记录；依赖不明确时只读对应类型要求。交付时再加载人工审查说明；需起草、补充或修改输入时，按下表读取写作方法或类型细则。

| 当前任务 | 读取入口与交付范围 |
| --- | --- |
| 已有图片的定向材质修整或重新布光 | [targeted-image-revision.md](references/targeted-image-revision.md)；按本次目标明确变化范围与保留内容，直接使用指定原图。 |
| 动态角色参考定义、提示词或修订 | [dynamic-character-video.md](types/dynamic-character-video.md)；承接已选 Cxx 与剧本，按需制作整页短动态参考。 |
| 白模视频定义、规划、制作或修订 | [whitebox-video.md](types/whitebox-video.md)。 |
| 图片生成、收集或恢复 | [browser-execution.md](references/browser-execution.md) 与 [候选生成记录](templates/generation-record.md)；执行完整的项目与聊天命名、独立聊天、异步提交核验、原图归档及恢复流程。 |
| 资产规划与类型选择 | [planning.md](references/planning.md)；图片视觉规划按需读取 [regional-anchor.md](references/regional-anchor.md)、[style-aesthetic.md](references/style-aesthetic.md) 与 [方案模板](templates/visual-direction-proposal.md)。 |
| 起草或修改单幅效果图 | [craft.md](references/craft.md) 与 [style-aesthetic.md](references/style-aesthetic.md)。 |
| 起草或修改单项正式图片资产 | [contracts.md](references/contracts.md) 与所选 `types/<asset>.md`；类型对应关系见 planning，字段、几何和呈现按类型合同保留。 |
| 起草或修改九宫格 / 四宫格 | 默认使用 [multi-angle.md](types/multi-angle.md)；用户直接要求或选择 fallback 时使用 [multi-angle-2x2.md](types/multi-angle-2x2.md)。基础地点须已选定；审查九宫格时不擅自追加或执行四宫格。 |
| 图片人工审查交付、反馈整理与修订 | [review-protocol.md](references/review-protocol.md)；供人查阅类型要点或按反馈修改输入时再读相关类型清单，Agent 不自行看图判断。 |

交付止于本次请求的产物，不自动安排后续制作阶段。
