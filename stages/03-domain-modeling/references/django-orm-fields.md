# Django ORM Field Reference

Common model fields for this project. Use it when writing `models.py` so the schema
matches the token contract.

## Field types used here

| Field | Use for |
|-------|---------|
| `CharField(max_length=...)` | names, keys, short values |
| `SlugField` | URL-safe identifiers (palette slug) |
| `TextField` | component markup, long descriptions |
| `BooleanField` | `is_published` flags |
| `URLField` | reference links |
| `ForeignKey(..., on_delete=...)` | token -> palette, compatibility -> stack/kit |

## Relationships in this domain

- `Token` has a `ForeignKey` to `Palette` (a palette has many tokens).
- `Compatibility` has `ForeignKey`s to both `Stack` and `UIKit`.
- `Scenario.recommended_stack` uses an array (see `postgres-fields.md`).

## Conventions

- Add `__str__` to every model so the admin shows readable labels.
- Use `slug` for anything that appears in a URL.
- Schema is the contract: after stage 03, change it only through migrations.

Reference: https://docs.djangoproject.com/en/stable/ref/models/fields/
