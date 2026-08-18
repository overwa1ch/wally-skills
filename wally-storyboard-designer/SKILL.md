---
name: wally-storyboard-designer
description: Convert user-supplied scene-divided scripts, scene excerpts, briefs, tables, images, reference boards, partial or conflicting materials, director scripts, shot sequences, storyboards, or mixtures into optional scene-layout SVGs, visually optimized scenes, processed director scripts, storyboard designs, adversarial multi-agent 主镜 judgments, the fixed storyboard prompt, and the fixed shot-table prompt while inheriting the source work definition. Use for 导演脚本, 镜头脚本, 场景布局, 主镜判断, 分镜设计, 故事板, 分镜表, Bxx, 景别, 构图, 运镜, 镜头连续性, returned-board review, or existing copy-ready storyboard prompts. Trigger from professional storyboard or shot-design intent; explicit wally mention is not required. Keep original screenwriting, static asset design, performance/dialogue/audio design, and final video prompt assembly outside this skill.
---

# Wally Storyboard Designer

Provide on-demand storyboard-domain functions for the user's supplied story, scene, image, board, or shot material.

Current version: `wally-storyboard-designer@2026-08-18-v2.1-adversarial-main-shot`

## Changelog

- `2026-08-18-v2.1-adversarial-main-shot`: Require blind multi-agent proposal, adversarial deletion and merge tests, and evidence-based adjudication before locking any source scene's main-shot set.
- `2026-08-18-v2.0-source-scene-authority`: Treat the source screenplay's existing scene boundaries, exact headings, and order as the sole scene authority for every generation product.
- `2026-07-28-v1.19-work-definition-inheritance`: Inherit and display the upstream work definition without originating it.
- `v1.18-functional-only-scope`: Keep storyboard-domain functions on demand.

## Accept the user's current material

- Accept scene-divided scripts, individual scene excerpts, briefs, test plots, tables, images, reference boards, asset references, partial artifacts, conflicting drafts, director scripts, shot sequences, storyboards, or any mixture.
- Do not require completeness, a locked or approved source, a particular schema, an asset package, a route choice, or a fixed starting stage. Surface only conflicts that would materially change the named product.
- Preserve supplied story facts. Do not expand, rewrite, doctor, or originate the screenplay; send original screenwriting work to `wally-screenplay-writer`.
- For a generation product that needs scene boundaries, require an upstream screenplay or excerpt with explicit source scenes. When those boundaries are absent, stop and route scene formation to `wally-screenplay-writer`; never split, merge, or number the material in this skill.
- Treat the source scene boundaries, exact headings, and order as the sole authority. Never split, merge, rename, normalize, or renumber them.
- A source scene may contain multiple action chains, multiple dramatic beats, multiple storyboard pages, and any number of necessary shots.
- Preserve the latest explicit or approved `作品定义` as source authority. Keep work form, commercial function, narrative mode, delivery format, and audiovisual position distinct.
- **Functions are on-demand.** Deliver exactly the product the user names — nothing before it, nothing after it. Do not pull in earlier stages, volunteer later stages, or ask sequence questions. If the named product lacks a required input, name the missing input and stop; do not produce the upstream product uninvited.

## Inherit the work definition

- Copy the source screenplay's `## 作品定义` block verbatim into every complete processed director script, shot-sequence design, storyboard design, or storyboard review.
- When the user states the definition directly but the source lacks a block, transcribe only those explicit decisions into the same field structure; do not infer unsupported classification.
- Treat work type as upstream story authority. This skill may use `剧情短片`, `广告片`, `纪录片`, `MV或视觉片`, or `剧集内容` to control coverage and shot language, but it may not originate or doctor that choice.
- For a complete director script or storyboard design, surface a missing definition when the difference between advertisement, narrative film, documentary, MV/visual piece, or episodic content would materially change the result. Request the definition from the user or `wally-screenplay-writer`; do not silently guess.
- Keep definition metadata outside source scene passages and shot blocks. Do not turn labels such as commercial function, genre, or audiovisual position into visible objects, dialogue, or per-shot prompt detail.
- Keep the fixed storyboard and shot-table prompt templates verbatim. Their exact-payload contract is unchanged.

## Route the work

### Scene-layout SVG

When the user requests spatial planning, read [references/scene-layout-svg-rules.md](references/scene-layout-svg-rules.md). Create the requested SVGs immediately. Do not ask whether the user wants SVGs when the request already names them.

### Visual optimization

