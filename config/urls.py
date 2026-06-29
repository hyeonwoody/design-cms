"""
Root URL configuration.

Route layout (kept separate so the tabbed pages and the API never collide):
  /django-admin/  Django admin (superuser management)
  /admin/         Wagtail admin (the CMS designers use)
  /documents/     Wagtail document serving
  /api/           DRF API consumed by the tabbed front end
  /               Project pages (apps.core), then Wagtail page serving as fallback
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

# Register DRF viewsets here as the catalog/library/compat apps gain models.
router = DefaultRouter()

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("api/", include(router.urls)),
    path("", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Wagtail's page-serving catch-all must come last.
urlpatterns += [
    path("", include(wagtail_urls)),
]
