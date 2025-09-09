#!/usr/bin/env python3
"""
Bulk sync all GitHub issue checkboxes to Claude's TodoWrite.
Creates a comprehensive todo list from all project issues.
"""

import re
import json
import subprocess
from pathlib import Path

def get_all_open_issues():
    """Fetch all open issues for the repository."""
    try:
        result = subprocess.run(
            ['gh', 'issue', 'list', '--state', 'open', '--json', 'number,title,body,labels', '--limit', '100'],
            capture_output=True,
            text=True,
            check=True
        )
        
        issues = json.loads(result.stdout)
        return issues
    except subprocess.CalledProcessError as e:
        print(f"Error fetching issues: {e}")
        return []

def parse_checkboxes_from_issue(issue):
    """Extract all checkboxes from an issue."""
    checkboxes = []
    body = issue.get('body', '')
    
    if not body:
        return checkboxes
    
    # Match GitHub checkbox syntax: - [ ] or - [x]
    checkbox_pattern = r'^[\s]*[-*]\s*\[([ xX])\]\s*(.+)$'
    
    for line in body.split('\n'):
        match = re.match(checkbox_pattern, line.strip())
        if match:
            is_checked = match.group(1).lower() == 'x'
            content = match.group(2).strip()
            
            # Create todo with issue context
            todo_content = f"#{issue['number']}: {content}"
            
            checkboxes.append({
                'content': todo_content,
                'status': 'completed' if is_checked else 'pending',
                'activeForm': f"Working on: {content[:50]}",
                'issue_number': issue['number'],
                'issue_title': issue['title']
            })
    
    return checkboxes

def bulk_sync_todos(mode='all'):
    """Sync todos based on mode: all, assigned, or specific issue."""
    
    print("🔄 BULK TODO SYNC FROM GITHUB")
    print("=" * 60)
    
    all_todos = []
    issues_processed = 0
    
    if mode == 'all':
        print("\n📋 Fetching ALL open issues...")
        issues = get_all_open_issues()
    elif mode == 'assigned':
        print("\n👤 Fetching issues assigned to you...")
        result = subprocess.run(
            ['gh', 'issue', 'list', '--assignee', '@me', '--state', 'open', '--json', 'number,title,body,labels'],
            capture_output=True,
            text=True,
            check=True
        )
        issues = json.loads(result.stdout)
    else:
        # Specific issue number
        result = subprocess.run(
            ['gh', 'issue', 'view', mode, '--json', 'number,title,body,labels'],
            capture_output=True,
            text=True,
            check=True
        )
        issues = [json.loads(result.stdout)]
    
    # Process each issue
    for issue in issues:
        checkboxes = parse_checkboxes_from_issue(issue)
        if checkboxes:
            issues_processed += 1
            print(f"\n📌 Issue #{issue['number']}: {issue['title']}")
            print(f"   Found {len(checkboxes)} checkboxes")
            
            # Show first few items
            for cb in checkboxes[:3]:
                status = "✅" if cb['status'] == 'completed' else "⬜"
                print(f"   {status} {cb['content'][:60]}...")
            
            if len(checkboxes) > 3:
                print(f"   ... and {len(checkboxes) - 3} more")
            
            all_todos.extend(checkboxes)
    
    # Summary and format for TodoWrite
    print("\n" + "=" * 60)
    print(f"📊 SYNC SUMMARY")
    print(f"   Issues processed: {issues_processed}")
    print(f"   Total checkboxes: {len(all_todos)}")
    
    completed = sum(1 for t in all_todos if t['status'] == 'completed')
    pending = len(all_todos) - completed
    
    print(f"   ✅ Completed: {completed}")
    print(f"   ⬜ Pending: {pending}")
    
    # Group by issue for better organization
    by_issue = {}
    for todo in all_todos:
        issue_num = todo['issue_number']
        if issue_num not in by_issue:
            by_issue[issue_num] = []
        by_issue[issue_num].append(todo)
    
    # Format for TodoWrite (remove extra fields)
    todos_for_claude = []
    for todo in all_todos:
        todos_for_claude.append({
            'content': todo['content'],
            'status': todo['status'],
            'activeForm': todo['activeForm']
        })
    
    # Save to a file for Claude to load
    output_file = Path.home() / '.claude' / 'bulk-todos.json'
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(todos_for_claude, f, indent=2)
    
    print(f"\n💾 Todos saved to: {output_file}")
    print(f"📝 Use TodoWrite to load these {len(todos_for_claude)} todos")
    
    # Show the JSON for direct use
    print("\n🔧 To load in Claude, use TodoWrite with this data:")
    print(f"   (Showing first 5 todos, full list in {output_file})")
    print(json.dumps(todos_for_claude[:5], indent=2))
    
    return todos_for_claude

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == '--all':
            bulk_sync_todos('all')
        elif arg == '--assigned':
            bulk_sync_todos('assigned')
        else:
            # Assume it's an issue number
            bulk_sync_todos(arg)
    else:
        # Default to all open issues
        bulk_sync_todos('all')