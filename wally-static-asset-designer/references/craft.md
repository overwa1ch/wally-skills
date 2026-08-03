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

## Strong/weak pairs

- Weak: 一位美丽的中年女售货员，极致细节，4K高清，超写实。
- Strong: 45岁女售货员，深蓝的确良工作服袖口磨出毛边，齐耳短发别黑色发卡，指关节粗大，神态温和带倦意。
- Weak: 一个充满年代感的供销社，氛围感拉满。
- Strong: 水磨石地面，L形玻璃木柜台，到顶的木货架摆着搪瓷缸和暖水瓶，双管日光灯的垂线缠着胶布，墙面绿漆起皮。

The strong version names visible nouns, materials, and wear; the weak version stacks judgments the model cannot see.

## Separate durable structure from model routing

Model choice, text-rendering ability, weighting behavior, and punctuation interpretation change over time. Treat them as current platform guidance, not permanent design rules. State a model recommendation only when the user names the available platform or asks for routing.

Production asset boards may need technical structure that is longer than a natural Preview prompt. Keep that structure purposeful: the design specification and generation instruction still belong in one copy-ready prompt.
