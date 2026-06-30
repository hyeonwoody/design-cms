"""
Stack, UIKit, and Compatibility: the stack x UI-kit matrix (F4).

Each Compatibility row records how well one Stack pairs with one UIKit, with a level
and a short rationale.
"""
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Stack(models.Model):
    name = models.CharField(max_length=100, unique=True)

    panels = [FieldPanel("name")]

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


@register_snippet
class UIKit(models.Model):
    name = models.CharField(max_length=100, unique=True)

    panels = [FieldPanel("name")]

    class Meta:
        ordering = ["name"]
        verbose_name = "UI kit"

    def __str__(self):
        return self.name


@register_snippet
class Compatibility(models.Model):
    class Level(models.TextChoices):
        FULL = "full", "Full"
        PARTIAL = "partial", "Partial"
        NONE = "none", "None"

    stack = models.ForeignKey(
        Stack, on_delete=models.CASCADE, related_name="compatibilities"
    )
    kit = models.ForeignKey(
        UIKit, on_delete=models.CASCADE, related_name="compatibilities"
    )
    level = models.CharField(
        max_length=20, choices=Level.choices, default=Level.PARTIAL
    )
    rationale = models.TextField(blank=True)

    panels = [
        FieldPanel("stack"),
        FieldPanel("kit"),
        FieldPanel("level"),
        FieldPanel("rationale"),
    ]

    class Meta:
        ordering = ["stack__name", "kit__name"]
        verbose_name_plural = "compatibilities"
        constraints = [
            models.UniqueConstraint(
                fields=["stack", "kit"], name="unique_stack_kit_pair"
            )
        ]

    def __str__(self):
        return f"{self.stack} x {self.kit}: {self.get_level_display()}"
