---
title: Mandatory Tauri React Design Tokens
description: Absolute installation, ownership, generation, usage, and verification contract for the canonical Tauri React token asset.
summary: Makes the packaged tokens.json file the immutable source of truth for every React frontend hosted by a Tauri v2 application.
version: 1.1.0
author: René Krewinkel
parent_skill: tauri-design
priority: critical
enforcement: absolute
scope:
  - tauri-v2 applications with React frontends
  - new application creation
  - design-system configuration
read_when:
  - before styling a Tauri React application
  - when creating or configuring design tokens
  - when reviewing a Tauri React frontend
success_criteria:
  - canonical token asset exists at the required destination
  - downstream styles are derived from the token asset
  - exact-byte verification passes
failure_conditions:
  - a Tauri React app defines a competing token source
  - the required token file is absent or modified
  - components bypass available semantic tokens with literals
---

# Mandatory Tauri React tokens

Apply this contract only when Tauri v2 hosts a React frontend. Do not impose this token file on clean React, Next.js, Expo, React Native, or other non-Tauri applications.

## Canonical source

The packaged asset is:

```text
<tauri-design-skill>/assets/tokens.json
```

Its required project destination is:

```text
<application-root>/src/resources/design/tokens.json
```

The packaged JSON is the absolute source of truth. If prose examples, generated SCSS, legacy tokens, or component literals disagree with it, the packaged JSON wins.

Do not manually recreate or normalize the file. Preserve its keys, values, ordering, and exact bytes.

## Mandatory installation

Before implementing application styling, run:

```shell
python3 <tauri-design-skill>/scripts/install_tokens.py \
  --project-root <application-root>
```

For a deliberate migration of an existing different token file, inspect the differences first and then run:

```shell
python3 <tauri-design-skill>/scripts/install_tokens.py \
  --project-root <application-root> \
  --force
```

Do not use `--force` without understanding the affected generated styles and component contracts.

## Ownership

Treat `src/resources/design/tokens.json` as the canonical design input:

- generate SCSS variables, CSS custom properties, typed token maps, or documentation from it
- never edit generated outputs as the source
- do not introduce a second token JSON file
- do not redefine available colors, spacing, radii, shadows, typography, opacity, z-index, or form states as scattered literals
- add a token upstream when a genuinely new semantic value is required

Changing the canonical asset in this skills repository is a design-system change. Changing only a downstream application copy is a failure.

## Required token domains

Consume the supplied domains:

- transparent page foundation
- dark application surfaces and editor layers
- primary, secondary, disabled, warning, and semantic states
- semantic icon colors
- language and content-type colors
- native-style traffic-light colors
- regular, bold, link, label, and heading typography
- compact desktop spacing scale
- control, panel, modal, and pill radii
- modal shadow
- semantic success, warning, danger, and information colors
- base, select, and modal z-index layers
- hidden, disabled, muted, backdrop, and full opacity
- input, focus, disabled, and error form contracts

Use semantic token names in components. Avoid coupling component names to raw color values.

## Generation

When the application generates SCSS:

1. Read only the canonical JSON.
2. Generate into an established derived file such as `src/resources/styles/tokens/_tokens.scss`.
3. Keep generation deterministic.
4. Make the generated file reproducible from a clean checkout.
5. Run generation before builds when the repository workflow expects committed derived output.

Do not edit the generated SCSS instead of the JSON.

## Verification

Verify exact bytes:

```shell
python3 <tauri-design-skill>/scripts/install_tokens.py \
  --project-root <application-root> \
  --check
```

Then verify:

1. JSON parsing succeeds.
2. Token generation succeeds.
3. TypeScript and Vite builds succeed.
4. Components consume generated semantic variables.
5. The Tauri webview renders transparent roots, layered surfaces, fields, controls, modals, and state colors correctly.

## Completion gate

Do not report a Tauri v2 + React application complete unless:

- the exact canonical asset exists at `src/resources/design/tokens.json`
- the installer check passes
- derived token output is current
- no competing token source exists
- component styling uses the canonical semantic values
- browser and native Tauri design verification pass
