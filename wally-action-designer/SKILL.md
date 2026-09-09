---
name: wally-action-designer
description: Design AI-video performance, blocking, camera, lighting, sound, and object-to-reference bindings from supplied materials. Use for 表演设计, 动作设计, 视频导演提示词, 参考素材与对象绑定, 提示词修改, or 回片审查. Preserve approved story and dialogue while developing their execution.
---

# Wally Action Designer

Turn the user's current materials into an executable director-design prompt body for one video scope, and review returned videos against the delivered body.

Version: `wally-action-designer@2026-09-08-v3.21-example-cleanup`

## Tasks

Complete the task the user names. Ask for missing information only when it is required for the dependent work.

### A. Design a director body

1. Identify the requested scope, supplied duration and format, story, dialogue, reference materials, and explicit execution decisions.
2. Read [craft.md](references/craft.md) for performance and filmmaking decisions, and [contract.md](references/contract.md) for output structure.
3. Develop performance, action, camera, timing, lighting, and sound. Return the finished prompt body directly.

### B. Review a prompt body

Read [contract.md](references/contract.md). Identify omissions or contradictions that affect execution and correct them in the relevant field. Read `craft.md` when reviewing performance or filmmaking choices.

### C. Review a returned video

Read [review.md](references/review.md) for comparison with the delivered body, findings, and rerun, edit, or extension decisions.

## Responsibilities and handoffs

- Preserve the supplied story, approved dialogue, and the user's explicit execution decisions. Develop the remaining performance and filmmaking choices.
- When spoken wording requires creation or revision, resolve it through `wally-screenplay-writer` before writing its performance.
- When a required visual anchor is missing, describe the needed image for `wally-static-asset-designer` before continuing the dependent design.
- `wally-helper` handles final Route A/B assembly when requested.
