from rest_framework import serializers

from .models import Compatibility


class CompatibilitySerializer(serializers.ModelSerializer):
    stack = serializers.StringRelatedField()
    kit = serializers.StringRelatedField()
    level = serializers.CharField(source="get_level_display", read_only=True)

    class Meta:
        model = Compatibility
        fields = ["id", "stack", "kit", "level", "rationale"]
