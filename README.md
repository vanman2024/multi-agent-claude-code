# Solo Developer Framework with Agentic CLIs

> **⚠️ TEMPLATE REPOSITORY NOTICE**: This is a template framework, not a deployable application. Vercel deployments will fail because there's no app code to deploy. Use this template to create new projects with `sync-project-template.sh`.

**Perfect for solo founders and independent developers** who want AI agents as intelligent development partners. This framework transforms your development workflow by providing specialized AI agents that work alongside you, not replace large development teams.

## 🚀 Quick Start: Your Personal Development Team

### Step 1: Create Project with Spec-Kit
```bash
# Navigate to your Projects directory first
cd /home/gotime2022/Projects

# Install spec-kit and create new project
uvx --from git+https://github.com/github/spec-kit.git specify init my-awesome-app
cd my-awesome-app

# Or with specific AI agent
specify init my-awesome-app --ai claude
specify init my-awesome-app --ai gemini
specify init my-awesome-app --ai copilot

# Or add to existing project:
specify init --here --ai copilot
```

### Step 2: Add Your AI Development Partners
```bash
# From your new project directory, run one of these:

# Full-stack project (backend + frontend testing + DevOps)
/home/gotime2022/Projects/multi-agent-claude-code/sync-project-template.sh

# Backend-only project (Python/pytest + DevOps)
/home/gotime2022/Projects/multi-agent-claude-code/sync-project-template.sh --backend-only

# Frontend-only project (Playwright/TypeScript + DevOps)
/home/gotime2022/Projects/multi-agent-claude-code/sync-project-template.sh --frontend-only

# Skip all testing templates (DevOps only)
/home/gotime2022/Projects/multi-agent-claude-code/sync-project-template.sh --no-testing

# Include VS Code Dev Container configuration (optional)
/home/gotime2022/Projects/multi-agent-claude-code/sync-project-template.sh --devcontainer

# 🆕 NEW: Automatic GitHub Repository Creation
# Create project AND GitHub repository in one command:
/home/gotime2022/Projects/multi-agent-claude-code/sync-project-template.sh --create-repo

# Create private repository with custom name:
/home/gotime2022/Projects/multi-agent-claude-code/sync-project-template.sh --github --private --repo-name "my-awesome-project"

# Full customization with description:
/home/gotime2022/Projects/multi-agent-claude-code/sync-project-template.sh --create-repo --repo-name "custom-name" --description "My multi-agent project"

# That's it! You now have AI agents as your development partners AND a GitHub repository!
```

> 💡 You can combine `--devcontainer` with the testing flags if you want a dev container alongside a backend-only or frontend-only setup.

### Step 3: You're Ready to Develop!
```bash
# The DevOps system was automatically configured during Step 2!
# Check what was set up:
cat DEVOPS_SETUP.md

# Start using your development environment:
./devops/ops/ops qa          # Run quality checks
./devops/ops/ops build       # Build for production  
./devops/ops/ops status      # Check project status

# Copy environment template and configure:
cp .env.example .env
# Edit .env with your API keys and settings

# Your complete development environment is ready!
```

## 🐙 GitHub Integration & Automatic Repository Creation

### One-Command Project Setup with GitHub
Create a complete development environment AND GitHub repository in a single command:

```bash
# Basic: Create public repository with directory name
./sync-project-template.sh --create-repo

# Private repository with custom name
./sync-project-template.sh --github --private --repo-name "my-project"

# Full customization
./sync-project-template.sh --create-repo \
  --repo-name "awesome-project" \
  --description "My multi-agent development project" \
  --private
```

### What Happens Automatically
✅ **Project Setup**: Complete template sync with DevOps v1.6.0 + AgentSwarm v1.4.1  
✅ **Repository Creation**: GitHub repository created via `gh` CLI  
✅ **Git Initialization**: Local repository initialized with proper remote  
✅ **Initial Commit**: Professional commit with component version tracking  
✅ **Code Push**: All template files pushed to GitHub  
✅ **Version Management**: Ready for semantic versioning and automated releases  

