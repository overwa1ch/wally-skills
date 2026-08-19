# Director Script Output Contract

Principle: 一切为了讲故事，内容是优先级最高的评判标准。Every shot in a 分镜脚本 exists to tell the source scene's story; when judging any shot or any generated board, content is the first criterion and every other criterion ranks below it. Choose shots by this alone: a shot exists only for a story job the audience needs at that moment.

Core principle: 如果你不确定，就写得更少，而不是更多。

思路：先找关键画面——单纯的画面，对故事最重要的画面，不是符合传统分镜的画面。每个关键画面当成一个镜头写，这就是主镜。找到之后，再去想怎么衔接，第二遍直接用下面的格式把分镜设计完。
Approach: first find the key pictures — pure pictures, the ones that matter most to the story, not pictures shaped by storyboard convention. Write each key picture as a shot; these are the main shots (主镜). Then work out how they connect and, in the second pass, complete the shot design in the same format.

The 分镜脚本 (processed director script) is read by the user and by the image model that draws the test boards; write for those two readers.

## Shot format

Prepend the inherited `## 作品定义` block verbatim and keep it outside scene text and shot blocks. Group shots under the original source scene headings, in source order. Each shot:

```text
分镜XX｜镜头类型：…
拍摄手法：景别 + 机位 + [按需焦段/光学] + 运镜
画面内容：写清楚前景+主体+[背景]，仅限取景框内可见的内容，严禁过度详细。（写太多会让模型尝试把每个词都塞进画面，形成“提示词污染”，画面怪异混乱。）
任务：一句——该镜头向观众传达什么信息？
```

- `镜头类型`: write `主镜` for every key-picture shot from the first pass; connecting shots leave it empty or name a type only when known (道具空镜、状态空镜、插入). Add `｜时长：约Ns` only when the user gives a duration budget.
- `景别`: shot size (全景 / 中景 / 近景 / 特写) plus its positive visible boundary.
- `机位`: where the camera is — position, side or angle, height, distance; an off-frame height reference becomes a height.
- `焦段 / 光学效果`: only when it materially controls the image.
- `运镜`: start, physical path, relation to the subject, and landing. When no stronger move is motivated, default to a slow push-in to a slightly tighter framing. Use `固定镜头` only when the user locks it or stillness itself is the narrative point, and say so in `任务`. Use exact verbs (`推近`、`后退`、`横移`、`升`、`降`、`摇`、`俯仰`、`环绕`、`跟拍`、`手持`); never write `镜头跟随`、`动态运镜`、`镜头运动`、`推进感` or `轻微晃动` as a complete instruction.

## Targeted Revision

- When the user reports what they saw in the boards or names shots to change, revise only the named shots and keep the rest verbatim.
- Write the change into the shot text; keep reasons in chat or a separate record. The document shows the current target state only.
