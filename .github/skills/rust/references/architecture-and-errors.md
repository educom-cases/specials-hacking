---
title: Rust Architecture and Error Boundaries
description: Crate layout, module ownership, public API, typed models, errors, async work, configuration boundaries, and documentation rules.
summary: Keeps generic Rust code cohesive, testable, explicit, and independent from executable or framework orchestration.
version: 1.0.0
author: René Krewinkel
parent_skill: rust
enforcement: strict
read_when:
  - creating or restructuring a crate
  - designing a public API
  - adding errors or async behavior
  - reviewing Rust architecture
governs:
  - crate structure
  - modules
  - public APIs
  - error handling
  - async boundaries
  - documentation
---

# Rust architecture and error boundaries

## Crate roles

For a binary with reusable behavior:

```text
.
├── Cargo.toml
├── Cargo.lock
├── src/
│   ├── main.rs
│   ├── lib.rs
│   ├── config.rs
│   ├── error.rs
│   └── <domain>/
│       ├── mod.rs
│       ├── model.rs
│       └── service.rs
└── tests/
    └── <public-behavior>.rs
```

- `main.rs` parses process inputs, constructs dependencies, starts runtimes, calls the library, reports the top-level error, and chooses an exit code.
- `lib.rs` declares modules and deliberately re-exports the public surface. It must not contain unrelated feature implementations.
- A small domain may remain one module. Split only when responsibilities or independent tests justify it.
- Keep adapters for databases, filesystems, networks, CLIs, and frameworks at boundaries around domain behavior.

For a workspace, give every member one reason to exist. Put shared dependency versions and lints in workspace metadata when doing so reduces drift.

## Public API

- Keep items private until a consumer needs them.
- Prefer domain names over implementation names.
- Use newtypes where raw strings or integers have domain invariants.
- Use enums for closed state sets and handle every variant explicitly.
- Avoid exposing dependency-specific types unless the crate intentionally acts as an adapter for that dependency.
- Document public behavior, errors, panics, safety requirements, and important examples.
- Treat a public signature change as a compatibility decision, not a local refactor.

## Errors

- Return `Result` for expected operational failure.
- Define typed library errors when callers need to inspect failure categories.
- Use an application-level context aggregator such as `anyhow` only at executable or orchestration boundaries.
- Preserve the original error source and add action-oriented context at I/O, parsing, configuration, database, and network boundaries.
- Do not use `unwrap`, `expect`, `panic!`, `todo!`, or `unimplemented!` for production input or recoverable operational failure.
- A deliberate invariant panic must be locally obvious and covered by tests.
- Map errors once at each architectural boundary. Avoid stringifying early.

## Async and blocking work

- Use async only across actual asynchronous I/O or coordination boundaries.
- Do not hold mutex guards across `.await`.
- Keep blocking filesystem, database, compression, or CPU-heavy work off async executor workers; use the runtime's blocking facility or a dedicated worker.
- Apply timeouts and cancellation behavior to network operations when the caller can otherwise wait indefinitely.
- Bound channels, concurrency, retries, and result sizes.
- Keep async runtime setup in the executable boundary rather than embedding it in pure domain code.

## Data and configuration

- Parse external data into boundary types, validate it, and convert it into domain types.
- Keep serialization naming and backward compatibility explicit.
- Never hard-code expanded user-home or platform configuration directories.
- Keep credentials out of committed configuration and logs.
- Make absent, malformed, and incompatible configuration distinct outcomes when they require different recovery.

## Documentation

- Keep crate-level docs aligned with actual purpose and examples.
- Include `# Errors` and `# Panics` sections where public behavior warrants them.
- Use doctests for stable, compact public API examples.
- Update module or architecture documentation when ownership changes.
