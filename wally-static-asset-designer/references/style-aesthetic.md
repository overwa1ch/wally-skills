# Style Aesthetic

Use `style_aesthetic` to define how the confirmed world and subjects are visually represented.

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

Compare `style_aesthetic` with `regional_anchor` before Preview:

- Can the palette and light exist in the stated climate and space?
- Does the finish preserve the required materials, age, wear, and social condition?
- Does stylization distort culturally or historically important forms?
- Do both directions demand incompatible cleanliness, saturation, geometry, or texture?

When a collision exists, state the regional fact, the conflicting aesthetic rule, and one or more compatible syntheses. Let the user decide. Do not silently privilege one anchor or force both into the same prompt.
