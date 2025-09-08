---
allowed-tools: Bash(*), Read(*), TodoWrite(*), mcp__github(*)
description: Intelligent git workflow management with working state tracking
argument-hint: [status | commit | push | sync | pr | stash | log | stable | rollback | tags]
---

# Git Command

<!--
WHEN TO USE THIS COMMAND:
- Managing git operations with context awareness
- Creating intelligent commit messages
- Tracking and marking stable/working states
- Rolling back to known good commits
- Syncing with GitHub

EXAMPLES:
/git                - Show smart status + recent stable states
/git commit         - Commit with intelligent message
/git commit stable  - Commit and mark as stable state
/git push           - Push with safety checks
/git sync           - Pull, rebase, and push
/git pr             - Create PR with context
/git stable         - List all stable states
/git rollback       - Show recent stable states to rollback to
/git tags           - List all version tags
/git log            - Show recent commits with stability markers

NO COMPLEX FLAGS - Just simple operations that work intelligently
-->

## Your Task

Handle git operations intelligently based on the argument provided.

### STEP-BY-STEP PROCEDURES (FOLLOW IN ORDER):

---

### Operation: status (default when no args)

**Step 1**: Check current branch
Run: !`git branch --show-current`

**Step 2**: Check for uncommitted changes
Run: !`git status --short`

**Step 3**: Check if branch has upstream
Run: !`git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "No upstream"`

**Step 4**: Check commits ahead/behind
Run: !`git rev-list --left-right --count HEAD...@{u} 2>/dev/null || echo "0 0"`

**Step 5**: Show current issue context
- If branch matches pattern `[0-9]+-.*`, extract issue number
- Show: "Working on issue #[number]"

**Step 6**: Check for recent stable states
Run: !`git tag -l "*-stable" --sort=-version:refname | head -3`
Show: "Recent stable tags: [list]"

**Step 7**: Display summary
Show:
- Current branch
- Files changed (grouped by type)
- Commits ahead/behind
- Issue context if found
- Last commit message
- Recent stable states if any

---

### Operation: commit

**Step 1**: Check for changes
Run: !`git status --porcelain`
If empty, say "Nothing to commit" and STOP

**Step 2**: Stage all changes
Run: !`git add -A`

**Step 3**: Analyze changes to generate message
Run: !`git diff --cached --stat`

**Step 4**: Generate commit message
Based on the changes:
- If mostly docs: "docs: [description]"
- If new feature: "feat: [description]"
- If bug fix: "fix: [description]"
- If refactor: "refactor: [description]"
- If tests: "test: [description]"

**Step 5**: Check for issue reference
- Get branch name
- If it contains issue number, add "Related to #[number]" to message

**Step 6**: Create commit
Run: !`git commit -m "[generated message]"`

**Step 7**: Show what was committed
Run: !`git log -1 --oneline`

---

### Operation: push

**Step 1**: Check if there are commits to push
Run: !`git log @{u}.. --oneline 2>/dev/null | wc -l`
If 0, say "Nothing to push" and STOP

**Step 2**: Run tests if test command exists
Run: !`npm test 2>/dev/null || echo "No tests configured"`

**Step 3**: Push with lease
Run: !`git push --force-with-lease`

**Step 4**: Show push result
Say: "Pushed [number] commits to [branch]"

**Step 5**: If PR exists, show URL
Run: !`gh pr view --json url -q .url 2>/dev/null || echo "No PR yet"`

---

### Operation: sync

**Step 1**: Stash any changes
Run: !`git stash push -m "sync-stash-$(date +%s)"`

**Step 2**: Fetch latest
Run: !`git fetch origin`

**Step 3**: Pull with rebase
Run: !`git pull --rebase origin main`

**Step 4**: Reapply stash if any
Run: !`git stash pop 2>/dev/null || echo "No stash to apply"`

**Step 5**: Push if ahead
Run: !`git push --force-with-lease 2>/dev/null || echo "Nothing to push"`

---

### Operation: pr

