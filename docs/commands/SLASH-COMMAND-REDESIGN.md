# Slash Command Redesign Documentation

## Core Principle
**Slash commands are INSTRUCTION SETS for Claude Code or agents, NOT executable code.**

They tell Claude/agents:
- WHAT files to load for context
- WHAT to analyze or determine
- WHICH tools to use
- HOW to report results

## The New Pattern

### 1. File Loading Section
```markdown
## Load Context
- @file1.md
- @file2.json
- @templates/template.md
```

### 2. Variable/Prompt Sections
```markdown
## <variable_name>
Content that will be reused throughout the command.
This could be prompts, templates, or instructions.
</variable_name>

## <another_variable>
Another reusable block of content.
</another_variable>
```

### 3. Instructions Section
```markdown
## Your Instructions

You need to [do something] with "$ARGUMENTS"

### Step 1: Description
Use the <variable_name> to do something.
Run: !python3 scripts/command.py "$ARGUMENTS"

### Step 2: Another Step
Reference the <another_variable> content.
Use mcp__github__some_tool with the parameters.
```

## Commands Redesign Status

### ✅ Completed
- **create-issue-clean.md** - Full pattern implementation with templates and variables

### 🔄 In Progress
- **create-issue-v2.md** - Has @ loading, needs variable cleanup
- **create-issue-proper.md** - Has Task delegation, needs simplification

### ⏳ To Update
- **work.md** - Complex bash logic needs Python script extraction
- **deploy.md** - Needs deployment checklist variables
- **test.md** - Needs test suite selection logic
- **discussions.md** - Needs discussion template variables
- **wip.md** - Needs work-in-progress tracking variables
- **recover.md** - Needs recovery strategy variables

## Migration Strategy

### Phase 1: Extract Logic to Python Scripts
For each complex command:
1. Identify complex bash/logic sections
2. Create Python script in `scripts/commands/`
3. Replace logic with simple script call

### Phase 2: Add Context Loading
1. Identify files the command needs
2. Add `@` references at the top
3. Ensure templates are loaded if needed

### Phase 3: Create Variables
1. Find repeated content or complex prompts
2. Wrap in `<variable_name>` blocks
3. Reference variables in instructions

### Phase 4: Simplify Instructions
1. Remove code syntax (JavaScript, complex bash)
2. Make instructions declarative
3. Focus on WHAT, not HOW

## Example Transformation

### Before (Bad)
```markdown
### Step 1: Complex Logic
```bash
if [[ "$BRANCH" != "main" ]]; then
  echo "Error"
  exit 1
fi
```

### After (Good)
```markdown
## <branch_check>
Verify you're on the main branch before proceeding.
If not on main, tell the user to switch first.
</branch_check>

### Step 1: Check Branch
Run: !git branch --show-current
Follow the <branch_check> instructions based on output.
```

## Python Script Guidelines

### Structure
```python
#!/usr/bin/env python3
"""
Brief description of what the script does.
"""

def analyze_complexity(title: str) -> dict:
    """All complex logic goes here."""
    # Complex analysis
    return {"complexity": 2, "size": "S"}

def main():
    # Parse arguments
    # Run logic
    # Output results
    pass

if __name__ == "__main__":
    main()
```

### Integration
```markdown
### Step X: Run Analysis
Execute: !python3 scripts/commands/analyze.py "$ARGUMENTS"
Use the output to determine next steps.
```

## Testing Strategy

### Test Each Command Pattern
1. File loading with `@` - Does context load?
2. Variable references - Do `<variables>` work?
3. Python script execution - Do scripts run?
4. Tool usage - Do MCP tools execute?
5. Error handling - What happens on failure?

### Validation Checklist
- [ ] No code syntax in markdown
- [ ] All complex logic in Python scripts
- [ ] Files loaded with @ symbol
- [ ] Variables defined and referenced
- [ ] Instructions are declarative
- [ ] Tools described, not coded

## Benefits of New Pattern

1. **Clarity** - Instructions are readable and clear
2. **Reusability** - Variables can be reused
3. **Maintainability** - Logic in Python is easier to test
4. **Consistency** - Same pattern across all commands
5. **Debugging** - Easier to see what went wrong
6. **Parallel Execution** - Can run multiple agents simultaneously

## Next Steps

1. Complete migration of remaining commands
2. Test each command with real scenarios
3. Document any edge cases found
4. Create command generator tool
5. Train team on new patterns