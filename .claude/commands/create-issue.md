---
allowed-tools: mcp__github(*), Read(*), Bash(*), TodoWrite(*)
description: Create GitHub issues with proper templates and automatic agent assignment
argument-hint: [type] [title] [issue_number]
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

```bash
# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Check if on main
if [[ "$CURRENT_BRANCH" != "main" ]]; then
  echo "❌ ERROR: You must be on main branch to create issues!"
  echo ""
  echo "Run these commands first:"
  echo "  git checkout main"
  echo "  git pull origin main"
  echo ""
  echo "Current branch: $CURRENT_BRANCH"
  echo "Required branch: main"
  echo ""
  echo "See WORKFLOW.md for the required process."
  exit 1
fi

# Check if main is up to date
git fetch origin main --quiet
LOCAL=$(git rev-parse main)
REMOTE=$(git rev-parse origin/main)

if [[ "$LOCAL" != "$REMOTE" ]]; then
  echo "⚠️ Your main branch is not up to date!"
  echo "Local:  $LOCAL"
  echo "Remote: $REMOTE"
  echo ""
  echo "🔄 Auto-pulling latest changes..."
  git pull origin main

  if [ $? -ne 0 ]; then
    echo "❌ ERROR: Failed to pull latest changes"
    echo "Please resolve any conflicts and try again"
    exit 1
  fi

  echo "✅ Successfully pulled latest changes"
fi

echo "✅ On main branch with latest changes - proceeding..."
```

If not on main or not up to date, STOP and tell the user to:
1. `git checkout main`
2. `git pull origin main`
3. Then retry the command

**DO NOT PROCEED if not on main with latest changes!**

### Step 1: Check for Existing Similar Issues

Before creating a new issue, check if similar work is already tracked:

```bash
# Show all open issues
echo "📋 Checking existing open issues..."
gh issue list --state open --limit 20 --json number,title,labels | jq -r '.[] | "#\(.number): \(.title)"'

# Ask user to confirm
echo ""
echo "❓ Is your issue already covered by any of the above?"
echo "   If yes, work on that existing issue instead."
echo "   If no, proceed to create a new issue."
```

If a similar issue exists, suggest using `/work #[existing-issue]` instead.

### Step 2: Determine Issue Type

Ask the user:
```
What type of issue should this be?
- **feature**: New functionality, enhancements, or refactoring
- **bug**: Something is broken or not working
- **task**: Simple work item or chore
```

Also ask for:
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

Based on the type, read the template:
- feature/enhancement/refactor → Read templates/local_dev/feature-template.md
- bug → Read templates/local_dev/bug-template.md
- task → Read templates/local_dev/task-template.md

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

Use mcp__github__create_issue with:
- owner: from repository context
- repo: from repository context
- title: provided by user
- body: filled template with metadata section + testing requirements
- labels: [issue-type] (ONLY the type: bug, feature, enhancement, refactor, task)

### Step 6: Create and Link Branch

**IMMEDIATELY after issue creation, create linked branch:**

```bash
# Get the issue number that was just created
ISSUE_NUMBER=$(gh issue list --limit 1 --json number -q '.[0].number')

# Create branch name based on type and issue number
ISSUE_TYPE=$(gh issue view $ISSUE_NUMBER --json labels -q '.labels[0].name')
ISSUE_TITLE=$(gh issue view $ISSUE_NUMBER --json title -q '.title' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | cut -c1-30)
BRANCH_NAME="${ISSUE_TYPE}-${ISSUE_NUMBER}-${ISSUE_TITLE}"

# Create and push the branch
git checkout -b $BRANCH_NAME
git push -u origin $BRANCH_NAME

# Link branch to issue using gh issue develop
gh issue develop $ISSUE_NUMBER --base $BRANCH_NAME

echo "✅ Created and linked branch: $BRANCH_NAME"
echo "✅ Branch now shows in issue #$ISSUE_NUMBER Development section"

# Switch back to main for clean state
git checkout main
```

