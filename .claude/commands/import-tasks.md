---
allowed-tools: Bash(*), Read(*), TodoWrite(*)
description: Import spec-kit tasks into Claude Code's TodoWrite for execution
argument-hint: [optional: spec-directory-name]
---

# Import Spec-Kit Tasks to TodoWrite

## Context
- Current directory: !`pwd`
- Available specs: !`ls -d specs/*/ 2>/dev/null | head -5`

## Your Task

When user runs `/import-tasks $ARGUMENTS`, import spec-kit generated tasks into your TodoWrite tool for execution.

### Phase 1: Find Tasks File

```bash
# If specific spec provided
if [ -n "$ARGUMENTS" ]; then
  TASKS_FILE="specs/$ARGUMENTS/tasks.md"
else
  # Find most recent tasks.md
  TASKS_FILE=$(ls -t specs/*/tasks.md 2>/dev/null | head -1)
fi

if [ ! -f "$TASKS_FILE" ]; then
  echo "❌ No tasks.md found"
  echo "Run spec-kit's 'tasks' command first"
  exit 1
fi

echo "📋 Importing from: $TASKS_FILE"
```

### Phase 2: Read and Parse Tasks

Read the tasks.md file and extract all tasks in format:
- `T001-T010`: Infrastructure (PRIORITY!)
- `T011-T023`: Tests
- `T024+`: Features

Convert each to TodoWrite format:
```javascript
{
  content: "T001: Create solution structure",
  status: "pending",
  activeForm: "Creating solution structure"
}
```

### Phase 3: Load into TodoWrite

Use TodoWrite to load ALL tasks at once:
```javascript
TodoWrite({
  todos: [
    // Infrastructure - mark first as in_progress
    {content: "T001: Create .NET solution", status: "in_progress", activeForm: "Creating .NET solution"},
    {content: "T002: Setup database", status: "pending", activeForm: "Setting up database"},
    // ... all other tasks
  ]
})
```

### Phase 4: Execution Strategy

After importing, inform user of execution order:
```
✅ Imported 52 tasks from spec-kit!

Execution Strategy:
1. Infrastructure (T001-T010) - Starting now!
   🏗️ MUST complete before features
   
2. Tests (T011-T023) - Next priority
   🧪 TDD approach
   
3. Features (T024-T052) - After infrastructure
   ✨ Can parallelize some tasks

Starting with T001...
```

Then immediately begin executing T001!

## Example Execution

```
User: /import-tasks

You: 
📋 Reading spec-kit tasks from specs/001-taskify/tasks.md...

Found 52 tasks:
- Infrastructure: 10 tasks
- Tests: 13 tasks  
- Implementation: 29 tasks

Loading into TodoWrite...
[Use TodoWrite tool to load all tasks]

✅ All tasks imported! 

🚀 Starting execution with infrastructure:
T001: Create .NET solution...
[Begin executing using Bash and other tools]
```

## Smart Task Ordering

When loading into TodoWrite, ensure:
1. **T001 is marked "in_progress"** - start immediately
2. **T002-T010 marked "pending"** - infrastructure queue
3. **T011+ marked "pending"** - wait for infrastructure

## Execution Tips

For each task:
1. Update TodoWrite status to "in_progress"
2. Execute using appropriate tools (Bash, Write, etc.)
3. Mark "completed" when done
4. Move to next task

Infrastructure tasks typically need:
- `dotnet new` commands
- Package installations
- Git initialization
- Docker setup

## Important Notes

- ALWAYS complete T001-T010 first (infrastructure)
- These tasks come from spec-kit's generation
- Claude Code executes them using its tools
- Track progress in TodoWrite throughout
- If task fails, note it and continue or fix