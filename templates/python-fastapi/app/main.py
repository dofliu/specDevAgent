"""Minimal FastAPI application shipped with the specDevAgent template."""

from fastapi import FastAPI

app = FastAPI(title="specDevAgent FastAPI Scaffold")


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a simple health payload used by automated checks."""
    return {"status": "ok", "message": "Hello from specDevAgent"}
