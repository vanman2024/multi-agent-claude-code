#!/usr/bin/env python3
"""
Hook: Sync TodoWrite with GitHub PR checkboxes
Event: PostToolUse (TodoWrite)
Purpose: Bidirectional sync between Claude's todos and GitHub PR checkboxes
"""

import json
import sys
import os
import re
import subprocess
from pathlib import Path

def get_pr_for_branch():
    """Get PR number for current branch"""
    try:
        result = subprocess.run(
            ["gh", "pr", "list", "--head", subprocess.check_output(
                ["git", "branch", "--show-current"], text=True).strip(),
             "--json", "number"],
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            if data:
                return data[0].get("number")
    except:
        pass
    return None

def get_pr_body(pr_number):
    """Get PR description with checkboxes"""
    try:
        result = subprocess.run(
            ["gh", "pr", "view", str(pr_number), "--json", "body"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("body", "")
    except:
        pass
    return ""

def update_pr_checkboxes(pr_number, todos):
    """Update GitHub PR checkboxes based on TodoWrite state"""
    
    # Get current PR body
    current_body = get_pr_body(pr_number)
    if not current_body:
        return False
    
    updated_body = current_body
    
    # Map todo items to checkboxes
    for todo in todos:
        content = todo.get("content", "")
        status = todo.get("status", "pending")
        
        # Find matching checkbox in PR body (fuzzy match)
        # Look for unchecked box with similar text
        pattern = r'\[ \]([^\n]*' + re.escape(content[:20]) + r'[^\n]*)'
        
        if status == "completed":
            # Check the box
            updated_body = re.sub(pattern, r'[x]\1', updated_body, count=1)
        
        # Also try exact match
        if status == "completed":
            updated_body = updated_body.replace(f"[ ] {content}", f"[x] {content}")
        elif status == "pending":
            updated_body = updated_body.replace(f"[x] {content}", f"[ ] {content}")
    
    # Only update if changed
    if updated_body != current_body:
        # Update PR description
        try:
            # Write to temp file to avoid shell escaping issues
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                f.write(updated_body)
                temp_path = f.name
            
            result = subprocess.run(
                ["gh", "pr", "edit", str(pr_number), "--body-file", temp_path],
                capture_output=True, text=True
            )
            
            os.unlink(temp_path)
            
            if result.returncode == 0:
                print(f"✅ Synced {len(todos)} todos to PR #{pr_number} checkboxes")
                return True
        except Exception as e:
            print(f"Error updating PR: {e}", file=sys.stderr)
    
    return False

def main():
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    
    # Only process TodoWrite tool
    tool_name = input_data.get("tool_name", "")
    if tool_name != "TodoWrite":
        sys.exit(0)
    
    # Get the todos from tool input
    tool_input = input_data.get("tool_input", {})
    todos = tool_input.get("todos", [])
    
    if not todos:
        sys.exit(0)
    
    # Find PR for current branch
    pr_number = get_pr_for_branch()
    if not pr_number:
        print("No PR found for current branch", file=sys.stderr)
        sys.exit(0)
    
    # Sync todos to GitHub PR checkboxes
    if update_pr_checkboxes(pr_number, todos):
        # Also add a comment about the sync
        completed = sum(1 for t in todos if t.get("status") == "completed")
        total = len(todos)
        
        comment = f"🔄 **Todo Sync Update**\n\n"
        comment += f"Progress: {completed}/{total} tasks completed\n\n"
        comment += "Updated PR checkboxes to match TodoWrite state.\n"
        
        subprocess.run(
            ["gh", "pr", "comment", str(pr_number), "--body", comment],
            capture_output=True
        )
    
    sys.exit(0)

if __name__ == "__main__":
    main()