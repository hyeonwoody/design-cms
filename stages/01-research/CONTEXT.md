# Research

Turn the project brief into a requirements document that classifies the data and
lists the features that become tabs.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| User | (conversation) | Project brief / goals | What the CMS must do |
| Reference | `references/django-overview.md` | Full file | What the framework can do |
| Reference | `references/wcag-contrast.md` | Full file | Token accessibility thresholds |
| Domain | `../../design-system/CONTEXT.md` | Full file | Routes to token contract and tab model |

## Process

1. Capture the brief. If no prototype exists, draft one yourself (no designer is available)
2. List every feature and mark each as a tab in the UI
3. Classify data: variable (palettes, tokens, components, scenarios, compatibility, references) vs fixed constants (spacing scale, layout, contrast thresholds)
4. Run the audit, then save to output/

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| 2 | Feature list with proposed tabs | Whether the tab inventory is complete and correctly scoped |

## Audit

| Check | Pass Condition |
|-------|---------------|
| Feature coverage | Every feature maps to one requirement item and one tab |
| Data classification | Every data element is labeled variable or fixed, with no overlap |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Requirements brief | `output/requirements-brief.md` | Variable-vs-fixed table + tab inventory |
