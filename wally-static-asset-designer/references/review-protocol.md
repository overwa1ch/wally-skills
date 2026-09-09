# Review Protocol (shared)

Load this file plus the asset's `types/<asset>.md` checklist when reviewing a returned image, an existing asset, an asset plan, or a generation brief.

## Evidence base

- Compare the product with the user's target, supplied materials, visible references, and its type contract when present.
- Accept incomplete or mixed materials. State what remains unverifiable.
- Treat a storyboard as valid evidence for visible state, composition, space, and props while respecting its level of detail.

## Shared checks

1. **Fidelity:** preserve explicit identity, object, setting, screenplay tone, `regional_anchor`, and world facts. Preview follows its declared candidate style; production assets follow the user-selected global `style_aesthetic`.
2. **Reuse value:** expose the views, structure, scale, state, and materials needed for consistent reuse.
3. **Physical coherence:** keep anatomy, weight, joints, contact, construction, mechanisms, lighting, and surface behavior coherent with the established world and selected medium.
4. **Readability:** make silhouettes, feet, hands, faces, edges, entrances, paths, contact points, and important details visible where relevant.
5. **Continuity:** keep identity, proportions, wardrobe logic, prop state, location structure, and material history stable across views.
6. **Drift control:** remove unsupported beauty polish, luxury styling, brands, landmarks, text, extra subjects, story action, or layout modules.

Then run the type checklist in the asset's `types/<asset>.md`.

肤质、表面与造型按当前版本适用的媒介和风格判断。漫画、插画或其他风格化表达本身不构成错误；标记的是无依据地偏离选定方向、参考事实或类型合同，不把写实程度当作通用及格线。

## 候选包与用户选择

- 生成任务按 [SKILL.md](../SKILL.md) 的数量要求逐版检查，再横向比较：每个方向须有不同的完整提示词和可见设计差异，不能用重复文案、随机重画或技术重试充数。
- Preview 各方向都要符合剧本整体调性；正式资产各版本都要继承已选全局风格和基础参考。指出差异和客观问题，不把个人审美偏好写成技术失败。
- 版本号、原图、提示词和评审一一对应；缺图、失败和不足数量明确保留。不得只展示 Agent 喜欢的一版，也不把未下载原图的结果计为已交付候选。
- 每版技术 verdict 与用户选择分别记录。用户自行选满意的版本；没有明确选择时保持未选定，不向依赖它的下一阶段传播“已批准”状态。

## Non-asset product checks

- **regional_anchor:** concise visible cues for geography, climate, era, social conditions, architecture, materials, daily life, practical light, and avoidances; world truth without prescribing an image finish. Flag plot summary, biography, abstract theme, unsupported place names, tourist landmarks, brand invention, or per-asset repetition.
- **style_aesthetic:** visible rules for medium, stylization, shape, color, light, material rendering, texture, atmosphere, imperfection, and avoidances that preserve locked regional, historical, material, and social facts. Flag empty prestige language, contradictory cleanliness or saturation, generic genre replacement, or style rules that erase the world.
- **Preview:** each candidate is one person-led effect image in a permitted medium, sharing the representative content baseline while testing a distinct global style direction compatible with the screenplay. Flag prompt pollution, irrelevant off-frame detail, conflicting world facts, tonal drift, generic AI polish, or a result that cannot guide production assets.
- **Production prompt:** one copy-ready prompt containing both the design specification and the generation instruction, with only relevant anchor effects translated in. Flag a detached duplicate design report, missing presentation instructions, or abstract anchor text pasted without translation.

## Findings and verdict

For every material issue, state the visible location or field, the observed problem, its continuity impact, and the smallest concrete revision. Preserve decisions that already work. When requesting regeneration, restate what must stay unchanged (invariants) alongside the correction.

Use one technical verdict per candidate or reviewed product: **usable**, **usable with minor revisions**, or **revise and return**. List missing evidence as open issues instead of inventing a failed gate. A technical verdict does not select or approve a candidate on the user's behalf.
