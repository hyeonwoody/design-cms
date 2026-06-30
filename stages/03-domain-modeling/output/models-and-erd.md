# Models and ERD: Design CMS

The domain model for the eight entities, implemented as Wagtail snippets across the
four apps. These models are the canonical design-token contract; later changes happen
only through migrations. Implemented in `apps/*/models.py`; migrations applied.

## Entity-Relationship Diagram

```
catalog
  Palette (1) -----< (many) Token
    name                      key
    slug (unique)             value
    is_published              [unique: (palette, key)]

library
  Component                 Scenario
    category                  title
    name                      description
    markup                    recommended_stack : text[]  (ArrayField)

compat
  Stack (1) ----<            >---- (1) UIKit
              Compatibility
                stack  (FK -> Stack)
                kit    (FK -> UIKit)
                level  (full | partial | none)
                rationale
                [unique: (stack, kit)]

core
  Reference
    category
    title
    url
```

## Models by App

| App | Model | Key fields | Notes |
|-----|-------|-----------|-------|
| catalog | `Palette` | name, slug (unique), is_published | `ClusterableModel` snippet; `InlinePanel` edits tokens |
| catalog | `Token` | palette (ParentalKey), key, value | `Orderable` child; unique (palette, key) |
| library | `Component` | category, name, markup | snippet |
| library | `Scenario` | title, description, recommended_stack | `recommended_stack` is a Postgres `ArrayField` of names |
| compat | `Stack` | name (unique) | snippet |
| compat | `UIKit` | name (unique) | snippet |
| compat | `Compatibility` | stack (FK), kit (FK), level, rationale | unique (stack, kit); level is a `TextChoices` |
| core | `Reference` | category, title, url | snippet |

## Contract Fidelity

Palette and Token match `design-system/token-contract.md` exactly:
Palette(name, slug, is_published) and Token(palette, key, value). Token adds a unique
constraint on (palette, key) so a key is unambiguous within a palette, which the
inline editor (F7) relies on when patching a value.

## Wagtail / F7 Notes

- All eight models are `@register_snippet`, so they are editable in `/admin/`.
- Palette is a `ClusterableModel` and Token an `Orderable` `ParentalKey` child, so
  tokens are edited inline under their palette (one screen).
- For F7 (inline editing at `/`), Stage 04 exposes writable serializers for Palette
  and Token and allows PATCH under `DjangoModelPermissionsOrAnonReadOnly` (the same
  `catalog.change_*` permission Wagtail enforces).

## Migration Plan

| App | Migration | Creates |
|-----|-----------|---------|
| catalog | `0001_initial` | Palette, Token |
| compat | `0001_initial` | Stack, UIKit, Compatibility |
| core | `0001_initial` | Reference |
| library | `0001_initial` | Component, Scenario |

Applied with `python manage.py migrate`. ArrayField requires PostgreSQL (in use).

## Audit

| Check | Result |
|-------|--------|
| Entity coverage | PASS - all 8 variable-data types from Stage 01 have a model |
| Contract fidelity | PASS - Palette/Token fields match the token contract |
| Migration validity | PASS - `makemigrations`/`migrate` ran cleanly; `check` reports 0 issues; all 8 tables verified present |

## Handoff to Stage 04 (Core API)

Build serializers + viewsets for each model under `/api/`, register snippets (done),
wire the Palettes tab to read/write via the API, and implement the Figma import. Note:
the `Scenario.recommended_stack` ArrayField needs a usable admin widget
(`SimpleArrayField`) and a list field in its serializer.
