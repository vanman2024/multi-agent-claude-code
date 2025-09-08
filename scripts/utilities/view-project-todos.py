#!/usr/bin/env python3
"""
Project-specific todo viewer.

This script ONLY shows todos for the current working directory's project.
It uses the project path to find all Claude sessions linked to THIS project
and displays their todos in a clean table format.

The viewer is read-only and project-isolated - it won't show todos from
other projects on your system.
"""

import json
import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def truncate(text, width):
    """Truncate text to fit in column width"""
    if len(text) <= width:
        return text
    return text[:width-3] + "..."

def get_project_todos(project_path=None):
    """Get all todos for the current project"""
    if not project_path:
        project_path = os.getcwd()
    
    project_hash = project_path.replace('/', '-')
    project_dir = Path.home() / '.claude' / 'projects' / project_hash
    todo_dir = Path.home() / '.claude' / 'todos'
    
    if not project_dir.exists():
        print(f"No project data found for {project_path}")
        return
    
    # Find all session files for this project
    session_files = list(project_dir.glob('*.jsonl'))
    
    todos_list = []
    stats = {'total': 0, 'completed': 0, 'in_progress': 0, 'pending': 0}
    
    for session_file in session_files:
        session_id = session_file.stem
        todo_file = todo_dir / f"{session_id}.json"
        
        if todo_file.exists() and todo_file.stat().st_size > 2:
            try:
                todos = json.loads(todo_file.read_text())
                for todo in todos:
                    status = todo.get('status', 'unknown')
                    content = todo.get('content', 'No content')
                    
                    # Add to list for table
                    todos_list.append({
                        'status': status,
                        'content': content,
                        'session': session_id[:8] + "..."
                    })
                    
                    # Update stats
                    stats['total'] += 1
                    if status == 'completed':
                        stats['completed'] += 1
                    elif status == 'in_progress':
                        stats['in_progress'] += 1
                    elif status == 'pending':
                        stats['pending'] += 1
            except:
                pass
    
    # Display results
    if stats['total'] == 0:
        print(f"\n📋 No todos found for project: {project_path}")
        print(f"   Project hash: {project_hash}")
        return
    
    print(f"\n📋 TODO LIST FOR CURRENT PROJECT")
    print(f"📁 Project: {project_path}")
    print(f"📂 Name: {os.path.basename(project_path)}")
    print("=" * 100)
    
    # Sort todos: in_progress first, then pending, then completed
    priority = {'in_progress': 0, 'pending': 1, 'completed': 2}
    todos_list.sort(key=lambda x: (priority.get(x['status'], 3), x['content']))
    
    # Print table header
    print(f"\n{'Status':<12} {'Task':<70} {'Session':<15}")
    print("-" * 100)
    
    # Print todos in table format
    for todo in todos_list:
        status = todo['status']
        
        # Status with emoji
        if status == 'completed':
            status_display = "✅ Done"
        elif status == 'in_progress':
            status_display = "🔄 Active"
        elif status == 'pending':
            status_display = "⏳ Pending"
        else:
            status_display = "❓ Unknown"
        
        # Print row
        content = truncate(todo['content'], 70)
        print(f"{status_display:<12} {content:<70} {todo['session']:<15}")
    
    # Print summary
    print("-" * 100)
    print(f"\n📊 SUMMARY")
    print("-" * 40)
    print(f"{'Total Tasks:':<20} {stats['total']:>5}")
    print(f"{'✅ Completed:':<20} {stats['completed']:>5} ({stats['completed']*100//stats['total'] if stats['total'] else 0}%)")
    print(f"{'🔄 In Progress:':<20} {stats['in_progress']:>5} ({stats['in_progress']*100//stats['total'] if stats['total'] else 0}%)")
    print(f"{'⏳ Pending:':<20} {stats['pending']:>5} ({stats['pending']*100//stats['total'] if stats['total'] else 0}%)")
    print()

if __name__ == "__main__":
    get_project_todos()