---
name: tauri-window-chrome
description: Create, configure, implement, review, debug, or verify reliable custom window chrome for Tauri v2 desktop applications with React frontends. Use when making a frameless or transparent window, custom title bar, traffic-light controls, draggable regions, startup reveal behavior, native show fallback, application shell, responsive desktop workspace, window capabilities, or native window smoke test. Apply whenever visible is false; two independent reveal paths are mandatory.
metadata:
  title: Tauri v2 Window Chrome Contract
  summary: Enforces a single transparent custom-chrome surface, synchronized native permissions, safe dragging and controls, dual-path startup reveal, and native verification.
  version: 1.1.0
  author: René Krewinkel
  priority: critical
  enforcement: strict
  scope: project-wide
  derived_from:
    application: Tox
    design_system: Pastebook
    source: WINDOW_CHROME_INSTRUCTIONS.md
  applies_to:
    - tauri-v2
    - react
    - typescript
    - rust
    - desktop
    - custom-window-chrome
  requires:
    - one synchronized main-window label
    - explicit Tauri v2 window capabilities
    - frontend post-paint reveal
    - delayed native reveal fallback
    - accessible native window controls
    - full-relaunch native verification
  governs:
    - tauri.conf.json window configuration
    - window capability scope
    - Rust startup fallback
    - React application shell
    - custom title bar
    - window controls and drag regions
    - transparent root composition
    - desktop workspace sizing
    - native verification
  triggers:
    - create a Tauri v2 desktop application
    - remove native window decorations
    - make a Tauri window transparent
    - create a custom title bar
    - add close minimize or maximize controls
    - debug window dragging
    - hide a window during startup
    - debug an invisible Tauri window
    - verify native window behavior
  keywords:
    - tauri-v2
    - window-chrome
    - titlebar
    - frameless
    - transparent-window
    - startup-visibility
    - native-window
    - drag-region
    - traffic-lights
  success_criteria:
    - exactly one visible rounded application surface fills the transparent native window
    - the label main is synchronized across configuration capabilities frontend and Rust
    - hidden startup has independent frontend and native reveal paths
    - close minimize maximize drag and native resize work in the Tauri webview
    - native verification distinguishes process window existence visibility and controls
    - generated design-token names are checked before use
  failure_conditions:
    - visible false relies on only a frontend show call
    - builds are treated as proof that a native window appears
    - labels or capability scopes disagree
    - interactive controls can initiate a window drag
    - multiple full-window backgrounds create a rectangular second surface
    - responsive styles exceed the fixed title-bar height
    - plausible but nonexistent generated token variables are used
  agent_instructions: Read the routed references, preserve one canonical chrome implementation, implement both startup reveal paths whenever the window starts hidden, and complete native verification after a full Tauri relaunch.
  tags:
    - tauri
    - desktop
    - custom-chrome
    - native-window
    - startup-reliability
    - react
---

# Tauri v2 window chrome

Implement a native-feeling frameless Tauri window whose React shell is the only visible surface. Treat startup visibility as a native reliability boundary, not as styling.

## Read the relevant references

- Read [native-window-and-startup.md](references/native-window-and-startup.md) when creating or changing the window, capabilities, labels, startup visibility, Rust setup, or native fallback.
- Read [frontend-shell-and-controls.md](references/frontend-shell-and-controls.md) when implementing the React shell, transparent roots, title bar, identity, controls, drag behavior, or action placement.
- Read [workspace-and-tokens.md](references/workspace-and-tokens.md) when sizing panes, integrating the mandatory Tauri React tokens, or resolving shell density and overflow.
- Read [verification-and-troubleshooting.md](references/verification-and-troubleshooting.md) before completion and whenever visibility, controls, dragging, clipping, backgrounds, or dev-server startup fails.

Also apply `rust-tauri` for native architecture and `tauri-design` for the mandatory React–Tauri token asset and broader visual system.

## Mandatory workflow

1. Inspect the current window label, Tauri configuration, capability scope, Rust setup, React startup, page roots, shell, actions, generated tokens, tests, and development-server state.
2. Configure one frameless transparent main window and keep its exact label synchronized across every boundary.
3. If the window starts hidden, implement both reveal paths:
   - React calls `show()` after two painted frames.
   - Rust calls `show()` after a delayed native fallback.
4. Build one fixed-height custom title bar with identity, accessible native controls, safe draggable space, and optional application actions.
5. Keep the page and intermediate wrappers transparent; let only the application shell draw the full-window surface.
6. Fit the workspace below the title bar with explicit shrinking and scrolling behavior.
7. Add or update component tests and stories without creating a second shell implementation.
8. Run code-level checks, fully relaunch Tauri, and verify native behavior independently of build success.

## Non-negotiable rules

- Keep the main window label exactly `main` unless an existing application deliberately uses another label; if so, use that one exact value everywhere.
- Whenever `visible: false` is configured, frontend reveal without a native fallback is incomplete.
- Include `allow-show`, control, and dragging permissions before debugging frontend handlers.
- Do not rely solely on `data-tauri-drag-region`; call `startDragging()` and exclude interactive descendants.
- Use native edge resizing. Do not add resize overlays.
- Keep close, minimize, and maximize together and give each an accessible name.
- Do not let action-bar padding or responsive rules make the title bar taller than its fixed height.
- Check generated token output before referencing a CSS variable.
- Fully restart Tauri after native configuration, capabilities, or Rust startup changes.
- Do not report completion until the native window exists, is visible, and its controls work.

## Completion gate

Complete every applicable item in [verification-and-troubleshooting.md](references/verification-and-troubleshooting.md). Report an unavailable native check with the exact environment constraint; never silently replace it with a browser or build check.
