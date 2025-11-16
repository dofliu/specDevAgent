# Next Action Plan

The table below summarizes the prioritized workstreams, owners, and the signal we will use to call each stream “done.” Use it as a
dashboard before diving into the detailed checklists that follow.

| Priority | Initiative | Driver | Status | Next checkpoint |
| --- | --- | --- | --- | --- |
| P0 | Automate CLI regression coverage | Tooling Guild | 🟡 Drafting pytest harness | Demo failing+passing tests in CI |
| P1 | Package and version templates | Template Working Group | ⚪ Not started | Design registry contract |
| P1 | Expand agent-facing docs/playbooks | Docs Team | 🟡 Outline ready | Publish playbook draft |
| P2 | Enforce metadata quality via schema + linters | Platform Team | 🟢 CLI lint shipped | Add pre-commit hook + schema patterns |

---

## 1. Automate CLI Regression Coverage
**Objective**: guarantee that the CLI pathways agents rely on (`init`, `scaffold`, `validate`) never regress.

1. Add a `tests/cli` package that shells out to `cli/agent_cli.py` using `subprocess` to run `init`, `scaffold`, and `validate`
workflows against a pytest-managed temporary directory.
2. Seed fixtures for valid and invalid `project.json` payloads so validation edge cases (missing documents, empty strings, wrong
 types) are asserted in CI.
3. Wire the suite into GitHub Actions (or another CI runner) so every push exercises the CLI exactly the way agents are expected
 to use it.
4. **Exit criteria**: CI must fail if any CLI command returns a non-zero code, and the pipeline runtime should stay under 3 minutes.

## 2. Promote Templates as Installable Packages
**Objective**: enable reproducible scaffolds by treating templates as versioned artifacts.

1. Break the FastAPI scaffold into a versioned package under `templates/python-fastapi` with its own `pyproject.toml` so it can
be published and reused independently.
2. Update the CLI to fetch templates via a simple registry (local path or Git URL) and verify template integrity hashes before applying them.
3. Document how agents can pin template versions inside `project.json` to ensure reproducible scaffolds.
4. **Exit criteria**: CLI users can specify `--template python-fastapi@0.1.0` and receive a deterministic scaffold verified by a hash.

## 3. Enrich Agent-Facing Documentation
**Objective**: shrink onboarding time for new agents and reduce misinterpretation of CLI feedback.

1. Extend `docs/overview.md` with concrete acceptance criteria for each lifecycle stage (init, scaffold, validate, iterate) and highlight common failure recovery steps.
2. Create a “playbook” section containing example transcripts of successful and unsuccessful runs so agents learn to interpret CLI output consistently.
3. Cross-link these docs from the README quickstart and surface them in the CLI `--help` output (e.g., `see docs/overview.md#playbook`).
4. **Exit criteria**: at least two end-to-end transcripts live in the docs and are referenced from CLI help text.

## 4. Enforce Metadata Quality via Schema + Linters
**Objective**: keep `project.json` trustworthy by pairing schema constraints with automated linting.

1. 擴充 `schema/project.schema.json` 的欄位限制（kebab-case ID、角色枚舉、Markdown 路徑）——**已完成**。
2. 導入 `python cli/agent_cli.py lint-metadata` 子命令，獨立檢查中繼資料並支援 `--check-documents` ——**已完成**。
3. 下一步：加入 pre-commit hook 與 CI 工作，確保 lint-metadata 自動執行。
4. **Exit criteria**: `python cli/agent_cli.py lint-metadata` 與 pre-commit/CI 皆必須阻擋違規的 metadata 內容，並提供清楚的欄位/檔名提示。
