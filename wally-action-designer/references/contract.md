# Adaptive Director Body Contract（单一真源）

Define the finished `wally-action-designer` body here. This is the output-structure contract, not a promise that generation is deterministic. `craft.md` owns generation method; this file owns field selection, execution-carrier selection, formatting, and reviewable completeness; `review.md` owns rerun, edit, and extension decisions.

## Core rule

First identify information that is present in the supplied material and materially controls generation. Output only the fields that carry that information.

- Do not output an empty field, placeholder, a standalone `无` or `不适用` field value, or filler written only to complete a schema.
- Treat the local Sora skill's prompt-augmentation template as the semantic source of truth for every emitted borrowed label: `Use case`, `Primary request`, `Scene/background`, `Subject`, `Action`, `Camera`, `Lighting/mood`, `Color palette`, `Style/format`, `Timing/beats`, `Audio`, `Text (verbatim)`, `Dialogue`, and `Constraints`. Keep those labels' Sora meanings and include-only-when-relevant behavior; do not invent a Wally-specific alternative meaning. Use Sora's `Constraints: <must keep/must avoid>` slot as the single constraint structure and compile any independent negative failure modes into it; never emit a separate `Avoid:` field. `Acting`, `Continuity`, `Physics`, and Shot blocks are Action Designer additions and may extend the structure without redefining borrowed fields.
- Give each fact one owning field. If another field already expresses it completely, omit the duplicate field or sentence.
- Treat every populated global field as a promise to every Shot within its stated scope. A Shot may specialize a global control but may not contradict it. When authoritative Shots differ, narrow or condition the global wording to the actual shared rule, or move the specific control into its owning Shot; never rewrite a valid Shot merely to rescue an overbroad global sentence.
- An omitted field is not a defect unless its missing information makes this task non-executable.
- `Audio` always carries real content because every Wally director body requires a complete sound state. If music is unspecified, default to no BGM and substantive ambience/SFX; if music is explicitly supplied or requested, describe it accurately; if absolute silence is required, add no sound. Designed silence is content; an empty audio placeholder is not.

## Canonical field order

Keep every field that is used in this relative order. There is no required-field checklist apart from the substantive adaptive `Audio` contract above.

```text
Use case:
Primary request:
Scene/background:
Subject:
Style/format:
Lighting/mood:
Color palette:
Camera:
Acting:
Continuity:
Physics:
Action:
Timing/beats:
Audio:
Text (verbatim):
Dialogue:
Constraints:
```

When Shot blocks are the top-level execution carrier, place them where top-level `Action` and `Timing/beats` would appear: after any used `Physics` field and before `Audio`. Each Shot then owns one or more direct local timecode lines. Those lines belong to the Shot block and do not violate the one-carrier rule. Do not add a replacement summary paragraph.

The body starts directly at its first populated field. Use short labeled lines and omit irrelevant sections. Map any useful prose-scene information into the existing fields; do not add an unlabeled prose template, title, preface, `风格前缀：`, `Reference:`, platform handle, `Mixed N`, upload order, Asset List, Reference List, or Route heading.

## Choose one top-level execution carrier

### Action only

Use `Action:` for one continuous action when exact internal timing is not needed. Do not create `Timing/beats`, `Shot 1`, or an unlabeled story summary.

### Action plus Timing/beats

Use `Action:` plus `Timing/beats:` for a single shot or continuous take whose order, synchronization, or stage change matters. Let `Action` own only participant or tool roles and the overall task identity; let the beats own every ordered step, stage change, sound trigger, and landing. Do not repeat the beat verbs or ending inside `Action`, and do not create `Shot 1` or an unlabeled story summary.

### Shot blocks

Use one or more `**Shot N [start-end s]**` blocks only when:

- the material contains multiple shots;
- an approved storyboard, director script, or other shot authority locks shot decisions; or
- the user explicitly requests Shot output.

Preserve authoritative shot count, order, framing, movement, action, space, props, dialogue, and outcomes. When shot count is genuinely open, use the fewest shots that execute the supplied process. With Shot blocks, omit global `Action:`, global `Timing/beats:`, and any unlabeled execution-summary paragraph.

Give every Shot one direct local timeline:

- one continuous action: one range spanning the Shot duration, such as `0.0-4.0s: [one clear action and landing]`; or
- staged action: multiple sequential lines such as `0.0-2.0s: [first action]` and `2.0-4.0s: [second action and landing]`.

