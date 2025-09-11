# Spec-Kit Commands Quick Reference

## Core Commands (In Order)

### 1. `/specify` - Create Functional Specification
**When**: Starting a new feature
**Focus**: WHAT and WHY (no tech stack)

```
/specify Build a photo organization app that allows users to:
- Create albums grouped by date
- Drag and drop to reorganize
- Preview photos in tile interface
- Store metadata locally
```

**Creates**: `specs/001-feature-name/spec.md`

### 2. `/plan` - Technical Implementation Plan
**When**: After specification is complete
**Focus**: HOW and WITH WHAT

```
/plan Use Vite with minimal libraries. 
Vanilla HTML, CSS, JavaScript.
SQLite for local metadata storage.
No cloud uploads.
```

**Creates**: 
- `specs/001-feature-name/plan.md`
- `specs/001-feature-name/research.md`
- `specs/001-feature-name/data-model.md`
- `specs/001-feature-name/contracts/`

### 3. `/tasks` - Generate Implementation Tasks
**When**: After plan is complete
**Focus**: Step-by-step breakdown

```
/tasks
```

**Creates**: `specs/001-feature-name/tasks.md` with T001-T050+ tasks

### 4. Implementation (NOT a slash command)
**When**: After tasks are generated
**Focus**: Building the solution

```
# Just tell your AI agent to implement:
"Implement the tasks from specs/001-feature-name/tasks.md"
"Start with infrastructure tasks T001-T010"
"Build the database schema first"
```

**Note**: No `/implement` command exists - just instruct the AI directly

## Helper Commands

### Check Prerequisites
```bash
./scripts/check-task-prerequisites.sh T001
```

### Create New Feature Branch
```bash
./scripts/create-new-feature.sh "feature-name"
```

### Update CLAUDE.md
```bash
./scripts/update-claude-md.sh
```

## Validation Prompts

### After `/specify`
```
Review the acceptance checklist and check off completed items
```

### After `/plan`
```
Audit the implementation plan for missing pieces
Cross-check for over-engineering
Validate against constitution.md
```

### Before Implementation
```
Verify all prerequisites are installed
Check that plan references implementation details
Ensure tasks are properly sequenced
```

## Common Refinements

### Add More Details to Spec
```
For each project, include 5-15 tasks randomly distributed
Ensure at least one task in each completion stage
```

### Research Specific Technologies
```
Research .NET Aspire specifics for our implementation
Focus on version compatibility and recent changes
```

### Simplify Over-Engineering
```
Review plan for unnecessary complexity
Remove components not explicitly requested
Follow YAGNI principle
```

## File Structure After Each Command

### After `/specify`
```
specs/001-feature/
└── spec.md
```

### After `/plan`
```
specs/001-feature/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    └── api-spec.json
```

### After `/tasks`
```
specs/001-feature/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── tasks.md          # NEW
└── contracts/
    └── api-spec.json
```

## Tips

1. **Be explicit** in specifications
2. **Don't mention tech** in `/specify`
3. **Research first** for new technologies
4. **Validate each phase** before proceeding
5. **Check constitution.md** for principles
6. **Create PRs** to track progress
7. **Test frequently** during implementation