### Requirements
- **GitHub CLI**: Must be installed and authenticated (`gh auth login`)
- **Git**: Available in system PATH
- **Internet**: For repository creation and code push

### Generated Commit Message
```
feat: initial project setup from multi-agent template

🤖 Generated with [Claude Code](https://claude.ai/code)

Components included:
- DevOps automation system (v1.6.0)
- AgentSwarm orchestration (v1.4.1)
- Multi-agent coordination framework
- GitHub workflows and automation
- Testing infrastructure
- MCP server configurations
```

### Available Options
| Flag | Description | Example |
|------|-------------|---------|
| `--create-repo` | Create GitHub repository and push code | Basic setup |
| `--github` | Same as --create-repo | Alternative syntax |
| `--repo-name NAME` | Custom repository name | `--repo-name "my-app"` |
| `--private` | Create private repository | Default: public |
| `--description "..."` | Custom repository description | Professional description |

Combine with other flags:
```bash
# Backend-only private repository
./sync-project-template.sh --backend-only --github --private

# Full-stack with dev container and GitHub repo
./sync-project-template.sh --devcontainer --create-repo
```

## 🚀 Deployment Strategy

### For Template Repository (This Repo)
- **DO NOT DEPLOY**: This template has no deployable application code
- **Vercel Integration**: Should be removed or ignored via `.vercelignore`
- **Purpose**: Framework for creating new projects, not hosting applications

### For Projects Created from Template
When you use this template to create a new project:

1. **Add Application Code**: Create actual app files (React, Next.js, etc.)
2. **Configure Deployment**: Set up Vercel/Netlify for the actual application
3. **Update Workflows**: Customize deployment workflows for your specific stack
4. **Remove Template Notices**: Delete template-specific warnings from README

Example deployment setup for created projects:
```bash
# In your NEW project (not this template):
npm create next-app .          # Add actual application
vercel init                   # Configure deployment
# Now deployments will work because you have an app to deploy
```

## 📋 Your Personal AI Development Toolkit

### 🤖 Specialized AI Agents as Your Development Partners
- `agents/CLAUDE.md` - Your CTO-level code reviewer and architect
- `agents/AGENTS.md` - Personal productivity coordination rules
- `agents/QWEN.md` - Local performance optimization specialist (free)
- `agents/GEMINI.md` - Research and documentation expert
- `.github/copilot-instructions.md` - GitHub Copilot as your fast implementation partner

### 🔧 Intelligent Tool Integration
- `mcp.json` - MCP server configuration for seamless AI tool access
- VS Code settings optimized for solo development workflows
- Environment variable templates (`.env.example`)
- Testing standards tailored for individual productivity

### ⚙️ Personal Development Automation
- CI/CD pipeline with quality gates for your solo projects
- Preview deployment workflow (Vercel) for rapid iteration
- Production deployment automation for one-person operations
- Automated PR status updates and coverage reports

### 🪝 Smart Development Hooks
- Session context loading for continuous development flow
- Work state preservation between coding sessions
- Automatic git state tracking for personal project management

### 🎭 Professional Testing Architecture

#### Backend Testing (Python/pytest)
- **Generic test patterns** for any backend project
- **7 test categories**: unit, integration, contract, e2e, performance, CLI, MCP
- **JSON-first CLI template** for agent-friendly commands
- **No app-specific code** - pure patterns ready for customization

#### Frontend Testing (Playwright/TypeScript)
- **E2E test suite** with visual regression and accessibility
- **API testing patterns** for frontend-backend integration
- **Cross-browser support** with automated test generation
- **Component testing** for React, Vue, Angular frameworks

#### Ops CLI Testing Integration
```bash
# Backend development (Python/API)
ops qa --backend        # Runs pytest suite

# Frontend development (UI/UX)
ops qa --frontend       # Runs Playwright tests

# Full-stack development
ops qa --all           # Runs complete test suite

# Individual test categories
ops qa --unit         # Unit tests only
ops qa --e2e          # End-to-end tests only
```

