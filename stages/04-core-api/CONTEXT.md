# Core API

Turn the models into a working application: tabbed MVT pages, a DRF API, the Admin
CMS, and Figma token import.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Previous stage | `../03-domain-modeling/output/models-and-erd.md` | Full file | What to serialize and render |
| Reference | `references/drf-serializers-viewsets.md` | Full file | API layer |
| Reference | `references/django-admin.md` | Full file | Admin as the CMS editing surface |
| Reference | `references/figma-tokens-api.md` | Full file | Import Figma variables into tokens |
| Shared | `../../shared/constants.md` | Full file | Fixed values templates import from |

## Process

1. Build MVT: `base.html` plus one partial per tab
2. Build DRF API: serializers, viewsets, router under `{{API_BASE_PATH}}`
3. Register models in Admin; `Token` inline under `Palette`; `is_published` toggle
4. Build the Figma import tab: map Figma variables to `Palette`/`Token` records
5. Run the audit, then save to output/

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| 1 | Tab layout and base template structure | Whether the tab UI matches the intended design |

## Audit

| Check | Pass Condition |
|-------|---------------|
| Admin coverage | Every model is registered in the Admin |
| API integrity | Each endpoint serializes and returns published records only |
| CMS round-trip | Editing a token in Admin changes the API response and the page |
| Tab reachability | Every tab is reachable from the base template |
| Figma import | Importing a Figma file produces valid `Token` rows |
| Static serving | Static assets serve under the production config |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Working Django app | `output/` | MVT templates, DRF API, Admin CMS, Figma import source tree |
