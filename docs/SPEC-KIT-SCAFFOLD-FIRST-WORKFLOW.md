# Spec-Kit Scaffold-First Workflow

## The Right Approach: Infrastructure First, Features Second

You're absolutely right - looking at spec-kit's output, it's creating the entire project scaffold first (Tasks T001-T010), then building features on top. This is the correct approach!

## The Scaffold-First Pattern

```
1. PROJECT SCAFFOLDING (Foundation)
   ├── Solution structure
   ├── Database setup
   ├── Core libraries
   ├── Test infrastructure
   ├── CI/CD pipeline
   └── Basic configuration

2. THEN ADD FEATURES (Built on scaffold)
   ├── Feature 1: Authentication
   ├── Feature 2: Task Management
   ├── Feature 3: Notifications
   └── Feature 4: UI Components
```

## Optimal Workflow

### Phase 1: Project Vision & Scaffold
```bash
# 1. Discovery and vision
/project-setup
# Creates PROJECT_PLAN.md

# 2. Generate complete project scaffold
specify scaffold "Taskify: Team productivity platform with .NET Aspire, Blazor, PostgreSQL"
# This creates the INFRASTRUCTURE spec:
# - specs/000-scaffold/
#   - spec.md (project structure)
#   - research.md (tech stack decisions)
#   - plan.md (architecture)
#   - tasks.md (T001-T010: setup tasks)
```

### Phase 2: Import and Build Scaffold
```bash
# 3. Import scaffold tasks to GitHub
/import-spec 000-scaffold
# Creates Issue #1: Project Infrastructure (10 tasks)

# 4. Build the foundation
/work #1
# This creates:
# - Solution structure
# - Database connections
# - Core libraries
# - Test projects
# - Docker setup
# - CI/CD workflows
```

### Phase 3: Progressive Feature Development
NOW that scaffold exists, add features:

```bash
# 5. Generate feature specs on existing scaffold
specify feature "Authentication" --on-scaffold
# Creates specs/001-authentication/

specify feature "Task Management" --on-scaffold
# Creates specs/002-task-management/

specify feature "Real-time Updates" --on-scaffold
# Creates specs/003-realtime/

# 6. Import features as needed
/import-spec 001-authentication
/work #2

/import-spec 002-task-management
/work #3
```

## Looking at Taskify's Structure

From the tasks.md you showed, spec-kit does exactly this:

### Infrastructure Tasks (T001-T010)
```
T001: Create .NET solution
T002: Create Aspire AppHost
T003: Create Blazor project
T004: Create API project
T005: Create class libraries
T006: Create test projects
T007: Add packages
T008: Configure Aspire
T009: Setup formatting
T010: Initialize git
```

### Then Feature Tasks (T011+)
```
T011-T023: API Contract Tests
T024-T028: Integration Tests
T029-T034: Entity Models
T035-T040: Database Layer
T041-T046: API Implementation
T047-T052: UI Components
```

## The Revised Command Structure

### `/project-scaffold`
Generate complete infrastructure spec:
```bash
/project-scaffold
# Interactive: asks about tech stack, database, deployment
# Generates: specs/000-scaffold/ with ~10-15 setup tasks
# Creates: Issue #1 for infrastructure
```

### `/feature-spec [name]`
Generate feature on existing scaffold:
```bash
/feature-spec "Authentication"
# Assumes scaffold exists
# Generates: specs/XXX-authentication/
# Reuses: Existing database, libraries, test infrastructure
```

### `/import-scaffold`
Special handling for scaffold:
```bash
/import-scaffold
# Creates high-priority issue
# Labels: infrastructure, blocking
# Must complete before features
```

## The Scaffold Specification

When running `specify scaffold`, it should include:

### 1. Project Structure
```yaml
solution:
  name: Taskify
  projects:
    - Taskify.AppHost (orchestration)
    - Taskify.Web (frontend)
    - Taskify.Api (backend)
    - Taskify.Core (domain)
    - Taskify.Data (persistence)
    - Taskify.Tests.Unit
    - Taskify.Tests.Integration
```

### 2. Infrastructure Components
```yaml
database: PostgreSQL
cache: Redis (optional)
messaging: SignalR
hosting: Docker + Aspire
ci_cd: GitHub Actions
monitoring: OpenTelemetry
```

### 3. Development Setup
```yaml
tools:
  - .editorconfig
  - Directory.Build.props
  - docker-compose.yml
  - .github/workflows/
conventions:
  - Code formatting rules
  - Naming conventions
  - Project references
```

## Example: Building Taskify Correctly

```bash
# STEP 1: Vision
/project-setup
> "Team task management with Kanban boards"
> Tech: .NET 8, Blazor, PostgreSQL
> Creates: PROJECT_PLAN.md

# STEP 2: Scaffold
specify scaffold "Taskify with .NET Aspire, Blazor Server, PostgreSQL"
# Creates: specs/000-scaffold/
# - Solution structure
# - Database setup
# - Test infrastructure
# - Docker configuration

# STEP 3: Build Foundation
/import-spec 000-scaffold
# Issue #1: Infrastructure Setup (10 tasks)

/work #1
# BUILDS THE ENTIRE PROJECT STRUCTURE

# STEP 4: Add Features (on existing scaffold)
specify feature "User Authentication with predefined users"
/import-spec 001-authentication
/work #2

specify feature "Kanban board with drag-drop"
/import-spec 002-kanban
/work #3

specify feature "Comments and notifications"
/import-spec 003-comments
/work #4
```

## Benefits of Scaffold-First

1. **Solid Foundation**: Everything builds on tested infrastructure
2. **No Rework**: Features use existing patterns/libraries
3. **Parallel Development**: Once scaffold done, features can be parallel
4. **Consistent Architecture**: All features follow same patterns
5. **Early Testing**: Test infrastructure ready from day 1
6. **Deployment Ready**: CI/CD pipeline from the start

## The Key Insight

Spec-kit is doing it right:
- **Tasks T001-T010**: Complete scaffold (no features yet!)
- **Tasks T011-T023**: Tests for features (TDD)
- **Tasks T024-T052**: Feature implementation

We should follow this pattern:
1. Scaffold completely first
2. Test infrastructure next
3. Features last

This is why those first 10 tasks are so important - they're the foundation everything else builds on!