---
allowed-tools: Bash(*), Read(*)
description: Push completed todos back to GitHub checkboxes
argument-hint: [issue-number]
---

# Push Completed Todos to GitHub

## Your Task
Update GitHub issue checkboxes based on your completed todos.

Run the update script:
!python3 scripts/utilities/update-github-checkboxes.py $ARGUMENTS

This will:
1. Look for completed todos matching the issue number
2. Find the corresponding checkboxes in the GitHub issue
3. Check the boxes for completed items
4. Update the issue on GitHub

Show the results to the user.