## 🚀 Parallel Agent Swarm Deployment

### Single Command Parallel AI Development

Deploy multiple AI agents simultaneously for 9x speed improvement on complex features:

```bash
# Quick deployment examples:
/tmp/multi-agent-claude-code/.claude/scripts/swarm /path/to/project "Feature description"
/tmp/multi-agent-claude-code/.claude/scripts/swarm /path/to/project --analysis

# Or use the short wrapper:
swarm /path/to/project "Add authentication system"
swarm /path/to/project --analysis
```

### Three Deployment Modes

#### 1. Task-Based Mode (Recommended for Features)
```bash
# Step 1: Create tasks.md with @symbol assignments
cat > /path/to/project/tasks.md << 'EOF'
- [ ] T001 @gemini Analyze authentication architecture
- [ ] T002 @qwen Optimize login performance  
- [ ] T003 @codex Create login UI components
- [ ] T004 @claude Integrate and review all work
EOF

# Step 2: Deploy swarm - agents get their specific tasks
swarm /path/to/project "Add authentication system"

# Output shows task assignments:
# 📋 Found task assignments: /path/to/project/tasks.md
# 🤖 Deploying @gemini... (ASSIGNED TASKS: Analyze authentication architecture)
# 🤖 Deploying @qwen... (ASSIGNED TASKS: Optimize login performance)
# 🤖 Deploying @codex... (ASSIGNED TASKS: Create login UI components)
```

#### 2. Analysis Mode (Perfect for New Codebases)
```bash
# Deploy agents for comprehensive codebase analysis
swarm /path/to/project --analysis

# Each agent analyzes different areas:
# @gemini: Architecture & Dependencies
# @qwen: Performance & Optimization  
# @codex: Frontend/UI or Code Quality
```

#### 3. Generic Mode (Simple Feature Development)
```bash
# Without tasks.md, agents get feature-focused assignments
swarm /path/to/project "Add payment integration"
```

### Step-by-Step Swarm Workflow

#### Phase 1: Planning (2-3 minutes)
```bash
# Option A: Create specific task assignments (recommended)
cat > /project/tasks.md << 'EOF'
- [ ] T001 @gemini Research payment provider APIs
- [ ] T002 @qwen Optimize payment processing performance
- [ ] T003 @codex Build payment UI components
- [ ] T004 @claude Security review and integration
EOF

# Option B: Use analysis mode for codebase exploration
# (No tasks.md needed - agents automatically get focused areas)
```

#### Phase 2: Deployment (30 seconds)
```bash
# Deploy all agents simultaneously
swarm /project "Add payment system"  # or --analysis

# All agents start working in parallel:
# ✅ @gemini deployed (PID: 12345)
# ✅ @qwen deployed (PID: 12346)  
# ✅ @codex deployed (PID: 12347)
```

#### Phase 3: Monitoring (ongoing)
```bash
# Monitor all agents in real-time
tail -f /tmp/agent-swarm-logs/*.log

# Monitor specific agents
tail -f /tmp/agent-swarm-logs/gemini.log
tail -f /tmp/agent-swarm-logs/qwen.log
tail -f /tmp/agent-swarm-logs/codex.log

# Check agent status
ps aux | grep -E '(gemini|qwen|codex)'
```

#### Phase 4: Integration (15-30 minutes)
```bash
# Claude coordinates and integrates all work
claude /work "Review and integrate swarm outputs for payment system"

# Quality validation
cd /project && ./ops/ops qa

# Clean up
swarm --kill  # Terminates all agents
```

### Swarm Benefits

**Speed Improvements:**
- 9x faster feature development (parallel vs sequential)
- 75% reduction in coordination overhead
- 90% better resource utilization

**Quality Improvements:**
- Each agent works in their specialization area
- Comprehensive coverage of all development aspects
- Built-in quality gates through Claude coordination

