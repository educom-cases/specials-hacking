---
title: Window Workspace and Token Integration
description: Desktop pane sizing, fixed-header containment, scrolling, transparent token foundation, and generated-variable verification.
summary: Keeps the custom chrome and application workspace usable without overflow or invented token names.
version: 1.0.0
author: René Krewinkel
parent_skill: tauri-window-chrome
enforcement: strict
read_when:
  - laying out the workspace below custom chrome
  - implementing a sidebar and content pane
  - integrating Tauri design tokens
  - debugging clipping or overflow
governs:
  - workspace layout
  - pane sizing
  - scrolling
  - generated tokens
  - responsive behavior
---

# Window workspace and token integration

## Workspace containment

The title bar is fixed-height; the workspace consumes the remainder:

```scss
.AppShell__content {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}
```

`min-height: 0` is required on nested flex or grid content that owns scrolling. Without it, a child can force the shell beyond the native window.

## Two-column workspaces

For a navigation/content product, use explicit grid sizing:

```scss
.WorkspaceLayout {
  display: grid;
  grid-template-columns: minmax(13rem, 25%) minmax(0, 1fr);
  height: 100%;
  width: 100%;

  @media (max-width: 768px) {
    grid-template-columns: minmax(11rem, 34%) minmax(0, 1fr);
  }
}
```

Adapt ratios to product needs while preserving these invariants:

- navigation keeps a readable minimum width
- the primary surface uses `minmax(0, 1fr)` so it can shrink
- scrolling belongs to intentional pane content
- a desktop workspace does not unexpectedly stack unless that behavior is designed
- optional panes collapse cleanly rather than leaving unusable slivers

## Mandatory React–Tauri tokens

Apply the `tauri-design` skill. The exact canonical asset must exist at:

```text
src/resources/design/tokens.json
```

The page foundation must remain transparent, and the shell should consume semantic surface, separator, traffic-light, foreground, spacing, radius, and shadow tokens.

Regenerate project-specific derived output using the repository's established commands. Typical commands are:

```shell
npm run token
npm run scss
```

Do not assume these script names exist; inspect `package.json`.

## Verify generated names

Inspect the generated CSS custom properties or SCSS variables before using them. Plausible names can be absent and silently break the interface.

When an existing component references an obsolete variable:

1. inspect the canonical JSON token
2. inspect current generated output
3. select the correct semantic generated name
4. regenerate output
5. verify the computed style in the Tauri webview

Do not fix a missing generated name by introducing an unrelated raw literal.
