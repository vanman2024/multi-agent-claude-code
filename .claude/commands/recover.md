---
allowed-tools: Bash(*), Read(*)
description: Find and recover deleted files from Git history
argument-hint: [list | search <pattern> | file <path> | recent]
---

# Recover Command - Find & Restore Deleted Files

<!--
WHEN TO USE THIS COMMAND:
- Finding files that were deleted from the project
- Searching for lost code or documentation
- Recovering accidentally deleted files
- Exploring what was removed from the codebase
- Cherry-picking old implementations back

EXAMPLES:
/recover                    - Show recent deletions (last 30 days)
/recover list              - List ALL deleted files in history
/recover search auth       - Find deleted files matching "auth"
/recover file src/auth.js  - Recover specific deleted file
/recover recent            - Show files deleted in last 10 commits

This command helps you find and restore any file that was ever tracked by Git.
-->

## Your Task

Help recover deleted files from Git history based on the argument provided.

### STEP-BY-STEP PROCEDURES (FOLLOW IN ORDER):

---

### Operation: recent (default when no args)

**Step 1**: Show files deleted in last 30 days
Run: !`git log --diff-filter=D --summary --since="30 days ago" | grep "delete mode" | awk '{print $NF}' | sort -u`

**Step 2**: Count total deletions
Run: !`git log --diff-filter=D --summary --since="30 days ago" | grep -c "delete mode"`

**Step 3**: Show summary
Display:
- Number of files deleted in last 30 days
- List of deleted files (grouped by type if many)
- Tip: Use `/recover file <path>` to restore any file

---

### Operation: list

**Step 1**: Get ALL deleted files from entire history
Run: !`git log --diff-filter=D --summary --all | grep "delete mode" | awk '{print $NF}' | sort -u`

**Step 2**: Group by file type
- Group .js/.ts files as "JavaScript/TypeScript"
- Group .md files as "Documentation"
- Group .json/.yaml as "Configuration"
- Group others as "Other files"

**Step 3**: Show counts and samples
For each group, show:
- Total count
- First 5 file paths as examples
- If more than 20 total, say "Use /recover search <pattern> to filter"

---

### Operation: search <pattern>

**Step 1**: Find deleted files matching pattern
Run: !`git log --diff-filter=D --summary --all | grep "delete mode" | awk '{print $NF}' | grep -i "<pattern>" | sort -u`

**Step 2**: For each matching file, show when deleted
Run: !`git log --diff-filter=D --summary --follow -- <file> | head -1`

**Step 3**: Show recovery options
For each file found:
- Show file path
- Show commit where deleted (first 7 chars of SHA)
- Show date deleted
- Show command to recover: `/recover file <path>`

---

### Operation: file <path>

**Step 1**: Check if file currently exists
Run: !`test -f "<path>" && echo "EXISTS" || echo "DELETED"`
If EXISTS, say "File already exists. Use a different name or delete current file first." and STOP

**Step 2**: Find the commit that deleted the file
Run: !`git rev-list -n 1 HEAD -- "<path>"`
Save as DELETE_COMMIT

**Step 3**: Get the last commit before deletion
Run: !`git rev-list -n 1 ${DELETE_COMMIT}^ -- "<path>"`
Save as LAST_COMMIT

**Step 4**: Show file info before deletion
Run: !`git show --stat ${LAST_COMMIT} -- "<path>" | head -5`

**Step 5**: Show preview of file content
Run: !`git show ${LAST_COMMIT}:"<path>" | head -20`
Say: "Showing first 20 lines of file..."

**Step 6**: Ask for confirmation
Say: "Recover this file to its original location?"
Options:
1. Yes - restore to original path
2. Different name - restore with new name
3. View full - see entire file content
4. Cancel

**Step 7**: If confirmed, restore the file
Run: !`git checkout ${LAST_COMMIT} -- "<path>"`
Say: "✓ File recovered: <path>"
Say: "Note: File is staged for commit. Review and commit when ready."

---

### Operation: recent

**Step 1**: Show files deleted in last 10 commits
Run: !`git log --diff-filter=D --summary -10 | grep "delete mode" | awk '{print $NF}'`

**Step 2**: Show commit info for each deletion
Run: !`git log --diff-filter=D --oneline -10`

**Step 3**: Display organized summary
Show:
- Commit hash | commit message | files deleted
- Group by commit
- Show recovery command for each

---

## Special Features

### Finding Lost Code Snippets
If user mentions specific code/function/text they lost:

**Step 1**: Search through deleted file contents
Run: !`git grep "<search_term>" $(git rev-list --all) -- | grep -v "^Binary" | head -20`

**Step 2**: If found, identify the file
Show which deleted files contained that code

**Step 3**: Offer to recover those files

### Bulk Recovery
If user wants to recover multiple files:

**Step 1**: List files to recover
**Step 2**: Check none currently exist
**Step 3**: Restore all at once
Run: !`git checkout <commit>^ -- file1 file2 file3...`

### Show Deletion History
For any file path, show its deletion history:

**Step 1**: Show all times file was deleted/added
Run: !`git log --follow --diff-filter=AD --summary -- "<path>"`

This shows if file was deleted and re-added multiple times.

## Important Rules

1. **ALWAYS check if file exists** before recovering
2. **Show preview** of what will be recovered
3. **Files are staged** after recovery - remind user to review
4. **Preserve path structure** unless user wants different location
5. **Can recover entire directories** using same technique

## Error Handling

If file never existed:
- Say "No file found at that path in Git history"
- Suggest using `/recover search` with partial name

If very old deletion (>1 year):
- Warn that file is very old
- Show last modified date
- Still offer to recover if wanted

## Tips to Share

After any recovery operation, remind user:
- "Recovered files are staged but not committed"
- "Review the changes with 'git diff --staged'"
- "Commit when satisfied or 'git reset' to unstage"
- "Use '/recover list' to see all deleted files"