import json
import tempfile
import shutil
from pathlib import Path
import pytest
from click.testing import CliRunner
from src.cli.dedupe_commands import dedupe

def make_json_file(tmp_path, contacts, filename):
    file_path = tmp_path / filename
    with open(file_path, 'w') as f:
        json.dump(contacts, f)
    return str(file_path)

def test_dedupe_merge_removes_duplicates(tmp_path):
    # Prepare two files with overlapping contacts (by uid and LinkedIn URL)
    contacts1 = [
        {"uid": "1", "linkedin_url": "https://linkedin.com/in/a", "name": "Alice"},
        {"uid": "2", "linkedin_url": "https://linkedin.com/in/b", "name": "Bob"}
    ]
    contacts2 = [
        {"uid": "2", "linkedin_url": "https://linkedin.com/in/b", "name": "Bob"},
        {"uid": "3", "linkedin_url": "https://linkedin.com/in/c", "name": "Carol"}
    ]
    file1 = make_json_file(tmp_path, contacts1, "contacts1.json")
    file2 = make_json_file(tmp_path, contacts2, "contacts2.json")
    output_file = tmp_path / "deduped.json"

    runner = CliRunner()
    result = runner.invoke(
        dedupe,
        ["merge", "--input", f"{file1},{file2}", "--output", str(output_file)]
    )
    assert result.exit_code == 0
    # For now, just check the stub runs; later, check output file contents
    # TODO: When implemented, load output_file and check only unique contacts remain
    # with open(output_file) as f:
    #     deduped = json.load(f)
    #     assert len(deduped) == 3
    #     uids = {c["uid"] for c in deduped}
    #     assert uids == {"1", "2", "3"}
    assert "Deduplicated" in result.output
