"""Views for the tabbed front end."""
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Single-page shell that hosts the feature tabs.

    Each tab is fetched from its DRF endpoint by the front-end JS. The Palettes tab
    becomes editable inline (F7) only when the current user holds the matching model
    change permission, the same one Wagtail enforces in /admin/.
    """

    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tabs"] = [
            {"slug": "palettes", "label": "Palettes", "endpoint": "/api/palettes/"},
            {"slug": "components", "label": "Components", "endpoint": "/api/components/"},
            {"slug": "scenarios", "label": "Scenarios", "endpoint": "/api/scenarios/"},
            {"slug": "compatibility", "label": "Compatibility", "endpoint": "/api/compatibility/"},
            {"slug": "references", "label": "References", "endpoint": "/api/references/"},
            {"slug": "figma-import", "label": "Figma Import", "endpoint": ""},
        ]
        user = self.request.user
        context["can_edit_palettes"] = user.has_perm("catalog.change_palette")
        context["can_edit_tokens"] = user.has_perm("catalog.change_token")
        return context
