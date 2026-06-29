# Shared Constants

Fixed values that templates and code import from one place (Pattern 15). These are
constants, not design tokens: design tokens live in the database and are edited in
the CMS. The values here do not change per palette.

## Spacing

- Baseline unit: 4px
- Scale: 4, 8, 12, 16, 24, 32, 48, 64

## Contrast thresholds

- AA: contrast ratio >= 4.5
- AAA: contrast ratio >= 7

## Layout

- Max content width: 1200px
- Tab bar position: top, sticky

## Project

- API base path: `{{API_BASE_PATH}}`
- Database name: `{{DB_NAME}}`

Change a value here once and every template/view that imports it updates.
