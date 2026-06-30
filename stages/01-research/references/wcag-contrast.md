# WCAG Contrast Reference

Color tokens in the CMS should meet WCAG 2.1 contrast ratios so designers do not
ship inaccessible palettes. Use these thresholds when classifying token requirements.

## Contrast ratio thresholds

| Level | Normal text | Large text (>=18pt or 14pt bold) |
|-------|-------------|----------------------------------|
| AA | >= 4.5 : 1 | >= 3 : 1 |
| AAA | >= 7 : 1 | >= 4.5 : 1 |

## How it applies here

- Treat the AA/AAA thresholds as **fixed constants** (they do not vary per palette). They live in `shared/constants.md`.
- A palette's color **token values** are **variable data** edited in the CMS.
- A later enhancement (out of initial scope) could flag tokens that fail AA in the admin.

Reference: https://www.w3.org/TR/WCAG21/#contrast-minimum