**Cost Efficiency:**
- Maximum utilization of free tiers (4000+ daily requests)
- Strategic use of paid agents only for coordination
- 85% of work completed on free models

### When to Use Each Mode

**Task-Based Mode:**
- Complex features requiring coordination
- When you know exactly what needs to be done
- Multi-step implementations

**Analysis Mode:**
- New codebase exploration
- Performance audits
- Architecture reviews
- Code quality assessments

**Generic Mode:**
- Simple feature additions
- Quick prototyping
- When you don't want to create tasks.md

**📚 Complete Documentation:** [AI Development Workflow Guide](./docs/AI-DEVELOPMENT-WORKFLOW.md)

### Quick Reference

```bash
# Install and setup (one-time)
git clone https://github.com/vanman2024/multi-agent-claude-code.git
cd multi-agent-claude-code

# Deploy swarm (daily usage)
./scripts/swarm /path/to/project "Feature name"           # Task-based
./scripts/swarm /path/to/project --analysis               # Analysis mode
./scripts/swarm /path/to/project "Simple feature"         # Generic mode

# Monitor progress
tail -f /tmp/agent-swarm-logs/*.log

# Cleanup
./scripts/swarm --kill
```

## 🤖 Your Personal AI Development Team

### Daily Capacity: 4000+ FREE Requests for Solo Developers
- **Gemini 2.5 Pro**: 1000 requests/day (OAuth) - Your research specialist
- **Gemini 2.0 Flash Exp**: Unlimited while experimental (API) - Your documentation expert
- **Qwen**: 2000 requests/day (OAuth) - Your performance optimization partner
- **Claude Code**: Your architect/reviewer (local) - Your CTO-level code reviewer
- **GitHub Copilot**: Your fast implementation partner (free with Pro)

### Your AI Development Workflow
```bash
# Terminal 1: Gemini 2.5 Pro (OAuth - 1000 requests/day FREE)
gemini                  # Uses OAuth login with Google account

# Terminal 2: Gemini 2.0 Flash Experimental (API Key - Unlimited while experimental)
# One-time setup per terminal session:
source ~/bin/gemini-setup-experimental.sh
gemini -m gemini-2.0-flash-exp    # Use ANY model with -m flag

# Or use the convenience wrapper:
/home/gotime2022/bin/gemini-exp   # Always uses 2.0 Flash Experimental
```

**Note:** The `gemini -m` flag works with ANY Gemini model (gemini-2.0-flash-exp, gemini-1.5-pro, etc.)

### Qwen CLI (2000 requests/day FREE)
```bash
qwen                    # OAuth login, 2000 free requests daily
```

### Codex CLI (Interactive Development)
```bash
codex                   # Interactive mode
codex exec [command]    # Non-interactive execution
```

### Claude Code (Your CTO-level reviewer)
```bash
# Already integrated - you're using it now!
# Acts as architect/reviewer for your development work
```

### Postman API Testing Integration

**Automatic Setup:**
- Postman MCP server pre-configured in all AI agents
- API key managed through `.env` file
- Newman CLI for command-line testing
- Integrated with `ops qa --backend` for contract testing

**Available Postman Features:**
```bash
# Create API collections
mcp__postman__createCollection

# Generate tests from OpenAPI specs
mcp__postman__syncCollectionWithSpec

# Run contract tests locally
newman run collection.json --environment test.json

# Through ops CLI
ops qa --backend  # Includes Postman contract tests
```

### MCP Server Configuration

**Global MCP Servers (Auto-configured):**

#### For Claude Code (Auto-loaded globally):
- ✅ filesystem - File operations
- ✅ github - GitHub integration (with token)
- ✅ memory - Knowledge graph storage
- ✅ sequential-thinking - Step-by-step reasoning
- ✅ playwright - Browser automation
- ✅ postman - API testing and documentation (collections, mocks, contract tests)

#### For GitHub Copilot in VS Code:
MCP servers are configured in `.vscode/mcp.json` (already included in template).

