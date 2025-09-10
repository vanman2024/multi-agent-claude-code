# Spec-Kit Hierarchical Workflow

## The Spec-Kit Generation Hierarchy

Based on analyzing spec-kit's actual output, here's the hierarchical flow it follows:

```
1. SPEC.MD (High-level vision)
   ↓
2. RESEARCH.MD (Clarifications & decisions)
   ↓
3. PLAN.MD (Technical architecture)
   ↓
4. DATA-MODEL.MD + CONTRACTS/ (Design artifacts)
   ↓
5. TASKS.MD (52 granular implementation tasks)
```

Each level builds on the previous, creating increasingly detailed specifications.

## Our Integrated Workflow

### Step 1: High-Level Vision (Like PROJECT_PLAN.md)
```bash
# Use our discovery process first
/project-setup
# Creates PROJECT_PLAN.md with vision

# OR if you already know what you want:
specify "Build a task management system for teams"
# Creates initial spec.md
```

### Step 2: Feature Breakdown
Instead of generating ALL 52 tasks at once, break into features:

```bash
# Generate specs for individual features
specify "Authentication system with JWT and role-based access"
specify "Kanban board with drag-drop functionality"
specify "Real-time notifications using SignalR"
```

Each generates its own spec hierarchy:
- `specs/001-authentication/`
- `specs/002-kanban-board/`
- `specs/003-notifications/`

### Step 3: Research & Clarification Phase
For each feature, spec-kit generates:
- **research.md** - Technology decisions, clarifications
- **data-model.md** - Entity relationships
- **contracts/** - API specifications

### Step 4: Task Generation
Only after research/design, generate tasks:
```bash
specify tasks 001-authentication
# Generates ~8-10 tasks just for auth
```

### Step 5: Import to GitHub
```bash
/import-from-spec-kit 001-authentication
# Creates GitHub issue with 8-10 tasks as checkboxes
```

## The Optimal Flow

### Phase 1: Discovery & Vision
```bash
# Start with our interactive discovery
/project-setup

# This creates:
# - PROJECT_PLAN.md (high-level vision)
# - GitHub repo structure
# - Project board
```

### Phase 2: Feature Specification
```bash
# For each major feature in PROJECT_PLAN:
specify "Feature: User Authentication"
# Creates: specs/001-user-authentication/
# - spec.md (what)
# - research.md (how)
# - plan.md (architecture)

specify "Feature: Task Management"
# Creates: specs/002-task-management/
# - spec.md
# - research.md
# - plan.md
```

### Phase 3: Progressive Task Generation
```bash
# Generate tasks only when ready to implement
specify tasks 001-user-authentication
# Creates: specs/001-user-authentication/tasks.md
# ~10 tasks

# Import to GitHub
/import-from-spec-kit 001-user-authentication
# Creates: Issue #1 with 10 task checkboxes
```

### Phase 4: Implementation
```bash
# Work on the imported issue
/work #1
# Follows spec-kit's detailed tasks
```

## Key Insight: Granular Generation

Instead of:
```bash
specify "Build complete Taskify application"
# → 52 tasks, overwhelming
```

Do this:
```bash
specify "Authentication" # → 8 tasks
specify "Projects"       # → 6 tasks
specify "Tasks"          # → 12 tasks
specify "Comments"       # → 8 tasks
specify "UI"            # → 10 tasks
specify "Testing"       # → 8 tasks
```

## The Hybrid Commands We Need

### 1. `/spec-feature [name]`
Wraps spec-kit to generate single feature:
```bash
/spec-feature "User Authentication"
# Runs: specify "User Authentication"
# Creates: specs/XXX-user-authentication/
# But NOT tasks yet
```

### 2. `/spec-tasks [feature-id]`
Generate tasks for ready features:
```bash
/spec-tasks 001-user-authentication
# Runs: specify tasks 001-user-authentication
# Creates: tasks.md with ~10 tasks
```

### 3. `/import-spec [feature-id]`
Import single feature to GitHub:
```bash
/import-spec 001-user-authentication
# Creates single GitHub issue
# With ~10 task checkboxes
```

### 4. `/spec-status`
Show spec generation status:
```bash
/spec-status
# Output:
✅ 001-authentication (spec, research, plan, tasks) → Issue #1
✅ 002-projects (spec, research, plan, tasks) → Issue #2
🔄 003-tasks (spec, research, plan) → Ready for tasks
📝 004-comments (spec) → Needs research
⏳ 005-ui → Not started
```

## Spec-Kit File Structure Explained

```
specs/
└── 001-develop-taskify-a/
    ├── spec.md           # WHAT: Feature requirements
    ├── research.md       # WHY: Tech decisions, clarifications
    ├── plan.md          # HOW: Architecture, phases
    ├── data-model.md    # SCHEMA: Entities, relationships
    ├── contracts/       # API: OpenAPI specs
    │   └── api-spec.yaml
    ├── quickstart.md    # USAGE: How to run/test
    └── tasks.md         # DO: Numbered implementation tasks
```

## Integration Points

### Our PROJECT_PLAN.md → spec-kit's spec.md
```markdown
# PROJECT_PLAN.md (our format)
## Core Features
- User Authentication
- Task Management
- Real-time Updates

# Becomes multiple spec.md files:
specs/001-authentication/spec.md
specs/002-task-management/spec.md
specs/003-realtime/spec.md
```

### Spec-kit tasks.md → GitHub Issues
```markdown
# tasks.md (52 tasks)
T001-T010: Setup
T011-T023: Tests
T024-T040: Implementation

# Becomes GitHub issues:
Issue #1: Setup & Infrastructure (T001-T010)
Issue #2: Test Suite (T011-T023)
Issue #3: Core Implementation (T024-T040)
```

## Benefits of This Approach

1. **Not Overwhelming**: 8-10 tasks per feature vs 52 at once
2. **Progressive Detail**: Start high-level, add detail as needed
3. **Flexible**: Can change course without regenerating everything
4. **Traceable**: Every task traces back to spec
5. **Parallel Work**: Different people can spec different features
6. **Quality Gates**: Research before plan, plan before tasks

## Example: Building Taskify the Right Way

```bash
# 1. Discovery
/project-setup
> "Task management for teams"
> Creates PROJECT_PLAN.md

# 2. Break into features (from PROJECT_PLAN)
/spec-feature "User Management"
/spec-feature "Project Organization"
/spec-feature "Task Workflow"
/spec-feature "Team Collaboration"

# 3. Progressive implementation
/spec-tasks 001-user-management
/import-spec 001-user-management
/work #1

# 4. Continue with next feature
/spec-tasks 002-project-organization
/import-spec 002-project-organization
/work #2
```

This way you get spec-kit's comprehensive planning WITHOUT the overwhelming 52-task monster!