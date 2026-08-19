---
name: wally-storyboard-designer
description: "Design the 分镜脚本 (processed director script) and issue the fixed storyboard and shot-table test prompts for user-supplied scene-divided scripts, scene excerpts, briefs, tables, images, partial or conflicting materials, existing director scripts, or mixtures, inheriting the source work definition and the source scene structure. Use for 分镜脚本, 导演脚本, 镜头脚本, 场景布局, 拍摄手法, 景别, 机位, 运镜, 分镜脚本修订, the fixed 故事板 prompt, or the fixed 分镜表 prompt. This skill is the test layer: it designs shots in text and hands the user a cheap visual test; the user judges the generated boards. Trigger from professional shot-design or storyboard-test intent; explicit wally mention is not required. Keep original screenwriting, static asset design, performance/dialogue/audio design, returned-board review, and final video prompt assembly outside this skill."
---

# Wally Storyboard Designer

Provide on-demand storyboard-domain functions for the user's supplied story, scene, or shot material.

This skill is the test layer of the Wally pipeline. It designs the 分镜脚本 (processed director script) in text, then issues the fixed storyboard or shot-table prompt so the user can generate boards cheaply and see whether the shot design reads as intended. The user judges the generated boards; this skill does not review them. What the user saw comes back here as targeted 分镜脚本 revision instructions.

Current version: `wally-storyboard-designer@2026-08-19-v3.9-four-rule-layout`

## Changelog

- `2026-08-19-v3.9-four-rule-layout`: Reduce the scene-layout SVG contract to four rules: explicit source scenes, initial state only, active-interaction content only, and true top-down geometry. Remove camera-continuity construction and visual-hierarchy directives from this product.
- `2026-08-19-v3.1-interaction-layout`: Restrict scene-layout SVGs to character starting positions and only the environment or objects that characters visibly interact with; passive location-establishing boundaries and background anchors are omitted.
- `2026-08-18-v3.0-test-layer`: Reposition the skill as the test layer. Cut visual optimization, storyboard design, main-shot adjudication, returned-board review, continuity validation, and the fixed document scaffold together with their guides; merge the composition rules into the shot format and retire that file. The 分镜脚本 now follows one principle (一切为了讲故事，内容是优先级最高的评判标准), one contract (shot format `拍摄手法 / 画面内容 / 任务`, duration only on request, the core rule 如果你不确定，就写得更少, and a two-pass approach: key pictures written as main shots first, connecting shots second), and the fixed test prompts; the user judges the boards.
- `2026-08-18-v2.1-adversarial-main-shot`: Require blind multi-agent proposal, adversarial deletion and merge tests, and evidence-based adjudication before locking any source scene's main-shot set.
- `2026-08-18-v2.0-source-scene-authority`: Treat the source screenplay's existing scene boundaries, exact headings, and order as the sole scene authority for every generation product.
- `2026-07-28-v1.19-work-definition-inheritance`: Inherit and display the upstream work definition without originating it.
- `v1.18-functional-only-scope`: Keep storyboard-domain functions on demand.

## Accept the user's current material

- Accept scene-divided scripts, individual scene excerpts, briefs, test plots, tables, images, asset references, partial artifacts, conflicting drafts, existing director scripts or shot sequences, the user's observations from generated boards, or any mixture.
- Do not require completeness, a locked or approved source, a particular schema, an asset package, a route choice, or a fixed starting stage. Surface only conflicts that would materially change the named product.
- Preserve supplied story facts. Do not expand, rewrite, doctor, or originate the screenplay; send original screenwriting work to `wally-screenplay-writer`.
- For a generation product that needs scene boundaries, require an upstream screenplay or excerpt with explicit source scenes. When those boundaries are absent, stop and route scene formation to `wally-screenplay-writer`; never split, merge, or number the material in this skill.
- Treat the source scene boundaries, exact headings, and order as the sole authority. Never split, merge, rename, normalize, or renumber them.
- A source scene may contain multiple action chains, multiple dramatic beats, multiple storyboard pages, and any number of necessary shots.
- Preserve the latest explicit or approved `作品定义` as source authority. Keep work form, commercial function, narrative mode, delivery format, and audiovisual position distinct.
- **Functions are on-demand.** Deliver exactly the product the user names — nothing before it, nothing after it. Do not pull in earlier stages, volunteer later stages, or ask sequence questions. If the named product lacks a required input, name the missing input and stop; do not produce the upstream product uninvited.

