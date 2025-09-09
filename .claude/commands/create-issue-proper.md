---
allowed-tools: Read(*), mcp__github__create_issue(*), mcp__github__assign_copilot_to_issue(*), Task(*), TodoWrite(*)
description: Create issue with proper context loading and agent delegation
argument-hint: "issue title"
---

# Create Issue (Proper)

## Load Context Files
Read these files to understand the project structure:
- @README.md
- @CLAUDE.md  
- @package.json
- @.github/COPILOT-WORKFLOW.md

## <issue_analysis_prompt>
Based on the loaded context and the user's request: "$ARGUMENTS"

Analyze and determine:
1. Issue type (feature/bug/enhancement/task)
2. Complexity (1-5 scale)
3. Size (XS/S/M/L/XL)
4. Which files would need modification
5. Dependencies and considerations
6. Whether Copilot can handle it (complexity ≤2 AND size ≤S)
</issue_analysis_prompt>

## <issue_template>
Create a properly structured issue with:
- Clear description
- Acceptance criteria with checkboxes
- Testing requirements
- Metadata section with complexity/size/priority
</issue_template>

## Your Task

### Step 1: Load Project Context
Read the context files listed above to understand the codebase.

### Step 2: Analyze Issue Requirements  
Use the Task tool with agent-type="general-purpose" and prompt=<issue_analysis_prompt>

### Step 3: Create Issue Template
Based on the analysis, create the issue body using <issue_template>

### Step 4: Create GitHub Issue
Use mcp__github__create_issue with the analyzed details

### Step 5: Auto-Assign If Simple
If complexity ≤2 AND size ≤S:
- Use mcp__github__assign_copilot_to_issue
- Add to TodoWrite for tracking

### Step 6: Report Results
Show issue number and URL