# Design System Context

Shared domain context for the CMS. Stages read these files; these files do not read
any stage (one-way references).

## Routing

| Resource | Location | Contains |
|----------|----------|----------|
| Token contract | `token-contract.md` | The canonical palette/token schema all stages align to |
| Tab model | `tab-model.md` | The canonical list of UI tabs and what each one manages |