Do not add `Action:`, `Timing/beats:`, `beat N`, bullets, brackets, or parentheses to Shot-local timecode lines. Each range stands at the start of its own line, includes `s` immediately after the end time, and ends with an ASCII colon. The local timeline owns every ordered verb and landing for that Shot; any preceding Shot text may establish only the visible setup, framing, camera, space, or initial state.

Shot headers use the full-video timeline and retain the `s` suffix inside ASCII square brackets. Direct Shot-local timecode lines reset to `0.0s`, stay sequential and non-overlapping, and end at the Shot duration. Never repeat the header's global timestamps inside the local sequence. Use whole seconds or at most one decimal when needed; do not import frame or millisecond precision unless the user explicitly requires it.

Apply the short-beat and multi-Shot action economy defined in `craft.md`. A Shot with no meaningful stage change uses one direct local timecode line spanning its duration.

Every exact time range requires a user-supplied or explicitly approved target duration. Keep ranges ordered and within that duration; do not invent seconds.

Before finalizing, compare every Shot against every populated global field and the downstream `Audio` and `Constraints` fields in both directions. Resolve conflicts in the field that owns the overbroad or misplaced claim. In particular:

- a global `Camera`, `Acting`, `Continuity`, or `Physics` statement must either hold for every Shot it covers or explicitly scope the Shots or conditions where it applies;
- `Audio` must not assign sound, music, dialogue, or silence that contradicts a Shot-specific requirement;
- `Constraints` must not freeze, preserve, forbid, or require an object, hand, camera, text, or state that a Shot must add, remove, move, reveal, hide, or change. Its negative clauses must not ban required physical signage, product marks, screen content, props, actions, or camera behavior; target only the unwanted added or malformed version when the required version must remain.

## Field specs

### Use case

Use Sora's exact meaning: `<where the clip will be used>`. Include it only when the user or locked material supplies a concrete destination or placement, such as a product teaser, social ad, UI product demo, cinematic insert, or ambient background loop, and that fact adds control not already fully expressed elsewhere. Do not describe why the prompt is being written, the AI-generation workflow, reference-video analysis, model evaluation, a director body, an acceptance document, or the requested action itself. If no concrete clip use is supplied or the line would be redundant, omit the field.

### Primary request

