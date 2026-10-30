---
name: wally-camera-designer
description: Use only when the user explicitly requests wally-camera-designer or $wally-camera-designer by name. Design how an AI-video scene is seen and heard, including shots, durations, timestamps, framing, camera movement, eye-lines, light, imaging look, optics and sound space, and assemble the final video prompt from screenplay dialogue, asset references, performance and close-combat outputs. Use for 摄影设计, 成像设计, 视频提示词, 视频导演提示词, 镜头与时间线, 参考素材与对象绑定, 提示词组装, 提示词修改, or 回片审查. Preserve approved story, dialogue, performance and shot decisions while developing their execution.
---

# Wally Camera Designer

决定观众怎样看到和听到这场戏，并把各技能的产出组装成最终视频提示词。一个场景是一场完整的戏；镜头数量服务于该场设计。

Version: `wally-camera-designer@2026-10-30-v1.5-conditional-flare`

最终提示词使用十个英文标签段落，按需选用：`REFERENCE`、`FORMAT`、`STYLE`、`CAMERA`、`ACTING TASKS`、`THE SHOT`、`SPOKEN LINE`、`LIGHT`、`AUDIO`、`NEGATIVE`。全局段写整场不变的控制，只在某一刻发生的事写进 THE SHOT 的时间段。THE SHOT 内保留 `SHOT` 编号，需要精确节拍时用 timestamp 分段，主要控制动作先后、反应和状态变化时用连续段落，按镜头需要或用户指定选择，见[交付约定](references/contract.md)。

## 按任务读取

| 当前任务 | 读取入口 |
| --- | --- |
| 新写或组装视频提示词 | [交付约定](references/contract.md)；设计镜头、光与声音时读[摄影设计](references/camera-craft.md)。 |
| 修改或检查已有提示词 | 先读[交付约定](references/contract.md)，保留原稿；需要重新设计摄影时再读摄影设计。 |
| 已选变形镜头外观，或虚化、光斑、光条、畸变问题 | [光学与变形镜头](references/optics-anamorphic.md)。 |
| 具体摄影问题或回片中的摄影偏差 | [摄影问题排查](references/camera-troubleshooting.md)。 |
| 审查生成视频 | [回片审查](references/review.md)；需要改稿时再读交付约定。 |
| 没有人物表演产出的简单镜头 | [描述粒度](references/granularity.md)；对白按[SPOKEN LINE 与声音身份](references/spoken-line.md)。 |

写入提示词前按[提示词写作规则](references/prompt-writing-rules.md)检查；组装完成后按交付约定中的组装检查复核。

## 内容边界

- 保留故事、已确认台词、表演设计及用户明确的执行决定，设计它们如何被看到和听到。
- 原创或改写台词属于 `wally-screenplay-writer`；人物意图、策略与逐拍表演属于 `wally-performance-designer`；近身格斗招式属于 `higgsfield-fight-scene`；图片资产与白模视频参考制作属于 `wally-asset-designer`。仅在当前工作确实依赖缺失内容时指出缺口，不自动扩展任务。
- 本技能的提示词可直接作为白模视频制作的镜头依据。