## Inherit the work definition

- Copy the source screenplay's `## 作品定义` block verbatim into every complete 分镜脚本.
- When the user states the definition directly but the source lacks a block, transcribe only those explicit decisions into the same field structure; do not infer unsupported classification.
- Treat work type as upstream story authority. This skill may use `剧情短片`, `广告片`, `纪录片`, `MV或视觉片`, or `剧集内容` to control coverage and shot language, but it may not originate or doctor that choice.
- For a complete 分镜脚本, surface a missing definition when the difference between advertisement, narrative film, documentary, MV/visual piece, or episodic content would materially change the result. Request the definition from the user or `wally-screenplay-writer`; do not silently guess.
- Keep definition metadata outside source scene passages and shot blocks. Do not turn labels such as commercial function, genre, or audiovisual position into visible objects, dialogue, or per-shot prompt detail.

## Workflow

One loop: design the 分镜脚本 in text → issue the fixed test prompt → the user judges the boards → targeted revision. Each step is also a product the user can request on its own; do not pull in an earlier step or volunteer a later one.

### Scene-layout SVG (optional, before shots)

When the user explicitly starts a new spatial-planning SVG task, read [references/scene-layout-svg-rules.md](references/scene-layout-svg-rules.md) and create only the named SVGs. A stopped or deleted SVG request does not carry forward into later turns.

### 分镜脚本 (processed director script)

Read [references/director-script-output-contract.md](references/director-script-output-contract.md): choose shots by its principle, prepend the inherited work definition, group shots under the original source scene headings, and write each shot in its format. When the user brings back what they saw in the boards, apply the contract's targeted-revision rule: only the named shots change.

### Fixed storyboard and shot-table prompts (the test step)

These prompts are how a 分镜脚本 gets tested: the user uploads the 分镜脚本 and any static assets to the image model, sends the fixed prompt, generates boards, and judges them by eye.

- Keep the fixed storyboard and shot-table prompt templates verbatim. Their exact-payload contract is unchanged.
- For the storyboard prompt, read [templates/storyboard-prompt-template.md](templates/storyboard-prompt-template.md) and output only its stored, labeled `【故事板生成模版】` payload and separate labeled `【短任务提示词】` payload. There is no rough/formal grade; one fixed storyboard prompt serves every storyboard request, and `Bxx` remains only the identifier for returned boards.
- For the shot-table (分镜表) prompt, read [templates/shot-table-prompt-template.md](templates/shot-table-prompt-template.md) and output only its stored, labeled `【分镜表生成模版】` payload and separate labeled `【短任务提示词】` payload.
- For either short-task payload, replace only the literal `【源场景标题】` with the exact original source scene heading when the request or supplied material provides one. Do not infer, normalize, rename, or renumber a heading. Leave `【源场景标题】` unchanged for a generic reusable prompt with no exact source heading.
- Storyboards and shot tables have different strengths: a storyboard gives annotated per-shot direction sketches (景别/运镜/动作); a shot table renders the model's native 分镜表 concept — the complete source-scene shot sequence, numbered panels, no text, no style constraints. One source scene may use multiple pages and as many shots as needed. The choice between the two products belongs to the user.
- The exact runtime `【源场景标题】` replacement above is the only allowed payload substitution. Do not modify the stored templates or otherwise fill, summarize, explain, relabel, wrap, or append anything to either fixed prompt.
- If the requested prompt type is unclear and cannot be inferred, ask only whether the user wants the storyboard prompt or the shot-table 分镜表 prompt.

## Boundaries

- Do not originate, rewrite, validate, or doctor a screenplay as a screenplay; do not produce a visually optimized rewrite of source scenes.
- Do not split, merge, rename, normalize, or renumber source scenes.
- Do not design character, group, scale, prop, scene, or other static assets.
- Do not design performance, dialogue, vocal delivery, timing performance, or audio design.
- Do not offer returned-board review as a product. The user judges the generated boards; treat what the user reports as revision input to the 分镜脚本.
- Do not choose Route A/B or assemble a final image-to-video or text-to-video prompt.
- Keep both fixed prompt templates, including the storyboard style block inside the storyboard template, unchanged unless the user explicitly requests an exact template edit. For an authorized edit, change only the named text surface and preserve the rest verbatim.
