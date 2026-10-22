---
title: Window Chrome Verification and Troubleshooting
description: Code checks, full-relaunch native smoke tests, evidence levels, component coverage, and ordered failure diagnosis.
summary: Separates build success from proof that the Tauri process owns a visible and operable native window.
version: 1.0.0
author: René Krewinkel
parent_skill: tauri-window-chrome
priority: critical
enforcement: strict
read_when:
  - before reporting window chrome complete
  - debugging an invisible window
  - debugging controls or dragging
  - diagnosing clipping backgrounds or dev-server conflicts
governs:
  - tests
  - builds
  - native smoke tests
  - troubleshooting order
---

# Window chrome verification and troubleshooting

## Automated checks

Use the scripts present in the target repository. A typical React–Tauri sequence is:

```shell
npm run token
npm run scss
npx vitest run
npm run build
cargo fmt --manifest-path src-tauri/Cargo.toml -- --check
cargo check --manifest-path src-tauri/Cargo.toml
cargo test --manifest-path src-tauri/Cargo.toml -- --nocapture
```

Add or update tests that prove:

- the title bar renders once
- close, minimize, and maximize have accessible names
- optional application actions render correctly
- window-control variants preserve button semantics
- the application identity renders
- the shell works with and without trailing actions

Build and test success does not prove native visibility or behavior.

## Avoid dev-server conflicts

Before launching Tauri, check whether the configured dev-server port is already in use. Do not let a second Vite process or port conflict hide the actual native result.

If the correct Vite server is already running, use the project's supported method to skip `beforeDevCommand`. For the standard CLI:

```shell
npx tauri dev --no-watch -c '{"build":{"beforeDevCommand":""}}'
```

Confirm the existing server belongs to the target application before reusing it.

## Native evidence levels

Verify these as separate facts:

1. the Tauri process exists
2. the process owns the expected native window
3. the native window is visible
4. the native controls and movement work

Do not infer a later fact from an earlier one.

## Full-relaunch smoke test

After configuration, capability, or Rust changes:

1. stop the prior Tauri process
2. rebuild and launch a fresh Tauri process
3. wait longer than the native reveal fallback
4. confirm exactly one application window exists
5. confirm it is visible
6. drag using empty title-bar space
7. verify minimize, maximize, and close
8. verify native edge resizing
9. verify restored geometry remains reachable
10. confirm no rectangular background appears behind rounded shell corners
11. confirm title-bar actions fit without clipping at supported widths

On macOS, an optional diagnostic is:

```shell
osascript -e \
  'tell application "System Events" to tell process "<process-name>" to count windows'
```

Use the correct process name. A count of zero means CSS changes cannot solve the immediate failure.

## Troubleshooting order

### Process runs but no window appears

1. Confirm whether `visible` is `false`.
2. Confirm React calls `show()` after two painted frames.
3. Confirm `core:window:allow-show` exists.
4. Confirm Rust contains the delayed native `show()` fallback.
5. Confirm configuration, capabilities, frontend, and Rust identify the same label.
6. Fully stop and restart Tauri.
7. Confirm the Rust process remains alive.
8. Check the operating-system window count and visibility.

### All window actions fail

1. Inspect capability permissions and window scope.
2. Confirm execution is in the Tauri webview, not a browser tab.
3. Confirm handlers use `getCurrentWindow()`.
4. Fully relaunch after capability changes.

### Dragging fails but controls work

1. Confirm `allow-start-dragging`.
2. Confirm the mouse handler is attached.
3. Check for positioned overlays.
4. Confirm interactive descendants are excluded.
5. Test empty spacer space, not a button.

### Header actions clip

1. Remove inherited action-group padding.
2. Inspect responsive rules that restore padding or larger dimensions.
3. Keep every child within the fixed title-bar height.

### A rectangular second surface appears

1. Make `html`, `body`, and `#root` transparent.
2. Remove body padding.
3. Remove full-window backgrounds from intermediate wrappers.
4. Keep the native background transparent.
5. Let only the outer application shell draw the visible surface.

### Tauri starts the wrong frontend

1. Inspect the configured dev URL and port.
2. Identify the process currently owning that port.
3. Stop an unrelated server or deliberately reuse the correct one.
4. Relaunch Tauri without masking startup errors.

## Completion checklist

- All configured labels and scopes agree.
- Both reveal paths exist when startup is hidden.
- Generated token names exist.
- Automated checks pass.
- A fresh Tauri process owns one visible window.
- Drag, resize, close, minimize, maximize, and restoration work.
- The transparent single-surface composition is visually correct.
- Responsive title-bar actions do not clip.
