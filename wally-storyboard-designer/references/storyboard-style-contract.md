# Storyboard Style Contract

Use this file for every storyboard module call: script direction, `Bxx` boards, returned-board review, and redrawing source selection.

## Fixed Visual Style

- Each short task prompt targets the current `SEG` and asks for multiple separated storyboard versions.
- If the user asks for another `SEG`, output another current-task prompt.
- The following Chinese style prompt is canonical and immutable. Use it verbatim in every model-facing storyboard template; the fixed storyboard prompt must use this exact same style block. Do not rewrite, paraphrase, compress, expand, translate, or change any character unless the user explicitly requests a storyboard style prompt edit.

```text
使用极其简单的 2D 预览草图风格：
- 原则：如果你不确定，就画得更少，而不是更多。
- 只有人物/人偶的造型
- 没有面部细节，没有服装细节，没有解剖细节
- 没有纹理，没有阴影，没有抛光的渲染
- 黑色松散的草图线条
- 用红色方框表示相机取景框
- 箭头表示运动/力/呼吸/方向
- 粗略的导演缩略图，不是概念艺术

画面使用清晰分镜图风格，保持粗略预览完成度。
红色箭头表示"关键"人物动作、运镜(取景框移动)，箭头标记上写简短的中文说明。
把关键过程尽可能详细地画出来。
每一格下方添加简短中文说明，固定写：景别：...｜运镜：...｜人物动作：...。
将宽高比设为 16:9。
```
- Use clear storyboard drawing, not a polished poster.
- Add fixed short Chinese notes under each panel in this form: `景别：...｜运镜：...｜人物动作：...`.
- Use red camera viewfinder boxes.
- Use arrows to show motion, force, breath, or direction.
- Use red arrows to mark key character actions and camera movement (camera viewfinder movement). Arrow marks carry short Chinese labels.
- Set aspect ratio to 16:9.
- Draw the key process in as much detail as possible.

## Style Limits

- Keep labels, arrows, and notes secondary to the panel image.
- Keep storyboard pages separate from character design sheets and final-look style frames.
- Treat polished posters, concept art, manga cleanup, film stills, UI legends, raw JSON, schema field names, dense diagrams, and long text columns as style drift.

## Context Behavior

- Script-only direction boards judge画面内容、节奏和表达方向. They may use role labels and rough placeholders without stable identity.
- `Bxx` boards with approved assets use them for identity provenance, but still draw people as labeled mannequins.
- Returned-board review judges whether the board communicates the SEG clearly in this fixed style, and whether the communicated shots prove the design; a faithful board that exposes a design flaw is a successful test, not a failed board.
- Route A final-look redraw leaves this style behind; it preserves one approved panel's composition and removes storyboard artifacts.

## Continuous Action

Use same-panel continuous action only when one important motion benefits from it:

- one character or body part may appear in two solid-line positions;
- connect positions with one arrow;
- use sparingly so it reads as one moving subject, not two people.
