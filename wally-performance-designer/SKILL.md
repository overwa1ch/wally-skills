---
name: wally-performance-designer
description: Use only when the user explicitly requests wally-performance-designer or $wally-performance-designer by name. Design character performance for AI video from supplied screenplay, character and scene materials, including what each character does, wants, says, hears and how they respond, using scene events, scene direction, tactics and beats keyed to dialogue. Use for 人物表演设计, 表演设计, 表演任务, 对白表演, 互动表演, 表演修订, or 回片中的表演问题. Preserve approved story and dialogue; shots, timing and final prompt assembly belong to wally-camera-designer.
---

# Wally Performance Designer

根据当前材料设计人物如何行动、说话、倾听和回应。保留已确认的剧情、台词及执行决定，交付可由摄影与成像组装进最终视频提示词的表演内容。

Version: `wally-performance-designer@2026-10-30-v1.0-higgs-acting-fusion`

## 按任务读取

| 当前任务 | 读取入口 |
| --- | --- |
| 新写人物表演 | [设计方法](references/acting-method.md)与[表演交付](references/performance-fields.md)；粒度见[描述粒度](references/granularity.md)。 |
| 修订已有提示词中的表演 | 先读[表演交付](references/performance-fields.md)，保留原稿；需要重新设计时再读设计方法。 |
| 意图或策略变化难以落成可见互动 | 按需读取[互动表演案例](references/interaction-examples.md)中对应的一例。 |
| 写对白与声音身份 | [SPOKEN LINE 与声音身份](references/spoken-line.md)。 |
| 回片中的表演问题 | [设计方法](references/acting-method.md#回片中的表演问题)。 |

写入提示词前按[提示词写作规则](references/prompt-writing-rules.md)检查。

## 档位与确认

按复杂程度分简单、标准、完整三档，判断方法见设计方法。完整档先交付设计说明，用户确认后再写提示词版本；动机有多种可能且会改变表演色彩时，先请用户选择。

## 内容边界

- 保留故事、已确认台词及用户明确的执行决定，设计它们如何被表演出来。原创或改写台词属于 `wally-screenplay-writer`。
- 镜头划分、时长、时间戳、机位、灯光、成像和最终提示词组装属于 `wally-camera-designer`；人物调度以已有分镜或白模为准。
- 近身格斗的招式与拍子属于 `higgsfield-fight-scene`，人物表演负责打斗中的意图与反应。
- 仅在当前工作确实依赖缺失内容时指出缺口，不自动扩展任务。
