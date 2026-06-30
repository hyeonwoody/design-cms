from rest_framework import viewsets

from .models import Compatibility
from .serializers import CompatibilitySerializer


class CompatibilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Compatibility.objects.select_related("stack", "kit")
    serializer_class = CompatibilitySerializer
