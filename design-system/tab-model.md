# Tab Model

The front end organizes every tool and feature as its own tab. This is the canonical
tab list. Stage 02 routes each tab; stage 04 renders one template partial per tab.

| Tab | Manages | Backed by app |
|-----|---------|---------------|
| Palettes | Palettes and their tokens | `catalog` |
| Components | Component markup and categories | `library` |
| Scenarios | Usage scenarios and recommended stacks | `library` |
| Compatibility | Stack x UI-kit compatibility matrix | `compat` |
| References | Design-system and tooling links | `core` |
| Figma Import | Import/sync tokens from Figma into palettes | `catalog` |

Tabs are stable across runs. Adding or removing a tab is a structural change: update
this file, the stage 02 route map, and the stage 04 templates together.
