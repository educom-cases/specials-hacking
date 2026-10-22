#!/usr/bin/env python3
"""Validate the cross-agent skill repository and its package metadata."""

from __future__ import annotations

import argparse
import glob
import re
import sys
import tomllib
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("error: PyYAML is required; install it with `python3 -m pip install pyyaml`", file=sys.stderr)
    raise SystemExit(2)


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
MARKDOWN_LINK_PATTERN = re.compile(r"\]\(([^)#]+)(?:#[^)]+)?\)")
COPILOT_AGENT_SUFFIX = ".agent.md"


class ValidationError(Exception):
    """A repository invariant failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_toml(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing TOML file: {path}")
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        raise ValidationError(f"invalid TOML in {path}: {error}") from error


def load_frontmatter(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing Markdown file: {path}")
    match = FRONTMATTER_PATTERN.match(path.read_text(encoding="utf-8"))
    require(match is not None, f"missing or invalid YAML frontmatter: {path}")
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        raise ValidationError(f"invalid YAML frontmatter in {path}: {error}") from error
    require(isinstance(data, dict), f"frontmatter must be a mapping: {path}")
    return data


def validate_relative_pattern(skill_dir: Path, group: str, pattern: str) -> None:
    candidate = Path(pattern)
    require(not candidate.is_absolute(), f"{skill_dir}: absolute file pattern in {group}: {pattern}")
    require(".." not in candidate.parts, f"{skill_dir}: parent traversal in {group}: {pattern}")
    matches = glob.glob(str(skill_dir / pattern), recursive=True)
    require(bool(matches), f"{skill_dir}: {group} pattern matches nothing: {pattern}")


def validate_links(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for target in MARKDOWN_LINK_PATTERN.findall(text):
        if "://" in target or target.startswith("mailto:"):
            continue
        require((path.parent / target).exists(), f"broken link: {path} -> {target}")


def validate_repository(root: Path) -> tuple[int, int, int]:
    root_manifest = load_toml(root / "skill-repository.toml")
    require(root_manifest.get("schema_version") == 1, "unsupported repository schema_version")

    skills_dir = root / root_manifest["skills_directory"]
    profiles_dir = root / root_manifest["profiles_directory"]
    require(skills_dir.is_dir(), f"missing skills directory: {skills_dir}")
    require(profiles_dir.is_dir(), f"missing profiles directory: {profiles_dir}")

    installation = root_manifest.get("installation", {})
    modes = installation.get("supported_modes", [])
    require(installation.get("default_mode") in modes, "default installation mode is unsupported")
    require(installation.get("conflict_policy") in {"error", "replace", "skip"}, "invalid conflict policy")

    agents = root_manifest.get("agents", {})
    require(isinstance(agents, dict) and agents, "no agent targets declared")
    for agent_name, agent in agents.items():
        require(NAME_PATTERN.fullmatch(agent_name) is not None, f"invalid agent identifier: {agent_name}")
        require(agent.get("supports_agent_skills") is True, f"{agent_name}: Agent Skills support is disabled")
        preferred = agent.get("preferred_skill_directory")
        compatible = agent.get("compatible_skill_directories", [])
        require(preferred in compatible, f"{agent_name}: preferred directory is not compatible")

    skill_packages: dict[str, dict[str, Any]] = {}
    for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        package = load_toml(skill_dir / "skill.toml")
        entrypoint_name = package.get("entrypoint")
        require(entrypoint_name == "SKILL.md", f"{skill_dir}: entrypoint must be SKILL.md")
        entrypoint = skill_dir / entrypoint_name
        frontmatter = load_frontmatter(entrypoint)

        name = package.get("name")
        require(isinstance(name, str) and NAME_PATTERN.fullmatch(name) is not None, f"{skill_dir}: invalid name")
        require(name == skill_dir.name, f"{skill_dir}: directory and package names differ")
        require(name == frontmatter.get("name"), f"{skill_dir}: package and frontmatter names differ")

        metadata = frontmatter.get("metadata", {})
        require(isinstance(metadata, dict), f"{skill_dir}: metadata must be a mapping")
        require(package.get("version") == metadata.get("version"), f"{skill_dir}: versions differ")
        require(package.get("schema_version") == 1, f"{skill_dir}: unsupported package schema")

        compatible_agents = set(package.get("compatible_agents", []))
        require(bool(compatible_agents), f"{skill_dir}: no compatible agents")
        require(compatible_agents <= set(agents), f"{skill_dir}: unknown compatible agent")

        dependencies = set(package.get("dependencies", []))
        incompatible = set(package.get("incompatible_skills", []))
        require(not dependencies & incompatible, f"{skill_dir}: dependency is also incompatible")

        files = package.get("files", {})
        require("SKILL.md" in files.get("shared", []), f"{skill_dir}: SKILL.md must be shared")
        require("skill.toml" in files.get("repository_only", []), f"{skill_dir}: skill.toml must be repository-only")
        for group, patterns in files.items():
            require(isinstance(patterns, list), f"{skill_dir}: files.{group} must be a list")
            for pattern in patterns:
                require(isinstance(pattern, str), f"{skill_dir}: non-string file pattern in {group}")
                validate_relative_pattern(skill_dir, group, pattern)

        for agent_name in agents:
            require(agent_name in files, f"{skill_dir}: missing files.{agent_name} group")

        validate_links(entrypoint)
        openai_yaml = skill_dir / "agents" / "openai.yaml"
        if openai_yaml.exists():
            try:
                require(isinstance(yaml.safe_load(openai_yaml.read_text(encoding="utf-8")), dict), f"invalid mapping: {openai_yaml}")
            except yaml.YAMLError as error:
                raise ValidationError(f"invalid YAML in {openai_yaml}: {error}") from error

        skill_packages[name] = package

    require(bool(skill_packages), "no skills found")
    for name, package in skill_packages.items():
        require(set(package["dependencies"]) <= set(skill_packages), f"{name}: unknown dependency")
        require(set(package["incompatible_skills"]) <= set(skill_packages), f"{name}: unknown incompatible skill")

    copilot_agents_dir = root / ".github" / "agents"
    require(copilot_agents_dir.is_dir(), f"missing Copilot agents directory: {copilot_agents_dir}")
    copilot_agent_paths = sorted(copilot_agents_dir.glob(f"*{COPILOT_AGENT_SUFFIX}"))
    copilot_agent_names = {
        path.name[: -len(COPILOT_AGENT_SUFFIX)]
        for path in copilot_agent_paths
    }
    require(copilot_agent_names == set(skill_packages), "Copilot agent profile catalog is incomplete")
    for path in copilot_agent_paths:
        skill_name = path.name[: -len(COPILOT_AGENT_SUFFIX)]
        frontmatter = load_frontmatter(path)
        require(frontmatter.get("name") == skill_name, f"{path}: name must match its skill")
        description = frontmatter.get("description")
        require(isinstance(description, str) and description.strip(), f"{path}: description is required")
        require(frontmatter.get("user-invocable") is True, f"{path}: user-invocable must be true")
        require(
            frontmatter.get("disable-model-invocation") is False,
            f"{path}: disable-model-invocation must be false",
        )
        text = path.read_text(encoding="utf-8")
        canonical_entrypoint = f"skills/{skill_name}/SKILL.md"
        require(canonical_entrypoint in text, f"{path}: does not route to {canonical_entrypoint}")

    maintenance_skill = root_manifest.get("maintenance_skill")
    require(maintenance_skill in skill_packages, "maintenance_skill does not identify a known skill")

    profile_count = 0
    detection_priorities: dict[int, str] = {}
    for profile_path in sorted(profiles_dir.glob("*.toml")):
        profile = load_toml(profile_path)
        require(profile.get("schema_version") == 1, f"{profile_path}: unsupported schema")
        require(profile.get("name") == profile_path.stem, f"{profile_path}: filename and name differ")
        selected_names = profile.get("skills", [])
        require(bool(selected_names), f"{profile_path}: profile has no skills")
        require(set(selected_names) <= set(skill_packages), f"{profile_path}: unknown skill")

        selected = [skill_packages[name] for name in selected_names]
        available_platforms = set().union(*(set(item["platforms"]) for item in selected))
        available_technologies = set().union(*(set(item["technologies"]) for item in selected))
        require(set(profile.get("platforms", [])) <= available_platforms, f"{profile_path}: unsupported platform")
        require(set(profile.get("technologies", [])) <= available_technologies, f"{profile_path}: unsupported technology")
        detection = profile.get("detection")
        require(isinstance(detection, dict), f"{profile_path}: missing detection rules")
        priority = detection.get("priority")
        require(isinstance(priority, int), f"{profile_path}: detection priority must be an integer")
        require(priority not in detection_priorities, f"{profile_path}: duplicate detection priority")
        detection_priorities[priority] = profile["name"]
        path_any = detection.get("path_any", [])
        dependency_any = detection.get("package_json_dependencies_any", [])
        require(isinstance(path_any, list), f"{profile_path}: detection.path_any must be a list")
        require(
            isinstance(dependency_any, list),
            f"{profile_path}: detection.package_json_dependencies_any must be a list",
        )
        require(bool(path_any or dependency_any), f"{profile_path}: detection requires at least one signal")
        profile_count += 1

    skills_entrypoint = load_frontmatter(root / "SKILLS.md")
    require(set(skills_entrypoint.get("skills", [])) == set(skill_packages), "SKILLS.md catalog is incomplete")

    for path in [root / "README.md", root / "SKILLS.md", root / "AGENTS.md", root / "CLAUDE.md"]:
        validate_links(path)

    return len(skill_packages), profile_count, len(agents)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[3],
        help="repository root; defaults to the root containing this skill",
    )
    args = parser.parse_args()

    try:
        skills, profiles, agents = validate_repository(args.root.resolve())
    except (KeyError, TypeError, ValidationError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"Validated {skills} skills, {profiles} profiles, and {agents} agent targets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
