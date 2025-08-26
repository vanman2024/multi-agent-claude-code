# Multi-Agent Development Framework

## What is this?

This is a **template framework** for building AI-powered applications using multiple agents (GitHub Copilot, Claude Code, and custom agents) working together with comprehensive GitHub automation.

## Quick Start (After Cloning)

### 1. Get Your Copy

```bash
# Clone the template repository
git clone https://github.com/vanman2024/multi-agent-claude-code.git my-new-project
cd my-new-project

# Remove the template's git history and start fresh
rm -rf .git
git init
git add .
git commit -m "Initial commit from template"

# Add your own GitHub repo as origin
git remote add origin https://github.com/yourusername/your-new-repo.git
git push -u origin main
```

### 2. Install Required Tools

```bash
# Install CLI tools first
npm install -g newman vercel     # Postman and Vercel CLIs
brew install gh doctl             # GitHub and DigitalOcean CLIs (or apt install)
npx playwright install            # Download browser binaries for Playwright

# Add MCP servers (see templates/guides/MCP-SETUP.md for full details)
GITHUB_TOKEN=$(gh auth token)
claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer $GITHUB_TOKEN"
claude mcp add playwright -- npx @modelcontextprotocol/server-playwright
claude mcp add postman -- npx @modelcontextprotocol/server-postman
claude mcp add supabase -- npx @modelcontextprotocol/server-supabase
```

### 3. Run Project Setup

```bash
# Start Claude Code
claude

# Run the setup command
/setup-project
```

This will:
- Guide you through project type selection
- Set up GitHub repository and project board
- Configure Supabase database
- Link Vercel for frontend
- Set up DigitalOcean for backend
- Create all necessary secrets

### 4. Configure GitHub Secrets

Follow [secrets-setup.md](./secrets-setup.md) to add required secrets:

```bash
# Essential secrets
gh secret set ANTHROPIC_API_KEY
gh secret set SUPABASE_URL
gh secret set SUPABASE_ANON_KEY
gh secret set VERCEL_TOKEN
gh secret set DIGITALOCEAN_ACCESS_TOKEN
```

### 5. Install GitHub Apps

1. **GitHub Copilot** (Required)
   - Install from: https://github.com/apps/copilot
   - Enables autonomous task completion

2. **Claude Code GitHub App** (Optional)
   - Install from: https://github.com/apps/claude
   - Provides PR reviews and @claude mentions

### 6. Create Your First Feature

```bash
# Use the create-feature command
/create-feature user-authentication

# This will:
# 1. Create a GitHub issue with specs
# 2. Set complexity and size fields
# 3. Auto-assign to Copilot (if simple) or flag for agents
# 4. Create feature branch
# 5. Update project board
```

### 7. Build the Feature

```bash
# For complex features requiring local work
/build-feature

# This orchestrates multiple agents:
# - architect: Database design
# - backend-tester: API implementation
# - frontend-tester: UI components
# - All working together locally
```

## How The System Works

### Three-Layer Architecture

1. **GitHub Copilot** - Handles simple tasks (Complexity 1-2, Size XS/S)
2. **Local Agents** - Handle complex work with MCP servers
3. **GitHub Automation** - CI/CD, deployments, project tracking

### Workflow Pattern

```
Create Issue → Assign Agent → Local Development → Push → CI/CD → Deploy
```

### Key Commands

- `/setup-project` - Initial project configuration
- `/create-feature` - Create new feature with issue
- `/build-feature` - Build feature from issue
- `/refactor` - Improve existing code
- `/deploy` - Deploy to staging/production
- `/test` - Run test suites

## Project Structure

```
your-project/
├── .github/
│   ├── workflows/        # GitHub Actions automation
│   └── COPILOT-WORKFLOW.md  # Agent assignment rules
├── .claude/
│   ├── commands/         # Slash commands
│   ├── hooks/           # Local automation hooks
│   └── settings.json    # Hook configuration
├── src/                 # Your application code
├── tests/              # Test suites
└── CLAUDE.md           # AI assistant instructions
```

## Development Workflow

### For Simple Tasks (Copilot)
1. Create issue with `/create-feature`
2. Copilot auto-assigned if Complexity ≤ 2 AND Size ∈ {XS, S}
3. Copilot creates PR
4. CI/CD runs tests
5. Merge and deploy

### For Complex Tasks (Local Agents)
1. Create issue with `/create-feature`
2. Run `/build-feature` locally
3. Agents collaborate to implement
4. Test locally
5. Push to trigger CI/CD
6. Deploy automatically

## Customization

### Add Your Tech Stack

Edit `.claude/commands/project-setup.md` to define your stack:
- Frontend framework
- Backend language
- Database choice
- Authentication method
- Payment processor

### Configure Agents

See [agent-overview.md](./agent-overview.md) for what's included:
- frontend-tester
- backend-tester
- refactor
- architect
- security
- integrations
- reviewer

### Modify Workflows

GitHub workflows in `.github/workflows/`:
- Adjust deployment targets
- Change test commands
- Add environment-specific configs

## Documentation

- **[mcp-setup.md](./templates/guides/mcp-setup.md)** - Essential MCP servers and CLI tools setup
- **[design-specs.md](./templates/guides/design-specs.md)** - Frontend design specifications template
- **[secrets-setup.md](./secrets-setup.md)** - GitHub secrets configuration
- **[agent-overview.md](./agent-overview.md)** - Understanding the 7 agents
- **[copilot-workflow.md](./.github/copilot-workflow.md)** - Agent routing rules

## Next Steps

1. **Install MCP servers**: Follow templates/guides/mcp-setup.md first
2. **Start with infrastructure**: Create database schema
3. **Build incrementally**: Use `/create-feature` for each piece
4. **Let automation work**: Trust the GitHub workflows
5. **Monitor progress**: Check project board regularly

## Support

- **Issues**: Create in this template repo for framework bugs
- **Documentation**: See `/docs` folder for detailed guides
- **Updates**: Pull latest template changes carefully

Remember: This is a framework that orchestrates AI agents to build software faster. Let the automation do the heavy lifting!