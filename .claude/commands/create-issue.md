---
allowed-tools: mcp__github(*), Read(*), Bash(*), TodoWrite(*)
description: Create GitHub issues with proper templates and automatic agent assignment
argument-hint: [title] [description]
---

# Create Issue

## Context
- Current branch: !`git branch --show-current`
- Repository info: !`git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/' | tr '/' ' '`

## Your Task

When user runs `/create-issue $ARGUMENTS`, follow these steps:

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

Based on the type, read the template from `templates/local_dev/`:
- feature → @templates/local_dev/feature-template.md
- bug → @templates/local_dev/bug-template.md
- enhancement → @templates/local_dev/enhancement-template.md
- refactor → @templates/local_dev/refactor-template.md
- task → @templates/local_dev/task-template.md
- generic/other → @templates/local_dev/issue-template.md

### Step 3: Fill Template

Using the template structure:
1. Replace placeholders with actual content
2. Keep all checkboxes unchecked `[ ]` (they represent work to be done)
3. Add complexity and size metadata
4. Include acceptance criteria

### Step 4: Create GitHub Issue

Use `mcp__github__create_issue` to create the issue:

```javascript
const issueData = {
  owner: "{owner}",
  repo: "{repo}",
  title: title,
  body: filledTemplate + "\n\n**Complexity:** " + complexity + "\n**Size:** " + size,
  labels: [issueType], // 'feature', 'bug', 'enhancement', etc.
  assignees: ["@me"]
};

const issue = await mcp__github__create_issue(issueData);
```

### Step 5: Agent Assignment

Determine assignment based on BOTH complexity AND size:

```javascript
const isSmallAndSimple = (complexity <= 2) && (size === 'XS' || size === 'S');

if (isSmallAndSimple) {
  // Small AND simple - assign to Copilot
  await mcp__github__assign_copilot_to_issue({
    owner: owner,
    repo: repo,
    issueNumber: issue.number
  });
  
  await mcp__github__add_issue_comment({
    owner: owner,
    repo: repo,
    issue_number: issue.number,
    body: `🤖 **Assigned to GitHub Copilot** (Complexity: ${complexity}, Size: ${size})

This task is small and simple enough for Copilot to handle autonomously.

@copilot Please implement this following the specifications above.`
  });
} else {
  // Complex OR larger task - needs Claude Code
  const reason = complexity >= 3 
    ? `complexity level ${complexity}` 
    : `size ${size} requires coordination`;
    
  await mcp__github__add_issue_comment({
    owner: owner,
    repo: repo,
    issue_number: issue.number,
    body: `🧠 **Requires Claude Code/Agent Orchestration** (Complexity: ${complexity}, Size: ${size})

This task needs advanced handling due to ${reason}.

Next step: Run \`/build-issue ${issue.number}\` when ready to begin implementation.`
  });
}
```

### Step 6: Summary

Provide the user with:
```
✅ Issue Created: #${issue.number}
📋 Type: ${issueType}
🏷️ Labels: ${labels}
🤖 Assignment: ${isSmallAndSimple ? 'GitHub Copilot' : 'Claude Code Agents'}
🔗 URL: ${issue.html_url}

${isSmallAndSimple ? 
  'Copilot will begin work automatically.' : 
  'Run `/build-issue ' + issue.number + '` to start implementation.'}
```

## Important Notes

- GitHub Actions will automatically handle project board updates
- Feature branches are created automatically by workflows
- No manual project board management needed
- Let automation handle the plumbing, focus on the content