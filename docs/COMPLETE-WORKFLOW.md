# Complete Workflow: Spec-Kit + Multi-Agent Framework

## The Correct Order of Operations

### Step 1: Initialize Spec-Kit Scaffolding
```bash
# Create spec-kit's own scaffolding (NOT project scaffolding)
cd ~/Projects
uvx --from git+https://github.com/github/spec-kit.git specify init taskify
cd taskify

# This creates:
# - memory/constitution.md (spec-kit rules)
# - scripts/ (spec-kit's helper scripts)
# - templates/ (spec-kit's templates)
# - .claude/ (Claude Code configuration)
```

### Step 2: Create Project Vision
```bash
# Run our project-setup to create high-level vision
/project-setup

# Interactive discovery:
# - What are you building?
# - Who are the users?
# - What's the business model?
# - What makes it unique?

# Creates: docs/PROJECT_PLAN.md
```

### Step 3: Generate Functional Specification
```bash
# Pass PROJECT_PLAN requirements to spec-kit
/specify "Build Taskify as described in PROJECT_PLAN.md: 
         Team productivity platform with Kanban boards,
         5 predefined users (1 PM, 4 engineers),
         3 sample projects, drag-drop between columns,
         commenting system, visual task highlighting.
         
         Include full infrastructure:
         - CI/CD pipeline with GitHub Actions
         - Docker containerization
         - Comprehensive testing (unit, integration, E2E)
         - Database migrations and seeding
         - Real-time updates
         - Environment configurations
         - Monitoring and error tracking"

# Creates: specs/001-taskify/spec.md
# Creates: New branch 001-taskify
```

### Step 4: Add Technical Details
```bash
# Specify the tech stack
/plan "React with TypeScript, Node.js/Express backend,
       PostgreSQL database, WebSockets for real-time,
       Docker for containerization, GitHub Actions CI/CD,
       Jest and Playwright for testing, Vercel deployment"

# Creates: 
# - specs/001-taskify/plan.md
# - specs/001-taskify/research.md
# - specs/001-taskify/data-model.md
# - specs/001-taskify/contracts/
```

### Step 5: Generate Implementation Tasks
```bash
# Generate all tasks including project scaffolding
/tasks

# Creates: specs/001-taskify/tasks.md
# With tasks like:
# T001-T010: PROJECT SCAFFOLDING (create actual project structure)
# T011-T025: Testing infrastructure
# T026-T040: Core implementation
# T041-T052: Features
```

### Step 6: Import Tasks to Claude Code
```bash
# Load all tasks into Claude's TodoWrite
/import-tasks

# This imports all 52+ tasks into Claude's todo system
# Ready for execution starting with T001
```

### Step 7: Execute with Claude Code
```bash
# Claude executes tasks in order
# T001: Create project structure (npm init, folder structure)
# T002: Setup database (PostgreSQL, migrations)
# T003: Initialize Git repository
# T004: Setup Docker configuration
# T005: Configure CI/CD pipeline
# ... and so on

# Claude tracks progress in TodoWrite throughout
```

## Key Understanding

### What Each Tool Does:

1. **`specify init`** - Creates spec-kit's scaffolding only
   - Templates, scripts, memory files
   - NOT the actual project

2. **`/project-setup`** - Creates project vision
   - PROJECT_PLAN.md with requirements
   - High-level decisions
   - Business context

3. **`/specify`** - Creates functional specification
   - WHAT to build (no tech details)
   - User stories
   - Functional requirements

4. **`/plan`** - Adds technical details
   - HOW to build it
   - Tech stack
   - Architecture decisions

5. **`/tasks`** - Generates ALL tasks including:
   - **T001-T010**: Actual project scaffolding
   - **T011+**: Tests and features

6. **`/import-tasks`** - Brings tasks into Claude Code
   - Loads into TodoWrite
   - Ready for execution

7. **Claude executes** - Builds everything
   - Creates actual project structure
   - Implements all features
   - Uses its tools (Bash, Write, Edit)

## The Magic: T001-T010 ARE Project Scaffolding

The key insight: When spec-kit generates tasks, **T001-T010 are the actual project scaffolding tasks**:
- T001: Create solution/project structure
- T002: Setup database
- T003: Initialize Git
- T004: Setup Docker
- T005: Configure CI/CD
- T006: Create test projects
- T007: Add packages
- T008: Configure environment
- T009: Setup formatting
- T010: Create documentation structure

These tasks, when executed by Claude Code, create the actual project structure!

## Complete Example

```bash
# 1. Initialize spec-kit (its scaffolding)
uvx --from git+https://github.com/github/spec-kit.git specify init taskify
cd taskify

# 2. Create vision
/project-setup
> Interactive: "Team task management with Kanban"
> Creates: docs/PROJECT_PLAN.md

# 3. Generate specification
/specify "$(cat docs/PROJECT_PLAN.md)"
> Creates: specs/001-taskify/spec.md

# 4. Add technical details
/plan "React, Node.js, PostgreSQL, Docker, CI/CD"
> Creates: plan.md, research.md, data-model.md

# 5. Generate tasks
/tasks
> Creates: tasks.md with 52 tasks
> T001-T010 = Project scaffolding
> T011-T052 = Tests and features

# 6. Import to Claude
/import-tasks
> Loads all 52 tasks into TodoWrite

# 7. Execute
# Claude starts with T001
# Executes each task using Bash, Write, Edit tools
# Creates actual project, implements features
# Tracks progress in TodoWrite
```

## Result

By the end:
1. ✅ Complete project structure created
2. ✅ CI/CD pipeline configured
3. ✅ Docker setup complete
4. ✅ Database configured
5. ✅ Tests written and passing
6. ✅ Features implemented
7. ✅ Ready for deployment

All from a single requirements description!