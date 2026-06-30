"""
Palette and Token: the design-token contract.

Palette is a Wagtail snippet so designers manage it in /admin/. Token is an inline
child of Palette (ParentalKey + Orderable), edited on the same screen via InlinePanel
and also editable inline at / through the API (F7). See
design-system/token-contract.md for the canonical shape.
"""
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet


@register_snippet
class Palette(ClusterableModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_published = models.BooleanField(
        default=False,
        help_text="Only published palettes appear in the public API.",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("is_published"),
        InlinePanel("tokens", label="Tokens"),
    ]

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Token(Orderable):
    palette = ParentalKey(
        Palette, on_delete=models.CASCADE, related_name="tokens"
    )
    key = models.CharField(
        max_length=100, help_text="Token name, e.g. color.primary or space.md"
    )
    value = models.CharField(
        max_length=200, help_text="Token value, e.g. #2563EB or 16px"
    )

    panels = [
        FieldPanel("key"),
        FieldPanel("value"),
    ]

    class Meta(Orderable.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=["palette", "key"], name="unique_token_key_per_palette"
            )
        ]

    def __str__(self):
        return f"{self.key}: {self.value}"
