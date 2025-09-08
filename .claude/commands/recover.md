---
allowed-tools: Bash(*), Read(*)
description: Find and recover deleted files from Git history
argument-hint: [list | search <pattern> | file <path> | recent]
---

# Recover Deleted Files

## Your Task

Help user recover deleted files based on: $ARGUMENTS

### If no arguments or "recent":
Show files deleted in last 30 days:
!git log --diff-filter=D --summary --since="30 days ago" --format="%h %s" | grep -B1 "delete mode" | head -20

### If argument is "list":
Show all deleted files:
!git log --diff-filter=D --summary --all | grep "delete mode" | awk '{print $NF}' | sort -u | head -50

### If argument starts with "search":
Extract search term and find matching deleted files:
!git log --diff-filter=D --summary --all | grep "delete mode" | awk '{print $NF}' | grep -i "$ARGUMENTS" | head -20

### If argument starts with "file" or is a file path:
1. Check if file exists:
   !test -f "$ARGUMENTS" && echo "File exists" || echo "File was deleted"
   
2. If deleted, find deletion commit:
   !git log --diff-filter=D --format="%h" -- "$ARGUMENTS" | head -1
   
3. Recover the file (use the commit hash from step 2):
   !git checkout COMMIT~1 -- "$ARGUMENTS"
   
Tell user: "File recovered and staged. Review with 'git diff --staged'"