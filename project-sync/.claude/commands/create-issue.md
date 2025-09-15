---
allowed-tools: mcp__github(*), Read(*), Bash(*), TodoWrite(*)
description: Create GitHub issues with proper templates and automatic agent assignment
argument-hint: [--feature|--bug|--task|--hotfix|--simple] "title"
---

# Create Issue

<!--
WHEN TO USE THIS COMMAND:
- Planning a new feature that needs tracking
- Documenting a bug for the record  
- Creating work items for sprint planning
- Work that needs review/approval
- Tasks you want Copilot to handle (simple ones)

WHEN NOT TO USE:
- Quick fixes (use /wip instead)
- Exploratory work (use /wip instead)
- Documentation updates (just do them)

FLAGS:
--simple     : Use GitHub issue templates (simpler, no agent assignment)
--feature    : New functionality (complex mode with agent routing)
--bug        : Something broken (complex mode with agent routing)
--task       : Simple task (uses GitHub template)
--hotfix     : Emergency fix (uses GitHub template, creates branch)

AUTO-ASSIGNMENT (Complex Mode Only):
- Copilot gets: Complexity ≤2 AND Size ≤S
- Claude gets: Everything else
-->

## Context
- Current repository: !`gh repo view --json nameWithOwner -q .nameWithOwner`
- Current branch: !`git branch --show-current`
- Open issues: !`gh issue list --state open --limit 5 --json number,title,labels`
- Recent issues: !`gh issue list --state open --limit 3 --json number,title`

## Your Task

When user runs `/create-issue $ARGUMENTS`, follow these steps:

### Step 0: Detect Repository Context and Mode

First, get the current repository information and determine mode:
```bash
# Get repository owner and name
REPO_INFO=$(gh repo view --json owner,name 2>/dev/null)
if [ -z "$REPO_INFO" ]; then
  echo "Error: Not in a GitHub repository or gh CLI not configured"
  exit 1
fi

OWNER=$(echo "$REPO_INFO" | jq -r '.owner.login')
REPO=$(echo "$REPO_INFO" | jq -r '.name')
echo "Working in repository: $OWNER/$REPO"

# Check for --simple flag or simple issue types
ARGS="$ARGUMENTS"
SIMPLE_MODE=false

if [[ "$ARGS" == *"--simple"* ]] || [[ "$ARGS" == *"--task"* ]] || [[ "$ARGS" == *"--hotfix"* ]]; then
  SIMPLE_MODE=true
  echo "Using simple mode with GitHub issue templates"
fi
```

### Step 0.5: Simple Mode - Use GitHub Issue Templates

If SIMPLE_MODE is true, use a simplified workflow:

```bash
if [ "$SIMPLE_MODE" = true ]; then
  # Parse type from arguments
  TYPE=""
  TITLE=""
  
  if [[ "$ARGS" == *"--bug"* ]]; then
    TYPE="bug"
    TITLE=$(echo "$ARGS" | sed 's/--bug//' | xargs)
  elif [[ "$ARGS" == *"--feature"* ]]; then
    TYPE="feature"
    TITLE=$(echo "$ARGS" | sed 's/--feature//' | xargs)
  elif [[ "$ARGS" == *"--task"* ]]; then
    TYPE="task"
    TITLE=$(echo "$ARGS" | sed 's/--task//' | xargs)
  elif [[ "$ARGS" == *"--hotfix"* ]]; then
    TYPE="hotfix"
    TITLE=$(echo "$ARGS" | sed 's/--hotfix//' | xargs)
  else
    # Ask for type
    echo "Select issue type:"
    echo "1) Bug"
    echo "2) Feature"
    echo "3) Task"
    echo "4) Hotfix"
    read -p "Choice (1-4): " CHOICE
    
    case $CHOICE in
      1) TYPE="bug";;
      2) TYPE="feature";;
      3) TYPE="task";;
      4) TYPE="hotfix";;
    esac
    
    TITLE=$(echo "$ARGS" | sed 's/--simple//' | xargs)
  fi
  
  # Read appropriate GitHub template
  TEMPLATE_PATH=".github/ISSUE_TEMPLATE/${TYPE}_report.yml"
  if [[ "$TYPE" == "feature" ]]; then
    TEMPLATE_PATH=".github/ISSUE_TEMPLATE/feature_request.yml"
  fi
  
  # Simple prompts based on template
  echo "Creating $TYPE: $TITLE"
  
  # Gather minimal information
  BODY=""
  
  if [[ "$TYPE" == "bug" ]]; then
    echo "What's broken? (required):"
    read DESCRIPTION
    echo "Steps to reproduce (or press Enter to skip):"
    read STEPS
    BODY="## What's broken?\n$DESCRIPTION\n\n## Steps to Reproduce\n$STEPS"
  elif [[ "$TYPE" == "feature" ]]; then
    echo "Describe the feature (required):"
    read DESCRIPTION
    echo "What problem does it solve? (or press Enter to skip):"
    read PROBLEM
    BODY="## Description\n$DESCRIPTION\n\n## Problem it Solves\n$PROBLEM"
  elif [[ "$TYPE" == "task" ]]; then
    echo "What needs to be done? (required):"
    read DESCRIPTION
    BODY="## Task\n$DESCRIPTION"
  elif [[ "$TYPE" == "hotfix" ]]; then
    echo "What's critically broken? (required):"
    read CRITICAL
    echo "Impact (required):"
    read IMPACT
    BODY="## Critical Issue\n$CRITICAL\n\n## Impact\n$IMPACT"
  fi
  
  # Create issue with appropriate labels
  LABELS="$TYPE"
  if [[ "$TYPE" == "feature" ]]; then
    LABELS="enhancement"
  elif [[ "$TYPE" == "hotfix" ]]; then
    LABELS="hotfix,urgent"
  fi
  
  # Use mcp__github__create_issue
  # owner: $OWNER
  # repo: $REPO
  # title: "[$TYPE]: $TITLE"
  # body: $BODY
  # labels: [$LABELS]
  
  echo "✅ Simple issue created #$ISSUE_NUMBER"
  echo "No agent assignment or complexity estimation"
  exit 0
fi
```

