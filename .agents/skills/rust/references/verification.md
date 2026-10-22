---
title: Generic Rust Verification
description: Mandatory formatting, linting, checks, tests, documentation, dependency review, security review, and final architecture checks.
summary: Defines the evidence required before generic Rust work is complete.
version: 1.0.0
author: René Krewinkel
parent_skill: rust
priority: critical
enforcement: strict
read_when:
  - writing Rust tests
  - changing dependencies or features
  - reviewing Rust code
  - before reporting completion
governs:
  - rustfmt
  - clippy
  - cargo check
  - cargo test
  - cargo doc
  - dependency verification
---

# Generic Rust verification

## Test strategy

- Put focused unit tests beside private implementation.
- Put integration tests under `tests/` for public crate behavior.
- Test success, validation failures, operational errors, and boundary conversions.
- Test serialization representations that are persisted or consumed externally.
- Use temporary directories, ephemeral ports, and isolated test databases. Never mutate user configuration or production data.
- Keep network-dependent tests explicitly identified and bounded.
- Add compile-fail or doctest coverage when a public API contract is best expressed at compile time.

## Commands

Run from the crate or workspace root, adapting feature flags to project policy:

```shell
cargo fmt --all -- --check
cargo check --workspace --all-targets --all-features
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-targets --all-features
cargo doc --workspace --all-features --no-deps
```

Also run the repository's configured MSRV, platform matrix, feature-power-set, audit, deny, or unused-dependency checks when present.

Do not blindly use `--all-features` when features are intentionally incompatible. Run and document the supported combinations instead.

## Dependency review

For every dependency change:

1. Confirm the crate is actually used.
2. Confirm package identity and source URL.
3. Inspect enabled default and optional features.
4. Inspect duplicate major versions and platform requirements.
5. Confirm `Cargo.lock` changed only as expected.
6. Run the checks with the resulting resolved Git commit.
7. Review licenses and advisories using repository tooling when available.

For the preferred Codeberg crates, compare `Cargo.lock` source entries with the exact URLs in [preferred-codeberg-crates.md](preferred-codeberg-crates.md).

## Final review

Confirm:

- The crate role and module ownership are clear.
- `main.rs` and `lib.rs` remain small composition surfaces.
- Public items are intentional and documented.
- Ordinary failures return contextual errors.
- Async code does not hold locks across awaits or perform unbounded blocking work.
- Configuration and credentials are handled safely.
- Applicable preferred crates use the required Codeberg sources.
- Non-applicable preferred crates were not added.
- Tests do not touch user or production state.
- Formatting, checks, lints, tests, and docs pass.
