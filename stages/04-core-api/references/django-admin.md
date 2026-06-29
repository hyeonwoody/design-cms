# Django Admin as the CMS

The admin is the editing surface for designers. No separate CMS UI is built. Use this
when registering models in stage 04.

## Register a model

```python
from django.contrib import admin

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]
    search_fields = ["name"]
```

## Edit tokens inside their palette (inline)

A designer opens one palette and edits all its tokens on the same screen.

```python
class TokenInline(admin.TabularInline):
    model = Token
    extra = 1

@admin.register(Palette)
class PaletteAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_published"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["is_published"]
    inlines = [TokenInline]
```

## CMS rules

- Register every model so nothing is uneditable.
- `is_published` controls API visibility: edit in the admin, the API reflects it.
- Editing a token must change both the API response and the rendered page (audit check).

Reference: https://docs.djangoproject.com/en/stable/ref/contrib/admin/
