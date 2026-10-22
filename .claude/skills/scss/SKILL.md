---
name: scss
description: Create, update, or review SCSS component styles for React applications, especially projects generated with atomic-bomb. Use when adding React components, editing `*.style.scss` partials, organizing BEM-like component selectors and `data-object-type` variants, adding responsive S/M/L/XL rules, or checking Sass `_index.scss` barrels and stylesheet inclusion.
metadata:
  title: SCSS Component Styles
  summary: Enforces colocated React SCSS partials, predictable selector nesting, responsive rules, and verified Sass barrels.
  version: 1.1.0
  author: René Krewinkel
  priority: high
  enforcement: strict
  scope: project
  applies_to:
    - React component styles
    - SCSS partials
    - atomic-bomb projects
    - Sass barrels
    - responsive component styling
  requires:
    - one SCSS partial per React component
    - component-root selector nesting
    - verified Sass barrel inclusion
  governs:
    - component stylesheet naming
    - SCSS selector structure
    - data-object-type variants
    - component breakpoints
    - Sass barrel integrity
  triggers:
    - create a React component
    - add component styles
    - edit a style.scss partial
    - add an SCSS variant
    - add responsive component styles
    - verify an atomic-bomb barrel
  keywords:
    - scss
    - sass
    - react
    - component-styling
    - atomic-bomb
    - bem
    - responsive-design
    - sass-barrels
  success_criteria:
    - every React component has the correctly named colocated SCSS partial
    - component elements and variants remain nested under one root selector
    - responsive rules use the repository breakpoint contract without accidental cascade conflicts
    - each component partial is included by an inspected Sass barrel
    - the effective Sass entrypoint compiles
  failure_conditions:
    - a component stylesheet uses an unrelated filename or global selector
    - variant nesting compiles to a malformed selector
    - a partial is created without checking its barrel
    - responsive overrides silently conflict because of query ordering
    - Sass validation is skipped
  agent_instructions: Inspect the existing Sass pipeline first, keep each React component in its matching partial, nest elements and variants beneath the component root, verify the actual `_index.scss` barrel contents, and compile the effective Sass entrypoint before completion.
  tags:
    - frontend
    - react
    - scss
    - components
    - atomic-bomb
---

# SCSS component styles

Apply this contract to React components styled with SCSS. Assume `atomic-bomb` conventions when the project exposes them; otherwise keep the same partial, selector, responsive, and verification rules within the project's existing Sass pipeline.

## Inspect before editing

1. Locate the component, its current style imports, nearby component folders, Sass barrels, and the effective Sass entrypoint.
2. Read the relevant `_index.scss` files completely. Do not infer barrel contents from filenames.
3. Inspect `package.json` or the project's build configuration for the canonical Sass command.
4. Preserve an established project convention when it is more specific than this skill, and report the difference when it prevents this contract from being applied exactly.
5. When `create-atomic-resources` or generated resource tokens are present, also load and follow `atomic-resources-components`; that skill owns token values and resource generation, while this skill owns component partial structure and barrel integrity.

## Create the component partial

For every React component named `<Component>`, create or maintain a colocated `_<Component>.style.scss` partial. Preserve the component's exact case.

```text
Button/
|-- Button.tsx
|-- _Button.style.scss
|-- _index.scss
`-- index.tsx
```

Use one component root class matching the component name, such as `.Button`. Nest its elements, state selectors, variants, and media queries inside that root. Do not spread one component's rules across unrelated partials.

Read [component-partial-pattern.md](references/component-partial-pattern.md) whenever creating or changing a component partial, variant, subcomponent, responsive rule, or Sass barrel. It contains the required selector pattern, breakpoint contract, and barrel checks.

## Verify the barrel

For each component partial:

1. When `atomic-bomb` is present, confirm that the colocated `_index.scss` exists; restore it if it is missing. In other projects, preserve component barrels whenever the existing layout uses them.
2. Read its contents and verify that it loads or forwards the component partial exactly once with the syntax already used by adjacent components.
3. Follow parent barrels through to the effective Sass entrypoint. A correct local barrel that is never consumed is incomplete.
4. Add only the missing `@use` or `@forward`; do not replace a working barrel style or duplicate inclusion elsewhere.
5. Only outside `atomic-bomb`, if the project does not use Sass barrels, verify the explicit import path that includes the partial instead and do not invent an isolated barrel that the build never consumes.

## Validate

Run the project's existing Sass or build command after changing SCSS. Prefer a declared package script. If none exists, identify the actual entrypoint and run Sass directly, for example:

```shell
npx sass --quiet --no-source-map <entrypoint.scss> <output.css>
```

Also run the component or application checks affected by the change. Before completion, confirm:

- The component partial exists with the exact `_<Component>.style.scss` name.
- The component root, elements, variants, and responsive overrides follow the reference pattern.
- Variant element selectors compile to selectors that can match the component markup.
- The component `_index.scss` and every required parent barrel were inspected.
- The partial reaches the effective Sass entrypoint exactly once.
- Sass compilation and applicable tests pass.
