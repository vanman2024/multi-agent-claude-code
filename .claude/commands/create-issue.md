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
  echo "❌ ERROR: Your main branch is not up to date!"
  echo ""
  echo "Run this command first:"
  echo "  git pull origin main"
  echo ""
  echo "Local main:  $LOCAL"
  echo "Remote main: $REMOTE"
  echo ""
  echo "See WORKFLOW.md for the required process."
  exit 1
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
3. Add complexity and size metadata
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

Check what Copilot can handle:
```bash
# Get the created issue number
ISSUE_NUMBER={from mcp__github response}

# Determine what Copilot can do
COPILOT_CAPABLE=false
COPILOT_TASK=""

# Check different Copilot capabilities
if [[ "$ISSUE_TYPE" == "task" ]] && [[ "$TITLE" =~ "test" || "$TITLE" =~ "unit test" ]]; then
  # Copilot is great at writing tests
  COPILOT_CAPABLE=true
  COPILOT_TASK="write unit tests"
  
elif [[ "$ISSUE_TYPE" == "bug" ]] && [[ $COMPLEXITY -le 2 ]]; then
  # Simple bug fixes with clear reproduction steps
  COPILOT_CAPABLE=true
  COPILOT_TASK="fix bug"
  
elif [[ "$ISSUE_TYPE" == "task" ]] && [[ "$TITLE" =~ "document" || "$TITLE" =~ "readme" ]]; then
  # Documentation updates
  COPILOT_CAPABLE=true
  COPILOT_TASK="update documentation"
  
elif [[ "$ISSUE_TYPE" == "refactor" ]] && [[ $COMPLEXITY -le 2 ]] && [[ "$SIZE" == "XS" || "$SIZE" == "S" ]]; then
  # Simple refactoring (rename, extract method, etc.)
  COPILOT_CAPABLE=true
  COPILOT_TASK="refactor code"
  
elif [[ $COMPLEXITY -le 2 ]] && [[ "$SIZE" == "XS" || "$SIZE" == "S" ]]; then
  # Small AND simple implementation
  COPILOT_CAPABLE=true
  COPILOT_TASK="implement feature"
fi

if [[ "$COPILOT_CAPABLE" == "true" ]]; then
  echo "Assigning to GitHub Copilot for: $COPILOT_TASK"
  
  # ACTUALLY ASSIGN COPILOT using MCP
  # Use mcp__github__assign_copilot_to_issue to assign Copilot
  # This triggers Copilot to start working
  
  # Add specific instructions for Copilot
  gh issue comment $ISSUE_NUMBER --body "🤖 **Assigned to GitHub Copilot**
  
Task: $COPILOT_TASK
Complexity: $COMPLEXITY  
Size: $SIZE

Copilot Instructions:
$(case "$COPILOT_TASK" in
  "write unit tests")
    echo "- Write comprehensive unit tests"
    echo "- Aim for 80%+ code coverage"
    echo "- Include edge cases and error scenarios"
    echo "- Follow existing test patterns in the codebase"
    ;;
  "fix bug")
    echo "- Fix the bug as described"
    echo "- Add tests to prevent regression"
    echo "- Verify the fix doesn't break existing functionality"
    ;;
  "update documentation")
    echo "- Update documentation as requested"
    echo "- Keep consistent with existing style"
    echo "- Include code examples if relevant"
    ;;
  "refactor code")
    echo "- Refactor without changing functionality"
    echo "- Ensure all tests still pass"
    echo "- Follow project coding standards"
    ;;
  *)
    echo "- Implement as specified in issue description"
    echo "- Write tests for new functionality"
    echo "- Follow project patterns and standards"
    ;;
esac)

Copilot has been assigned and will begin work automatically."
else
  # Complex OR large - needs Claude Code
  echo "This requires Claude Code local development"
  
  # Add comment with next steps
  gh issue comment $ISSUE_NUMBER --body "🧠 **Requires Claude Code/Agent Orchestration**

Complexity: $COMPLEXITY
Size: $SIZE
Issue Type: $ISSUE_TYPE

Next step: Run \`/work #$ISSUE_NUMBER\` when ready to begin implementation."
fi
```

### Step 7: Sprint Assignment (Optional)

Ask if this should be added to current sprint:
```bash
# If yes, add sprint label
gh issue edit $ISSUE_NUMBER --add-label "sprint:current"

# Check sprint capacity
gh issue list --label "sprint:current" --json number | jq length
# Warn if sprint has > 10 issues
```

### Step 8: Priority Setting

Ask for priority (P0/P1/P2/P3):
```bash
# Add priority label
gh issue edit $ISSUE_NUMBER --add-label "P$PRIORITY"

# If P0, also add urgent label
if [[ $PRIORITY == "0" ]]; then
  gh issue edit $ISSUE_NUMBER --add-label "urgent"
fi
```

### Step 9: Summary

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