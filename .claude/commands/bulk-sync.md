---
allowed-tools: Bash(*), Read(*), TodoWrite(*)
description: Bulk sync all GitHub issue checkboxes to todos
argument-hint: [--all | --assigned | issue-number]
---

# Bulk Sync GitHub Issues to Todos

## Your Task
Fetch checkboxes from multiple GitHub issues and load them into TodoWrite.

Run the bulk sync script:
!python3 scripts/utilities/bulk-sync-todos.py $ARGUMENTS

Then:
1. Read the generated bulk-todos.json file:
@/home/$USER/.claude/bulk-todos.json

2. Use TodoWrite to load all the todos from the file

3. Show a summary of what was loaded

This creates a comprehensive todo list from GitHub issues, making you aware of all work items across the project.