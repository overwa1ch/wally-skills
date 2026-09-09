# Adaptive Director Body Contract（单一真源）

Field selection and output syntax for the finished director-design prompt.

## Core rule

First identify information that is present in the supplied material and materially controls generation. Output only the fields that carry that information.

- State control requirements directly. Include a restriction when the supplied task or an observed failure establishes its purpose and scope.
- Do not output an empty field, placeholder, a standalone `无` or `不适用` field value, or filler written only to complete a schema.
- Give each fact one owning field. If another field already expresses it completely, omit the duplicate field or sentence.
- Treat every populated global field as a promise to every Shot within its stated scope. A Shot may specialize a global control but may not contradict it. When Shots need different controls, narrow or condition the global wording to the actual shared rule, or move the specific control into its owning Shot; never rewrite a valid Shot merely to rescue an overbroad global sentence.
- An omitted field is not a defect unless its missing information makes this task non-executable.

## Canonical field order

Begin with `Style` and keep other populated fields in this relative order. Always include the sound state in `Audio`; select the remaining fields according to the task.

```text
Style:
Reference:
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

The body starts directly at `Style:`. Use short labeled lines and omit irrelevant sections. `Reference` owns material identifiers and their object bindings; later fields and Shots use the same object names. Map prose-scene information into the existing fields. Upload instructions, Asset/Reference Lists, and Route headings belong to final assembly.

## Choose one top-level execution carrier

### Action only

Use `Action:` for one continuous action when exact internal timing is not needed. Do not create `Timing/beats`, `Shot 1`, or an unlabeled story summary.

### Action plus Timing/beats

Use `Action:` plus `Timing/beats:` for a single shot or continuous take whose order, synchronization, or stage change matters. Let `Action` establish the participants, tools, initial state, and overall task; let the beats own every ordered step, stage change, sound trigger, and landing. Do not repeat the beat verbs or ending inside `Action`, and do not create `Shot 1` or an unlabeled story summary.

### Shot blocks

Use one or more Shot blocks in the form `**Shot 1 [0.0-4.0s]**` only when:

- the requested video needs multiple shots; or
- the user explicitly requests Shot output.

Preserve shot count, order, framing, movement, action, space, and props when explicitly specified by the user, together with approved dialogue and story outcomes. Develop remaining choices from the supplied materials. When shot count is open, use the fewest shots that execute the supplied process. With Shot blocks, omit global `Action:`, global `Timing/beats:`, and any unlabeled execution-summary paragraph.

Give every Shot one direct local timeline:

- one continuous action: one range spanning the Shot duration; or
- staged action: sequential ranges divided at meaningful changes in action or response.

Do not add `Action:`, `Timing/beats:`, `beat N`, bullets, or parentheses to Shot-local timecode lines. Each range stands at the start of its own line, includes `s` immediately after the end time, and ends with an ASCII colon. The local timeline owns every ordered verb and landing for that Shot; any preceding Shot text may establish only the visible setup, framing, camera, space, or initial state.

Shot headers use the full-video timeline. Direct Shot-local timecode lines reset to `0.0s`, stay sequential and non-overlapping, and end at the Shot duration. Never repeat the header's global timestamps inside the local sequence. Use whole seconds or at most one decimal when needed; do not import frame or millisecond precision unless the user explicitly requires it.

Every exact time range requires a user-supplied or explicitly approved target duration. Keep ranges ordered and within that duration; do not invent seconds.

## Field specs

### Style

Open with the supplied era, region, location, and time of day together with the overall visual treatment, medium, realism, aspect ratio, or content format. Put detailed capture, lens, and filter choices in `Camera`. Include the supplied duration and shot count here when they define the requested clip. Use the information the task provides; for multiple locations or times, keep the shared visual treatment here and state each location and time in its Shot setup.

### Reference

Place `Reference` immediately after `Style` when the prompt uses reference materials. Write ordinary sentences that explicitly connect each named object and reference purpose to its material identifier: **object + aspect to follow + source label**. Objects can be characters, locations, props, vehicles, or other named subjects. Distinguish a character's appearance source from their voice source; each clause must make that correspondence unambiguous.

Use the material labels supplied by the user or shown on the platform, preserving syntax such as `{{Mixed 1}}` or an existing `@` handle. When platform numbering is unavailable, use supplied, distinguishable attachment names; resolve an ambiguous object-to-material assignment before finalizing that binding. Later Shots, `Acting`, and `Audio` refer to the same object names. `Continuity` describes how their states and relationships persist across cuts.

Apply a reference to its stated aspect. A character appearance image controls appearance; a voice sample controls the named speaker's vocal character. Treat an image as the exact opening composition when the user assigns it the first-frame role.

### Lighting/mood

Specify light quality, motivated sources, direction, subject/background exposure, atmosphere, or a story-driven light change only when light materially controls the result. Preserve one lighting logic across visibly continuous Shots.

### Color palette

Specify three to five stable color anchors, saturation, contrast, or material color relationships only when color is independently controlled.

### Camera

Describe the intended image and viewing experience: what stays sharp, how much background remains readable, skin and material texture, grain, highlight and shadow treatment, motion rendering, camera stability, movement, and editing rhythm. Select the aspects that matter to this scene and write them in connected prose.

Choose named equipment, film stocks, filters, and numerical settings by the specific control they add to this scene: composition, focus, motion, color response, texture, or continuity. Use the level of technical detail those controls require. Keep useful precision and consolidate equivalent settings; each retained detail needs a concrete purpose and a plausible technical basis. Treat values in supplied examples as scene-specific choices to reassess, while preserving parameters explicitly locked by the user. A model prompt may use equipment as a look reference; claims of physical feasibility or generation improvement require corresponding evidence.

Keep shared photographic choices here; place each Shot's framing, position, focus, movement, and specific cut or sound bridge in that Shot. Include its lens and aperture when supported by the above rule. Light-source placement belongs to `Lighting/mood`.

### Acting

Use only for recurring human or character controls that are directly visible or audible across the declared scope: posture baseline, gaze behavior, movement tempo, vocal intensity, listener response, restraint, theatricality, or lip-sync. Omit the field when those facts are already owned by the timeline.

### Continuity

Use only for identity, wardrobe, prop, position, state, edit, or cross-shot invariants that must survive a cut or transformation. Establish one canonical core description for a continuing character or product and repeat that wording exactly wherever the body must restate it; do not synonym-rewrite or add competing traits. A single continuous action with no independent invariant does not require this field.

Keep object-to-material bindings in `Reference`; put required cross-shot states and relationships in `Continuity`.

Do not generalize one Shot's hand count, left/right assignment, wardrobe, prop count, visibility, or state to all Shots. If a Shot intentionally differs, state the applicable scope or the permitted transition instead of declaring an absolute invariant.

### Physics

Use only for non-default material, fluid, smoke, cloth, collision, deformation, reflection, transformation, contact, or occlusion rules. State the causal physical behavior once; do not repeat it in `Action` or `Constraints`.

Scope a physical result to the Shots or events that actually display it. Do not require every Shot to show an entry, impact, deformation, collection, reflection, or final state that only some Shots contain.

### Action

Write the primary visible process with playable verbs, reachable targets, cause before response, and the intended landing.

### Timing/beats

Use this top-level field only with the single-shot `Action plus Timing/beats` carrier and only when timing or synchronization matters. Each beat owns its time-specific action, change, dialogue, visible text, or sound trigger. In Shot mode, use the Shot-local timing form instead and omit this field.

### Shot blocks

For each Shot, include only useful visible controls. Build the frame-zero setup adaptively from: viewpoint and axis relationship; shot size, lens, angle, and camera position; foreground framing or occlusion; focus owner and depth of field; foreground-subject-background layers and initial positions; initial visible scene and subject state; and camera behavior already active at frame zero. Use visible subject relationships for axis and position instead of invented compass directions or opaque table-side labels. Do not mechanically populate every slot.

Every setup sentence before the local timeline describes only facts or an already-active camera behavior true at that Shot's `0.0s`. Every action, camera response, path, contact, state change, landing, locked dialogue, visible text change, or decisive sound trigger after frame zero belongs to a direct Shot-local timecode line. When useful, order those changes as trigger, camera response, subject path or contact, relationship landing, and exact dialogue or sound. Use one full-duration line when no meaningful stage change exists; use multiple lines when order or timing matters. Identify each Shot's main story job, primary action, and dominant camera behavior while preserving the user's explicit requirements.

Budget duration for action preparation, camera response, contact, settling, spoken delivery, and listener registration according to their causal dependencies and natural overlap. If approved action, camera, and dialogue cannot fit, simplify an unlocked camera response or report the locked-duration conflict. Compress background extras into one low-weight shared state unless an individual changes the story.

For independently generated clips, begin a visibly continuous Shot with the prior landing as facts already true at 0.0s. A fresh setup defines its own frame-one state. Never narrate history the model cannot remember.

### Audio

Describe the complete sound state using the applicable branch:

- Music unspecified: start with `无BGM。`, then design the ambience, room tone, foley, action-triggered sound, voice acoustics, spatial behavior, transitions, and meaningful silence that matter.
- Music explicitly supplied or requested: accurately describe the supplied or controlled music and its relationship to voices and scene sounds; do not output `无BGM。`.
- Absolute silence explicitly required: state that the whole scope is absolutely silent and add no ambience, foley, dialogue, voiceover, or music.

Put an exact causal sound in a beat or Shot when its trigger controls timing; keep the global field for the shared sound state. Do not infer music merely because the use case is an advertisement or montage.

### Text (verbatim)

Include only when the model must render exact visible text. Enclose every exact string in Chinese double quotation marks `“……”`, state its screen/surface and position, and require stable legibility without motion blur when the user leaves camera choices open. Preserve camera decisions explicitly specified by the user and report a genuine legibility conflict instead of silently redesigning the Shot. Put time-bound text in the relevant beat or Shot instead of repeating it here.

### Dialogue

Use consistently labeled speaker lines. Include only when actual spoken content exists and its wording is explicitly locked by the user or approved in the supplied screenplay. Preserve approved wording, speaker label, order, and voice mode exactly; control only audible delivery, lipsync, pauses, timing, placement, and acoustics. If wording is absent, provisional, contradictory, too long, or requires invention/rewrite, report the conflict and route the wording decision to `wally-screenplay-writer`; do not create alternatives. Keep dialogue in `「……」`, keep lines short enough for the available beat, and use consistent speaker labels. Put time-bound dialogue in the relevant beat or Shot instead of repeating it here. Write the speaker's visible action or indispensable audible delivery as ordinary prose in the same timeline sentence.

### Constraints

Put unique positive invariants first, followed by only the independent negative failure modes that materially threaten this generation, in the same `Constraints:` paragraph or line. Do not add nested `Must keep`, `Must avoid`, or `Avoid` sublabels, and never emit a separate `Avoid:` field. Do not convert every descriptive fact into a constraint or restate a positive invariant in negative form.

Check every invariant against the Shot timeline. Do not use `始终`, `保持不变`, `只有`, or an equivalent absolute when a required beat changes that property. State the stable interval and the permitted mover, entrant, exit, reveal, or transformation explicitly.

Before adding a negative clause, verify that no Shot requires the physical or diegetic form being restricted. When it does, target only the added overlay, substitution, malformed copy, or other unwanted variant while preserving the required form. Omit negative clauses entirely when no independent high-risk failure is present.
