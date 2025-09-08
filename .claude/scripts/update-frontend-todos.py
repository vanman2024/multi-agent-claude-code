#!/usr/bin/env python3

"""
Import ALL todos from all session files without de-duplication
This gives the frontend the full 146 todos it expects
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Paths
TODO_DIR = Path.home() / '.claude' / 'todos'
PROJECT_DIR = Path.home() / '.claude' / 'projects' / '-home-gotime2022-Projects-multi-agent-claude-code'
MASTER_FILE = PROJECT_DIR / 'todo-archive' / 'master-todos.json'

def main():
    # Find all session registration files for this project
    session_files = list(PROJECT_DIR.glob('*.jsonl'))
    print(f"Found {len(session_files)} sessions registered to this project")
    
    # Collect ALL todos without de-duplication (to match frontend count)
    all_todos = []
    
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
                    todo['session_date'] = datetime.fromtimestamp(reg_file.stat().st_mtime).isoformat()
                    all_todos.append(todo)  # Keep ALL todos, including duplicates
                            
            except Exception as e:
                print(f"Error reading {todo_file}: {e}")
    
    # Count by status
    status_counts = {}
    for todo in all_todos:
        status = todo.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Save to master file with ALL todos (including duplicates)
    MASTER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MASTER_FILE, 'w') as f:
        json.dump(all_todos, f, indent=2)
    
    print(f"\n✅ Successfully imported {len(all_todos)} todos (including duplicates)!")
    print(f"\nBreakdown by status:")
    print(f"  Completed:   {status_counts.get('completed', 0)}")
    print(f"  In Progress: {status_counts.get('in_progress', 0)}")
    print(f"  Pending:     {status_counts.get('pending', 0)}")
    print(f"\n📊 Total: {len(all_todos)} todos in master archive")

if __name__ == '__main__':
    main()