### Step 7: Check Dependencies

After creating issue and branch, check if it depends on other work:
```bash
# Ask user if this depends on other issues
# If yes, add dependency note to issue body
gh issue edit $ISSUE_NUMBER --body-file updated-body.md

# Add blocked label if has dependencies
gh issue edit $ISSUE_NUMBER --add-label "blocked"
```

### Step 8: Agent Assignment

**IMMEDIATE Copilot Auto-Assignment for Simple Tasks:**

```javascript
// Determine if Copilot should handle this (BOTH conditions must be true)
const shouldAutoAssignCopilot = (complexity, size, type, labels) => {
  // Check complexity (must be simple)
  const isSimple = complexity <= 2;

  // Check size (must be small)
  const isSmall = ['XS', 'S'].includes(size);

  // Check for blocking labels
  const hasBlockingLabels = labels.some(l =>
    ['security', 'architecture', 'blocked'].includes(l)
  );

  // Auto-assign if BOTH simple AND small AND no blockers
  return isSimple && isSmall && !hasBlockingLabels;
};

// Implementation
if (shouldAutoAssignCopilot(COMPLEXITY, SIZE, ISSUE_TYPE, LABELS)) {
  echo "🤖 Auto-assigning to GitHub Copilot (Complexity: $COMPLEXITY, Size: $SIZE)"

  // IMMEDIATELY assign Copilot using MCP
  // This triggers Copilot to start working within seconds!
  await mcp__github__assign_copilot_to_issue({
    owner: 'vanman2024',
    repo: 'multi-agent-claude-code',
    issueNumber: ISSUE_NUMBER
  });

  // Determine task type for instructions
  let COPILOT_TASK = "";
  if (TITLE.includes("test")) {
    COPILOT_TASK = "write unit tests";
  } else if (ISSUE_TYPE === "bug") {
    COPILOT_TASK = "fix bug";
  } else if (TITLE.includes("document") || TITLE.includes("readme")) {
    COPILOT_TASK = "update documentation";
  } else if (ISSUE_TYPE === "refactor") {
    COPILOT_TASK = "refactor code";
  } else {
    COPILOT_TASK = "implement feature";
  }

  // Add specific instructions comment
  await mcp__github__add_issue_comment({
    owner: 'vanman2024',
    repo: 'multi-agent-claude-code',
    issue_number: ISSUE_NUMBER,
    body: `🤖 **GitHub Copilot Auto-Assigned**

**Task**: ${COPILOT_TASK}
**Complexity**: ${COMPLEXITY}/5 (Simple)
**Size**: ${SIZE} (Small)
**Type**: ${ISSUE_TYPE}

**Expected Timeline**:
- 👀 Copilot acknowledges: ~5 seconds
- 🌿 Branch created: ~30 seconds
- 📝 Draft PR opened: ~1 minute
- 💻 Implementation: 10-15 minutes
- ✅ PR ready for review: ~17 minutes

**Copilot Instructions**:
${getTaskInstructions(COPILOT_TASK)}

Copilot has been assigned and will begin work automatically within seconds.
Watch for branch: \`copilot/${ISSUE_TYPE}-${ISSUE_NUMBER}\``
  });

  ASSIGNMENT = "copilot";

} else {
  // Complex OR large OR has blocking labels - needs Claude Code
  echo "📋 Requires Claude Code (Complexity: $COMPLEXITY, Size: $SIZE)"

  let reason = "";
  if (COMPLEXITY > 2) reason = "High complexity (${COMPLEXITY}/5)";
  else if (!['XS', 'S'].includes(SIZE)) reason = "Large size (${SIZE})";
  else if (hasBlockingLabels) reason = "Has blocking labels";

  await mcp__github__add_issue_comment({
    owner: 'vanman2024',
    repo: 'multi-agent-claude-code',
    issue_number: ISSUE_NUMBER,
    body: `🧠 **Requires Claude Code/Agent Orchestration**

**Reason**: ${reason}
**Complexity**: ${COMPLEXITY}/5
**Size**: ${SIZE}
**Type**: ${ISSUE_TYPE}

This task exceeds Copilot's capabilities (complexity > 2 OR size > S).
Requires Claude Code agents with full MCP tool access.

**Next step**: Run \`/work #${ISSUE_NUMBER}\` when ready to begin implementation.`
  });

  ASSIGNMENT = "claude-code";
}

