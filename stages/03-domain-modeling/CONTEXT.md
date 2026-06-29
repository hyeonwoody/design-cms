# Domain Modeling

Turn the app/route map into Django models, migrations, and an ERD. The models are
the canonical design-token contract.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Previous stage | `../02-discovery/output/app-route-map.md` | Full file | Entities to model |
| Reference | `references/django-orm-fields.md` | Full file | Field selection |
| Reference | `references/postgres-fields.md` | Full file | JSONField/ArrayField for tokens and stacks |
| Reference | `references/python-setup.md` | Full file | Install Python + PostgreSQL before running migrations |
| Domain | `../../design-system/token-contract.md` | Full file | The token schema models must satisfy |

## Process

1. Define models per app (`Palette`, `Token`, `Component`, `Scenario`, `Stack`, `UIKit`, `Compatibility`, `Reference`)
2. Generate migrations and an ERD
3. Lock the schema as the design-token contract (later changes only via migration)
4. Run the audit, then save to output/

## Audit

| Check | Pass Condition |
|-------|---------------|
| Entity coverage | Every variable-data type from stage 01 has a model |
| Contract fidelity | Model fields match the token contract in `design-system/token-contract.md` |
| Migration validity | Migrations generate without errors against the target schema |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Models + migrations + ERD | `output/models-and-erd.md` | models.py listing, migration plan, ERD |
