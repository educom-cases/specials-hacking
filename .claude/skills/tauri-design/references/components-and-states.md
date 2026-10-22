---
title: Tauri Workbench Components and States
description: Controls, fields, lists, chips, editors, previews, chat, empty states, selection, accessibility, and complete interaction-state rules.
summary: Defines how compact Atomic Design components behave consistently inside the dark workbench shell.
version: 1.1.0
author: René Krewinkel
parent_skill: tauri-design
enforcement: strict
read_when:
  - implementing UI components
  - adding interactive or content states
  - reviewing accessibility and desktop behavior
---

# Components and states

## Contents

- Component contract
- Buttons and icons
- Fields and selectors
- Lists and metadata
- Chips and tags
- Editors and previews
- Tasks and notes
- Chat
- Empty, loading, and error states
- Selection and accessibility

## Component contract

Build reusable Atoms, Molecules, Organisms, Templates, and Pages according to the React contract. Express visual variants through semantic props and stable attributes such as `data-object-type`, `data-state`, `data-role`, and `aria-*`.

Keep SCSS colocated with the owning component and consume shared semantic tokens. Do not add inline styles or raw visual literals in JSX.

## Buttons and icons

Base buttons use:

- transparent background
- no border
- 4px radius
- white text
- inline-flex alignment
- `0.5rem` internal gap
- compact `4px 12px` padding

Variants:

- primary and active: blue fill
- secondary: 10% white fill
- icon-only: at least 2rem square, 6px padding, 60% idle opacity
- destructive: danger semantics without a permanently loud surface
- disabled: 5% white fill, muted text, `not-allowed` cursor

On hover, focus, active, and selected states, increase clarity without shifting layout. Use `aria-pressed` for toggles. Add tooltips when an icon's meaning is not immediately universal.

## Fields and selectors

Inputs, textareas, and selects use:

- `#282c34` background
- one-pixel 10% white border
- 6px radius
- white text
- regular sans-serif
- `10px 12px` padding
- full available width

Implement a visible `:focus-visible` ring using the primary blue plus sufficient contrast. Placeholder text must remain distinguishable from entered values.

Textarea defaults:

- 10rem minimum for document content
- 3–4rem minimum for inline task, note, or chat composition
- vertical resizing only when the surrounding layout can accommodate it

Use a consistent dark theme for third-party selects. Match their control height, surface, border, menu, focus, and option selection to native fields.

## Lists and metadata

Use full-width list rows rather than individual floating cards:

- 6px radius
- `10px` padding
- `2px 8px` outer spacing
- `0.625rem` internal gap
- transparent default surface
- blue selected surface
- blue or subtle-white hover surface

Give each row a clear primary title and muted monospace metadata. Clamp or wrap deliberately; never let long content force pane width.

Place destructive row actions at the far edge and prevent them from triggering row selection. Confirm irreversible deletion through a native or accessible modal.

## Chips and tags

Use pill geometry for compact taxonomy:

- neutral fill and border at approximately 8% white
- monospace small or tiny text
- `0.25rem 0.6rem` interactive padding
- blue active and hover state

Prefix tags consistently when the product uses hash semantics. Wrap tag clouds with `0.5rem` gaps. Avoid turning chips into the dominant visual element.

## Editors and previews

Treat code editing as the primary surface, not an embedded widget:

- remove conflicting third-party borders and radii
- let editor, theme wrapper, and editor root all flex to full height
- use monospace and a 1.6 line-height
- preserve gutters, folding, matching, completion, active-line, and selection visibility
- expose zoom through bounded toolbar controls

Rendered content must use a contained typography system. Sanitize or safely render user-controlled Markdown and HTML.

Media preview uses a checkerboard only to communicate transparency. Provide meaningful alternative text when the image conveys content.

## Tasks and notes

Use compact inline composition:

- content field grows
- create/save control remains at the edge
- list scrolls independently
- each task uses a subtle 4% white surface and 6px radius
- completion uses active state plus accessible semantics
- editing occurs in place without changing pane structure

Do not hide save, cancel, or deletion consequences.

## Chat

Use the wider context pane. Keep:

- messages in an independently scrolling column
- composer fixed at the bottom behind a subtle top border
- assistant messages left-aligned on an 8% white surface
- user messages right-aligned on the primary blue surface
- maximum assistant width around 88%
- narrower user messages when content permits
- small `1.45` line-height and `0.55rem 0.7rem` padding

Place copy or create-from-result actions below assistant output. Use a restrained loader inside an assistant-style bubble.

## Empty, loading, and error states

Empty states use one concise muted monospace sentence close to the affected region. Explain the next action:

- create or paste the first item
- select an item to manage attached data
- add tags to populate a cloud
- ask a first question

Loading states must preserve layout. Disable duplicate actions and show localized progress.

Errors must identify the failed operation and recovery path. Use danger color plus text or icon; do not rely on color alone.

## Selection and accessibility

Disable accidental selection across chrome, toolbars, and pane furniture. Restore text selection for:

- editors
- inputs and textareas
- selects
- rendered previews
- chat transcripts
- media previews
- dialogs
- editable content

Every interactive element must support:

- keyboard reachability
- visible focus
- accessible name
- programmatic state
- adequate hit target
- non-color feedback

Respect reduced motion. Preserve contrast for muted text, separators, and disabled controls under the actual webview renderer.