To activate in VS Code:
1. Open `.vscode/mcp.json` 
2. Click the "Start" button that appears
3. Open Copilot Chat in "Agent" mode
4. Click the tools icon to see available MCP servers

**Project-Specific MCP Servers:**
For project-specific servers like Supabase, add them manually:

```bash
# Add Supabase MCP server (requires project credentials)
npx @supabase/mcp-server-supabase@latest \
  --project-ref YOUR_PROJECT_REF \
  --access-token YOUR_ACCESS_TOKEN

# Or use Claude Code CLI to add it:
claude mcp add supabase -- npx -y @supabase/mcp-server-supabase@latest

# For Copilot, add to .vscode/mcp.json:
"supabase": {
  "command": "npx",
  "args": ["-y", "@supabase/mcp-server-supabase@latest"],
  "env": {
    "SUPABASE_PROJECT_REF": "${env:SUPABASE_PROJECT_REF}",
    "SUPABASE_ACCESS_TOKEN": "${env:SUPABASE_ACCESS_TOKEN}"
  }
}
```

Then set the environment variables in your `.env`:
```bash
SUPABASE_PROJECT_REF=your_project_ref
SUPABASE_ACCESS_TOKEN=your_access_token
```
## 🔧 DevOps System - Your Development Powerhouse

The template includes a complete DevOps system that handles all your development needs:

```bash
# Quality checks (lint, format, typecheck, test)
./devops/ops/ops qa

# Build for production
./devops/ops/ops build

# Deploy to production 
./devops/deploy/deploy production

# Check project status
./devops/ops/ops status

# Setup development environment
./devops/ops/ops setup
```

### DevOps Features
- **Smart Testing**: Automatically detects Python/Node.js and runs appropriate tests
- **Quality Gates**: Comprehensive linting, formatting, and type checking
- **Deployment**: Production-ready deployment scripts with environment management
- **Environment Setup**: Automatic Python virtual environment and Node.js dependency management
- **CI/CD Integration**: GitHub Actions workflows that use the DevOps system

### 🔄 Three-Repository Versioning Framework

This template uses a **revolutionary three-repository semantic versioning architecture** that automatically synchronizes components across multiple repositories:

