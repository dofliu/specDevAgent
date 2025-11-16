import subprocess
import sys
from pathlib import Path

CLI = Path(__file__).resolve().parents[1] / "cli" / "agent_cli.py"


def run_cli(*args, cwd=None):
    result = subprocess.run(
        [sys.executable, str(CLI), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=cwd,
    )
    return result
