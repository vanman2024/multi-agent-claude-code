---
allowed-tools: Bash(*), TodoWrite(*), TodoRead(*)
description: Bulk sync all GitHub issue checkboxes to todos
argument-hint: [--all | --assigned | issue-number]
---

# Bulk Sync GitHub Issues to Todos

## Your Task
Fetch checkboxes from multiple GitHub issues and intelligently merge with existing todos.

1. Get current todos and prepare for deduplication:
   - Use TodoRead to get your current todo list
   - Export as JSON for the Python script to use

2. Run the bulk sync script with deduplication:
   - Pass existing todos via environment variable
   - Get new unique todos in JSON format
   - The script will compare and deduplicate

3. If there are new todos, use TodoWrite to ADD them:
   - Parse the JSON output from the script
   - Append new todos to existing list (don't replace)
   - Update TodoWrite with combined list

4. Show a summary of what was synced:
   - How many new todos were found
   - How many duplicates were avoided
   - What was added to your list

This creates a comprehensive todo list from GitHub issues, avoiding duplicates.