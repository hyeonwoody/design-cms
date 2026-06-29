# DRF Serializers and ViewSets

How to expose models as the API the tabs consume. Use this when building the API
layer in stage 04.

## Serializer

Turns a model into JSON. Nest tokens inside their palette so the front end gets a
palette and its tokens in one request.

```python
from rest_framework import serializers

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["key", "value"]

class PaletteSerializer(serializers.ModelSerializer):
    tokens = TokenSerializer(many=True, read_only=True)
    class Meta:
        model = Palette
        fields = ["name", "slug", "is_published", "tokens"]
```

## ViewSet

Read-only is enough: the admin edits, the API serves. Only show published palettes.

```python
from rest_framework import viewsets

class PaletteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaletteSerializer
    def get_queryset(self):
        return Palette.objects.filter(is_published=True).prefetch_related("tokens")
```

## Router

```python
router.register("palettes", PaletteViewSet, basename="palette")
# served under {{API_BASE_PATH}}
```

## Endpoints to build

`{{API_BASE_PATH}}palettes/`, `palettes/{slug}/`, `scenarios/`, `compatibility/`.

Reference: https://www.django-rest-framework.org/api-guide/viewsets/