Use Sora's exact meaning: `<user's main prompt>`. State the user's requested clip or change directly. Do not replace it with workflow commentary, a field inventory, or a duplicate `Use case`.

### Scene/background

Use Sora's meaning: `<location, time of day, atmosphere>`. Add only supplied or materially controlled visible setting facts, including background occupancy, era, spatial context, cleanliness, contamination, damage, or disorder when needed. Omit it when a supplied image already fixes the background and no change or preservation instruction is needed. In Shot mode, keep differing per-Shot scene conditions in the owning Shot instead of flattening them into one global line.

### Subject

Use Sora's meaning: `<main subject>`. Name the visible main person, object, material, or product and only its initial state needed to identify the subject. Use the supplied human-readable identity name verbatim when it materially supports continuity, without outputting a binding or handle. Do not use this field as a continuity checklist or complete prop inventory unless the inventory itself is the main subject.

### Style/format

Use Sora's meaning: `<film/animation/format cues>`. Specify visible medium, realism, image texture, capture character, period treatment, aspect ratio, filter character, grade, or decisive format only when the task supplies or needs them. Translate abstract praise into visible controls. Do not invent a prestige style paragraph.

### Lighting/mood

Use Sora's meaning: `<lighting + mood>`. Specify light quality, motivated sources, direction, subject/background exposure, atmosphere, or a story-driven light change only when light materially controls the result. Preserve one lighting logic across visibly continuous Shots.

### Color palette

Use Sora's meaning: `<3-5 color anchors>`. Specify stable color anchors, saturation, contrast, or material color relationships only when color is independently controlled.

### Camera

Use Sora's meaning: `<shot type, angle, motion>`. State shared framing or capture behavior: shot size, angle, lens character, depth of field, stability, one dominant movement, edit logic, or aspect ratio, but only the controls that matter. Use lens, depth of field, and straight-on text-framing heuristics from `craft.md` only when the task or material actually leaves those decisions open. In Shot mode, keep shot-specific position, path, subject relation, and landing inside each Shot.

When Shots use different valid camera states, express only their common capture logic globally and keep each exact state in its Shot. Do not say `每镜`, `全程`, `始终`, or `只有` for a movement or stability rule that any Shot violates.

Use `固定机位` only when the camera has no translation or rotation; never pair it with push, pull, pan, tilt, track, or orbit.

### Acting

Use only for actual human or character performance, vocal weight, dialogue mode, restraint, theatricality, listener behavior, or lip-sync control. Object motion, hands performing a craft operation, and ordinary subject movement do not automatically require `Acting`.

### Continuity

Use only for identity, wardrobe, prop, position, state, edit, or cross-shot invariants that must survive a cut or transformation. Establish one canonical core description for a continuing character or product and repeat that wording exactly wherever the body must restate it; do not synonym-rewrite or add competing traits. A single continuous action with no independent invariant does not require this field.

Do not generalize one Shot's hand count, left/right assignment, wardrobe, prop count, visibility, or state to all Shots. If a Shot intentionally differs, state the applicable scope or the permitted transition instead of declaring an absolute invariant.

### Physics

Use only for non-default material, fluid, smoke, cloth, collision, deformation, reflection, transformation, contact, or occlusion rules. State the causal physical behavior once; do not repeat it in `Action` or `Constraints`.

Scope a physical result to the Shots or events that actually display it. Do not require every Shot to show an entry, impact, deformation, collection, reflection, or final state that only some Shots contain.

### Action

Use Sora's meaning: `<single clear action>`. Write the primary visible process with playable verbs, reachable targets, cause before response, and the intended landing. Keep supplied actions; do not infer gait mechanics, force, weight transfer, micro-gestures, or secondary reactions.

### Timing/beats

Use Sora's meaning: `<counts or beats>`. Use this top-level field only with the single-shot `Action plus Timing/beats` carrier and only when timing or synchronization matters. Each beat owns its time-specific action, change, dialogue, visible text, or sound trigger. Apply the counts-or-steps rule from `craft.md`. In Shot mode, use the Shot-local timing form instead and omit this field.

### Shot blocks

For each Shot, include only useful visible controls: global time range, framing, frame-zero camera position or camera behavior already active at frame zero, spatial relationship, initial visible scene and subject state, direct Shot-local timecode lines, locked dialogue, visible text, and decisive sound trigger. Every setup sentence before the local timeline describes only facts or an already-active camera behavior true at that Shot's `0.0s`; every action, camera, or state change after frame zero belongs to a direct local timecode line. Use one full-duration line when no meaningful stage change exists; use multiple lines when order or timing matters. One Shot has one main story job, one primary action, and one dominant camera behavior unless the shot authority explicitly locks more.

For cleaning, restoration, organization, damage-removal, before/after, or product-efficacy work, every affected Shot must establish a renderable frame-zero condition before its first action: name the visible dirt, debris, damage, or disorder; quantify its amount or density in practical visual terms; describe its distribution pattern; and locate it on the relevant surface, edge, seam, groove, corner, container, or background zone. A display or storage Shot must instead state that its presentation surface is clean, empty, or orderly and identify the objects intentionally present. Do not use a bare adjective such as `脏乱` as the whole setup. When source or locked material controls the condition, preserve it; when the condition is open, choose the smallest visible setup that makes the intended effect readable without inventing a product claim.

For independently generated clips, begin a visibly continuous Shot with the prior landing as facts already true at 0.0s. A fresh setup defines its own frame-one state. Never narrate history the model cannot remember.

### Audio

Use Sora's meaning: `<ambient cue / music / voiceover if requested>`. Action Designer extends this borrowed field into one complete sound state using exactly the applicable branch:

- Music unspecified: start with `无BGM。`, then design the ambience, room tone, foley, action-triggered sound, voice acoustics, spatial behavior, transitions, and meaningful silence that matter.
- Music explicitly supplied or requested: accurately describe the supplied or controlled music and its relationship to voices and scene sounds; do not output `无BGM。`.
- Absolute silence explicitly required: state that the whole scope is absolutely silent and add no ambience, foley, dialogue, voiceover, or music.

Put an exact causal sound in a beat or Shot when its trigger controls timing; keep the global field for the shared sound state. Do not infer music merely because the use case is an advertisement or montage.

### Text (verbatim)

Use Sora's meaning: `<exact text>`. Include only when the model must render exact visible text. Enclose every exact string in Chinese double quotation marks `“……”`, state its screen/surface and position, and require stable legibility without motion blur when camera authority leaves that choice open. Preserve locked camera decisions and report a genuine legibility conflict instead of silently redesigning the Shot. Put time-bound text in the relevant beat or Shot instead of repeating it here.

### Dialogue

Use Sora's dedicated dialogue block with short, consistently labeled speaker lines. Include only when actual spoken content exists and its wording is explicitly locked by the user or approved in the supplied screenplay. Preserve approved wording, speaker label, order, and voice mode exactly; control only delivery, acting, lipsync, pauses, timing, placement, and acoustics. If wording is absent, provisional, contradictory, too long, or requires invention/rewrite, report the conflict and route the wording decision to `wally-screenplay-writer`; do not create alternatives. Keep dialogue in `「……」`, keep lines short enough for the available beat, and use consistent speaker labels. Put time-bound dialogue in the relevant beat or Shot instead of repeating it here.

### Constraints

Use Sora's meaning: `<must keep/must avoid>`. This is the only constraint structure. Put unique positive invariants first, followed by only the independent negative failure modes that materially threaten this generation, in the same `Constraints:` paragraph or line. Do not add nested `Must keep`, `Must avoid`, or `Avoid` sublabels, and never emit a separate `Avoid:` field. Do not convert every descriptive fact into a constraint or restate a positive invariant in negative form.

Check every invariant against the Shot timeline. Do not use `始终`, `保持不变`, `只有`, or an equivalent absolute when a required beat changes that property. State the stable interval and the permitted mover, entrant, exit, reveal, or transformation explicitly.

Before adding a negative clause, verify that no Shot requires the physical or diegetic form being restricted. When it does, target only the added overlay, substitution, malformed copy, or other unwanted variant while preserving the required form. Omit negative clauses entirely when no independent high-risk failure is present.

## Output discipline

- Preserve locked story facts, dialogue, speaker, order, and outcomes exactly.
- Preserve supplied shot authority; compile it into executable model language without redesigning it.
- Treat a supplied input image as frame zero: place only already-visible composition, identity, product state, and set dressing in setup fields or Shot setup; let the execution carrier own what happens next.
- Keep psychological reasoning internal; convert it into gaze, breath, posture, action, pause, voice, distance, contact, or refusal only when supported.
- Keep each fact at one layer. Global fields own shared controls; a top-level Action/Timing carrier or each Shot's direct local timeline owns execution; `Constraints` owns unique positive invariants and independent negative failure modes in one structure.
- Resolve every global-to-Shot and Shot-to-downstream contradiction before output. Prefer narrowing the overbroad field over weakening or redesigning authoritative Shot content.
- Do not emit both a global execution summary and a detailed execution carrier.
- Use ASCII square brackets for Shot headers, such as `Shot 1 [0.0-5.0s]`. Format each Shot-local action as a standalone range with `s` immediately before the ASCII colon, such as `0.0-2.0s: ...`; use no `Action:`, `beat N`, brackets, parentheses, or bullets on those local lines. Keep performance directions and audio triggers in forms such as `角色[压低声音]：「台词」` and `[Audio trigger: ...]` only when relevant.
- Return only the finished body, without notes or analysis.

## Adaptive skeletons

### Continuous action

```text
[Only populated fields before execution, in canonical order.]
Action: [One continuous visible process and landing.]
Audio: [Complete adaptive sound state: default no-BGM ambience/SFX, explicitly supplied music, or explicit absolute silence.]
[Only populated Text, Dialogue, or Constraints fields, in canonical order.]
```

### Single shot with precise beats

```text
[Only populated fields before execution, in canonical order.]
Action: [Concise whole process.]
Timing/beats:
0.0-1.0s: [First meaningful stage.]
1.0-3.2s: [Second meaningful stage.]
3.2-4.0s: [Landing.]
Audio: [Complete adaptive sound state: default no-BGM ambience/SFX, explicitly supplied music, or explicit absolute silence.]
[Only populated Text, Dialogue, or Constraints fields, in canonical order.]
```

### Multiple or authoritative shots

```text
[Only populated global fields through Physics, in canonical order.]

