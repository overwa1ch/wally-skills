# Static Asset Planning and Design

Use this guide to decide which reusable static assets the project needs and what each asset must lock.

## Read the evidence

- Extract stable identity, temporary state, material, scale, spatial, cultural, and continuity facts from any supplied format.
- Separate explicit facts from inference. Surface contradictions that would change identity, structure, scale, location, or visual direction.
- Convert abstract information into visible choices: silhouette, proportion, construction, surface history, climate traces, practical light, grip points, entrances, paths, or fixed structures.
- Treat storyboards as evidence at their actual level of detail. Rough marks do not establish fine identity or texture.

## Propose the smallest useful asset set

Plan an asset when it materially improves later consistency or reuse. For each proposed item, explain:

- what it locks;
- where it will be reused;
- which supplied facts support it;
- which other asset or reference it depends on;
- what remains unresolved.

Invite the user to add, remove, merge, split, or rename items.

## Choose an asset family

- **`Cxx`:** one stable named or continuity-critical identity.
- **`Cxx-Lxx`:** one character's makeup, styling, condition, expressions, and key actions in one scene. Create one `Cxx-Lxx` per character per scene.
- **`Gxx`:** one coherent anonymous social, occupational, or crowd pool of 6—8 people without named identities.
- **`CSxx`:** relative scale and body-proportion comparison among relevant `Cxx` characters.
- **`Pxx`:** one recurring, signature, or mechanism-critical prop in its base design and baseline state.
- **`Pxx-state`:** one approved base `Pxx` in one production-critical changed condition, such as damaged, wet, depleted, opened, or activated.
- **`Sxx location_reference`:** one stable location identity shown through one reusable wide establishing view.

Use these labels for traceability only. Natural asset names are valid.

## Separate stable and variable information

- Put stable face, bone structure, body proportion, baseline hair, wardrobe logic, shoes, accessories, and life traces in the base character.
- Put one scene's makeup and styling changes, dirt, wetness, fatigue, injury, carried objects, expressions, key actions, and physical state in that scene's character-state asset.
- Put recurring prop structure, scale, mechanism, material, markings, wear, and baseline state in `Pxx`. Put one story-critical damaged, wet, depleted, opened, activated, or otherwise changed condition in one `Pxx-state` when it must be locked visually.
- Put stable spatial identity, structure, materials, and visible use traces in the location asset.
- Put shared world facts in `regional_anchor` and shared treatment in `style_aesthetic`. Translate only their relevant visible effects into each prompt.

## Design for the intended use

Identify the views, scale, state, and relationships required for reuse. The selected production template owns layout, background, light, and output form.

For every asset, lock only useful dimensions:

- identity or object definition;
- stable structure and proportions;
- materials and surface history;
- current state when relevant;
- views needed for downstream reuse;
- scale or spatial relationships;
- prohibited drift.

Do not describe details outside the selected view. Do not add action, scene dressing, mood, or visible body parts that the output format cannot show.

## Preserve intrinsic dependencies

- A production `Cxx-Lxx` should use the relevant base identity image. Without it, provide a draft and mark identity lock unresolved.
- Do not merge one character's multiple scenes into one `Cxx-Lxx`, even when the makeup and styling are unchanged. Do not split one scene by individual actions; collect that scene's state progression and key actions on one sheet.
- A production `CSxx` should use the relevant `Cxx` images. Use one shared image scale, one shared ground line, and confirmed relative proportions; do not derive a new character design from narrative importance.
- Use one `Gxx` for one coherent group function. Split groups when occupation, class, age function, or social role requires a materially different makeup and styling system; do not crowd unrelated people onto one sheet.
- Use one `Pxx` for one prop design. Keep its base asset free of story staging and alternate-state panels. A production `Pxx-state` must use the approved base `Pxx` image, show one changed condition consistently across all views, and remain free of before/after comparison panels. Without the base image, name the missing input and stop; provide an identity-unresolved draft only when the user explicitly requests one.
- Use one `Sxx location_reference` for one stable location. Describe only the spatial, architectural, furnishing, material, sign, light, and atmosphere facts that materially establish its identity and reuse.
