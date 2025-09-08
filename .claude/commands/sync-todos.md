---
allowed-tools: Bash(*), mcp__github__get_issue(*), TodoWrite(*)
description: Sync todos with GitHub issue checkboxes
argument-hint: [issue-number]
---

# Sync Todos with GitHub Issues

## Your Task
Fetch the latest checkboxes from a GitHub issue and update your TodoWrite list.

If an issue number is provided in $ARGUMENTS:
1. Run the GitHub checkbox parser:
!python3 scripts/utilities/github-checkbox-parser.py $ARGUMENTS

2. Use mcp__github__get_issue to get the full issue details for issue #$ARGUMENTS

3. Parse the checkboxes from the issue body and update TodoWrite with:
   - Any new checkboxes not in your current todos
   - Status updates for existing todos (completed/pending)
   - Prefix each todo with the issue number (e.g., "#152: Task description")

4. Show what was added/updated

If no issue number provided:
1. Show current todos with: !python3 scripts/utilities/view-project-todos.py
2. Identify issue numbers in the todos
3. Suggest running the command with a specific issue number