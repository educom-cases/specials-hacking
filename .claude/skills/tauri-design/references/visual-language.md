---
title: Tauri Workbench Visual Language
description: Pastebook-derived semantic colors, surfaces, typography, iconography, geometry, spacing, and motion for the Tauri design skill.
summary: Defines the visual primitives that make the desktop shell read as one compact, layered productivity environment.
version: 1.1.0
author: René Krewinkel
parent_skill: tauri-design
enforcement: strict
read_when:
  - defining design tokens
  - styling components
  - choosing type, color, borders, radii, icons, or motion
---

# Visual language

The exact packaged `../assets/tokens.json` is the canonical source of truth. The values below explain its intended use; when any prose and the JSON differ, the JSON wins.

## Contents

- Character
- Color system
- Typography
- Geometry and spacing
- Iconography
- Motion
- Anti-patterns

## Character

Build a quiet, technical desktop workbench:

- dark without becoming black
- compact without becoming cramped
- layered through small surface shifts and hairline borders
- colorful only where actions, types, or states benefit from recognition
- rounded at the outer shell and local controls, not around every content group
- optimized for sustained editing and scanning

## Color system

Define semantic tokens from this reference palette:

```text
shell                 #24272d
window-bar            #2d333f
editor-and-input      #282c34
preview-deep          #1f232b
deepest-neutral       #1c1c27
text-primary          #ffffff
text-muted            rgba(255, 255, 255, 0.40)
primary               #3c7bfa
secondary-control     rgba(255, 255, 255, 0.10)
disabled-control      rgba(255, 255, 255, 0.05)
separator-subtle      rgba(255, 255, 255, 0.06)
separator             rgba(255, 255, 255, 0.08)
separator-strong      rgba(255, 255, 255, 0.14)
danger                #fc3c3d
modal-backdrop        rgba(8, 10, 14, 0.68)
modal-shadow          rgba(0, 0, 0, 0.45)
```

Use the surfaces by responsibility:

- `shell` for navigation, inspectors, toolbars, and modal surfaces
- `window-bar` for the native-style top boundary
- `editor-and-input` for the central work area, fields, code blocks, and editors
- `preview-deep` for rendered previews or media inspection

Do not scatter these literals through components. Generate CSS custom properties or SCSS variables with semantic names.

### Selection and state

- Use `primary` for selected list rows, active tools, primary buttons, selected chips, and user chat bubbles.
- Use translucent white at 4–10% for hover, secondary controls, assistant content, and subtle item backgrounds.
- Use `danger` for destructive intent or errors, but keep ordinary close icons a softer semantic red.
- Pair state color with shape, text, opacity, icon, border, or `aria-pressed`.

### Semantic accent colors

Use small accents for recognition, not large surfaces:

```text
add / link blue       #58a6ff
menu violet           #c792ea
save yellow           #ffcb6b
copy cyan             #89ddff
details light blue    #7dcfff
todo green            #a5d6a7
notes orange          #f78c6c
tags lime             #c3e88d
zoom blue             #82aaff
delete rose           #f07178
close pink-red        #f7768e
```

Language or content-type dots may use familiar ecosystem colors. Keep them at approximately `0.55rem` so they remain metadata rather than decoration.

## Typography

Use a humanist sans-serif family comparable to FreeSans:

- regular for content and controls
- bold for application identity, headings, and important labels
- monospace for code, snippet metadata, tags, status labels, and machine-oriented values

Reference scale:

```text
large                 1.4rem
default               1.1rem
main                  1rem
small                 0.8rem
tiny                  0.6rem
```

Use uppercase labels with approximately `0.08em` tracking for pane titles and operational status. Keep these labels small and muted.

Content previews may use:

- `2rem` for level-one headings
- `1.5rem` for level-two headings
- `1.25rem` for level-three headings
- `1.65` body line-height

## Geometry and spacing

Use a compact spacing rhythm based on `0.25rem`, `0.5rem`, `0.75rem`, and `1rem`.

Reference dimensions:

```text
outer shell radius        20px
window bar                40px
pane toolbar/status       36px
navigation pane           292px
context pane              292px
chat context maximum      520px or 44vw
icon control              32px minimum
traffic light             12px
modal width               28rem maximum
field radius              6px
list item radius          6px
modal/message radius      8px
chip radius               999px
```

Use one-pixel translucent borders to define regions. Prefer gaps and alignment over nested container padding.

## Iconography

Use a consistent outlined or Material-style icon family. Each icon must have one stable meaning across the application.

- Group related toolbar actions.
- Separate action groups with a `1px × 1rem` divider.
- Give icon-only buttons an accessible name.
- Use at least a `2rem` hit target even when the glyph is smaller.
- Keep inactive icon controls around 60% opacity and restore full opacity on hover, active, and focus.
- Do not use unlabeled icons when their meaning is product-specific or ambiguous.

Native-style window controls use 12px circular red, yellow, and green targets. Expose `aria-label` values and real Tauri behavior.

## Motion

Use restrained transitions between `200ms` and `400ms` with an ease curve for:

- pane width and opacity
- button background and opacity
- selected chips and rows
- modal appearance

Do not animate editor content, window movement, or frequent status updates. Disable nonessential animation under `prefers-reduced-motion`.

## Anti-patterns

Do not introduce:

- light page backgrounds behind the application surface
- gradients as decoration; the checkerboard media preview is the exception
- glassmorphism or heavy blur
- oversized marketing typography
- excessive shadows
- a card around every field or list group
- multiple competing accent colors at large scale
- controls without hover, focus, active, and disabled states
