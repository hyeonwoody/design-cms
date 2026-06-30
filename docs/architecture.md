# Architecture: Design CMS

How the app is put together: the data model, the apps, the routes, the tabbed UI,
the permission model, and the Figma sync flow.

## Stack

| Layer | Choice |
|-------|--------|
| Language | Python 3.11 |
| Web framework | Django 5.1 |
| CMS | Wagtail 6.4 (admin + snippets) |
| API | Django REST Framework 3.17 |
| Database | PostgreSQL 16 (in Docker) |
| Static files | WhiteNoise |
| Server | Gunicorn (production) |

The database runs in Docker (`docker-compose.yml`); the Django app runs locally in a
virtualenv during development.

## Apps

| App | Owns | Responsibility |
|-----|------|----------------|
| `apps.catalog` | Palette, Token | Design tokens; Figma import; inline editing (F7) |
| `apps.library` | Component, Scenario | Component gallery; usage scenarios |
| `apps.compat` | Stack, UIKit, Compatibility | Stack x UI-kit matrix |
| `apps.core` | Reference + IndexView | Reference links; tabbed UI shell |
| `apps.home` | Wagtail page tree | Page serving fallback |

All domain models are Wagtail snippets (`@register_snippet`), so designers edit them
in the Wagtail admin without any custom CRUD screens.

## ERD

```
catalog.Palette (1) ----< catalog.Token (many)
  name                      key
  slug (unique)             value
  is_published              [unique: (palette, key)]   Token is an Orderable child
                                                        (ParentalKey) edited inline
library.Component           library.Scenario
  category                    title
  name                        description
  markup                      recommended_stack : text[] (ArrayField)

compat.Stack (1) ----<                >---- (1) compat.UIKit
                  compat.Compatibility
                    stack (FK)  kit (FK)
                    level (full | partial | none)
                    rationale
                    [unique: (stack, kit)]

core.Reference
  category  title  url
```

The design-token contract (Palette + Token) is canonical; see
`../design-system/token-contract.md`. Each palette carries the six color tokens
`color.background/foreground/muted/card/border/accent`.

## Routing

Top-level prefixes are mutually exclusive (`config/urls.py`):

| Path | Handler | Purpose |
|------|---------|---------|
| `/` | `apps.core.IndexView` | Tabbed UI shell |
| `/admin/` | Wagtail | CMS designers use |
| `/django-admin/` | Django admin | Superuser/user management |
| `/api/...` | DRF router | Data for the tabs (read + F7 write) |
| `/api/figma/import/` | `FigmaImportView` | Trigger a Figma token import |
| `/documents/` | Wagtail documents | Document serving |
| (anything else) | Wagtail page serving | Catch-all, registered last |

### API endpoints

`GET /api/{palettes,tokens,components,scenarios,compatibility,references}/`
plus `PATCH /api/palettes/{slug}/` and `PATCH /api/tokens/{id}/` for inline editing.
Anonymous responses include published palettes only.

## Tabbed UI

`IndexView` renders six tabs (Palettes, Components, Scenarios, Compatibility,
References, Figma Import). `static/js/app.js` lazy-loads each tab from its endpoint.

- **Palettes tab** mirrors the design POC: a palette switcher applies the active
  palette's six tokens as CSS variables, instantly re-theming a live preview.
- **Live updates**: the Palettes tab polls `/api/palettes/` every 10s and re-renders
  when the data changes, so a palette published by one admin appears for other users
  without a reload. It skips re-rendering while a token input is focused.

## Permission model (F7 inline editing)

The writable viewsets use DRF's `DjangoModelPermissionsOrAnonReadOnly`:

- Anonymous and unprivileged users: read-only (published palettes only).
- A user with `catalog.change_palette` / `catalog.change_token` can `PATCH` from the
  front end. This is the same permission Wagtail enforces in `/admin/`, so the set of
  editors is identical, just not confined to the admin UI.

The front end surfaces edit controls only when `IndexView` passes `can_edit_palettes`
/ `can_edit_tokens` (from `request.user.has_perm(...)`).

## Figma sync flow

1. A user with palette edit permission opens the Figma Import tab and clicks import
   (or runs `python manage.py import_figma`).
2. `apps/catalog/figma.py` fetches published variables from
   `https://api.figma.com/v1/files/{FIGMA_FILE_KEY}/variables/published`
   (token from `FIGMA_ACCESS_TOKEN` in `.env`, never in code).
3. Variable collections map to palettes (by slug); variables map to tokens (by key,
   `color/primary` -> `color.primary`); color values resolve to hex.
4. Imported palettes start unpublished so a designer reviews them before they go live.

## Deployment notes

- Settings split: `config/settings/base.py` + `prod.py` (security headers, HTTPS).
- `python manage.py collectstatic` then serve via WhiteNoise.
- Run under Gunicorn: `gunicorn config.wsgi`.
- Set `DEBUG=False`, a real `SECRET_KEY`, and `ALLOWED_HOSTS` in production.
