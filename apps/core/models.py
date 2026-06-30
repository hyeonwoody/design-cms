"""
Reference: curated design-system and tooling links (F5), as a Wagtail snippet.
"""
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Reference(models.Model):
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    url = models.URLField()

    panels = [
        FieldPanel("category"),
        FieldPanel("title"),
        FieldPanel("url"),
    ]

    class Meta:
        ordering = ["category", "title"]

    def __str__(self):
        return self.title
