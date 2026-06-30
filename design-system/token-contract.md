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

## Color token convention

Modeled on the K-Design POC (https://k-design-studio.netlify.app/poc/design). Each
palette defines the same six color tokens, so swapping palettes re-themes the UI
instantly (the front end applies them as CSS variables):

| Token key | Role |
|-----------|------|
| `color.background` | Primary surface |
| `color.foreground` | Primary text |
| `color.muted` | Secondary text / borders |
| `color.card` | Elevated surface |
| `color.border` | Divider color |
| `color.accent` | Interactive highlight |

The reference palettes are seeded by `python manage.py seed_palettes` (see the command
for the current set) as theme-matched starting points to refine. Spacing is the fixed
4px scale in `shared/constants.md`, not a per-palette token.

## Source of values

The starting token set is seeded from the nine reference palettes above, and can also
be imported from Figma file `{{FIGMA_FILE_KEY}}`. See
`stages/04-core-api/references/figma-tokens-api.md` for the import mapping.

## Accessibility

Color tokens must meet the contrast thresholds in
`stages/01-research/references/wcag-contrast.md` (AA >= 4.5, AAA >= 7).
