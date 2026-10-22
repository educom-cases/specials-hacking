---
name: configure-src-alias
description: Configure, repair, review, or verify the exact @ source import alias for a Vite and TypeScript application. Use when a repository needs @/... imports to resolve consistently, when creating or changing tsconfig.app.json or vite.config.ts, when replacing deep relative imports, or when TypeScript and Vite disagree about source-module resolution.
metadata:
  title: Configure @ Source Alias
  summary: Enforces one exact @ alias to the repository src directory across TypeScript type-checking and Vite development and production builds.
  version: 1.1.0
  author: René Krewinkel
  priority: critical
  enforcement: absolute
  scope: project-wide
  applies_to:
    - vite
    - typescript
    - react
    - frontend
    - source-imports
  requires:
    - tsconfig.app.json
    - vite.config.ts
    - src directory
  governs:
    - baseUrl
    - TypeScript paths
    - Vite resolve aliases
    - source import style
  triggers:
    - configure @ alias
    - configure source imports
    - create Vite application
    - update tsconfig.app.json
    - update vite.config.ts
    - replace deep relative imports
    - fix module resolution
  keywords:
    - vite
    - typescript
    - source-alias
    - path-alias
    - import-alias
    - baseurl
    - node-url
  success_criteria:
    - TypeScript resolves @ imports during type-checking
    - Vite resolves @ imports during development and builds
    - "@ points only to the repository src directory"
    - existing configuration remains intact
  failure_conditions:
    - only TypeScript is configured
    - only Vite is configured
    - the alias name differs from @
    - "@ points outside the repository src directory"
    - existing configuration is replaced instead of merged
  agent_instructions: Configure both TypeScript and Vite with the exact @ alias, preserve unrelated configuration, verify an @ import through type-checking and Vite, and do not report completion when only one resolver works.
  tags:
    - vite
    - typescript
    - source-alias
    - configuration
---

# Configure the `@` source alias

Apply this contract as an absolute MUST for Vite and TypeScript applications. Do not apply Vite-specific configuration to Next.js, Expo, React Native, or another stack that does not use Vite.

## Goal

Make `@/...` imports resolve consistently during TypeScript type-checking, Vite development, and Vite production builds.

## Required files

Update both:

1. `tsconfig.app.json`
2. `vite.config.ts`

Do not complete application configuration when only one file is wired.

## TypeScript configuration

Set `baseUrl` to the repository root and map `@/*` only to `src/*`:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

Merge these keys into the existing `compilerOptions`. Preserve unrelated compiler options and the repository's formatting style.

The required values are exact:

```text
baseUrl = .
alias = @/*
target = ./src/*
```

## Vite configuration

Import the Node URL helpers:

```ts
import { fileURLToPath, URL } from 'node:url'
```

Add or merge this resolver into the exported Vite configuration:

```ts
resolve: {
  alias: {
    '@': fileURLToPath(new URL('./src', import.meta.url))
  }
}
```

Preserve existing plugins, server settings, build settings, other aliases, and formatting. If `resolve` or `alias` already exists, merge the `@` entry instead of replacing the object.

The Vite alias must:

- be named exactly `@`
- resolve through `fileURLToPath(new URL('./src', import.meta.url))`
- point only to the repository `src` directory

Do not substitute a working-directory-dependent relative string. Do not wire `@` to the repository root.

## Import usage

Prefer `@/...` for imports that would otherwise cross multiple directory levels.

Replace:

```ts
import Button from '../../../components/Button'
```

With:

```ts
import Button from '@/components/Button'
```

Keep short same-directory relative imports when they communicate local ownership more clearly.

## Verification

Verify all three resolution surfaces:

1. Type-check a real `@/...` import.
2. Start or build through Vite.
3. Confirm the imported module loads at runtime.

Run the repository's normal TypeScript and Vite checks. At minimum:

```shell
tsc --noEmit
npm run build
```

Use the package manager and scripts already selected by the repository.

## Completion gate

Do not report configuration complete unless:

- `tsconfig.app.json` contains exact `baseUrl` and `paths` values
- `vite.config.ts` imports `fileURLToPath` and `URL` from `node:url`
- `vite.config.ts` maps exact alias `@` to `./src`
- existing configuration remains intact
- TypeScript and Vite checks pass
