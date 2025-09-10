# Spec-Kit Integration Guide

## Quick Start: The Complete Workflow

```bash
# 1. Initialize spec-kit scaffolding (NOT project structure)
uvx --from git+https://github.com/github/spec-kit.git specify init my-app
cd my-app

# 2. Create project vision (optional but recommended)
/project-setup
# Creates: docs/PROJECT_PLAN.md

# 3. Generate functional specification (no tech stack yet!)
/specify "Build [app description with all requirements]"
# Creates: specs/001-feature/spec.md

# 4. Add technical details
/plan "Tech stack: React, Node.js, PostgreSQL, Docker, CI/CD..."
# Creates: plan.md, research.md, data-model.md

# 5. Generate implementation tasks
/tasks
# Creates: tasks.md with T001-T010 (scaffolding) + T011-T052 (features)

# 6. Import to Claude Code
/import-tasks
# Loads all tasks into TodoWrite

# 7. Claude executes starting with T001
# Builds complete project from scratch
```

## Understanding the Architecture

### What Creates What

| Tool | Creates | Purpose |
|------|---------|---------|
| `specify init` | spec-kit scaffolding | memory/, scripts/, templates/ |
| `/project-setup` | PROJECT_PLAN.md | High-level vision |
| `/specify` | spec.md | Functional requirements |
| `/plan` | plan.md, research.md | Technical decisions |
| `/tasks` | tasks.md | Implementation tasks |
| **T001-T010** | **ACTUAL PROJECT** | **Project scaffolding** |

### The Key Insight

**T001-T010 tasks CREATE your actual project structure:**
- T001: Create solution/project (`npm init`, `dotnet new`, etc.)
- T002: Setup database
- T003: Initialize Git
- T004: Setup Docker
- T005: Configure CI/CD
- T006-T010: Testing, packages, configuration

## Project Setup in WSL

### Correct Directory Structure
```bash
# ✅ CORRECT: Independent projects
/mnt/c/Users/angel/Projects/
├── my-app/          # Created by specify init
├── taskify/         # Another project
└── spec-kit/        # Reference clone (optional)

# ❌ WRONG: Nested projects
/mnt/c/Users/angel/Projects/spec-kit/
└── my-app/          # DON'T create inside spec-kit!
```

### Initialize Correctly
```bash
cd /mnt/c/Users/angel/Projects
uvx --from git+https://github.com/github/spec-kit.git specify init my-app
cd my-app
```

## Wrapper Commands

### `/specify` - Functional Requirements
```bash
/specify "Build Taskify with Kanban boards, 5 users, drag-drop..."
```
- Pure WHAT, no HOW
- No tech stack mentioned
- Creates spec.md

### `/plan` - Technical Details
```bash
/plan "Use React, PostgreSQL, Docker, GitHub Actions CI/CD..."
```
- NOW specify tech stack
- Creates plan.md, research.md
- Architecture decisions

### `/tasks` - Generate Tasks
```bash
/tasks
```
- Creates tasks.md
- T001-T010: Infrastructure
- T011+: Features

### `/import-tasks` - Load into Claude
```bash
/import-tasks
```
- Parses tasks.md
- Loads into TodoWrite
- Ready for execution

## Getting Comprehensive Infrastructure

To ensure spec-kit generates complete infrastructure (not just basic setup), include these in your `/specify` prompt:

```
Build [application] with comprehensive infrastructure:
- CI/CD pipeline using GitHub Actions
- Docker containerization for all services
- Unit, integration, and E2E testing
- Database migrations and seeding
- Environment configurations (dev/staging/prod)
- Monitoring and error tracking
- API documentation generation
- Security scanning
- Automated deployments
```

This ensures T001-T020 cover all infrastructure needs, not just T001-T010.

## Integration Points

### Spec-Kit Handles
- Specification generation
- Task breakdown
- Branch creation
- Template structure

### Claude Code Handles
- Task execution
- Progress tracking (TodoWrite)
- File creation/editing
- Running commands
- Testing

### Our Framework Adds
- `/project-setup` for vision
- `/import-tasks` bridge
- GitHub issue creation (optional)
- Deployment commands
- MCP server integration

## Common Workflows

### Starting Fresh
```bash
specify init my-app
cd my-app
/project-setup        # Create vision
/specify "[requirements]"
/plan "[tech stack]"
/tasks
/import-tasks
# Claude executes
```

### Using Existing Spec-Kit Project
```bash
cd existing-project
/import-tasks         # Import existing tasks.md
# Claude continues execution
```

### Adding Features Later
```bash
/specify "Add user authentication feature"
/plan "Use JWT, bcrypt, session management"
/tasks
/import-tasks 002-authentication
# Claude executes new feature
```

## Tips for Success

1. **Always complete T001-T010 first** - Infrastructure is foundation
2. **Be explicit in requirements** - Include CI/CD, Docker, testing needs
3. **Let spec-kit handle branches** - It creates 001-feature branches
4. **Use TodoWrite for tracking** - Claude's progress system
5. **Don't nest projects** - Keep each project independent

## Troubleshooting

### "specify command not found"
```bash
# Install uv and spec-kit
curl -LsSf https://astral.sh/uv/install.sh | sh
uvx --from git+https://github.com/github/spec-kit.git specify init my-app
```

### Tasks not importing
```bash
# Check tasks.md exists
ls specs/*/tasks.md
# Run /tasks if missing
```

### Wrong directory structure
```bash
# Check if nested (bad)
git rev-parse --show-toplevel
# Should show your project, not spec-kit
```

## The Power of Integration

By combining:
- **Spec-Kit**: Specification-driven development
- **Claude Code**: AI-powered execution
- **TodoWrite**: Progress tracking

You get:
- Complete project from description
- Proper architecture from day 1
- No missed requirements
- Systematic implementation
- Full traceability

---

*This guide consolidates all spec-kit integration documentation. For PROJECT_PLAN.md template, see docs/PROJECT_PLAN.md*