# Style Aesthetic

Use `style_aesthetic` to define how the confirmed world and subjects are visually represented.

## 候选与选定

Preview 前保留剧本整体调性、世界事实和用户明确锁定的媒介边界，在这些条件内提出多个不同的风格方向，不提前把一个候选当成全局定稿。候选设计与数量见 [preview.md](preview.md) 和 [SKILL.md](../SKILL.md)。

Preview 选图后，将用户选定图像实际呈现的媒介、造型、色彩、光线、材质与纹理提炼为当前 `style_aesthetic`，并引用该选定原图。后续正式资产共同继承；未选候选保留在生成记录中，不混入全局规则。

## 整体风格包括什么

整体风格按以下三项理解和讨论，用简短文字与实际画面表达：

| 内容 | 定义范围 |
| --- | --- |
| 图片类型 | 真实电影剧照、摄影、插画或其他已确定的产物形式。 |
| 文化语境 | 地域、时代及相关服装、装备、建筑和生活材料的文化依据。 |
| 视觉风格 | 根据剧本与真实参考，提炼决定整体质感的关键可见特征，用简洁明确的画面描述写入提示词，使模型获得具体生成依据。风格名称仅作概括，不能替代定义。 |

字段始终叫“视觉风格”，“整体质感”是它要实现的效果。用户主要判断画面是否贴合剧本、是否愿意采用该方向。Agent 负责读剧本、选择真实参考、筛选关键定义并验证结果，不要求用户先提供摄影或美术指标。

表达方式保持灵活：可以从真实风格名称展开，也可以先概括整体观感，再用相互配合的关键视觉特征写清画面。保留已有有效写法，结合具体剧本和回图判断采用哪种表达；不同写法可以并存。

视觉风格正文必须写清风格具体呈现为什么样的画面。按所选方向保留真正决定结果的少量特征，可涉及色彩关系、光影方式、人物与环境的表面表现或成像质地；不要求逐项填满，不堆术语。情绪词须落实到有参考依据的可见表现，不能只写导演名称或“高级、电影感、有氛围”。构图、人物动作与空间关系仍留在构图描述。文化语境的事实范围遵循 [regional-anchor.md](regional-anchor.md)。

给模型的关键定义应进入正文，参照选型分析和来源留在记录。采用参考图时，核对图像与正文定义是否一致；参考图不能代替关键定义。具体器材或数值仍须查证，不凭图片外观猜测。生成后对照定义检查关键特征是否出现；未获回图验证时只称候选写法，不宣称稳定复现或一次必定成功。本规则本身不触发生图。

## 按剧本选择参照

先读当前剧本，结合题材、人物处境、情绪变化、关键场景与叙事重点寻找真实影视作品。参照可以来自相近题材，也可以与剧本形成有意义的反差；后者需说明它服务于剧本中的哪项具体需求，不能只用“有化学反应”代替分析。把作品、适配理由和证据保存在选型记录中。

先明确关键视觉定义及其真实依据，再按需要补充名称、参数或图像参考。用户认可的纯文本方案可以直接测试；仅在采用图像参考时要求实际接入，不因当前没有参考图而擅自改换任务。

- **风格参考图作为主要依据**：先核看来自真实作品、摄影或用户已有候选的图像，结合剧本选择，在记录中明确来源与引用用途。使用平台实际提供的风格参考方式接入；平台无独立风格控件时，只能按实际附件能力说明用途并核看结果，不能声称实现了同等控制。参考用于视觉表现，图中人物身份、服装、道具和布局仍以本项目材料与构图描述为准。尚未被用户选定的图可以用于当前候选测试，不自动成为全局依据。
- **风格名称作为辅助**：采用真实存在、可确认的风格名称或导演风格名称，并写出该方向关键、具体的视觉定义。不能凭名称不同认定方向已经不同；生图正文不写“《某片》风格”，也不自创风格名称。特征直接表述为画面要求，省略“借用某片哪些特征”等分析性说明。
- **摄影参数作为有证据的辅助**：从适配剧本的真实作品中查证实际摄影机、镜头、胶片、滤镜或相关参数；使用摄影师访谈、制作资料、专业摄影组织或厂商的一手资料。只写来源确实支持的配置及取值，未公开的焦距、光圈等省略。区分全片器材清单与特定场景配置，不用前者推定某个镜头的实际设置，也不将多部作品的设备拼成一套声称真实使用过的配置。图片外观不能证明器材或数值；有真实出处也不保证模型准确模拟。作品名、来源及证据适用范围留在记录中。

## 可复用的整体风格

整体风格正文依次写图片类型、自然融入的时代地域与必要物质文化、视觉风格的关键具体定义；名称或已查证参数按需辅助，采用的视觉参考随输入实际接入。正文不用“文化锚点为”等说明性措辞。用户指定真实剧照时，以“一张真实电影剧照”定义产物，候选均遵守这一媒介边界。

选定后保存参考图的可追溯位置、完整正文和实际生效的平台设置，后续共同复用。Preview 先按 [代表画面规则](preview.md) 检验同一风格对全片主要表现目标的适配；跨主体、构图及随机结果的风格保持程度以实际图像核验。各场景保留剧情需要的时段、光源与情绪变化。仅吸收动作设计 `Style`、`Camera` 中适用于静态图像的内容，不引入运镜、剪辑、帧率或时序。

当前图片的主体、动作、景别、机位、位置与空间关系进入构图描述；全局光影、色彩与成像倾向保存在整体风格中。构图只额外规定当前画面确需看清的对象与有依据的局部照明关系，不用统一摄影效果预先覆盖候选差异。

## Use style extraction when it helps

If the user has complex reference images, videos, moodboards, generated samples, or mixed media that require systematic extraction, recommend the related Wally skill `wally-visual-style-extractor`.

- Treat it as a user-managed handoff with no runtime dependency or shared files.
- Do not require it when the user can already state the desired style.
- Accept its result in any format as ordinary user-provided material.
- Treat extracted rules as candidates, not automatically approved truth.

## Draft efficiently

Use visible, testable language; omit reputation words and quality slogans.

## Agent 内部适配检查

Compare each candidate `style_aesthetic` with the screenplay's overall tone and `regional_anchor` before Preview:

- Can the palette and light exist in the stated climate and space?
- Does the direction preserve the screenplay's emotional register, narrative attitude, and character circumstances?
- Does the finish preserve the required materials, age, wear, and social condition?
- Does stylization distort culturally or historically important forms?
- Do both directions demand incompatible cleanliness, saturation, geometry, or texture?

When a collision exists, state the regional fact, the conflicting aesthetic rule, and one or more compatible syntheses. Let the user decide. Do not silently privilege one anchor or force both into the same prompt.
