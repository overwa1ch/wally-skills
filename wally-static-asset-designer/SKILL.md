---
name: wally-static-asset-designer
description: Use only when the user explicitly requests wally-static-asset-designer or $wally-static-asset-designer by name. Plan and generate Preview and reusable static assets through ChatGPT Web in the in-app Browser. Submit each complete input in its own chat, keep dispatching while earlier jobs generate, and collect the whole round for human visual review. Use for asset lists, regional_anchor, style_aesthetic, character, prop, location and multi-angle references, or revisions from human feedback. Keep screenplay, storyboard, performance, dialogue, audio and final video prompts outside this skill.
---

# Wally Static Asset Designer

规划静态资产，先用 Preview 选择全局视觉效果，再生成各项资产的候选版本，由用户逐项选择并归档。

Version: `wally-static-asset-designer@2026-10-10-v2.18-lean-execution`

## 共用边界

- 接受剧本、文字、表格、图像、故事板、参考板、已有资产、部分材料和混合输入。只处理会影响当前产物的缺失与矛盾，不要求用户从固定起点重做。
- 保留剧本事实、整体调性与用户已确认的视觉约束。故事板只作为状态、构图、空间与道具的证据，不修改镜头序列。
- Agent 根据文字材料、用户说明和已选关系准备输入，直接绑定所需参考图，不查看或评判图像内容。图片用途不清楚且影响输入时，只补问必要的用途说明。具体生产依赖由所选类型文件维护。
- 图像内容、整体观感、风格差异和资产可用性统一由人审查。Agent 只核对提交回执、任务状态、文件关联及尺寸等元数据；类型清单用于起草提示词和供人审查，不作为 Agent 审图任务。
- 只交付用户点名的产品。完整流程仅在用户要求建立整套资产系统或完成全流程时运行；已有选定的 Preview 或基础资产直接继承。
- 不创作剧本、分镜、表演、对白、时序或声音，不编写视频提示词。

## 候选版本与选择

本节统一维护每轮候选包的最低数量，适用于提示词准备与对应图像生成：

| 产品 | 不同完整生成输入（正文与所需参考） | 独立图像版本 | 变化范围 |
| --- | --- | --- | --- |
| Preview 完整方向探索 | 至少 8 个风格方向，每个方向为同一组代表画面分别写完整输入 | 每个方向的每个代表画面至少 1 版 | 符合剧本整体调性的不同全局视觉风格方向。 |
| 每项静态资产，包括九宫格、四宫格 | 至少 4 套 | 至少 4 版 | 按类型合同继承已选图片类型与所需参考，在当前资产允许的范围内形成不同候选。 |

- Preview 分别记录风格方向与代表画面；同一风格的多张画面共同验证该方向，不能充作多个风格方向。正式资产的一套完整生成输入对应一个候选版本。各方向或版本须有可见、可解释的设计差异；采用不同风格参考时可以共用正文，但须记录并实际接入各自参考。重复输入、只改编号或依赖随机结果不构成不同方案。
- 每轮全部候选交给人审查；首轮完成后停在人工审查，不自行筛选、评分、视觉修正或开始下一轮。Agent 说明各输入的设计意图和执行状态，记录人的反馈后再落实获授权的修订。
- 用户选定后记录版本与原图，依赖它的生产才能继续。批量执行授权只覆盖生成候选，不替代选图；用户明确指定采用已有版本时直接记录，不重复询问。
- 只整理人工审查意见、解释或归档时不自动补生成候选包。用户针对一个候选要求修正时，只修该候选；新一轮方向探索才重新形成候选包。
- 用户限定单一风格、某个模型或某项表现验证时，按限定范围执行并记录为专项测试；完成该测试不等于完成全局风格选型。

## 按任务读取

只读当前任务对应入口，按表中触发条件读取其引用；历史版本留在 Changelog，不默认加载。用户只要提示词时交付文本；要图时默认内部准备输入，通过内置 Browser 操作 ChatGPT Web 提交、收集完整候选包并交人审图。

**定稿执行**：核对范围、候选数和已选参考依赖，逐字沿用完整输入，加载浏览器流程与生成记录；定稿或记录不足以确认所需已选参考依赖时，只按需读取对应类型的依赖要求。交付时再加载人工审查流程；需起草、补充或修改输入时，转入对应起草入口读取 Preview、写作合同或类型细则。

| 当前任务 | 读取入口与交付范围 |
| --- | --- |
| 生成、收集或恢复 | [browser-execution.md](references/browser-execution.md) 与 [候选生成记录](templates/generation-record.md)；执行完整的项目与聊天命名、独立聊天、异步提交核验、原图归档及恢复流程。 |
| 资产规划与视觉边界 | [planning.md](references/planning.md)、[regional-anchor.md](references/regional-anchor.md)、[style-aesthetic.md](references/style-aesthetic.md)，使用 [方案模板](templates/visual-direction-proposal.md)；确认资产范围、剧本调性和不可变事实，风格方向留待 Preview 看图选择。 |
| 起草或修改 Preview / 自然效果图 | [preview.md](references/preview.md)、[craft.md](references/craft.md) 与 [Preview 模板](templates/preview-prompt.md)；按它们引用的风格规则写作，无风格参考图的单帧写法见[纪实摄影示例](examples/preview-documentary.md)。 |
| 起草或修改单项正式资产 | [contracts.md](references/contracts.md) 与所选 `types/<asset>.md`；类型对应关系见 planning，字段、几何和呈现按类型合同保留。 |
| 起草或修改九宫格 / 四宫格 | 默认使用 [multi-angle.md](types/multi-angle.md)；用户直接要求或选择 fallback 时使用 [multi-angle-2x2.md](types/multi-angle-2x2.md)。基础地点须已选定；审查九宫格时不擅自追加或执行四宫格。 |
| 人工审查交付、反馈整理与修订 | [review-protocol.md](references/review-protocol.md)；供人查阅类型要点或按反馈修改输入时再读相关类型清单，Agent 不自行看图判断。 |

完整流程：资产范围与剧本调性 → Preview 候选 → 用户选择全局效果 → 各资产候选 → 用户逐项选择 → 按需制作依赖资产或多角度参考。一次产物是一项资产的一组可比较候选，不附重复设计报告。
