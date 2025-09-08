#!/usr/bin/env python3

"""
Import ALL todos from ALL sessions registered to this project
"""

import json
import os
from pathlib import Path
from collections import defaultdict

# Paths
TODO_DIR = Path.home() / '.claude' / 'todos'
PROJECT_DIR = Path.home() / '.claude' / 'projects' / '-home-gotime2022-Projects-multi-agent-claude-code'
MASTER_FILE = PROJECT_DIR / 'todo-archive' / 'master-todos.json'

def main():
    # Find all session registration files for this project
    session_files = list(PROJECT_DIR.glob('*.jsonl'))
    print(f"Found {len(session_files)} sessions registered to this project")
    
    # Collect all todos from these sessions
    all_todos = []
    todos_by_content = {}
    
    for reg_file in session_files:
        session_id = reg_file.stem
        todo_file = TODO_DIR / f"{session_id}.json"
        
        if todo_file.exists():
            try:
                with open(todo_file) as f:
                    session_todos = json.load(f)
                
                for todo in session_todos:
                    # Add session metadata
                    todo['session_id'] = session_id
                    
                    # Use content as key to merge duplicates
                    content = todo.get('content', '')
                    if content:
                        # If duplicate, keep the one with most recent/complete status
                        if content in todos_by_content:
                            existing = todos_by_content[content]
                            # Prefer completed > in_progress > pending
                            status_priority = {'completed': 3, 'in_progress': 2, 'pending': 1}
                            if status_priority.get(todo.get('status', ''), 0) > status_priority.get(existing.get('status', ''), 0):
                                todos_by_content[content] = todo
                        else:
                            todos_by_content[content] = todo
                            
            except Exception as e:
                print(f"Error reading {todo_file}: {e}")
    
    # Convert back to list
    all_todos = list(todos_by_content.values())
    
    # Count by status
    status_counts = defaultdict(int)
    for todo in all_todos:
        status_counts[todo.get('status', 'unknown')] += 1
    
    # Save to master file
    MASTER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MASTER_FILE, 'w') as f:
        json.dump(all_todos, f, indent=2)
    
    print(f"\n✅ Successfully imported {len(all_todos)} unique todos!")
    print(f"\nBreakdown by status:")
    print(f"  Completed:   {status_counts['completed']}")
    print(f"  In Progress: {status_counts['in_progress']}")
    print(f"  Pending:     {status_counts['pending']}")
    print(f"  Unknown:     {status_counts['unknown']}")
    print(f"\n📊 Total: {len(all_todos)} todos in master archive")

if __name__ == '__main__':
    main()