**Shot 1 [0.0-4.0s]**
[Only this Shot's useful setup, framing, camera, space, or initial-state controls.]
0.0-2.0s: [First sequential action.]
2.0-4.0s: [Second action and landing.]

**Shot 2 [4.0-7.0s]**
[Only this Shot's useful setup, framing, camera, space, or initial-state controls.]
0.0-3.0s: [One continuous action and landing.]

Audio: [Shared adaptive sound state not already owned by a Shot trigger.]
[Only populated Text, Dialogue, or Constraints fields, in canonical order.]
```

## Gold example: 4-second clay test

```text
Primary request: 生成一条写实的4秒竖屏手作视频。
Scene/background: 简洁的浅灰白桌面，安静室内，没有其他工具或杂物。
Subject: 一双结构自然稳定的成人手；一个手掌大小的白色黏土半身像，开场时已有完整脸部、头颈、肩膀和多层衣褶，后脑没有头发。
Style/format: 9:16竖屏写实手机手作教程质感，连续实拍感，无定格动画或跳帧。
Lighting/mood: 柔和均匀的中性顶光，白色黏土纹理清楚。
Camera: 固定俯斜微距近景，主体居中，全程无变焦、摇移或切镜。
Physics: 黏土只在手指实际接触并施压的位置变形，附加块逐步与后脑融合，不自行融化、增殖或瞬间变形。
Action: 一只手全程只负责托稳半身像，另一只手是唯一塑形执行者，只处理后脑的附加黏土。
Timing/beats:
0.0-1.0s: 独立小块黏土被贴稳在后脑。
1.0-3.2s: 指腹沿上缘和两侧接缝按压、推开并向下抹合。
3.2-4.0s: 手指离开，完成状态稳定展示。
Audio: 无BGM。只有轻微室内底噪和指腹摩擦柔软黏土的近距离声音，无旁白。
Constraints: 始终只有一个半身像和一块附加黏土；既有脸部、衣褶、肩膀和整体比例保持不变；避免多指或缺指、手指穿透黏土、手与雕像粘连、雕像重置或复制、新增工具、字幕、水印或任何文字。
```

The example intentionally has no `Use case`, because no concrete destination for the finished clip was supplied; “AI视频模型测试” would describe evaluation intent rather than where the clip will be used. It also has no `Acting`, `Continuity`, `Color palette`, story summary, `Shot 1`, or separate `Avoid`; `Action` owns hand roles and the overall landing, `Timing/beats` owns step detail, and physics, invariants, and failure modes each have one owner.

## Pre-flight checklist

- Does every emitted field carry unique task-specific control information?
- Does every borrowed Sora label keep the local Sora template's meaning, and has every irrelevant borrowed field been omitted?
- If `Use case` appears, does it answer where the finished clip will be used, without describing the prompt, workflow, evaluation process, director body, or action request?
- Are empty fields, placeholders, filler, and redundant restatements absent?
- Is the top-level execution carrier the smallest sufficient one: Action, Action plus Timing/beats, or Shots?
- If Shots are used, are global Action, global Timing/beats, and an unlabeled execution summary absent, and does every Shot contain one or more direct local timecode lines with no `Action:`, `beat N`, parentheses, bullets, or brackets, and with `s` immediately before the ASCII colon?
- Do direct Shot-local timecode lines reset to `0.0s`, remain sequential and non-overlapping, use no more than one decimal when needed, and end at that Shot's duration without repeating global timestamps?
- If exact time ranges are used, do they fit the approved duration?
- For cleaning, restoration, organization, damage-removal, before/after, or product-efficacy work, does every affected Shot establish the frame-zero condition with visible type, amount or density, distribution, and location; and does every display or storage Shot establish its clean or ordered baseline?
- Does every global field hold for every Shot it claims to cover, with valid local differences expressed as specializations rather than contradictions?
- Do `Audio` or `Constraints` assign, freeze, or prohibit anything that a Shot must change, move, reveal, sound, display, or preserve?
- Have absolute terms such as `每镜`, `全程`, `始终`, `只有`, `不`, and `保持不变` been checked against every Shot and beat in their stated scope?
- Are cause, action, response, and landing executable and source-preserving?
- Are `Acting`, `Continuity`, and `Physics` present only for their actual professional purposes?
- Does `Audio` use the correct branch: default `无BGM。` plus substantive ambience/SFX, explicitly supplied music without `无BGM。`, or explicit absolute silence with no added sound?
- If an input image anchors frame zero, do setup fields contain only already-visible facts while every subsequent change stays in the execution carrier?
- When continuing identity or product description is restated, is its canonical core wording identical rather than synonym-rewritten or contradicted?
- If exact visible text exists, are its wording, surface/position, and stable legibility controlled without overriding shot authority?
- Are exact visible strings in `“……”` and dialogue in `「……」`, only when they exist?
- Does one `Constraints:` field contain only unique positive invariants and independent negative failure modes, with no separate `Avoid:` field or nested must-keep/must-avoid structure?
- Is the body free of `Reference:`, platform handles, and Route/Asset/Reference-List content?
- Does the product stay inside director-design responsibility?