If not in simple mode, continue with the complex workflow below...

### Step 1: Check if Creating Sub-Issue

First, determine if this is a sub-issue for an existing parent:

```bash
echo "Are you creating a sub-issue for an existing issue? (y/n)"
```

If yes:
- Ask for parent issue number
- Skip to simplified creation (no complexity/size questions)
- After creation, link using GraphQL mutation:
  ```graphql
  mutation {
    addSubIssue(input: {
      issueId: "PARENT_NODE_ID"
      subIssueId: "SUB_NODE_ID"
    }) {
      issue { number }
    }
  }
  ```
- Add to TodoWrite: "Issue #XXX: [Sub-issue title]"
- Skip all other steps and finish

If no, continue with regular issue creation...

### Step 2: Check for Existing Similar Issues

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

### Step 3: Determine Issue Type

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

### Step 4: Load Appropriate Template

Based on the type, read the template:
- feature → Read templates/local_dev/feature-template.md
- enhancement → Read templates/local_dev/enhancement-template.md
- bug → Read templates/local_dev/bug-template.md
- task/refactor → Read templates/local_dev/task-template.md

### Step 5: Fill Template

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

### Step 6: Create GitHub Issue

Use mcp__github__create_issue with:
- owner: $OWNER (from Step 0)
- repo: $REPO (from Step 0)
- title: provided by user
- body: filled template with metadata section + testing requirements
- labels: [issue-type] (ONLY the type: bug, feature, enhancement, refactor, task)

Store the created issue number for potential sub-issue creation.

### Step 7: Create Sub-Issues (if needed for main issue)

After creating the main issue (if not already a sub-issue), ask if it should be broken into sub-issues:

```bash
echo "Would you like to break this issue into sub-issues? (y/n)"
```

If yes, for complex features or enhancements, suggest natural sub-issues:
- **Feature**: Design, Implementation, Tests, Documentation
- **Bug**: Reproduce, Fix root cause, Add tests, Verify fix
- **Enhancement**: Research, Implement, Validate, Document

For each sub-issue:
1. Create using mcp__github__create_issue
2. Get the parent and sub-issue node IDs using GraphQL:
   ```graphql
   query {
     repository(owner: "$OWNER", name: "$REPO") {
       issue(number: ISSUE_NUMBER) { id }
     }
   }
   ```
3. Link as sub-issue using GraphQL mutation:
   ```graphql
   mutation {
     addSubIssue(input: {
       issueId: "PARENT_NODE_ID"
       subIssueId: "SUB_NODE_ID"
     }) {
       issue { number }
     }
   }
   ```
4. Add to TodoWrite: "Issue #XXX: [Sub-issue title]"

### Step 8: Check Dependencies

**NOTE: Branch creation happens when work starts (via `/work` command), not during issue creation**

After creating issue, check if it depends on other work:
```bash
# Ask user if this depends on other issues
# If yes, add dependency note to issue body
echo "Does this issue depend on any other issues? (y/n)"
# If yes, update the body to include dependencies
# Note: We don't use labels for dependencies, just track in issue body
```

### Step 9: Agent Assignment

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
    ['security', 'architecture'].includes(l)
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
    owner: OWNER,
    repo: REPO,
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
    owner: OWNER,
    repo: REPO,
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
    owner: OWNER,
    repo: REPO,
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

### Step 10: Milestone Assignment (Optional)

Ask user if they want to assign a milestone:
```bash
# List available milestones
echo "Available milestones:"
gh api repos/${OWNER}/${REPO}/milestones --jq '.[] | "\(.number): \(.title)"'

# Ask user to select milestone (or skip)
echo "Select milestone number (or press Enter to skip):"
read MILESTONE_NUMBER

if [[ ! -z "$MILESTONE_NUMBER" ]]; then
  # Get milestone title for confirmation
  MILESTONE_TITLE=$(gh api repos/${OWNER}/${REPO}/milestones --jq ".[] | select(.number==$MILESTONE_NUMBER) | .title")
  echo "Assigning to milestone: $MILESTONE_TITLE"
  gh issue edit $ISSUE_NUMBER --milestone $MILESTONE_NUMBER
else
  echo "No milestone assigned - can be set manually later"
fi
```

### Step 11: Sprint Assignment (Optional)

```bash
# Sprint tracking happens via GitHub Projects, not labels
# Project board will automatically track the issue
echo "Issue will be tracked in the project board automatically"
```

### Step 12: Priority Setting

Ask for priority (P0/P1/P2/P3) and add it to the metadata section in issue body.
DO NOT add priority as a label - it's tracked in the metadata and project board fields.

### Step 13: Summary

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

- **No branch switching required** - Issues can be created from any branch
- GitHub Actions will automatically handle project board updates
- Branches are created when work starts (via `/work`), not during issue creation
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
