# Django Routing Reference

How to split page routes (MVT) from API routes (DRF) so the tabbed UI and the API do
not collide. Use this when drawing the route table in discovery.

## Page routes (MVT)

Defined in each app's `urls.py`, included from `config/urls.py`. The tabbed UI lives
under `/`. Each tab is either its own path or an anchor on the single page.

```python
# config/urls.py
urlpatterns = [
    path("", include("apps.core.urls")),       # tabbed pages
    path("api/", include(api_router.urls)),      # DRF API
    path("admin/", admin.site.urls),             # CMS
]
```

## API routes (DRF)

Built with a router so endpoints are consistent:

```python
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("palettes", PaletteViewSet)
router.register("scenarios", ScenarioViewSet)
# -> /api/palettes/, /api/scenarios/, ...
```

## Rules for the route map

- Page routes and API routes never share a prefix. API lives under `{{API_BASE_PATH}}`.
- Every tab in `design-system/tab-model.md` gets one home route.
- The admin (`/admin/`) is the CMS; do not build a second editing UI.

Reference: https://docs.djangoproject.com/en/stable/topics/http/urls/
