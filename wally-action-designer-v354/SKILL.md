---
name: wally-action-designer-v354
description: Use only when the user explicitly requests wally-action-designer-v354 or $wally-action-designer-v354 by name. Use the frozen Wally V3.54 all-in-one action method for AI-video performance and prompt design or review only when the user selects V3.54, 拆分前版本, or 旧版表演设计, including comparisons with the current camera and performance skills. Keep each version separate.
---

# Wally Action Designer V3.54 拆分前对照

本入口调用2026-10-30拆分为摄影与成像、人物表演两个技能之前的完整 V3.54，用于和新版本做对照测试，不预设两者的效果优劣。

Source version: `wally-action-designer@2026-10-27-v3.54-interaction-camera-cases`

先读取[原始技能入口](references/v3.54/SKILL.original.md)，再按其任务路由读取相邻的[交付约定](references/v3.54/references/contract.md)、[设计方法](references/v3.54/references/craft.md)或[回片审查](references/v3.54/references/review.md)；需要时读取[互动表演案例](references/v3.54/references/interaction-examples.md)与[摄影问题排查](references/v3.54/references/camera-troubleshooting.md)。归档入口中的相对路径以该入口所在目录为基准。

- 按归档 V3.54 的19字段、写法和方法执行，不自动套用 `wally-camera-designer` 的10段格式、`wally-performance-designer` 的方法或近身打斗入口。
- 对照测试时各版分别加载、分别交付，并在提示词正文之外标明版本；不混合各版方法，也不因版本更新就判断效果更好。
- `references/v3.54/` 保存七份原文件的完整原字节。原入口只改存储文件名为 `references/v3.54/SKILL.original.md`，以区分独立调用入口；归档中的原调用名称与 UI 元数据仅作源文件保存，不改变本入口调用名。
- 未获用户明确授权，不修改冻结原文。用户未指定版本时使用当前的摄影与成像、人物表演技能，不由本对照入口替换。
