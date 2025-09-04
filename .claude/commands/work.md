---
allowed-tools: Task(*), mcp__github(*), Bash(*), Read(*), Write(*), Edit(*), TodoWrite(*)
description: Intelligently selects and implements work based on sprint priorities and dependencies
argument-hint: [#issue-number] [--deploy] [--test]
---

# Work - Intelligent Implementation Command

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

### Step 1: Determine Work Mode

Parse `$ARGUMENTS` to determine action:
- If `#123` provided → work on that specific issue
- If `--deploy` → deploy current branch to Vercel
- If `--test` → run test suite
- If no arguments → intelligently select next work item

### Step 2: Intelligent Work Selection (when no issue specified)

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

### Step 3: Verify Selection Is Valid

Before starting work, use mcp__github__get_issue to verify:
- No "blocked" label
- All dependencies (if any) are closed
- Not already assigned to someone else

### Step 4: Get Complete Issue Context

Use mcp__github__get_issue to retrieve:
- Title and full description
- All labels (type, priority, size, complexity)
- Current state and assignees
- Implementation checklist from body
- Comments for additional context

### Step 5: Create GitHub-Linked Branch

**CRITICAL: Use gh issue develop to create branch on GitHub first:**
!`gh issue develop $ISSUE_NUMBER --checkout`

This command:
- Creates the branch ON GitHub first (properly linked to issue)
- Checks it out locally
- Shows up in the issue's Development section
- Ensures proper GitHub tracking

Get the created branch name:
!`git branch --show-current`

**Important:** The branch name will be something like `123-feature-description` based on the issue.

### Step 6: Optional Worktree Support (if parallel work needed)

**Only if user needs to work on multiple issues simultaneously:**

Check if worktrees are needed:
- Check existing worktrees: !`git worktree list`
- If already working on another issue, offer worktree option

**If parallel work is needed:**
Ask user: "You're working on issue #[OTHER_ISSUE]. Would you like to:
1. Create a worktree for issue #[ISSUE_NUMBER] (work on both)
2. Switch branches (pause current work)
3. Cancel

Choose (1/2/3):"

**If user chooses worktree (option 1):**
- Get current branch: !`git branch --show-current`
- Create worktree path: `../worktrees/issue-$ISSUE_NUMBER`
- Create worktree: !`git worktree add "$WORKTREE_PATH" "$BRANCH_NAME"`
- Inform user: "Created worktree at $WORKTREE_PATH"
- Instruct: "Run: cd $WORKTREE_PATH to continue work there"

**Note:** Worktrees are secondary - branch creation via `gh issue develop` is primary!

### Step 7: Configure Git for Issue Tracking (NEW)

**CRITICAL: Set up automatic issue references in commits**

Set up git commit template for this branch:
- Extract issue number: !`echo $BRANCH_NAME | grep -oP '^\d+'`
- Create template: !`echo -e "\n\nRelated to #$ISSUE_NUMBER" > .gitmessage`
- Set template: !`git config commit.template .gitmessage`

Remind user that ALL commits must reference the issue for GitHub timeline tracking.

### Step 8: Implementation Routing

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

### Step 9: Update Issue Status

Use mcp__github APIs:
1. Add "status:in-progress" label: `mcp__github__update_issue`
2. Add starting work comment: `mcp__github__add_issue_comment`

### Step 10: Work Through Issue Checkboxes - BATCH SYNC APPROACH

**CRITICAL: Work locally with TodoWrite, then batch sync to GitHub when complete**

#### A. Parse Issue Checkboxes to TodoWrite
Use mcp__github__get_issue to get the full issue body, then extract checkboxes:
- Find all `- [ ]` (unchecked) and `- [x]` (checked) patterns  
- Create TodoWrite list with items like: "CHECKBOX 1: Add user authentication endpoints"
- Track checkbox text exactly as it appears in GitHub
- Work entirely in TodoWrite (fast, no API calls during work)

#### B. Systematic Local Execution
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

#### D. Efficient Batch Approach Benefits
- **No API rate limiting** - Single update instead of multiple
- **Atomic update** - All checkboxes change together  
- **Fast local work** - TodoWrite operations are instant
- **Clear completion signal** - One comment when everything is done
- **Reliable sync** - Direct mapping between TodoWrite and GitHub checkboxes

**DO NOT manually create a PR - automation will handle it when ALL checkboxes are complete**

### Step 11: Ensure All Commits Reference the Issue

**For EVERY commit made during work:**

Example commit formats:
- Feature: `feat: Add new feature\n\nRelated to #$ISSUE_NUMBER`
- Bug fix: `fix: Update validation logic #$ISSUE_NUMBER`  
- Documentation: `docs: Update README\n\nPart of #$ISSUE_NUMBER`

**NEVER use "Closes #XX" except in the final PR description**

### Step 12: Run Tests and Validation

Before marking work complete:
!`npm test` or !`pytest` depending on project
!`npm run lint` or appropriate linter
!`npm run typecheck` if TypeScript project

### Step 13: Let Automation Create the PR

**When all checkboxes are complete:**
1. Push your branch: !`git push -u origin $BRANCH_NAME`
2. The automation workflow will detect completed checkboxes
3. It will automatically create the PR with proper "Closes #XX" link
4. PR will transition from draft to ready automatically

**DO NOT manually create PRs with gh pr create**

### Step 14: Clean Up After Merge

When PR is merged (by automation or manually):
1. Checkout main: !`git checkout main`
2. Pull latest: !`git pull origin main`
3. Delete local branch: !`git branch -d $BRANCH_NAME`
4. If using worktree, remove it: !`git worktree remove ../worktrees/issue-$ISSUE_NUMBER-*`

### Step 15: Update Dependencies

Check if this unblocks other issues:
- Use mcp__github__list_issues with label "blocked"
- For each, check if it depended on the completed issue
- Remove "blocked" label if unblocked using mcp__github__update_issue

## Special Actions

### Deploy (--deploy)
!`vercel --prod`

### Test (--test)
!`npm test` or !`pytest` or appropriate test command

## Examples

**Examples:**

- Intelligent auto-selection: `/work` → Finds issue #35 that unblocks 3 others
- Work on specific issue: `/work #42`
- Deploy current work: `/work --deploy` 
- Run tests: `/work --test`

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