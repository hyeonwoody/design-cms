# Onboarding Questionnaire: Design System CMS

<!-- Read this file when the user types "setup". Ask ALL questions in a single
     conversational pass. The user answers in one message. Collect answers, replace
     placeholders across the listed files, then scan for remaining {{ patterns. -->

### Q1: What is the project name?
- Placeholder: `{{PROJECT_NAME}}`
- Files: `CLAUDE.md`, `CONTEXT.md`, `stages/05-documentation/references/django-deploy.md`
- Type: free text
- Default: `design-cms`

### Q2: Which Python and Django versions?
- Placeholder: `{{PYTHON_VERSION}}`, `{{DJANGO_VERSION}}`
- Files: `stages/03-domain-modeling/references/python-setup.md`, `stages/05-documentation/references/django-deploy.md`
- Type: free text
- Default: Python 3.12, Django 5.x

### Q3: What database name should the app use?
- Placeholder: `{{DB_NAME}}`
- Files: `shared/constants.md`, `stages/03-domain-modeling/references/python-setup.md`
- Type: free text
- Default: `design_system_cms`

### Q4: What API base path?
- Placeholder: `{{API_BASE_PATH}}`
- Files: `shared/constants.md`, `stages/02-discovery/CONTEXT.md`, `stages/04-core-api/CONTEXT.md`
- Type: free text
- Default: `/api/`

### Q5: Which Figma file holds your design tokens?
- Placeholder: `{{FIGMA_FILE_KEY}}`, `{{PALETTE_SET}}`
- Files: `design-system/token-contract.md`, `shared/seed-data.md`, `stages/04-core-api/references/figma-tokens-api.md`
- Type: free text (file key from the Figma URL; describe the starter palette set)
- Default: leave blank to seed an empty palette and import later
- Note: the Figma access token is a secret. It goes in `.env`, never in these files. The placeholder `{{FIGMA_ACCESS_TOKEN}}` stays only in `.env.example`.

---

## After Onboarding

Tell the user: "Configured. Start with Stage 01 -- Research. Describe what the CMS
should do and I will turn it into requirements and a tab inventory."

Then point them to `stages/01-research/CONTEXT.md`.

After all replacements, scan the workspace for remaining `{{` patterns (except
`{{FIGMA_ACCESS_TOKEN}}` in `.env.example`). If any remain, ask for the missing info.
