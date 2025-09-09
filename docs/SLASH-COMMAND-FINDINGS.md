# Slash Command Pattern Findings

## CRITICAL UNDERSTANDING: Slash Commands Are Instructions, Not Code!

**Slash commands are PROMPTS that tell Claude Code or agents WHAT to do.**
They are NOT the execution itself. They're instructions for:
- Running Python/bash scripts
- Calling sub-agents via Task tool  
- Using MCP tools
- Following a workflow

Think of them as **recipes** or **instruction manuals** that Claude Code reads and follows.

## Current Investigation (2025-09-09)

### Key Discovery from Screenshot
The screenshot shows advanced slash command patterns that we haven't been using:

1. **File Loading with `@` Symbol**
   - Files are loaded into context BEFORE execution
   - Example: `- @templates/local_dev/feature-template.md`
   - This ensures the content is available for filling/using

2. **Variable/Prompt Sections with `<variable_name>`**
   - Reusable prompts stored in variables
   - Example: `<scrape_loop_prompt>` contains instructions
   - These get passed to agents via Task tool

3. **Agent Delegation Pattern**
   - Use `@agent-name` to reference specific agents
   - Task tool runs agents in PARALLEL, not sequential
   - Much more efficient than sequential bash commands

### The Problem We Had

Our original slash commands had TOO MUCH inline logic:
```markdown
# BAD - Complex bash logic in the command
if [[ "$CURRENT_BRANCH" != "main" ]]; then
  echo "ERROR..."
  exit 1
fi
```

### The Solution

1. **Move logic to Python scripts**
2. **Use `@` to load context files**
3. **Keep slash commands simple - just orchestration**

## GitHub Operations: gh CLI vs MCP

### Current Confusion
- Anthropic previously recommended `gh` CLI
- But that was BEFORE MCP GitHub server existed
- Now we have both options

### When to Use What

#### Use `gh` CLI for:
```bash
# Quick queries and checks
!gh issue list --state open
!gh pr status
!gh repo view

# When you need formatted output
!gh issue list --json number,title --jq '.[]'

# Workflow operations
!gh workflow run
!gh run list
```

#### Use MCP GitHub tools for:
```markdown
# Creating/modifying content
mcp__github__create_issue(...)
mcp__github__assign_copilot_to_issue(...)
mcp__github__add_issue_comment(...)

# Complex operations with structured data
mcp__github__create_pull_request(...)
mcp__github__merge_pull_request(...)
```

### Why the JavaScript Syntax Appeared

**MISTAKE**: I put JavaScript-style code in the markdown:
```javascript
// This shouldn't be in slash commands!
mcp__github__assign_copilot_to_issue({
  owner: "vanman2024",
  repo: "multi-agent-claude-code",
  issueNumber: [created_issue_number]
})
```

**CORRECT**: Slash commands should just describe the action:
```markdown
Use mcp__github__assign_copilot_to_issue with:
- owner: vanman2024
- repo: multi-agent-claude-code  
- issueNumber: [the created issue number]
```

The actual tool calling is handled by Claude Code when executing the command, not written literally in the markdown.

## Proper Slash Command Structure

### Template Pattern
```markdown
---
allowed-tools: Read(*), mcp__github(*), Task(*), Bash(*)
description: Brief description
argument-hint: what user should provide
---

# Command Name

## Load Context Files
- @file1.md
- @file2.json
- @directory/file.ts

## <variable_name>
Content that will be reused
</variable_name>

## Your Task

### Step 1: Simple Description
Action to take (not HOW, just WHAT)

### Step 2: Use Tools
Describe tool usage, don't write code
```

## Python Scripts vs Bash

### When to Use Python Scripts
- Complex logic (if/else, loops, parsing)
- API interactions
- Data transformation
- Error handling
- State management

### When to Use Bash
- Simple commands (`git status`, `ls`)
- Piping operations
- Quick file operations
- System checks

### Integration Pattern
```markdown
# In slash command - SIMPLE
Run: !python3 scripts/commands/complex-logic.py "$ARGUMENTS"

# In Python script - COMPLEX LOGIC
def analyze_and_decide():
    # All the complex logic here
    pass
```

## Current Status of Our Commands

### Commands to Refactor
1. **create-issue.md** - Original, too complex with inline bash
2. **create-issue-v2.md** - Better, uses @ loading
3. **create-issue-proper.md** - Good pattern with Task delegation
4. **create-issue-final.md** - Best version, but needs JavaScript removal

### Next Steps
1. Remove JavaScript syntax from commands
2. Ensure all use @ file loading
3. Move complex logic to Python scripts
4. Test parallel agent execution

## Best Practices Going Forward

### DO:
✅ Load files with `@` symbol
✅ Use `<variables>` for reusable content  
✅ Delegate to agents via Task tool
✅ Keep commands simple and declarative
✅ Use Python for complex logic

### DON'T:
❌ Put programming code in slash commands
❌ Use complex bash logic inline
❌ Run sequential operations when parallel is possible
❌ Mix gh CLI and MCP for same operation
❌ Forget to load context before using it

## Questions Still Open

1. **Should we prefer gh CLI or MCP for all operations?**
   - Current thinking: Use MCP for create/modify, gh for query
   
2. **How do we handle error states in slash commands?**
   - Need to test what happens when operations fail
   
3. **Can we call Python scripts with complex parameters?**
   - Need to test parameter passing patterns

4. **How does parallel Task execution actually work?**
   - Need to test with real multi-agent scenarios