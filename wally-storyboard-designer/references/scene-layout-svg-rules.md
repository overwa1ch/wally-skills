# Scene Layout SVG Rules

Use whenever the user requests spatial planning from supplied material with enough spatial facts. A complete, locked, or approved screenplay is not required.

## Purpose

Create one simple top-down spatial check per supplied source scene.

## Input Behavior

- Create one SVG per supplied scene immediately. Do not ask whether the user wants SVGs and do not require another storyboard-domain product first.
- Require explicit source-scene boundaries. If they are absent, stop and route scene formation to `wally-screenplay-writer`; never infer, split, merge, or number scenes here.
- If the supplied material lacks the spatial facts needed for the requested SVG, name only the missing facts and stop. Do not produce a screenplay, director script, storyboard, or other upstream product uninvited.

## Output

Create local `.svg` files, one per scene, with clear names such as:

```text
<project-or-title>-scene-01-layout.svg
<project-or-title>-scene-02-layout.svg
```

If the scene count is small and the user asks for one file, a single multi-panel SVG is acceptable, but default to one SVG per scene.
Create multiple layouts for one source scene only when the user explicitly requests them; do not create new scene units from internal spatial changes.

## Drawing Rules

Use simple geometric shapes only:

- Room or location boundary.
- Major doors, windows, entrances, exits, or partitions.
- Main furniture or large spatial anchors.
- Main character positions at the scene's starting state.
- Scene label and short labels for characters / key spatial anchors.

Default to static layout only.

Keep out:

- movement arrows or blocking paths unless requested
- camera positions, camera-side zones, focal lengths, shot numbers, coverage diagrams, frame boundaries
- storyboard panels, `Bxx`, standalone video-generation timestamp prompts, video prompts
- small prop ledgers, decorative objects, texture, lighting design, style concepts
- minor items that do not affect spatial understanding

## Content Selection

For each scene, include:

- The minimum space needed to understand where characters start.
- The minimum furniture/partition layout needed to explain interaction.
- Key fixed obstacles that affect later blocking.

Leave dramatically important small props to the supplied story material or director script when they do not affect spatial layout.

## Review Criteria

Before delivery, check:

- Scene count: one SVG exists for each supplied source scene in scope unless the user explicitly requested multiple layouts for one scene.
- Layout clarity: the viewer can tell where characters are and what major spatial areas exist.
- Simplicity: no clutter, no small prop overload, no camera/shot/storyboard content.
- Source fidelity: locations and character positions match the supplied material.
- Technical validity: each SVG parses as valid XML.

## Review Prompt

Tell the user:

```text
场景俯视布局 SVG 已画完，请审查空间和人物位置是否对。
```
