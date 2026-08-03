# Director Design Craft

How to design the drama, visible specificity, motion, interaction, dialogue, timing, and sound of one executable AI-video prompt. Apply only the sections the current task needs. This file owns platform-independent generation craft; `contract.md` owns output syntax, and `review.md` owns returned-video iteration.

## 1. Treat The Body As A Cinematography Brief

- Treat the generation body as a cinematography brief, not a guarantee of identical pixels or motion. The same sufficient body can yield different variants; generation variance is normal and belongs to returned-video review.
- Use the shortest prompt that still carries every independent control. A shorter body leaves more creative freedom; a longer body adds control but also more opportunities for competing instructions.
- When clip boundaries are genuinely open and precision matters, prefer shorter executable units. Never change an approved duration, split an authoritative Shot, or discard required action merely to shorten a clip.
- Start with the main subject, main action, camera behavior, and indispensable invariants. Add another control only when the material requires it or a returned result proves the omission matters.

## 2. Build The Dramatic Chain

Resolve these questions internally before writing cues:

1. What does each performer want in the current beat?
2. What blocks that action now?
3. What is the playable tactic?
4. What triggers the first visible change?
5. Who initiates, who responds, and what relationship state lands at the end?

Keep the chain continuous across the whole requested scope. Each unit needs only its current causal link; do not repeat the full analysis in every line.

## 3. Choose And Keep The Execution Unit Executable

- Use one top-level `Action` for a continuous process, add top-level `Timing/beats` only when one single shot or continuous take needs ordered timing, and use Shot blocks only for multiple or authoritative shots. Inside each Shot block, write direct local timecode lines; those lines are part of the Shot carrier and never create a second top-level carrier. Do not turn a single continuous take into `Shot 1` merely to satisfy a format.
- Keep one grammatically clear main subject and one main action per execution unit. Treat secondary people, props, background activity, and routine motion as subordinate unless they change the story outcome.
- Preserve every approved action, but identify one primary action and one dominant camera behavior for each execution unit unless the shot authority explicitly locks more. Keep supplied continuous background processes low-weight instead of turning them into additional choreography.
- Use plain visible nouns and verbs. Name relevant materials such as metal, fabric, glass, leather, or clay when they affect appearance or physics. State only the path, direction, timing, or landing needed to make the approved action unambiguous; do not infer gait mechanics, force, weight transfer, micro-gestures, or secondary body reactions.
- Use direct local timecode lines such as `0-2s:`, `2-4s:`, and `4-6s:` when timing matters inside a Shot. Never prefix them with `beat N` or wrap them in parentheses. Always place `s` immediately before the ASCII colon.
- Keep actions sequential, not simultaneous.
- For a 4-second clip, limit the action to one or two beats. For other durations, use the fewest source-supported beats that make the sequence executable; continuous background state does not create another beat.
- Describe actions as counts or steps when possible and supported by the supplied material or exact synchronization. Never invent a count to make ordinary movement sound more precise.
- Keep every multi-Shot block distinct. Give each Shot one camera setup, one action, and one lighting recipe only when lighting is materially controlled. Treat each Shot as a creative unit that can later be edited or stitched.
- Build each Shot setup from only the controls that materially disambiguate frame zero. Select them in this order when needed: viewpoint and axis relationship; shot size, lens, angle, and camera position; foreground framing or occlusion; focus owner and plausible depth of field; foreground-subject-background layers and initial positions. Describe the axis through visible subject relationships rather than inventing compass directions or opaque position labels.
- Let the local timeline own every change after frame zero. Order the useful controls as trigger, camera response, subject path or contact, relationship landing, and exact dialogue or sound. Omit any stage that does not change execution.
- Fit the action, camera response, contact, settling, dialogue, and listener registration inside the Shot duration. When they cannot fit sequentially, simplify an unlocked camera response or report the locked-duration conflict; do not compress everything into simultaneous motion.

## 4. Specify Style, Camera, Light, And Continuity Visibly

- Name the visible subject, relevant materials, setting, time of day, and atmosphere only when supplied or materially controlled. Replace vague praise with renderable nouns and verbs: `湿沥青、斑马线、霓虹倒映在积水中` carries more control than `漂亮的夜街`.
- Put a decisive style cue in the early `Style/format` field. Express it as visible medium, capture texture, period treatment, filter character, or grade instead of abstract prestige language.

### Build Camera From Conditional Control Dimensions

Compose camera direction from only the dimensions that add independent control:

