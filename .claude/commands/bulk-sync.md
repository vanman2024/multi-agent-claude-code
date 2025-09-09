---
allowed-tools: Bash(*), TodoWrite(*)
description: Bulk sync all GitHub issue checkboxes to todos
argument-hint: [--all | --assigned | issue-number]
---

# Bulk Sync GitHub Issues to Todos

## Your Task
Fetch checkboxes from multiple GitHub issues and intelligently merge with existing todos.

1. First, export your current todos to avoid duplicates:
   - Get your current todo list from TodoWrite
   - Save it to a temporary JSON file for the script to use

2. Run the bulk sync script with deduplication:
!python3 scripts/utilities/bulk-sync-todos.py $ARGUMENTS

3. The script will:
   - Fetch all checkboxes from GitHub (body + comments)
   - Compare against your existing todos
   - Return only NEW unique todos to add

4. If there are new todos, use TodoWrite to ADD them (don't replace your whole list)

5. Show a summary:
   - How many new todos were found
   - How many duplicates were avoided
   - What was added to your list

This creates a comprehensive todo list from GitHub issues, making you aware of all work items across the project.