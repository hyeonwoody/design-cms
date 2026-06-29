# PostgreSQL Field Reference

PostgreSQL-specific fields that store flexible structures without extra tables. Use
them where the token contract calls for lists or nested values.

## ArrayField

Stores a list in one column. Used for `Scenario.recommended_stack`.

```python
from django.contrib.postgres.fields import ArrayField
from django.db import models

class Scenario(models.Model):
    recommended_stack = ArrayField(models.CharField(max_length=50), default=list)
```

## JSONField

Stores arbitrary JSON. Useful for token metadata that does not deserve its own
columns. Available as `models.JSONField` on modern Django.

```python
class Token(models.Model):
    palette = models.ForeignKey("Palette", on_delete=models.CASCADE, related_name="tokens")
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    meta = models.JSONField(default=dict, blank=True)
```

## When to use which

- Flat list of strings -> `ArrayField`.
- Open-ended structured data -> `JSONField`.
- A value designers edit one-by-one -> a real column (so it shows cleanly in the admin).

Requires PostgreSQL (see `python-setup.md`). These fields do not work on SQLite.

Reference: https://docs.djangoproject.com/en/stable/ref/contrib/postgres/fields/