When the user wants a more shootable or storyboard-ready version, read [references/visual-optimization-rules.md](references/visual-optimization-rules.md). Preserve story content while making visible action, blocking, transitions, sound sources, and continuity anchors executable.

### Processed director script

Read [references/director-script-output-contract.md](references/director-script-output-contract.md). Prepend the inherited work definition, then apply its frame-visibility and prompt-hygiene rules to every shot block: write only what the exact crop can show, and keep off-frame continuity in validation. Write every `拍摄手法` in this order: `拍摄角度 + 景别（取景框） + 机位 + 运镜`; add focal length or optical effect only when it materially controls the image. Keep angle, crop, camera position, and camera movement distinct. Define camera movement for every shot with its start, path, subject relation, and landing. Default to a slow push-in when no stronger movement is motivated. Use `固定镜头` only when the user locks it or stillness itself is the narrative point. Use [references/ai-video-composition-rules.md](references/ai-video-composition-rules.md) only when the user explicitly requests composition-heavy output. Validate with [references/continuity-validation-rules.md](references/continuity-validation-rules.md) before delivery.

### Storyboard design or review

- For every storyboard design, redesign, `Bxx`, or returned-board review, first read [references/storyboard-style-contract.md](references/storyboard-style-contract.md) so the canonical surface is available without changing it.
- For direct storyboard design, redesign, shot-sequence revision, or main-shot judgment, read [references/main-shot-adjudication.md](references/main-shot-adjudication.md), then [references/storyboard-design.md](references/storyboard-design.md).
- Lock each source scene's main-shot set through the required multi-agent adversarial protocol before designing coverage around it. Never substitute one agent's judgment, majority vote, average score, or consensus language for the evidence-based adjudication.
- If independent agents are unavailable, label the result `主镜未裁决` and stop before claiming a final main-shot set; do not silently perform a single-agent substitute.
- For a returned board or existing shot sequence, read [references/storyboard-review.md](references/storyboard-review.md).
- Prepend the inherited `## 作品定义` block to the delivered design or review; use it to judge whether coverage and shot language fit the source work.
- Cite concrete panels, shots, pages, or visible features when reviewing. Preserve usable choices and propose the smallest correction.
- Classify each finding as board-execution failure or shot-design failure: a faithful board that exposes a design flaw is a successful test, and its revision routes to the shot design, not to a redraw.
- Review from text: the user views the boards and reports observations; do not open board images unless explicitly asked. Offer a per-panel viewing checklist derived from the design to make the user's pass fast.

### Fixed storyboard and shot-table prompts

- For the storyboard prompt, read [templates/storyboard-prompt-template.md](templates/storyboard-prompt-template.md) and output only its stored, labeled `【故事板生成模版】` payload and separate labeled `【短任务提示词】` payload. There is no rough/formal grade; one fixed storyboard prompt serves every storyboard request, and `Bxx` remains only the identifier for returned boards.
- For the shot-table (分镜表) prompt, read [templates/shot-table-prompt-template.md](templates/shot-table-prompt-template.md) and output only its stored, labeled `【分镜表生成模版】` payload and separate labeled `【短任务提示词】` payload.
- For either short-task payload, replace only the literal `【源场景标题】` with the exact original source scene heading when the request or supplied material provides one. Do not infer, normalize, rename, or renumber a heading. Leave `【源场景标题】` unchanged for a generic reusable prompt with no exact source heading.
- Storyboards and shot tables have different strengths: a storyboard gives annotated per-shot direction sketches (景别/运镜/动作); a shot table renders the model's native 分镜表 concept — the complete source-scene shot sequence, numbered panels, no text, no style constraints. One source scene may use multiple pages and as many shots as needed. The choice between the two products belongs to the user.
- The exact runtime `【源场景标题】` replacement above is the only allowed payload substitution. Do not modify the stored templates or otherwise fill, summarize, explain, relabel, wrap, or append anything to either fixed prompt.
- If the requested prompt type is unclear and cannot be inferred, ask only whether the user wants the storyboard prompt or the shot-table 分镜表 prompt.

## Boundaries

- Do not originate, rewrite, validate, or doctor a screenplay as a screenplay.
- Do not split, merge, rename, normalize, or renumber source scenes.
- Do not design character, group, scale, prop, scene, or other static assets.
- Do not design performance, dialogue, vocal delivery, timing performance, or audio design.
- Do not choose Route A/B or assemble a final image-to-video or text-to-video prompt.
- Keep the canonical storyboard style block and both fixed prompt templates unchanged unless the user explicitly requests an exact template edit. For an authorized edit, change only the named text surface and preserve the rest verbatim.
