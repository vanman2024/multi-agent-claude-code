---
allowed-tools: mcp__github(*), Read(*), Bash(*), TodoWrite(*)
description: Create GitHub issues with proper templates and automatic agent assignment
argument-hint: [--feature|--enhancement|--bug|--refactor|--chore|--docs|--quick|--hotfix] "title"
---

# Create Issue

## Context
- Current branch: !`git branch --show-current`
- Open issues: !`gh issue list --state open --limit 5 --json number,title,labels`
- Current sprint: !`gh issue list --label "sprint:current" --json number,title`

## Your Task

When user runs `/create-issue $ARGUMENTS`, follow these steps:

### Step 0: 🔴 ENFORCE WORKFLOW - MUST BE ON MAIN WITH LATEST

**CRITICAL: Before doing ANYTHING else, check branch and sync status:**

First check current branch with: !`git branch --show-current`

If not on main branch:
- Show error that user must be on main branch to create issues
- Tell user to run: git checkout main
- Tell user to run: git pull origin main
- Reference WORKFLOW.md for the required process
- STOP and do not proceed

If on main branch, check if up to date:
- Fetch latest with: !`git fetch origin main --quiet`
- Compare local and remote commits
- If behind remote, auto-pull with: !`git pull origin main`
- If pull fails, tell user to resolve conflicts and try again

Only proceed when on main branch with all latest changes.

**DO NOT PROCEED if not on main with latest changes!**

### Step 0.5: 🔍 CHECK FOR EXISTING WORKTREES

**CRITICAL: Check if already working on another issue in a worktree:**

Use bash to check for existing worktrees:
- Run `git worktree list` to see all active worktrees
- Check if any worktree is not on main branch
- If found, warn user they have active work in progress

If active worktree found on non-main branch:
- Show the worktree path and branch name
- Ask if they want to continue with new issue or finish existing work
- Suggest using `/work` to return to existing work
- Only proceed if user confirms they want to create new issue

This prevents:
- Creating overlapping work
- Forgetting about in-progress tasks
- Conflicting branches

### Step 1: Check for Existing Similar Issues

Before creating a new issue, check if similar work is already tracked:

Show all open issues with: !`gh issue list --state open --limit 20 --json number,title,labels | jq -r '.[] | "#\(.number): \(.title)"'`

Ask user to confirm if their issue is already covered by any existing issues.
If yes, suggest using `/work #[existing-issue]` instead.
If no, proceed to create a new issue.

### Step 1.5: Parse Flags and Auto-Detect Type

Parse `$ARGUMENTS` to extract any flags and determine the issue type:

Check if arguments start with a flag like `--feature`, `--enhancement`, `--bug`, etc.
Extract the flag and the title that follows it.

**Flag Mapping:**
- `--feature` → Use feature template, full workflow, branch prefix: `feature/`
- `--enhancement` → Use enhancement template, normal workflow, branch prefix: `enhancement/`
- `--bug` → Use bug template, normal workflow, branch prefix: `fix/`
- `--refactor` → Use task template, light workflow, branch prefix: `refactor/`
- `--chore` → Use task template, light workflow, branch prefix: `chore/`
- `--docs` → Use task template, minimal workflow, branch prefix: `docs/`
- `--quick` → Auto-detect type but use minimal workflow
- `--hotfix` → Use bug template, emergency workflow, branch prefix: `hotfix/`

**Auto-Detection (when no flag provided):**
If no flag is present, analyze the title for keywords:
- Words like "add", "create", "implement", "build", "new" → feature
- Words like "update", "improve", "enhance" → enhancement
- Words like "fix", "broken", "error", "fails", "bug", "crash" → bug
- Words like "refactor", "reorganize", "clean", "restructure" → refactor
- Words like "document", "readme", "docs", "comment" → documentation
- Words like "dependency", "config", "setup", "chore" → chore
- If no keywords match → default to task

Store the determined type, template path, and workflow mode for use in later steps.

**WORKFLOW ROUTING BASED ON FLAG:**

**If `--quick` flag:** 
- **JUMP TO MINIMAL WORKFLOW** (Step 5 directly)
- Skip templates, complexity assessment, milestones

**If `--hotfix` flag:**
- **JUMP TO EMERGENCY WORKFLOW** (Step 3 with bug template)
- Skip non-critical steps

**If `--docs` or `--chore` flag:**
- **USE LIGHT WORKFLOW** 
- Skip milestones and sprint assignment

**Otherwise continue with full workflow...**

