#!/usr/bin/env python3
"""Command-line interface for the specDevAgent development workflow."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, Iterable, List

BASE_STRUCTURE_DIRS: List[str] = [
    "docs",
    "docs/decisions",
    "docs/process",
    "docs/research",
    "src",
    "tests",
]

BASE_STRUCTURE_FILES: Dict[str, str] = {
    "project.md": "# Project Overview\n\nDescribe the project scope, stakeholders, and key milestones here.\n",
    "todo.md": "# Task Backlog\n\n- [ ] T001: Define discovery questions\n",
    "development.log": "# Development Log\n\n## 0.1.0\n- Project scaffolded.\n",
    "docs/discovery.md": "# Discovery Notes\n\nCapture stakeholder interviews, assumptions, and open questions.\n",
    "docs/inception.md": "# Inception Summary\n\nDocument the initial solution outline, success metrics, and risks.\n",
    "docs/process/plan.md": "# Iteration Planning\n\nDetail objectives, scope, and deliverables for the current cycle.\n",
    "docs/process/retro.md": "# Iteration Retrospective\n\nRecord wins, challenges, and follow-up actions after each cycle.\n",
    "docs/decisions/adr-0001.md": "# ADR-0001 — Project Initialization\n\n- **Status:** Accepted\n- **Context:** Describe the reason for choosing this scaffold.\n- **Decision:** Document the agreed approach.\n- **Consequences:** Capture trade-offs and future considerations.\n",
}

AGENT_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_AGENT_ROLES = {
    "orchestrator",
    "developer",
    "reviewer",
    "qa",
    "researcher",
}

PROJECT_METADATA_TEMPLATE = {
    "name": "Sample Project",
    "description": "Short description of the problem space and desired outcome.",
    "version": "0.1.0",
    "agents": [
        {
            "id": "primary",
            "role": "orchestrator",
            "responsibilities": [
                "Plan tasks based on discovery artifacts",
                "Coordinate code, tests, and documentation updates",
            ],
        }
    ],
    "documents": {
        "project": "project.md",
        "todo": "todo.md",
        "log": "development.log",
    },
}

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = REPOSITORY_ROOT / "templates"


class ValidationError(Exception):
    """Raised when the project structure or metadata fails validation."""


def available_templates() -> List[str]:
    if not TEMPLATE_ROOT.is_dir():
        return []
    return sorted(entry.name for entry in TEMPLATE_ROOT.iterdir() if entry.is_dir())


def ensure_directories(root: Path, directories: Iterable[str]) -> None:
    for directory in directories:
        target = root / directory
        target.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str, *, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def init_project(args: argparse.Namespace) -> None:
    root = Path(args.path).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    ensure_directories(root, BASE_STRUCTURE_DIRS)

    created_files: List[Path] = []
    skipped_files: List[Path] = []

    for relative_path, content in BASE_STRUCTURE_FILES.items():
        target = root / relative_path
        if write_file(target, content, force=args.force):
            created_files.append(target)
        else:
            skipped_files.append(target)

    metadata_path = root / "project.json"
    if not metadata_path.exists() or args.force:
        metadata_path.write_text(
            json.dumps(PROJECT_METADATA_TEMPLATE, indent=2),
            encoding="utf-8",
        )
        created_files.append(metadata_path)
    else:
        skipped_files.append(metadata_path)

    print(f"Initialized project at {root}")
    if created_files:
        print("Created files:")
        for path in created_files:
            print(f"  - {path.relative_to(root)}")
    if skipped_files:
        print("Skipped existing files (use --force to overwrite):")
        for path in skipped_files:
            print(f"  - {path.relative_to(root)}")


def load_project_metadata(project_root: Path, *, metadata_path: Path | None = None) -> Dict:
    metadata_path = metadata_path or (project_root / "project.json")
    if not metadata_path.is_file():
        raise ValidationError("Missing project.json metadata file.")
    try:
        return json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"project.json is not valid JSON: {exc}") from exc


def validate_metadata(metadata: Dict) -> List[str]:
    issues: List[str] = []
    required_fields = ["name", "description", "version", "agents", "documents"]
    for field in required_fields:
        if field not in metadata:
            issues.append(f"Metadata missing required field: {field}")

    for text_field in ["name", "description"]:
        if text_field in metadata:
            value = metadata[text_field]
            if not isinstance(value, str) or not value.strip():
                issues.append(
                    f"Metadata field '{text_field}' must be a non-empty string."
                )

    if "version" in metadata and isinstance(metadata["version"], str):
        if not metadata["version"].count(".") == 2:
            issues.append("Metadata version should follow semantic versioning (e.g. 0.1.0).")
    else:
        issues.append("Metadata field 'version' must be a string.")

    if "agents" in metadata:
        if not isinstance(metadata["agents"], list) or not metadata["agents"]:
            issues.append("Metadata 'agents' must be a non-empty list.")
        else:
            for index, agent in enumerate(metadata["agents"], start=1):
                if not isinstance(agent, dict):
                    issues.append(f"Agent entry #{index} must be an object.")
                    continue
                for key in ["id", "role", "responsibilities"]:
                    if key not in agent:
                        issues.append(f"Agent entry #{index} missing '{key}'.")
                if "responsibilities" in agent and not isinstance(agent["responsibilities"], list):
                    issues.append(f"Agent entry #{index} field 'responsibilities' must be a list.")
                elif isinstance(agent.get("responsibilities"), list):
                    if not agent["responsibilities"]:
                        issues.append(
                            f"Agent entry #{index} must declare at least one responsibility."
                        )
                    for responsibility in agent["responsibilities"]:
                        if not isinstance(responsibility, str) or not responsibility.strip():
                            issues.append(
                                f"Agent entry #{index} has an invalid responsibility entry;"
                                " each responsibility must be a non-empty string."
                            )

                if "id" in agent and not isinstance(agent["id"], str):
                    issues.append(f"Agent entry #{index} field 'id' must be a string.")
                elif isinstance(agent.get("id"), str):
                    if not AGENT_ID_PATTERN.fullmatch(agent["id"].strip()):
                        issues.append(
                            f"Agent entry #{index} id must be kebab-case (e.g. orchestrator-bot)."
                        )
                if "role" in agent and not isinstance(agent["role"], str):
                    issues.append(f"Agent entry #{index} field 'role' must be a string.")
                elif isinstance(agent.get("role"), str):
                    if agent["role"] not in ALLOWED_AGENT_ROLES:
                        issues.append(
                            "Agent role must be one of: "
                            + ", ".join(sorted(ALLOWED_AGENT_ROLES))
                        )

    if "documents" in metadata:
        documents = metadata["documents"]
        if not isinstance(documents, dict):
            issues.append("Metadata 'documents' must be an object.")
        else:
            for key in ["project", "todo", "log"]:
                if key not in documents:
                    issues.append(f"Metadata 'documents' missing '{key}'.")
            for key, value in documents.items():
                if not isinstance(value, str) or not value.strip():
                    issues.append(
                        f"Metadata document reference '{key}' must be a non-empty string."
                    )
                elif not value.endswith(".md") and key != "log":
                    issues.append(
                        f"Metadata document '{key}' should reference a markdown file (got '{value}')."
                    )

            unexpected_keys = set(documents) - {"project", "todo", "log"}
            if unexpected_keys:
                issues.append(
                    "Metadata 'documents' includes unsupported keys: "
                    + ", ".join(sorted(unexpected_keys))
                )

    return issues


def validate_project(args: argparse.Namespace) -> None:
    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        raise ValidationError(f"Project path does not exist: {root}")

    missing_dirs = [d for d in BASE_STRUCTURE_DIRS if not (root / d).is_dir()]
    missing_files = [f for f in BASE_STRUCTURE_FILES if not (root / f).is_file()]

    metadata = load_project_metadata(root)
    metadata_issues = validate_metadata(metadata)
    document_reference_issues = collect_document_reference_issues(root, metadata)

    issues: List[str] = []
    if missing_dirs:
        issues.append("Missing directories:\n  - " + "\n  - ".join(missing_dirs))
    if missing_files:
        issues.append("Missing files:\n  - " + "\n  - ".join(missing_files))
    if metadata_issues:
        issues.append("Metadata issues:\n  - " + "\n  - ".join(metadata_issues))
    if document_reference_issues:
        issues.append("Document references:\n  - " + "\n  - ".join(document_reference_issues))

    if issues:
        print("Validation failed:")
        for issue in issues:
            print(issue)
        raise ValidationError("Project validation did not pass.")

    print(f"Project at {root} matches the expected specDevAgent scaffold.")


def collect_document_reference_issues(root: Path, metadata: Dict) -> List[str]:
    issues: List[str] = []
    documents = metadata.get("documents", {}) if isinstance(metadata, dict) else {}
    if isinstance(documents, dict):
        for key, relative_path in documents.items():
            if isinstance(relative_path, str) and relative_path.strip():
                referenced_path = root / relative_path
                if not referenced_path.exists():
                    issues.append(
                        f"Metadata document '{key}' points to missing file: {relative_path}"
                    )
    return issues


def lint_metadata(args: argparse.Namespace) -> None:
    target = Path(args.path).expanduser().resolve()
    if target.is_dir():
        metadata_path = target / "project.json"
        project_root = target
    else:
        metadata_path = target
        project_root = metadata_path.parent

    metadata = load_project_metadata(project_root, metadata_path=metadata_path)
    metadata_issues = validate_metadata(metadata)

    document_reference_issues: List[str] = []
    if args.check_documents:
        document_reference_issues = collect_document_reference_issues(project_root, metadata)

    if metadata_issues or document_reference_issues:
        print("Metadata lint failed:")
        if metadata_issues:
            print("Schema issues:\n  - " + "\n  - ".join(metadata_issues))
        if document_reference_issues:
            print("Document references:\n  - " + "\n  - ".join(document_reference_issues))
        raise ValidationError("Metadata lint did not pass.")

    print(f"Metadata at {metadata_path} satisfies specDevAgent lint rules.")


def status_project(args: argparse.Namespace) -> None:
    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        raise ValidationError(f"Project path does not exist: {root}")

    print(f"Project status for {root}:")

    missing_dirs = [d for d in BASE_STRUCTURE_DIRS if not (root / d).is_dir()]
    missing_files = [f for f in BASE_STRUCTURE_FILES if not (root / f).is_file()]

    if missing_dirs:
        print("- Directory skeleton: missing entries ->")
        for directory in missing_dirs:
            print(f"    • {directory}")
    else:
        print("- Directory skeleton: all expected folders are present.")

    if missing_files:
        print("- Baseline files: missing entries ->")
        for file_name in missing_files:
            print(f"    • {file_name}")
    else:
        print("- Baseline files: all starter docs exist.")

    metadata = None
    metadata_error: str | None = None
    try:
        metadata = load_project_metadata(root)
    except ValidationError as exc:
        metadata_error = str(exc)

    metadata_issues: List[str] = []
    document_reference_issues: List[str] = []
    if metadata is not None:
        metadata_issues = validate_metadata(metadata)
        document_reference_issues = collect_document_reference_issues(root, metadata)

        name = metadata.get("name", "<unknown>")
        version = metadata.get("version", "?<no version>")
        print(f"- Metadata: {name} (version {version})")

        agents = metadata.get("agents")
        if isinstance(agents, list):
            roles = sorted(
                {
                    agent.get("role", "?")
                    for agent in agents
                    if isinstance(agent, dict) and agent.get("role")
                }
            )
            print(
                f"  • Agents: {len(agents)} registered"
                + (f" — roles: {', '.join(roles)}" if roles else "")
            )

        documents = metadata.get("documents")
        if isinstance(documents, dict):
            print("  • Documents:")
            for key in sorted(documents):
                value = documents[key]
                if isinstance(value, str) and value.strip():
                    referenced_path = root / value
                    status = "found" if referenced_path.exists() else "missing"
                    print(f"    - {key}: {value} ({status})")
                else:
                    print(f"    - {key}: <invalid reference>")

    if metadata_error:
        print(f"- Metadata error: {metadata_error}")

    if metadata_issues:
        print("- Metadata schema warnings:")
        for issue in metadata_issues:
            print(f"    • {issue}")

    if document_reference_issues:
        print("- Document reference warnings:")
        for issue in document_reference_issues:
            print(f"    • {issue}")

    available = available_templates()
    if available:
        print("- Available templates:")
        for template in available:
            print(f"    • {template}")
    else:
        print("- Available templates: none detected.")

    issue_count = (
        len(missing_dirs)
        + len(missing_files)
        + len(metadata_issues)
        + len(document_reference_issues)
        + (1 if metadata_error else 0)
    )

    if issue_count:
        print(f"- Warnings detected: {issue_count}. Run 'validate' for strict enforcement.")
    else:
        print("- No warnings detected. Project is ready for deeper validation or development.")


def scaffold_project(args: argparse.Namespace) -> None:
    root = Path(args.path).expanduser().resolve()
    template_dir = TEMPLATE_ROOT / args.template
    if not template_dir.is_dir():
        raise ValidationError(f"Template '{args.template}' was not found in {TEMPLATE_ROOT}.")

    root.mkdir(parents=True, exist_ok=True)
    copied: List[Path] = []
    skipped: List[Path] = []

    for item in template_dir.iterdir():
        destination = root / item.name
        if item.is_dir():
            shutil.copytree(item, destination, dirs_exist_ok=True)
            copied.append(destination)
            continue
        if destination.exists() and not args.force:
            skipped.append(destination)
            continue
        shutil.copy2(item, destination)
        copied.append(destination)

    print(f"Applied template '{args.template}' into {root}")
    if copied:
        print("Copied artifacts:")
        for path in copied:
            print(f"  - {path.relative_to(root)}")
    if skipped:
        print("Skipped existing paths (use --force to overwrite):")
        for path in skipped:
            print(f"  - {path.relative_to(root)}")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="specDevAgent project toolkit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize a new project scaffold")
    init_parser.add_argument("path", help="Directory where the scaffold will be generated")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    init_parser.set_defaults(func=init_project)

    validate_parser = subparsers.add_parser("validate", help="Validate an existing project against the spec")
    validate_parser.add_argument("path", help="Project directory to validate")
    validate_parser.set_defaults(func=validate_project)

    scaffold_parser = subparsers.add_parser(
        "scaffold", help="Copy a template into the target directory"
    )
    scaffold_parser.add_argument("path", help="Project directory where the template will be applied")
    scaffold_parser.add_argument("--template", required=True, help="Template name (e.g. python-fastapi)")
    scaffold_parser.add_argument("--force", action="store_true", help="Overwrite files that already exist")
    scaffold_parser.set_defaults(func=scaffold_project)

    status_parser = subparsers.add_parser(
        "status",
        help="Summarize the project scaffold, metadata, and known document issues",
        description=(
            "Summarize metadata, directory health, and referenced documents without "
            "failing the task. Use this when you need a quick briefing before "
            "editing or reviewing a project."
        ),
    )
    status_parser.add_argument(
        "path",
        nargs="?",
        default=Path.cwd(),
        help="Project directory to inspect (default: current working directory)",
    )
    status_parser.set_defaults(func=status_project)

    lint_parser = subparsers.add_parser(
        "lint-metadata",
        help="Check project.json for schema and policy violations",
        description=(
            "Lint project metadata independently from the rest of the scaffold. "
            "See docs/overview.md#metadata-linting for guidance."
        ),
    )
    lint_parser.add_argument(
        "path",
        nargs="?",
        default=Path.cwd(),
        help="Project directory (default: current working directory) or path to project.json",
    )
    lint_parser.add_argument(
        "--check-documents",
        action="store_true",
        help="Ensure referenced documents exist relative to the project root",
    )
    lint_parser.set_defaults(func=lint_metadata)

    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    try:
        args = parse_args(argv or sys.argv[1:])
        args.func(args)
        return 0
    except ValidationError as exc:
        print(exc)
        return 1
    except KeyboardInterrupt:
        print("Aborted by user.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
