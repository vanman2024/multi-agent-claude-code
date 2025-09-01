---
allowed-tools: mcp__github(*), Read(*), Bash(*), TodoWrite(*)
description: Create GitHub issues with proper templates and automatic agent assignment
argument-hint: [type] [title]
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

### Step 1: Determine Issue Type

Ask the user:
```
What type of issue should this be?
- **feature**: New functionality to be added
- **bug**: Something is broken or not working
- **enhancement**: Improve existing functionality  
- **refactor**: Code cleanup/restructuring
- **task**: Simple work item
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

### Step 2: Load Appropriate Template

Based on the type, read the template:
- feature → Read templates/local_dev/feature-template.md
- bug → Read templates/local_dev/bug-template.md
- enhancement → Read templates/local_dev/enhancement-template.md
- refactor → Read templates/local_dev/refactor-template.md
- task → Read templates/local_dev/task-template.md
- generic/other → Read templates/local_dev/issue-template.md

### Step 3: Fill Template

Using the template structure:
1. Replace placeholders with actual content
2. Keep all checkboxes unchecked `[ ]` (they represent work to be done)
3. Add metadata section at the bottom:
   ```markdown
   ---
   **Metadata** (for automation parsing):
   - **Priority**: P0/P1/P2/P3 (ask user)
   - **Complexity**: 1-5 (from Step 1)
   - **Size**: XS/S/M/L/XL (from Step 1)
   - **Component**: Frontend/Backend/Database/Auth/Infra
   - **Milestone**: (Optional - ask user: MVP Core/Beta/v1.0 or leave blank)
   ```
4. Include acceptance criteria
5. Add testing requirements section

### Step 4: Create GitHub Issue

Use mcp__github__create_issue with:
- owner: from repository context
- repo: from repository context
- title: provided by user
- body: filled template + complexity/size metadata + testing requirements
- labels: [issue-type, "complexity-X", "size-Y"]

### Step 5: Check Dependencies

After creating issue, check if it depends on other work:
```bash
# Ask user if this depends on other issues
# If yes, add dependency note to issue body
gh issue edit $ISSUE_NUMBER --body-file updated-body.md

# Add blocked label if has dependencies
gh issue edit $ISSUE_NUMBER --add-label "blocked"
```

### Step 6: Agent Assignment

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

### Step 7: Milestone Assignment (Optional)

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

### Step 8: Sprint Assignment (Optional)

Ask if this should be added to current sprint:
```bash
# If yes, add sprint label
gh issue edit $ISSUE_NUMBER --add-label "sprint:current"

# Check sprint capacity
gh issue list --label "sprint:current" --json number | jq length
# Warn if sprint has > 10 issues
```

### Step 9: Priority Setting

Ask for priority (P0/P1/P2/P3):
```bash
# Add priority label
gh issue edit $ISSUE_NUMBER --add-label "P$PRIORITY"

# If P0, also add urgent label
if [[ $PRIORITY == "0" ]]; then
  gh issue edit $ISSUE_NUMBER --add-label "urgent"
fi
```

### Step 10: Summary

Provide the user with:
```bash
# Get the issue URL
ISSUE_URL=$(gh issue view $ISSUE_NUMBER --json url --jq .url)

echo "✅ Issue Created: #$ISSUE_NUMBER"
echo "📋 Type: $ISSUE_TYPE"
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