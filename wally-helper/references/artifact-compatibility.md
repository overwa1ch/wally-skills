# Artifact Compatibility and Assembly Rules

Single source for cross-product compatibility review and final assembly. Review whether the supplied products can be assembled for the requested route; preserve specialist content. Never author a missing specialist field or repair professional content inside Helper.

## Shared checks

- Confirm exactly one current generation scope.
- Confirm the content type when Route A needs its fixed tone line.
- Confirm that names for the same character, prop, place, and scope are unambiguous across products.
- Confirm that platform handles resolve to the user-intended approved references and every binding has a declared role.
- Confirm that the director-design product belongs to the current scope and contains no `Reference:`, platform handle, `Reference List`, or `Asset List`.
- Accept both legacy V2 fixed director bodies and V3 adaptive bodies. Do not require a fixed combination of `Style`, `Lighting`, `Camera`, execution paragraph, Shot, or Avoid labels.
- Review semantic sufficiency: the fields and execution carrier actually present must express the requested visible process, necessary initial or ending state, and any task-critical timing, camera, performance, physics, text, dialogue, invariants, or failure controls. Omitted fields pass when they add no independent control value.
- Confirm exactly one director-body `Audio:` field (legacy `SFX:` also passes) and preserve its approved branch: **default** starts with `无BGM。` and supplies a substantive non-musical sound state; **explicit music** describes the supplied/requested music and omits `无BGM`; **absolute silence** states full-scope silence and adds no ambience, foley, dialogue, voiceover, or music. Advertising or montage context never implies music by itself.
- If exact ranges are present, confirm that they are ordered and fit the approved duration. Do not require timecodes from a body that intentionally uses Action only.
- Reject unresolved contradictions or missing information that makes this particular task non-executable. Return such a body to `wally-action-designer`; do not fill the gap here.

If names differ but identity is clear, normalize only the model-facing display label and keep a temporary mapping. If identity is unclear, request one binding decision.

## Route A checks

- A storyboard platform reference is present and covers the current scope.
- Necessary static references are bound by visible names and platform handles.
- The optional Preview image is included only when supplied and selected.
- The outer `Reference List` names the storyboard as the model-facing controller of shot order, camera movement, character action, spatial relationships, and prop relationships.
- Paste the complete director-design product unchanged, whether it is legacy fixed or V3 adaptive.

## Route B checks

- Every model-facing reference has a quoted referable screen-object identity name, a confirmed platform handle, an asset form, and a role.
- Every entry maps to an approved finished file. A multi-view, nine-grid, or multi-state board remains one asset unless separate finished files and handles actually exist.
- The static references cover identities and structures the current generation scope cannot safely infer from text alone. If required coverage is absent, request a static-asset product instead of inventing a name or handle.
- Every asset in `Asset List` uses `“[referable screen-object identity]” = @[confirmed platform handle] - [asset form and use]`.
- Cite each exact quoted identity in an execution-bearing location where it visibly controls generation: `Subject`, `Action`, `Timing/beats`, or a Shot. A citation only in `Continuity`, an explanation, a summary, or the outer list fails.
- For a legacy V2 body, cite each visible asset in its relevant timecoded Shot. For a V3 body, use whichever allowed execution carrier the body actually contains; never add Shot solely for asset citation.
- Keep the storyboard out of the model-facing `Asset List`.
- Preserve the director body's field order, execution carrier, timing, action, dialogue, camera, lighting, acting, physics, audio, and outcomes while inserting only minimal identity citations.
- If the body ends with `Avoid:` or legacy `避免：`, remove that field from `Prompt` and move its content once into `Constraints` as `禁止出现：`. Normalize only declared `source_aliases` or bare declared identities to their exact quoted identity while moving it; preserve every other character. If neither trailing field exists, omit the `禁止出现：` line completely.

## Outer reference binding rule

Use only confirmed platform bindings that resolve to approved finished assets. Route A writes them in `Reference List`; Route B writes them in `Asset List` as `“[referable screen-object identity]” = @[confirmed platform handle] - [asset form and use]`.

