# Director Design Craft

How to design the drama, visible specificity, motion, interaction, dialogue, timing, and sound of one executable AI-video prompt. Apply only the sections the current task needs. This file owns platform-independent generation craft; `contract.md` owns output syntax, and `review.md` owns returned-video iteration.

## 1. Treat The Body As A Cinematography Brief

- Treat the generation body as a cinematography brief. The same sufficient body can yield different variants; generation variance belongs to returned-video review.
- When clip boundaries are open and precision matters, prefer shorter executable units while preserving durations, cuts, and actions explicitly specified by the user.
- Start with the main subject, main action, camera behavior, and indispensable invariants. Add another control only when the material requires it or a returned result proves the omission matters.

## 2. Build The Dramatic Chain

Resolve these questions internally before writing cues:

1. What does each performer want in the current beat?
2. What blocks that action now?
3. What is the playable tactic?
4. What triggers the first visible change?
5. Who initiates, who responds, and what visible state lands at the end?

Keep the chain continuous across the whole requested scope. Write each unit's current causal link.

## 3. Choose And Keep The Execution Unit Executable

- Keep one grammatically clear main subject and one main action per execution unit. Treat secondary people, props, background activity, and routine motion as subordinate unless they change the story outcome.
- Identify the primary action and dominant camera behavior for each execution unit, preserving the actions and camera behavior explicitly specified by the user. Keep supplied continuous background processes low-weight.
- Use plain visible nouns and verbs. Name materials when they affect appearance or physics; specify path, direction, timing, and landing where they clarify the action.
- Divide beats at meaningful changes in action or response, according to the available duration.
- Use counts or steps when supplied by the material or needed for synchronization.

## 4. Specify Style, Camera, And Light Visibly

- Describe the visible subject, relevant materials, setting, time of day, and atmosphere with concrete nouns and verbs, using the supplied facts and the choices that materially control the result.

### Choose Camera Treatment For The Scene

- Decide what the viewer needs to see first: a face, both performers, a prop detail, or their spatial relationship. Set focus and background legibility around that need.
- Choose texture, color response, filtration, and highlight treatment for the scene's light, skin, materials, and atmosphere. Judge focal length and aperture together with capture format, working distance, and the depth that must remain readable; use the parameter-selection rule in `contract.md`.
- Match frame cadence and shutter-motion rendering to the medium and action. Distinguish a locked-off camera from stabilized or handheld capture; `稳定手持` keeps composition controlled while allowing subtle irregular drift or micro-correction.
- Motivate camera movement through performer action, gaze, sound, spatial reveal, or a change in relationship or attention. Match its speed, amplitude, and perspective change to the beat's emotional intensity. Describe the start, path, subject relation, and landing when those facts matter. Preserve the user's explicit movement decisions.
- Let cuts follow changes in relationship, tactic, pressure, information, or focal ownership. For a J-cut or L-cut, identify which sound crosses the cut and what the viewer sees while hearing it; use the speaker's delivery and listener's response to determine the cut point.

- Prefer straight-on, stable framing for UI or exact on-screen text when the user leaves camera choices open.
- When lighting matters, state its quality, motivated source, and direction. When color is independently controlled, name three to five palette anchors. Reuse the same lighting logic across visibly continuous Shots.
- For a strict filmic look or continuity-critical task, add only the independently controlled detail among format/look, lens or filter, grade or palette, lighting direction, texture, and sound. More detail is not automatically more control.

## 5. Stage Interaction As Relationship Change

For two or more performers, establish only the spatial facts that affect the interaction:

- initial relation: distance, gaze, orientation, visibility, occlusion, access, or route;
- trigger: sound, look, line, prop, approach, interruption, or unexpected movement;
- initiative: one performer acts with a readable tactic;
- response: another performer changes attention, position, action, or refusal;
- landing: someone changes another person's route, distance, control, access, or visible response.

Use observation, concealment, approach, pursuit, withdrawal, interception, yielding, blocking, passing, shared prop contact, or deliberate stillness when supported by the material.

In group scenes, give the primary action full clarity and compress the group into one shared low-weight response unless an individual response changes the story.

## 6. Execute Approved Dialogue And Visible Text For Action

- Check that each line fits the available duration with room for breath, pause, interruption, and listener response.
- Attach dialogue to an action, withheld action, or change of tactic. Specify the speaker's delivery and the listener's response where they clarify the interaction.
- Control lip movement only when sync, deliberate silence, closed-mouth listening, overlap, or off-screen delivery matters.
- Preserve supported voiceover, off-screen speech, phone/radio speech, overlap, and silence when the task includes them; report technical conflicts instead of silently converting the mode.
- Keep exact visible text short when the material allows it. Preserve its exact wording and specify its screen, surface, or frame position; use a stable, legible camera state when authority leaves that decision open.

## 7. Use Timing Without False Precision

When reliable timing exists and materially affects execution:

- keep ranges ordered, continuous when the task requires continuity, and non-overlapping unless overlap is intentional;
- budget spoken words, breath, action preparation, contact, reaction, and settling time;
- place the cause before the response and allow the response to register;
- shorten the action or flag a duration conflict when the beat cannot fit.

When exact timing is unnecessary, describe the order and pauses inside `Action` with relative timing.

## 8. Use Sound To Shape The Action

Use sound when it changes action timing, attention, space, or relationship:

- an approaching sound triggers a look or concealment;
- a contact sound confirms impact, placement, release, or breakage;
- a sound stops with the performer and makes the stop legible;
- a door, object, device, or voice reveals new information;
- a brief sound accent lands a relationship or emotional turn.

Keep the shared sound state concise; move a sound into its beat or Shot only when the exact trigger changes action or editing.

## 9. Read Initial Conditions And References

When the result depends on a visible before-state, establish the relevant physical condition, extent, and location before the action. Preserve supplied conditions; develop open details only to the extent needed to make the intended change readable.

Use each supplied reference for the evidence it can reliably carry:

- character images: identity and visible state;
- scene and prop images: environment, spatial features, and object appearance;
- action video: mechanics, weight, rhythm, and contact;
- audio: delivery, cadence, voice continuity, and sound timing;
- scripts and notes: story authority, dialogue, intention, and constraints.

The user may override this allocation. When references conflict, preserve the declared reference roles and record the unresolved execution risk briefly.
