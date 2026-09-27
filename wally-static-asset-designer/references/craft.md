# Image Prompt Craft

提示词使用精简、可见、可核对的描述。

## 整体风格＋构图描述

Preview 与自然效果图的正文只组织为以下两部分，每条信息只写在其所属部分：

1. **整体风格**：包含图片类型、文化语境与视觉风格。正文先定义图片类型，再自然写入地域、时代和必要物质文化，随后把所选风格关键、具体的可见特征写成画面要求；名称只能辅助概括，不能替代定义。由 Agent 结合剧本和真实参考提炼，不要求用户逐项提供技术指标。用户指定真实剧照时，开头写“一张真实电影剧照”，文化信息不冠以“文化锚点为”等标签。视觉风格的定义与验证见 [style-aesthetic.md](style-aesthetic.md)，文化取舍见 [regional-anchor.md](regional-anchor.md)。
2. **构图描述**：只写当前画面的可见内容、空间关系与观察方式。按画面需要描述主体外观、服装道具、姿态与视线、环境、位置与遮挡、前中后景、景别、视角和需要看清的对象；只保留当前取景内有用的内容。具体窗、灯等光源的位置，以及剧情或用户明确要求的时段、局部照明关系可以保留；整体光质、反差、色调、颗粒、锐度和景深倾向归入整体风格。不要给所有候选额外固定同一种午后光、全画面清晰度或背景虚化。

构图描述不写作品介绍、故事背景、角色履历、身份头衔、剧情解释或抽象动机。文化锚点在整体风格中明确保留，其对当前画面的影响落实为有依据的服装、装备、建筑、材质与生活痕迹；不因限制背景介绍而删除文化锚点。姓名、职务和剧情等信息只在内部用于识别对象或理解材料，画面需要的部分转译为可见特征，未产生可见差异的信息省略。

正文使用短句，优先描述最重要的风格特征、主体和关系。版本号、候选方向名、参照作品、剧本适配分析、参数出处、评审说明及生成历史保存在记录中，不进入这两段；不写“《某片》风格”。视觉风格的关键可见定义必须进入正文，不附选型过程或长篇分析。实际需要生成的画内文字按对应类型合同另行声明。

正式资产板式按 `types/<asset>.md` 和 `contracts.md` 保留所需的视图、网格与结构指令；其中的构图描述同样遵守上述可见信息边界。

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
- 风格命名：“王家卫风格”可作为真实风格名称的写法示范；适配性和生效程度仍需分别分析与看图验证。不能改写成“《重庆森林》风格”，也不把名称本身当作稳定复现的证据。

## Separate durable structure from model routing

Model choice, text-rendering ability, weighting behavior, and punctuation interpretation change over time. Treat them as current platform guidance, not permanent design rules. State a model recommendation only when the user names the available platform or asks for routing.

Production asset boards may need technical structure that is longer than a natural Preview prompt. Keep that structure purposeful: the design specification and generation instruction still belong in one copy-ready prompt.
