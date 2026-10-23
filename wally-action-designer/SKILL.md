---
name: wally-action-designer
description: Use only when explicitly requested by name. 按场景设计或修订 AI 视频的表演、互动、摄影、灯光、声音及参考绑定，也可按要求审查回片。
---

# Wally Action Designer

根据当前材料完成用户指定范围的表演设计。一个场景是一场完整的戏；镜头数量服务于该场设计。

交付使用 `REFERENCE:`、`STYLE PREFIX:`、`STYLE:`、`COMPOSITION:`、`THE SHOT:`、`SPOKEN LINE:`、`CHARACTER ACTING:` 等英文标签，字段按需选用。THE SHOT 内保留 `SHOT` 编号，需要精确节拍时用 timestamp 分段，主要控制动作先后、反应和状态变化时用连续段落，按镜头需要或用户指定选择。总体字段写宏观控制，THE SHOT 写具体执行，二者保持一致并避免重复总体描述，见[总体控制与时间段](references/contract.md#总体控制与时间段)。动作与表演一起描述；有时间段或多镜头时写入对应时间段或 `SHOT`。

Version: `wally-action-designer@2026-10-23-v3.52-whitebox-reference-framework`

## 按任务读取

| 当前任务 | 读取入口 |
| --- | --- |
| 新写表演设计 | [交付约定](references/contract.md)；涉及的表演与视听选择见 [设计方法](references/craft.md)。 |
| 修改或检查已有设计 | 先读 [交付约定](references/contract.md)，保留原稿；只有需要重新设计表演与视听时才读设计方法。 |
| 审查生成视频 | 读 [回片审查](references/review.md)；需要改稿时再读交付约定。 |

## 内容边界

- 保留故事、已确认台词及用户明确的执行决定，设计它们如何发生。
- 原创或改写台词属于 `wally-screenplay-writer`；静态资产制作属于 `wally-static-asset-designer`。仅在当前工作确实依赖缺失内容时指出缺口，不自动扩展任务。
- 表演设计可直接作为分镜表生成的导演脚本依据。
