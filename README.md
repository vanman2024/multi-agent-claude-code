# 🚀 Multi-Agent Development Framework (Template)

<div align="center">

![Version](https://img.shields.io/badge/Version-v2.0.0-purple?style=for-the-badge)
![GitHub](https://img.shields.io/badge/GitHub-Native-black?style=for-the-badge&logo=github)
![Copilot](https://img.shields.io/badge/GitHub_Copilot-Free-blue?style=for-the-badge&logo=github)
![Claude](https://img.shields.io/badge/Claude_Code-Local-orange?style=for-the-badge)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-black?style=for-the-badge&logo=vercel)

**⚠️ TEMPLATE FRAMEWORK: Clone this to bootstrap your AI-driven development**

**Simplified AI-driven development: Two commands, infinite possibilities**

[Quick Start](#-quick-start) • [Core Workflow](#-core-workflow) • [Documentation](#-documentation)

</div>

---

## 🎯 What's New in v2.0

**NEW PRIMARY WORKFLOW**: Work-in-Progress (WIP) driven development
- `/wip` - Start exploratory work WITHOUT issues (90% of daily work)
- `/wip branch-name` - Resume any existing branch instantly
- `/wip-status` - See all your WIP branches with worktree indicators

**SIMPLIFIED ISSUE WORKFLOW**: When you DO need issues
- `/create-issue` - Smart routing to Copilot (simple) or Claude (complex)
- `/work` - Full issue→PR→merge workflow with tracking

**WORKTREE SUPPORT**: Parallel development made easy
- Automatic worktree detection and navigation
- Option to create new branches as worktrees
- Visual indicators (📁) for worktree branches

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

### 3️⃣ Setup MCP Servers

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

### 4️⃣ Initialize Project

```bash
# One-time project setup
/project-setup

# This will:
# - Gather all your requirements
# - Configure tech stack
# - Set up GitHub repo
# - Initialize database
# - Configure Vercel deployment
```

---

## 🔄 Core Workflow (For Real Application Development)

### Primary: Issue-Driven Development

```bash
# 1. Create issue for any significant work
/create-issue "Add user authentication system"
# Issue #150 created - stays open during entire development

# 2. Start implementation
/work #150
# Creates branch: 150-add-user-authentication
# This branch lives for days/weeks as you build

# 3. Resume work across sessions
/wip 150-add-user-authentication
# Quick way to get back to your issue branch
# Work continues, issue stays OPEN

# 4. Create PR only when feature is complete
gh pr create --body "Closes #150"
# NOW the issue will close when PR merges
```

### Secondary: Quick Fixes & Experiments

```bash
# For tiny fixes (typos, small tweaks)
/wip fix-typo
# No issue needed for trivial changes

# For experiments before committing
/wip test-new-api
# Try things out, then create issue if it works

# See all your branches
/wip-status
# Shows both issue branches and experimental branches
```

### ⚠️ Auto-Sync Protection
Commands automatically `git pull` to prevent divergence. The `/wip` workflow embraces exploration while `/work` provides structure when needed.

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

## 📚 Documentation

Key documentation files:

- `docs/WORKFLOW.md` - Complete development workflow
- `docs/guides/TEMPLATE_PHILOSOPHY.md` - Core design principles  
- `docs/INFRASTRUCTURE_REQUIREMENTS.md` - Current implementation status
- `CLAUDE.md` - AI assistant instructions

---

## 🎯 Key Principles

1. **Issue-Centric**: Everything starts with a GitHub issue
2. **Two Commands**: `/create-issue` and `/work` handle everything
3. **Smart Routing**: AI automatically picks Copilot vs Claude
4. **Cost-Free**: No paid services required (uses free tiers)
5. **Unified Deploy**: Everything goes to Vercel

---

## 🔧 Available Commands

### Core Commands
- `/create-issue` - Create any type of work item
- `/work [#issue]` - Implement issues intelligently

### Utility Commands
- `/project-setup` - Initial project configuration
- `/add-mcp` - Add MCP servers
- `/deploy` - Quick Vercel deployment
- `/copilot-review` - Request PR review

### Archived Commands
Old commands like `/build-feature`, `/enhance`, etc. are archived.
Use `/work` for everything now!

---

## 💡 Examples

```bash
# Create a new feature
/create-issue
> Type: feature
> Title: Add user authentication
> Complexity: 3
> Size: M

# Work on it
/work #35

# Deploy when ready
/work --deploy

# Request review
/copilot-review
```

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