- **Capture physics**: frame cadence and shutter-motion rendering. For explicitly filmic live action with open capture settings, `24fps，180°快门运动模糊` is an available baseline, not a universal requirement. Omit or replace it for source-matched footage, phone-native UGC, tutorials, sports, high-speed action, slow motion, animation, UI capture, or any locked setting.
- **Optical behavior**: lens character, focus falloff, and depth of field. `自然光学景深` means physically plausible, shot-appropriate focus behavior; it never means every Shot must be shallow. Longer-lens close-ups such as 85mm+ can favor isolation, 24–35mm wide views can preserve context, and group or spatial-establishing Shots may need deeper focus.
- **Stability and capture texture**: distinguish a truly locked-off camera from stabilized or handheld capture. `稳定手持` keeps composition controlled while allowing subtle irregular breathing drift or micro-correction; it is not rhythmic shaking. Use looser handheld motion only when the supplied style requires it.
- **Movement motivation**: use one dominant move per execution unit—locked-off, dolly, orbit, lateral slide, pan, tilt, track, or restrained handheld drift. Start camera movement because of a performer, prop, gaze, sound, or spatial reveal; describe its start, path, subject relation, and landing when those facts matter.
- **Edit grammar**: when narrative edit authority is open, let cuts follow changes in relationship, tactic, pressure, information, or focal ownership rather than cutting mechanically on every line. In shot-reverse-shot, let framing distance, emphasis, or reaction value progress with the beat instead of repeating equal-status reaction coverage. Preserve every approved cut and camera decision when shot authority is locked.

For example, when all five dimensions genuinely apply: `Camera: 真实电影摄影，24fps，180°快门运动模糊，自然光学景深；稳定手持，只有轻微不规则呼吸漂移。镜头运动由人物动作、视线与声音触发，正反打随关系压力递进景别。` Shorten or omit any clause that the current task does not control.

- Prefer straight-on, stable framing for UI or exact on-screen text when shot authority leaves the camera open. Never replace a locked camera decision merely to follow this heuristic.
- When lighting matters, state its quality, motivated source, and direction. When color is independently controlled, name three to five palette anchors. Reuse the same lighting logic across visibly continuous Shots.
- For a strict filmic look or continuity-critical task, add only the independently controlled detail among format/look, lens or filter, grade or palette, lighting direction, texture, and sound. More detail is not automatically more control.
- Establish one canonical core description for each continuing character or product and reuse that exact wording across Shots. Do not mix competing traits that can shift identity, silhouette, material, or pose. Use a supplied human-readable identity name verbatim when it helps continuity, without emitting bindings or handles.
- Treat all camera, lens, light, palette, and style advice as conditional craft. Approved storyboard or director-script authority always wins.

## 5. Stage Interaction As Relationship Change

For two or more performers, establish only the spatial facts that affect the interaction:

- initial relation: distance, gaze, orientation, visibility, occlusion, access, or route;
- trigger: sound, look, line, prop, approach, interruption, or unexpected movement;
- initiative: one performer acts with a readable tactic;
- response: another performer changes attention, position, action, or refusal;
- landing: someone changes another person's route, distance, control, access, or emotional cover.

Use observation, concealment, approach, pursuit, withdrawal, interception, yielding, blocking, passing, shared prop contact, or deliberate stillness when supported by the material. Avoid stand-and-deliver dialogue when the relationship should be changing.

In group scenes, give the primary action full clarity and compress the group into one shared low-weight response unless an individual response changes the story.

## 6. Execute Approved Dialogue And Visible Text For Action

- Accept only wording explicitly locked by the user or approved in the supplied screenplay. Preserve wording, speaker, and order exactly.
- Check that each line fits the available duration with room for breath, pause, interruption, and listener response.
- Attach dialogue to an action, withheld action, or change of tactic. Do not decorate every line with a gesture.
- Give the speaker at most one action or state that changes delivery.
- Give the listener at most the first useful response unless later reactions create a new beat.
- Control lip movement only when sync, deliberate silence, closed-mouth listening, overlap, or off-screen delivery matters.
- When wording is missing, provisional, contradictory, or needs invention/revision, report that boundary and route the wording decision to `wally-screenplay-writer`; never propose alternatives here.
- Preserve supported voiceover, off-screen speech, phone/radio speech, overlap, and silence when the task includes them; report technical conflicts instead of silently converting the mode.
- Keep exact visible text short when the material allows it. Preserve its exact wording and specify its screen, surface, or frame position; use a stable, legible camera state when authority leaves that decision open.
- Keep dialogue in its dedicated field or owning timecode line, label speakers consistently, and use only the number of short lines that can fit with action, breath, and response.

## 7. Use Timing Without False Precision

When reliable timing exists and materially affects execution:

