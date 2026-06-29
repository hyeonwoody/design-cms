# Documentation

Turn the working application into run and deploy documentation. This stage is
required: the project is a portfolio and interview deliverable.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Previous stage | `../04-core-api/output/` | Source tree | What to document |
| Stage 03 | `../03-domain-modeling/output/models-and-erd.md` | ERD | Architecture doc |
| Reference | `references/django-deploy.md` | Full file | Deploy and run checklist |

## Process

1. Write `README.md`: install, run, migrate, seed
2. Write `docs/architecture.md`: ERD, routing, tab map, Figma flow
3. Write `.env.example` listing every required variable
4. Run the audit, then save to output/

## Audit

| Check | Pass Condition |
|-------|---------------|
| Reproducible run | A reader can set up and run the app from the README alone |
| Command coverage | Migration and seed commands are documented and correct |
| Env completeness | Every variable the app reads appears in `.env.example` |
| Architecture clarity | The doc covers the ERD, the tab UI, and the Figma sync flow |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Project docs | `output/README.md`, `output/docs/architecture.md`, `output/.env.example` | Markdown + env template |
