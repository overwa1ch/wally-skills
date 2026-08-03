# Preview Visual Test

Preview tests the combined visual system before production asset prompts are written.

## Entry condition

Enter immediately after the user confirms:

- the static asset plan;
- the provisional `regional_anchor`;
- the provisional `style_aesthetic`.

If the user explicitly supplied these as locked decisions, proceed without repeating the discussion.

## Build one representative effect image

- Make a person the visual subject.
- Choose the confirmed visual medium: live-action photography, 2D animation, 3D animation, stop motion, illustration, picture-book art, game cinematic, or another approved form.
- Combine representative character appearance, action, environment, regional facts, aesthetic treatment, light, color, materials, atmosphere, and a few credible imperfections.
- Test the overall visual direction, not plot coverage, storyboard layout, or a sequence of shots.
- Use one representative direction by default. Provide variants only when the user asks or when a named unresolved choice requires comparison.

## Give the prompt for user testing

Return one copy-ready prompt using the recommended order in `craft.md`. Do not generate the image unless the user separately requests image generation.

Translate the anchors into visible language. Do not paste abstract `regional_anchor` or `style_aesthetic` blocks into the prompt unchanged.

## Review the returned Preview

Check:

- whether the person appears to belong in the world;
- whether style preserves regional, historical, material, and social truth;
- whether medium, stylization, palette, light, texture, and atmosphere match the decision;
- whether visible imperfections support authenticity or craft;
- whether prompt pollution introduced competing objects, full-body detail outside frame, generic polish, or AI artifacts.

Name the smallest change needed in the anchor, aesthetic, character direction, or Preview prompt. Continue to production prompts only after user confirmation.
