---
allowed-tools: mcp__github(*), Read(*), Bash(*), TodoWrite(*)
description: Create GitHub issues using templates with automatic agent assignment
argument-hint: [type] [title] [options]
---

# Create Issue

## Context
- Issue templates: @/home/gotime2022/Projects/multi-agent-claude-code/templates/local_dev/issue-template.md
- Current branch: !`git branch --show-current`
- Repository info: !`git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/' | tr '/' ' '`

## Your Task

When user runs `/create-issue $ARGUMENTS`, follow these steps:

### Step 1: Parse and Analyze Input
Parse $ARGUMENTS for explicit type indicators or flags:
- Check for keywords: "bug", "feature", "refactor", "task", "enhancement", "fix"
- Look for flags: --assign-copilot, --complexity=[1-5], --size=[XS|S|M|L|XL]

**IF TYPE IS UNCLEAR (most common case):**
1. Analyze the provided text/snippet
2. **ASK THE USER** what type of issue this should be:
   ```
   Based on what you provided, what type of issue should this be?
   - bug (something is broken)
   - feature (new functionality) 
   - refactor (improve existing code)
   - task (simple work item)
   - generic (general issue)
   ```
3. Also ask for complexity and size if not provided:
   - Complexity (1-5): How complex is this?
   - Size (XS/S/M/L/XL): How much work is this?

### Step 2: Select and Load Template
**CRITICAL: You MUST read the actual template file and use its EXACT structure**

Based on issue type, read the appropriate template:
- feature → READ file: @/home/gotime2022/Projects/multi-agent-claude-code/templates/local_dev/feature-template.md
- bug → READ file: @/home/gotime2022/Projects/multi-agent-claude-code/templates/local_dev/bug-template.md
- refactor → READ file: @/home/gotime2022/Projects/multi-agent-claude-code/templates/local_dev/refactor-template.md
- task → READ file: @/home/gotime2022/Projects/multi-agent-claude-code/templates/local_dev/task-template.md
- generic → READ file: @/home/gotime2022/Projects/multi-agent-claude-code/templates/local_dev/issue-template.md

**IMPORTANT RULES:**
1. ALWAYS use the Read tool to load the template file
2. KEEP ALL CHECKBOXES UNCHECKED `[ ]` - they represent work to be done
3. FOLLOW THE TEMPLATE STRUCTURE EXACTLY - don't add extra sections
4. PRESERVE the template's markdown formatting

### Step 3: Gather Issue Details
Ask the user to fill in ONLY the sections that exist in the loaded template:
- Fill in placeholders like [What needs to be refactored]
- Select appropriate checkbox items (but keep them unchecked)
- Choose options like [Low/Medium/High] for risk level
- Add specific file paths where indicated

### Step 4: Create GitHub Issue
Use mcp__github__create_issue with:
```javascript
{
  owner: "[from git remote]",
  repo: "[from git remote]",
  title: "[provided title]",
  body: "[EXACT template structure with user's content filled in]",
  labels: "[labels from template bottom]",
  assignees: [] // Initially empty
}
```

**TEMPLATE COMPLIANCE CHECK:**
- ✅ All checkboxes start unchecked `[ ]`
- ✅ Template structure is preserved exactly
- ✅ Only template sections are included (no extras)
- ✅ Labels match those specified at template bottom

### Step 5: Auto-Assignment Logic
After creating the issue, check if it should be assigned to Copilot:

```javascript
const complexity = parseInt(flags.complexity) || 0;
const size = flags.size || 'M';
const isSmallAndSimple = (complexity <= 2) && (size === 'XS' || size === 'S');

if (flags.assignCopilot || isSmallAndSimple) {
  // Assign to Copilot for small, simple tasks
  await mcp__github__assign_copilot_to_issue({
    owner: "[owner]",
    repo: "[repo]",
    issueNumber: [created_issue_number]
  });
  console.log("✅ Assigned to GitHub Copilot (small & simple task)");
} else {
  console.log("📋 Issue created for Claude Code agents (complex or large task)");
}
```

### Step 6: Update Project Board (if applicable)
If a project board is configured, add the issue:
```javascript
// Get project board ID from repo settings
// Add issue to appropriate column based on type/priority
```

### Step 7: Create Branch (optional)
If user wants to start working immediately:
```bash
git checkout -b [type]/[issue-number]-[slugified-title]
git push -u origin [branch-name]
```

## Examples

### Create a simple task (auto-assigns to Copilot)
```
/create-issue task "Fix typo in README" --complexity=1 --size=XS
```

### Create a feature (stays with Claude Code)
```
/create-issue feature "Add user authentication" --complexity=4 --size=L
```

### Create a bug with explicit Copilot assignment
```
/create-issue bug "Button not responding" --assign-copilot
```

## Agent Assignment Rules Reminder

**Copilot gets tasks that are BOTH:**
- Complexity: 1-2 (simple logic)
- Size: XS or S (< 2 hours)

**Claude Code handles:**
- Complexity: 3-5 (complex logic)
- Size: M, L, XL (> 2 hours)
- Any security-sensitive tasks
- Architecture decisions

## Output Format

After successful creation:
```
✅ Created Issue #[number]: [title]
🏷️ Labels: [labels]
🤖 Assigned to: [Copilot/Claude Code]
🔗 URL: https://github.com/[owner]/[repo]/issues/[number]
🌿 Branch: [if created]
```