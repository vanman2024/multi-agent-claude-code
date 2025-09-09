---
allowed-tools: Bash(*), mcp__github__assign_copilot_to_issue(*), TodoWrite(*)
description: Create GitHub issue with automatic complexity assessment
argument-hint: "issue title"
---

# Create Issue V2

## <assessment_prompt>
Analyze the issue title and determine:
- Complexity (1-5)
- Size (XS/S/M/L/XL)
- Whether Copilot can handle it (complexity ≤2 AND size ≤S)
</assessment_prompt>

## Your Task

Create a GitHub issue with automatic agent assignment.

### Step 1: Create Issue
Run: !python3 scripts/commands/create-issue.py "$ARGUMENTS"

### Step 2: Get Issue Number
Store the issue number from the output for agent assignment.

### Step 3: Auto-Assign Agent
If the script indicates Copilot assignment (simple + small):
- Use mcp__github__assign_copilot_to_issue with the issue number
- Agent: @agent-copilot-handler

If the script indicates Claude Code required:
- Add to TodoWrite: "Issue #[number]: $ARGUMENTS"
- Note: Implementation via /work command

### Step 4: Report Success
Show the issue URL and next steps.