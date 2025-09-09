---
allowed-tools: Read(*), mcp__github__create_issue(*), mcp__github__assign_copilot_to_issue(*), mcp__github__add_issue_comment(*), Task(*), TodoWrite(*), Bash(*)
description: Create GitHub issue with template loading and intelligent assignment
argument-hint: "[--feature|--bug|--enhancement|--task] issue title"
---

# Create Issue (Final)

## Load All Issue Templates
- @templates/local_dev/feature-template.md
- @templates/local_dev/bug-template.md
- @templates/local_dev/enhancement-template.md
- @templates/local_dev/task-template.md
- @templates/local_dev/architecture-template.md
- @templates/local_dev/infrastructure-template.md

## Load Project Context
- @CLAUDE.md
- @package.json
- @.github/COPILOT-WORKFLOW.md

## <complexity_assessment>
Analyze "$ARGUMENTS" to determine:
1. Issue type from title keywords or flags
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

## Your Task

### Step 1: Ensure on Main Branch
Run: !git branch --show-current
If not on main:
- Tell user to run: `git checkout main && git pull`
- Exit

### Step 2: Analyze Request
Use the <complexity_assessment> to evaluate "$ARGUMENTS"

### Step 3: Select and Fill Template
1. Choose template based on <template_selection>
2. Fill in the template placeholders:
   - Replace [Feature Name] with title
   - Fill acceptance criteria based on description
   - Set metadata section with assessed values
   - Keep all checkboxes unchecked (they're work items)

### Step 4: Create GitHub Issue
Use mcp__github__create_issue:
```json
{
  "owner": "vanman2024",
  "repo": "multi-agent-claude-code",
  "title": "$ARGUMENTS",
  "body": "[filled template content]",
  "labels": ["[issue-type]"]
}
```

### Step 5: Auto-Assign Based on Complexity
If complexity ≤ 2 AND size ∈ {XS, S}:
- Use mcp__github__assign_copilot_to_issue with the created issue number
- Add comment via mcp__github__add_issue_comment explaining Copilot assignment
- Comment should include: "🤖 Auto-assigned to GitHub Copilot, Complexity: [X]/5, Size: [Y]"

Otherwise (complex or large):
- Add to TodoWrite: "Issue #[number]: $ARGUMENTS"  
- Add comment via mcp__github__add_issue_comment explaining Claude Code requirement
- Comment should include: "🧠 Requires Claude Code agents, Run /work #[number] to begin"

### Step 6: Report Success
```
✅ Created Issue #[number]
📋 Type: [issue-type]
🤖 Assignment: [Copilot/Claude Code]
🔗 https://github.com/vanman2024/multi-agent-claude-code/issues/[number]
```