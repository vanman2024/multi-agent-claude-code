---
allowed-tools: Bash(*), Read(*), Write(*), Glob(*), TodoWrite(*), mcp__github__create_issue(*)
description: Wrapper for spec-kit's /tasks command - generates implementation tasks from plan
argument-hint: [optional: specific feature or "all"]
---

# Tasks - Generate Implementation Tasks

## Context
- Current directory: !`pwd`
- Plans ready: !`ls -la specs/*/plan.md 2>/dev/null | wc -l`

## Your Task

When user runs `/tasks $ARGUMENTS`, generate implementation tasks from technical plans.

### Phase 1: Identify Target Spec

```bash
# Find spec with plan but no tasks
for dir in specs/*/; do
  if [ -f "$dir/plan.md" ] && [ ! -f "$dir/tasks.md" ]; then
    echo "Found plan ready for tasks: $dir"
    SPEC_DIR="$dir"
    break
  fi
done

if [ -z "$SPEC_DIR" ]; then
  echo "❌ No plans found that need task generation"
  echo "Run '/plan' first to create technical details"
  exit 1
fi
```

### Phase 2: Generate Tasks

```bash
# Run spec-kit's tasks command
cd "$SPEC_DIR"
tasks
```

This generates `tasks.md` with numbered tasks like:
- T001-T010: Infrastructure/Scaffold
- T011-T023: Tests (TDD)
- T024-T040: Core Implementation
- T041-T052: UI/Features

### Phase 3: Analyze Task Structure

Read the generated tasks.md and identify:
1. **Scaffold tasks** (usually T001-T010)
2. **Test tasks** (TDD requirements)
3. **Feature tasks** (grouped by area)
4. **Polish tasks** (documentation, performance)

### Phase 4: Create GitHub Issues

Group tasks intelligently and create issues:

```javascript
// Infrastructure Issue (MUST be first)
if (has_scaffold_tasks) {
  mcp__github__create_issue({
    title: "Infrastructure: Project Scaffold",
    body: "## Priority: BLOCKING\n\nTasks T001-T010...",
    labels: ["infrastructure", "blocking", "size:L"],
    milestone: "Sprint 1"
  });
}

// Feature Issues (grouped)
for (each feature_group) {
  mcp__github__create_issue({
    title: `Feature: ${feature_name}`,
    body: `Implements tasks T${start}-T${end}...`,
    labels: ["feature", complexity_label, size_label],
    milestone: "Sprint 2"
  });
}
```

### Phase 5: Track Task Mapping

Use TodoWrite to create mapping:
```
Task Mapping:
- Issue #1: Infrastructure (T001-T010) [BLOCKING]
- Issue #2: Test Suite (T011-T023)
- Issue #3: Authentication (T024-T031)
- Issue #4: Task Management (T032-T040)
- Issue #5: UI Components (T041-T052)
```

### Phase 6: Report Results

```
✅ Tasks generated and imported!

📄 Tasks file: specs/001-feature/tasks.md
📊 Total tasks: 52

GitHub Issues Created:
🔧 #1: Infrastructure Setup (10 tasks) - BLOCKING
🧪 #2: Test Suite (13 tasks)
✨ #3: Core Features (18 tasks)
🎨 #4: UI Implementation (11 tasks)

Implementation Order:
1. Start with #1 (infrastructure) - MUST complete first
2. Then #2 (tests) for TDD approach
3. Parallel work on #3 and #4

Next: Run '/work #1' to build infrastructure
```

## Intelligent Grouping Rules

### Scaffold Tasks (T001-T010)
- ALWAYS create as Issue #1
- Label: infrastructure, blocking
- Priority: HIGHEST
- Must complete before features

### Test Tasks
- Group by test type (unit, integration, e2e)
- Can run parallel to features
- Label: testing

### Feature Tasks
- Group by functional area
- 8-12 tasks per issue ideal
- Label by complexity

### Example Grouping

From 52 tasks:
```
Issue #1: Infrastructure (T001-T010)
- Create solution
- Setup database
- Configure Docker
- Initialize git

Issue #2: API Tests (T011-T023)
- Contract tests
- Integration tests

Issue #3: Data Layer (T024-T034)
- Entity models
- Migrations
- Repositories

Issue #4: API Implementation (T035-T045)
- Controllers
- SignalR hubs
- Middleware

Issue #5: UI Components (T046-T052)
- Blazor components
- Drag-drop
- Real-time updates
```

## Important Notes

- Infrastructure MUST be Issue #1 and completed first
- Group tasks logically (8-12 per issue)
- Respect dependencies between tasks
- Use appropriate labels for routing (Copilot vs Claude)
- Create clear implementation order