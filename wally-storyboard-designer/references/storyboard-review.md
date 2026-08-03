# Storyboard Review Guide

Use this guide to review a returned board, a draft storyboard, or an existing shot sequence against the materials and objective the user provides.

## Text-based review protocol

The reviewing agent reviews text, not pixels. The user views the returned boards and reports observations in text; the agent checks those observations against the upstream design documents, classifies each finding, routes it, and delivers the verdict. Do not open or visually inspect board images by default — agent image review is slow and adds little over the user's eyes. To keep the user's viewing fast, derive a per-panel checklist from the design (one line per panel: the single thing to verify) and let the user answer it in text. Open an image only when the user explicitly asks for a second look at a named panel.

## Set the evidence base

- Review against the current user request, supplied story facts, visible reference constraints, and any accepted storyboard decisions.
- Accept incomplete, mixed, or nonstandard materials. Identify what can and cannot be verified from them.
- Distinguish a confirmed mismatch from an open question. Do not convert missing context into a false error.

## Review in priority order

### 1. Story coverage

- Confirm that the board stays inside the requested scope.
- Confirm the entry state, key process or turn, required visible facts, and ending state.
- Flag invented beats, missing consequences, premature future action, and panels that serve no story function.

### 2. Shot order and continuity

- Check that adjacent panels create a legible cause-and-effect sequence.
- Check screen direction, eyelines, entrances, exits, object position, subject count, and spatial orientation.
- Require a reorientation shot when an axis or geography change would otherwise read as an error.

### 3. Action readability

- Confirm who acts, what moves, what receives the action, and what changes.
- Confirm that key actions show a readable start, decisive change, and result.
- Flag hidden gestures, ambiguous arrows, overloaded panels, duplicate-looking subjects, and missing intermediate states.

### 4. Shot size and camera movement

- Confirm that each shot size supports geography, interaction, information, or reaction.
- Confirm that shot directions follow `拍摄角度 + 景别（取景框） + 机位 + [按需：焦段 / 光学效果] + 运镜`, with angle, visible crop, and physical camera position kept distinct.
- Confirm that every panel states a complete camera move; an undecided move defaults to a slow push-in.
- Accept `固定` only when the user locks it or the panel states a narrative purpose for stillness.
- For a moving camera, confirm the start, physical path, relation to the subject, and landing frame.
- Confirm that subject movement and camera movement are written separately.
- Flag movements that conflict with subject motion, obscure the key action, repeat without value, or substitute motion for missing coverage.
- Flag `跟随`、`动态运镜`、`镜头运动`、`推进感` or `轻微晃动` when they appear without a physical path and landing.

### 5. Visual rhythm and density

- Check that each panel has one primary visual job.
- Check that important processes receive enough panels and predictable repetition is compressed.
- Flag repeated room views, decorative angles, tiny text, dense diagrams, rigid UI-like layouts, or arrows that overpower the image.

### 6. Style compliance

When the canonical storyboard style is requested, read `storyboard-style-contract.md` and check it verbatim. In particular, flag:

- readable facial, clothing, hair, anatomy, texture, shading, or polished rendering detail;
- manga cleanup, concept art, poster art, film-still treatment, environment rendering, or character-sheet presentation;
- missing loose black lines, red camera viewfinder boxes, required arrows, or concise Chinese notes;
- missing or altered `景别：...｜运镜：...｜人物动作：...` notes;
- an aspect ratio that conflicts with the requested or canonical format.

Apply style checks only when that style is part of the current task.

## Classify each finding before revising

A board is a test of the shot design. Sort every material issue into one of three:

1. **Board-execution failure:** the board misdrew the supplied design — wrong order, missing action, broken style, unreadable arrows. The design stands; request a corrected redraw.
2. **Shot-design failure:** the board faithfully rendered the design and the result still fails — the action cannot read in this shot size, the composition hides the story point, the spatial relation contradicts itself, the rhythm has no beat. The test succeeded by exposing it: route the finding to the shot design (director script or storyboard design) for revision before any redraw.
3. **Undecidable from this board:** the panel is too ambiguous to attribute. Request a targeted redraw of only that panel to isolate the cause.

## Write actionable findings

For every material issue, state:

1. **Location:** panel, shot, page, or visible region.
2. **Finding:** the observable problem.
3. **Impact:** what becomes unclear, discontinuous, off-story, or stylistically inconsistent.
4. **Revision:** the smallest concrete change that fixes it.

Group repeated symptoms under one root cause. Preserve panels and decisions that already work.

## Give the verdict

Use one verdict:

- **Usable:** no material storyboard issue remains.
- **Usable with minor revisions:** the sequence works and named local corrections do not change its structure.
- **Revise and return:** story coverage, continuity, action clarity, camera logic, or required style prevents reliable use.

Verdicts judge the shot design under test as much as the drawing: when shot-design failures dominate, the primary deliverable is the design-revision list — the board has done its job by exposing them.

List unverifiable items as open issues. Do not use approval gates, route selection, asset production, performance design, or final-prompt readiness as storyboard-review criteria.
