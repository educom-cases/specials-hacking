---
title: Rust and Tauri Verification
description: Mandatory unit, persistence, serialization, native-window, formatting, build, and final review checks.
summary: Defines the evidence required before Rust and Tauri work can be reported complete.
version: 2.3.0
author: René Krewinkel
parent_skill: rust-tauri
enforcement: strict
read_when:
  - writing tests
  - reviewing Rust or Tauri code
  - debugging a boundary failure
  - before reporting completion
governs:
  - tests
  - formatting
  - cargo checks
  - frontend build
  - native verification
---

# Verification

## Tests

- Put pure unit tests beside their modules under `#[cfg(test)]`.
- Test serialized values whenever Rust enums or fields cross the frontend boundary.
- Test detection, editor selection, normalization, and migration logic independently from the Tauri runtime where possible.
- Use a temporary database for persistence tests. Never read or mutate the user's configured database.
- Test both fresh schema initialization and upgrades from existing schemas.
- Test Rust command contracts and matching frontend boundary validation.

## Commands

Run from the repository root:

```shell
cargo fmt --manifest-path src-tauri/Cargo.toml -- --check
cargo check --manifest-path src-tauri/Cargo.toml
cargo test --manifest-path src-tauri/Cargo.toml -- --nocapture
npm run build
```

Run `npm run check` for the combined project check. If an environment or platform dependency blocks a command, report the exact constraint and run all remaining checks.

## Final review

Confirm:

- Configuration and related paths use `app_config`.
- Feature logic lives in the correct domain module.
- Database access stays in Rust and uses parameterized SQL.
- Schema changes have safe migration behavior.
- Commands use typed payloads, typed results, and actionable errors.
- Every command is registered and has a validated TypeScript wrapper.
- Serde names, Zod schemas, payload fields, and invoke argument names agree.
- Capabilities and dependencies are minimal.
- The main window has frameless transparent chrome with top-boundary controls, application icon, and readable label.
- The window label and capability scope are both `main`.
- Move, resize, close, minimize, maximize, startup show, and restoration work after a full Tauri relaunch.
- Only the main layout draws the visible rounded window surface.
- When the frontend is React, `src/resources/design/tokens.json` exists and is byte-for-byte identical to the packaged `tauri-design/assets/tokens.json`.
- Formatting, Rust checks, Rust tests, frontend tests, and the frontend build pass.
