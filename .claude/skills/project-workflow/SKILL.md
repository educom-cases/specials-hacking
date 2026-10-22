---
name: project-workflow
description: Required workflow for every software development task. Select and apply relevant installed skills, coordinate cross-stack work, use the repository's issue workflow, and carry significant changes through commit and review.
metadata:
  title: Project Workflow
  summary: Provides a reusable, cross-agent workflow for skill selection, issue-based development, commits, and review completion.
  version: 1.0.0
  author: René Krewinkel
  priority: critical
  enforcement: strict
  scope: project-wide
  applies_to:
    - software development
    - issue-based changes
    - cross-stack implementation
    - code review preparation
  requires:
    - applicable installed skills are loaded
    - repository issue and review conventions are followed
  governs:
    - skill selection
    - cross-stack workflows
    - component-structure routing
    - issue development
    - commits and pull requests
  triggers:
    - any software development task
    - start work on an issue
    - coordinate multiple skills
    - prepare a significant change for review
  keywords:
    - project-workflow
    - skill-selection
    - issue-workflow
    - cross-stack
    - code-review
  success_criteria:
    - every applicable installed skill and its required references are followed
    - cross-stack tasks satisfy each applicable skill
    - issue-linked work follows the repository's issue workflow
    - significant changes have descriptive commits and enter the required review process
  failure_conditions:
    - an applicable skill or required reference is skipped
    - platform-specific hosting commands are assumed without checking repository conventions
    - an issue-linked change bypasses the repository's issue workflow
    - a significant change lacks a descriptive commit or required review request
  agent_instructions: Read and follow this skill for every development task. Load every applicable installed skill, follow cross-stack requirements together, and use the repository's own issue, commit, and review conventions.
  tags:
    - workflow
    - cross-agent
    - project-wide
    - issue-tracking
---

# Project workflow

Use this skill for every software development task, together with all applicable technology-specific skills. It defines the shared workflow; it does not replace the technical contracts in those skills.

## Select and load skills

1. Identify the active agent and its supported skill directories. Use the repository's skill configuration when available; otherwise use that agent's documented project skill locations.
2. Inspect the installed skills and select every skill whose triggers match the task. For work spanning technologies or layers, load all matching skills together.
3. Read each selected skill's complete `SKILL.md` before changing files. Follow its priority, required references, dependencies, and completion checks.
4. When component work is in scope, load and follow the component-structure guidance for the applicable UI technology, regardless of which other skills are selected. For React work, this includes the React skill's `references/component-structure.md`.
5. Resolve conflicts using the project's documented precedence. Do not silently discard an applicable requirement.

## Work from issues through review

When a task is tied to a tracked issue:

1. Read the issue and the repository's contribution guidance.
2. Start from the issue using the hosting platform's established workflow before implementation. Do not assume a particular host or command-line tool.
3. Make changes that address the issue and keep the commit message specific to those changes.
4. Commit and push each significant change when required by the repository workflow or the user.
5. Once the issue is resolved, close it through the hosting platform and create or update the required pull request or merge request, with a clear title, summary, and target branch.

For work without a tracked issue, follow repository contribution guidance and explicit user instructions for branching, commits, pushing, and review.

## Finish the task

- Run the validation required by every applicable skill and by the repository.
- Confirm the requested changes are complete and the working tree state is understood.
- Report what changed, the validation performed, and any workflow step that could not be completed.
