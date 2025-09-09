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

## <complexity_assessment>
Analyze "$ARGUMENTS" to determine:
1. Issue type from title keywords
2. Complexity (1-5) based on:
   - Simple (1-2): typos, renames, documentation, simple endpoints
   - Moderate (3): multiple components, integration work
   - Complex (4-5): architecture, security, migrations, infrastructure
3. Size estimate:
   - XS: < 1 hour
   - S: 1-4 hours  
   - M: 1-2 days
   - L: 3-5 days
   - XL: > 1 week
4. Copilot eligibility: complexity ≤ 2 AND size ∈ {XS, S}
</complexity_assessment>

## <template_selection>
Based on the issue type:
- "bug" or "fix" → bug-template.md
- "feature" or "add" → feature-template.md
- "enhance" or "improve" → enhancement-template.md
- "architecture" → architecture-template.md
- "infrastructure" or "ci/cd" → infrastructure-template.md
- default → task-template.md
</template_selection>

## <copilot_assignment_comment>
🤖 **GitHub Copilot Auto-Assigned**

**Complexity**: [X]/5 (Simple)
**Size**: [Y] (Small)

Copilot will begin work automatically within seconds.
Expected timeline: ~15 minutes for implementation.
</copilot_assignment_comment>

## <claude_assignment_comment>
🧠 **Requires Claude Code Agents**

**Complexity**: [X]/5
**Size**: [Y]

This task exceeds Copilot's capabilities.
Run `/work #[number]` when ready to begin implementation.
</claude_assignment_comment>

## Your Instructions

You need to create a GitHub issue for: "$ARGUMENTS"

### Step 1: Verify Prerequisites
Run this command to check you're on main branch:
!git branch --show-current

If not on main, tell the user to switch to main first.

### Step 2: Analyze the Request
Use the <complexity_assessment> instructions to analyze "$ARGUMENTS".
Store the determined complexity and size values.

### Step 3: Select and Fill Template
Use the <template_selection> instructions to pick the right template.
Fill the selected template with:
- Title from "$ARGUMENTS"
- Proper checkboxes (unchecked - they're work items)
- Metadata section with the assessed complexity and size

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
- Use mcp__github__add_issue_comment with the <copilot_assignment_comment> content

Otherwise:
- Add to your todo list using TodoWrite: "Issue #[number]: [title]"
- Use mcp__github__add_issue_comment with the <claude_assignment_comment> content

### Step 6: Report What You Did
Tell the user:
- Issue number created
- Who it was assigned to
- Link to the issue