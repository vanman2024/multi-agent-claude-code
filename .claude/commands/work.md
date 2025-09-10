---
allowed-tools: Task(*), mcp__github(*), Bash(*), Read(*), Write(*), Edit(*), TodoWrite(*)
description: Intelligently selects and implements work based on sprint priorities and dependencies
argument-hint: [#issue-number | branch-name | commit-sha] | --worktree | --status | --resume | --deploy | --continue | --from-commit
---

# Work - Intelligent Implementation Command

<!--
WHEN TO USE THIS COMMAND:
- Starting work on a specific issue (#123)
- Auto-selecting next priority task (just /work)
- Creating formal branches with PRs linked to issues
- When you need the full issue→PR→merge workflow

WHEN NOT TO USE:
- Exploratory work (use /wip instead)
- Quick fixes without issues (use /wip instead)
- You're not ready to commit to an issue

KEY DIFFERENCES FROM /wip:
- /work creates branches FROM issues with full tracking
- /wip creates branches WITHOUT issues for exploration
- /work auto-links PRs to issues
- /wip is for "figure it out as you go" work

EXAMPLES:
/work #123              - Work on specific issue (must be on main)
/work #123 --worktree   - Work on issue in isolated worktree (from any branch)
/work                   - Auto-pick next priority
/work feature-branch    - Continue work on existing branch
/work abc123def         - Continue from specific commit
/work --continue        - Resume from last commit on current branch
/work --status          - See all active work
/work --copilot-first   - Try Copilot, fallback to Claude
-->

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
  --worktree                   Create isolated worktree for this work
  --status                     Show triage view of all active work
  --resume                     Auto-resume most recent incomplete work
  --deploy                     Deploy current branch to production
  --discussion <num>           Create issue from discussion #num
  
COPILOT INTEGRATION:
  --copilot-first             Try Copilot first, Claude as backup
  --copilot-review            Get Copilot's code review  
  --copilot-only              Only assign to Copilot (no Claude)
  --no-copilot                Bypass Copilot, use Claude directly
  --parallel                  Work with Copilot simultaneously
  
EXAMPLES:
  /work                        Smart selection from sprint
  /work #142                   Work on issue #142 (must be on main)
  /work #142 --worktree       Work on #142 in isolated worktree
  /work --status              See all active work
  /work --resume              Continue where you left off
  /work --discussion 125      Convert discussion to issue
  /work #150 --copilot-first  Try Copilot, Claude as backup
  
For detailed flag documentation, see: FLAGS.md
```

## Context
The command should check:
- Current branch using git commands
- Sprint issues using GitHub CLI 
- Blocked issues using GitHub API
- In progress issues using GitHub API

## <worktree_branch_check>
**CRITICAL: Branch/Worktree Decision Logic**

Before proceeding with any work:
1. Check if $ARGUMENTS contains --worktree flag
2. Get current branch: git branch --show-current
3. Apply these rules:

**IF --worktree flag is present:**
- Can be on ANY branch (doesn't matter where you are)
- Will create NEW branch from origin/main in isolated worktree
- The new branch is always based on latest main, NOT current branch
- Continue with worktree creation workflow (Step 0.5)

**IF NO --worktree flag (normal workflow):**
- **MUST be on main branch**
- Will create feature branch from current position
- If NOT on main: 
  - STOP IMMEDIATELY
  - Display error: "❌ Must be on main branch to start work"
  - Show current branch: "[current_branch_name]"
  - Provide options:
    ```
    Option 1: Switch to main
    git checkout main && git pull origin main
    /work #[issue]
    
    Option 2: Use worktree (work from any branch)
    /work #[issue] --worktree
    ```
  - EXIT - do not proceed past this point

**Summary:**
- Normal workflow: Must be on main, branches from current position
- Worktree workflow: Can be anywhere, always branches from origin/main
</worktree_branch_check>

## Your Task

When user runs `/work $ARGUMENTS`, intelligently select and implement work.

### Argument Processing

Parse the provided arguments to extract:
- Issue numbers (extract digits, can have # prefix)
- Flags like --deploy, --status, --resume, etc.
- Store issue number in ISSUE_NUM variable if found

### Step 0: 🔴 ENFORCE WORKFLOW - Check Branch/Worktree Requirements

**CRITICAL: Apply the <worktree_branch_check> logic FIRST**

1. Check if --worktree flag is in $ARGUMENTS
2. Get current branch: git branch --show-current
3. Follow <worktree_branch_check> rules:
   - If --worktree: proceed with worktree creation (skip to Step 0.5)
   - If NOT on main AND no --worktree: STOP with error message
   - If on main: continue to sync check

**If on main (normal workflow):**
- Fetch and compare with: git fetch origin main
- If behind, auto-pull with: git pull origin main

### Step 0.5: Worktree Creation (if --worktree flag)

**IMPORTANT**: Worktree operations DO NOT affect the current directory/branch!
- The current directory stays on whatever branch it's on
- Worktree creates a SEPARATE directory with its own branch
- No disruption to any work happening in current location

If --worktree flag is present:
1. Get issue details and determine expected branch name (e.g., 123-feature-name)
2. Check current branch: git branch --show-current (just for decision logic)
3. **Decision point:**
   
   **CASE A: Already on the target branch**
   - If current branch matches expected branch for this issue:
   - ASK: "You're already on branch [branch-name] for issue #123. Options:"
     ```
     1. Continue working here (no worktree needed)
     2. Create separate worktree instance (for parallel work)
     3. Cancel
     ```
   - If option 1: Skip worktree, continue normal workflow
   - If option 2: Create worktree with suffix (e.g., 123-feature-name-wt2)
   
   **CASE B: Branch exists but we're not on it**
   - Check if branch exists: git branch -r | grep [branch-name]
   - If exists, ASK: "Branch [branch-name] already exists. Options:"
     ```
     1. Create worktree using existing branch
     2. Create new branch with suffix (123-feature-name-v2)
     3. Cancel
     ```
   
   **CASE C: Branch doesn't exist (normal case)**
   - Fetch latest: git fetch origin main
   - Create worktree path: ../worktree-issue-[number]
   - Create worktree FROM origin/main WITHOUT switching current directory:
     ```
     git worktree add [path] -b [issue-branch-name] origin/main
     ```
     This creates the worktree in a SEPARATE directory without affecting current work
   
4. Switch to worktree directory: cd [path]
5. Continue with normal workflow from there

**DO NOT PROCEED if not on main with latest changes!**

### Step 1: Parse Arguments and Determine Work Mode

Parse `$ARGUMENTS` to extract any flags and issue numbers. Look for:
- `--deploy` flag for deployment
- `--discussion` flag followed by a discussion number
- `--resume` flag to resume recent work
- `--status` flag to show work triage
- Issue numbers (with or without # prefix)

**Extract issue number from arguments:**
Use command substitution to extract issue numbers from the arguments.

If arguments contain an issue number, extract and store it for use.

Store these variables for later use:
- `ISSUE_NUM` - Issue number to work on (if provided)
- Flags can be checked with `echo "$ARGUMENTS" | grep -q -- "--flag-name"`

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

Check for existing worktree using git worktree list to look for branches matching the issue number.

**If worktree exists for the issue:**
- Parse the worktree path from the output
- Display: "Found existing worktree for issue #$ISSUE_NUM at: [path]"
- Ask: "Do you want to continue working in the existing worktree? (y/n)"
- If yes: Instruct user to `cd [worktree_path]` and work there
- If no: Ask if they want to remove it and start fresh

**If no worktree but branch exists:**
- Check for existing branches matching the issue number
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

Use mcp__github APIs to retrieve complete context:

**Get issue details:**
Use mcp__github__get_issue with owner/repo/issue_number to get:
- Title and full description
- All labels (type, priority, size, complexity)
- Current state and assignees  
- Implementation checklist from body

**Get issue comments for additional context:**
Use mcp__github__get_issue_comments with owner/repo/issue_number to get:
- All comments from team members
- Additional requirements or clarifications
- Design decisions and context
- Links to related issues or PRs

**Extract inline quotes and code blocks:**
Parse the issue body and comments for:
- Quoted text blocks (lines starting with `>`) - Often contain important context
- Code blocks (```) - May contain examples or implementation hints
- Inline code (`backticks`) - Specific function/variable names to use
- Blockquotes with citations - References to documentation or specs

**Parse all context together:**
- Combine issue body + all comments for full understanding
- Look for updates to requirements in comments
- Check for any design decisions or constraints mentioned
- Note any related work or dependencies mentioned in comments
- **IMPORTANT: Pay special attention to quoted sections** - They often contain:
  - User feedback that needs addressing
  - Error messages to fix
  - Specific requirements from stakeholders
  - Examples of expected behavior

### Step 9: Create GitHub-Linked Branch (If No Worktree Exists)

**CRITICAL: Only create branch if no worktree exists!**

If no existing worktree was found in Step 4:

Use the GitHub CLI command: gh issue develop $ISSUE_NUM --checkout

This command:
- Creates the branch ON GitHub first (properly linked to issue)
- Checks it out locally
- Shows up in the issue's Development section
- Ensures proper GitHub tracking

Get the created branch name using: git branch --show-current

**Important:** The branch name will be something like `123-feature-description` based on the issue.

**Note:** Draft PR will be created after your first meaningful commit (see Step 14a)

### Step 10: Optional Additional Worktree (if parallel work needed)

**Only if user needs to work on multiple issues simultaneously:**

Check if worktrees are needed:
- Check existing worktrees using: git worktree list
- If already working on another issue, offer worktree option

**If parallel work is needed:**
Ask user: "You're working on issue #[OTHER_ISSUE]. Would you like to:
1. Create a worktree for issue #[ISSUE_NUMBER] (work on both)
2. Switch branches (pause current work)
3. Cancel

Choose (1/2/3):"

**If user chooses worktree (option 1):**
- Get current branch using: git branch --show-current
- Create worktree path: ../worktrees/issue-$ISSUE_NUM
- Create worktree using: git worktree add [path] [branch]
- Inform user: "Created worktree at [path]"
- Instruct: "Run: cd [path] to continue work there"

**Note:** Worktrees are secondary - branch creation via `gh issue develop` is primary!

### Step 11: Configure Git for Issue Tracking

**CRITICAL: Set up automatic issue references in commits**

Set up git commit template for this branch:
- Extract issue number from branch name
- Create template file with issue reference
- Configure git to use the template

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

1. Push the branch with first commit using: git push -u origin [branch-name]

2. Create draft PR to trigger automation:
   - Get issue title using GitHub CLI
   - Create draft PR with appropriate title and body linking to the issue

**Closes #$ISSUE_NUM**

This draft PR tracks work progress and triggers automation.

### Implementation Progress:
Work in progress - checkboxes will be validated by automation

### Status:
- [ ] Implementation in progress
- [ ] Tests added/passing
- [ ] Linting passing
- [ ] Ready for review" --draft --base main`

3. Get PR number for reference using GitHub CLI to list PRs for the branch

This draft PR:
- Triggers checkbox validation on real code
- Enables preview deployments
- Shows progress in GitHub UI
- Can be abandoned if needed
- Converts to ready when complete

#### 14b. Parse Issue Checkboxes to TodoWrite
Use mcp__github__get_issue to get the full issue body, then extract checkboxes:
- Find all `- [ ]` (unchecked) and `- [x]` (checked) patterns  
- Create TodoWrite list with items like: "CHECKBOX 1: Add user authentication endpoints"
- Track checkbox text exactly as it appears in GitHub
- Work entirely in TodoWrite (fast, no API calls during work)

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

Before marking work complete, check what's available and run if exists:

**Check for Node.js project:**
- Check if package.json exists
- If Node project, run available scripts:
  - Test script if available: npm test
  - Lint script if available: npm run lint
  - TypeCheck script if available: npm run typecheck

**Check for Python project:**
- Check for pytest availability and run if found
- Check for flake8 availability and run if found

**If no testing infrastructure exists:**
- Note: "No test infrastructure detected - proceeding without tests"
- This is common for template repositories or new projects

### Step 17: Convert Draft PR to Ready

**When all checkboxes are complete and tests pass:**

1. Push final changes using: git push
2. Convert draft to ready using: gh pr ready [PR_NUMBER]
3. The PR is now ready for review/merge
4. Automation may auto-merge if all checks pass

**The draft PR was already created in Step 14a**

### Step 18: Clean Up After Merge

When PR is merged (by automation or manually):
1. Checkout main using: git checkout main
2. Pull latest using: git pull origin main
3. Delete local branch using: git branch -d [branch_name]
4. If using worktree, remove it using: git worktree remove [worktree_path]

### Step 19: Update Dependencies

Check if this unblocks other issues:
- Use mcp__github__list_issues with label "blocked"
- For each, check if it depended on the completed issue
- Remove "blocked" label if unblocked using mcp__github__update_issue

## Special Actions

### Deploy (--deploy)
Use vercel --prod to deploy to production

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
5. **Template Compliance** - Uses exclamation syntax, no bash code blocks
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