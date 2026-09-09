# Director Script Output Contract

Principle: 一切为了讲故事，内容是优先级最高的评判标准。Every shot in a 分镜脚本 exists to tell the source scene's story; when judging any shot or any generated board, content is the first criterion and every other criterion ranks below it. Choose shots by this alone: a shot exists only for a story job the audience needs at that moment.

Core principle: 如果你不确定，就写得更少，而不是更多。

思路：先找关键画面——单纯的画面，对故事最重要的画面，不是符合传统分镜的画面。每个关键画面当成一个镜头写，这就是主镜。找到之后，再去想怎么衔接，第二遍直接用下面的格式把分镜设计完。
Approach: first find the key pictures — pure pictures, the ones that matter most to the story, not pictures shaped by storyboard convention. Write each key picture as a shot; these are the main shots (主镜). Then work out how they connect and, in the second pass, complete the shot design in the same format.

The 分镜脚本 (processed director script) is read by the user and by the image model that draws the test boards; write for those two readers.

## Inherit the work definition

- Copy the source screenplay's `## 作品定义` block verbatim into every complete 分镜脚本.
- When the user states the definition directly but the source lacks a block, transcribe only those explicit decisions into the same field structure; do not infer unsupported classification.
- Treat work type as upstream story authority. This skill may use `剧情短片`, `广告片`, `纪录片`, `MV或视觉片`, or `剧集内容` to control coverage and shot language, but it may not originate or doctor that choice.
- For a complete 分镜脚本, surface a missing definition when the difference between advertisement, narrative film, documentary, MV/visual piece, or episodic content would materially change the result. Request the definition from the user or `wally-screenplay-writer`; do not silently guess.
- Keep definition metadata outside source scene passages and shot blocks. Do not turn labels such as commercial function, genre, or audiovisual position into visible objects, dialogue, or per-shot prompt detail.

## Shot format

Group shots under the original source scene headings, in source order. Each shot:

```text
分镜XX｜镜头类型：…
拍摄手法：景别 + 机位 + [按需焦段/光学] + [按需运镜]
画面内容：[按需前景] + 主体的可见动作或状态 + [按需必要背景]
任务：一句——该镜头向观众传达什么信息？
```

- `镜头类型`: write `主镜` for every key-picture shot from the first pass; connecting shots leave it empty or name a type only when known (道具空镜、状态空镜、插入). Add `｜时长：约Ns` only when the user gives a duration budget.
- `景别`: shot size (全景 / 中景 / 近景 / 特写) plus its positive visible boundary.
- `机位`: where the camera is — position, side or angle, height, distance; an off-frame height reference becomes a height.
- `焦段 / 光学效果`: only when it materially controls the image.
- `运镜`: only when needed. If no movement is written, the camera is fixed.

## 画面内容合同

`画面内容`只回答一个问题：在这个镜头需要被读懂的关键时刻，取景框内具体能看见什么。它不是场景摘要，也不解释镜头为什么成立。

- 默认只写一个主要主体和一个核心可见动作或状态。第二个主体只在两者的可见互动、对照、遮挡或因果本身就是镜头任务时加入。
- 前景、背景和道具都不是必填项。只在它们控制构图、参与动作，或承载观众此刻必须获得的信息时写入。
- 每个名词和身体部位都必须能画进 `拍摄手法` 声明的景别与正向取景边界。不要把框外人物、全身细节、远处物体或未出现的动作带进近景、特写或插入镜头。
- 只写可被画出的具体对象、位置、动作和状态。把心理、象征、关系解释、剧情意义和镜头理由留在 `任务`；不要为了表现这些抽象意思而发明源材料没有提供的表情、手势或动作。
- 摄影角度、景别、机位、焦段、光学效果和摄影机运动只写在 `拍摄手法`，不要在 `画面内容` 重复。
- 当前景、主体或背景在镜头内发生必要的可见变化时，用最少的起幅、变化和落幅描述写清结果；不要在这里重复摄影机路径。
- 写正向目标画面，不列“不出现什么”的负面清单。安全限制或排除项留在镜头块之外。
- 最后做删词测试：删掉任一名词或细节，如果不改变镜头任务、可见动作或构图控制，就删除它。

推荐句式：

```text
画面内容：[必要前景]；主体位于哪里，正在做什么或处于什么状态；[必要的第二主体或背景变化]。
```

例：

```text
画面内容：哥哥的肩膀虚化在左前景；肖志祥位于画面中央，低头拍了一下棉袄内袋。
```

## Targeted Revision

- When the user reports what they saw in the boards or names shots to change, revise only the named shots and keep the rest verbatim.
- Write the change into the shot text; keep reasons in chat or a separate record. The document shows the current target state only.
