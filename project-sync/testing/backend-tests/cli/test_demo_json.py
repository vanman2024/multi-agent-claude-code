import json
import os
import subprocess
from pathlib import Path
import pytest


@pytest.mark.cli
def test_demo_sum_json_contract():
    repo_root = Path(__file__).resolve().parents[3]
    ops_path = repo_root / "project-sync" / "scripts" / "ops"
    assert ops_path.exists() and os.access(ops_path, os.X_OK)

    # Execute demo command via ops
    proc = subprocess.run(
        [str(ops_path), "demo", "sum", "--a", "2", "--b", "3", "--format", "json"],
        cwd=str(repo_root / "project-sync"),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr

    # Stable JSON schema contract
    payload = json.loads(proc.stdout.strip())
    assert payload == {
        "code": "SUM_OK",
        "data": {"a": 2, "b": 3, "sum": 5},
        "message": "",
        "ok": True,
        "version": "1",
    }

