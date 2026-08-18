# Director Script Output Contract

Use when writing a `processed director script`.

## Document Structure

```text
# Processed Director Script

版本：
模式：source-preserving / visual-optimized
来源：
状态：DIRECTOR_SCRIPT_READY

## 作品定义
Copy the latest explicit or approved work-definition block from the source screenplay or user brief.

## 完整剧本 / 来源
Keep the supplied screenplay or excerpt under its original scene headings and in its original scene order.

## 导演脚本
<原始场景标题，逐字保留>

分镜01｜分镜时间：00:00-00:03｜景别/镜头类型：近景 / 道具空镜
...

<下一个原始场景标题，逐字保留>

分镜02｜分镜时间：00:03-00:06｜景别/镜头类型：中景
...
```

Use provided source as authority. A generation request requires explicit source-scene boundaries; when they are absent, stop and route scene formation to `wally-screenplay-writer`. Preserve every source scene boundary, heading, and position exactly; never split, merge, rename, normalize, or renumber scenes. For locked briefs, test prompts, or excerpts, cite them directly and keep the source scenes plus director script complete. Run continuity validation internally before delivery; show a compact PASS line or table only when requested.

The work definition is required metadata for a complete director script. Copy it without reinterpretation and keep it outside source scene text and individual shot blocks. If the distinction between advertisement, narrative film, documentary, MV/visual piece, or episodic content would materially change the shot design and the source does not decide it, report the missing definition instead of guessing.

Core principle: if unsure, write less. Use only visible, shootable anchors that control the frame, action, timing, sound, continuity, or handoff. Do not fill uncertainty with invented props, extra blocking, mood words, or explanatory coverage.

## Frame Visibility And Prompt Hygiene

Treat every shot block as a crop-bounded visual instruction.

- Name only the subjects, body parts, props, actions, and changes visible inside that shot's frame.
- Let shot size control the allowed detail. A close-up or insert contains its focal subject and the minimum visible contact needed for the action; it does not inherit full-body, wardrobe, distant-prop, or background details from the scene.
- Give each shot one primary visual job. Add a second element only when their visible contact, cause, obstruction, or result is the shot.
- Let the previous shot establish an off-frame cause. Do not repeat the unseen source inside the reaction shot.
- If an off-frame sound continues, write `沿用` or a source-neutral transition in `声音` instead of naming an unseen object.
- Describe the visible viewpoint without inventing equipment that need not appear. Example: `自拍角度，手臂伸向镜头。` Name a phone only when the phone is visible.
- Keep off-frame layout, prop position, and body-state continuity in internal validation or a separate continuity baseline. Bring an anchor into a shot block only when the frame shows it.
- Write the positive target frame. Do not add negative inventories of excluded body parts, props, clothing, or background.

Cut any detail whose removal does not change what should be drawn, the visible action, or continuity inside the frame.

Compact examples:

```text
正面贴地特写，只拍右脚。右脚快速抬落。
水杯与嘴部特写。喝一小口。
自拍角度，手臂伸向镜头。
```

## Shooting Method Grammar

Write `拍摄手法` as one compact semicolon-separated sentence in this order:

`拍摄角度 + 景别（取景框） + 机位 + [按需：焦段 / 光学效果] + 运镜`

- `拍摄角度`: state the lens orientation that changes the view, such as 正面、侧面、斜侧、背面、平视、俯拍 or 仰拍.
- `景别（取景框）`: state the shot size, then the positive visible boundary, such as `脸部近景特写，仅拍脸部`.
- `机位`: state the camera's physical position, height, distance, or side relative to the subject. Keep it separate from lens orientation. Translate an off-frame object used only as a height reference into an executable height or position instead of naming that object.
- `焦段 / 光学效果`: add only when focal length, distortion, fisheye, macro, or another optical choice materially controls the image.
- `运镜`: state the start, physical path, relation to the subject, and landing under the Camera Movement Contract.

Keep this order while using only the precision that changes the image. Do not invent measurements or add a slot merely to make the sentence longer.

Compact example:

```text
超低角度仰拍；脸部近景特写，仅拍脸部；摄影机位于人物正前方，距地约75厘米；从脸部近景缓慢推近至更紧的脸部特写，脸部保持画面中央。
```

## Camera Movement Contract

Define camera movement in every shot.

- For a moving camera, write one physical path in this order: `起点 + movement verb / path + relation to subject + landing`.
- When no stronger move is motivated, use a slow push-in: state the starting shot size, push slowly toward the focal subject, and land on a slightly tighter framing.
- Use `固定镜头` only when the user explicitly locks the camera or when stillness itself is the narrative point, such as a deliberate before/after match, surveillance view, freeze, or deadpan hold. State that purpose in `镜头任务 / 情绪落点`.
- Use exact movement verbs: `推近`、`后退`、`横移`、`升`、`降`、`摇`、`俯仰`、`环绕`、`跟拍`、`手持`.
- Separate camera movement from subject movement. State both when both move.
- For tracking, state whether the camera is in front of, behind, beside, or parallel to the subject, and whether distance changes.
- For pan or tilt, state the starting direction or visible anchor and the final visible anchor.
- For push-in, pull-back, rise, descend, or lateral movement, state the first framing and final framing or subject scale.
- For handheld, state the movement baseline and intensity, then state where the frame settles or cuts.
- Keep the movement path inside the visible crop and use only visible anchors.
- Let subject motion remain independent from the default slow push. Keep the push small enough that the subject action stays readable.

