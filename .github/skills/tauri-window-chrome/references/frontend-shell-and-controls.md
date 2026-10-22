---
title: Frontend Shell and Window Controls
description: Single-surface React shell, fixed custom title bar, identity, accessible controls, safe dragging, and transparent root rules.
summary: Defines the frontend half of a native-feeling Tauri v2 custom window.
version: 1.0.0
author: René Krewinkel
parent_skill: tauri-window-chrome
enforcement: strict
read_when:
  - implementing a custom title bar
  - adding window controls
  - debugging dragging
  - removing duplicate window backgrounds
governs:
  - React application shell
  - page roots
  - custom title bar
  - window identity
  - window controls
  - draggable regions
---

# Frontend shell and window controls

## One visible application surface

Keep `html`, `body`, `#root`, and intermediate application wrappers transparent. Only the outer shell draws the full-window background:

```scss
html,
body,
#root {
  background-color: transparent;
  height: 100%;
  overflow: hidden;
}

body {
  margin: 0;
  padding: 0;
}

.AppShell {
  background-color: var(--bg-surface);
  border-radius: var(--border-radius-panel);
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  width: 100%;
}
```

Use `width: 100%`, not an overflowing `100vw`. Do not add body padding to reveal rounded corners. The transparent native window provides the outside area.

## Fixed title-bar structure

Use one compact title bar:

```text
WindowHeader
├── Identity
│   ├── TrafficLights
│   │   ├── Close
│   │   ├── Minimize
│   │   └── Maximize
│   ├── AppIcon
│   └── AppLabel
├── DragRegion
└── OptionalApplicationActions
```

A 40 px bar is the default:

```scss
.AppShell__windowHeader {
  align-items: center;
  background-color: var(--bg-surface-window-bar);
  border-bottom: 1px solid var(--bg-white-subtle);
  display: flex;
  flex: 0 0 2.5rem;
  gap: var(--spacing-three-quarters);
  height: 2.5rem;
  min-height: 2.5rem;
  overflow: hidden;
  padding: 0 var(--spacing-three-quarters);
  user-select: none;
}

.AppShell__dragRegion {
  align-self: stretch;
  flex: 1;
}
```

Remove inherited action-bar padding and check responsive media queries. Nested actions must remain within the fixed height.

## Identity and controls

- Place controls, application icon, and readable application name together at the leading edge.
- Mark the icon decorative when adjacent text communicates the same identity.
- Keep normal application actions on the trailing edge.
- Give close, minimize, and maximize explicit accessible labels.
- Render native-style traffic lights as compact semantic variants; do not remove the accessible button behavior.

Connect controls directly:

```tsx
void getCurrentWindow().close()
void getCurrentWindow().minimize()
void getCurrentWindow().toggleMaximize()
```

Use the canonical Tauri design traffic-light tokens instead of raw colors.

## Reliable dragging

Keep `data-tauri-drag-region` as declarative support, but also call the API:

```tsx
const handleStartWindowDrag = (event: MouseEvent<HTMLElement>) => {
  if (event.button !== 0) {
    return
  }

  const target = event.target
  if (
    target instanceof HTMLElement &&
    target.closest('button, input, textarea, select, a, [role="button"]') !== null
  ) {
    return
  }

  void getCurrentWindow().startDragging()
}
```

Attach it to the title bar or dedicated spacer. The interactive-descendant guard is mandatory: a control press must never start a native drag.

## Component ownership

Extend the existing application shell, icon button, and action-group components. Do not create a parallel title-bar component tree that duplicates the live shell.

Add semantic control variants and tests to established primitives. Preserve normal application action glyphs when window-control variants use traffic-light circles.
