---
title: Tauri Workbench Shell and Layout
description: Custom chrome, workspace hierarchy, pane proportions, editor surfaces, status regions, dialogs, responsive behavior, and window-state requirements.
summary: Translates the Pastebook shell into a reusable desktop information architecture centered on one flexible work surface.
version: 1.1.0
author: René Krewinkel
parent_skill: tauri-design
enforcement: strict
read_when:
  - creating the application shell
  - changing custom chrome or pane layout
  - adding editors, previews, inspectors, status bars, or dialogs
---

# Shell and layout

## Contents

- Window surface
- Custom chrome
- Workspace
- Primary surface
- Contextual tools
- Status
- Dialogs
- Responsive behavior

## Window surface

Configure a transparent, undecorated Tauri window and keep `html`, `body`, `#root`, and the outer application template transparent. Draw exactly one visible full-height surface inside it.

The visible shell must:

- fill `100vh` and `100%` width
- use `overflow: hidden`
- use a 20px outer radius
- use `#24272d` as its base
- contain the chrome and workspace in one column
- avoid body padding or a second background behind rounded corners

Use an initial desktop canvas around 1600×900 for dense editor workflows, then choose minimum dimensions from actual feature usability rather than blindly fixing the minimum to the initial size.

## Custom chrome

Use a 40px top boundary:

```text
[close minimize maximize] [app icon] [app label] [draggable spacer] [global action groups]
```

Style it with:

- `#2d333f` background
- one-pixel bottom border at 8% white
- 12px horizontal padding
- `0.75rem` major gaps

Place the application identity beside the traffic lights, not in the workspace. Render the icon at approximately `1.25rem` high and the label in small bold muted text.

Keep interactive controls outside the effective drag target. Invoke `startDragging()` only for the primary mouse button and only when the event did not originate in a button, link, field, or interactive role.

Group global actions with compact icon buttons and 1px separators. Typical groups are:

1. navigation visibility
2. create
3. selection and clipboard
4. zoom
5. save
6. contextual tools
7. close current object

Do not put native window controls among application actions.

## Workspace

Compose one horizontal flex workspace below the chrome:

```text
navigation | primary surface | contextual tools
```

Every pane must use `min-height: 0` and control its own overflow. The primary surface must use `flex: 1` and `min-width: 0`.

### Navigation pane

Use a 292px fixed basis at desktop width. Include:

- a 36px title row
- a scrollable list body
- compact selected and hover states
- a zero-width collapsed state with opacity `0` and pointer events disabled

Use a one-pixel right separator. Do not place global settings in the list.

### Context pane

Use a 292px basis for metadata, tags, notes, and tasks. Use a 36px title row and one-pixel left separator.

For chat, documentation, or another reading-heavy tool, expand to `min(44vw, 520px)`.

Closing the pane must release its width completely. Switching tools should preserve the shared pane boundary instead of opening stacked drawers.

## Primary surface

Use `#282c34` for the central editor or work surface. It owns:

- optional editor toolbar
- main content/editor region
- optional media or rendered preview
- bottom status region

Do not put content in generic padded cards. Let the work surface fill available space.

### Code and text editors

Make the editor a flex child with `min-height: 0` and full width. Integrate editor gutters and active lines into the same surface:

- monospace content and gutters
- 1.6 line-height
- subtle 4% white active-line fill
- one-pixel translucent gutter separator

### Markdown preview

Place rendered Markdown beside the editor at approximately 42% width with a 20rem minimum. Use `#1f232b`, a left separator, `1.5rem` padding, and independent scrolling.

### Media preview

Place media above the editor when source text remains editable. Use:

- maximum 40% height
- minimum 12rem height
- centered `object-fit: contain`
- independent scrolling
- subtle checkerboard made from 4% white over `#1f232b`

Never let a large preview displace all editing controls.

## Contextual tools

Use one right pane with named views such as Details, Tags, Tasks, Notes, or Chat.

- Stack form fields with `0.75–1rem` gaps.
- Keep create/edit actions inline with their associated content.
- Use scrolling only in the list or message body, not the whole pane.
- Keep chat composition fixed below the scrolling transcript.
- Keep empty-state explanations inside the pane with compact margins.

## Status

Place a 36px status row at the bottom of the primary surface. Use the shell background, a subtle top border, and small uppercase monospace labels.

Divide it into:

- current object or selection on the left
- transient status near the center
- type/language, version, and settings on the right

Use a small semantic dot for type or language. Status must remain informative without becoming a second toolbar.

## Dialogs

Use a fixed modal backdrop at `rgba(8, 10, 14, 0.68)` and a centered shell-colored dialog:

- maximum width `28rem`
- 8px radius
- one-pixel 10% white border
- `0 18px 50px rgba(0, 0, 0, 0.45)` shadow
- separated compact header
- `0.875rem` body padding

Keep modal content text-selectable. Trap focus, restore focus on close, close through an explicit accessible control, and handle Escape when safe.

## Responsive behavior

At widths below approximately 1024px:

- reduce navigation to about 240px
- reduce ordinary context tools to about 280px
- limit chat to `min(50vw, 460px)`

Below approximately 768px, do not squeeze all three panes into columns. Collapse or overlay secondary panes and preserve the primary task. Tauri desktop products may enforce a sensible minimum window width when all features cannot remain usable.
