# Continuity Validation Rules

Use after drafting a `processed director script`, before delivery.

## Goal

Check whether the director script can be shot and cut as a continuous scene.
Focus on camera movement, character blocking, eyeline, screen direction, prop / animal position, shot order, and whether each shot earns its place.
Validation may track off-frame facts. Keep those facts in the checklist or continuity baseline until a shot can show them.

Continuity validation is mandatory, but it is internal by default.
The artifact should include a full validation table only when the user asks for validation evidence.
If evidence is requested, give a compact summary or a short table outside the director script body.

## Internal Checklist

Use this checklist in reasoning, validation records, or requested evidence:

```text
结论：PASS / REVISE

空间与屏幕方向基准：
- 角色初始位置：
- 角色结束位置：
- 主要视线 / 运动方向：
- 关键遮挡关系：
- 动作 / 道具承接：

逐镜检查：
| 时间段 | 拍摄手法连续性 | 人物调度 | 道具 / 声音承接 | 分镜合理性 | 判断 |
| --- | --- | --- | --- | --- | --- |

阻塞问题：
- 无 / ...
```

## Checks

- Camera continuity: screen direction, entrance / exit direction, eyeline match, shot-size progression, motivated camera movement, and whether the move can connect to the previous shot.
- Scene authority: every source scene boundary, exact heading, and position remains unchanged; scene transitions preserve the supplied order.
- Shooting-method structure: each shot orders `拍摄角度 + 景别（取景框） + 机位 + [按需：焦段 / 光学效果] + 运镜`; angle, visible crop, and physical camera position remain distinct.
- Camera-movement completeness: every shot defines start, physical path, relation to the subject, and landing. An undecided move uses a slow push-in.
- Fixed-camera exception: `固定镜头` has an explicit user lock or a stated narrative purpose for stillness.
- Blocking continuity: character position, distance, facing direction, body orientation, line of sight, prop contact, animal / group position, and whether every movement has visible cause and result.
- Shot logic: each shot has a clear visible job; empty shots, inserts, and transitions connect action, prop state, relationship, or aftermath; durations fit visible action; reveals and reversals occur in the right order.
- Frame visibility: every visual noun in the shot fits the stated crop; the shot task adds no unshown body part, wardrobe, prop, background, reflection, or source.

## Blocking Problems

Revise the director script before delivery when any of these appear:

- A character jumps position, facing direction, or side of frame without visible movement or transition.
- A shot lacks a readable action, object state, sound state, or task.
- A shot's landed beat cannot plausibly lead into the next shot.
- Eyeline direction does not match the other character, object, animal, or threat position.
- Screen direction changes in a way that confuses who approaches, retreats, blocks, watches, or is watched.
- A key prop, animal, door, vehicle, or hand contact changes position without cause.
- Camera movement makes the character action harder to read.
- Camera movement is written only as `跟随`、`动态运镜`、`镜头运动`、`推进感` or `轻微晃动`, without a physical path and landing.
- Camera movement and subject movement are merged into one ambiguous action.
- Shooting angle, visible crop, and camera position are merged or written out of order, making the frame or placement ambiguous.
- A shot defaults to `固定镜头` without an explicit user lock or a narrative reason for stillness.
- An empty shot or insert interrupts the main action without establishing space, delaying a reveal, transferring attention, or landing aftermath.
- A shot is too short for the described movement, reaction, or blocking change.
- The sequence order weakens the intended threat, protection, reversal, reveal, or payoff.
- A close-up or insert lists off-frame full-body, wardrobe, distant-prop, background, reflection, or source detail.
- An off-frame continuity fact is repeated inside a shot and could cause the image model to draw it.

## Revision Rule

Keep fixes minimal.
Preserve the source story and its exact source scene boundaries, headings, and order. Never split, merge, rename, normalize, or renumber a scene.
Adjust shot order, shot size, camera movement, blocking, transition, duration, or visible action wording only as needed.
Move off-frame continuity facts into validation instead of repeating them in shot blocks.

Apply revisions directly in the director script before delivery. Keep editing-history language out of the artifact. Put validation notes in validation records, logs, or chat summaries.
