---
allowed-tools: Bash(*), Read(*), Write(*), Glob(*), TodoWrite(*)
description: Wrapper for spec-kit's /plan command - adds technical implementation details to specs
argument-hint: [tech stack and implementation requirements]
---

# Plan - Technical Implementation

## Context
- Current directory: !`pwd`
- Current specs: !`ls -la specs/*/spec.md 2>/dev/null | head -5`

## Your Task

When user runs `/plan $ARGUMENTS`, add technical implementation details to existing specifications.

### Phase 1: Identify Current Spec

Find the latest spec that needs planning:
```bash
# Find spec directories without plan.md
for dir in specs/*/; do
  if [ -f "$dir/spec.md" ] && [ ! -f "$dir/plan.md" ]; then
    echo "Found spec needing plan: $dir"
    SPEC_DIR="$dir"
    break
  fi
done

if [ -z "$SPEC_DIR" ]; then
  echo "❌ No specifications found that need planning"
  echo "Run '/specify' first to create functional requirements"
  exit 1
fi
```

### Phase 2: Generate Technical Plan

NOW you specify the tech stack and implementation details:
```bash
# Run spec-kit's plan command
cd "$SPEC_DIR"
plan "$ARGUMENTS"
```

This creates:
- `research.md` - Technology decisions and clarifications
- `plan.md` - Technical architecture and phases
- `data-model.md` - Entity relationships and schemas
- `contracts/` - API specifications
- `quickstart.md` - How to run the application

### Phase 3: Validate Tech Stack

Check that the plan matches requirements:
1. Read `research.md` to verify tech choices
2. Ensure constitution compliance in `plan.md`
3. Verify data model completeness
4. Check API contracts match features

### Phase 4: Track Progress

Use TodoWrite:
```
- [x] Functional spec created
- [x] Technical plan generated
- [ ] Research complete
- [ ] Data model defined
- [ ] API contracts specified
- [ ] Ready for task generation
```

### Phase 5: Report Results

```
✅ Technical plan generated!

📁 Location: specs/001-feature-name/
📄 Files created:
  - plan.md (architecture)
  - research.md (tech decisions)
  - data-model.md (schemas)
  - contracts/api-spec.yaml
  - quickstart.md (usage)

Tech Stack:
[Parse from plan.md and show summary]

Next steps:
1. Review research.md for tech decisions
2. Validate constitution compliance
3. Run '/tasks' to generate implementation tasks
4. Use '/import-spec' to create GitHub issues
```

## Example Usage

```
User: /plan We are going to generate this using .NET Aspire, using Postgres as the database. The frontend should use Blazor server with drag-and-drop task boards, real-time updates.

You:
📂 Working on: specs/001-develop-taskify/

🔬 Researching tech stack...
- .NET Aspire for orchestration
- PostgreSQL for persistence
- Blazor Server for real-time UI
- SignalR for updates

📝 Generating technical plan...
[spec-kit output]

✅ Plan complete!
- Architecture: .NET Aspire with microservices
- Database: PostgreSQL with EF Core
- Frontend: Blazor Server
- Real-time: SignalR hubs
- Testing: xUnit + Testcontainers

Constitution check: ✅ Passed
- Using frameworks directly
- No unnecessary abstractions
- Clear separation of concerns

Next: Run '/tasks' to generate implementation tasks
```

## Important Notes

- This command REQUIRES an existing spec (from /specify)
- NOW is when you specify tech stack
- Research emerging tech if needed
- Validate against constitution
- Plan should be detailed enough for implementation