# Design CMS

Build a Django + DRF + PostgreSQL CMS where UI/UX designers manage design tokens,
palettes, components, and compatibility data. The front end organizes each feature
as a tab; design tokens import from Figma; documentation is a required deliverable.

## Folder Map

```
design-cms/
├── CLAUDE.md              (you are here)
├── CONTEXT.md             (start here for task routing)
├── setup/
│   └── questionnaire.md   (onboarding -- asks about the project, stack, Figma)
├── design-system/         (shared domain context: token contract, tab model)
├── shared/                (cross-stage files: constants, seed data)
└── stages/
    ├── 01-research/       (brief -> requirements + tab inventory)
    ├── 02-discovery/      (requirements -> app structure & routing)
    ├── 03-domain-modeling/(app map -> Django models + migrations + ERD)
    ├── 04-core-api/       (models -> MVT pages + DRF API + Admin CMS + Figma)
    └── 05-documentation/  (app -> README, architecture, .env.example)
```

## Triggers

| Keyword | Action |
|---------|--------|
| `setup` | Run onboarding -- asks about the project name, stack versions, and Figma |
| `status` | Show pipeline completion for all five stages |

### How `status` works

Scan `stages/*/output/`. If a stage's output folder has files other than .gitkeep,
it is COMPLETE, else PENDING. Render:

```
Pipeline Status: design-cms

  [01-research] --> [02-discovery] --> [03-domain-modeling] --> [04-core-api] --> [05-documentation]
      STATUS            STATUS               STATUS                  STATUS              STATUS
```

## Routing

| Task | Go To |
|------|-------|
| Turn a brief into requirements | `stages/01-research/CONTEXT.md` |
| Design app structure and routes | `stages/02-discovery/CONTEXT.md` |
| Model the domain | `stages/03-domain-modeling/CONTEXT.md` |
| Build the app, API, and CMS | `stages/04-core-api/CONTEXT.md` |
| Write run and deploy docs | `stages/05-documentation/CONTEXT.md` |

## What to Load

| Task | Load These | Do NOT Load |
|------|-----------|-------------|
| Research | `stages/01-research/references/`, `design-system/CONTEXT.md` | `stages/02` through `05` |
| Discovery | `stages/01-research/output/`, `stages/02-discovery/references/` | `references/examples`, later stages |
| Domain modeling | `stages/02-discovery/output/`, `stages/03-domain-modeling/references/`, `design-system/token-contract.md` | `stages/01`, `stages/04`, `stages/05` |
| Core API | `stages/03-domain-modeling/output/`, `stages/04-core-api/references/`, `shared/constants.md` | `stages/01`, `stages/02` |
| Documentation | `stages/04-core-api/output/`, `stages/03-domain-modeling/output/`, `stages/05-documentation/references/` | `stages/01`, `stages/02` |

## Stage Handoffs

Each stage writes its output to its own `output/` folder. The next stage reads from
there. If you edit an output file between stages, the next stage picks up your edits.
The flow is sequential (01 through 05); stage 05 also reads models from stage 03.
