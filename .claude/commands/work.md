---
allowed-tools: Task(*), mcp__github(*), Bash(*), Read(*), Write(*), Edit(*), TodoWrite(*)
description: Intelligently selects and implements work based on sprint priorities and dependencies
argument-hint: [#issue-number] | --status | --resume | --deploy | --discussion #num | --copilot-first | --copilot-review | --copilot-only | --no-copilot | --parallel | --worktree
---

# Work - Intelligent Implementation Command

## Quick Help (if --help flag provided)

If user runs `/work --help`, display this and exit:

```
/work - Intelligent work implementation with context awareness

USAGE:
  /work [#issue-number]         Work on specific issue
  /work                         Auto-select next priority issue
  /work --status               Show all your active work
  /work --resume               Resume most recent work
  
FLAGS:
  --status                     Show triage view of all active work
  --resume                     Auto-resume most recent incomplete work
  --deploy                     Deploy current branch to production
  --discussion <num>           Create issue from discussion #num
  --parallel                   Create worktree for parallel work
  --worktree                   Force worktree creation (same as --parallel)
  
COPILOT INTEGRATION:
  --copilot-first             Try Copilot first, Claude as backup
  --copilot-review            Get Copilot's code review  
  --copilot-only              Only assign to Copilot (no Claude)
  --no-copilot                Bypass Copilot, use Claude directly
  
EXAMPLES:
  /work                        Smart selection from sprint
  /work #142                   Work on issue #142
  /work #143 --parallel        Work on #143 in parallel (worktree)
  /work --status              See all active work
  /work --resume              Continue where you left off
  /work --discussion 125      Convert discussion to issue
  /work #150 --copilot-first  Try Copilot, Claude as backup
  
For detailed flag documentation, see: FLAGS.md
```

## Context
- Current branch: !`git branch --show-current`
- Sprint issues: !`gh issue list --label "sprint:current" --state open --json number,title,labels`
- Blocked issues: !`gh issue list --label "blocked" --state open --json number,title`
- In progress: !`gh issue list --label "status:in-progress" --state open --json number,title,assignees`

## Your Task

When user runs `/work $ARGUMENTS`, intelligently select and implement work.

### Step 0: 🔴 ENFORCE WORKFLOW - MUST BE ON MAIN WITH LATEST

**CRITICAL: Before doing ANYTHING else, check branch and sync status:**

Use the Bash tool to verify you're on main with latest changes:
- Check current branch: !`git branch --show-current`
- If not on main, STOP and tell user to: `git checkout main && git pull origin main`
- Fetch and compare: !`git fetch origin main && git rev-parse main` vs !`git rev-parse origin/main`
- If behind, auto-pull: !`git pull origin main`

**DO NOT PROCEED if not on main with latest changes!**

### Step 0.5: 🔍 CHECK FOR EXISTING WORKTREES AND BRANCHES

**CRITICAL: Check for any existing work before creating new branches:**

Check for existing worktrees using: !`git worktree list`
- If any worktree exists that's not on main branch, show it to user
- Ask if they want to continue with that work or start new work
- If continuing existing work, tell them to cd into that worktree directory

Check for existing local branches using: !`git branch --list "[0-9]*-*"`
- Show any branches that start with issue numbers
- Check if branch exists locally that matches the issue they want to work on
- If branch already exists for this issue, switch to it instead of creating new

This prevents:
- Creating duplicate branches for same issue
- Losing work in existing worktrees
- Conflicting branch names
- Overwriting existing work

### Step 1: Parse Arguments and Determine Work Mode

Parse `$ARGUMENTS` to extract any flags and issue numbers. Look for:
- `--deploy` flag for deployment
- `--discussion` flag followed by a discussion number
- `--resume` flag to resume recent work
- `--status` flag to show work triage
- `--parallel` or `--worktree` flag to force worktree creation
- Issue numbers (with or without # prefix)

Store these in variables for later use, especially PARALLEL_FLAG.

**Determine Action Priority:**
- If `--status` flag → Show work triage view (see Step 1.5)
- If `--resume` flag → Resume most recent work (see Step 1.5)
- If issue number provided → Work on that specific issue
- If `--deploy` flag → Deploy current branch to Vercel
- If `--discussion` flag → Create issue from discussion (see Step 2)
- If no arguments → Check for incomplete work first (see Step 1.5)

### Step 1.5: Check for Incomplete Work & Handle Resume/Status

#### Handle --status Flag
**If the --status flag was provided:**

Display a comprehensive view of all active work:
1. Use git to find all branches starting with issue numbers
2. Sort them by most recent activity
3. For each branch, check if it has any WIP commits
4. Get the issue title from GitHub using the issue number
5. Display each issue with:
   - Issue number and title
   - Branch name and WIP indicator if present
   - Time since last activity
6. Also list any active worktrees

After showing the status, prompt the user to select which issue to resume or 'new' for fresh work.

#### Handle --resume Flag  
**If the --resume flag was provided:**

Automatically resume the most recent incomplete work:
1. Find the most recently modified branch that starts with an issue number
2. Extract the issue number from the branch name
3. Check if a worktree exists for this issue:
   - If yes: Tell the user to cd into that worktree directory
   - If no: Switch to that branch and sync with main
4. Check for any WIP commits and if found, soft reset them to keep changes staged
5. If no recent work is found, inform the user and suggest using /work without flags

Continue to Step 4 with the resumed issue number.

#### Auto-Detection (No Flags)
**If no flags were provided and no specific issue was specified:**

Check for incomplete work automatically:
1. Look for branches with recent activity (within last 7 days)
2. If found, show the issue number and how long ago it was worked on
3. Prompt the user: "Resume this work? (y/n)"
4. If yes: Set the issue number and continue to Step 4
5. If no or nothing found: Continue to Step 3 for fresh work selection

### Step 2: Handle Discussion-Linked Issue Creation

**If the --discussion flag was provided with a number:**

1. Use GitHub GraphQL API to fetch the discussion details (title, body, category, author)
2. Create a new issue with:
   - Title prefixed with "[FROM DISCUSSION #XX]"
   - Body containing link back to the original discussion
   - Original discussion content preserved
   - Standard implementation checklist added
3. Update the discussion status:
   - Remove `discussion:exploring` or `discussion:approved` labels if present
   - Add `discussion:in-progress` label to the discussion
   - Get discussion ID using GraphQL
   - Add comment with status update:
     ```
     📍 Status: In Progress
     🔗 Issue: #[created-issue-number]
     📅 Started: [current-date]
     ```
4. Capture the newly created issue number
5. Continue with the normal workflow using this issue number

### Step 3: Intelligent Work Selection (when no issue specified)

If no issue number was provided and no discussion referenced, select one:
- Check sprint, priorities, dependencies
- Select best issue to work on
- Set `ISSUE_NUM` to the selected issue number

### Step 4: Check for Existing Worktrees/Branches

**NOW check if a worktree or branch already exists for `ISSUE_NUM`:**

Check for existing worktree:
!`git worktree list | grep -E "issue-$ISSUE_NUM|$ISSUE_NUM-" | head -1`

**If worktree exists for the issue:**
- Parse the worktree path from the output
- Display: "Found existing worktree for issue #$ISSUE_NUM at: [path]"
- Ask: "Do you want to continue working in the existing worktree? (y/n)"
- If yes: Instruct user to `cd [worktree_path]` and work there
- If no: Ask if they want to remove it and start fresh

**If no worktree but branch exists:**
- Check: !`git branch -a | grep -E "$ISSUE_NUM-" | head -1`
- If branch exists locally: Switch to it
- If branch exists remotely: Check it out locally

### Step 5: Determine Final Work Mode

After handling worktrees/branches, determine final action:
- If `ISSUE_NUM` set → work on that specific issue
- If `DEPLOY_FLAG` → deploy current branch to Vercel
- Continue with issue implementation

### Step 6: Advanced Work Selection Details

#### Check Current Sprint
Use mcp__github__list_issues with label filter "sprint:current" to find sprint work.

#### Check Project Board Status
Use mcp__github__list_issues with label "status:in-progress" to check if work is already active.
If something is in progress, suggest continuing it rather than starting new work.

#### Analyze Dependencies and Blockers
For each potential issue:
1. Use mcp__github__get_issue to get full details
2. Check for "blocked" label
3. Parse body for "Depends on #XX" patterns
4. For each dependency, check if it's closed using mcp__github__get_issue
5. Prioritize issues that unblock the most other work

#### Priority Rules for Selection
1. **Unblocked work that unblocks others** - Issues that when completed, unblock other issues
2. **High priority unblocked issues** - Check for P0, P1, P2 labels
3. **Small quick wins** - Issues labeled "good first issue" or "size:XS"
4. **Continue in-progress work** - If user has work in progress, suggest continuing it
5. **Next in sprint sequence** - Follow logical order if issues are numbered sequentially

### Step 7: Verify Selection Is Valid

Before starting work, use mcp__github__get_issue to verify:
- No "blocked" label
- All dependencies (if any) are closed
- Not already assigned to someone else

### Step 8: Get Complete Issue Context

Use mcp__github__get_issue to retrieve:
- Title and full description
- All labels (type, priority, size, complexity)
- Current state and assignees
- Implementation checklist from body
- Comments for additional context

**IMMEDIATELY after getting issue: Create TodoWrite from checkboxes**
- Extract all `- [ ]` and `- [x]` items from Definition of Done
- Use TodoWrite tool to create todo list
- This MUST happen before proceeding to Step 9

### Step 9: Create Branch or Worktree Based on Context

**Decision logic for branch vs worktree:**

Check current work status:
- Check current branch: !`git branch --show-current`
- Check existing worktrees: !`git worktree list`

**Determine branch prefix based on issue type:**
- Get issue labels from Step 8
- Map label to prefix:
  - `feature` → `feature/`
  - `enhancement` → `enhancement/`
  - `bug` → `fix/` or `bugfix/`
  - `refactor` → `refactor/`
  - `chore` → `chore/`
  - `documentation` → `docs/`
  - Default → no prefix

**Create branch name with prefix:**
- Format: `[prefix]$ISSUE_NUM-brief-description`
- Example: `enhancement/141-add-type-flags`
- Example: `fix/142-login-error`
- Example: `feature/143-user-dashboard`

**If `--parallel` or `--worktree` flag was provided:**
- ALWAYS create a worktree regardless of current branch
- This explicitly enables parallel development

**If already on a non-main branch (working on another issue):**
- Ask user: "You're currently working on another issue. Would you like to:"
  - Option 1: Create worktree for parallel work (recommended)
  - Option 2: Switch branches (pause current work)
  - Option 3: Cancel
- If user chooses Option 1 or has --parallel flag, create worktree

**To create worktree for parallel work:**
1. Create branch with prefix: !`git checkout -b $BRANCH_NAME`
2. Link to issue: !`gh issue develop $ISSUE_NUM --name $BRANCH_NAME --checkout=false`
3. Create worktree: !`git worktree add ../worktree-$ISSUE_NUM $BRANCH_NAME`
4. Tell user:
   - "Created worktree at ../worktree-$ISSUE_NUM"
   - "cd ../worktree-$ISSUE_NUM to work on issue #$ISSUE_NUM"
   - "Your current work remains untouched here"

**If on main branch (not working on anything):**
- Create and checkout branch with prefix: !`git checkout -b $BRANCH_NAME`
- Link to issue for GitHub tracking
- No worktree needed unless --parallel flag was provided

### Step 10: Working Directory Instructions

**If worktree was created (parallel work):**
- Tell user: "Worktree created at ../worktree-$ISSUE_NUM"
- Instruct: "cd ../worktree-$ISSUE_NUM to work on issue #$ISSUE_NUM"
- Note: "You can switch between worktrees to work on multiple issues"

**If regular branch checkout (single work):**
- Continue in current directory
- Work proceeds normally on the checked-out branch

### Step 11: Configure Git for Issue Tracking

**CRITICAL: Set up automatic issue references in commits**

Set up git commit template for this branch:
- Extract issue number: !`echo $BRANCH_NAME | grep -oP '^\d+'`
- Create template: !`echo -e "\n\nRelated to #$ISSUE_NUM" > .gitmessage`
- Set template: !`git config commit.template .gitmessage`

Remind user that ALL commits must reference the issue for GitHub timeline tracking.

### Step 12: Implementation Routing

Based on issue labels (complexity and size):

#### For Simple Issues (Complexity 1-2, Size XS-S)
- Implement directly using Read/Write/Edit tools
- Follow the issue's implementation checklist
- Create straightforward solution

#### For Complex Issues (Complexity 3+, Size M+)
Use Task tool with appropriate agent:
- **Features/Bugs** → general-purpose agent
- **Refactoring** → code-refactorer agent  
- **Security** → security-auth-compliance agent
- **Integration** → integration-architect agent

### Step 13: Update Issue Status

Use mcp__github APIs:
1. Add "status:in-progress" label: `mcp__github__update_issue`
2. Add starting work comment with PR link: `mcp__github__add_issue_comment`
   - Include: "🚀 Started work in PR #[PR_NUMBER]"

### Step 14: Work Through Issue Checkboxes

#### 14a. Create Draft PR After First Commit

**After making your first meaningful commit:**

1. Push the branch with first commit:
   !`git push -u origin $BRANCH_NAME`

2. Create draft PR to trigger automation:
   ```bash
   # Get issue title first
   ISSUE_TITLE=$(gh issue view $ISSUE_NUM --json title --jq .title)
   
   gh pr create \
     --title "[DRAFT] Issue #$ISSUE_NUM: $ISSUE_TITLE" \
     --body "## Working on Issue #$ISSUE_NUM
   
   **Closes #$ISSUE_NUM**
   
   This draft PR tracks work progress and triggers automation.
   
   ### Implementation Progress:
   Work in progress - checkboxes will be validated by automation
   
   ### Status:
   - [ ] Implementation in progress
   - [ ] Tests added/passing
   - [ ] Linting passing
   - [ ] Ready for review" \
     --draft \
     --base main
   ```

3. Get PR number for reference:
   !`gh pr list --head $BRANCH_NAME --json number --jq .[0].number`

This draft PR:
- Triggers checkbox validation on real code
- Enables preview deployments
- Shows progress in GitHub UI
- Can be abandoned if needed
- Converts to ready when complete

#### 14b. Parse Issue Checkboxes to TodoWrite

**MANDATORY: Extract and create todos from issue checkboxes**

1. Use mcp__github__get_issue to get the issue body
2. Extract ALL checkboxes from "Definition of Done" section:
   - Find all `- [ ]` (unchecked) patterns
   - Find all `- [x]` (checked) patterns  
3. Use TodoWrite tool to create the list:
   - Each checkbox becomes a todo item
   - Format: "CHECKBOX N: [exact text from issue]"
   - Set status: "pending" for unchecked, "completed" for checked
4. This MUST happen before any implementation starts
5. All work tracking happens through TodoWrite (no API calls during work)

#### 14c. Systematic Local Execution
For each TodoWrite checkbox item:

1. **Mark TodoWrite as in_progress**
2. **Parse the checkbox text** to understand what needs to be done
3. **Determine implementation approach**:
   - Code changes → Use Read/Write/Edit tools
   - Testing → Run appropriate test commands  
   - Documentation → Update relevant files
   - Configuration → Modify config files
4. **Execute the checkbox task** using appropriate tools
5. **Mark TodoWrite as completed** (locally only)
6. **Make commits** with normal commit messages
7. **Continue to next TodoWrite item**

#### C. Batch Sync When All TodoWrite Complete
**ONLY when ALL TodoWrite items are marked completed:**

1. **Get current GitHub issue body** with mcp__github__get_issue
2. **For each completed TodoWrite checkbox:**
   - Find matching checkbox in issue body: `- [ ] [checkbox text]`
   - Replace with: `- [x] [checkbox text]`
3. **Update entire issue body at once** with mcp__github__update_issue  
4. **Add single completion comment** with mcp__github__add_issue_comment:
   ```
   ✅ **All checkboxes completed!**
   
   **Completed tasks:**
   - ✅ Add user authentication endpoints
   - ✅ Create login form component  
   - ✅ Add password validation
   - ✅ Write unit tests
   - ✅ Update documentation
   
   **Status:** Ready for PR creation via automation
   ```

#### 14d. Efficient Batch Approach Benefits
- **No API rate limiting** - Single update instead of multiple
- **Atomic update** - All checkboxes change together  
- **Fast local work** - TodoWrite operations are instant
- **Clear completion signal** - One comment when everything is done
- **Reliable sync** - Direct mapping between TodoWrite and GitHub checkboxes

**Draft PR was already created in Step 14a after first commit**

### Step 15: Ensure All Commits Reference the Issue

**For EVERY commit made during work:**

Example commit formats:
- Feature: `feat: Add new feature\n\nRelated to #$ISSUE_NUM`
- Bug fix: `fix: Update validation logic #$ISSUE_NUM`  
- Documentation: `docs: Update README\n\nPart of #$ISSUE_NUM`

**NEVER use "Closes #XX" except in the PR description (already added)**

### Step 16: Run Tests and Validation

Before marking work complete:
!`npm test` or !`pytest` depending on project
!`npm run lint` or appropriate linter
!`npm run typecheck` if TypeScript project

### Step 17: Convert Draft PR to Ready

**When all checkboxes are complete and tests pass:**

1. Push final changes: !`git push`
2. Convert draft to ready: !`gh pr ready $PR_NUMBER`
3. The PR is now ready for review/merge
4. Automation may auto-merge if all checks pass

**The draft PR was already created in Step 14a**

### Step 18: Clean Up After Merge

When PR is merged (by automation or manually):
1. Checkout main: !`git checkout main`
2. Pull latest: !`git pull origin main`
3. Delete local branch: !`git branch -d $BRANCH_NAME`
4. If using worktree, remove it: !`git worktree remove ../worktrees/issue-$ISSUE_NUM-*`

### Step 19: Update Dependencies

Check if this unblocks other issues:
- Use mcp__github__list_issues with label "blocked"
- For each, check if it depended on the completed issue
- Remove "blocked" label if unblocked using mcp__github__update_issue

## Special Actions

### Deploy (--deploy)
!`vercel --prod`

## Examples

**Examples:**

- Intelligent auto-selection: `/work` → Finds issue #35 that unblocks 3 others
- Work on specific issue: `/work #42`
- Create issue from discussion: `/work --discussion 125`
- Deploy current work: `/work --deploy`

## Real-Time Checkbox Implementation Example

**Issue #42 has checkboxes:**
```
- [ ] Add user authentication API endpoint
- [ ] Create login form component
- [ ] Add password validation
- [ ] Write unit tests
- [ ] Update documentation
```

**When `/work #42` runs:**

1. **Parse checkboxes**: Creates 5 TodoWrite items locally
   ```
   - CHECKBOX 1: Add user authentication API endpoint (pending)
   - CHECKBOX 2: Create login form component (pending)  
   - CHECKBOX 3: Add password validation (pending)
   - CHECKBOX 4: Write unit tests (pending)
   - CHECKBOX 5: Update documentation (pending)
   ```

2. **Work through TodoWrite locally** (fast, no GitHub API calls):
   - Mark item 1 in_progress → implement auth endpoint → mark completed
   - Commit: `"feat: Add user authentication API endpoint"`
   - Mark item 2 in_progress → implement login form → mark completed  
   - Commit: `"feat: Create login form component"`
   - Continue until all 5 TodoWrite items are completed

3. **Batch sync when ALL TodoWrite complete**:
   - Get GitHub issue body
   - Update all checkboxes at once: `- [ ]` → `- [x]` for all 5
   - Single GitHub update with mcp__github__update_issue
   - Add completion comment: "✅ All checkboxes completed!"

4. **Final result**: 
   - All GitHub checkboxes show `- [x]` simultaneously
   - One completion comment instead of 5 individual ones
   - Automation detects all checkboxes complete → creates PR

**Result**: Efficient batch update, no API rate limits, atomic checkbox completion

## Key Improvements in This Version

1. **Batch Checkbox Management** - Parses checkboxes, works locally, batch syncs to GitHub when complete
2. **Worktree Support** - Automatically creates worktrees for parallel development
3. **Issue Reference Enforcement** - Every commit references the issue for timeline tracking
4. **No Manual PR Creation** - Automation handles PR when checkboxes complete
5. **Template Compliance** - Uses `!` syntax, no bash code blocks
6. **MCP Function Usage** - Proper use of mcp__github functions instead of complex bash
7. **Checkbox-First Workflow** - Focus on issue completion, not PR management
8. **Batch GitHub Integration** - Single atomic update when all TodoWrite items complete

## Intelligence Summary

The `/work` command intelligently:
- ✅ Checks sprint and project board
- ✅ Analyzes dependencies and blockers
- ✅ Prioritizes work that unblocks other work
- ✅ Parses GitHub checkboxes into local TodoWrite items
- ✅ Executes checkbox work efficiently using local TodoWrite
- ✅ Batch syncs completed TodoWrite to GitHub when all tasks done
- ✅ Manages worktrees for parallel development
- ✅ Enforces issue references in all commits
- ✅ Updates issue status throughout
- ✅ Lets automation handle PR lifecycle
- ✅ Cleans up branches and worktrees after merge