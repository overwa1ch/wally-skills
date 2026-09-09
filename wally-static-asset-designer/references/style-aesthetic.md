# Style Aesthetic

Use `style_aesthetic` to define how the confirmed world and subjects are visually represented.

## 候选与选定

Preview 前保留剧本整体调性、世界事实和用户明确锁定的媒介边界，在这些条件内提出多个不同的风格方向，不提前把一个候选当成全局定稿。候选设计与数量见 [preview.md](preview.md) 和 [SKILL.md](../SKILL.md)。

Preview 选图后，将用户选定图像实际呈现的媒介、造型、色彩、光线、材质与纹理提炼为当前 `style_aesthetic`，并引用该选定原图。后续正式资产共同继承；未选候选保留在生成记录中，不混入全局规则。

## Define the treatment

Capture only the dimensions that materially affect generation:

- visual medium and production form;
- realism or stylization level;
- shape, line, volume, and surface treatment;
- palette, saturation, contrast, and color relationships;
- light quality and shadow behavior;
- material rendering, image texture, grain, and finish;
- overall emotional register and intended imperfections;
- recurring visual clichés, polish, or AI artifacts to avoid.

Global photographic or rendering language may live here. Specific shot size, camera position, panel composition, or camera movement belongs to storyboard work.

## Use style extraction when it helps

If the user has complex reference images, videos, moodboards, generated samples, or mixed media that require systematic extraction, recommend the related Wally skill `wally-visual-style-extractor`.

- Treat it as a user-managed handoff with no runtime dependency or shared files.
- Do not require it when the user can already state the desired style.
- Accept its result in any format as ordinary user-provided material.
- Treat extracted rules as candidates, not automatically approved truth.

## Draft efficiently

Use visible, testable language; omit reputation words and quality slogans.

## Check compatibility

Compare each candidate `style_aesthetic` with the screenplay's overall tone and `regional_anchor` before Preview:

- Can the palette and light exist in the stated climate and space?
- Does the direction preserve the screenplay's emotional register, narrative attitude, and character circumstances?
- Does the finish preserve the required materials, age, wear, and social condition?
- Does stylization distort culturally or historically important forms?
- Do both directions demand incompatible cleanliness, saturation, geometry, or texture?

When a collision exists, state the regional fact, the conflicting aesthetic rule, and one or more compatible syntheses. Let the user decide. Do not silently privilege one anchor or force both into the same prompt.
