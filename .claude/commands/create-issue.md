---
allowed-tools: mcp__github(*), Read(*), Bash(*), TodoWrite(*)
description: Create GitHub issues with proper templates and automatic agent assignment
argument-hint: "title" [additional details]
---

# Create Issue

## Usage Examples

```bash
# Simple usage - Claude handles everything intelligently
/create-issue "Add user authentication"
# Claude will:
# 1. Notice you're on branch 141, offer to stash
# 2. Switch to main
# 3. Ask: "What type? [1-8]" → You choose: 1 (Feature)
# 4. Have conversation: "What problem does this solve? Who are the users?"
# 5. Create issue with your answers
# 6. Offer to return to branch 141

# With file context using @ reference
/create-issue "Fix validation error" @src/validators/user.ts

# Multiple files for context
/create-issue "Refactor API layer" @src/api/index.ts @src/api/types.ts

# Reference a discussion
/create-issue "OAuth integration from discussion #25"

# Detailed description inline
/create-issue "Add dark mode toggle - should persist user preference and apply to all components"
```

## Example Conversation Flow

```
User: /create-issue "Improve search performance"

Claude: You're on branch 141 with uncommitted changes.
        1. Stash and switch to main
        2. Stay on current branch
        Choose [1/2]: 1

Claude: ✅ Stashed work and switched to main

Claude: What type of issue is this?
        1. 🚀 Feature     2. ✨ Enhancement
        3. 🐛 Bug        4. 🔧 Refactor
        Based on "improve", this looks like Enhancement [2]. 
        Choose [1-8]: 2

Claude: Great, you want to enhance existing functionality. Tell me:
        - What currently exists that you want to improve?
        - What specific improvements are you planning?
        - How will users benefit?

User: The current search takes 3-5 seconds. I want to add 
      caching and optimize the query. Users will see instant results.

Claude: ✅ Created issue #142: Improve search performance
        Would you like to return to branch 141?
```

**Note:** When using @ references in Claude Code, the files are automatically included in context.
Claude will analyze the referenced files to better understand the issue scope.

## Context
- Current branch: !`git branch --show-current`
- Open issues: !`gh issue list --state open --limit 5 --json number,title,labels`

## Your Task

When user runs `/create-issue` (with or without arguments), follow these steps:

**If NO arguments provided:**
- Ask: "What would you like to create an issue for? Please provide a title."
- Wait for user to provide the title
- Then continue with the steps below

### Step 0: Branch Check (Simplified)

Get current branch: !`git branch --show-current`

**For now, just create issues from the current branch to avoid stash conflicts.**

If not on main, just note: "Creating issue from feature branch: [branch name]"

Continue with issue creation.

### Step 0.5: Check for Active Work

Check worktrees: !`git worktree list`

If any worktrees exist besides main, mention them but continue.

### Step 1: Intelligent Issue Analysis

Analyze the proposed issue title/description against existing issues:

Show all open issues with: !`gh issue list --state open --limit 20 --json number,title,labels | jq -r '.[] | "#\(.number): \(.title)"'`

**Intelligent Analysis:**
Analyze the new issue title for:
- **Keywords overlap** with existing issues (e.g., "OAuth", "authentication", "user login")
- **Component similarity** (e.g., both mention "API", "frontend", "database")
- **Feature relationships** (e.g., "token refresh" relates to "authentication system")
- **Scope indicators** (e.g., "Add", "Fix", "Enhance" vs "Implement", "Build", "Create")

**Smart Recommendations:**
1. **Exact duplicate detected**: "This appears to be covered by issue #X. Use `/work #X` instead?"
2. **Sub-issue candidate**: "This looks like part of #X: [Parent Title]. Create as sub-issue?"
3. **Related but separate**: "Related to #X but different scope. Create standalone issue?"
4. **Independent work**: "No related issues found. Create standalone issue."

**Present recommendation with reasoning:**
- Show the suggested action
- Explain why (e.g., "Both involve OAuth authentication")
- Let user override if they disagree
- Only ask for confirmation, don't make them choose from scratch

**Auto-execution:**
- If confidence is high (>80% match), auto-suggest and execute with user confirmation
- If unclear, present options with reasoning

**Intelligence Examples:**
- New: "Add OAuth token refresh" + Existing: "#42 Implement authentication system" → **Sub-issue** (OAuth relates to auth)
- New: "Fix login button styling" + Existing: "#42 Implement authentication system" → **Sub-issue** (login is part of auth)  
- New: "Add user dashboard" + Existing: "#42 Implement authentication system" → **Separate** (different feature, but auth dependency)
- New: "Update README" + Existing: "#42 Implement authentication system" → **Separate** (unrelated)
- New: "Implement authentication" + Existing: "#42 Implement authentication system" → **Duplicate** (same work)

### Step 1.5: Select Issue Type

**Present numbered options to the user:**

Based on your title "$TITLE", what type of issue is this?

