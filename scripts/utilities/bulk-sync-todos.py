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

def parse_checkboxes_from_text(text, issue_number, source="body"):
    """Extract checkboxes from any text (body, comments, etc)."""
    checkboxes = []
    
    if not text:
        return checkboxes
    
    # Match GitHub checkbox syntax: - [ ] or - [x]
    checkbox_pattern = r'^[\s]*[-*]\s*\[([ xX])\]\s*(.+)$'
    
    for line in text.split('\n'):
        match = re.match(checkbox_pattern, line.strip())
        if match:
            is_checked = match.group(1).lower() == 'x'
            content = match.group(2).strip()
            
            # Create todo with issue context and source
            if source == "comment":
                todo_content = f"#{issue_number} (comment): {content}"
            elif source == "sub-issue":
                todo_content = f"#{issue_number} (sub): {content}"
            else:
                todo_content = f"#{issue_number}: {content}"
            
            checkboxes.append({
                'content': todo_content,
                'status': 'completed' if is_checked else 'pending',
                'activeForm': f"Working on: {content[:50]}",
                'issue_number': issue_number,
                'source': source
            })
    
    return checkboxes

def get_issue_comments(issue_number):
    """Fetch all comments for an issue."""
    try:
        result = subprocess.run(
            ['gh', 'issue', 'view', str(issue_number), '--comments', '--json', 'comments'],
            capture_output=True,
            text=True,
            check=True
        )
        
        data = json.loads(result.stdout)
        return data.get('comments', [])
    except:
        return []

def get_sub_issues(issue_number):
    """Fetch sub-issues linked to this issue."""
    try:
        # Use gh to get the issue body and parse for sub-issue references
        result = subprocess.run(
            ['gh', 'api', f'repos/:owner/:repo/issues/{issue_number}/timeline', 
             '--jq', '.[] | select(.event == "cross-referenced") | .source.issue.number'],
            capture_output=True,
            text=True
        )
        
        sub_issue_numbers = [int(n) for n in result.stdout.strip().split('\n') if n]
        return sub_issue_numbers
    except:
        return []

def parse_checkboxes_from_issue(issue):
    """Extract all checkboxes from issue body, comments, and sub-issues."""
    all_checkboxes = []
    issue_number = issue['number']
    
    # 1. Parse main issue body
    body_checkboxes = parse_checkboxes_from_text(
        issue.get('body', ''), 
        issue_number, 
        source="body"
    )
    all_checkboxes.extend(body_checkboxes)
    
    # 2. Parse comments
    comments = get_issue_comments(issue_number)
    for comment in comments:
        comment_text = comment.get('body', '')
        comment_checkboxes = parse_checkboxes_from_text(
            comment_text,
            issue_number,
            source="comment"
        )
        if comment_checkboxes:
            all_checkboxes.extend(comment_checkboxes)
    
    # Store issue title for reference
    for cb in all_checkboxes:
        cb['issue_title'] = issue['title']
    
    return all_checkboxes

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
            
            # Count by source
            body_count = sum(1 for cb in checkboxes if cb.get('source') == 'body')
            comment_count = sum(1 for cb in checkboxes if cb.get('source') == 'comment')
            
            print(f"\n📌 Issue #{issue['number']}: {issue['title']}")
            print(f"   Found {len(checkboxes)} checkboxes total:")
            print(f"   📝 From body: {body_count}")
            if comment_count > 0:
                print(f"   💬 From comments: {comment_count}")
            
            # Show first few items
            for cb in checkboxes[:3]:
                status = "✅" if cb['status'] == 'completed' else "⬜"
                source_indicator = " 💬" if cb.get('source') == 'comment' else ""
                print(f"   {status} {cb['content'][:60]}...{source_indicator}")
            
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
    
    print(f"\n📝 Ready to load {len(todos_for_claude)} todos into TodoWrite")
    
    # Show the JSON for direct use with TodoWrite
    print("\n🔧 JSON for TodoWrite (copy this entire block):")
    print("=" * 60)
    print(json.dumps(todos_for_claude, indent=2))
    print("=" * 60)
    
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