### Step 2: Determine Issue Type (Conditional)

**Skip this step if type was already determined from flag or auto-detection in Step 1.5**

If no type was determined, ask the user:
```
What type of issue should this be?
- **feature**: New functionality
- **enhancement**: Improvement to existing functionality
- **bug**: Something is broken or not working
- **refactor**: Code cleanup without functional changes
- **chore**: Maintenance tasks
- **documentation**: Documentation updates
- **task**: Simple work item
```

### Step 2.5: Determine Complexity and Size (Conditional)

**BRANCH BASED ON WORKFLOW MODE:**

**If minimal/quick workflow**: 
- Auto-set complexity=1, size=XS
- **SKIP TO STEP 5** (bypass template loading)

**If emergency/hotfix workflow**: 
- Auto-set complexity=2, size=S
- **CONTINUE TO STEP 3** (use bug template)

**If light workflow (chore/docs)**: 
- Ask only for size
- Auto-set complexity=2
- **SKIP STEPS 9-11** (no milestones/sprints needed)

**If normal/full workflow**: Ask for both:
- **Complexity** (1-5): How complex is this?
  - 1: Trivial - Following exact patterns
  - 2: Simple - Minor variations
  - 3: Moderate - Multiple components
  - 4: Complex - Architectural decisions
  - 5: Very Complex - Novel solutions
- **Size** (XS/S/M/L/XL): How much work?
  - XS: < 1 hour
  - S: 1-4 hours
  - M: 1-2 days
  - L: 3-5 days
  - XL: > 1 week

### Step 3: Load Appropriate Template

Based on the determined type from Step 1.5 or Step 2, read the template:
- **feature** → Read templates/local_dev/feature-template.md
- **enhancement** → Read templates/local_dev/enhancement-template.md
- **bug** → Read templates/local_dev/bug-template.md
- **refactor** → Read templates/local_dev/task-template.md
- **chore** → Read templates/local_dev/task-template.md
- **documentation** → Read templates/local_dev/task-template.md
- **task** → Read templates/local_dev/task-template.md

**For minimal/quick workflow**: Skip template loading, create simple issue with just title and description
**For emergency/hotfix workflow**: Use bug template but skip non-essential sections

### Step 4: Fill Template

Using the template structure:
1. Replace placeholders with actual content
2. Keep all checkboxes unchecked `[ ]` (they represent work to be done)
3. Add metadata section at the bottom (EXACTLY as shown):
   ```markdown
   ---

   ## Metadata
   *For automation parsing - DO NOT REMOVE*

   **Priority**: P0/P1/P2/P3 (ask user)
   **Size**: XS/S/M/L/XL (from Step 1)
   **Points**: [1-13 based on size: XS=1-2, S=2-3, M=5, L=8, XL=13]
   **Goal**: Features/User Experience/Performance/Tech Debt/MVP (ask user)
   **Component**: Frontend/Backend/Database/Auth/Infra
   **Milestone**: (Optional - ask user or leave blank)
   ```
4. Include acceptance criteria
5. Add testing requirements section

### Step 5: Create GitHub Issue

**MINIMAL WORKFLOW (if --quick flag):**
- Create issue with just title and simple body
- Auto-assign to Copilot if possible
- Skip all remaining steps
- **END HERE**

**STANDARD WORKFLOW:**

Use mcp__github__create_issue with:
- owner: from repository context
- repo: from repository context
- title: provided by user
- body: filled template with metadata section + testing requirements
- labels: [issue-type] (ONLY the type: bug, feature, enhancement, refactor, task)

### Step 6: Check Dependencies

**NOTE: Branch creation happens when work starts (via `/work` command), not during issue creation**

After creating issue, check if it depends on other work:

Ask user if this issue depends on other issues.
If yes:
- Add dependency note to issue body using: !`gh issue edit $ISSUE_NUMBER --body-file updated-body.md`
- Add blocked label using: !`gh issue edit $ISSUE_NUMBER --add-label "blocked"`

### Step 8: Agent Assignment

**IMMEDIATE Copilot Auto-Assignment for Simple Tasks:**

Determine if Copilot should handle this task by checking:
- Complexity must be 2 or less (simple)
- Size must be XS or S (small)
- No blocking labels (security, architecture, blocked)

Auto-assign to Copilot only if ALL conditions are met:
- BOTH simple (complexity ≤ 2) AND small (size XS/S)
- AND no blocking labels present