```
1. 🚀 Feature - New functionality
2. ✨ Enhancement - Improve existing functionality  
3. 🐛 Bug - Something is broken
4. 🔧 Refactor - Code cleanup (no functional changes)
5. 📝 Documentation - Update docs/README
6. 🔨 Chore - Maintenance tasks
7. 🚨 Hotfix - Emergency fix (skip most checks)
8. ⚡ Quick - Minimal issue (skip templates)

Choose [1-8]: _
```

**Smart Auto-Detection:**
Analyze the title for keywords and suggest default:
- Words like "add", "create", "implement", "build", "new" → Suggest 1 (Feature)
- Words like "update", "improve", "enhance" → Suggest 2 (Enhancement)
- Words like "fix", "broken", "error", "fails", "bug", "crash" → Suggest 3 (Bug)
- Words like "refactor", "reorganize", "clean", "restructure" → Suggest 4 (Refactor)
- Words like "document", "readme", "docs", "comment" → Suggest 5 (Documentation)
- Words like "dependency", "config", "setup", "chore" → Suggest 6 (Chore)

Show suggestion: "Based on keywords, this looks like an Enhancement [2]. Press Enter to accept or choose a different number."

**Type Mapping:**
- 1 (Feature) → Use feature template, full workflow, branch prefix: `feature/`
- 2 (Enhancement) → Use enhancement template, normal workflow, branch prefix: `enhancement/`
- 3 (Bug) → Use bug template, normal workflow, branch prefix: `fix/`
- 4 (Refactor) → Use task template, light workflow, branch prefix: `refactor/`
- 5 (Documentation) → Use task template, minimal workflow, branch prefix: `docs/`
- 6 (Chore) → Use task template, light workflow, branch prefix: `chore/`
- 7 (Hotfix) → Use bug template, emergency workflow, branch prefix: `hotfix/`
- 8 (Quick) → Skip templates, minimal workflow

Store the selected type, template path, and workflow mode for use in later steps.

### Step 1.6: Contextual Conversation Based on Type

**Based on the selected type, have a targeted conversation:**

**If Feature (1) selected:**
```
"I see you're adding a new feature. Let me help you flesh this out:
- What problem does this feature solve?
- Who are the primary users?
- Are there any existing features this integrates with?
- Any specific requirements or constraints?"
```

**If Enhancement (2) selected:**
```
"Great, you want to enhance existing functionality. Tell me:
- What currently exists that you want to improve?
- What specific improvements are you planning?
- How will users benefit from this enhancement?
- Any performance or UX goals?"
```

**If Bug (3) selected:**
```
"Let's document this bug properly:
- What's the current broken behavior?
- What should happen instead?
- Steps to reproduce?
- Any error messages or logs?
- How critical is this? (blocking users, minor annoyance, etc.)"
```

**If Refactor (4) selected:**
```
"Refactoring for better code quality. Please provide:
- What code needs refactoring? (@reference files if possible)
- Why does it need refactoring? (performance, readability, maintainability)
- Will this change any external behavior?
- Any specific patterns you want to follow?"
```

**If Documentation (5) selected:**
```
"Documentation update needed. Tell me:
- What needs documenting? (new feature, API, setup instructions)
- Is this updating existing docs or creating new ones?
- Who's the target audience? (developers, users, admins)
- Any specific sections that are confusing?"
```

**If Chore (6) selected:**
```
"Maintenance task. Quick details:
- What needs to be done? (update deps, config changes, cleanup)
- Any risks or breaking changes?
- Estimated effort?"
```

**If Hotfix (7) selected:**
```
"🚨 Emergency fix needed! Quick info:
- What's broken in production?
- How many users affected?
- Temporary workaround available?
- Root cause if known?"
```

**If Quick (8) selected:**
```
"Quick issue - just need the basics:
- One-line description of what needs doing
- Any files involved? (@reference them)
- That's it! Creating minimal issue..."
```

**Gather responses:**
- Let user provide answers naturally
- Use any @-referenced files for additional context
- If user provides minimal info, ask follow-ups
- If user provides extensive detail, skip remaining questions

**WORKFLOW ROUTING BASED ON TYPE:**

**If `--quick` flag:** 
- **JUMP TO MINIMAL WORKFLOW** (Step 5 directly)
- Skip templates, complexity assessment, milestones

**If `--hotfix` flag:**
- **JUMP TO EMERGENCY WORKFLOW** (Step 3 with bug template)
- Skip non-critical steps

**If `--docs` or `--chore` flag:**
- **USE LIGHT WORKFLOW** 
- Skip milestones (sprints handled by GitHub Projects)

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
- **SKIP STEPS 9-10** (no milestones needed, projects handle sprints)

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

### Step 3.5: Compile Issue Details

Use the information gathered from the contextual conversation in Step 1.6:

**Information already collected:**
- Type-specific details from the conversation
- User's answers to targeted questions
- Any @-referenced files provided
- Context about the problem/feature/enhancement

**Additional details if needed:**
- If conversation didn't cover everything, ask follow-ups
- Use @-referenced files to understand implementation context
- Check for related code that might be affected

