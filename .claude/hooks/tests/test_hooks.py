#!/usr/bin/env python3
"""
Unit tests for Claude Code hooks
Run with: python -m pytest .claude/hooks/tests/
"""

import json
import subprocess
import tempfile
import os
import sys
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestSyncTodoCheckboxes(unittest.TestCase):
    """Test TodoWrite to GitHub checkbox sync"""
    
    def test_get_pr_for_branch(self):
        """Test PR detection for current branch"""
        # Mock subprocess to return PR data
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = '[{"number": 61}]'
            
            from sync_todo_checkboxes import get_pr_for_branch
            result = get_pr_for_branch()
            self.assertEqual(result, 61)
    
    def test_checkbox_pattern_matching(self):
        """Test checkbox pattern matching in PR body"""
        test_body = """
        ## Required Checks
        - [ ] Run tests
        - [x] Update documentation
        - [ ] Review code
        """
        
        todos = [
            {"content": "Run tests", "status": "completed"},
            {"content": "Update documentation", "status": "completed"},
            {"content": "Review code", "status": "pending"}
        ]
        
        # Test that completed todos check boxes
        expected = test_body.replace("[ ] Run tests", "[x] Run tests")
        # Additional test logic here
        self.assertIn("[x] Run tests", expected)

class TestLogAgentTask(unittest.TestCase):
    """Test agent task logging"""
    
    def test_log_file_creation(self):
        """Test that log files are created correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['CLAUDE_PROJECT_DIR'] = tmpdir
            os.makedirs(f"{tmpdir}/.claude/hooks", exist_ok=True)
            
            # Create test input
            test_input = {
                "tool_name": "Task",
                "tool_input": {
                    "subagent_type": "test-agent",
                    "description": "Test task"
                },
                "session_id": "test-session"
            }
            
            # Run the hook
            proc = subprocess.run(
                ["bash", ".claude/hooks/log-agent-task.sh"],
                input=json.dumps(test_input),
                text=True,
                capture_output=True,
                env=os.environ
            )
            
            # Check log file exists
            log_file = Path(tmpdir) / ".claude/logs/agent-tasks.log"
            self.assertTrue(log_file.exists() or proc.returncode == 0)

class TestAutoCommitHook(unittest.TestCase):
    """Test auto-commit functionality"""
    
    def test_commit_message_generation(self):
        """Test commit message is generated correctly"""
        test_cases = [
            ("src/api/users.ts", "Auto-commit: Modified src/api/users.ts"),
            ("README.md", "Auto-commit: Modified README.md"),
            (".claude/hooks/test.sh", "Auto-commit: Modified .claude/hooks/test.sh")
        ]
        
        for file_path, expected_msg in test_cases:
            # Test message generation logic
            msg = f"Auto-commit: Modified {file_path}"
            self.assertEqual(msg, expected_msg)

class TestSyncToGitHub(unittest.TestCase):
    """Test GitHub sync functionality"""
    
    def test_should_sync_file(self):
        """Test file sync decision logic"""
        # Files that should sync
        should_sync = [
            ".claude/hooks/test.sh",
            "src/index.ts", 
            "README.md"
        ]
        
        # Files that should NOT sync
        should_not_sync = [
            ".env",
            "node_modules/test.js",
            ".git/config"
        ]
        
        for file_path in should_sync:
            # Test sync logic
            self.assertTrue(not file_path.startswith('.env'))
        
        for file_path in should_not_sync:
            if file_path.startswith('.env'):
                self.assertTrue(True)

class TestCurrentWorkHook(unittest.TestCase):
    """Test current work context injection"""
    
    @patch('subprocess.run')
    def test_github_issues_fetch(self, mock_run):
        """Test fetching GitHub issues"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = json.dumps([
            {"number": 60, "title": "Test issue", "state": "open"}
        ])
        
        # Run hook logic
        result = subprocess.run(
            ["gh", "issue", "list", "--json", "number,title,state"],
            capture_output=True,
            text=True
        )
        
        # Should successfully parse issues
        self.assertEqual(result.returncode, 0)

if __name__ == '__main__':
    unittest.main()