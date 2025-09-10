# Complete Spec-Kit Integration Guide

## The Unified Workflow: Spec-Kit + Multi-Agent Framework

We've successfully integrated spec-kit's specification-driven development with our multi-agent execution framework. Here's the complete workflow:

## Quick Start Commands

```bash
# 1. Create functional requirements (no tech stack)
/specify "Build a team task management system with Kanban boards..."

# 2. Add technical implementation details
/plan "Use .NET Aspire, Blazor Server, PostgreSQL..."

# 3. Generate implementation tasks
/tasks

# 4. Start building
/work #1
```

## The Complete Workflow

### Step 1: Project Vision (Our Framework)
```bash
/project-setup
```
- Interactive discovery process
- Creates PROJECT_PLAN.md
- Sets up GitHub repository
- Initializes project board

### Step 2: Functional Specification (Spec-Kit)
```bash
/specify "Detailed requirements without tech stack"
```
- Creates branch: `001-feature-name`
- Generates: `specs/001-feature/spec.md`
- Pure functional requirements
- User stories and workflows
- NO technical decisions yet

### Step 3: Technical Planning (Spec-Kit)
```bash
/plan "Tech stack and architecture decisions"
```
Generates in `specs/001-feature/`:
- `research.md` - Technology research
- `plan.md` - Architecture decisions
- `data-model.md` - Database schemas
- `contracts/` - API specifications
- `quickstart.md` - Usage guide

### Step 4: Task Generation (Spec-Kit)
```bash
/tasks
```
- Generates `tasks.md` with 40-60 tasks
- Creates GitHub issues automatically
- Groups tasks intelligently:
  - Issue #1: Infrastructure (T001-T010) [BLOCKING]
  - Issue #2: Tests (T011-T023)
  - Issue #3-6: Features (T024-T052)

### Step 5: Implementation (Our Framework)
```bash
/work #1  # Build infrastructure first!
/work #2  # Then tests
/work #3  # Then features
```
- Agents follow spec-kit's detailed tasks
- Automatic PR creation
- CI/CD validation
- Smart routing (Copilot for simple, Claude for complex)

## The Magic: Scaffold-First Pattern

Spec-kit generates tasks in the RIGHT order:

### Infrastructure First (T001-T010)
```
T001: Create solution structure
T002: Setup database
T003: Configure Docker
T004: Initialize packages
...
```
**MUST complete before features!**

### Then Tests (T011-T023)
```
T011: API contract tests
T012: Integration tests
T013: E2E test setup
...
```

### Finally Features (T024+)
```
T024: Entity models
T025: API controllers
T026: UI components
...
```

## Command Reference

### Our Framework Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/project-setup` | Initial discovery & vision | Very first step |
| `/work #N` | Implement GitHub issues | After tasks created |
| `/create-issue` | Manual issue creation | For non-spec work |
| `/deploy` | Deploy to production | After implementation |

### Spec-Kit Wrapper Commands

| Command | Purpose | Output |
|---------|---------|--------|
| `/specify` | Functional requirements | `spec.md` |
| `/plan` | Technical decisions | `plan.md`, `research.md` |
| `/tasks` | Implementation tasks | `tasks.md` + GitHub issues |

### Utility Commands

| Command | Purpose |
|---------|---------|
| `/import-spec` | Import existing spec-kit tasks |
| `/spec-status` | Show specification progress |
| `/copilot-review` | Request code review |

## Best Practices

### 1. Don't Skip Infrastructure
- Issue #1 is ALWAYS infrastructure
- Complete it before starting features
- This prevents rework and ensures consistency

### 2. Use the Right Granularity
Instead of one massive spec:
```bash
# ❌ Wrong
/specify "Build complete application with auth, tasks, UI, etc"
# → 100+ overwhelming tasks

# ✅ Right
/specify "Core task management"  # → 30 tasks
/specify "User authentication"   # → 20 tasks
/specify "Reporting dashboard"   # → 25 tasks
```

### 3. Validate at Each Step
```bash
/specify "Requirements"
# Review: Is it complete? Clear?

/plan "Tech stack"
# Review: Does it match requirements? Constitution compliant?

/tasks
# Review: Are tasks grouped well? Dependencies clear?
```

### 4. Follow Task Dependencies
```
Infrastructure → Tests → Features → Polish
     #1          #2      #3-5       #6
```

## Example: Building a Complete Application

### Initial Setup
```bash
# 1. Vision
/project-setup
> "Team productivity platform"
> Creates PROJECT_PLAN.md

# 2. Scaffold specification
/specify "Basic application scaffold with user system, projects, and tasks"
> Creates specs/001-scaffold/spec.md
```

### Technical Planning
```bash
# 3. Define architecture
/plan ".NET Aspire, Blazor Server, PostgreSQL, Docker"
> Creates complete technical design

# 4. Generate and import tasks
/tasks
> Creates 52 tasks → 6 GitHub issues
```

### Implementation
```bash
# 5. Build infrastructure (MUST BE FIRST!)
/work #1
> Completes T001-T010
> Solution structure ready

# 6. Add tests
/work #2
> Completes T011-T023
> Test infrastructure ready

# 7. Build features (can be parallel)
/work #3  # Authentication
/work #4  # Task management
/work #5  # UI components
```

### Deployment
```bash
# 8. Final polish and deploy
/work #6  # Documentation, performance
/deploy
> Production ready!
```

## Troubleshooting

### "spec-kit not initialized"
```bash
cd your-project
specify init --ai claude
```

### "No specs found"
```bash
# Check you're in the right directory
ls specs/
# Run /specify first
```

### "Tasks already exist"
```bash
# Check existing tasks
cat specs/*/tasks.md
# Or create new feature spec
/specify "New feature"
```

## The Power of Integration

By combining:
- **Spec-Kit**: Comprehensive specification engine
- **Multi-Agent**: Intelligent execution framework
- **GitHub**: Issue tracking and collaboration
- **AI Agents**: Automated implementation

We get:
- ✅ Clear specifications before coding
- ✅ Proper architecture from day 1
- ✅ Automatic task distribution
- ✅ Intelligent agent routing
- ✅ Complete traceability
- ✅ No rework from poor planning

## Next Steps

1. Install spec-kit if not already:
   ```bash
   npm install -g @github/spec-kit
   ```

2. Initialize in your project:
   ```bash
   specify init --ai claude
   ```

3. Start building:
   ```bash
   /specify "Your application requirements"
   /plan "Your tech stack"
   /tasks
   /work #1
   ```

The future of development: AI-driven, specification-first, automatically executed! 🚀