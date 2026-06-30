from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .figma import import_from_figma
from .models import Palette, Token
from .serializers import PaletteSerializer, TokenSerializer

# GET is open (published only for anonymous); PATCH needs the model change
# permission, the same one Wagtail enforces in /admin/. No POST/DELETE via API.
WRITE_METHODS = ["get", "patch", "head", "options"]


class PaletteViewSet(viewsets.ModelViewSet):
    serializer_class = PaletteSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    lookup_field = "slug"
    http_method_names = WRITE_METHODS

    def get_queryset(self):
        qs = Palette.objects.prefetch_related("tokens")
        if self.request.user.has_perm("catalog.change_palette"):
            return qs
        return qs.filter(is_published=True)


class TokenViewSet(viewsets.ModelViewSet):
    """Inline token editing (F7): PATCH a token's value from the Palettes tab."""

    serializer_class = TokenSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    http_method_names = WRITE_METHODS

    def get_queryset(self):
        qs = Token.objects.select_related("palette")
        if self.request.user.has_perm("catalog.change_token"):
            return qs
        return qs.filter(palette__is_published=True)


class FigmaImportView(APIView):
    """POST endpoint behind the Figma Import tab. Requires palette edit permission."""

    def post(self, request):
        if not request.user.has_perm("catalog.change_palette"):
            return Response(
                {"detail": "You do not have permission to import palettes."},
                status=status.HTTP_403_FORBIDDEN,
            )
        file_key = request.data.get("file_key") or settings.FIGMA_FILE_KEY
        access_token = settings.FIGMA_ACCESS_TOKEN
        if not file_key or not access_token:
            return Response(
                {"detail": "Figma is not configured. Set FIGMA_FILE_KEY and "
                           "FIGMA_ACCESS_TOKEN in .env."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            result = import_from_figma(file_key, access_token)
        except Exception as exc:  # network/parse errors surface to the user
            return Response(
                {"detail": f"Figma import failed: {exc}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        return Response(result)