**Common sources for details:**
- **@-referenced files**: Automatically included in context
- User can paste from a discussion: "Copy from GitHub Discussion #XX"
- Reference existing documentation: "Based on docs/api-guide.md section Y"  
- Reference existing code: "Enhance the UserProfile component in src/components/"
- User provides details directly in response
- Link to external requirements or designs

**If user references a discussion:**
- Use mcp__github functions to fetch discussion content
- Extract key requirements from discussion
- Reference the discussion in the issue body

**If @-referenced files are provided:**
- Analyze the code to understand the context
- Identify specific functions/components mentioned
- Note any TODO comments or existing issues in code
- Use this to write more accurate issue description

**If user provides minimal details:**
- Ask follow-up questions to clarify scope
- Ask about edge cases or error handling needs
- Ask about testing requirements

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

### Step 6: Handle Sub-Issue Creation (If Applicable)

**If this was marked as a sub-issue in Step 1:**
- Use the issue number created in Step 5 and the parent issue number from Step 1
- Add as sub-issue using: `mcp__github__add_sub_issue` with:
  - owner: vanman2024
  - repo: multi-agent-claude-code  
  - issue_number: [parent issue number from Step 1]
  - sub_issue_id: [newly created issue ID - get from created issue response]
- Add comment to parent issue noting the new sub-issue
- Skip milestone assignment (sub-issues inherit parent milestone)

**If this is a standalone issue:**
- Continue with dependency checking below

### Step 7: Check Dependencies

**REMINDER: No branch exists yet - branches are created by `/work`, not `/create-issue`**

After creating issue, check if it depends on other work:

Ask user if this issue depends on other issues.
If yes:
- Add dependency note to issue body using the actual issue number from Step 5
- Note: "Depends on #[other-issue-number]" in the issue description
- Do NOT try to add a 'blocked' label (it doesn't exist in most repos)
- Dependencies are tracked through issue descriptions, not labels

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
- Include instruction to run `/work #[actual-issue-number]` when ready (using the issue number from Step 5)
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

### Step 9: Milestone Assignment (Optional - Skip for Sub-Issues)

**For sub-issues: ALWAYS SKIP - they inherit parent milestone.**
**For standalone issues: SKIP for now to avoid errors.**

Milestones can be set manually later if needed using:
- Go to the issue in GitHub
- Use the milestone dropdown on the right side
- Available milestones: MVP Core, Beta Release, v1.0 Production, etc.

**Future enhancement**: Add proper interactive milestone selection that:
- Lists your actual milestones (MVP Core, Beta Release, etc.)
- Lets you choose by name, not number
- Only assigns if you actually select one

### Step 10: GitHub Projects Integration (Future)

**Note**: Sprint management will be handled through GitHub Projects, not labels.

For now, skip automatic project assignment. Issues can be manually added to project boards later.

When GitHub Projects integration is implemented:
- Issues will be automatically added to active project
- Sprint/iteration assignment will be handled by project automation
- No manual sprint labels needed

### Step 10.5: Priority Setting

Ask for priority (P0/P1/P2/P3) and add it to the metadata section in issue body.
DO NOT add priority as a label - it's tracked in the metadata and project board fields.

### Step 11: Summary & Context Return

Provide the user with:

Get the issue URL using the actual issue number from Step 5.
- Use the issue number that was just created, NOT a hardcoded example
- Command pattern: gh issue view [ACTUAL_ISSUE_NUMBER] --json url --jq .url

Show summary with actual values from the created issue:
- ✅ Issue Created: #(actual issue number from Step 5)
- 📋 Type: (actual type determined in Step 1.5/Step 2)
- 🏷️ Labels: (get from issue using gh issue view with actual issue number)
- 🤖 Assignment: (copilot or claude-code based on Step 8)
- 🔗 URL: (actual URL retrieved above)

If assignment is "copilot":
- Note that Copilot will begin work automatically

If assignment is "claude-code":
- Tell user to run `/work #[actual-issue-number]` to start implementation

### Step 12: Next Steps

Show the user what they can do next:

**To work on the new issue:**
- Run: `/work #[new-issue-number]` to start implementation
- This will create a new branch and draft PR

**To continue with current work:**
- Stay on your current branch and continue working

## Important Notes

- **Branches are created by `/work`, NOT by `/create-issue`**
  - `/create-issue` only creates the GitHub issue
  - `/work #123` creates the branch and draft PR
  - This separation keeps planning (issues) separate from implementation (branches)
- GitHub Actions will automatically handle project board updates
- Branch prefixes are determined by issue type (feature/, enhancement/, fix/, etc.)
- No manual project board management needed
- Dependencies should be tracked with "Depends on #XX" in issue body
- GitHub Projects will handle sprint/iteration management
- **Milestones**:
  - Used for high-level release goals (MVP Core, Beta, v1.0)
  - NOT automatically assigned based on priority/type
  - Can be set manually or left blank for later assignment
  - Projects handle sprints, iterations, and work prioritization
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
