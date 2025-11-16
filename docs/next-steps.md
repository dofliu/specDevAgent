# Next Action Plan

## 1. Automate CLI Regression Coverage
1. Add a `tests/cli` package that shells out to `cli/agent_cli.py` using `subprocess` to run `init`, `scaffold`, and `validate` workflows against a pytest-managed temporary directory.
2. Seed fixtures for valid and invalid `project.json` payloads so validation edge cases (missing documents, empty strings, wrong types) are asserted in CI.
3. Wire the suite into GitHub Actions (or another CI runner) so every push exercises the CLI exactly the way agents are expected to use it.

## 2. Promote Templates as Installable Packages
1. Break the FastAPI scaffold into a versioned package under `templates/python-fastapi` with its own `pyproject.toml` so it can be published and reused independently.
2. Update the CLI to fetch templates via a simple registry (local path or Git URL) and verify template integrity hashes before applying them.
3. Document how agents can pin template versions inside `project.json` to ensure reproducible scaffolds.

## 3. Enrich Agent-Facing Documentation
1. Extend `docs/overview.md` with concrete acceptance criteria for each lifecycle stage (init, scaffold, validate, iterate) and highlight common failure recovery steps.
2. Create a “playbook” section containing example transcripts of successful and unsuccessful runs so agents learn to interpret CLI output consistently.
3. Cross-link these docs from the README quickstart and surface them in the CLI `--help` output (e.g., `see docs/overview.md#playbook`).

## 4. Enforce Metadata Quality via Schema + Linters
1. Expand `schema/project.schema.json` with pattern constraints for identifiers (e.g., kebab-case agent IDs) and enumerations for supported roles/responsibilities.
2. Implement a `python -m metadata_lint` command (or CLI subcommand) that loads the schema, reports violations with file/field context, and suggests fixes.
3. Add pre-commit hooks so contributors run the metadata lint automatically before committing.
