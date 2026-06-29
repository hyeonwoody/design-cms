"""Views for the tabbed front end."""
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Single-page shell that hosts the feature tabs.

    Skeleton: renders the tab bar from a static list. Stage 04 wires each tab to live
    data fetched from the DRF API.
    """

    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tabs"] = [
            {"slug": "palettes", "label": "Palettes"},
            {"slug": "components", "label": "Components"},
            {"slug": "scenarios", "label": "Scenarios"},
            {"slug": "compatibility", "label": "Compatibility"},
            {"slug": "references", "label": "References"},
            {"slug": "figma-import", "label": "Figma Import"},
        ]
        return context
