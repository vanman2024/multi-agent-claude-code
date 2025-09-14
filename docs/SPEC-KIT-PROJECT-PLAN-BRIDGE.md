# Project Sync System - Complete Multi-Agent Setup

## What is Project Sync?

The **Project Sync System** is a comprehensive template that copies all necessary files for multi-agent coordination from this repository to your new project. Think of it as a "project template expander" that gives you everything you need for AI-driven development.

## What Gets Copied to Your Project

### 🤖 Agent Coordination Files
- `agents/CLAUDE.md` - Claude Code subagent instructions
- `agents/AGENTS.md` - Multi-agent coordination rules
- `agents/QWEN.md` - Local Ollama agent (free)
 
- `agents/GEMINI.md` - Google AI research agent
- `.github/copilot-instructions.md` - GitHub Copilot configuration

### 🔧 MCP & Tools Configuration
- `mcp.json` - Shared MCP server configuration for all agents
- VS Code settings with AI tool extensions
- Environment variable template (`.env.example`)
- Testing standards for your detected tech stack

### ⚙️ GitHub Automation
- CI/CD pipeline with quality gates
- Preview deployment workflow (Vercel)
- Production deployment automation
- Automated PR status updates and coverage reports

### 🪝 Development Hooks
- Session context loading for agents
- Work state preservation between sessions
- Automatic git state tracking

### 📋 Project Essentials
- `.gitignore` additions for AI development
- Helper scripts for production readiness
- Documentation templates
- Package.json script additions based on tech stack

## How It Works

1. **Tech Stack Detection**: Automatically detects React/Next.js, Python/FastAPI, Node.js/Express, etc.
2. **Smart Configuration**: Applies appropriate testing standards and scripts for your framework
3. **File Copying**: Copies all template files while preserving your existing project structure
4. **No Conflicts**: Only adds files, never overwrites existing project files

## Usage

### Option 1: Simple Setup (Recommended)
```bash
# From the multi-agent-claude-code directory
./sync-project-template.sh
```

### Option 2: Manual Sync
```bash
# Sync to specific project directory
node project-sync/scripts/sync-project.js /path/to/your/project
```

### Option 3: Integration with Spec-Kit
If you're using spec-kit for project initialization:
```bash
# After spec-kit init
./sync-project-template.sh
```

## What You Get After Setup

### 📊 Smart Agent Routing
- Simple tasks (Complexity ≤2, Size XS/S) → GitHub Copilot (free)
- Complex tasks (Complexity 3-5, any size) → Claude Code agents
- Local development → Qwen API (2000 requests/day free)
- Research → Gemini CLI
- Interactive development → Codex API

### 🧪 Testing Infrastructure
Based on your detected tech stack:
- **React/Next.js**: Jest, Playwright, ESLint, TypeScript checking
- **Python/FastAPI**: pytest, coverage, ruff/flake8, mypy
- **Node.js/Express**: Jest, supertest, ESLint, TypeScript

### 🚀 Deployment Ready
- Vercel deployment workflows
- Environment variable templates
- Production readiness scripts
- Security scanning and linting

### 🔄 Agent Coordination
- @symbol task assignment system
- Shared MCP server access across all tools
- Context preservation between sessions
- Work state tracking

## Technical Details

### Configuration Files
- `project-sync-config.template.json` - Master configuration template
- Dynamic tech stack detection and framework-specific settings
- Testing command standards for different project types
- MCP server routing (local vs remote access)

### Agent Capabilities
Each agent gets configured with appropriate tool access:
- **Claude Code**: Full MCP access (filesystem, git, github, memory, etc.)
- **Qwen**: Performance optimization with API access
- **Gemini**: Research and documentation tools
- **Copilot**: GitHub integration and VS Code extensions

### Template vs Project Mode
- **Template Mode**: You're building/improving this framework
- **Project Mode**: You're using this framework to build applications

This project sync system bridges the gap between spec-kit project initialization and full AI agent coordination, giving you the best of both worlds.

## Integration with Spec-Kit

The project sync system works seamlessly with spec-kit projects:

1. **Initialize with spec-kit**: Use spec-kit to create your project structure and initial planning
2. **Add AI coordination**: Run `./sync-project-template.sh` to layer on the multi-agent system
3. **Start developing**: Use @symbol coordination with spec-kit's generated plans

### Example Workflow:
```bash
# Create new project with spec-kit
npx @spec-kit/cli init my-app

# Enter project directory  
cd my-app

# Add AI agent coordination
/path/to/multi-agent-claude-code/sync-project-template.sh

# Start developing with AI agents
code .
```

Now you have both spec-kit's planning capabilities AND the full multi-agent coordination system ready to go!