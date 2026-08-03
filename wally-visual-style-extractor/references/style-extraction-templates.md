# Elastic Style Extraction Templates

Select one smallest matching artifact. Within it, preserve the exact field labels below, keep populated fields in listed relative order, and delete every field, subsection, list, or JSON key that has no evidence or current task value. Do not translate, rename, bold, or replace labels, and do not invent extra headings. Never output an empty placeholder, a standalone `无` or `不适用` value, or filler guessed only to complete the structure.

Keep one fact in one owning field. Use `Uncertainties` only when evidence limits materially affect the answer. Return only the selected artifact without a preface or appendix; do not flatten it into free prose.

For every canonical or supporting established term that affects the result, give a direct source URL or a precise offline source note, explain its direct relevance, and state match strength. When lookup is unavailable or sources are insufficient, do not confirm the term from memory. Use `Canonical match: none confirmed` in `Style Lookup Result`, or the matching canonical-status field in another selected artifact, and disclose the evidence limit in `Uncertainties`.

## Style Lookup Result

Use for a style-name, classification, or established-term query without full system extraction.

Begin with `Query:` and use only the populated labels from this block exactly as written.

```text
Query:
Canonical match:
Supporting established terms:
Medium or genre:
Descriptive modifiers, not style names:
Sources:
- [Established term — direct source URL or precise offline source note — direct relevance — match strength.]
Match strength: [Overall classification strength; each term keeps its own strength in Sources.]
Rejected near-matches:
Working description (non-canonical):
Uncertainties:
```

When no exact term is confirmed, `Canonical match: none confirmed` is a substantive result, not an empty value. Include closest sourced terms when available. Use `Working description (non-canonical)` only for unmatched wording that helps the user; never promote it to an established style.

## Analysis Card

Use for a complete evidence-backed extraction. Omit whole sections that do not carry distinct information.

```text
Style name:
Working description (non-canonical):
Canonical status:
Established-style lookup:
- Candidate term:
- Source:
- Match strength:
- Rejected near-match:
Classification:
- Parent style or movement:
- Supporting established styles:
- Medium or genre:
- Descriptive modifiers, not style names:
Source samples:
Style thesis:

Stage 1 - Constraint extraction:
- What the references refuse:
- Immutable conditions:
- Single-image content to ignore:

Stage 2 - Sample purification:
- Cross-sample commonalities:
- Accidental details removed:

Stage 3 - Style system:
- Space / composition:
- Light / atmosphere:
- Color / texture:

Keep:
- [Stable repeated choice.]

Avoid:
- [Excluded or suppressed trait.]

Degrees of freedom:
- Flexible:
- Fixed:

Evidence strength:
- Strong:
- Provisional:

Uncertainties:
```

Use either `Style name` or `Working description (non-canonical)` according to the lookup result. The top-level `Evidence strength` block is the only owner of evidence confidence. Do not repeat Keep/Avoid rules inside the Stage 3 blocks.

## Three-Stage Brief

Use when the user wants the extraction summarized through its three stages rather than a full card.

```text
Constraint extraction:
- [Absent, rejected, muted, or non-negotiable traits supported by evidence.]

Sample purification:
- [Cross-sample repeated choices after subject-specific noise is removed.]

System building:
- Space / composition:
- Light / atmosphere:
- Color / texture:
- Rules / constraints:

Uncertainties:
```

If only one stage has substantive content, output only that stage. If one sample limits purification, disclose that under `Uncertainties`; do not invent cross-sample evidence.

## Reusable JSON Prompt

Use for a reusable style-layer generation template. Keep valid JSON and preserve the relative key order below, but omit every irrelevant key and empty container. Placeholder values are allowed only when the user requests a reusable template whose purpose is to be filled later. Copy `subject`, `scene`, and `camera` from user-provided material or leave fillable placeholders; do not author missing story action, production design, shot design, camera setup, or camera movement. Repeated style evidence may populate `composition` and style-rule fields, but it does not authorize filling those three protected keys.

```json
{
  "classification": {
    "canonical_status": "<established | composite | no_confirmed_exact_match>",
    "parent_style": "<documented style or movement>",
    "supporting_styles": ["<documented style, genre, or aesthetic>"],
    "descriptive_modifiers": ["<visible trait, not a claimed style name>"],
    "sources": [
      {
        "term": "<canonical or supporting established term>",
        "source": "<direct source URL or precise offline source note>",
        "relevance": "<direct relevance to the supplied evidence>",
        "match_strength": "<strong | moderate | weak>"
      }
    ],
    "match_strength": "<overall classification strength: strong | moderate | weak>"
  },
  "subject": "<user-supplied subject and action, or reusable placeholder>",
  "scene": "<user-supplied setting, or reusable placeholder>",
  "composition": "<subject position, viewing order, density, negative space>",
  "camera": "<user-supplied camera value, or reusable placeholder>",
  "lighting": {
    "source": "<where light comes from>",
    "target": "<what it illuminates>",
    "shadow": "<where shadows fall>",
    "ratio": "<contrast or light ratio>",
    "temperature": "<warm/cool/mixed>"
  },
  "color_palette": ["#HEX1", "#HEX2", "#HEX3"],
  "materials": "<surface qualities, grain, reflections, roughness>",
  "environment_language": "<architecture, props, cultural or brand cues>",
  "style_rules": {
    "keep": ["<stable repeated choice>"],
    "avoid": ["<excluded trait or model default>"]
  },
  "rendering": "<finish, texture, fidelity, sharpness>",
  "constraints": "<style and quality boundaries not already owned above>",
  "uncertainties": ["<material evidence limit>"]
}
```

When the user specifies a different schema, preserve that schema and apply the same omission rule. Do not wrap it in an additional Analysis Card.

## Transfer Validation

Use when testing whether a style system survives a different subject or context.

```text
New subject:
Expected style signals:
Rules that must survive:
Rules that may flex:
Likely failure modes:
Observed transfer result:
Corrections if it drifts:
Uncertainties:
```

Output only fields supported by the proposed or observed test. Do not claim an observed result before a generated sample exists.

## Common failure modes

- Inventing a polished-sounding style name before checking established vocabularies.
- Treating a descriptive phrase, `-ism`, `-core`, or hybrid label as established without sources.
- Forcing one label when a combination of existing styles is more accurate.
- Calling a near-match canonical while ignoring defining features it lacks.
- Copying subject matter instead of extracting repeatable choices.
- Using one image as proof of a whole style.
- Keeping abstract adjectives without translating them into visible controls.
- Duplicating the same rule across multiple fields or artifacts.
- Filling every template field despite missing evidence.
- Over-constraining every dimension and removing useful variation.
