---
title: Tauri Persistence and Command Contracts
description: SQLite ownership, migrations, managed state, Tauri command, Serde, invoke, Zod, error, and path-safety requirements.
summary: Defines a typed end-to-end boundary from React through Tauri commands to parameterized SQLite operations.
version: 2.3.0
author: René Krewinkel
parent_skill: rust-tauri
enforcement: strict
read_when:
  - changing persistence or schema
  - adding a migration
  - adding managed state or a command
  - changing Rust-TypeScript boundary data
governs:
  - sqlite
  - rusqlite
  - migrations
  - tauri commands
  - serde
  - invoke wrappers
  - zod
---

# Persistence and commands

## Contents

- Boundary flow
- Database lifecycle
- Stable command contracts
- Paths, errors, and blocking work

## Boundary flow

Use SQLite only in Rust. The frontend must communicate through typed `invoke` wrappers and must never open the database, construct SQL, or depend on a database path.

```text
React feature
  -> src/lib/<domain>/index.ts invoke wrapper
  -> registered #[tauri::command]
  -> managed DatabaseState
  -> operation-specific SQL
  -> SQLite
  -> serializable Rust result
  -> Zod validation at the frontend boundary
```

## Database lifecycle

- Open the configured database during `run()` before building the application.
- Create the database parent directory before opening SQLite.
- Execute schema creation and required idempotent migrations before accepting commands.
- Store `rusqlite::Connection` in `DatabaseState` behind `Mutex<Connection>` and register it with `.manage(database)`.
- Receive it as `tauri::State<'_, DatabaseState>`.
- Convert lock, SQLite, serialization, and validation failures into actionable command errors. Do not panic during request handling.
- Use `rusqlite::params!`; never interpolate user input into SQL.
- Use a transaction when several writes must succeed or fail together.
- Generate record IDs in Rust with UUID v4.
- Store timestamps as UTC ISO-8601 strings.
- Keep `PRAGMA foreign_keys = ON`.
- Serialize snippet tags as JSON in a SQLite `TEXT` column and normalize them at the persistence boundary.
- Keep schema changes backward compatible. Add an idempotent migration and test fresh initialization plus upgrade behavior.
- Preserve lifecycle semantics: snippets and todos are soft-deleted by default; notes are one-per-snippet and may be hard-deleted; foreign keys cascade child removal when a snippet is hard-deleted.

## Stable command contracts

- Mark frontend-callable functions with `#[tauri::command]`.
- Use dedicated `Deserialize` payload structs for non-trivial input.
- Use serializable domain types for output and `Result<T, E>` for fallible commands.
- Keep errors useful without leaking sensitive values.
- Keep field and enum serialization in `snake_case` when existing frontend schemas expect it.
- Register every command in `tauri::generate_handler!` in `src-tauri/src/lib.rs`; the attribute alone does not expose it.
- Add or update the wrapper under `src/lib/<domain>/index.ts`.
- Validate frontend input and output with the matching Zod schema under `src/lib/<domain>/schema.ts`.
- Pass multi-field command data in a `payload` object and match its fields to Serde exactly.
- For direct Rust parameters such as `snippet_id`, use Tauri's camel-case JavaScript argument name, such as `snippetId`.
- Keep window and plugin access in Tauri-facing orchestration. Keep pure domain logic independent of an application handle.

When adding a command, update all four:

1. Rust payload/result types and command implementation.
2. `tauri::generate_handler!` registration.
3. TypeScript `invoke` wrapper and Zod schemas.
4. Rust and frontend boundary tests.

## Paths, errors, and blocking work

- Treat a configured database path as application input. Return a clear startup error when it cannot be created or opened.
- Do not log snippet content, API keys, config secrets, or raw database values.
- Avoid holding the database mutex during filesystem, network, window, or unrelated slow work.
- Do not run blocking database work on Tauri's async runtime. Keep commands synchronous while operations remain short; move substantial blocking work to a dedicated blocking task or worker.
