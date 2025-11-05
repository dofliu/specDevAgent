# Python FastAPI Template

This template provisions a minimal FastAPI service and an accompanying smoke
 test that the specDevAgent CLI can drop into a freshly initialized project.

## What you get

- `app/main.py` — a FastAPI application exposing a single health endpoint.
- `tests/test_main.py` — a pytest suite that exercises the health endpoint.
- `requirements.txt` — dependencies required to run the application and tests.

## Usage

```bash
python cli/agent_cli.py scaffold /path/to/project --template python-fastapi
```

After scaffolding:

```bash
cd /path/to/project
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

The default endpoint will respond with a JSON payload of `{"status": "ok"}`.
