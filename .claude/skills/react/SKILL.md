---
name: react
description: Mandatory implementation contract for creating, modifying, reviewing, or debugging React, React Native, Expo, Next.js, Vite, and TypeScript frontends. Use for components, pages, features, domains, state, services, APIs, styling, build configuration, source import aliases, Storybook stories, tests, or UI architecture that must follow Atomic Design, Domain-Driven Design, Separation of Concerns, React Context, Zod, Vitest, and Bomber MCP generation.
metadata:
  title: React Development Contract
  summary: Enforces domain analysis, atomic decomposition, Bomber MCP generation, implementation boundaries, validation, and a strict frontend Definition of Done.
  version: 2.8.0
  author: René Krewinkel
  priority: critical
  enforcement: strict
  scope: project-wide
  applies_to:
    - react
    - react-native
    - expo
    - nextjs
    - typescript
    - frontend
    - ui-development
    - vite
  requires:
    - Atomic Design
    - Domain-Driven Design
    - Separation of Concerns
    - TypeScript
    - React Context
    - Storybook
    - Vitest
    - Zod
    - Bomber MCP
  governs:
    - architecture
    - folder-structure
    - component-generation
    - domain-generation
    - state-management
    - validation
    - testing
    - storybook
    - styling
    - source-import-aliases
  triggers:
    - create component
    - create feature
    - create page
    - create domain
    - build UI
    - implement frontend functionality
    - add state
    - add service
    - add API
    - review React code
    - debug React code
    - configure a Vite React application
    - configure source imports
  keywords:
    - atomic-design
    - ddd
    - bomber
    - bomber-mcp
    - react
    - react-native
    - expo
    - nextjs
    - typescript
    - storybook
    - vitest
    - zod
    - vite
    - source-alias
  success_criteria:
    - Bomber MCP is used for every supported resource
    - Atomic Design and domain boundaries are respected
    - TypeScript and Zod enforce internal and external contracts
    - Reusable components have Vitest tests and Storybook stories
    - Business logic remains outside UI components
    - Semantic or reusable native elements are represented by Atoms
    - Vite applications resolve the @ source alias in TypeScript and Vite
  failure_conditions:
    - A Bomber-supported resource is created manually
    - Domain Analysis or Atomic Analysis is skipped
    - A monolithic component is introduced
    - Business logic is placed in a UI component
    - Required validation, tests, or stories are missing
    - Raw semantic HTML is repeated instead of represented by Atoms
    - A Vite application configures the @ alias on only the TypeScript or Vite side
  agent_instructions: Follow Requirement Analysis, Domain Analysis, Atomic Analysis, Bomber Generation, Implementation, Validation, and Refinement in order. Stop and complete a missing prerequisite before proceeding.
  tags:
    - react
    - frontend
    - architecture
    - atomic-design
    - domain-driven-design
    - bomber-mcp
---

# React development contract

Follow this contract for every in-scope frontend change. Do not skip, reorder, or silently simplify mandatory steps.

## Read the relevant references

Read these files before changing code:

- Read [workflow-and-generation.md](references/workflow-and-generation.md) for every implementation task. It defines requirement analysis, domain analysis, atomic analysis, and mandatory Bomber MCP generation.
- Always read and follow [component-structure.md](references/component-structure.md) for every React implementation, review, or debugging task. Its critical structure rules apply alongside the architecture rules, even when the task does not explicitly mention component organization.
- Read [architecture-and-components.md](references/architecture-and-components.md) when designing or changing domains, layers, components, state, or native element wrappers.
- Read [quality-and-definition-of-done.md](references/quality-and-definition-of-done.md) before implementation and again before completion. It defines TypeScript, validation, styling, tests, Storybook, and completion checks.
- Invoke and follow the standalone `configure-src-alias` skill whenever creating or configuring a Vite application, changing TypeScript or Vite configuration, or introducing imports from `src`. Its exact two-sided `@` alias contract is mandatory.
- Invoke and follow the standalone `atomic-resources-components` skill whenever creating or updating UI components in a project that uses `create-atomic-resources`, generated resource CSS variables, Sass resource utilities, or `atomic-bomb` component structure.
- Invoke and follow the standalone `scss` skill whenever creating, updating, or reviewing React component SCSS partials, variants, responsive rules, or Sass barrels. Do not apply it to React Native styling.

For a review-only task, read the references governing the reviewed code and report violations. Do not mutate code unless the user asks for changes.

## Primary objective

Create predictable frontends using:

- Atomic Design
- Domain-Driven Design
- Separation of Concerns
- TypeScript
- React Context
- Zod
- Storybook
- Vitest
- Bomber MCP

## Mandatory execution order

Use this sequence:

```text
1. Requirement Analysis
2. Domain Analysis
3. Atomic Analysis
4. Bomber Generation
5. Implementation
6. Validation
7. Refinement
```

Do not begin implementation before steps 1 through 4 are complete.

## Core constraints

- Assign every component to exactly one Atomic Design layer: atom, molecule, organism, template, or page.
- Choose the lowest reusable atomic level.
- Identify domains before creating UI.
- Generate every Bomber-supported resource through Bomber MCP; do not create one manually.
- Keep business rules, API calls, validation, and data transformation out of UI components.
- Validate all external data with Zod.
- Use React Context for global state.
- Add Vitest and React Testing Library coverage for every reusable component.
- Add Storybook stories for every reusable component.
- Do not use Tailwind, inline styles, Styled Components, or CSS-in-JS.
- Do not repeat raw semantic HTML elements in higher-level components; create or reuse the matching Atom.
- In every Vite-based application, configure the `@` alias to the repository `src` directory in both `tsconfig.app.json` and `vite.config.ts`. Configuring only one side is a failure.

## Completion gate

Complete a feature only when all relevant items in [quality-and-definition-of-done.md](references/quality-and-definition-of-done.md) pass. If a required tool or check is unavailable, report the exact constraint and run every remaining check.
