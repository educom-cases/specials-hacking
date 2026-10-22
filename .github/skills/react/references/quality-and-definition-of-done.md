---
title: React Quality and Definition of Done
description: Mandatory language, validation, styling, testing, Storybook, and completion requirements for the React skill.
summary: Provides the pre-code and final verification gates used to decide whether frontend work is complete.
version: 2.5.0
author: René Krewinkel
parent_skill: react
enforcement: strict
read_when:
  - before implementation
  - while adding validation, styles, tests, or stories
  - while configuring a Vite application
  - before reporting completion
governs:
  - typescript
  - zod
  - styling
  - vitest
  - storybook
  - definition of done
  - source-import-aliases
---

# Quality and Definition of Done

## TypeScript

Use TypeScript. Do not use `any`. Prefer explicit `type`, `interface`, and `enum` declarations where appropriate.

## Validation

Validate all external data with Zod before application or domain code consumes it:

```ts
const UserSchema = z.object({
  id: z.string(),
  name: z.string()
})
```

Using unvalidated API or external data is a failure.

## Styling

Do not use:

- Tailwind
- inline styles
- Styled Components
- CSS-in-JS

Prefer:

- SCSS
- CSS Modules
- design tokens

When component styles use SCSS, the standalone `scss` skill owns component partial naming, selector nesting, responsive rules, and Sass barrel verification. When the project also uses `create-atomic-resources`, generated resource CSS variables, Sass resource utilities, or `atomic-bomb` component structure, the standalone `atomic-resources-components` skill owns token usage, resource stylesheet imports, Sass utility usage, and token/CSS rebuild checks.

## Testing

Give every reusable component a colocated `Component.test.tsx` file. Use Vitest and React Testing Library.

## Storybook

Give every reusable component a colocated `Component.stories.tsx` file. Include default, variant, and edge-case stories.

## Pre-code checklist

Before writing implementation code, verify:

- Requirement Analysis is complete.
- Domain Analysis is complete.
- Atomic Analysis is complete.
- Bomber Generation is complete.
- Required native-element Atoms are generated.
- No reusable native HTML element is used directly.
- Every Vite application has the mandatory `@` source alias configured in both TypeScript and Vite.
- `atomic-resources-components` has been loaded when the project uses `create-atomic-resources`, generated resource CSS variables, Sass resource utilities, or `atomic-bomb` component structure.
- `scss` has been loaded when React component styles use SCSS.

Stop and complete any missing item.

## Definition of Done

A feature is complete only when:

- Domain structure is generated.
- Atomic structure is generated.
- Bomber MCP generated every supported resource.
- Required native-element Atoms exist.
- Native HTML elements are wrapped where required.
- TypeScript passes.
- Zod validation covers external data.
- Vitest tests pass.
- Storybook stories cover default, variants, and edge cases.
- No inline styles, Tailwind, Styled Components, or CSS-in-JS are introduced.
- No duplicated UI or repeated raw semantic HTML is introduced.
- No business logic exists inside UI components.
- Atomic Design and domain boundaries are respected.
- Vite applications resolve `@/...` imports through both `tsconfig.app.json` and `vite.config.ts`.
- Resource token, Sass, and CSS checks from `atomic-resources-components` pass when that skill applies.
- Component partial, selector, responsive, barrel, and compilation checks from `scss` pass when that skill applies.
