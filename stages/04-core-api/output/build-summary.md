# Build Summary: Core API

The working application. The source tree at the project root is the real output
(`apps/`, `config/`, `templates/`, `static/`); this file records what was built and
the audit. Built on Wagtail (CMS) + DRF (API) per the Stage 02/03 decisions.

## What was built

### CMS surface (Wagtail, not Django admin)
All eight models are `@register_snippet`, so designers edit them at `/admin/`. Token
is an inline (`InlinePanel`) under Palette. This replaces the "Django Admin as CMS"
note in the original contract; the editing surface is Wagtail.

### DRF API (`/api/`)
| Endpoint | Methods | Notes |
|----------|---------|-------|
| `/api/palettes/` `/api/palettes/{slug}/` | GET, PATCH | Published-only for anonymous; drafts visible to editors |
| `/api/tokens/{id}/` | GET, PATCH | F7 inline token editing |
| `/api/components/` | GET | Read-only |
| `/api/scenarios/` | GET | Read-only |
| `/api/compatibility/` | GET | Read-only; stack/kit names + level label |
| `/api/references/` | GET | Read-only |
| `/api/figma/import/` | POST | Triggers Figma import; requires `catalog.change_palette` |

Permission: `DjangoModelPermissionsOrAnonReadOnly` on the writable viewsets, so write
access maps to the same `catalog.change_*` permission Wagtail enforces.

### Figma import (F6)
`apps/catalog/figma.py` fetches published Figma variables (stdlib `urllib`, no new
dependency), maps variable collections to palettes and variables to tokens, and
upserts. Runnable two ways: `python manage.py import_figma` or the Figma Import tab
(POST endpoint). Imported palettes start unpublished for review.

### Tabbed front end (F1-F7)
`apps/core` `IndexView` renders six tabs; `static/js/app.js` lazy-loads each tab from
its endpoint. The Palettes tab shows editable token inputs (which PATCH the API) only
when the user has the edit permission, surfaced via `can_edit_palettes` /
`can_edit_tokens`. F7 editing happens at `/`, not only `/admin/`.

## Audit

| Check | Result |
|-------|--------|
| Admin coverage | PASS - all 8 models registered as Wagtail snippets |
| API integrity | PASS - endpoints serialize; anonymous palettes are published-only (verified) |
| CMS round-trip | PASS - PATCH updates the token value and the same record backs `/admin/` and the API (verified PATCH 200, value changed) |
| Tab reachability | PASS - all six tabs render and load from the base template |
| Figma import | PASS (logic) - import command and endpoint implemented and registered; needs live `FIGMA_FILE_KEY`/`FIGMA_ACCESS_TOKEN` to exercise end-to-end |
| Static serving | PASS - `collectstatic` ran under WhiteNoise (242 files, post-processed) |

Smoke tests confirmed: anonymous sees published palettes only and is blocked from
PATCH (403); an editor with `change_token` PATCHes successfully (200) and sees drafts.

## Design-token model + live updates (K-Design POC reference)

Modeled on https://k-design-studio.netlify.app/poc/design:
- **Six color tokens per palette** (`color.background/foreground/muted/card/border/accent`)
  documented in `design-system/token-contract.md`.
- **Reference palettes** seeded by `python manage.py seed_palettes` (theme-matched
  starting points; see the command for the current set). Also dumped to
  `fixtures/palettes.json`.
- **Palette switcher + live preview**: the Palettes tab applies the active palette's
  tokens as CSS variables, so switching re-themes the preview instantly (POC behavior).
- **Cross-user live updates**: the Palettes tab polls `/api/palettes/` every 10s and
  re-renders when the data changes (skipping re-render while an input is focused, so it
  never clobbers an in-progress edit). When an admin publishes a new palette in Wagtail,
  other users see it within the poll interval without reloading. Drafts remain visible
  only to editors. (Upgrade path for instant push: Django Channels websockets.)

## Handoff to Stage 05 (Documentation)

Document install/run (Docker DB + venv app), the route map, the ERD, the tab UI, the
Figma flow, and the permission model. Remaining nice-to-haves: pagination on list
endpoints, an admin widget check for `Scenario.recommended_stack`, and seed fixtures.
