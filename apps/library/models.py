"""
Component and Scenario, registered as Wagtail snippets.

Component holds reusable markup grouped by category (F2). Scenario describes a usage
situation and a recommended stack as a list of names (F3).
"""
from django.contrib.postgres.fields import ArrayField
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Component(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    markup = models.TextField(help_text="HTML markup for the component.")

    panels = [
        FieldPanel("category"),
        FieldPanel("name"),
        FieldPanel("markup"),
    ]

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.category} / {self.name}"


@register_snippet
class Scenario(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    recommended_stack = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text="Ordered list of recommended stack names.",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("recommended_stack"),
    ]

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
