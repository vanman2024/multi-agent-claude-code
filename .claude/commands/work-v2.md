---
allowed-tools: Bash(*), Read(*), Write(*), Edit(*), TodoWrite(*), Task(*)
description: Start work on an issue with automatic setup
argument-hint: [#issue-number | --auto]
---

# Work V2

## <work_context>
Set up the development environment for working on an issue:
- Create feature branch
- Create draft PR
- Set up todo tracking
</work_context>

## Your Task

### Step 1: Start Work
Run: !python3 scripts/commands/work-on-issue.py $ARGUMENTS

### Step 2: Add to Todo List
Extract issue number and title from output.
Add to TodoWrite: "Issue #[number]: [title]"

### Step 3: Analyze Implementation Needs
Use @agent-analyzer agent to:
- Read issue description
- Identify files to modify
- Plan implementation approach

### Step 4: Begin Implementation
Based on complexity:
- Simple (1-2): Direct implementation
- Complex (3-5): Use Task tool with specialized agents