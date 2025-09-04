# User Test Story: /work Command Verification

## Overview
This document provides a step-by-step user test to verify that the `/work` command fixes are functioning correctly, addressing all the critical issues identified in #126.

---

## Test Scenarios

### Scenario 1: Starting Work from Wrong Branch
**Given:** User is on branch `134-feature-unified-testing-strategy`  
**When:** User runs `/work #150`  
**Then:** 
- ❌ Command should STOP immediately
- Show error: "You must be on main branch to start work!"
- Instruct user to: `git checkout main && git pull origin main`
- Should NOT proceed with any work

**Verification Steps:**
```bash
git checkout 134-feature-unified-testing-strategy
/work #150
# Expect: Error message and stop
```

---

### Scenario 2: Auto-Pull Latest Changes
**Given:** User is on main branch but behind origin/main  
**When:** User runs `/work #151`  
**Then:**
- Detect main is behind
- Show: "🔄 Auto-pulling latest changes..."
- Execute `git pull origin main`
- Continue with work selection

**Verification Steps:**
```bash
git checkout main
git reset --hard HEAD~2  # Simulate being behind
/work #151
# Expect: Auto-pull then proceed
```

---

### Scenario 3: Worktree Creation Prompt
**Given:** User is on a feature branch when trying to work on different issue  
**When:** User runs `/work #152`  
**Then:** Should see prompt:
```
You're currently on branch [feature-x]. Would you like to:
1. Create a worktree for issue #152 (recommended for parallel work)
2. Switch to main and work normally (will lose current branch context)
3. Cancel and continue working on current branch

Choose (1/2/3):
```

**Verification:**
- Option 1 → Creates worktree at `../worktrees/issue-152-*`
- Option 2 → Switches to main
- Option 3 → Cancels operation

---

### Scenario 4: Issue Reference in Commits
**Given:** User is working on issue #126  
**When:** Claude makes ANY commit  
**Then:**
- Git commit template should be configured
- ALL commits must include "Related to #126" or "#126"
- Should see reminder about issue references

**Verification Steps:**
```bash
# After /work starts on issue
cat .gitmessage  # Should show template with issue reference
git log --oneline -5  # All commits should show #126
```

**Expected Commit Format:**
```
feat: Add new feature

Related to #126
```

---

### Scenario 5: No Manual PR Creation
**Given:** User completes work on issue #126  
**When:** All checkboxes are checked in the issue  
**Then:**
- Should NOT see any `gh pr create` commands
- Should see: "Push your branch and let automation create PR"
- Automation workflow should trigger PR creation

**Verification:**
- Check that `/work` command has NO `gh pr create` commands
- Verify automation workflow exists for PR creation
- Confirm PR is created ONLY after checkboxes complete

---

### Scenario 6: Intelligent Issue Selection
**Given:** User runs `/work` with no arguments  
**When:** Multiple issues exist in sprint  
**Then:** Should prioritize in this order:
1. Issues that unblock other work
2. High priority (P0, P1, P2) unblocked issues
3. Small quick wins (size:XS)
4. Continue in-progress work
5. Next in sprint sequence

**Verification Steps:**
```bash
/work
# Should see analysis of available issues
# Should explain WHY it selected the specific issue
```

---

### Scenario 7: Checkbox-First Workflow
**Given:** User is working on issue with checkboxes  
**When:** Implementing the solution  
**Then:**
- Should work through checkboxes systematically
- Update issue with progress
- Use TodoWrite to track locally
- NO PR until checkboxes complete

**Verification:**
- Issue body has checkboxes
- Work progresses through them
- No premature PR creation

---

### Scenario 8: Template Compliance
**Given:** Reading the `/work` command file  
**When:** Reviewing the implementation  
**Then:**
- NO bash code blocks (no ```bash sections)
- Uses `!` syntax for inline commands
- Uses MCP functions like `mcp__github__get_issue`
- Proper step-by-step descriptions

**Verification:**
```bash
cat .claude/commands/work.md | grep -c '```bash'  # Should be minimal
cat .claude/commands/work.md | grep -c '!\`'       # Should have many
```

---

## Complete Test Flow

### Setup
```bash
# 1. Ensure you're on main
git checkout main
git pull origin main

# 2. Create test issue
/create-issue
# Title: Test work command functionality
# Complexity: 2
# Size: S
```

### Test Execution
```bash
# 3. Try from wrong branch (should fail)
git checkout -b test-branch
/work #[TEST_ISSUE]
# Expect: Error about not being on main

# 4. Try from main (should work)
git checkout main
/work #[TEST_ISSUE]
# Expect: Branch creation, status updates

# 5. Check commit references
git log --oneline -1
# Expect: Contains #[TEST_ISSUE]

# 6. Verify no PR created
gh pr list --head $(git branch --show-current)
# Expect: No PR yet (until checkboxes done)
```

### Expected Timeline in Issue
After test, issue #[TEST_ISSUE] timeline should show:
- ✅ All commits with issue references
- ✅ Status label updates
- ✅ Branch creation noted
- ✅ Work progress comments

---

## Success Criteria

✅ **PASS** if:
1. Enforces main branch + latest changes
2. Prompts for worktree when needed
3. ALL commits reference the issue
4. No manual PR creation
5. Template format compliance (! syntax)
6. Checkbox-first workflow
7. Intelligent issue selection

❌ **FAIL** if:
1. Allows work from non-main branch without prompt
2. Creates PRs manually
3. Commits lack issue references
4. Uses bash code blocks
5. Skips checkbox workflow

---

## Notes for Testing

- Test both with and without arguments: `/work` vs `/work #123`
- Test with multiple active branches/worktrees
- Verify GitHub timeline shows all commits
- Check that automation handles PR lifecycle
- Ensure worktree cleanup happens after merge

---

## Regression Tests

After fixes, ensure these still work:
- `/work --deploy` - Deployment flag
- `/work --test` - Test execution
- Sprint issue filtering
- Dependency checking
- Priority-based selection