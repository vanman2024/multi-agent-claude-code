#!/usr/bin/env python3
"""
Update GitHub issue checkboxes based on completed todos.
This syncs completed todos back to GitHub by checking the boxes.
"""

import json
import subprocess
import sys
import re
from pathlib import Path

def get_issue_body(issue_number):
    """Fetch the current issue body from GitHub."""
    try:
        result = subprocess.run(
            ['gh', 'issue', 'view', str(issue_number), '--json', 'body'],
            capture_output=True,
            text=True,
            check=True
        )
        
        data = json.loads(result.stdout)
        return data.get('body', '')
    except subprocess.CalledProcessError as e:
        print(f"Error fetching issue #{issue_number}: {e}")
        return None

def update_issue_body(issue_number, new_body):
    """Update the issue body on GitHub."""
    try:
        # Write body to temp file to avoid escaping issues
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(new_body)
            temp_file = f.name
        
        result = subprocess.run(
            ['gh', 'issue', 'edit', str(issue_number), '--body-file', temp_file],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Clean up temp file
        Path(temp_file).unlink()
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error updating issue #{issue_number}: {e}")
        return False

def load_completed_todos(issue_number):
    """Load completed todos for a specific issue from local todo files."""
    completed_items = []
    todo_dir = Path.home() / '.claude' / 'todos'
    
    if not todo_dir.exists():
        return completed_items
    
    # Look through all todo files for this issue
    for todo_file in todo_dir.glob('*.json'):
        try:
            with open(todo_file, 'r') as f:
                todos = json.load(f)
                
                for todo in todos:
                    content = todo.get('content', '')
                    status = todo.get('status', '')
                    
                    # Check if this todo is for our issue and is completed
                    if f"#{issue_number}:" in content and status == 'completed':
                        # Extract the actual task description
                        task_text = content.split(f"#{issue_number}:", 1)[1].strip()
                        # Remove any source indicators
                        task_text = re.sub(r'\s*\(comment\):\s*', '', task_text)
                        task_text = re.sub(r'\s*\(sub\):\s*', '', task_text)
                        completed_items.append(task_text)
        except:
            pass
    
    return completed_items

def update_checkboxes_in_body(body, completed_items):
    """Update checkbox status in the issue body."""
    if not body or not completed_items:
        return body
    
    updated_body = body
    changes_made = 0
    
    for item in completed_items:
        # Escape special regex characters in the item text
        escaped_item = re.escape(item)
        
        # Pattern to find unchecked box with this text
        pattern = r'^(\s*[-*]\s*)\[ \](\s*' + escaped_item + r')$'
        replacement = r'\1[x]\2'
        
        # Check if we can find and update this checkbox
        new_body = re.sub(pattern, replacement, updated_body, flags=re.MULTILINE)
        
        if new_body != updated_body:
            changes_made += 1
            updated_body = new_body
            print(f"  ✅ Checked: {item[:60]}...")
    
    return updated_body, changes_made

def sync_completed_todos_to_github(issue_number):
    """Main function to sync completed todos back to GitHub."""
    print(f"\n🔄 SYNCING COMPLETED TODOS TO GITHUB ISSUE #{issue_number}")
    print("=" * 60)
    
    # Step 1: Get current issue body
    print(f"\n📋 Fetching issue #{issue_number} from GitHub...")
    current_body = get_issue_body(issue_number)
    
    if not current_body:
        print("❌ Failed to fetch issue")
        return False
    
    # Step 2: Load completed todos
    print(f"\n🔍 Looking for completed todos for issue #{issue_number}...")
    completed_items = load_completed_todos(issue_number)
    
    if not completed_items:
        print("  No completed todos found for this issue")
        return True
    
    print(f"  Found {len(completed_items)} completed todos")
    
    # Step 3: Update checkboxes in body
    print(f"\n📝 Updating checkboxes in issue body...")
    updated_body, changes = update_checkboxes_in_body(current_body, completed_items)
    
    if changes == 0:
        print("  No checkboxes needed updating (already checked or not found)")
        return True
    
    # Step 4: Push updates to GitHub
    print(f"\n⬆️ Pushing {changes} checkbox updates to GitHub...")
    if update_issue_body(issue_number, updated_body):
        print(f"✅ Successfully updated {changes} checkboxes in issue #{issue_number}")
        return True
    else:
        print(f"❌ Failed to update issue #{issue_number}")
        return False

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 update-github-checkboxes.py <issue-number>")
        print("\nThis script syncs completed todos back to GitHub by checking the boxes.")
        sys.exit(1)
    
    try:
        issue_number = int(sys.argv[1])
    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid issue number")
        sys.exit(1)
    
    # Run the sync
    success = sync_completed_todos_to_github(issue_number)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()