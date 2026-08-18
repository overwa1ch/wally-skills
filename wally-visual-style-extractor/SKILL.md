---
name: wally-visual-style-extractor
description: "Identify established visual styles and extract reusable style systems from any user-provided material, format, stage, or combination, including reference images, moodboards, generated outputs, videos, brand materials, and craft notes. Use to name or classify a visual style, research established art/design/film/internet-aesthetic terms, avoid unsupported style names, analyze references, create reusable style rules or style-layer prompt/JSON templates, define keep/avoid constraints, compare samples, and validate transfer. Trigger from professional visual-style analysis or extraction intent; explicit wally mention is not required. Produce only visual-style lookup, analysis, reusable style controls, and transfer validation, not asset designs, storyboards, action or performance design, dialogue, audio, timing, or final image/video prompts."
---

# Wally Visual Style Extractor

Current version: `wally-visual-style-extractor@2026-07-22-v1.6-boundary-evidence-ownership` (keeps visual-style work separate from asset, shot, action, audio, and final-prompt design; one top-level Evidence strength block owns evidence confidence). | v1.5 choose the smallest matching structured artifact and output only evidence-backed or task-required fields. | v1.4 every deliverable uses the matching structured template. | v1.3 professional-intent-trigger. | v1.2 wally-only-trigger superseded. | v1.1 existing-style-lookup-first.

## Core Principle

Treat style as repeated choices, not as a prompt string. Map those choices to established styles before naming anything new. Most references recombine existing movements, genres, design languages, or internet aesthetics.

## Route from the user's actual materials

- Accept prose, scripts, tables, images, videos, moodboards, reference boards, generated samples, brand materials, platform links, partial analyses, contradictory labels, or any mixture.
- Inspect supplied visual references before relying on their captions or claimed style names. Distinguish visible evidence, user decisions, provisional inference, source claims, and material conflicts.
- Do not require an upstream artifact, schema, approval state, identifier system, fixed sample count, or fixed starting stage.
- When a link or source cannot be accessed, state that evidence limit. Continue with the usable material and keep unsupported conclusions provisional.

## Stage 0: Existing-Style Lookup

Before assigning a style name:

1. Search existing art, design, photography, architecture, film, fashion, subculture, and internet-aesthetic vocabularies.
2. Prefer museums, archives, professional bodies, scholarship, and established aesthetic indexes. Record a direct source URL or precise offline source note, its direct relevance, and match strength for each established term that affects the result.
3. Separate the canonical style or movement from supporting styles, medium or genre, period cues, and descriptive modifiers.
4. Use a combination of established terms when no single term covers the reference.

Do not turn a descriptive phrase into a canonical style name. Do not confirm a canonical or supporting established term from unaided memory when lookup is unavailable or the sources do not support it. In `Style Lookup Result`, report `Canonical match: none confirmed`; in another selected artifact, use its matching canonical-status field. Disclose the limitation in `Uncertainties` and give sourced near-matches when available. Coin a new name only when the user explicitly asks for naming or branding. Otherwise label unmatched wording as a non-canonical working description.

## Three-Stage Extraction Workflow

### 1. Constraint Extraction

Start by asking what the reference refuses. Identify exclusions, suppressed traits, and immutable conditions. If removing a condition would break the style, treat it as a core constraint.

Avoid describing only semantic content. A subject, prop, costume, or location is not a style rule unless it survives across unrelated samples.

### 2. Sample Purification

Use multiple same-style, different-content samples when possible. Compare them to remove accidental content and isolate repeated visual choices.

If only one sample exists, label conclusions as provisional and separate likely style rules from single-image artifacts.

### 3. System Building

Translate constraints and commonalities into a reusable style guide with four default blocks:

- Space and composition: scale, horizon, density, subject size, negative space.
- Light and atmosphere: source, direction, shadow, practical light, haze, dust, fog, snow, air clarity.
- Color and texture: palette, saturation, contrast, grain, surface finish, material age.
- Rules and constraints: keep rules, avoid rules, prompt order, negative prompt.

Validate by transfer. Apply the system to a new subject; if it only works on the original content, it is still copying rather than extracting style.

## Artifact routing

Choose the smallest artifact that directly answers the request:

- Style name or classification lookup only: `Style Lookup Result`.
- Full evidence-backed extraction: `Analysis Card`.
- Concise explanation of the extraction stages: `Three-Stage Brief`.
- Reusable style-layer generation structure: `Reusable JSON Prompt`, or the user's specified structure.
- Cross-subject portability test: `Transfer Validation`.

Do not append the other artifacts unless requested. Read `references/style-extraction-templates.md`, use the matching structure, and keep its populated fields in relative order. Preserve the selected template's exact field labels; do not translate, rename, bold, or replace them with improvised headings.

`Reusable JSON Prompt` remains a style-layer artifact. Copy `subject`, `scene`, and `camera` values from the user's material or leave reusable placeholders when the user asks for a fillable template; do not author missing story action, production design, shot design, camera setup, or camera movement. Repeated composition or camera evidence may be recorded in the owning style-analysis or style-rule fields, but it does not authorize filling those three JSON keys.

Within the selected artifact:

- Output a field only when evidence exists or the current task genuinely needs it.
- Omit empty headings, empty lists, empty JSON keys, standalone `无` or `不适用` values, and filler inferred only to complete the template. Preserve a placeholder only when the user explicitly requests a reusable fillable template.
- Keep each fact in one owning field; do not restate the same rule across classification, stages, Keep, Avoid, and validation.
- When insufficient evidence matters, state it in `Uncertainties` instead of inventing a conclusion.
- Stay structured; do not flatten the artifact into free prose.
- Return only the selected artifact. Do not add a preface, recommendation section, search-query appendix, or another heading outside its fields.

When lookup finds no exact established term, report that as a substantive classification result, give the closest sourced terms when available, and label any unmatched wording `Working description (non-canonical)`. Never present a working description as an established style.

## Prompting Guidance

When the user requests a reusable fillable generation structure, order user-supplied values or placeholders with concrete controls before abstract descriptors:

```text
[subject and action] + [scene] + [lighting] + [camera/composition/materials] + [style micro-adjustment] + [avoid constraints]
```

Do not let words like cinematic, premium, dreamy, authentic, gritty, or editorial stand alone. Translate them into visible choices.

Likewise, do not convert a visible-choice summary into a new `-ism`, `-core`, movement, genre, or aesthetic label without documented prior usage.

## Boundaries

- Own established-style lookup, classification, reference analysis, reusable visual rules, style-layer prompt or JSON structures, Keep/Avoid constraints, and transfer validation.
- Record composition, lens, or camera tendencies only when they repeat across the evidence or the user supplies them as fixed values. Do not design a shot sequence, camera path, timing plan, action, performance, dialogue, or audio.
- Do not design static-asset identities, asset-sheet geometry, storyboards, director scripts, or final image-to-video or text-to-video prompts.
- For mixed cross-module requests, return only the requested visual-style artifact and leave the remaining work to its specialist; do not append or assemble another product. If a request contains no visual-style product, name the matching specialist and stop.

## References

For every deliverable, read `references/style-extraction-templates.md` and use only the smallest matching structured template.
