# Requirements Brief: Design CMS

The product brief, feature/tab inventory, and data classification that later stages
build from. No designer was available, so the brief below is drafted from the domain
context (`design-system/token-contract.md`, `design-system/tab-model.md`).

## Product Brief

Design CMS is a web application where UI/UX designers manage a design system as
data. Designers edit palettes, tokens, components, usage scenarios, and stack
compatibility through the Wagtail CMS admin. The public front end presents each
feature as a tab and reads published data from a REST API. Design tokens can be
imported from a Figma file so the system stays in sync with the source of truth.

- **Who edits:** designers, through the Wagtail admin (`/admin/`)
- **Who consumes:** product teams, through the tabbed UI (`/`) and the API (`/api/`)
- **Source of truth for tokens:** a Figma file, imported on demand

## Feature -> Tab Inventory

Every feature is one tab in the UI and one requirement item.

| # | Feature | Tab | What the user can do | Backing app |
|---|---------|-----|----------------------|-------------|
| F1 | Palette management | Palettes | View published palettes and their tokens; edit in CMS | catalog |
| F2 | Component gallery | Components | Browse component markup grouped by category | library |
| F3 | Usage scenarios | Scenarios | Read scenarios and their recommended stacks | library |
| F4 | Compatibility matrix | Compatibility | See which stacks pair with which UI kits, and why | compat |
| F5 | Reference links | References | Open curated design-system and tooling links | core |
| F6 | Figma token import | Figma Import | Import/sync tokens from a Figma file into palettes | catalog |
| F7 | Inline palette editing | Palettes | Edit palette colors directly on the front-end without visiting /admin | catalog |

## Data Classification

### Variable data (lives in the database, edited in the CMS)

| Data | Fields | Owned by feature |
|------|--------|------------------|
| Palette | name, slug, is_published | F1 |
| Token | palette, key, value | F1, F6 |
| Component | category, name, markup | F2 |
| Scenario | title, description, recommended_stack | F3 |
| Stack | name | F4 |
| UIKit | name | F4 |
| Compatibility | stack, kit, level, rationale | F4 |
| Reference | category, title, url | F5 |

### Fixed constants (live in templates/code, not the database)

| Constant | Value | Home |
|----------|-------|------|
| Spacing baseline | 4px scale (4, 8, 12, 16, 24, 32, 48, 64) | `shared/constants.md` |
| Layout | max content width 1200px, sticky top tab bar | `shared/constants.md` |
| Contrast thresholds | AA >= 4.5, AAA >= 7 | `shared/constants.md` |
| Tab set | the six tabs above (structural) | `design-system/tab-model.md` |
| API base path | `/api/` | `shared/constants.md` |

## Audit

| Check | Result |
|-------|--------|
| Feature coverage | PASS - F1..F7 each map to exactly one requirement item and one tab |
| Data classification | PASS - every data element is labeled variable or fixed with no overlap |

## Handoff to Stage 02 (Discovery)

Stage 02 turns this into app boundaries and routes. The apps are already implied:
`catalog` (F1, F6), `library` (F2, F3), `compat` (F4), `core` (F5 + page shell). The
tab set is locked; routing must give each tab a home and keep page routes separate
from `/api/`.
