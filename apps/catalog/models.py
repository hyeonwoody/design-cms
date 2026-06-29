"""
Palette and Token live here (the design-token contract).

Skeleton: models deferred to Stage 03 (domain-modeling). In the Wagtail build they
become @register_snippet models so designers edit them in the Wagtail admin, with
Token managed inline under Palette.
"""
# from wagtail.snippets.models import register_snippet
#
# @register_snippet
# class Palette(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True)
#     is_published = models.BooleanField(default=False)
#
# class Token(models.Model):
#     palette = models.ForeignKey(Palette, on_delete=models.CASCADE, related_name="tokens")
#     key = models.CharField(max_length=100)
#     value = models.CharField(max_length=200)
