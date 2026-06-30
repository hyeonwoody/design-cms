from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.catalog.figma import import_from_figma


class Command(BaseCommand):
    help = "Import design tokens from a Figma file into palettes and tokens."

    def add_arguments(self, parser):
        parser.add_argument("--file-key", default=settings.FIGMA_FILE_KEY)
        parser.add_argument("--token", default=settings.FIGMA_ACCESS_TOKEN)

    def handle(self, *args, **options):
        file_key = options["file_key"]
        access_token = options["token"]
        if not file_key or not access_token:
            raise CommandError(
                "Set FIGMA_FILE_KEY and FIGMA_ACCESS_TOKEN in .env, or pass "
                "--file-key and --token."
            )
        result = import_from_figma(file_key, access_token)
        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {result['palettes']} palette(s), "
                f"{result['tokens']} token(s)."
            )
        )
