import json

from .helpers import run_cli


def test_lint_metadata_passes_on_fresh_init(tmp_path):
    project_dir = tmp_path / "project"
    result = run_cli("init", str(project_dir))
    assert result.returncode == 0, result.stdout

    lint_result = run_cli("lint-metadata", str(project_dir))
    assert lint_result.returncode == 0, lint_result.stdout
    assert "lint rules" in lint_result.stdout


def test_lint_metadata_rejects_bad_agent_id(tmp_path):
    project_dir = tmp_path / "project"
    run_cli("init", str(project_dir))
    metadata_path = project_dir / "project.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["agents"][0]["id"] = "Primary Agent"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    lint_result = run_cli("lint-metadata", str(project_dir))
    assert lint_result.returncode == 1
    assert "kebab-case" in lint_result.stdout


def test_lint_metadata_rejects_unsupported_role(tmp_path):
    project_dir = tmp_path / "project"
    run_cli("init", str(project_dir))
    metadata_path = project_dir / "project.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["agents"][0]["role"] = "manager"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    lint_result = run_cli("lint-metadata", str(project_dir))
    assert lint_result.returncode == 1
    assert "Agent role must be one of" in lint_result.stdout