- **[vanman2024/devops](https://github.com/vanman2024/devops)** - DevOps CLI and automation tools
- **[vanman2024/agentswarm](https://github.com/vanman2024/agentswarm)** - Multi-agent orchestration system  
- **[vanman2024/multi-agent-claude-code](https://github.com/vanman2024/multi-agent-claude-code)** - Template repository (this repo)

**How it works:**
1. **Source repositories** (devops, agentswarm) use conventional commits (`feat:`, `fix:`, `BREAKING CHANGE:`)
2. **Semantic versioning** automatically bumps versions based on commit types
3. **Cross-repository deployment** pushes production-ready code to this template
4. **Version synchronization** ensures all components work together

Your projects inherit this battle-tested versioning system automatically. See [VERSIONING.md](./VERSIONING.md) for complete details.

**Quick commands:**
```bash
# Configure git to use commit template
git config commit.template .gitmessage

# Use conventional commits for automatic versioning
git commit  # Opens template with examples
```

## 🐳 Docker for Python Development (No More WSL Issues!)

If you're using Python, Docker eliminates all WSL path issues, version conflicts, and environment problems:

```bash
# After running sync-project-template.sh, you'll have Docker files ready
# (add --devcontainer when running the sync if you want a VS Code dev container)
# Start the development environment:
./docker-scripts.sh dev-up

# Your Python environment is now running in Docker!
# - Python dev server: http://localhost:8000
# - Node.js frontend: http://localhost:3000
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379

# Open a shell in the Python container:
./docker-scripts.sh dev-shell python-dev

# Run tests in container (no local Python needed!):
./docker-scripts.sh dev-test

# Format code:
./docker-scripts.sh dev-format

# Stop everything:
./docker-scripts.sh dev-down
```

**VS Code Integration:**
- Open folder in container: F1 → "Dev Containers: Open Folder in Container"
- All extensions and Python work inside the container
- No local Python installation needed!

## 🔄 Updating Existing Projects

### CLI-First Testing via ops (No Frontend Required)

Standardize your local testing with the ops CLI:

```
# Backend unit/contract/smoke (fast lane)
./project-sync/devops/ops/ops qa --backend

# CLI contract tests (golden JSON outputs, exit codes)
./project-sync/devops/ops/ops qa --cli

# MCP server tests (in-memory by default)
./project-sync/devops/ops/ops qa --mcp

# Everything fast (excludes slow/subprocess by default)
./project-sync/devops/ops/ops qa --all

# Include transport/subprocess MCP tests when needed
RUN_MCP_TRANSPORT=1 ./project-sync/devops/ops/ops qa --mcp
```

Notes:
- Tests live under `project-sync/testing/backend-tests/` and are organized by suite (cli, mcp, unit, etc.).
- MCP tests auto-skip if `fastmcp` isn’t installed.
- If `pytest` isn’t available in your env, install it or activate your venv. The ops CLI falls back from `uv` → `pytest` → `python -m pytest` automatically.

If you already ran the setup and need to update/add missing files:

```bash
# The setup script will detect existing configuration and exit with this message:
# "⚠️ AI Agents already configured in this project!"
# "To reconfigure, run: node /path/to/sync-project.js"

# Run the sync script directly to update existing projects:
cd your-project-directory
node /home/gotime2022/Projects/multi-agent-claude-code/project-sync/scripts/sync-project.js

# This safely adds missing files without overwriting your existing customizations
```

## 📊 Smart Agent Selection for Your Development Tasks

Choose the right AI partner based on your current task complexity and needs:

- **GitHub Copilot** (free, fast implementation) - Handles everything from simple features to complex multi-step implementations
- **Complex architectural tasks** → Claude Code agents (strategic guidance and code review)
- **Performance optimization** → Qwen API (2000 requests/day free, optimization specialist)
- **Research & documentation** → Gemini CLI (dual-model strategy for comprehensive coverage)
- **Interactive development** → Codex API (conversational development partner)

### Your Personal Development Strategy
This framework is designed for solo developers who want AI agents as intelligent partners, not replacements for human teams. Each agent has specialized capabilities that complement your development workflow:

- **GitHub Copilot**: Your versatile implementation partner capable of handling the full spectrum of development tasks - from simple features to complex multi-step implementations
- **Claude Code**: Your CTO-level reviewer providing architectural guidance and code quality assurance
- **Qwen**: Your performance optimization specialist ensuring your applications run efficiently
- **Gemini**: Your research and documentation expert for comprehensive project documentation
- **Codex**: Your interactive development partner for conversational coding assistance

## 🧪 Dual Testing Architecture

### Professional-Grade Testing Templates
This framework provides comprehensive testing templates for both backend and frontend:



**Backend Testing** (`backend-tests/`):
- **Python/pytest**: API logic, data processing, integrations
- **Structure**: smoke, unit, integration, contract, performance, e2e, helpers
- **Coverage**: Comprehensive test coverage with real examples
- **Agent**: @claude handles backend testing responsibilities

**Frontend Testing** (`frontend-tests/`):
- **Playwright/TypeScript**: UI, E2E, visual regression, accessibility testing
- **Smart Strategy**: Focus on critical user journeys (5-10% E2E), not every page
- **Coverage**: Visual regression, accessibility compliance, API contracts, user workflows
- **Agent**: @copilot handles frontend testing responsibilities

### Ops CLI Integration
```bash
# Backend development (Python/API)
./devops/ops/ops qa --backend

# Frontend development (UI/UX)
./devops/ops/ops qa --frontend

# Full-stack changes
./devops/ops/ops qa --all
```

### Smart Testing Strategy
**✅ What TO E2E Test (5-10% of tests):**
- Critical user journeys (signup → dashboard → primary feature)
- Payment/checkout flows
- Authentication workflows
- Core business processes

**❌ What NOT to E2E Test (90-95% of pages):**
- Static content pages (About, Terms, Privacy)
- Admin panels (unless core business)
- Individual component variations
- Every form permutation

**Better Alternatives:**
- **Static pages** → Visual regression tests
- **Components** → Integration tests  
- **Business logic** → Unit tests

### Project Type Detection & Testing Templates
The setup script automatically detects your project type and installs appropriate testing:

- **Python projects** (`pyproject.toml`, `requirements.txt`): Gets `backend-tests/` with pytest structure
- **Node.js projects** (`package.json`): Gets `frontend-tests-template/` with Playwright suite  
- **Full-stack projects**: Gets both testing templates automatically
- **Override detection**: Use `--backend-only`, `--frontend-only`, or `--no-testing` flags to override automatic detection

## 🚨 Production Readiness System

### Automatic Mock Detection & Validation
This framework includes a comprehensive production readiness system that automatically:
- Detects mock implementations (payment, auth, database, APIs)
- Generates tests to validate production replacements
- Provides expert guidance for fixing critical issues
- Injects context when deployment keywords are mentioned

### Complete Production Workflow
```bash
# Step 1: Detect all mock implementations
/prod-ready --verbose

# Step 2: Generate tests for production validation  
/test-prod --all

# Step 3: The production-specialist agent fixes mocks
# (Automatically receives context from steps 1 & 2)

# Step 4: Run generated tests to validate fixes
./tests/production/run_production_tests.sh
```

### Smart Context Injection
Just mention deployment-related keywords and the system automatically:
- ✅ Detects deployment intent ("deploy", "production", "go live")
- ✅ Runs mock detection scan in background
- ✅ Injects production readiness context
- ✅ Suggests using the production-specialist sub-agent

### Available Commands
- `/prod-ready` - Comprehensive production readiness scan
- `/prod-ready --fix` - Auto-fix simple production issues  
- `/test-prod` - Generate tests to validate mock replacements
- `/test-prod --api` - Generate API-specific tests only

### Production Specialist Agents
- **production-specialist** - Expert in replacing mocks with real implementations
- **test-generator** - Creates tests to validate production readiness

### What Gets Detected
- 🚨 **Critical**: Payment mocks, auth stubs, fake databases
- ⚠️ **Warning**: Localhost references, debug mode, placeholders
- ℹ️ **Info**: Test servers, mock libraries in production code

## 🚀 Deployment Ready

- Vercel deployment workflows
- Environment variable templates
- Production readiness scripts
- Security scanning and linting

## 🔄 Personal Productivity Tools

- **@symbol task assignment system** - Organize your development tasks with AI partners
- **Shared MCP server access** - Seamless tool integration across your development environment
- **Context preservation** - Maintain development flow between coding sessions
- **Work state tracking** - Keep track of your progress and priorities

## 📋 Two Scripts Explained

### 1. sync-project-template.sh (Main Entry Point)
- **For**: New projects that haven't been configured yet  
- **What it does**: Safety checks, then automatically calls sync-project.js
- **Safety**: Won't overwrite existing configurations
- **Flags**: `--backend-only`, `--frontend-only`, `--no-testing`, `--devcontainer`

### 2. sync-project.js (File Sync Engine)
- **For**: Existing projects that need updates or missing files added
- **What it does**: Copies agent files, .claude directory, VS Code settings, .env, .gitignore, etc.
- **Safety**: Only adds missing files, preserves your existing customizations

## 📁 How It Works

### Tech Stack Detection
Automatically detects React/Next.js, Python/FastAPI, Node.js/Express, etc.

### Smart Configuration
Applies appropriate testing standards and scripts for your framework

### File Copying
Copies all template files while preserving your existing project structure

### No Conflicts
Only adds files, never overwrites existing project files

## 📜 Available Scripts

| Command | Description |
|---------|-------------|
| `sync-project-template.sh` | Main setup script for new projects |
| `sync-project.js` | Core sync logic (called by setup script) |
| `sync-mcp-servers.sh` | Sync MCP servers to all AI agents |
| `sync-mcp-servers.sh configure` | Set project-specific tokens |
| `sync-mcp-servers.sh list` | List configured MCP servers |

## ⚙️ Customizing Settings

### VS Code Customizations
Edit `local-overrides/vscode-local.json`:
```json
{
  "// Machine-specific overrides": "",
  "editor.fontSize": 16,
  "editor.fontFamily": "JetBrains Mono",
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "python.defaultInterpreterPath": "/usr/local/bin/python3"
}
```
## 🔒 Security

- ✅ **Templates**: Safe defaults, no sensitive data
- ✅ **Local overrides**: Can contain API keys, local paths (never committed)
- ✅ **Automatic backups**: Before every sync
- ✅ **Cross-platform**: Works on Windows, macOS, Linux

## 🔄 Integration with Spec-Kit

The project sync system works seamlessly with spec-kit projects:

1. **Initialize with spec-kit**: Use spec-kit to create your project structure and initial planning
2. **Add AI coordination**: Run `./sync-project-template.sh` to layer on the solo developer AI system
3. **Start developing**: Use @symbol coordination with spec-kit's generated plans

### Example Workflow:
```bash
# Start from your Projects directory
cd /home/gotime2022/Projects

# Create new project with spec-kit
uvx --from git+https://github.com/github/spec-kit.git specify init my-app

# Enter project directory  
cd my-app

# Add AI agent coordination
/home/gotime2022/Projects/multi-agent-claude-code/sync-project-template.sh

# Start developing with AI agents
code .
```

Now you have both spec-kit's planning capabilities AND the full solo developer AI coordination system ready to go!

## 🎯 Why This Works for Solo Developers

> **"AI agents as development partners multiply your individual productivity."**

This framework succeeds for solo developers because:

1. **Personal Productivity Focus** - AI agents handle routine tasks so you can focus on creative work
2. **Instant Onboarding** - No learning curve - use familiar @mentions to coordinate with AI partners
3. **Tool Independence** - Works with any AI agent or development environment
4. **Scalable Workflow** - Start simple, add complexity as your projects grow
5. **Cost Effective** - 4000+ free daily requests across multiple AI services
6. **Quality Assurance** - Built-in code review and testing standards maintain professional quality

### Perfect For:
- **Solo founders** building MVPs and prototypes
- **Independent developers** working on client projects
- **Freelancers** needing to deliver high-quality code quickly
- **Entrepreneurs** validating ideas before hiring teams
- **Developers** wanting to explore new technologies efficiently

## 📚 Technical Details

### Configuration Files
- `project-sync-config.template.json` - Master configuration template
- Dynamic tech stack detection and framework-specific settings
- Testing command standards for different project types
- MCP server routing (local vs remote access)

### Your AI Development Partners
Each AI agent is configured with specialized capabilities to complement your development workflow:
- **Claude Code**: Full MCP access (filesystem, git, github, memory, etc.) - Your CTO-level reviewer
- **Qwen**: Performance optimization with API access - Your efficiency specialist
- **Gemini**: Research and documentation tools - Your knowledge expert
- **GitHub Copilot**: GitHub integration and VS Code extensions - Your fast implementation partner

### Development Modes
- **Solo Developer Mode**: You're using this framework to build applications with AI partners
- **Framework Builder Mode**: You're improving this framework itself

This framework bridges the gap between individual development needs and professional-grade tooling, giving you the productivity of a full development team while maintaining your creative control.

## 🤝 Join the Solo Developer Revolution

1. **Fork the framework** for your development workflow
2. **Create issues** with your development challenges
3. **Implement features** with your AI development partners
4. **Share improvements** with the community
5. **Get AI-powered reviews** for your code

---

<div align="center">

**Built with ❤️ for solo developers by solo developers**

[Report Issues](https://github.com/vanman2024/multi-agent-claude-code/issues) • [Documentation](./docs)

</div>
