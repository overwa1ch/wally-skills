# Image Prompt Craft

Write prompts as efficient visible instructions, not essays.

## Use ordered blocks

For a natural effect image or Preview, use this order:

1. generated object and core style;
2. main subject;
3. action and state;
4. scene, space, environment, and light;
5. composition and viewing angle;
6. emotion and atmosphere;
7. a few style-appropriate imperfections.

Put the most important object, medium, style, and subject first. Use short clauses separated by commas. Parentheses may add a precise clarification; do not use them as assumed emphasis.

Production asset sheets follow the drafting order in their `types/<asset>.md` file and the shared rules in `contracts.md` instead of this list.

## Keep the prompt visible and coherent

- Give a person something natural to do instead of defaulting to looking at the viewer.
- For multiple subjects, state the visual focus and supporting hierarchy.
- Mention only details visible in the selected framing. A close-up should not describe trousers or shoes.
- Describe the viewing geometry of a selfie rather than forcing a phone into frame when the phone should remain unseen.
- Add a few useful imperfections such as loose hair, natural folds, uneven light, surface wear, hand-made variation, or environmental residue.
- Remove synonyms, repeated quality claims, and decorative detail that competes with the main target.
- Avoid empty stacks such as `extremely detailed`, `4K`, and `ultra-realistic` when they make skin, hair, light, or materials hard and artificial.

## 关键短例

以下仅示范局部写法，不是完整提示词或候选包；示例事实不带入其他项目。

- 可见性：近景只拍上半身时，把“全套服装精致、鞋子沾泥”改为材料支持的“领口向外翻起，右肩有一道浅色擦痕”；不写画外鞋子。
- 风格转译：材料允许剪纸方向时，把“有艺术感”改为“人物用大块平面色形概括，纸边有轻微手工切割起伏，纸层投下薄而清楚的阴影”；不顺手增加年代、职业或剧情。

## Separate durable structure from model routing

Model choice, text-rendering ability, weighting behavior, and punctuation interpretation change over time. Treat them as current platform guidance, not permanent design rules. State a model recommendation only when the user names the available platform or asks for routing.

Production asset boards may need technical structure that is longer than a natural Preview prompt. Keep that structure purposeful: the design specification and generation instruction still belong in one copy-ready prompt.
