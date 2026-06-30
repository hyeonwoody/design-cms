# App and Route Map: Design CMS

Turns the requirements brief into Django app boundaries and a routing plan. Built on
Wagtail (CMS admin) + DRF (API). Page routes, API routes, and the two admins stay
separate so nothing collides.

## App Boundaries

| App | Owns (models) | Serves features |
|-----|---------------|-----------------|
| `catalog` | Palette, Token | F1 palettes, F6 Figma import, F7 inline editing |
| `library` | Component, Scenario | F2 components, F3 scenarios |
| `compat` | Stack, UIKit, Compatibility | F4 compatibility matrix |
| `core` | Reference + page shell | F5 references, tabbed UI host |
| `home` | Wagtail page tree | Wagtail page serving (fallback) |

Every admin-editable entity belongs to exactly one app (no shared ownership).

## Route Table

Top-level prefixes are mutually exclusive.

| Path | Handler | Purpose |
|------|---------|---------|
| `/` | `apps.core` (IndexView) | Tabbed UI shell |
| `/admin/` | Wagtail admin | CMS designers use to edit everything |
| `/django-admin/` | Django admin | Superuser/user management |
| `/api/` | DRF router | Data the tabs read (and write for F7) |
| `/documents/` | Wagtail documents | Document serving |
| `/<anything-else>/` | Wagtail page serving | Catch-all, registered last |

## API Routes

Read endpoints (anonymous, published records only):

| Endpoint | Method | Returns |
|----------|--------|---------|
| `/api/palettes/` | GET | Published palettes with nested tokens |
| `/api/palettes/{slug}/` | GET | One palette |
| `/api/components/` | GET | Components by category |
| `/api/scenarios/` | GET | Scenarios with recommended stacks |
| `/api/compatibility/` | GET | Stack x UI-kit matrix |
| `/api/references/` | GET | Reference links |

Write endpoints for **F7 inline palette editing** (permitted users, from `/` itself):

| Endpoint | Method | Action |
|----------|--------|--------|
| `/api/palettes/{slug}/` | PATCH | Update palette fields (e.g. name, is_published) |
| `/api/tokens/{id}/` | PATCH | Update a token value inline from the Palettes tab |

- Permission: `DjangoModelPermissionsOrAnonReadOnly`. Anonymous users get GET only;
  a user may PATCH only if they hold the model's `change` permission
  (`catalog.change_palette`, `catalog.change_token`). This is the **same** permission
  Wagtail checks in `/admin/`, so the set of people who can edit is identical, just
  not confined to the admin UI. Writes use the session + CSRF token, no API key.
- **Editing happens at `/`, not only `/admin/`.** The Palettes tab renders inline edit
  controls when, and only when, the current user passes the same permission check.
  The page view exposes this to the template/JS:

  | Context flag | Source | Effect on the Palettes tab |
  |--------------|--------|----------------------------|
  | `can_edit_palettes` | `request.user.has_perm("catalog.change_palette")` | Show/hide palette edit controls |
  | `can_edit_tokens` | `request.user.has_perm("catalog.change_token")` | Show/hide inline token-value editing |

  Permitted users edit colors inline and the JS PATCHes the API; everyone else sees a
  read-only view. The same Palette/Token records back both `/` and `/admin/`, so edits
  stay consistent wherever they are made.

## Tab Navigation Model

Single-page shell at `/`; one anchor per tab (no separate page reload). Tab set is
locked in `design-system/tab-model.md` (six tabs).

| Tab | Anchor | Reads | Writes (F7) |
|-----|--------|-------|-------------|
| Palettes | `#palettes` | `/api/palettes/` | PATCH `/api/palettes/{slug}/`, `/api/tokens/{id}/` |
| Components | `#components` | `/api/components/` | - |
| Scenarios | `#scenarios` | `/api/scenarios/` | - |
| Compatibility | `#compatibility` | `/api/compatibility/` | - |
| References | `#references` | `/api/references/` | - |
| Figma Import | `#figma-import` | triggers import action | writes via import, not inline |

## Audit

| Check | Result |
|-------|--------|
| Route separation | PASS - `/`, `/admin/`, `/django-admin/`, `/api/`, `/documents/` do not overlap; Wagtail catch-all is registered last |
| Tab coverage | PASS - all six tabs have a home anchor and a backing endpoint |
| Entity coverage | PASS - each of the 8 entities belongs to exactly one app |

## Handoff to Stage 03 (Domain Modeling)

Model the 8 entities as Wagtail snippets in their apps. F7 requires that Palette and
Token serializers expose writable fields, that the viewsets allow PATCH under
`DjangoModelPermissionsOrAnonReadOnly`, and that the Palettes tab view passes
`can_edit_palettes` / `can_edit_tokens` (from `request.user.has_perm(...)`) to the
template so inline editing surfaces at `/` for permitted users.
