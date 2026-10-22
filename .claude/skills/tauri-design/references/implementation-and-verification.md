---
title: Tauri Workbench Implementation and Verification
description: Required analysis, tokenization, implementation order, native verification, responsive review, and Definition of Done.
summary: Converts the visual system into a repeatable engineering workflow and evidence-based completion gate.
version: 1.1.0
author: René Krewinkel
parent_skill: tauri-design
enforcement: strict
read_when:
  - before implementation
  - while reviewing design quality
  - before reporting completion
---

# Implementation and verification

## Before implementation

Produce:

```text
Primary work object:
Global actions:
Navigation responsibilities:
Contextual responsibilities:
Status information:
Required content modes:
Window and minimum dimensions:
Collapse behavior:
Modal workflows:
```

Inspect existing tokens and components before adding new variants. Reuse semantic contracts instead of creating parallel component systems.

## Implementation order

1. Configure the transparent undecorated Tauri window and capabilities through the Rust-Tauri contract.
2. Install and verify the exact packaged token asset at `src/resources/design/tokens.json`.
3. Establish transparent document roots and the single visible shell.
4. Generate semantic styles from the canonical token source.
5. Implement custom chrome, application identity, drag behavior, and native controls.
6. Implement workspace regions and collapse states.
7. Implement the primary work surface and content modes.
8. Implement contextual tools and dialogs.
9. Implement every interaction, loading, empty, error, and accessibility state.
10. Verify in the browser for rapid layout iteration.
11. Relaunch and verify in the Tauri webview for native behavior and final rendering.

## Engineering rules

- Keep visual tokens in one canonical source and generate derived SCSS when the project uses token generation.
- Keep component styling colocated and imported through the established style entry point.
- Use semantic attributes for variants; do not build selectors from incidental DOM position.
- Keep `min-height: 0`, `min-width: 0`, and overflow ownership explicit in nested flex layouts.
- Avoid `transition: all` when a narrower property list is practical.
- Do not add inline styles to bypass the token or component system.
- Do not copy Pastebook product identity, wording, or icon artwork into another product. Reuse the design grammar and substitute the target application's identity.
- Keep business logic outside visual components.

## Browser review

Use browser review for:

- hierarchy and alignment
- overflow and scrolling
- hover, focus, active, disabled, loading, empty, and modal states
- editor and preview sizing
- narrow-width collapse behavior
- contrast and text selection

Inspect at the intended initial dimensions, around 1024px width, and near the supported minimum.

## Native Tauri review

After a full relaunch, verify:

- transparent corners reveal no back window
- only one rounded surface is visible
- close, minimize, maximize, drag, and resize work
- interactive controls do not initiate dragging
- restored position and dimensions remain on-screen
- the window appears only after restored state and initial paint
- font rendering, select menus, editor measurement, and focus match expectations
- pane animation remains smooth during native resize

Browser-only review cannot complete this gate.

## Definition of Done

Confirm:

- The primary work object dominates the flexible center.
- The exact mandatory token asset exists and passes the bundled `--check`.
- Navigation and contextual responsibilities are separated.
- Chrome contains native controls, product identity, a draggable spacer, and grouped global actions.
- Surface colors follow the layered charcoal hierarchy.
- Primary blue is reserved for meaningful action and selection.
- Typography distinguishes content from operational metadata.
- Borders, radii, spacing, and icon treatments come from semantic tokens.
- Lists use compact rows rather than excessive cards.
- Fields, controls, chips, editors, previews, dialogs, and chat follow their component contracts.
- Every interactive state is implemented and keyboard accessible.
- Optional panes release their space completely when closed.
- Content regions own their scrolling.
- Reduced-motion behavior exists.
- Browser layout checks pass.
- Native Tauri checks pass after relaunch.
- Existing React and Rust-Tauri completion gates pass.