- keep ranges ordered, continuous when the task requires continuity, and non-overlapping unless overlap is intentional;
- keep every Shot header on the full-video timeline, but reset its direct Shot-local timecode lines to `0.0s`; end the final local line at that Shot's duration and never mix global timestamps into the local sequence;
- use whole seconds or at most one decimal when needed, with local lines such as `0-2s:`, `2-4s:`, or `1.1-2.5s:`; do not carry frame or millisecond precision into the director body unless the user explicitly requires it;
- budget spoken words, breath, action preparation, contact, reaction, and settling time;
- place the cause before the response and allow the response to register;
- shorten the action or flag a duration conflict when the beat cannot fit.

When exact timing is unnecessary, keep the order inside `Action` with relative timing such as `先`, `随即`, `停半拍`, `被打断后`, and `落稳后`. A timecoded body requires a user-supplied or explicitly approved target duration; ask for it instead of inventing seconds.

## 8. Design A Complete Adaptive Sound State

- When the user and locked materials do not request music, default to `无BGM` and build a complete non-musical sound bed: ambience, room tone, routine foley, action-triggered sound, spatial acoustics, transitions, and meaningful silence.
- When the user or locked material explicitly contains music, describe that music accurately and omit `无BGM`; include only the supplied or materially controlled character, rhythm, entry, transition, and level relationship.
- When the user requires absolute silence, preserve absolute silence and add no ambience, foley, dialogue, voiceover, or music. A brief meaningful silence inside an otherwise audible scene remains a designed sound event.

Use sound when it changes action timing, attention, space, or relationship:

- an approaching sound triggers a look or concealment;
- a contact sound confirms impact, placement, release, or breakage;
- a sound stops with the performer and makes the stop legible;
- a door, object, device, or voice reveals new information;
- a brief sound accent lands a relationship or emotional turn.

Keep the shared sound state concise; move a sound into its beat or Shot only when the exact trigger changes action or editing.

## 9. Anchor Frame Zero And Assign Reference Roles

- Treat a supplied input image as the visible state already true at `0.0s`: it can lock composition, identity, product state, and set dressing. Describe only what happens after that frame; do not make `Action` rebuild or restage the image.
- Put frame-zero facts in the applicable global fields or Shot setup. Put every subsequent change, including entry, reveal, movement, transformation, or camera departure, in the owning top-level `Action`, `Timing/beats`, or direct Shot-local timecode line.
- For cleaning, restoration, organization, damage-removal, before/after, or product-efficacy work, make the starting condition renderable before the action: name the dirt, debris, damage, or disorder; its amount or density; its distribution pattern; and the surface, zone, edge, groove, or container where it sits. `脏乱`, `很多灰尘`, or `有碎屑` alone is too vague when the result depends on the starting state. For display or storage Shots, state the clean, empty, or orderly baseline and any intentionally present objects. When shot authority leaves this condition open, choose the smallest visible setup that makes the intended effect legible; do not exaggerate it into an unsupported product claim.
- If a necessary frame-zero anchor is missing, state the required composition, identity, or set-dressing anchor and route it to the static-asset workflow. Do not generate, redesign, or approve the asset inside Action Designer.

Use each supplied reference for the evidence it can reliably carry:

- character images: identity and visible state;
- storyboards or shot material: existing spatial and camera decisions;
- action video: mechanics, weight, rhythm, and contact;
- audio: delivery, cadence, voice continuity, and sound timing;
- scripts and notes: story authority, dialogue, intention, and constraints.

The user may override this allocation. When references conflict, preserve the declared authority and record the unresolved execution risk briefly.

## 10. Compress For Execution

For each chosen execution unit, write:

1. the dominant action;
2. the trigger or first response when it changes execution;
3. the relationship landing when it is not already visible in the action;
4. exact dialogue at the moment it is spoken;
5. the key sound only when it times or lands the beat.

One or two sentences per unit is usually enough. Merge the ending state into the last action instead of adding a repeated summary. Do not add an unlabeled story paragraph beside Action, beats, or Shots.

## 11. Strong/Weak Pairs

- Weak: 她很伤心地站在那里，气氛压抑，情绪拉满。
- Strong: 她背对柜台站定，手指反复摩挲围裙边，听到脚步声呼吸停半拍，没有回头。
- Weak: 镜头炫酷地运动，电影感十足。
- Strong: 机位从柜台端头齐胸高度起，随她的移动向左缓慢横移，在她停步时同步落定，浅景深让背景货架虚化。
- Weak: 上一镜里他刚展开伞，被外露的尖端吓了一跳。
- Strong: 开场承接：伞已完全展开停在前挡附近，外露尖端已经露出，右手已停在尖端旁。

The strong version converts psychology into gaze, breath, posture, and action, and gives camera movement a start, path, motivation, and landing; the weak version stacks judgments the model cannot execute. Entry states follow the same rule: write states the model can render at frame one, not events it must remember — and carry the prior shot's landing only when the two shots are visibly continuous; a fresh setup defines its own frame-one state instead.
