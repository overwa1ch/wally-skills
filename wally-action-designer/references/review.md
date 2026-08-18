# Returned-Video Review（回片评审）

Use when a generated video returns for acceptance or needs a rerun, targeted edit, or extension. During generation the director body was a cinematography brief and could yield variants; once delivered, it becomes the acceptance baseline. Approved storyboard or director-script authority stays higher if the body itself deviated from it.

## Procedure

Review text-first: ask the user to watch and report observations. Do not inspect frames by default; inspect a named moment only when the user explicitly requests it.

Choose the checklist unit from the body actually delivered:

- Shot blocks present: review Shot by Shot; review each direct Shot-local timecode line on that Shot's local timeline, then check declared cross-shot invariants.
- `Timing/beats` present: review beat by beat, then check the landing.
- `Action` only: review the complete continuous action from initial state through landing.

Accept partial evidence and state what remains unverified. Do not mark an omitted field as a failure. A missing field is a body defect only when the current generation needed that control and the omission made execution ambiguous or contradictory.

## Checks to apply when declared or materially required

1. **Duration and order:** declared duration and beats fit; direct Shot-local timecode lines reset to `0.0s`, stay sequential, and end at the Shot duration; cause precedes response; the landing registers.
2. **Subject and scene:** visible subjects, setting, spatial facts, and frame-zero scene condition match the body; where effect depends on a before-state, the contamination, damage, or disorder type, amount or density, distribution, and location are readable before action begins.
3. **Action fidelity:** the primary process, useful response, and landing occur as written; no unsupported choreography appears.
4. **Continuity:** when declared or required across cuts/states, identity, wardrobe, props, positions, and states remain invariant.
5. **Physics:** when declared, contact, deformation, fluid, cloth, collision, reflection, transformation, or occlusion behaves causally.
6. **Visible text:** every string in `“……”` renders verbatim at its declared moment; no conflicting text appears.
7. **Dialogue and acting:** approved wording, speaker, order, delivery, listener behavior, and lip sync hold where controlled.
8. **Camera, style, light, and color:** only the controls actually declared in these fields or Shots are acceptance criteria; no contradiction or unplanned camera move breaks execution.
9. **Audio:** the declared branch holds—default no BGM with designed ambience/SFX, explicitly requested music, or explicit absolute silence—and the controlled foley, causal triggers, voice acoustics, spatial behavior, and transitions occur as written.
10. **Constraints:** the single consolidated field's positive invariants hold and its specific negative failure modes do not occur.

## Findings and revision

For every material issue, report the execution unit and time when known, the observation, its impact, and the smallest concrete revision.

- Classify it before changing anything:
  - **body defect:** the brief omitted, contradicted, or ambiguously placed control information that this task needed;
  - **generation variance:** the body was sufficient, but this render missed or drifted from it;
  - **platform limit:** the requested behavior exceeds a known execution capability or cannot be repaired reliably through prompt wording.
- For generation variance, prefer another variant or rerun before rewriting a sufficient body. Do not overfit the prompt to one miss.
- For a targeted edit, change exactly one owning field or execution unit per iteration when possible, state `same shot` or the equivalent preservation intent, and repeat every invariant needed to keep unaffected content stable.
- For an extension, describe only the next beat. Preserve the entering motion, camera direction, subject trajectory, lighting logic, and sound continuity; use only the invariants needed to prevent drift rather than freezing the continuation.
- Add `Continuity`, `Physics`, or `Constraints` only when the observed problem proves that information is independently needed.
- Tighten the negative clause inside `Constraints` with a recurring high-risk failure, not a cumulative history or a separate `Avoid` field.
- Preserve every unaffected field, beat, Shot, dialogue line, timing, and outcome.
- If the result is close, let the user approve it as the new baseline and describe only the remaining tweak in the next edit.
- If the result is chaotic or repeatedly misfires, simplify in this order: freeze or reduce camera motion, reduce the action, clear the background; then restore one required control at a time.
- Report a platform limit plainly instead of accumulating contradictory detail or redesigning locked story and shot authority.

## Verdict

Return one verdict: **usable**, **usable with minor revisions**, or **revise and return**. Escalate story or shot-structure conflicts to the shot-authority owner instead of redesigning them here.
