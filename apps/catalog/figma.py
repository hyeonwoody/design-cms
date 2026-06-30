"""
Figma token import (F6).

Fetches published variables from a Figma file and upserts them as Palette/Token
records. Uses the stdlib (urllib) so no extra dependency is needed. See
stages/04-core-api/references/figma-tokens-api.md for the mapping.
"""
import json
import urllib.request

from django.utils.text import slugify

from .models import Palette, Token

FIGMA_VARIABLES_URL = "https://api.figma.com/v1/files/{key}/variables/published"


def fetch_published_variables(file_key, access_token):
    request = urllib.request.Request(
        FIGMA_VARIABLES_URL.format(key=file_key),
        headers={"X-Figma-Token": access_token},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def _rgba_to_hex(value):
    r, g, b = (round(value[c] * 255) for c in ("r", "g", "b"))
    return f"#{r:02X}{g:02X}{b:02X}"


def _resolve_value(variable):
    modes = variable.get("valuesByMode", {})
    if not modes:
        return ""
    value = next(iter(modes.values()))
    if isinstance(value, dict) and {"r", "g", "b"} <= set(value):
        return _rgba_to_hex(value)
    return str(value)


def import_from_figma(file_key, access_token):
    """Upsert palettes (from variable collections) and tokens (from variables).

    Imported palettes start unpublished so a designer reviews them before they hit
    the public API. Returns a summary dict.
    """
    data = fetch_published_variables(file_key, access_token)
    meta = data.get("meta", {})
    collections = meta.get("variableCollections", {})
    variables = meta.get("variables", {})

    collection_to_palette = {}
    for collection_id, collection in collections.items():
        name = collection.get("name", collection_id)
        palette, _ = Palette.objects.get_or_create(
            slug=slugify(name), defaults={"name": name, "is_published": False}
        )
        collection_to_palette[collection_id] = palette

    tokens_touched = 0
    for variable in variables.values():
        palette = collection_to_palette.get(variable.get("variableCollectionId"))
        if not palette:
            continue
        key = variable.get("name", "").replace("/", ".")
        if not key:
            continue
        Token.objects.update_or_create(
            palette=palette, key=key, defaults={"value": _resolve_value(variable)}
        )
        tokens_touched += 1

    return {"palettes": len(collection_to_palette), "tokens": tokens_touched}
