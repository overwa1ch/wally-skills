# Scene Layout SVG Rules

Use only when the user explicitly starts a new scene-layout SVG task. The current contract has four rules:

1. **Use explicit source scenes.** Create one local `.svg` per supplied source scene, using its exact boundary and order. Do not infer, split, merge, rename, or renumber scenes. If the scene boundary or required spatial facts are missing, name only what is missing and stop.
2. **Show only the initial state.** Capture the scene's first visible character and object arrangement. Do not add later dialogue, gaze, movement, contact, regrouping, or extra state panels unless the user explicitly requests another layout.
3. **Include only active interaction content.** Show the main characters' starting positions. Include an environment element, fixture, piece of furniture, large object, or prop only when a character is already physically touching, operating, opening, closing, crossing, sitting or leaning on, carrying, or otherwise using it in the initial state. Omit passive background, decorative context, and minor items that do not affect spatial understanding.
4. **Preserve true top-down geometry.** Use simple geometric shapes and one coherent approximate real-world footprint scale. Preserve supplied positions, orientations, contact distances, and object proportions; do not rearrange or rescale subjects to fill the canvas. Fit the viewBox to the included geometry and deliver valid XML.
