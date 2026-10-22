---
title: Native Window and Reliable Startup
description: Exact Tauri v2 window configuration, capabilities, label synchronization, frontend reveal, and mandatory native fallback.
summary: Prevents an initially hidden frameless window from remaining permanently invisible.
version: 1.0.0
author: René Krewinkel
parent_skill: tauri-window-chrome
priority: critical
enforcement: strict
read_when:
  - configuring a Tauri window
  - changing capabilities
  - hiding a window during startup
  - debugging an invisible window
governs:
  - src-tauri/tauri.conf.json
  - src-tauri/capabilities/default.json
  - src-tauri/src/lib.rs
  - React startup reveal
---

# Native window and reliable startup

## Window configuration

Configure a frameless transparent window in `src-tauri/tauri.conf.json`:

```json
{
  "app": {
    "macOSPrivateApi": true,
    "windows": [
      {
        "backgroundColor": "#00000000",
        "decorations": false,
        "height": 800,
        "label": "main",
        "minHeight": 520,
        "minWidth": 760,
        "resizable": true,
        "title": "<App Name>",
        "transparent": true,
        "visible": false,
        "width": 1200
      }
    ]
  }
}
```

- Choose dimensions appropriate for the product; preserve usable minimums.
- Use `macOSPrivateApi: true` for this transparent macOS configuration.
- Keep native resizing enabled.
- Do not add custom resize overlays.
- Fully relaunch Tauri after changing native configuration.

## One exact label

The configured label, capability window scope, frontend current-window handle, and Rust lookup must identify the same window. Prefer `main`:

```text
tauri.conf.json                 label: "main"
capabilities/default.json      windows: ["main"]
frontend                       getCurrentWindow()
Rust setup                     get_webview_window("main")
```

When these values disagree, window APIs can appear to fail even though the process remains healthy.

## Capabilities

Grant only the required Tauri v2 permissions in `src-tauri/capabilities/default.json`:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "core:window:allow-close",
    "core:window:allow-minimize",
    "core:window:allow-show",
    "core:window:allow-start-dragging",
    "core:window:allow-start-resize-dragging",
    "core:window:allow-toggle-maximize"
  ]
}
```

Add plugin permissions only when the application uses them. When all controls and dragging fail together, inspect capability scope before changing React code.

## Frontend post-paint reveal

An initially hidden window should normally appear after React has painted twice:

```tsx
useEffect(() => {
  const appWindow = getCurrentWindow()
  let paintedFrame = 0

  const showFrame = window.requestAnimationFrame(() => {
    paintedFrame = window.requestAnimationFrame(() => {
      void appWindow.show().catch(() => undefined)
    })
  })

  return () => {
    window.cancelAnimationFrame(showFrame)
    window.cancelAnimationFrame(paintedFrame)
  }
}, [])
```

Two frames reduce unstyled or partially rendered startup flashes. The `allow-show` permission is mandatory.

## Native reveal fallback

The frontend call is not sufficient by itself. A frontend exception, wrong dev-server target, stale capability configuration, IPC failure, or lifecycle timing issue can prevent it.

When `visible: false` is used, add this mandatory fallback during Tauri setup:

```rust
if let Some(window) = app.get_webview_window("main") {
    let fallback_window = window.clone();
    std::thread::spawn(move || {
        std::thread::sleep(std::time::Duration::from_millis(900));
        let _ = fallback_window.show();
    });
}
```

React normally shows the window first. Rust reveals it after approximately 900 ms if the frontend path fails. Calling `show()` on an already visible window is harmless.

Keep this setup logic in the composition root. Do not move unrelated feature logic into `lib.rs`.

## Restored geometry

When restoring dimensions or position:

- resolve available monitors before applying stale geometry
- clamp size to configured minimums and the monitor work area
- clamp position so the title bar remains reachable
- perform restoration before the normal frontend reveal
- preserve the native fallback even when restoration fails
