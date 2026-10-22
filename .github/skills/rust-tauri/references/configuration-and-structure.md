---
title: Tauri Configuration and Rust Module Structure
description: Mandatory app_config usage, dependency choices, path handling, and Rust module placement rules.
summary: Keeps configuration platform-aware and preserves a small composition root with domain-oriented modules.
version: 2.3.0
author: René Krewinkel
parent_skill: rust-tauri
enforcement: strict
read_when:
  - adding or changing configuration
  - resolving application paths
  - adding dependencies
  - creating or reorganizing Rust modules
governs:
  - app_config
  - Cargo dependencies
  - module structure
  - documentation
---

# Configuration and structure

## Use `app_config`

Use `app_config` for all application configuration. Do not replace it with direct home-directory lookup, environment-specific path assembly, `dirs`, `directories`, or another configuration crate.

- Define one application identifier, such as `const APP_NAME: &str = "app-name"`, and reuse it.
- Load configuration with `app_config::load_with_app(APP_NAME)`.
- Resolve the directory and filename with `app_config::config_dir_and_filename(APP_NAME)`.
- Use the resulting platform-aware location. A Unix-style setup commonly resolves to `~/.config/<app-name>/config.toml`; never hard-code the expanded path.
- Keep parsing, defaults, and config commands in `src-tauri/src/config/mod.rs`. Split only when responsibilities become materially distinct.
- Define typed settings. Return defaults for an absent file and handle malformed or invalid values deliberately.
- Resolve related files, including the default database and window-state file, from the directory returned by `app_config`.
- Expose only serializable, frontend-safe settings. Do not expose secrets or implementation-only configuration without an explicit requirement.

The current shape is:

```toml
[appearance]
theme = "default"

[database]
path = "~/.config/<app-name>/<app-name>.db"

[editor]
default_mode = "text"
supported_languages = ["react", "typescript", "javascript", "rust"]
```

When adding a setting, update the Rust type, default, loading logic, frontend Zod schema, and config schema documentation together.

## Preserve module structure

Organize behavior by domain and expose each module explicitly through `mod.rs`:

```text
src-tauri/
├── Cargo.toml
├── build.rs
├── tauri.conf.json
├── capabilities/
│   └── default.json
└── src/
    ├── main.rs
    ├── lib.rs
    ├── config/
    │   └── mod.rs
    ├── database/
    │   ├── mod.rs
    │   ├── documentation.md
    │   ├── model.rs
    │   ├── schema.rs
    │   ├── commands.rs
    │   ├── insert.rs
    │   ├── select.rs
    │   ├── update.rs
    │   └── delete.rs
    ├── detection/
    │   └── mod.rs
    └── editor/
        └── mod.rs
```

- Put domain models and enums in `model.rs`.
- Put schema creation and migration definitions in `schema.rs`.
- Put SQL in `insert.rs`, `select.rs`, `update.rs`, or `delete.rs` according to the operation.
- Put database commands and database-state orchestration in `database/commands.rs`.
- Re-export only types and constants needed by sibling modules from `database/mod.rs`.
- Create a domain directory when a feature has its own models or several operations. Use one `mod.rs` for a small cohesive domain.
- Do not place feature implementation, SQL, or large data types in `main.rs` or `lib.rs`.
- Update a module's `documentation.md` when its responsibilities or public operations change.
