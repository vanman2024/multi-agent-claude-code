---
allowed-tools: Read(*), Bash(*), mcp__github__create_issue(*), mcp__github__assign_copilot_to_issue(*), mcp__github__add_issue_comment(*), TodoWrite(*)
description: Create GitHub issue with proper templates and auto-assignment
argument-hint: "issue title/description"
---

# Create Issue (Clean)

## Load Templates Into Context
- @templates/local_dev/feature-template.md
- @templates/local_dev/bug-template.md
- @templates/local_dev/enhancement-template.md
- @templates/local_dev/task-template.md

## Load Project Configuration
- @CLAUDE.md
- @package.json

## Your Instructions

You need to create a GitHub issue for: "$ARGUMENTS"

### Step 1: Verify Prerequisites
Run this command to check you're on main branch:
!git branch --show-current

If not on main, tell the user to switch to main first.

### Step 2: Analyze the Request
Determine from "$ARGUMENTS":
- What type of issue (feature/bug/enhancement/task)
- Complexity (1-5 scale)
- Size (XS/S/M/L/XL)

Simple indicators (complexity 1-2, size XS-S):
- "fix typo", "update readme", "add comment"
- "rename function", "update dependency"
- "add endpoint", "fix test"

Complex indicators (complexity 3-5, size M-XL):
- "refactor", "architecture", "security"
- "authentication", "migration", "integration"
- "performance", "infrastructure"

### Step 3: Select and Fill Template
Choose the appropriate template from the loaded files based on issue type.
Fill in the template with:
- Title from "$ARGUMENTS"
- Proper checkboxes (unchecked - they're work items)
- Metadata section at the bottom

### Step 4: Create the Issue
Use mcp__github__create_issue to create the issue with:
- owner: vanman2024
- repo: multi-agent-claude-code
- title: from "$ARGUMENTS"
- body: the filled template
- labels: array with the issue type

Store the created issue number.

### Step 5: Assign to Appropriate Agent
If complexity ≤ 2 AND size is XS or S:
- Use mcp__github__assign_copilot_to_issue with the issue number
- Use mcp__github__add_issue_comment to add: "🤖 Auto-assigned to GitHub Copilot"

Otherwise:
- Add to your todo list using TodoWrite: "Issue #[number]: [title]"
- Use mcp__github__add_issue_comment to add: "🧠 Requires Claude Code agents"

### Step 6: Report What You Did
Tell the user:
- Issue number created
- Who it was assigned to
- Link to the issue