// Helper function for task instructions
function getTaskInstructions(taskType) {
  switch(taskType) {
    case "write unit tests":
      return `- Write comprehensive unit tests
- Aim for 80%+ code coverage
- Include edge cases and error scenarios
- Follow existing test patterns in the codebase
- Mock external dependencies`;

    case "fix bug":
      return `- Fix the bug as described in the issue
- Add regression tests to prevent recurrence
- Verify fix doesn't break existing functionality
- Update any affected documentation`;

    case "update documentation":
      return `- Update documentation as requested
- Keep consistent with existing style
- Include code examples where relevant
- Check for broken links`;

    case "refactor code":
      return `- Refactor without changing functionality
- Ensure all tests still pass
- Follow project coding standards
- Update imports and exports as needed`;

    default:
      return `- Implement as specified in issue description
- Write tests for new functionality
- Follow existing project patterns
- Add appropriate error handling`;
  }
}
```

### Step 9: Milestone Assignment (Optional)

Ask user if they want to assign a milestone:
```bash
# List available milestones
echo "Available milestones:"
gh api repos/vanman2024/multi-agent-claude-code/milestones --jq '.[] | "\(.number): \(.title)"'

# Ask user to select milestone (or skip)
echo "Select milestone number (or press Enter to skip):"
read MILESTONE_NUMBER

if [[ ! -z "$MILESTONE_NUMBER" ]]; then
  # Get milestone title for confirmation
  MILESTONE_TITLE=$(gh api repos/vanman2024/multi-agent-claude-code/milestones --jq ".[] | select(.number==$MILESTONE_NUMBER) | .title")
  echo "Assigning to milestone: $MILESTONE_TITLE"
  gh issue edit $ISSUE_NUMBER --milestone $MILESTONE_NUMBER
else
  echo "No milestone assigned - can be set manually later"
fi
```

### Step 10: Sprint Assignment (Optional)

Ask if this should be added to current sprint:
```bash
# If yes, add sprint label
gh issue edit $ISSUE_NUMBER --add-label "sprint:current"

# Check sprint capacity
gh issue list --label "sprint:current" --json number | jq length
# Warn if sprint has > 10 issues
```

### Step 11: Priority Setting

Ask for priority (P0/P1/P2/P3) and add it to the metadata section in issue body.
DO NOT add priority as a label - it's tracked in the metadata and project board fields.

### Step 12: Summary

Provide the user with:
```bash
# Get the issue URL
ISSUE_URL=$(gh issue view $ISSUE_NUMBER --json url --jq .url)

echo "✅ Issue Created: #$ISSUE_NUMBER"
echo "📋 Type: $ISSUE_TYPE"
echo "🌿 Branch: $BRANCH_NAME"
echo "🏷️ Labels: $(gh issue view $ISSUE_NUMBER --json labels --jq '.labels[].name' | tr '\n' ', ')"
echo "🤖 Assignment: $ASSIGNMENT"
echo "🔗 URL: $ISSUE_URL"

if [[ "$ASSIGNMENT" == "copilot" ]]; then
  echo "Copilot will begin work automatically."
else
  echo "Run '/work #$ISSUE_NUMBER' to start implementation."
fi
```

## Important Notes

- GitHub Actions will automatically handle project board updates
- Feature branches are created automatically by workflows
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
