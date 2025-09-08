#!/usr/bin/env python3
"""
Parse checkboxes from GitHub issues and sync with local todos.
"""

import re
import json
import subprocess
from pathlib import Path

def parse_checkboxes_from_markdown(text):
    """Extract checkbox items from markdown text."""
    checkboxes = []
    
    # Match GitHub checkbox syntax: - [ ] or - [x]
    checkbox_pattern = r'^[\s]*[-*]\s*\[([ xX])\]\s*(.+)$'
    
    for line in text.split('\n'):
        match = re.match(checkbox_pattern, line.strip())
        if match:
            is_checked = match.group(1).lower() == 'x'
            content = match.group(2).strip()
            checkboxes.append({
                'content': content,
                'status': 'completed' if is_checked else 'pending',
                'checked': is_checked
            })
    
    return checkboxes

def get_issue_from_github(issue_number):
    """Fetch issue details from GitHub using gh CLI."""
    try:
        # Get issue body using gh CLI
        result = subprocess.run(
            ['gh', 'issue', 'view', str(issue_number), '--json', 'body,title,number'],
            capture_output=True,
            text=True,
            check=True
        )
        
        issue_data = json.loads(result.stdout)
        return issue_data
    except subprocess.CalledProcessError as e:
        print(f"Error fetching issue #{issue_number}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing issue data: {e}")
        return None

def find_issue_numbers_in_todos(todos):
    """Find all issue numbers referenced in todos."""
    issue_numbers = set()
    issue_pattern = r'#(\d+)'
    
    for todo in todos:
        content = todo.get('content', '')
        matches = re.findall(issue_pattern, content)
        for match in matches:
            issue_numbers.add(int(match))
    
    return sorted(list(issue_numbers))

def sync_todos_with_github(issue_number=None):
    """Main sync function."""
    # Get current project todos
    todo_dir = Path.home() / '.claude' / 'todos'
    
    if issue_number:
        # Sync specific issue
        print(f"\n🔄 Syncing with GitHub Issue #{issue_number}")
        issue_data = get_issue_from_github(issue_number)
        
        if issue_data:
            checkboxes = parse_checkboxes_from_markdown(issue_data['body'])
            
            print(f"\n📋 Found {len(checkboxes)} checkboxes in Issue #{issue_number}:")
            print(f"   Title: {issue_data['title']}")
            
            for cb in checkboxes:
                status_emoji = "✅" if cb['checked'] else "⬜"
                print(f"   {status_emoji} {cb['content']}")
            
            # Format for TodoWrite
            todos_for_claude = []
            for cb in checkboxes:
                todos_for_claude.append({
                    'content': f"#{issue_number}: {cb['content']}",
                    'status': cb['status']
                })
            
            print(f"\n💡 To update your todos, use TodoWrite with these items:")
            print(json.dumps(todos_for_claude, indent=2))
    else:
        print("\n🔍 Looking for issue references in current todos...")
        # This would need to read current todos and find issue numbers
        # For now, just show the concept
        print("📌 Tip: Run with an issue number to sync, e.g.: sync-todos 152")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        try:
            issue_num = int(sys.argv[1])
            sync_todos_with_github(issue_num)
        except ValueError:
            print(f"Error: '{sys.argv[1]}' is not a valid issue number")
    else:
        sync_todos_with_github()