# Design Token Contract

The canonical schema for palettes and tokens. The Django models in stage 03 are the
authoritative implementation of this contract; this file describes the shape they
must satisfy. Change the shape here and in the models together (via migration).

## Palette

A named, publishable group of tokens.

| Field | Meaning |
|-------|---------|
| name | Human-readable palette name |
| slug | URL-safe identifier |
| is_published | Only published palettes appear in the API |

## Token

A single design value belonging to a palette.

| Field | Meaning |
|-------|---------|
| palette | The palette this token belongs to |
| key | Token name (e.g. `color.primary`, `space.md`) |
| value | Token value (hex, size, etc.) |

## Source of values

The starting token set comes from `{{PALETTE_SET}}`, imported from Figma file
`{{FIGMA_FILE_KEY}}`. See `stages/04-core-api/references/figma-tokens-api.md` for the
import mapping.

## Accessibility

Color tokens must meet the contrast thresholds in
`stages/01-research/references/wcag-contrast.md` (AA >= 4.5, AAA >= 7).
