# 🚀 Multi-Agent Development Framework (Template)

<div align="center">

![Version](https://img.shields.io/badge/Version-v2.0.0-purple?style=for-the-badge)
![GitHub](https://img.shields.io/badge/GitHub-Native-black?style=for-the-badge&logo=github)
![Copilot](https://img.shields.io/badge/GitHub_Copilot-Free-blue?style=for-the-badge&logo=github)
![Claude](https://img.shields.io/badge/Claude_Code-Local-orange?style=for-the-badge)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-black?style=for-the-badge&logo=vercel)

**⚠️ TEMPLATE FRAMEWORK: Clone this to bootstrap your AI-driven development**

**Simplified AI-driven development: Issue-driven features with AI assistance**

[Quick Start](#-quick-start) • [Core Workflow](#-core-workflow) • [Documentation](#-documentation)

</div>

---

## 🎯 What's New: Five-Tier Development System

**COMPREHENSIVE PLANNING**: Project setup to production
- `/project-setup` - Interactive discovery and vision creation
- `/plan:generate` - Generate detailed technical documentation
- `/test:generate` - Create comprehensive test suites (90% coverage from day 1)

**SMART IMPLEMENTATION**: Right tool for the right job
- `/create-issue` - Smart routing to Copilot (simple) or Claude (complex)
- `/work` - Full issue→PR→merge workflow with tracking

**FIVE-TIER FRAMEWORK**:
- ⚙️ **Infrastructure** - Local DevOps setup (not tracked as issues)
- 🏗️ **Architecture** - System design decisions
- 🎨 **Design System** - UI/UX foundation
- 📱 **Standard Features** - Common app functionality
- 🎯 **Custom Features** - Your unique value (10-20 GitHub issues)

**COST-FREE**: No paid @claude GitHub App - uses free GitHub Copilot + local Claude Code

**UNIFIED**: Everything deploys to Vercel (frontend + backend)

---

## ⚡ Quick Start

### 1️⃣ Clone & Initialize

```bash
# Get the template
git clone https://github.com/vanman2024/multi-agent-claude-code.git my-project
cd my-project

# Make it yours
rm -rf .git && git init
git add . && git commit -m "Initial from template"
git remote add origin https://github.com/YOU/your-repo.git
git push -u origin main
```

### 2️⃣ Install Tools

```bash
# Required CLIs
brew install gh                    # GitHub CLI
npm install -g vercel newman        # Vercel & Postman
npx playwright install              # Browser automation
```

### 3️⃣ Configure API Keys & VSCode Settings

```bash
# FIRST TIME ONLY: Create personal config
./scripts/utilities/setup-personal-config.sh
# Saves to ~/.claude-code/personal-config.json

# FOR EACH PROJECT: Load your keys
./scripts/utilities/load-personal-config.sh
# Creates .env with all your saved keys

# Apply VSCode settings globally (recommended)
./scripts/utilities/vscode-settings-sync.sh --user
# Other options: --profile, --symlink, --copy, --git-template, --extension
```

### 4️⃣ Setup MCP Servers

```bash
# Start Claude Code
claude

# Add essential MCP servers
/add-mcp

# This configures:
# ✅ GitHub MCP (free, local API access)
# ✅ Playwright (browser testing)
# ✅ Supabase (database)
# ✅ Postman (API testing)
```

### 5️⃣ Initialize Project with Five-Tier System

```bash
# Step 1: Interactive project discovery and vision
/project-setup
# Creates: docs/PROJECT_PLAN.md (your north star vision)

# Step 2: Generate detailed technical documentation
/plan:generate
# Creates: ARCHITECTURE.md, INFRASTRUCTURE.md, FEATURES.md, DESIGN_SYSTEM.md

# Step 3: Generate comprehensive test suites
/test:generate --all
# Creates: Unit tests, API tests (Postman), E2E tests

# Step 4: Start building
/create-issue "User authentication"
/work #1
```

---

## 🔄 Core Workflow: Plan → Build → Test → Deploy

### 🆕 Advanced Slash Command Patterns

Our slash commands use sophisticated patterns for maximum flexibility:

**Context Loading with `@`**:
```markdown
## Load Context
- @README.md
- @package.json
- @docs/architecture.md
```

**Reusable Variable Blocks**:
```markdown
## <analysis_instructions>
Analyze the request and determine complexity...
</analysis_instructions>

## <implementation_instructions>
Based on analysis, implement the solution...
</implementation_instructions>
```

**Stop Blocks for Workflow Control**:
```markdown
## <worktree_branch_check>
CRITICAL: Must be on main branch unless --worktree flag
</worktree_branch_check>
```

These patterns make slash commands intelligent prompts that guide Claude Code through complex workflows.

### Phase 1: Planning & Setup (Once per project)

```bash
# 1. Interactive project discovery
/project-setup
# Creates PROJECT_PLAN.md with vision & roadmap

# 2. Generate technical documentation
/plan:generate
# Creates detailed docs from vision

# 3. Generate test suites
/test:generate --all
# 90% test coverage before coding!
```

### Phase 2: Implementation (Daily work)

```bash
# Create issues for major features (10-20 total)
/create-issue "Add user authentication"
# Auto-assigns to Copilot if simple, Claude if complex

# Work on features
/work #150
# Creates branch, implements with tests

# Deploy when ready
/deploy
# Everything goes to Vercel
```

### ⚠️ Key Principles
- **Infrastructure tasks** = Local work (no issues needed)
- **Features** = GitHub issues (tracked and visible)
- **10-20 issues total** = Group related work together
- **Tests first** = Generate tests before implementation

---


### 📝 Work Journal System

**Automatic Activity Tracking** - The framework maintains a continuous work journal that:
- **Appends entries** every time Claude responds (never overwrites)
- **Tracks git state**: branch, uncommitted changes, unpushed commits
- **Session markers**: Special events like session_end are flagged
- **History preservation**: Keeps last 100 entries for work patterns
- **Located at**: `.claude/work-journal.json`


1. **Automatic Tracking**: TodoWrite usage tracked automatically
2. **Project Mapping**: Links todos to projects via session IDs
3. **Persistent Storage**: Todos in `~/.claude/todos/`, journal in `.claude/`
4. **Smart Filtering**: Bash scripts map sessions to projects
5. **Continuous Journal**: Hooks update work history on every response

### 🌳 Git Worktrees: Parallel Development (NEW!)

**Work on multiple issues simultaneously without disrupting your current work:**

```bash
# Work on issue in isolated worktree (doesn't affect current directory)
/work #123 --worktree

# Creates worktree at: worktrees/123-feature-name/
# Branches from origin/main automatically
# Your current work remains untouched
```

**Benefits of --worktree flag:**
- **No branch switching**: Stay on your current branch
- **Parallel work**: Multiple issues in separate directories
- **Clean isolation**: Each issue gets its own workspace
- **Auto-cleanup**: Worktrees removed after PR merge
- **Safe experimentation**: Test changes without affecting main work

### 🚀 Future GitHub Integration (Roadmap)

**Coming Soon**: Direct GitHub issue synchronization
- **Two-way sync**: TodoWrite ↔️ GitHub Issues
- **Auto-linking**: Todos automatically tied to issue numbers
- **PR tracking**: See which todos are in PRs
- **Status sync**: GitHub issue status updates Todo status
- **Milestone mapping**: Group todos by GitHub milestones
- **Team visibility**: Share todo progress via GitHub

This will create a unified development experience where local Claude Code work seamlessly integrates with GitHub's project management.

---

## 🤖 AI Agent Routing (When Activated)

### GitHub Copilot Handles (FREE)
- ✅ Simple implementations (Complexity ≤2, Size XS-S)
- ✅ Unit test writing
- ✅ Documentation updates
- ✅ Simple bug fixes
- ✅ Basic refactoring
- ✅ PR code reviews

### Claude Code Handles (LOCAL)
- 🧠 Complex features (Complexity ≥3)
- 🧠 Architecture decisions
- 🧠 Multi-file refactoring
- 🧠 Security implementations
- 🧠 Integration work
- 🧠 Large tasks (Size M+)

**Note**: Auto-routing to Copilot requires GitHub Actions to be fully operational (see issue #120)

---

## 📁 Project Structure

```
your-project/
├── 📋 .github/
│   ├── workflows/         # GitHub Actions CI/CD
│   └── ISSUE_TEMPLATE/    # Smart issue templates
├── 🤖 .claude/
│   ├── commands/          # Core slash commands
│   │   ├── create-issue.md
│   │   ├── work.md
│   │   ├── project-setup.md
│   │   ├── add-mcp.md
│   │   ├── deploy.md
│   │   └── copilot-review.md
│   ├── agents/            # Specialized sub-agents
│   └── hooks/             # Auto-sync & testing
├── 📚 docs/               # All documentation
├── 📖 Core Files
│   ├── README.md          # This file
│   └── CLAUDE.md          # AI instructions
```

---

## 🚀 Deployment

Everything deploys to **Vercel** automatically:

```bash
# Quick deploy
/deploy

# Or through work command
/work --deploy
```

**Vercel handles:**
- Frontend (React, Next.js, etc.)
- Backend APIs (serverless functions)
- Webhooks endpoints
- Global CDN
- Automatic HTTPS
- Preview deployments for PRs

---

## 🧰 Python Scripts as Utility Tools (NEW!)

**Python scripts in this framework are TOOLS, not decision-makers:**

```bash
scripts/utilities/
├── analyze-complexity.py      # Returns complexity score (data)
├── check-dependencies.py      # Lists dependent issues (data)
├── format-issue-body.py       # Formats markdown (transformation)
└── validate-pr-readiness.py   # Checks PR status (validation)
```

**Key Principle**: Python scripts are like MCP servers - they provide data/transformations, but Claude Code makes the decisions.

**Pattern**:
```python
# ✅ GOOD: Returns data for Claude to decide
def analyze_complexity(description):
    return {"score": 3, "factors": ["multi-file", "security"]}

# ❌ BAD: Makes decisions internally
def should_assign_to_copilot(description):
    if complexity > 2:
        return False  # Don't make decisions!
```

## 🪝 Strategic Hooks System

**6 essential hooks that fire at workflow boundaries, not every file change:**

### The 6 Working Hooks ✅
1. **SessionStart** (`load-context.sh`) - Loads git state, issues, PRs when you start
2. **UserPromptSubmit** (`verify-sync-before-claude.sh`) - Warns about unsynced changes before @claude
3. **Stop** (`work-checkpoint.sh`) - Commit reminders (5+/15+ changes, 3+ unpushed)
4. **SessionEnd** (`save-work-state.sh`) - Saves session state to work journal
5. **PostToolUse:TodoWrite** (`TodoWrite-post.sh`) - Auto-registers todo sessions with project
6. **Helper** (`register-session.sh`) - Links todo files to projects for proper tracking

### Hook Benefits
- **Minimal**: Only 6 hooks, all verified working
- **Strategic**: Fire at natural pauses, not constantly
- **Helpful**: Gentle reminders to commit and push
- **Invisible**: JSON output to Claude, not terminal spam
- **Auto-sync**: Todo persistence fixed automatically

See `.claude/hooks/README.md` for configuration details.

---

## 📚 Documentation

Essential guides:

### Planning & Setup
- `docs/development/DOCUMENT-GENERATION-FLOW.md` - Complete workflow diagram
- `docs/development/FIVE-TIER-SYSTEM.md` - Understanding the five tiers
- `templates/guides/*.md` - Templates for all documentation

### Development
- `docs/framework/WORKFLOW.md` - Development workflow and branch strategies
- `docs/framework/INFRASTRUCTURE_GUIDE.md` - How the framework automation works
- `docs/development/FLAGS.md` - All command flags reference

### Testing
- `docs/testing/API-MOCK-TESTING.md` - Newman/Postman API testing
- `docs/testing/TESTING-STRATEGY.md` - Comprehensive testing approach

### Configuration
- `CLAUDE.md` - AI assistant configuration and instructions
- `MCP_SERVERS_GUIDE.md` - MCP server setup and usage

---

## 🎯 Key Principles

1. **Issue-Centric**: Everything starts with a GitHub issue
2. **Two Commands**: `/create-issue` and `/work` handle everything
3. **Smart Routing**: AI automatically picks Copilot vs Claude
4. **Cost-Free**: No paid services required (uses free tiers)
5. **Unified Deploy**: Everything goes to Vercel

---

## 🔧 Available Commands

### Planning Commands (New!)
- `/project-setup` - Interactive discovery & create vision document
- `/plan:generate` - Generate detailed technical docs from vision
- `/test:generate` - Create comprehensive test suites

### Implementation Commands
- `/create-issue` - Create any type of work item
- `/work [#issue]` - Implement issues intelligently
- `/work [#issue] --worktree` - Work in isolated git worktree (NEW!)

### Utility Commands
- `/add-mcp` - Add MCP servers (GitHub, Supabase, Postman)
- `/deploy` - Quick Vercel deployment
- `/copilot-review` - Request PR review
- `/discussions` - Manage GitHub Discussions

---

## 💡 Complete Example: Building a SaaS App

```bash
# 1. Project Discovery (once)
/project-setup
> "Building a team collaboration tool"
> B2B SaaS, subscription model
> Creates: PROJECT_PLAN.md

# 2. Generate Documentation (once)
/plan:generate
> Creates: Technical specs from vision

# 3. Generate Tests (once)
/test:generate --all
> Creates: Complete test coverage

# 4. Build Features (ongoing)
/create-issue "User authentication system"
/create-issue "Team workspace management"
/create-issue "Real-time collaboration"
# Creates 10-20 major feature issues

# 5. Implementation
/work #1
> Copilot or Claude implements based on complexity

# 6. Deploy
/deploy
> Everything to Vercel
```

---

## 🎨 VSCode Settings Inheritance

Share consistent VSCode settings across all projects with multiple options:

### Quick Setup (Recommended)
```bash
# Apply settings globally to ALL projects
./scripts/utilities/vscode-settings-sync.sh --user
```

### Other Options Available:
1. **VSCode Profiles** (`--profile`) - Switch between different development contexts
2. **Symlink** (`--symlink`) - Projects always use latest template settings  
3. **Copy** (`--copy`) - Independent copy per project
4. **Git Template** (`--git-template`) - Auto-add to new git repos
5. **Settings Sync Extension** (`--extension`) - Sync across machines via GitHub Gist

See [VSCode Settings Guide](./docs/VSCODE-SETTINGS-INHERITANCE.md) for details.

---

## 🆓 Cost-Free Development

- **GitHub Copilot**: Free with GitHub Pro
- **Claude Code**: Uses your local API key
- **Vercel**: Generous free tier
- **Supabase**: Free tier for database
- **GitHub Actions**: 2000 free minutes/month

No @claude GitHub App fees!

---

## 🤝 Contributing

1. Fork the template
2. Create issues with `/create-issue`
3. Implement with `/work`
4. Submit PRs
5. Get Copilot reviews

---

<div align="center">

**Built with ❤️ by developers, for developers**

[Report Issues](https://github.com/vanman2024/multi-agent-claude-code/issues) • [Documentation](./docs) • [Discord](https://discord.gg/your-discord)

</div># Test deployment blocking Thu Sep  4 12:37:35 PDT 2025
