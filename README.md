# Solo Developer Framework with Agentic CLIs

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

# Full-stack project (backend + frontend testing)
/home/gotime2022/Projects/multi-agent-claude-code/sync-project-template.sh

# Backend-only project (Python/pytest)
/home/gotime2022/Projects/multi-agent-claude-code/sync-project-template.sh --backend-only

# Frontend-only project (Playwright/TypeScript)
/home/gotime2022/Projects/multi-agent-claude-code/sync-project-template.sh --frontend-only

# Skip all testing templates
/home/gotime2022/Projects/multi-agent-claude-code/sync-project-template.sh --no-testing

# That's it! You now have AI agents as your development partners.
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

### 🎭 Professional Testing Templates
- **Backend Tests**: Complete Python/pytest structure for API development
- **Frontend Tests**: Professional Playwright suite for UI validation
- **Universal Templates**: Cross-framework compatibility (React, Vue, Angular)
- **Personal Quality Assurance**: Clear testing responsibilities for your development workflow

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

### MCP Server Configuration

**Global MCP Servers (Auto-configured):**

#### For Claude Code (Auto-loaded globally):
- ✅ filesystem - File operations
- ✅ github - GitHub integration (with token)
- ✅ memory - Knowledge graph storage
- ✅ sequential-thinking - Step-by-step reasoning
- ✅ playwright - Browser automation
- ✅ postman - API testing

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
## 🐳 Docker for Python Development (No More WSL Issues!)

If you're using Python, Docker eliminates all WSL path issues, version conflicts, and environment problems:

```bash
# After running sync-project-template.sh, you'll have Docker files ready
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
./scripts/ops qa --backend

# Frontend development (UI/UX)
./scripts/ops qa --frontend

# Full-stack changes
./scripts/ops qa --all
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
2. **Add AI coordination**: Run `./sync-project-template.sh` to layer on the multi-agent system
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

Now you have both spec-kit's planning capabilities AND the full multi-agent coordination system ready to go!

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