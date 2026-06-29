# Seed Data Plan

The CMS ships with starter content loaded as Django fixtures. Stage 04 builds the
fixtures; `python manage.py loaddata` fills the database in one command.

| Fixture | Contains |
|---------|----------|
| `palettes.json` | Starter palettes and their tokens (from `{{PALETTE_SET}}`) |
| `scenarios.json` | Usage scenarios with recommended stacks |
| `compatibility.json` | Stack x UI-kit compatibility matrix |
| `references.json` | Design-system and tooling links |

Seed data mirrors the token contract in `design-system/token-contract.md`. When the
schema changes, regenerate the fixtures so they still load cleanly.