The equality binding makes the quoted identity the Prompt-facing name. It must work naturally as the person, place, vehicle, product, or prop in an execution sentence. Keep asset format and role after the hyphen. Do not expose internal IDs, provisional references, invented derivative asset names, or invented semantic handles. Positional handles such as `@图片1` must follow actual upload order and remain outside Prompt.

Never add, replace, or rewrite a `Reference:` line inside the director-design body.

### Machine-readable binding inventory

Pass the approved binding inventory to either route validator with `--bindings`. Use this exact JSON shape:

```json
{
  "schema_version": "wally-reference-bindings/v2",
  "bindings": [
    {
      "identity": "红伞",
      "handle": "@图片1",
      "kind": "static",
      "role": "P03 prop_reference；身份与外观",
      "source_aliases": ["雨伞", "道具伞"]
    },
    {
      "identity": "当前故事板",
      "handle": "@图片2",
      "kind": "storyboard",
      "role": "故事板",
      "source_aliases": []
    }
  ]
}
```

`schema_version`, `bindings`, and all five entry fields are required; unknown fields, duplicate identities/handles, and overlapping alias semantics are rejected. The only accepted version is `wally-reference-bindings/v2`; earlier formats are invalid. `kind` is one of `static`, `storyboard`, or `preview`. Route B globally rejects every `storyboard` binding; Route A requires exactly one `storyboard` for the current generation scope and may include `static` and one selected `preview`. `identity` and `handle` must match the rendered list exactly, and the rendered description must contain `role`. `source_aliases` lists every approved-body term that may be replaced by or normalized to the quoted identity; use an empty array only for a pure identity insertion.

## Director-body preservation

- Route A pastes the complete `wally-action-designer` body byte-for-byte.
- Route B preserves the supplied structure and execution content. Its only permitted edits are inserting the minimal quoted identity into `Subject`, `Action`, `Timing/beats`, or the relevant Shot, and extracting one trailing `Avoid:` or `避免：` into outer `Constraints`.
- Do not summarize, repair, retime, split, add a Shot, create a missing field, duplicate sound design, or convert between legacy and adaptive structures.

## One asset, one name

After binding, every mention of a bound asset in Prompt or Constraints uses its exact quoted identity name. Replace asset-denoting aliases such as `人物`, `产品`, `商品`, `折叠体`, `对比产品`, or `自家产品` with the bound name. Keep each product part to one canonical part name. Do not name an asset absent from the current generation scope; rewrite comparisons with other scopes into results directly visible here.

Image-form labels such as `人物三视图参考` and genre or technique words such as `产品演示` or `纸就产品` are not asset identities and are exempt. `scripts/validate_route_b_prompt.py` reports generic asset aliases outside quoted identities.

## Final format check

- Route B contains no separate `影片调性` line; tone comes from whatever populated director fields carry it.
- All template placeholders are replaced.
- No `Reference:` heading or platform handle appears inside the director body. Route B also contains no outer `Reference List`; Route A contains no `Asset List`.
- The outer reference list matches the selected route and contains only confirmed bindings.
- The Route B asset-name set equals the approved asset inventory for the current generation scope; a reference board appears once regardless of internal panels or states.
- Every Route B identity is cited in `Subject`, `Action`, `Timing/beats`, or a Shot. `Continuity` alone does not count. No raw handle, asset-form identity, `Asset Use:` section, or asset-summary block appears.
- When the director body supplied `Avoid:` or `避免：`, its content appears once as `禁止出现：` under outer `Constraints`; when it supplied neither, no empty `禁止出现：` line appears.
- Bodies containing approved `Voiceover`, `Dialogue`, or other speech include `画面中不得生成文字、字幕或对白气泡。`
- If the body contains approved voiceover or off-screen speech, use `不得添加导演正文之外的旁白、画外解说。`; otherwise use `无旁白、无画外解说。`.
- Do not add a separate no-BGM constraint outside director `Audio` or legacy `SFX`.
- Validate the chosen Audio branch explicitly with `--audio-mode default|music|silence`; the CLI never guesses intent.
