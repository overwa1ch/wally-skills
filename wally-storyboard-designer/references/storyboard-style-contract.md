# Storyboard Style Contract

This file is the canonical home of the immutable storyboard style block. The fixed storyboard prompt in `templates/storyboard-prompt-template.md` carries this exact block; the fixed shot-table prompt carries no style block by design.

## Fixed Visual Style

- The following Chinese style prompt is canonical and immutable. Use it verbatim in every model-facing storyboard template. Do not rewrite, paraphrase, compress, expand, translate, or change any character unless the user explicitly requests a storyboard style prompt edit.

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

## Use

- Read this file only to confirm that the storyboard template's style block is intact, or when the user asks about the storyboard style. It defines no shot-design or board-review rules.
- Each short task prompt targets the current source scene by its exact original heading and asks for multiple separated storyboard versions. For another source scene, output another short task prompt with that scene's exact original heading.
