---
title: React Component Structure
description: Critical rules for locating, naming, composing, and structuring React components across Atomic Design layers.
summary: Defines the required component file layout and file boundaries for React UI.
version: 1.0.0
author: René Krewinkel
parent_skill: react
scope: project-wide
priority: critical
enforcement: strict
read_when:
  - creating or moving React components
  - deciding where component files belong
  - reviewing component folder structure
governs:
  - component placement
  - component naming
  - component file boundaries
  - atomic layer directories
---

# React component structure

Apply this guidance with the React skill's architecture and component rules. These structure requirements have critical priority whenever component files are created, moved, or reviewed.

## Atomic layer placement

Place each component in exactly one Atomic Design layer and keep that layer visible in its path:

```text
src/
  components/
    atoms/
    molecules/
    organisms/
    templates/
    pages/
```

- `atoms/` contains the smallest reusable UI elements and wrappers for semantic native elements.
- `molecules/` combines Atoms into a focused UI unit.
- `organisms/` combines Atoms and Molecules into a larger interface section.
- `templates/` defines page layout and composition without owning domain behavior.
- `pages/` connects application behavior and domain data to a Template.

Do not place a component in multiple layers or use a generic `shared/` or `common/` directory to avoid choosing its layer. Keep domain models, business rules, API clients, and application workflows in their respective domain, infrastructure, and application areas instead of the component tree.

## Component folder

- It is REQUIRED to use Bomber MCP for component (and other objects) creation.
- If Bomber MCP is not available you MUST stop execution and inform the user
- After Bomber MCP has been executed, the directory structure should contain the following files
```text
Button/
├── Button.interface.ts     // Typescript interface for the component
├── Button.mdx              // Extensive description of the component including the code
├── Button.mock.ts          // File containing mock data for stories and unit tests
├── Button.stories.tsx      // Storybook stories file
├── Button.style.scss       // Style SCSS file
├── Button.test.tsx         // Unit test file
├── Button.tsx              // Component file
├── index.scss              // SCSS Barrel to export the scss
└── index.tsx               // Typescript Barrel to export the component
```
- When using React Native/ EXPO and Bomber MCP has been executed, the directory structure should contain the following files
```text
Button/
├── Button.interface.ts     // Typescript interface for the component
├── Button.mdx              // Extensive description of the component including the code
├── Button.mock.ts          // File containing mock data for stories and unit tests
├── Button.stories.tsx      // Storybook stories file
├── Button.style.ts         // Style typescript file
├── Button.test.tsx         // Unit test file
├── Button.tsx              // Component file
└── index.tsx               // Typescript Barrel to export the component
```


## Imports

### DO
- You MUST use the type-barrel for importing components:
```jsx
import { Button, Label, Paragraph } from '@/components/atoms'
```
- You MUST always group the import according to type: 
```jsx
import { Button, Label, Paragraph } from '@/components/atoms'
import { ButtonBar, Menu, FooterItem } from '@/components/molecules'
```

### DON'T
- it is FORBIDDEN to import from the highest level: `import { Button } from '@/components`
- it is FORBIDDEN to imporr from the lowest level: `import Button from '@/components/atoms/Button/Button`

## Function signatures

### DO
- You MUST use `const` as function description
```jsx
import ComponentInterface from './Component.interface'
export default const ComponentName = ({ arg1, arg2 }: ComponentInterface) => {  }
```
- You MUST use `const` as function description for generic functions, hooks, library functions, domain functions etc.

### DON'T
- it is FORBIDDEN to use `function` as function description


## Function and file composition

### DO 

- A component MUST ALWAYS have a return statement: 
```jsx
import { ThankYouInterface } from './ThankYou.interface'
import { languages } from '@/config'
import { Heading, Paragraph } from '@/components/atoms'

const ThankYou = ({ testID, language }: ThankYouInterface) => {

  const { thankYou, thankYouMessage } = languages[language]

  return (
    <div data-testid={testID} className={`ThankYou`}>
      <Heading text={thankYou} />
      <Paragraph text={thankYouMessage} />
    </div>
  )
}

export default ThankYou
```

- Checking for a state or complex constructions MUST ALWAYS use *private* functions:
```jsx
import { ThankYouInterface } from './ThankYou.interface'
import { languages } from '@/config'
import { Heading, Paragraph } from '@/components/atoms'

const ThankYou = ({ testID, language }: ThankYouInterface) => {
  
  const [showMsg, setShowMessage] = useState<boolean>(false)
  const { thankYou, thankYouMessage } = languages[language]
  
  const __renderMessage = () => {
    if(showMsg) {
      return(
        <Paragraph text={thankYouMessage} />
      )
    }
  }
  
  return (
    <div data-testid={testID} className={`ThankYou`}>
      <Heading text={thankYou} />
      { __renderMessage() } 
    </div>
  )
}

export default ThankYou
```

- if there are oneline-return statements in if-statements in *private* functions, you may omit the curly braces:
```jsx
 import { ThankYouInterface } from './ThankYou.interface'
import { languages } from '@/config'
import { Heading, Paragraph } from '@/components/atoms'

const ThankYou = ({ testID, language }: ThankYouInterface) => {
  
  const [showMsg, setShowMessage] = useState<boolean>(false)
  const { thankYou, thankYouMessage } = languages[language]
  
  const __renderMessage = () => {
    if(showMsg) return(<Paragraph text={thankYouMessage} />)
  }
  
  return (
    <div data-testid={testID} className={`ThankYou`}>
      <Heading text={thankYou} />
      { __renderMessage() } 
    </div>
  )
}

export default ThankYou
```
- *private* functions MUST ALWAYS be prefixed with a double underscore: `__renderSomething`
- if *private* functions are helpers that render UI elements, it MUST ALWAYS be prefixed with `__render`
- ALL function inside a component are considered *private* and therefor MUST start with a double underscore: `__handleClick()`

### DON'T

- it is FORBIDDEN to use an arrow return for a component: 
```jsx
const Avatar = ({ size = 'regular', className = '', ...props }: AvatarProps) => (
  <img className={`Avatar ${className}`.trim()} data-size={size} {...props} />
)
```

- it is FORBIDDEN to use this kind of code where types are defined INSIDE a component file
```jsx
import type { ImgHTMLAttributes } from 'react'

type AvatarProps = ImgHTMLAttributes<HTMLImageElement> & { size?: 'small' | 'regular' | 'large' }

const Avatar = ({ size = 'regular', className = '', ...props }: AvatarProps) => (
  <img className={`Avatar ${className}`.trim()} data-size={size} {...props} />
)

export default Avatar 
```

## Calling Components

### DO
- You MUST always pass arguments as ATTRIBUTES to a component
- Only if it is functionally required you MAY pass `children` to *molecules* or *organisms*
- It is REQUIRED to pass `children` to *templates*

**MUST DO**
```jsx
<Button text={'click me'} action={whateverAction} />
```

### DON'T
- For *atoms* it is FORBIDDEN to pass `children`

**MUST NEVER DO**
```jsx
<Button action={whateverAction}>Click me</Button>
```



## Required structure checks

Before completing component work, verify that:

1. Every component has one clear Atomic Design layer reflected in its directory.
2. Reusable component files are colocated in a named component directory.
3. Component tests and Storybook stories are colocated for reusable components.
4. UI component files contain rendering and local UI behavior, not business rules, API calls, validation, or data transformation.
5. The public barrel exports only the intended component API.
6. All above rules are followed and implemented with no exception.
7. Correct automatically when broken rules occur.
8. Ask user if unsure.
