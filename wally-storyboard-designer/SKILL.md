---
name: wally-storyboard-designer
description: "Design the 分镜脚本 (processed director script), issue the fixed storyboard and shot-table prompts, and execute their visual tests through ChatGPT Web in the in-app Browser when requested. Use for 分镜脚本, 导演脚本, 镜头脚本, 场景布局, 拍摄手法, 景别, 机位, 运镜, 分镜脚本修订, 提示词污染检查, 故事板 prompt/test, or 分镜表 prompt/test. Inherit the supplied work definition and source scenes. This is the shot-design test layer; keep original screenwriting, static-asset design, performance/dialogue/audio design, returned-board story judgment, and final video prompt assembly outside it."
---

# Wally Storyboard Designer

Provide on-demand storyboard-domain functions for the user's supplied story, scene, or shot material.

This skill is the test layer of the Wally pipeline: design the 分镜脚本 → issue fixed prompts or execute the requested ChatGPT Web visual test → the user judges the boards → apply targeted revisions. Each requested product can stand alone.

Current version: `wally-storyboard-designer@2026-09-08-v3.17-progressive-disclosure`

## 共用规则

- Accept scene-divided scripts, individual scene excerpts, briefs, test plots, tables, images, asset references, partial artifacts, conflicting drafts, existing director scripts or shot sequences, the user's observations from generated boards, or any mixture.
- Do not require completeness, a locked or approved source, a particular schema, an asset package, a route choice, or a fixed starting stage. Surface only conflicts that would materially change the named product.
- Preserve supplied story facts. Do not expand, rewrite, doctor, or originate the screenplay; send original screenwriting work to `wally-screenplay-writer`.
- For a generation product that needs scene boundaries, require an upstream screenplay or excerpt with explicit source scenes. When those boundaries are absent, stop and route scene formation to `wally-screenplay-writer`.
- Treat the source scene boundaries, exact headings, and order as the sole authority. Never split, merge, rename, normalize, or renumber them. A source scene may contain multiple action chains, dramatic beats, storyboard pages, and any number of necessary shots.
- Preserve the latest explicit or approved `作品定义` as source authority. Keep work form, commercial function, narrative mode, delivery format, and audiovisual position distinct.
- Functions are on-demand. Deliver exactly the product the user names. If it lacks a required input, name the missing input and stop; do not produce the upstream product uninvited.
- Keep the fixed storyboard and shot-table prompt templates verbatim. Do not insert a scene title or make any other runtime substitution. Only an explicit template-edit request authorizes changing the named text surface; preserve the rest.
- Do not offer returned-board review as a product. The user judges storytelling and visual quality; their observations are inputs to targeted 分镜脚本 revisions. Web execution includes only the technical intake checks defined in its workflow.
- Do not design static assets, performance, dialogue, vocal delivery, timing performance, or audio; do not choose Route A/B or assemble final video prompts.

## 按任务读取

只读取当前任务对应的文件；执行步骤与格式要求由该文件维护。无需默认通读 references、脚本源码或测试。历史版本记录留在仓库级 Changelog，不作为执行指令加载。

| 当前任务 | 读取入口与交付范围 |
| --- | --- |
| 新建场景布局 SVG | 仅在用户明确发起时读 [场景布局规则](references/scene-layout-svg-rules.md)，只做点名的 SVG；已停止或删除的请求不延续。 |
| 分镜脚本或定向修订 | 读 [导演脚本合同](references/director-script-output-contract.md)，按其作品定义、镜头格式与修订规则交付。 |
| 提示词污染检查 | 仅在用户要求时读 [污染检查](references/pollution-check.md)；检查由干净上下文执行，写作者不自查。用户要求应用报告时，再读导演脚本合同中的定向修订规则。 |
| 只要固定提示词 | 按所选产品读 [故事板模板](templates/storyboard-prompt-template.md) 或 [分镜表模板](templates/shot-table-prompt-template.md)，在当前对话分别展示两个带标签的正文块后结束。 |
| 执行网页视觉测试 | 读 [ChatGPT Web 流程](references/chatgpt-web-visual-test-workflow.md) 和所选模板，在内置 Browser 完成生成与交付。输入检查、脚本调用、网页提交、原图验收和组装规则都由该流程维护。 |

故事板提供带景别、运镜与动作说明的草图；分镜表依据导演脚本与静态资产展示带数字镜号的镜头序列。产品选择权在用户；类型无法从上下文确定时，只澄清要故事板还是分镜表。
