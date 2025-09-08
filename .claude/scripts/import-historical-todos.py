#!/usr/bin/env python3

"""
Import all historical todos from individual session files into the master archive
"""

import json
import os
from pathlib import Path

# Paths
TODO_DIR = Path.home() / '.claude' / 'todos'
PROJECT_DIR = Path.home() / '.claude' / 'projects' / '-home-gotime2022-Projects-multi-agent-claude-code'
TODO_INDEX = PROJECT_DIR / 'todo-index.json'
MASTER_FILE = PROJECT_DIR / 'todo-archive' / 'master-todos.json'

def main():
    # Load the todo index
    with open(TODO_INDEX) as f:
        index = json.load(f)
    
    print(f"Found {len(index['todo_mappings'])} sessions with {index['total_todos']} total todos")
    
    # Load existing master (if any)
    if MASTER_FILE.exists():
        with open(MASTER_FILE) as f:
            master_todos = json.load(f)
    else:
        master_todos = []
    
    # Create a map of existing todos by content
    existing_map = {todo.get('content', ''): todo for todo in master_todos}
    
    # Process each session file
    imported = 0
    skipped = 0
    
    for mapping in index['todo_mappings']:
        todo_file = TODO_DIR / mapping['todo_file']
        
        if todo_file.exists():
            try:
                with open(todo_file) as f:
                    session_todos = json.load(f)
                
                for todo in session_todos:
                    content = todo.get('content', '')
                    
                    # Skip if already exists
                    if content in existing_map:
                        skipped += 1
                        # Update status if newer
                        if todo.get('status') == 'completed' and existing_map[content].get('status') != 'completed':
                            existing_map[content]['status'] = 'completed'
                    else:
                        # Add metadata
                        todo['session_id'] = mapping['session_id']
                        todo['session_date'] = mapping['session_date']
                        existing_map[content] = todo
                        imported += 1
                        
            except Exception as e:
                print(f"Error processing {todo_file}: {e}")
    
    # Save updated master
    master_todos = list(existing_map.values())
    
    # Ensure directory exists
    MASTER_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(MASTER_FILE, 'w') as f:
        json.dump(master_todos, f, indent=2)
    
    print(f"✅ Imported {imported} new todos, skipped {skipped} duplicates")
    print(f"📊 Total in master archive: {len(master_todos)}")
    
    # Show status breakdown
    status_counts = {}
    for todo in master_todos:
        status = todo.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("\nStatus breakdown:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")

if __name__ == '__main__':
    main()