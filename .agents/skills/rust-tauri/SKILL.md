---
name: rust-tauri
description: Mandatory implementation contract for creating, modifying, reviewing, or debugging Rust backends and Tauri v2 desktop boundaries. Use for work in src-tauri, including Rust setup, Cargo dependencies, custom main-window chrome, app_config configuration, module organization, Tauri commands and managed state, SQLite and rusqlite persistence, migrations, Serde and TypeScript contracts, capabilities, security, and backend or boundary tests.
metadata:
  title: Rust and Tauri Development Contract
  summary: Enforces a local-first Tauri v2 architecture with strict Rust module boundaries, custom native-style chrome, app_config paths, SQLite persistence, typed command contracts, and end-to-end verification.
  version: 2.4.0
  author: René Krewinkel
  priority: critical
  enforcement: strict
  scope: project-wide
  applies_to:
    - rust
    - tauri-v2
    - src-tauri
    - desktop
    - sqlite
    - rusqlite
    - serde
    - typescript-bridge
  requires:
    - Rust 2021
    - Tauri v2
    - app_config
    - rusqlite with bundled SQLite
    - serde
    - serde_json
    - chrono
    - uuid v4
    - Zod frontend validation
    - the exact tauri-design token asset when the frontend is React
  governs:
    - application composition
    - window configuration and capabilities
    - custom window chrome
    - configuration and application paths
    - module and file organization
    - database access and migrations
    - Tauri commands and managed state
    - Rust-TypeScript boundary contracts
    - backend tests and project checks
    - mandatory Tauri React design tokens
  triggers:
    - create or modify a Tauri application
    - create or configure a Tauri v2 application with a React frontend
    - change src-tauri
    - add a Rust module
    - add a Tauri command
    - add managed state
    - configure a Tauri window
    - implement custom window controls
    - add SQLite persistence
    - create a migration
    - change a Serde boundary type
    - review or debug Rust backend code
  keywords:
    - rust
    - tauri
    - tauri-v2
    - sqlite
    - rusqlite
    - app-config
    - serde
    - commands
    - capabilities
    - migrations
    - custom-chrome
  success_criteria:
    - main.rs remains minimal and lib.rs remains a composition root
    - application paths and configuration use app_config
    - the main window uses the required frameless transparent custom chrome
    - database access remains behind typed Tauri commands
    - SQL is parameterized and schema upgrades are safely migrated
    - Rust serialization, invoke payloads, and Zod schemas agree
    - formatting, checks, tests, and frontend builds pass
    - every React-backed Tauri v2 app contains the exact packaged tauri-design token at src/resources/design/tokens.json
  failure_conditions:
    - feature logic, SQL, or large domain types are placed in main.rs or lib.rs
    - application paths bypass app_config
    - the frontend opens SQLite or constructs SQL
    - a command is not registered or lacks a validated TypeScript wrapper
    - user input is interpolated into SQL
    - schema changes omit idempotent migration coverage
    - browser-only testing is treated as proof of native window behavior
    - a React-backed Tauri v2 app omits or modifies the packaged tauri-design token
  agent_instructions: Preserve the local-first architecture, load the relevant references before implementation, keep the Tauri boundary typed and minimal, and complete every applicable verification check before reporting completion.
  tags:
    - rust
    - tauri
    - desktop
    - sqlite
    - backend
    - local-first
    - typed-boundaries
---

# Rust and Tauri development contract

Follow this contract for every change to the Rust backend or Tauri boundary. Preserve the local-first architecture and keep `src-tauri/src/lib.rs` as composition code rather than feature implementation.

## Read the relevant references

- Apply the generic [Rust Development Contract](../rust/SKILL.md) for crate architecture, public APIs, errors, dependency selection, and Cargo verification. This skill adds Tauri-specific requirements.
- For every Tauri v2 application with a React frontend, also apply [Tauri Workbench Design](../tauri-design/SKILL.md), read its design-token reference first, and install its exact packaged token before styling. This requirement does not apply to clean React applications or Tauri applications using another frontend.
- Apply [Tauri v2 Window Chrome](../tauri-window-chrome/SKILL.md) when creating an application or changing windows, capabilities, layout chrome, native controls, dragging, resizing, restoration, or startup visibility. It is the canonical window-chrome contract.
- Read [configuration-and-structure.md](references/configuration-and-structure.md) when changing configuration, application paths, dependencies, modules, files, or domain organization.
- Read [persistence-and-commands.md](references/persistence-and-commands.md) when changing SQLite, migrations, managed state, commands, Serde types, invoke wrappers, or Zod boundary schemas.
- Read [verification.md](references/verification.md) before completion and when reviewing or debugging Rust/Tauri work.

For a review-only task, read the references governing the reviewed code and report violations. Do not mutate code unless the user asks for changes.

## Existing setup

- Use Rust edition 2021 and Tauri v2.
- Keep `src-tauri/src/main.rs` minimal. It may only apply the Windows release attribute and call `<crate_name>_lib::run()`.
- Treat `src-tauri/src/lib.rs` as the composition root: declare top-level modules, initialize managed state, register plugins, perform setup, register commands, and run Tauri.
- Configure application and bundle behavior in `src-tauri/tauri.conf.json`.
- Declare frontend permissions in `src-tauri/capabilities/default.json`. Add only permissions required by the implementation.
- Add dependencies to `src-tauri/Cargo.toml`. Do not introduce another crate or workspace member without a concrete architectural need.
- Prefer `tauri` and official plugins, `serde`, `serde_json`, `app_config`, `rusqlite` with bundled SQLite, `chrono`, and UUID v4.

## Core constraints

- Use `app_config` for application configuration and platform-aware application paths.
- Keep feature behavior in domain modules with explicit public surfaces.
- Keep SQLite in Rust behind typed Tauri commands.
- Use parameterized SQL and safe, idempotent migrations.
- Keep command payloads, Rust serialization, TypeScript wrappers, invoke argument names, and Zod schemas synchronized.
- Map operational failures to actionable errors. Do not panic during request handling.
- Add only the capabilities and dependencies required by the implementation.
- Test native window behavior in the Tauri webview after a full relaunch.
- In a React-backed Tauri v2 app, preserve the exact `tauri-design/assets/tokens.json` bytes at `src/resources/design/tokens.json`; generated styles and components must consume the token rather than replace it.

## Completion gate

Complete work only after every applicable item in [verification.md](references/verification.md) passes. If an environment or platform dependency blocks a check, report the exact constraint and run the remaining checks.
