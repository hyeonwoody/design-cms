from rest_framework import serializers

from .models import Component, Scenario


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ["id", "category", "name", "markup"]


class ScenarioSerializer(serializers.ModelSerializer):
    recommended_stack = serializers.ListField(
        child=serializers.CharField(), allow_empty=True
    )

    class Meta:
        model = Scenario
        fields = ["id", "title", "description", "recommended_stack"]
