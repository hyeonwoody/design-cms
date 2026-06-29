# Figma Tokens Import

How the Figma Import tab pulls design tokens out of Figma and into `Palette`/`Token`
records. Use this when building the import feature in stage 04.

## Credentials

- File key: `{{FIGMA_FILE_KEY}}` (from the Figma file URL: `figma.com/file/<KEY>/...`).
- Access token: `{{FIGMA_ACCESS_TOKEN}}` lives in `.env`, never in code or markdown.

## Endpoint

Figma exposes published variables (the modern home of design tokens):

```
GET https://api.figma.com/v1/files/{{FIGMA_FILE_KEY}}/variables/published
Header: X-Figma-Token: <token from env>
```

Color and number variables map to tokens. Variable collections map to palettes.

## Mapping to the contract

| Figma | CMS model |
|-------|-----------|
| Variable collection | `Palette` (name, slug) |
| Variable name | `Token.key` (e.g. `color/primary` -> `color.primary`) |
| Variable resolved value | `Token.value` |

## Import flow

1. Fetch published variables for `{{FIGMA_FILE_KEY}}`.
2. Upsert a `Palette` per collection (match on slug).
3. Upsert a `Token` per variable under that palette (match on key).
4. Leave `is_published` off until a designer reviews, then toggle it in the admin.

Reference: https://www.figma.com/developers/api#variables