Do not use `镜头跟随`、`动态运镜`、`镜头运动`、`推进感` or `轻微晃动` as complete camera instructions.

Compact examples:

```text
镜头从人物中景缓慢推近至略紧的中近景，人物保持画面中央。
镜头从桌面左端开始，沿桌边向右横移，与纸带保持同速，落在出纸口。
摄影机位于双脚正前方，随双脚前进等距后退，落在纸带横过路线的位置。
固定镜头；保持启用前后完全相同的对照构图。
```

## Director Shot Fields

Group the `导演脚本` section by the screenplay's original source scenes. Copy every scene heading verbatim and preserve source order. One scene may contain multiple action chains, multiple dramatic beats, multiple storyboard pages, and any number of timecoded shot blocks. Use this field order:

```text
<原始场景标题，逐字保留>

分镜01｜分镜时间：00:00-00:03｜景别/镜头类型：近景 / 道具空镜
拍摄手法：
环境变化：
人物动作：
声音：
镜头任务 / 情绪落点：
```

## Field Rules

- Scene heading: copy the exact original source scene heading. Never infer, normalize, rename, split, merge, or renumber it.
- Shot heading: use `分镜XX｜分镜时间：MM:SS-MM:SS｜景别/镜头类型：...` with cumulative time. Put shot size first: 全景、中景、近景、特写. Add shot type only when known, such as 道具空镜、状态空镜、插入. Omit shot type when unclear. Keep camera movement out of this heading.
- `拍摄手法`: write one efficient sentence in the fixed Shooting Method Grammar order: `拍摄角度 + 景别（取景框） + 机位 + [按需：焦段 / 光学效果] + 运镜`. Keep angle, crop, and camera position distinct. Add another spatial layer only when it is visible and controls blocking, focus, or continuity. A close-up or insert does not import full-body, wardrobe, remote-prop, or background detail. Define the movement start, physical path, relation to the subject, and landing. Default to a slow push from the stated shot size to a slightly tighter framing. Use `固定镜头` only for a locked or intentionally still shot. Separate subject movement and camera movement.
- `环境变化`: write only the visible place, light, prop, or object change. Use `无` when nothing changes inside the crop.
- `人物动作`: write only visible actions of the body parts inside the crop. Do not explain them with off-frame causes.
- `声音`: write the visible source's sound, dialogue, silence, or transition. Use `沿用` when an off-frame source continues and naming it could expand the frame.
- `镜头任务 / 情绪落点`: state the shot's visible job or landed beat without introducing new visual nouns.

## Output Hygiene

- Write the current target state directly.
- Apply fixes in shot text; keep revision notes in chat, validation logs, or separate records.
- Put safety boundaries in a separate note when needed.
- Rewrite absent facts as present visible state, for example: `硬币留在收费单旁，医生手停在病历上方。`
- Use short physical nouns and active verbs. Let action, timing, sound, and object state carry emotion.
- Keep continuity notes outside the shot block when the frame cannot show them.

## Quality Checks

- First block usually locates place/time/relationship.
- Every block has readable action, prop/object state, sound state, focus change, camera movement, blocking, or aftermath.
- Every `拍摄手法` follows `拍摄角度 + 景别（取景框） + 机位 + [按需：焦段 / 光学效果] + 运镜`; angle, crop, and camera position do not collapse into one ambiguous phrase.
- Every shot contains a complete camera path with start, movement, subject relation, and landing.
- An undecided camera move defaults to a slow push from the current shot size to a slightly tighter framing.
- `固定镜头` appears only with an explicit user lock or a stated narrative purpose for stillness.
- Camera movement and subject movement are written as separate actions.
- No shot uses `跟随`、`动态运镜`、`镜头运动` or `推进感` as a complete instruction.
- Empty shots carry place, time, relationship, prop state, transition, or aftermath.
- Every visual noun in `拍摄手法`、`环境变化` and `人物动作` fits inside the stated crop.
- A close-up or insert contains no unshown full-body, wardrobe, remote prop, background, reflection, or off-frame source detail.
- `镜头任务 / 情绪落点` introduces no object or body part absent from the visible fields.
- Replace generic quality adjectives with visible evidence.
- In `拍摄手法`, keep only anchors that control the shot. Default spatial description is foreground only; do not add `中景是...` or `背景是...` unless requested.
- When camera movement is present, it should answer five checks compactly: why it moves, where it starts, how it travels, how the subject relates to the lens, and where it lands.
- Source scenes remain intact under their original headings and order; analysis belongs in reasoning or `导演脚本`.
- The document carries the latest source `作品定义`; work type and audiovisual style are not collapsed into one label.
- Keep `画面变化`, standalone `构图 / 空间层次` fields, separate wardrobe/prop/mood fields, storyboard panels, `Bxx`, asset IDs, and final video prompts out unless explicitly requested.
