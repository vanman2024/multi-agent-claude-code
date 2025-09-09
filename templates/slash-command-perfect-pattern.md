---
allowed-tools: Read(*), Task(*), Bash(*), mcp__github(*)
description: Example showing the perfect slash command pattern
argument-hint: "what the user should provide"
---

# Example Perfect Pattern

## Load Context
- @README.md
- @package.json
- @templates/local_dev/feature-template.md

## <analysis_instructions>
Look at the loaded files and the user input "$ARGUMENTS".
Determine what type of work this is and what's needed.
</analysis_instructions>

## <implementation_instructions>
Based on the analysis, implement the solution by:
1. Creating necessary files
2. Following existing patterns from the loaded context
3. Running tests if they exist
</implementation_instructions>

## Your Task

You are being instructed to:

### Step 1: Analyze the Request
Read the loaded context files and understand what "$ARGUMENTS" means in this project.

### Step 2: Run Analysis Script
Execute this Python script to analyze complexity:
!python3 scripts/commands/analyze-request.py "$ARGUMENTS"

### Step 3: Delegate to Specialized Agent
Based on the analysis, use the Task tool to delegate:
- If security-related: Use Task with subagent_type="security-auth-compliance"
- If architecture: Use Task with subagent_type="system-architect"  
- If testing: Use Task with subagent_type="backend-tester"
- Otherwise: Use Task with subagent_type="general-purpose"

Pass the <implementation_instructions> to the chosen agent.

### Step 4: Create GitHub Issue
After analysis completes, create an issue using mcp__github__create_issue with:
- The title from "$ARGUMENTS"
- The body from the filled template
- Appropriate labels based on type

### Step 5: Report Results
Show what was created and what the next steps are.

---

## Key Points About This Pattern

This slash command is telling YOU (Claude Code) or an agent:
1. WHAT files to read for context
2. WHAT script to run for analysis  
3. WHICH agent to delegate to
4. WHAT GitHub operation to perform
5. HOW to report results

It's NOT executing code directly - it's instructing you to execute it.