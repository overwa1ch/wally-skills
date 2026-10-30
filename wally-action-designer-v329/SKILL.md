---
name: wally-action-designer-v329
description: Use only when explicitly requested by name. 调用冻结的 Wally V3.29 原版进行表演设计、修订或回片审查，也用于与当前版分别对照。
---

# Wally Action Designer V3.29 原版对照

本入口调用 V3.30 之后研究修改之前保留的完整 V3.29，不预设它与当前研究版或官方版的效果优劣。

Source version: `wally-action-designer@2026-10-10-v3.29-unified-action`

先读取[原始技能入口](references/v3.29/SKILL.original.md)，再按其任务路由读取相邻的 [交付约定](references/v3.29/references/contract.md)、[设计方法](references/v3.29/references/craft.md)或[回片审查](references/v3.29/references/review.md)。归档入口中的相对路径以该入口所在目录为基准。

- 按归档 V3.29 的字段、写法和方法执行，不自动套用 V3.30 之后的修改（包括 V3.54 对照版与当前的摄影与成像、人物表演技能）或 ANERNEQ 规则。
- 对照测试时各版分别加载、分别交付，并在提示词正文之外标明版本；不混合各版方法，也不因版本更新就判断效果更好。
- `references/v3.29/` 保存五份原文件的完整原字节。原入口只改存储文件名为 `references/v3.29/SKILL.original.md`，以区分独立调用入口；归档中的原调用名称与 UI 元数据仅作源文件保存，不改变本入口调用名。
- 未获用户明确授权，不修改冻结原文。归档中的调用策略仅作历史保存；本共享入口只在用户明确点名并要求使用时启用，不自动替换当前版。
- 归档中提到的旧资产 skill 现名为 `wally-asset-designer`；涉及资产制作时使用当前名称，冻结原文保留历史称呼。
