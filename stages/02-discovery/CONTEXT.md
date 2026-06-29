# Discovery

Turn the requirements into an app structure and routing plan, including the tab
navigation model.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Previous stage | `../01-research/output/requirements-brief.md` | Full file | What to structure |
| Reference | `references/django-routing.md` | Full file | Page vs API route patterns |
| Domain | `../../design-system/tab-model.md` | Full file | Canonical tab list to route |

## Process

1. Group variable data into Django apps (`catalog`, `library`, `compat`, `core`)
2. Define page routes (tabbed sections under `/`) vs API routes (`{{API_BASE_PATH}}`)
3. Define the tab navigation model: one route or anchor per tab
4. Run the audit, then save to output/

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| 2 | Draft app boundaries and route table | Whether apps and route split are correct |

## Audit

| Check | Pass Condition |
|-------|---------------|
| Route separation | Page routes and API routes do not collide |
| Tab coverage | Every tab from the requirements brief has a home route |
| Entity coverage | Every admin-editable entity belongs to exactly one app |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| App/route map | `output/app-route-map.md` | App boundaries, route table, tab model |
