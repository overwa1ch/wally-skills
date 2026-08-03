# SEG Breakdown Rules

Use when turning any supplied story-bearing prose, screenplay, brief, prompt, table, image, partial draft, conflicting draft, existing board, or mixed material into story units. Completion and approval labels are not prerequisites; preserve only the usable facts in the supplied material and surface a conflict only when it would change the split.

## Core Rule

Build pure-script `SEG` story units. Each `SEG` contains one contiguous source passage with one pressure, one action chain, one turn, and one ending state. Split by story occurrence, pressure, and continuity space; repeated locations stay separate when intervening action, a new pressure, or a changed state separates them. Output only source text under each `SEG` header.

## Source-Preserving Split

Preserve source order, plot facts, cause/effect, dialogue meaning, character intent, locations, key props, and beat endings. For briefs, split only visible facts, actions, relationships, and required turns already present in the brief.

Start a new `SEG` when one changes materially:

- dramatic function
- main action chain
- reveal state
- power relation
- location or continuity space
- scene occurrence after another story passage, including returns to the same location
- prop state
- dialogue premise
- execution load would exceed a natural short video unit

Use the fewest `SEG` units that preserve these changes. Keep an immediate consequence, reaction, blackout, reveal, or other terminal beat with the action chain it completes; do not isolate a one-line ending state unless it starts a new pressure, occurrence, or continuity space.

Use story continuity as the split basis. Keep sentence splits, imagined camera angles, storyboard panels, and scene headings out of the decision unless they change story pressure or continuity.

## Compact Output

```text
SEG01｜地点 / 时间 或 来源片段名

动作描写、可见事实和对白，按原始顺序写成纯剧本内容。

角色A：对白。

动作继续。

SEG02｜地点 / 时间 或 来源片段名

动作描写、可见事实和对白，按原始顺序写成纯剧本内容。
```

## Constraints

- Keep the first pass source-preserving.
- Treat repeated locations as separate story occurrences when the plot leaves and later returns to them.
- Keep camera plans, shot counts, timestamp lines, asset/style prompts, storyboard plans, and analytical fields out of `SEG`.
- For briefs, write concise screenplay-style visible facts under each `SEG`; keep functional summaries in reasoning.