**Step 1**: Check for uncommitted changes
Run: !`git status --porcelain`
If not empty, say "Commit changes first" and STOP

**Step 2**: Push current branch
Run: !`git push -u origin HEAD`

**Step 3**: Get branch and issue info
- Extract issue number from branch name if present
- Get recent commits for PR body

**Step 4**: Generate PR title
- Use branch name to create readable title
- If issue number found: "[#number] Title"

**Step 5**: Generate PR body
Include:
- Summary of changes (from commits)
- If issue found: "Closes #[number]"
- List of commits

**Step 6**: Create PR
Run: !`gh pr create --title "[title]" --body "[body]"`

**Step 7**: Show PR URL
Display the created PR URL

---

### Operation: stash

**Step 1**: Check for changes
Run: !`git status --porcelain`
If empty, say "Nothing to stash" and STOP

**Step 2**: Create descriptive stash
Run: !`git stash push -m "WIP: $(date +%Y%m%d-%H%M%S)"`

**Step 3**: Show stash created
Say: "Changes stashed. Use 'git stash pop' to restore"

---

### Operation: log

**Step 1**: Show recent commits with graph and tags
Run: !`git log --oneline --graph --decorate -10`

**Step 2**: Highlight stable commits
Run: !`git log --oneline --grep="\[STABLE\]" -5 2>/dev/null || echo "No commits marked [STABLE]"`

**Step 3**: Show commit stats
Run: !`git log --stat -3`

---

### Operation: stable

**Step 1**: List all stable tags
Run: !`git tag -l "*-stable" --sort=-version:refname`

**Step 2**: List all working tags  
Run: !`git tag -l "*-working" --sort=-version:refname`

**Step 3**: Show commits marked [STABLE]
Run: !`git log --oneline --grep="\[STABLE\]" -10`

**Step 4**: Display summary
Show:
- Stable tags with dates
- Working tags with dates
- Commits marked as stable
- Current HEAD position relative to stable states

---

### Operation: rollback

**Step 1**: Show recent stable states
Run: !`git tag -l "*-stable" "*-working" --sort=-version:refname | head -5`

**Step 2**: Show current position
Run: !`git log -1 --oneline`

**Step 3**: Ask user which state to rollback to
Display options:
1. Latest stable tag
2. Latest working tag
3. Specific commit hash
4. Cancel

**Step 4**: If user confirms, perform rollback
WARNING: This will reset --hard, losing uncommitted changes
Run: !`git reset --hard [selected-ref]`

---

### Operation: tags

**Step 1**: List all version tags
Run: !`git tag -l "v*" --sort=-version:refname`

**Step 2**: List all stable/working tags
Run: !`git tag -l "*-stable" "*-working" --sort=-version:refname`

**Step 3**: Show what each tag points to
Run: !`git show-ref --tags | tail -10`

---

### Operation: commit with stable flag

When user runs `/git commit stable`:

**Step 1-6**: Same as regular commit

**Step 7**: Add [STABLE] marker to commit message
Prepend "[STABLE] " to the generated message

**Step 8**: Create stable tag
Run: !`git tag -a "stable-$(date +%Y%m%d-%H%M%S)" -m "Stable state: [description]"`

**Step 9**: Push tag to remote
Run: !`git push origin --tags`

---

## Work Journal Integration

After each operation, update `.claude/work-journal.json`:
- Track what operations were performed
- Save commit messages created
- Note issue context
- Record decisions made

## Important Rules

1. **NO AUTOMATIC COMMITS** - User must explicitly run /git commit
2. **ALWAYS CHECK STATE FIRST** - Don't assume, verify
3. **CLEAR FEEDBACK** - Tell user exactly what happened
4. **SAFETY FIRST** - Use --force-with-lease, not --force
5. **CONTEXT AWARE** - Use issue numbers, branch names

## Error Handling

If any git command fails:
1. Show the exact error
2. Suggest how to fix it
3. DON'T try to fix automatically
4. Let user decide next steps