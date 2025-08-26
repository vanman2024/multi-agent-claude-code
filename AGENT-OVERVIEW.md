# What's Included in This Template

This template comes pre-configured with everything you need for AI-powered development.

## 🤖 7 Specialized Agents (Already Configured)

Located in `.claude/agents/`:

| Agent | What It Does | When It's Used |
|-------|-------------|----------------|
| **frontend-tester** | Builds UI, writes tests, validates with Playwright | Frontend features, browser testing |
| **backend-tester** | Creates APIs, writes tests, validates with Postman | Backend features, API endpoints |
| **refactor** | Improves code quality, optimizes performance | Code cleanup, technical debt |
| **architect** | Designs databases, plans system architecture | Database schema, system design |
| **security** | Implements authentication, reviews security | Auth flows, security features |
| **integrations** | Connects external services, webhooks | Third-party APIs, service connections |
| **pr-reviewer** | Reviews code for standards and best practices | After code is written |

## ⚡ 6 Slash Commands (Ready to Use)

Located in `.claude/commands/`:

| Command | What It Does |
|---------|-------------|
| `/setup-project` | Configure your tech stack and deployment targets |
| `/create-feature` | Create GitHub issue → assign agent → create branch |
| `/build-feature` | Implement feature from issue using multiple agents |
| `/refactor` | Improve existing code across multiple files |
| `/enhance` | Add capabilities to existing features |
| `/add-mcp` | Add new MCP servers for additional tools |

## 🔄 3 Local Hooks (Auto-Running)

Located in `.claude/hooks/` and configured in `.claude/settings.json`:

| Hook | When It Runs | What It Does |
|------|-------------|--------------|
| **current-work.sh** | Every prompt | Injects current issue context from git branch |
| **auto-commit.sh** | After file edits | Creates atomic commits automatically |
| **test-before-push.sh** | Before git push | Runs tests to prevent broken code |

## 🚀 How It All Works Together

### 1. Starting a Feature
```bash
/create-feature user-authentication
```
This creates a GitHub issue, determines complexity, and assigns the right agent.

### 2. Task Routing
- **Simple tasks** (Complexity 1-2 AND Size XS/S) → GitHub Copilot handles autonomously
- **Complex tasks** → Claude Code agents work locally with you

### 3. Development Flow
```
Create Issue → Assign Agent → Local Work → Auto-commit → Push → CI/CD → Deploy
```

### 4. Using Claude Code CLI
```bash
# Start Claude Code in your project
claude

# The hooks automatically:
# - Know what issue you're working on
# - Commit your changes as you work
# - Test before pushing

# Run commands directly
/build-feature  # Implements current issue
/refactor      # Improves code quality
/test          # Runs appropriate tests
```

## 📁 File Structure

```
.claude/
├── agents/           # 7 pre-configured agents
│   ├── frontend-tester.md
│   ├── backend-tester.md
│   ├── refactor.md
│   └── ...
├── commands/         # 6 slash commands
│   ├── setup-project.md
│   ├── create-feature.md
│   └── ...
├── hooks/           # 3 automation hooks
│   ├── current-work.sh
│   ├── auto-commit.sh
│   └── test-before-push.sh
└── settings.json    # Hook configuration
```

## 🔧 Customization

### Add Your Own Agents
1. Create `.claude/agents/your-agent.md`
2. Define tools and model to use
3. Use with `Task` tool and `subagent_type: "your-agent"`

### Add Your Own Commands
1. Create `.claude/commands/your-command.md`
2. Define the workflow
3. Use with `/your-command`

### Modify Hooks
1. Edit scripts in `.claude/hooks/`
2. Update `.claude/settings.json` for when they trigger

## 🎯 Quick Start

1. **Clone this template**
2. **Run `/setup-project`** to configure your stack
3. **Create your first feature** with `/create-feature`
4. **Let the agents build it** with `/build-feature`

Everything is pre-configured and ready to use. No additional setup needed for the agents - just start building!