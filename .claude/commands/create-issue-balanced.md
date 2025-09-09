---
allowed-tools: Read(*), Bash(*), mcp__github__create_issue(*), mcp__github__assign_copilot_to_issue(*), mcp__github__add_issue_comment(*), mcp__github__add_sub_issue(*), Task(*), TodoWrite(*)
description: Create GitHub issue with balanced approach - context in command, logic in Python
argument-hint: "[--feature|--bug|--enhancement|--task] issue title"
---

# Create Issue (Balanced Approach)

## Load Issue Templates
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

## <branch_check_instructions>
Ensure we're on main branch with latest changes:
1. Check current branch with git branch --show-current
2. If not on main, tell user to: git checkout main && git pull
3. If on main but behind, auto-pull latest changes
4. Only proceed when on main with latest
</branch_check_instructions>

## <complexity_rules>
Simple (Complexity 1-2, Size XS-S):
- Typos, renames, documentation updates
- Simple bug fixes with clear cause
- Adding basic endpoints or functions
- Updating dependencies
- Simple test additions

Complex (Complexity 3-5, Size M-XL):
- Architecture changes
- Security implementations
- Database migrations
- Performance optimizations
- Multi-component integrations
- Infrastructure changes
</complexity_rules>

## <copilot_assignment_rules>
Copilot can handle if ALL true:
- Complexity ≤ 2
- Size ∈ {XS, S}
- No security/architecture labels
- Clear, focused scope

Otherwise needs Claude Code agents
</copilot_assignment_rules>

## <sub_issue_templates>
Feature sub-issues:
1. Design & Architecture
2. Backend Implementation
3. Frontend Implementation
4. Testing & Validation
5. Documentation

Bug sub-issues:
1. Reproduce & Diagnose
2. Implement Fix
3. Add Regression Tests
4. Verify No Side Effects

Enhancement sub-issues:
1. Research Current State
2. Design Improvements
3. Implementation
4. Migration/Compatibility
</sub_issue_templates>

## Your Instructions

You need to create a GitHub issue for: "$ARGUMENTS"

### Step 1: Validate Prerequisites
Follow <branch_check_instructions> to ensure proper branch state.
Run: !git branch --show-current
Run: !git fetch origin main && git rev-parse main && git rev-parse origin/main

If not on main or behind, handle according to instructions.

### Step 2: Analyze Request with Python
Run the Python script to analyze complexity and check for existing issues:
!python3 scripts/commands/create-issue-analyzer.py "$ARGUMENTS"

This script will:
- Check for existing similar issues
- Analyze complexity based on title/description
- Determine issue type
- Return JSON with recommendations

Store the output for use in next steps.

### Step 3: Load and Fill Template
Based on the Python script's analysis:
1. Select the appropriate template from loaded files
2. Fill template with:
   - Title from "$ARGUMENTS"
   - Description based on analysis
   - Checkboxes from template (keep unchecked)
   - Metadata from analysis (complexity, size, priority)

Use the actual template content loaded via @ symbols, not generic content.

### Step 4: Create Main Issue
Use mcp__github__create_issue with:
- owner: vanman2024
- repo: multi-agent-claude-code
- title: "$ARGUMENTS"
- body: [filled template from Step 3]
- labels: [issue-type from analysis]

Store the created issue number.

### Step 5: Check for Sub-Issue Creation
If Python analysis suggests sub-issues (complex features/bugs):
1. Ask user: "Create sub-issues for better tracking? (recommended for complexity > 2)"
2. If yes, use <sub_issue_templates> to determine sub-issues
3. For each sub-issue:
   - Create with mcp__github__create_issue
   - Link with mcp__github__add_sub_issue using parent issue number

### Step 6: Handle Dependencies
If user mentions dependencies or blockers:
1. Ask: "Does this depend on other issues?"
2. If yes, add comment with mcp__github__add_issue_comment noting dependencies

### Step 7: Agent Assignment
Based on <copilot_assignment_rules> and analysis from Step 2:

If Copilot-eligible:
- Use mcp__github__assign_copilot_to_issue with issue number
- Add comment with mcp__github__add_issue_comment:
  "🤖 Auto-assigned to Copilot (Complexity: X, Size: Y)"
- Include specific Copilot instructions based on issue type

Else:
- Add to TodoWrite: "Issue #[number]: $ARGUMENTS"
- Add comment with mcp__github__add_issue_comment:
  "🧠 Requires Claude Code agents (Complexity: X, Size: Y)"
- Use Task tool if immediate work needed:
  - subagent_type: based on issue type
  - prompt: implementation requirements

### Step 8: Set Milestones and Priority
Run: !gh api repos/vanman2024/multi-agent-claude-code/milestones --jq '.[] | "\(.number): \(.title)"'

If milestones exist:
1. Show available milestones
2. Ask user to select or skip
3. If selected, use gh issue edit to assign

### Step 9: Final Summary
Report to user:
```
✅ Issue Created: #[number]
📋 Type: [type]
🏷️ Labels: [labels]
🤖 Assignment: [Copilot/Claude Code]
📊 Complexity: [X]/5, Size: [Y]
🔗 URL: https://github.com/vanman2024/multi-agent-claude-code/issues/[number]

[If sub-issues created, list them]
[If dependencies noted, mention them]
[Next steps based on assignment]
```

## Important Notes

This balanced approach:
- **Slash command handles**: Context loading, MCP operations, orchestration
- **Python script handles**: Complex analysis, existing issue checks, complexity calculation
- **Variables provide**: Reusable rules and templates
- **@ loading ensures**: All templates are available in context
- **MCP tools do**: Actual GitHub operations that Python can't