If conditions are met for Copilot:
- Show message: "🤖 Auto-assigning to GitHub Copilot"
- Use mcp__github__assign_copilot_to_issue to assign Copilot
- Determine task type based on title and issue type:
  - If title includes "test" → "write unit tests"
  - If issue type is "bug" → "fix bug"
  - If title includes "document" or "readme" → "update documentation"
  - If issue type is "refactor" → "refactor code"
  - Otherwise → "implement feature"
- Add comment to issue with Copilot instructions using mcp__github__add_issue_comment
- Set assignment to "copilot"

If conditions NOT met (complex OR large OR has blocking labels):
- Show message: "📋 Requires Claude Code"
- Determine reason (high complexity, large size, or blocking labels)
- Add comment explaining why Claude Code is needed using mcp__github__add_issue_comment
- Include instruction to run `/work #[ISSUE_NUMBER]` when ready
- Set assignment to "claude-code"

**Task Instructions for Copilot Comments:**

For "write unit tests":
- Write comprehensive unit tests
- Aim for 80%+ code coverage
- Include edge cases and error scenarios
- Follow existing test patterns in the codebase
- Mock external dependencies

For "fix bug":
- Fix the bug as described in the issue
- Add regression tests to prevent recurrence
- Verify fix doesn't break existing functionality
- Update any affected documentation

For "update documentation":
- Update documentation as requested
- Keep consistent with existing style
- Include code examples where relevant
- Check for broken links

For "refactor code":
- Refactor without changing functionality
- Ensure all tests still pass
- Follow project coding standards
- Update imports and exports as needed

For default/feature implementation:
- Implement as specified in issue description
- Write tests for new functionality
- Follow existing project patterns
- Add appropriate error handling

### Step 9: Milestone Assignment (Optional)

Ask user if they want to assign a milestone:

List available milestones with: !`gh api repos/vanman2024/multi-agent-claude-code/milestones --jq '.[] | "\(.number): \(.title)"'`

Ask user to select milestone number (or skip).

If milestone selected:
- Get milestone title for confirmation
- Assign to issue using: !`gh issue edit $ISSUE_NUMBER --milestone $MILESTONE_NUMBER`

If no milestone selected:
- Note that it can be set manually later

### Step 10: Sprint Assignment (Optional)

Ask if this should be added to current sprint:

If yes:
- Add sprint label using: !`gh issue edit $ISSUE_NUMBER --add-label "sprint:current"`
- Check sprint capacity with: !`gh issue list --label "sprint:current" --json number | jq length`
- Warn if sprint has more than 10 issues

### Step 11: Priority Setting

Ask for priority (P0/P1/P2/P3) and add it to the metadata section in issue body.
DO NOT add priority as a label - it's tracked in the metadata and project board fields.

### Step 12: Summary

Provide the user with:

Get the issue URL using: !`gh issue view $ISSUE_NUMBER --json url --jq .url`

Show summary:
- ✅ Issue Created: #[ISSUE_NUMBER]
- 📋 Type: [ISSUE_TYPE]
- 🏷️ Labels: (get from issue using gh issue view)
- 🤖 Assignment: [ASSIGNMENT]
- 🔗 URL: [ISSUE_URL]

If assignment is "copilot":
- Note that Copilot will begin work automatically

If assignment is "claude-code":
- Tell user to run `/work #[ISSUE_NUMBER]` to start implementation

## Important Notes

- GitHub Actions will automatically handle project board updates
- Branches are created when work starts (via `/work`), not during issue creation
- Branch prefixes are determined by issue type (feature/, enhancement/, fix/, etc.)
- No manual project board management needed
- Dependencies should be tracked with "Depends on #XX" in issue body
- Sprint labels help with work prioritization in `/work` command
- **Milestones**:
  - Used for high-level release goals (MVP Core, Beta, v1.0)
  - NOT automatically assigned based on priority/type
  - Can be set manually or left blank for later assignment
  - Different from Projects (which track sprints/when work happens)
- **Copilot Capabilities**:
  - **Implementation**: Simple features (Complexity ≤2, Size XS/S)
  - **Unit Tests**: Can write comprehensive test suites
  - **Bug Fixes**: Simple bugs with clear reproduction steps
  - **Documentation**: README updates, code comments, docs
  - **Refactoring**: Simple refactors like renames, extract methods
  - **PR Reviews**: Use `/copilot-review` to request code review
- **Assignment Required**: Must use `mcp__github__assign_copilot_to_issue`
  - Just mentioning @copilot doesn't work
  - MCP call triggers actual Copilot engagement
