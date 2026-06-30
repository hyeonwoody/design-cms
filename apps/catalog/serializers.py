from rest_framework import serializers

from .models import Palette, Token


class TokenSerializer(serializers.ModelSerializer):
    """Read and inline-edit (F7) a single token."""

    palette = serializers.SlugRelatedField(
        slug_field="slug", queryset=Palette.objects.all()
    )

    class Meta:
        model = Token
        fields = ["id", "palette", "key", "value"]


class PaletteSerializer(serializers.ModelSerializer):
    tokens = TokenSerializer(many=True, read_only=True)

    class Meta:
        model = Palette
        fields = ["id", "name", "slug", "is_published", "tokens"]
