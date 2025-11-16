from .helpers import run_cli


def test_status_reports_clean_project(tmp_path):
    project_dir = tmp_path / "project"
    result = run_cli("init", str(project_dir))
    assert result.returncode == 0, result.stdout

    status_result = run_cli("status", str(project_dir))
    assert status_result.returncode == 0, status_result.stdout
    assert "Project status" in status_result.stdout
    assert "No warnings detected" in status_result.stdout


def test_status_flags_missing_documents(tmp_path):
    project_dir = tmp_path / "project"
    run_cli("init", str(project_dir))

    (project_dir / "project.md").unlink()

    status_result = run_cli("status", str(project_dir))
    assert status_result.returncode == 0, status_result.stdout
    assert "Warnings detected" in status_result.stdout
    assert "project.md" in status_result.stdout
