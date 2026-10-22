---
title: React Workflow and Bomber Generation
description: Mandatory pre-implementation analysis and generation workflow for the React skill.
summary: Defines the required outputs and failure conditions for requirement analysis, domain analysis, atomic analysis, and Bomber MCP generation.
version: 2.5.0
author: René Krewinkel
parent_skill: react
applies_to:
  - feature implementation
  - component creation
  - page creation
  - domain creation
  - state and service creation
enforcement: strict
read_when:
  - before every implementation task
  - before generating frontend resources
---

# Workflow and generation

## Contents

- Requirement Analysis
- Domain Analysis
- Atomic Analysis
- Native HTML element analysis
- Bomber Generation
- Implementation gate

## Requirement Analysis

Identify the business capability, user goal, required state, required services, and required UI.

Produce:

```text
Requirement Summary

Business Capability:
...

User Goal:
...

Required State:
...

Required Services:
...

Required UI:
...
```

## Domain Analysis

Identify domains before creating UI. Examples include Authentication, Commerce, Checkout, Inventory, Customer, Profile, and Orders.

For each identified domain, determine whether it needs:

```text
api
events
hooks
models
services
state
```

Produce:

```text
Domains

Authentication
    Models
    Services
    State

Customer
    Models
    Services
    State
```

Creating UI before identifying domains is a failure.

## Atomic Analysis

Before generating a component, ask:

```text
Can this be an Atom?
Can this be a Molecule?
Can this be an Organism?
```

Choose the lowest reusable level. Identify dependencies from lower to higher levels:

```text
Atoms:
- Button
- Label
- Input

Molecules:
- LoginForm

Organisms:
- LoginPanel

Templates:
- AuthenticationTemplate

Pages:
- LoginPage
```

Do not create a Molecule before its required Atoms exist. Do not create an Organism before its required Molecules exist.

If the project uses `create-atomic-resources`, generated resource CSS variables, Sass resource utilities, or `atomic-bomb` component structure, load and follow the standalone `atomic-resources-components` skill before generating or editing components.

## Native HTML element analysis

Represent every reusable, semantic, interactive, or presentational native HTML element with an Atom:

```text
button      -> Button
input       -> Input
label       -> Label
p           -> Paragraph
h1-h6       -> Heading
img          -> Image
a            -> Link
ul           -> List
ol           -> OrderedList
li           -> ListItem
span         -> Text
strong       -> StrongText
em           -> EmphasisText
small        -> SmallText
blockquote   -> Blockquote
code         -> Code
pre          -> PreformattedText
textarea     -> TextArea
select       -> Select
option       -> Option
form         -> Form
table        -> Table
thead        -> TableHead
tbody        -> TableBody
tr           -> TableRow
td           -> TableCell
th           -> TableHeaderCell
hr           -> Divider
```

Raw `div`, `section`, `main`, `article`, `aside`, `header`, `footer`, and `nav` elements may remain only when they are purely structural. Promote a structural element to an Atom, Molecule, or Organism when it gains styling, behavior, configuration, or reuse requirements.

Using reusable raw semantic elements directly in Molecules, Organisms, Templates, or Pages is a failure.

## Bomber Generation

If Bomber MCP supports a resource, generate it through Bomber MCP. Do not create it manually.

Generate required lower-level resources before their consumers:

1. Native-element and application Atoms
2. Molecules
3. Organisms
4. Templates
5. Pages
6. Domain and shared resources

Bomber-supported resources are:

```text
Atomic: atom, molecule, organism, template, page
Shared: hook, lib
Domain: api, event, helper, hook, model, service, state
```

Manual creation of a supported resource is a failure. Creating higher-level UI before the required semantic-element Atoms is also a failure.

## Implementation gate

Begin implementation only after:

- domains are identified
- atomic decomposition is complete
- required native-element Atoms exist
- Bomber generation is complete
