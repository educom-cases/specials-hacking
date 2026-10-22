# Component partial pattern

Use this pattern for React component SCSS partials. Adapt element names and declarations to the component, but keep the structural order.

## Base, elements, and variants

```scss
.Button {
  display: flex;
  flex-direction: row;

  // Subcomponents
  &__text-label {
  }

  &__icon {
  }

  // Variations
  &[data-object-type='primary'] {
    // Use the concrete element selector inside a variant.
    .Button__text-label {
    }

    .Button__icon {
    }
  }

  &[data-object-type='secondary'] {
    .Button__text-label {
    }

    .Button__icon {
    }
  }
}
```

Do not write `&__text-label` inside `&[data-object-type='primary']`. Sass combines that suffix with the complete outer selector and produces a malformed selector such as `.Button[data-object-type='primary']__text-label`. Use `.Button__text-label` inside the variant block so the result selects an element within the varied component.

Use the same component root class in JSX. Put `data-object-type` on that root element. Keep variant names aligned with the component's TypeScript union or runtime values; do not introduce misspellings such as `secodary`.

Omit empty selectors from production output. The empty blocks above show placement only; create a block when it has a declaration or a nested rule.

## Responsive rules

Use these named ranges unless the project defines a more specific breakpoint contract:

| Name | Range |
| --- | --- |
| S - Tablet | up to `768px` |
| M - Tablet/Laptop | `769px` through `1024px` |
| L - High Res | `1025px` through `1200px` |
| XL - Ultra High Res | `1201px` and above |

Keep responsive rules inside the component root and order them S, M, L, XL. Use non-overlapping ranges so later rules do not override smaller-screen rules accidentally:

```scss
.Button {
  // Base, subcomponents, and variations first.

  // S - Tablet
  @media (max-width: 768px) {
    &__text-label {
    }

    &__icon {
    }

    &[data-object-type='primary'] {
      .Button__text-label {
      }

      .Button__icon {
      }
    }

    &[data-object-type='secondary'] {
      .Button__text-label {
      }

      .Button__icon {
      }
    }
  }

  // M - Tablet/Laptop
  @media (min-width: 769px) and (max-width: 1024px) {
  }

  // L - High Res
  @media (min-width: 1025px) and (max-width: 1200px) {
  }

  // XL - Ultra High Res
  @media (min-width: 1201px) {
  }
}
```

Do not repeat declarations that are already correct at the base level. Add only overrides needed for a range. If the project intentionally uses overlapping `max-width` queries, order them from largest to smallest or otherwise prove that the cascade produces the intended result.

## Barrel checks

`atomic-bomb` component folders normally already contain `_index.scss`. Confirm the file and its contents before editing. Match the syntax used by adjacent components, for example:

```scss
@use 'Button.style';
```

or:

```scss
@forward 'Button.style';
```

Do not assume `@use` and `@forward` are interchangeable. `@use` evaluates the stylesheet in the current compilation; `@forward` exposes members to consumers. Follow the project's established barrel chain and compile the effective entrypoint to prove the component CSS is emitted.

Check all of the following:

1. The local `_index.scss` references the partial exactly once.
2. The parent atomic-level barrel references the component or its local barrel.
3. The resources or application Sass entrypoint loads the required parent barrel.
4. No direct import duplicates the barrel inclusion.
5. Relative paths and filename case resolve on a case-sensitive filesystem.
