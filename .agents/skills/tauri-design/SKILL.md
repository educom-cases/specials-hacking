---
name: tauri-design
description: Design, implement, review, or refine polished Tauri v2 desktop interfaces using the mandatory packaged React design tokens and Pastebook-derived dark workbench system. Use for every Tauri v2 application with a React frontend and for custom window chrome, application shells, editor or productivity workspaces, toolbars, sidebars, inspectors, status bars, dialogs, code or content previews, dense desktop controls, responsive pane behavior, visual tokens, interaction states, accessibility, or design QA.
metadata:
  title: Tauri Workbench Design Contract
  summary: Installs the mandatory React–Tauri token asset and applies Pastebook's layered dark desktop language, compact custom chrome, flexible editor-centered pane system, semantic iconography, operational typography, and native-webview verification.
  version: 1.2.0
  author: René Krewinkel
  priority: critical
  enforcement: strict
  scope: project-wide
  derived_from:
    application: Pastebook
    version: 0.3.1
    design_type: dark desktop productivity workbench
  applies_to:
    - tauri-v2
    - react
    - typescript
    - desktop-ui
    - custom-window-chrome
    - productivity-tools
    - editors
    - inspectors
  requires:
    - Tauri custom chrome
    - React Atomic Design
    - SCSS or CSS Modules
    - design tokens
    - exact packaged tokens.json
    - accessible interaction states
    - native-webview verification
  governs:
    - visual-language
    - color
    - typography
    - spacing
    - application-shell
    - pane-layout
    - controls
    - interaction-states
    - responsive-behavior
    - design-quality
    - mandatory-design-token
  triggers:
    - design a Tauri app
    - style a Tauri interface
    - build a desktop workbench
    - create custom titlebar
    - create editor layout
    - create sidebar or inspector
    - create desktop toolbar
    - review Tauri visual design
    - improve desktop UX
    - create Tauri React application
    - configure Tauri React tokens
  keywords:
    - tauri
    - desktop-design
    - workbench
    - custom-chrome
    - dark-ui
    - editor
    - sidebar
    - inspector
    - status-bar
    - pastebook
  success_criteria:
    - one coherent visible window surface
    - chrome, navigation, work surface, inspector, and status have clear hierarchy
    - exact semantic tokens replace scattered visual literals
    - compact controls expose hover, active, disabled, focus, and accessible labels
    - panes collapse without shrinking the work surface below usability
    - text selection is enabled only where content requires it
    - native Tauri behavior and visual states are verified in the webview
    - exact mandatory tokens exist at src/resources/design/tokens.json
  failure_conditions:
    - generic browser page styling replaces desktop application structure
    - excessive cards or gradients obscure the work hierarchy
    - native controls are placed inside the content workspace
    - raw colors and spacing proliferate outside tokens
    - icon-only actions lack names or state feedback
    - browser-only inspection is treated as native verification
    - a Tauri React frontend omits or modifies the packaged token asset
  agent_instructions: Derive the information architecture before styling, use the routed reference values as a coherent system, preserve the React and Rust-Tauri contracts, implement every relevant state, and verify the result at realistic desktop sizes in the Tauri webview.
  tags:
    - tauri
    - design-system
    - desktop
    - dark-workbench
    - productivity
    - custom-chrome
---

# Tauri workbench design

Create a focused desktop tool, not a decorated website. Use one dark application surface whose chrome, navigation, editor, contextual tools, and status read as parts of the same native-style workbench.

## Read the relevant references

- Read [design-tokens.md](references/design-tokens.md) first for every Tauri v2 application with a React frontend. Install and verify the packaged token asset before styling; this requirement is absolute.
- Read [visual-language.md](references/visual-language.md) before defining generated styles, typography, icons, surfaces, borders, radii, or motion.
- Read [shell-and-layout.md](references/shell-and-layout.md) when creating or changing custom chrome, pane composition, editor surfaces, status bars, dialogs, responsive behavior, or window geometry.
- Read [components-and-states.md](references/components-and-states.md) when implementing buttons, fields, lists, tags, editors, previews, chat, empty states, focus, selection, or accessibility.
- Read [implementation-and-verification.md](references/implementation-and-verification.md) before coding and again before reporting completion.

Also apply the `react` skill to frontend architecture and the `rust-tauri` skill to native window mechanics, capabilities, persistence, and command boundaries. This skill governs visual and interaction design when responsibilities overlap.

## Design workflow

1. Inspect the existing shell, component system, tokens, assets, window configuration, and native capabilities.
2. Install the exact packaged tokens at `src/resources/design/tokens.json`.
3. Identify the primary work object and make it the flexible center surface.
4. Assign secondary responsibilities to a left navigation pane, right contextual pane, compact top chrome, or bottom status region.
5. Generate and consume semantic styles from the mandatory token source.
6. Specify default, hover, active, focus-visible, disabled, loading, empty, error, collapsed, and modal states.
7. Implement through Atomic Design components and `data-object-type` or equivalent semantic variants.
8. Verify token bytes, hierarchy, density, reduced widths, and native Tauri interaction states.

## Core composition

Use this hierarchy when the product supports it:

```text
Application surface
├── 40px custom window bar
│   ├── native-style window controls
│   ├── application icon and label
│   ├── draggable spacer
│   └── grouped global actions
├── Flexible workspace
│   ├── collapsible 292px navigation pane
│   ├── flexible primary work surface
│   └── collapsible 292px contextual pane
└── 36px status region within the primary surface
```

Use a wider contextual pane, up to `min(44vw, 520px)`, for conversational or content-heavy tools.

## Non-negotiable design rules

- Draw only one rounded full-window surface over the transparent Tauri page.
- Use the exact packaged `assets/tokens.json` at `src/resources/design/tokens.json`; do not substitute a project-specific token foundation.
- Use layered charcoal surfaces and hairline translucent separators; do not create a field of floating cards.
- Reserve saturated blue for selection, primary action, and direct user-authored emphasis.
- Keep toolbars compact and group actions with spacing or one-pixel separators.
- Use readable sans-serif text for content and monospace for code, metadata, tags, and operational status.
- Use semantic icon color sparingly to improve scanning; never make color the only state signal.
- Collapse optional panes to zero width with opacity and pointer-event control rather than leaving unusable slivers.
- Disable shell-wide text selection while restoring it for editors, inputs, previews, chat, and dialogs.
- Respect reduced motion and keyboard focus.
- Keep native window actions in the chrome boundary and test them after a full Tauri relaunch.
