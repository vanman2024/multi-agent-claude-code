---
allowed-tools: Bash(*), TodoWrite(*)
description: Bulk sync all GitHub issue checkboxes to todos
argument-hint: [--all | --assigned | issue-number]
---

# Bulk Sync GitHub Issues to Todos

## Your Task
Fetch checkboxes from multiple GitHub issues and load them directly into TodoWrite.

1. Run the bulk sync script to get todos:
!python3 scripts/utilities/bulk-sync-todos.py $ARGUMENTS

2. Parse the JSON output from the script and load it directly into TodoWrite using the TodoWrite tool

3. Show a summary of what was loaded

This creates a comprehensive todo list from GitHub issues, making you aware of all work items across the project.