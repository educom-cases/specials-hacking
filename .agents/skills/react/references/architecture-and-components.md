---
title: React Architecture and Component Rules
description: Layer boundaries, Atomic Design responsibilities, state rules, and component composition requirements for the React skill.
summary: Keeps UI, application, domain, and infrastructure concerns separate while enforcing a project-wide Atom contract.
version: 2.4.0
author: René Krewinkel
parent_skill: react
enforcement: strict
read_when:
  - changing architecture or folder structure
  - creating or modifying components
  - adding state, services, APIs, or domain logic
governs:
  - separation of concerns
  - atomic design
  - component syntax
  - global state
---

# Architecture and components

## Contents

- Layer boundaries
- Atomic Design
- Atom rules
- Higher-level composition
- Components and state

## Layer boundaries

### UI layer

The UI layer renders, composes, and exposes styling hooks. It must not contain API calls, business rules, validation logic, or data transformation.

### Application layer

The application layer orchestrates workflows and coordinates state. Place it in hooks and services.

### Domain layer

The domain layer owns business rules, domain models, validation, and business policies. Place it under `domains/*`.

### Infrastructure layer

The infrastructure layer owns API calls, storage, and external systems. Place it in API and service modules.

## Atomic Design

Assign every component to exactly one of:

```text
atom
molecule
organism
template
page
```

Do not introduce exceptions or ambiguous cross-layer components.

## Atom rules

An Atom must:

- have one responsibility
- be reusable
- contain no business logic or API calls
- be independently testable
- wrap native HTML when the element is semantic, reusable, interactive, or repeated
- provide the project-wide implementation contract for its native element

Create or reuse these Atoms when the application needs their semantics:

```text
Button
Input
Label
Paragraph
Heading
Image
Link
Text
StrongText
EmphasisText
SmallText
List
OrderedList
ListItem
TextArea
Select
Option
Form
Table
TableHead
TableBody
TableRow
TableCell
TableHeaderCell
Divider
Icon
Avatar
Badge
```

Do not repeat raw semantic HTML throughout the application.

Purely structural `div`, `section`, `main`, `article`, `aside`, `header`, `footer`, and `nav` elements may remain raw for simple layout composition. Promote them when they become reusable, configured, styled, or behavior-driven.

Forbidden:

```tsx
<button>Save</button>
<label>Name</label>
<input />
<h1>Title</h1>
<p>Description</p>
```

Required:

```tsx
<Button text="Save" />
<Label text="Name" />
<Input name="name" />
<Heading text="Title" />
<Paragraph text="Description" />
```

## Higher-level composition

- Molecules combine Atoms. They may contain local UI behavior, but not business logic or API calls. Examples: `LoginForm`, `SearchForm`, `ProductCard`.
- Organisms combine Molecules and Atoms. They must not contain domain logic, API calls, or data persistence. Examples: `Header`, `Navigation`, `CheckoutSummary`.
- Templates define page-level layout and composition without owning domain behavior.
- Pages connect application and domain behavior to templates while preserving the lower-level boundaries.

## Components and state

Use TypeScript arrow components:

```tsx
const Button = () => {}
```

Do not use function declarations for components:

```tsx
function Button() {}
```

Use React Context for global state and avoid prop drilling:

```text
state
├── AppContext.tsx
├── AppProvider.tsx
└── AppReducer.ts
```
