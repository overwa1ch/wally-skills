---
name: higgsfield-fight-scene
description: Use only when explicitly requested by name, or when the user asks for the Higgsfield fight method or 近身打斗 skill. Turns a close-quarters fight into beats of position, action, contact and reaction for wally-camera-designer to place on the timeline. Do not use for gunfights, chases, ordinary pushes or hand-offs.
---

# Higgsfield Fight Scene 项目入口

本入口在当前项目中使用 Higgsfield 原作者的近身打斗技能。原文保存在 `references/source/`，保持原字节；本入口只说明项目适配边界。

Version: `higgsfield-fight-scene@2026-10-30-v2.4-project-entry`

## 使用

先读[原始技能入口](references/source/SKILL.original.md)，按其工作流和知识库路由读取相邻的参考文件；归档入口中的相对路径以该入口所在目录为基准。

## 项目适配边界

- 只在用户明确点名时使用。枪战、追逐、普通推搡和传递由人物表演与摄影处理。
- 原文中的 Victor 是原作者的需求方，在本项目由用户替代；原文提到 Victor 的偏好与优先级时，按当前用户的要求执行。
- 不执行原文的 INGEST 协议，不改写原文或重新打包。用户提供新的格斗资料时，按项目技能更新流程备份并记录，另行决定是否纳入。
- 归档保留了导入流程的示例文件名和已退役的打击物理资料名；本入口不依赖这些示例或退役资料，原文仅作来源保存。
- `FIGHT STYLE LOCK` 及 P1–P6 等套路只在用户选定截拳道或咏春时使用。持枪缠斗、争枪、与感染者扭打等不属于这两种风格的近身戏，只采用原文的方法：按“位置 → 动作 → 对方反应 → 新位置”分拍；罕见动作给出日常类比、先接触的部位和沿受力方向的反应；每次接触写出对方身体的反应；用正面状态锁定动作；一场打斗尽量在两到四拍内解决；景别保证相关肢体在画面内。不套用截拳道站架、招式名称或固定节奏，也不在没有资料依据时自创军事格斗风格。
- 原文提到的 ULTRALORDGEN、CINEDANCE 等格式引擎，在本项目由 `wally-camera-designer` 代替：分拍交给摄影与成像落到 THE SHOT 的时间段，打击声列入 AUDIO，景别要求写入 CAMERA 或对应时间段。原文要求放在提示词末尾的风格锁定，只在选定截拳道或咏春时写进最后一个打斗时间段。
- 打斗拍子内可写到肢体、轨迹、接触部位与反应方向；拍子之外回到完整动作写法。人物在打斗中的意图与情绪反应由 `wally-performance-designer` 设计。
- 写入提示词前按[提示词写作规则](references/prompt-writing-rules.md)检查；原文“不写禁止项”的要求与该规则一致。
- 原文的版本说明、示例与参考来源只作方法依据，不代表当前项目的人物、动作或平台已经验证。

交付分拍时，在提示词正文之外标明使用本入口及实际采用的风格或方法。
