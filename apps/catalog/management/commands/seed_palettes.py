"""
Seed the reference palettes used to demo the CMS.

Each palette defines the six color tokens: background, foreground, muted,
card, border, accent. Values are theme-matched starting points to refine. Idempotent:
re-running upserts each palette and its tokens in place (it does not delete palettes
that are no longer listed, so palettes added through the CMS are left untouched).
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.catalog.models import Palette, Token

TOKEN_KEYS = [
    "color.background",
    "color.foreground",
    "color.muted",
    "color.card",
    "color.border",
    "color.accent",
]

# name -> [background, foreground, muted, card, border, accent]
PALETTES = {
    "Ocean": ["#08131c", "#e8f5ff", "#7f9bb3", "#10202d", "#1d3648", "#0ea5e9"],
    "Emerald": ["#08130d", "#ebfff5", "#84a99a", "#0f2018", "#1d3a2b", "#34d399"],
    "Crimson": ["#18090b", "#fff1f2", "#b68d93", "#231214", "#3d2327", "#ef4444"],
    "Lavender": ["#120d1d", "#f3efff", "#9f97c0", "#1b1629", "#30284a", "#a855f7"],
    "Cyber": ["#050505", "#f5f5f5", "#8f8f8f", "#101010", "#262626", "#00e5ff"],
    "Coffee": ["#18120d", "#f4ece4", "#aa9889", "#241b15", "#3d3027", "#b7791f"],
    "Mint": ["#0a1714", "#eefdf8", "#84b3a6", "#13231f", "#254037", "#2dd4bf"],
    "Slate": ["#16181d", "#f2f4f7", "#8c94a3", "#20242d", "#353b48", "#64748b"],
    "Cherry": ["#17090d", "#fff5f6", "#b6949a", "#231318", "#3c242a", "#e11d48"],
    "Sky": ["#08121d", "#eef8ff", "#8ca7bf", "#102030", "#20374d", "#38bdf8"],
    "Royal": ["#0d1024", "#eef1ff", "#8d96c9", "#151937", "#2a2f57", "#4f46e5"],
    "Terminal": ["#050807", "#d7ffe2", "#7da58c", "#0d120f", "#203126", "#22c55e"],
    "Amber": ["#181105", "#fff8ea", "#c3aa6b", "#241b0b", "#423215", "#fbbf24"],
    "Ice": ["#0b1418", "#f2fdff", "#8eb3bc", "#132126", "#28414a", "#67e8f9"],
    "Graphite": ["#111111", "#efefef", "#8b8b8b", "#1b1b1b", "#333333", "#9ca3af"],
    "Jade":    ["#081410", "#e2f0ea", "#749e88", "#0e1e18", "#183028", "#34d399"],
}


class Command(BaseCommand):
    help = "Create or update the reference palettes and their color tokens."

    def handle(self, *args, **options):
        for name, values in PALETTES.items():
            palette, _ = Palette.objects.update_or_create(
                slug=slugify(name),
                defaults={"name": name, "is_published": True},
            )
            for index, (key, value) in enumerate(zip(TOKEN_KEYS, values)):
                Token.objects.update_or_create(
                    palette=palette,
                    key=key,
                    defaults={"value": value, "sort_order": index},
                )
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(PALETTES)} palettes x {len(TOKEN_KEYS)} tokens."
            )
        )
