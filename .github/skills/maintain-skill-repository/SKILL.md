---
name: maintain-skill-repository
description: Maintain, extend, validate, or review this cross-agent skills repository and its Rust skillx installer. Use when adding or changing skills, SKILL.md frontmatter, references, scripts, assets, skill.toml package manifests, platform profiles, agent targets, README.md, SKILLS.md, AGENTS.md, CLAUDE.md, repository schemas, validation behavior, installer behavior, or the managed lock-file contract.
metadata:
  title: Maintain the Skills Repository
  summary: Preserves cross-agent skill quality, package-manifest integrity, progressive disclosure, platform-profile resolution, documentation, and deterministic validation.
  version: 1.5.0
  author: René Krewinkel
  priority: critical
  enforcement: strict
  scope: repository-wide
  applies_to:
    - skill authoring
    - skill maintenance
    - package manifests
    - platform profiles
    - agent compatibility
    - repository documentation
    - installer development
  requires:
    - canonical Agent Skills layout
    - progressive disclosure
    - TOML package metadata
    - cross-agent compatibility
    - deterministic validation
  governs:
    - skills
    - references
    - scripts
    - profiles
    - repository manifests
    - agent entry points
    - validation
    - installer contracts
  triggers:
    - add a skill
    - update a skill
    - split a skill
    - add a platform profile
    - add an agent target
    - change package metadata
    - change repository documentation
    - build or modify the skills installer
    - validate the skills repository
  keywords:
    - agent-skills
    - repository-maintenance
    - skill-authoring
    - progressive-disclosure
    - package-manifest
    - platform-profile
    - codex
    - claude
    - copilot
  success_criteria:
    - canonical skill instructions remain agent-independent
    - package metadata agrees with skill frontmatter and directory names
    - profiles reference valid compatible skills
    - agent-specific files remain isolated
    - documentation and entry points remain synchronized
    - repository validation passes
  failure_conditions:
    - installed output is edited instead of canonical source
    - skill identity or version drifts between files
    - detailed rules are duplicated instead of routed
    - a profile or dependency references an unknown skill
    - repository-only files are treated as installable skill content
    - validation is skipped
  agent_instructions: Inspect the repository before editing, preserve unrelated work, update canonical sources and every affected index or manifest, run deterministic validation, and report any unresolved compatibility constraint.
  tags:
    - maintenance
    - agent-skills
    - validation
    - packaging
    - cross-agent
---

# Maintain the skills repository

Use this workflow for every repository-maintenance change.

## Establish scope

1. Read root `SKILLS.md`, `README.md`, and `skill-repository.toml`.
2. Inspect the complete target skill, including `SKILL.md`, `skill.toml`, directly linked references, scripts, assets, and agent metadata.
3. Inspect relevant profiles and root instruction files.
4. Check version-control status and preserve unrelated changes.
5. Distinguish canonical repository sources from generated or installed output.

Do not edit copies installed in another application's agent directory when the canonical source lives here.

## Preserve repository boundaries

- Keep reusable agent instructions in `skills/<name>/SKILL.md` and its bundled resources.
- Keep repository packaging and selection metadata consumed by `skillx` in `skills/<name>/skill.toml`.
- Keep platform combinations in `profiles/<name>.toml`.
- Keep agent discovery destinations and installer defaults in `skill-repository.toml`.
- Keep Codex-only presentation metadata in `agents/openai.yaml`.
- Keep GitHub Copilot custom-agent profiles in `.github/agents/<skill-name>.agent.md`.
- Keep root `AGENTS.md` and `CLAUDE.md` concise; route procedural detail to this skill.
- Keep human onboarding in `README.md` and agent routing in `SKILLS.md`.

## Add or update a skill

When adding a skill:

1. Create `skills/<name>/SKILL.md` with lowercase hyphen-case `name`, a trigger-complete `description`, and rich metadata nested under `metadata`.
2. Keep core workflow and routing in `SKILL.md`; move detailed or conditional material into directly linked `references/`.
3. Add scripts only for deterministic or repeatedly implemented behavior and execute them during verification.
4. Generate `agents/openai.yaml` from the completed skill.
5. Add a thin `.github/agents/<skill-name>.agent.md` Copilot profile that routes to the canonical skill without duplicating its rules.
6. Add `skill.toml` with matching name and version, selection metadata, compatibility, dependencies, and file groups.
7. Add the skill to root `SKILLS.md` and `README.md`.
8. Add it to a profile only when the profile represents a stable platform or technology combination.

When updating a skill:

- Change the canonical instruction or resource once; do not duplicate it in indexes.
- Keep the directory name, frontmatter `name`, package `name`, and catalog identifier identical.
- Keep frontmatter and package versions identical.
- Increment the version when installed behavior or packaging changes.
- Regenerate stale agent metadata.
- Refresh the corresponding Copilot profile when the skill's name, purpose, or routing changes.
- Recheck every profile that selects the skill.

## Maintain package metadata

Use `skill.toml` as the future installer's source of truth:

- `files.shared` contains portable Agent Skills content.
- Agent-named file groups contain only target-specific additions.
- `files.repository_only` contains packaging metadata that must not be installed.
- `dependencies` contains required skills.
- `incompatible_skills` contains selections that cannot coexist.
- `compatible_agents` references agent identifiers declared by `skill-repository.toml`.

Keep profile selection explicit. Do not infer a stable named profile solely from overlapping tags.

Give every profile deterministic detection signals and a unique priority. Keep technology-specific detection data in the profile manifest rather than hard-coding it in `skillx`.

## Maintain agent compatibility

Keep the canonical `SKILL.md` and shared resources portable across Codex, Claude Code, and GitHub Copilot. Add target-specific behavior only when an agent requires it, isolate it in the target's file group, and document the compatibility consequence.

Copilot custom agents are repository-level `.agent.md` files with YAML frontmatter, not skill-local YAML sidecars. Keep their prompts short and route them to `skills/<name>/SKILL.md`; canonical requirements belong in the skill. Keep Codex `agents/openai.yaml` metadata separate because Copilot does not consume that schema.

Keep `https://codeberg.org/ReneKrewinkel/krewinkel-skills/` as the default remote consumed by `skillx`. Preserve explicit path, environment, configured path, and local-ancestor precedence before the cached remote fallback.

When adding an agent:

1. Add its identifier, preferred skill directory, compatible directories, and repository instruction files to `skill-repository.toml`.
2. Update applicable `compatible_agents` arrays.
3. Add an agent-specific file group to each affected `skill.toml`.
4. Update `README.md` and validation coverage.

## Validate

Run from the repository root:

```shell
python3 skills/maintain-skill-repository/scripts/validate_repository.py
git diff --check
```

Also run the canonical Agent Skills validator against each changed skill when it is available.

Do not report completion when validation fails. Report unavailable checks and their exact constraints.
