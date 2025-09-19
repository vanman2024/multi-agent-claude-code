# Claude Code Documentation - Multi-Agent Template Framework

## CRITICAL: GitHub Repository Information
**Repository Owner**: vanman2024 (NOT gotime2022)
**Repository Name**: multi-agent-claude-code
**Full Path**: github.com/vanman2024/multi-agent-claude-code

## THIS IS A TEMPLATE FRAMEWORK

**Important**: You are working in a template repository that will be cloned to create new projects. This is NOT the actual project - it's the framework for building projects.

## CRITICAL: Project Constitution
**ALWAYS check for and incorporate `.specify/memory/constitution.md` if it exists in the project**. This file contains project-specific principles, constraints, and rules that override general instructions. The constitution is created during project setup and contains:
- Core development principles for the specific project
- Technology stack constraints
- Testing requirements
- Project-specific workflows
- Governance rules

Check for constitution at: `.specify/memory/constitution.md`

## Template Purpose

This Multi-Agent Development Framework template provides:
- Pre-configured GitHub automation workflows
- Agent orchestration system (Copilot + Claude Code agents)
- Slash commands for common development tasks
- Project board integration with complexity/size routing
- Automated CI/CD pipelines

When someone clones this template, they get a complete development framework ready to build their actual application.

## Working Modes

### Template Mode (Building the Framework)
**Use this mode when developing/improving this template repository itself**

- **Direct commits allowed** for template improvements
- **PRs optional** for significant changes  
- **Simplified workflow** since no CI/CD is running on template
- **Flexible approach** to quickly iterate on framework features

**When to use Template Mode:**
- Adding new slash commands
- Updating documentation
- Fixing workflow automation
- Improving agent configurations
- General template maintenance

**Workflow in Template Mode:**
```bash
git pull
# make changes directly
git add -A
git commit -m "feat: Add new feature to template"
git push
```

### Application Mode (Using the Framework)
**Use this mode when building actual applications with this template**

- **STRICT workflow required**: Issue → PR → Review → Merge
- **All changes need PRs** with proper reviews
- **Full CI/CD validation** on every PR
- **No direct commits** to main branch
- **Complete testing** before merge

**When to use Application Mode:**
- Building production applications
- Working with a team
- When CI/CD is configured
- For any code that will be deployed

**Workflow in Application Mode:**
```bash
/create-issue "Add user authentication"
/work #123  # Creates branch and draft PR
# implement with tests
# PR review process
# CI/CD validation
# Merge when all checks pass
```

### Key Distinction
- **Template Mode** = Building/improving the framework itself (flexible)
- **Application Mode** = Using the framework to build apps (strict)

When you clone this template for a new project, immediately switch to Application Mode and follow the full workflow.

## 🤖 @Symbol Multi-Agent Coordination System

### Revolutionary Coordination Approach
This project now uses the **@symbol coordination system** - a breakthrough in AI agent collaboration that integrates seamlessly with Claude Code's existing subagent architecture.

### How @Symbol Coordination Works with Claude Code
- **@claude**: Uses Claude Code's full subagent system (general-purpose, code-refactorer, pr-reviewer, etc.)
- **@copilot**: GitHub Copilot handles simple tasks (Complexity ≤2, Size XS-S) 
- **@qwen**: Local Qwen CLI for everyday coding tasks (FREE until rate limits)
- **@gemini**: Large document/codebase analysis via CLI (2M context, ~$0.075/million tokens using gemini-1.5-flash)
- **@codex**: Interactive development and prototyping

### Claude Code Subagent Integration
Claude Code's specialized agents work within the @symbol system:
- **@claude/general-purpose**: Complex multi-step tasks and research
- **@claude/code-refactorer**: Large-scale refactoring and optimization
- **@claude/pr-reviewer**: Code review and standards compliance
- **@claude/backend-tester**: API testing and validation
- **@claude/integration-architect**: Multi-service integrations
- **@claude/system-architect**: Database and API architecture
- **@claude/security-auth-compliance**: Authentication and security
- **@claude/frontend-playwright-tester**: End-to-end UI testing

### Primary Slash Commands

The two main commands you'll use 90% of the time:

#### 1. `/create-issue` - Universal Issue Creation
Creates ANY type of work item with automatic routing:
```bash
/create-issue "Add user authentication"
```
- Handles: features, bugs, enhancements, refactors, tasks
- Auto-assigns to Copilot for simple work (Complexity ≤2, Size XS/S)
- Routes complex work to Claude Code agents
- Applies proper labels and milestones

#### 2. `/work` - Universal Work Implementation  
One command for ALL implementation needs:
```bash
/work #123           # Work on specific issue
/work                # Auto-pick next issue from sprint
/work --deploy       # Deploy current work
/work --test         # Run tests for current work
```
- Intelligently selects next task based on priorities
- Analyzes dependencies and blockers
- Creates branches and PRs automatically
- Updates issue status throughout

#### Other Available Commands
- `/hotfix` - Emergency fixes that bypass normal workflow
- `/deploy` - Deploy to production
- `/copilot-review` - Request Copilot code review
- `/pr-comments` - Manage PR review comments
- `/add-mcp` - Add new MCP servers
- `/project-setup` - Initialize new project from template
- `/discussions` - Manage GitHub Discussions (see examples below)

#### 3. `/discussions` - GitHub Discussions Management
Manage ideas and discussions without cluttering the codebase:
```bash
/discussions                    # Show menu with 6 options
/discussions "new feature idea" # Quick create discussion
/discussions 125                # View discussion #125
```
- Create, list, and view GitHub Discussions
- Convert discussions to actionable issues
- Find overlapping discussions and issues
- Consolidate related discussions into unified work items

### Best Practices
- Use `/create-issue` to create issues with proper routing
- Simple tasks auto-assign to GitHub Copilot (free with GitHub Pro)
- Complex tasks require local Claude Code agents

### CRITICAL: Slash Command Rules
**ALWAYS use the templates in `/templates/slash-command-templates.md` when creating slash commands!**

**Key principles:**
- Keep commands SIMPLE - they should just run, not require complex logic
- Use the `!` syntax for bash commands (e.g., `!git status`)
- Use `@` for file references (e.g., `@package.json`)
- Use `$ARGUMENTS` for user input (passed directly from command)
- Use MCP functions directly (e.g., mcp__github__create_issue)

**NEVER use in slash commands:**
- Template placeholders like `<pattern>`, `<path>`, `<search_term>`
- Complex bash substitutions like `$(git rev-list --all)`
- Variables that need to be saved like `DELETE_COMMIT`
- Multi-step logic that requires state management
- Code blocks for implementation

**ALWAYS follow this structure:**
```markdown
---
allowed-tools: Bash(*), Read(*)
description: Brief description
argument-hint: [what user should provide]
---

# Command Name

## Your Task
[Simple description]

Run: !git [actual command that works]
```

- Follow the templates EXACTLY from `/templates/slash-command-templates.md`
- Test commands manually first to ensure they work
- Use `/work` for actual implementation, not slash commands

### /discussions Command Examples

**Interactive Menu** (no arguments):
```bash
/discussions
# Shows menu with 4 options:
# 1. Create new discussion
# 2. List existing discussions
# 3. Convert discussion to issue
# 4. View specific discussion
```

**Quick Create** (with topic):
```bash
/discussions "Add OAuth authentication support"
# Creates discussion directly with that title
```

**Quick View** (with number):
```bash
/discussions 125
# Views Discussion #125 directly
```

**Conversion Flow**:
- Analyzes discussion content for keywords
- Suggests type: bug (if has "fix/broken"), feature (if has "new/add"), or task
- User can override suggestion
- Creates issue using appropriate template
- Adds comment to discussion linking to new issue

## 🚀 Ops CLI Automation System

### Solo Developer Automation Made Simple

This template includes a powerful `ops` CLI automation system designed specifically for solo developers working with multiple AI agents. The system provides a unified interface for all development operations without over-engineering.

### Quick Setup for New Projects

When you run `sync-project-template.sh`, you automatically get:
- **scripts/ops** - Single automation CLI command
- **.automation/config.yml** - Unified configuration
- **Automated git hooks** (optional) for seamless workflow

### Core Operations Workflow

**Daily Development:**
```bash
ops qa                    # Quality checks (lint, test, format) - all tests
ops qa --backend          # Backend-only QA (Python/pytest)
ops qa --frontend         # Frontend-only QA (Playwright/TypeScript)
ops build --target PATH  # Build production version locally
ops verify-prod          # Test production build works
ops status                # Show current state and versions
```

**Release When Ready:**
```bash
ops release patch    # For bug fixes (v0.4.2 → v0.4.3)
ops release minor    # For new features (v0.4.2 → v0.5.0) 
ops release major    # For breaking changes (v0.4.2 → v1.0.0)
```

**Environment Management:**
```bash
ops env doctor       # Check WSL/Windows environment issues
ops setup TARGET     # Setup operations and target directory
ops sync             # Sync to all configured targets
```

### How It Integrates with Multi-Agent Development

**For @claude (You):**
- Always run `ops qa --backend` for Python/API work
- Use `ops qa --all` for full-stack changes
- Use `ops status` to check project state
- Run `ops env doctor` if environment issues arise
- Ensure `ops build` succeeds before marking work complete

**For @copilot:**
- Include `ops qa --frontend` for UI/UX work
- Include `ops qa --all` in PR workflows
- Check `ops status` for version information
- Use `ops verify-prod` to validate changes

**For @gemini and @qwen:**
- Reference `ops status` for current project state
- Include automation commands in documentation
- Validate environment with `ops env doctor`

### Agent Coordination with Ops CLI

**Before Starting Any Task:**
```bash
git pull                 # Get latest changes
ops status              # Check current project state
ops qa                  # Ensure clean starting point
```

**Before Completing Any Task:**
```bash
ops qa                  # Lint, test, format all code
ops build --target /tmp/test-build  # Verify production build
ops verify-prod /tmp/test-build     # Test production works
# Only then commit and mark task complete
```

**For Release Coordination:**
```bash
# Agents should suggest release when ready:
ops release patch       # For completed bug fixes
ops release minor       # For completed features
ops release major       # For breaking changes
```

### Configuration for Different Project Types

The `.automation/config.yml` adapts to your project:

**Python Projects:**
```yaml
versioning:
  source: pyproject.toml
qa:
  lint: ruff check .
  typecheck: mypy src
  tests: pytest -m "not slow"
```

**Node.js Projects:**
```yaml
versioning:
  source: package.json
qa:
  lint: npm run lint
  typecheck: npm run typecheck
  tests: npm test
```

**Multi-Language Projects:**
```yaml
qa:
  lint: true           # Auto-detects linters
  typecheck: true      # Auto-detects type checkers
  tests: "not slow"    # Runs appropriate test command
```

### Benefits for Multi-Agent Teams

1. **Consistent Quality:** All agents use same QA standards via `ops qa` (backend/frontend/all)
2. **Reliable Builds:** `ops build` ensures production readiness
3. **Clear State:** `ops status` shows what's deployed where
4. **Environment Safety:** `ops env doctor` catches WSL/path issues
5. **Simple Releases:** Semantic versioning with `ops release`

### Integration with Existing Workflows

**With GitHub Actions:**
```yaml
- name: Backend Quality Checks
  run: ./scripts/ops qa --backend

- name: Frontend Quality Checks  
  run: ./scripts/ops qa --frontend

- name: Production Build
  run: ./scripts/ops build --target dist/
```

**With Local Development:**
```bash
# Backend development
./scripts/ops qa --backend && ./scripts/ops build --target ~/deploy/

# Frontend development
./scripts/ops qa --frontend

# Full-stack changes
./scripts/ops qa --all && ./scripts/ops build --target ~/deploy/
```

### Troubleshooting for Agents

**Common Issues:**
- `ops env doctor` - Diagnose WSL/Windows path problems
- `ops status` - Check if project is properly configured
- `ops qa --help` - Get available quality check options

**Before Asking User:**
1. Run `ops env doctor` to check environment
2. Check `ops status` for configuration issues
3. Try `ops qa` to see if basic operations work

This automation system eliminates the confusion of multiple scripts and provides a single, reliable interface that all agents can use consistently.

## System Architecture: The House Metaphor 🏗️

Think of our system like building a house:

### The Layers of Construction

1. **Foundation (Database & Data Layer)**
   - Like concrete foundation - must be solid and unchanging
   - Tables, schemas, core data structures
   - Once set, expensive to change

2. **Plumbing (GitHub Automation & CI/CD)**
   - Carries things from place to place
   - No intelligence - just moves water (data/issues/code)
   - Workflows that route, deploy, test
   - **"Automation = Plumbing, Not Decision Making"**

3. **Framing (Backend Services & APIs)**
   - The structural support of the house
   - Load-bearing walls that hold everything up
   - API endpoints, service layers, business logic

4. **Electrical (Agent System & Intelligence)**
   - Powers the smart features of the house
   - Claude Code = Main electrical panel (controls everything)
   - Agents = Individual circuits (specialized tasks)
   - Makes intelligent decisions about what to power and when

5. **Drywall & Finishes (Frontend & UI)**
   - What users see and interact with
   - Can be changed without affecting structure
   - React components, UI elements, styling

6. **Smart Home System (Project Board & Orchestration)**
   - The control center that monitors everything
   - Doesn't make decisions, just shows status
   - GitHub Project Board tracks what's happening where

### Key Principle: Each Layer Has Its Role

- **Plumbing doesn't think** - it just moves things
- **Electrical makes decisions** - turns things on/off intelligently  
- **Foundation never changes** - or the house collapses
- **Finishes can be updated** - without touching structure

This is why our GitHub workflows (plumbing) should NEVER make intelligent decisions - they just move issues to boards, run tests, deploy code. The intelligence comes from Claude Code and agents (electrical system).

## Agent Assignment Rules

### The Golden Rule: Copilot Gets Small AND Simple Tasks

**Copilot ONLY handles tasks that are BOTH:**
- **Complexity**: 1-2 (out of 5) - Simple, straightforward logic
- **Size**: XS or S - Less than 2 hours of work

If either complexity > 2 OR size > S → Claude Code handles it.

### Quick Decision Matrix

| Complexity | Size | Agent | Example |
|------------|------|-------|---------|
| 1-2 | XS-S | Copilot | Fix typo, add endpoint, simple test |
| 1-2 | M-XL | Claude | Large refactor (too big for Copilot) |
| 3-5 | Any | Claude | Architecture, security, complex logic |

### How It Works

When creating issues via `/create-issue`:
```javascript
const isSmallAndSimple = (complexity <= 2) && (size === 'XS' || size === 'S');
if (isSmallAndSimple) {
  // Automatically assign to Copilot via MCP
  await mcp__github__assign_copilot_to_issue({...});
}
```

**See full workflow details:** [.github/COPILOT-WORKFLOW.md](./.github/COPILOT-WORKFLOW.md)

## CRITICAL WORKFLOW: Issue → PR → Merge → Deploy

### ⚠️ NEVER Skip Steps in This Workflow (Except for Minor Doc Updates)

**The Golden Rule**: ALWAYS create an issue BEFORE creating a PR

**EXCEPTIONS - Direct commits OK for:**
- Adding examples to existing documentation
- Fixing typos or grammar
- Clarifying existing documentation
- Updating comments in code
- Formatting improvements (no logic changes)

These are typically ignored by git history anyway and creating issues/PRs for every typo would be counterproductive.

### 🔄 MANDATORY PULL POINTS (Prevent Divergence)

**ALWAYS run `git pull` at these points:**
1. **Before creating any issue** - Start from latest code
2. **After ANY PR merges** (yours, Copilot's, anyone's) - Stay synced
3. **Before running `/work`** - Start implementation from latest
4. **Before making ANY commits** - Ensure you're not duplicating work
5. **Start of each work session** - Always begin fresh

**Why this matters:**
- Copilot works in GitHub, you work locally
- Without pulling, you're working on OLD code
- You could be fixing things already fixed
- Massive conflicts and wasted work

1. **Research Phase** (Planning)
   - Use TodoWrite to plan complex tasks
   - Think through the approach first
   - Don't create issues until strategy is solid

2. **Issue Creation** (Planning) - Use `/create-issue`
   ```bash
   git pull  # MANDATORY: Sync before creating issue
   /create-issue "Clear description of WHAT needs to be built"
   ```
   - Universal command for ALL issue types
   - Issues are planning documents (NO code yet)
   - Automatically determines complexity and routing
   - Auto-assigns to Copilot for simple tasks
   - NO branches created at this point
   - NO PRs created at this point

3. **Start Work** (Implementation) - Use `/work`
   ```bash
   git pull  # MANDATORY: Sync before starting work
   /work #123  # This creates branch AND draft PR
   ```
   - Universal command for ALL implementation
   - NOW branch is created  
   - NOW draft PR is created with "Closes #123" link
   - All commits go in the PR
   - Also supports: `/work` (auto-select), `/work --test`, `/work --deploy`

4. **Complete Work**
   - Check all PR checkboxes
   - Run tests and linting
   - Convert draft to ready
   - Request review if needed

5. **Merge**
   ```bash
   gh pr merge --squash --delete-branch
   ```
   - Issue auto-closes via "Closes #123"
   - Branch is deleted
   - Deployment triggers (if configured)

### 📝 CRITICAL: All Commits Must Reference the Issue

**GitHub requires explicit issue references in EVERY commit message** for them to appear in the issue timeline.

Even though your branch is named `123-feature-name` and was created with `gh issue develop 123`, GitHub will NOT automatically link commits to the issue. This is a GitHub limitation.

**EVERY commit must include the issue number:**
```bash
# ✅ CORRECT - These will show in issue timeline:
git commit -m "feat: Add authentication

Related to #123"

git commit -m "fix: Update validation logic #123"

git commit -m "docs: Update README

Part of #123"

# ❌ WRONG - These will NOT show in timeline:
git commit -m "feat: Add authentication"  # No issue reference!
```

**Reference types to use:**
- `Related to #123` - For most commits
- `Part of #123` - For partial work
- `Updates #123` - For updates
- `#123` - Simple reference
- `Closes #123` - ONLY in final PR or last commit (use once!)

**Why this matters:**
- Without references, commits are invisible in issue timeline
- Can't track what work was done for an issue
- Loses audit trail and traceability
- Makes debugging and reviews difficult

### ❌ Common Mistakes to AVOID

**NEVER DO THIS:**
- Create PR without issue first (like I did with PR #73)
- Create branches when issues are created
- Make commits without a PR
- Work without an issue number
- Skip the research/planning phase

**ALWAYS DO THIS:**
- Issue first, then PR
- Use `/work` command to start implementation
- Keep issues as planning docs only
- Put all code/commits in PRs

## Working with GitHub Discussions

### Adding Comments to Discussions
To add a comment to a GitHub Discussion, you need to:
1. First get the discussion ID using GraphQL
2. Then use that ID with the addDiscussionComment mutation

```bash
# Get discussion ID
DISCUSSION_ID=$(gh api graphql -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    discussion(number: NUMBER) {
      id
    }
  }
}' --jq .data.repository.discussion.id)

# Add comment
gh api graphql -f query='
mutation($discussionId: ID!, $body: String!) {
  addDiscussionComment(input: {discussionId: $discussionId, body: $body}) {
    comment { id }
  }
}' -F discussionId="$DISCUSSION_ID" -F body="Your comment text"
```

## Gemini CLI Configuration - Dual Terminal Setup

### 🚀 MAXIMIZE BOTH FREE MODELS

We now have TWO powerful Gemini models running FREE:
1. **Terminal 1**: Google OAuth → **Gemini 2.5 Pro** (FREE on personal accounts!)
2. **Terminal 2**: API Key → **Gemini 2.0 Flash Experimental** (FREE while in experimental!)

### Setup Instructions

#### Terminal 1: Google OAuth (Gemini 2.5 Pro)
```bash
# Just run gemini - API keys are commented out in .bashrc
gemini
# Choose option 1: Login with Google
# You'll get Gemini 2.5 Pro FREE on personal accounts
```

#### Terminal 2: API Key (Gemini 2.0 Flash Experimental)
```bash
# Source the setup script to enable API key for this terminal only
source /home/gotime2022/bin/gemini-setup-experimental.sh
# Now use the free experimental model
gemini -m gemini-2.0-flash-exp
```

### Model Comparison & Strategy

| Model | Auth Method | Cost | Context | Best For |
|-------|------------|------|---------|----------|
| **Gemini 2.5 Pro** | Google OAuth | FREE (personal) | 1M tokens | Complex reasoning, advanced tasks |
| **Gemini 2.0 Flash Exp** | API Key | FREE (experimental) | 1M tokens | Fast responses, agentic tasks |
| **Claude Code** | N/A | Via subscription | N/A | Architecture, complex debugging |

### Usage Strategy - Use ALL THREE to Maximum Advantage
1. **Gemini 2.0 Flash Exp** (Terminal 2): Rapid prototyping, quick questions, bulk processing
2. **Gemini 2.5 Pro** (Terminal 1): Complex analysis, when Flash Exp can't handle it
3. **Claude Code**: Architecture decisions, complex multi-file refactoring, debugging

### CRITICAL: Both Gemini Models are FREE
- **2.5 Pro**: Free on personal Google accounts (would cost $1.25/M input + $10/M output otherwise!)
- **2.0 Flash Exp**: Completely free during experimental phase (normally $0.10/M input + $0.40/M output)
- **USE THEM BOTH TO THE MAX WHILE THEY'RE FREE!**

### Configuration Files
- **API Key Script**: `/home/gotime2022/bin/gemini-setup-experimental.sh` (sets API key for terminal session)
- **API Keys**: Commented out in `~/.bashrc` (lines 192-193) to allow Google OAuth by default

## Working with MCP Servers

MCP (Model Context Protocol) servers allow Claude to interact with external tools and services. 

📚 **See the complete MCP Servers Guide**: [MCP_SERVERS_GUIDE.md](./MCP_SERVERS_GUIDE.md)

### Quick Reference

```bash
# Add servers
claude mcp add <name> -- <command>                    # Local stdio server
claude mcp add --transport http <name> <url>          # Remote HTTP server
claude mcp add --transport sse <name> <url>           # Remote SSE server

# Manage servers
claude mcp list                                       # List all servers
claude mcp get <name>                                 # Get server details
claude mcp remove <name>                              # Remove a server
/mcp                                                  # Check status/authenticate (in Claude Code)
```

The MCP_SERVERS_GUIDE.md contains:
- Popular MCP servers with installation commands
- Authentication setup
- Configuration scopes (local/project/user)
- Troubleshooting tips
- Security best practices

## Reading Windows Files and Screenshots in WSL

When working in WSL and needing to read Windows files (especially screenshots), use the WSL mount path:
- Windows path: `C:/Users/user/Pictures/Screenshots/screenshot.png`
- WSL path: `/mnt/c/Users/user/Pictures/Screenshots/screenshot.png`

Replace `C:/` with `/mnt/c/` and forward slashes throughout. This allows Claude Code to access Windows files from the WSL environment.

## VS Code Settings Changes

**IMPORTANT**: After modifying `.vscode/settings.json`, always restart VS Code to apply changes. Settings like Vim extension disable, formatters, and other configurations only take effect after restart.

## File Naming Conventions

### STRICT RULE: Consistent naming conventions

#### Special Files (UPPERCASE for recognition):
- `README.md` - GitHub specifically looks for this
- `CLAUDE.md` - Makes it clear this is for Claude Code  
- `LICENSE` - Standard convention
- `CHANGELOG.md` - If you have one

#### All Other Documentation (lowercase with hyphens):
- **Guide files**: `design-specs.md`, `mcp-setup.md`, `api-guide.md`
- **Config files**: `package.json`, `tsconfig.json`, `.env.example`
- **Code files**: `user-profile.ts`, `api-handler.js`, `database-schema.sql`

### ✅ ALWAYS:
- Use lowercase with hyphens for non-special files
- Be consistent within a project
- Use `.md` not `.MD` or `.markdown`

### ❌ NEVER:
- Mix naming styles randomly (pick a convention and stick to it)
- Use underscores in markdown files (use hyphens instead)
- Create variations like `ReadMe.md` or `Readme.MD`

## File Management Rules

### Prevent File Bloat
- NEVER create temporary test files - run tests in memory or use existing test files
- NEVER create duplicate documentation - always check for existing docs first
- NEVER create "example" or "sample" files unless explicitly requested
- ALWAYS clean up temporary files created during debugging
- ALWAYS prefer modifying existing files over creating new ones
- NEVER create backup copies (like file.old, file.backup) - rely on git
- NEVER create scratch/draft files - work directly in target files

### Before Creating Any File
1. Check if a similar file already exists
2. Verify the file will be actively used in the codebase
3. Ensure it's not a one-time use case
4. Confirm user explicitly requested its creation

### Cleanup Protocol
- Remove unused imports after refactoring
- Delete commented-out code blocks
- Remove console.logs and debug statements
- Clean up test files that were only for verification

## Documentation Rules

### CRITICAL: Prevent Documentation Duplication
**BEFORE creating ANY documentation:**
1. **SEARCH for existing docs first**:
   ```bash
   find . -name "*.md" | xargs grep -l -i "topic"
   ```
2. **CHECK if topic is already covered**:
   - WORKFLOW.md covers ALL workflow-related topics
   - docs/CHECKBOXES.md covers ALL checkbox topics  
   - CLAUDE.md covers ALL AI assistant instructions
   - MCP_SERVERS_GUIDE.md covers ALL MCP server topics
3. **UPDATE existing docs instead of creating new ones**
4. **CONSOLIDATE similar topics into single documents**

**Examples of what NOT to do:**
- ❌ Creating WORKFLOW_GUIDE.md when WORKFLOW.md exists
- ❌ Creating CHECKBOX_STRATEGY.md when docs/CHECKBOXES.md exists
- ❌ Creating MCP_SETUP.md when MCP_SERVERS_GUIDE.md exists

### CRITICAL: File Naming Convention
- **ALL DOCUMENTATION FILES MUST BE UPPERCASE**: README.md, CLAUDE.md, SETUP.md, etc.
- **NEVER use lowercase for documentation**: No readme.md, setup.md, guide.md
- **ALWAYS maintain consistency**: If it's documentation, it's UPPERCASE
- **Exception**: Only code files and configs use lowercase (package.json, index.js, etc.)

### Core Documentation Only
During development, maintain ONLY these essential documents:
- **README.md** - Project overview, setup, and quick start
- **CLAUDE.md** - AI assistant instructions (this file)
- **MCP-SERVERS-GUIDE.md** - MCP server reference (if using MCP)
- **API.md** - API endpoints (only if building an API)
- **CONTRIBUTING.md** - Contribution guidelines (only for open source)

### Documentation Principles
- **NO SPRAWL**: Do not create multiple documentation files
- **NO NOTES FILES**: Never create TODO.md, NOTES.md, THOUGHTS.md, IDEAS.md
- **NO DRAFTS**: Never create documentation drafts or WIP docs
- **NO EXAMPLES**: Do not create example or tutorial documentation during development
- **NO ARCHITECTURE DOCS**: Until explicitly requested for production
- **NO CHANGELOG**: Use git commits and PR descriptions instead

### When Asked About Documentation
- **UPDATE existing docs** rather than creating new ones
- **USE code comments** for implementation details
- **RELY on git history** for change tracking
- **WAIT for explicit request** before creating any new documentation

### Documentation Location Rules
- Keep all docs organized in /docs folder
- Exception: README.md and CLAUDE.md remain in root
- Never scatter README files throughout the codebase
- Never create documentation subfolders until product launch

### User Documentation vs Build Documentation
- During development: Focus only on build/developer documentation
- User documentation comes AFTER product is functional
- Never preemptively create user guides or tutorials
- API documentation only when API is complete and stable

## Testing & QA Standards

### Dual Testing Architecture
This template provides both backend and frontend testing capabilities:

**Backend Testing** (`backend-tests/`):
- **Python/pytest** for API logic, data processing, integrations
- **Structure**: smoke, unit, integration, contract, performance, e2e, helpers
- **Run**: `./scripts/ops qa --backend` or `python3 run.py -m pytest backend-tests/`
- **Coverage**: `pytest --cov=src --cov-report=term-missing backend-tests/`

**Frontend Testing** (`frontend-tests/`):
- **Playwright/TypeScript** for UI, E2E, visual, accessibility testing
- **Structure**: e2e, api, visual, accessibility, utils, config
- **Setup**: Run `./frontend-tests-template/setup-testing.sh` to activate
- **Run**: `./scripts/ops qa --frontend` or `npm run test:frontend`

### Testing Workflow
```bash
# Backend development (Python/API)
./scripts/ops qa --backend

# Frontend development (UI/UX)
./scripts/ops qa --frontend

# Full-stack changes
./scripts/ops qa --all

# Individual test suites
python3 run.py -m pytest backend-tests/unit/
npm run test:frontend:e2e
```

### API Testing with Postman
- **Postman MCP server**: Pre-configured for all agents
- **Contract Testing**: Use `mcp__postman__*` functions for API testing
- **Newman CLI**: Run collections with `newman run collection.json`
- **Mock Servers**: Create mock APIs for frontend development
- **Integration**: Part of `ops qa --backend` pipeline

### Agent Testing Responsibilities
- **@claude**: Backend testing, Python/pytest, API contract tests
- **@copilot**: Frontend testing, Playwright, UI component tests  
- **@gemini**: Integration testing, cross-browser validation
- **@qwen**: Performance testing, accessibility compliance

## Code Style & Conventions

### Language-Specific Rules
- **TypeScript**: Use strict mode, prefer interfaces over types, explicit return types
- **Python**: Follow PEP 8, use type hints for all functions, docstrings for public functions
- **React**: Functional components only, use hooks not classes, memo for expensive components
- **Node.js**: Use async/await over callbacks, handle Promise rejections
- **Database**: Always use transactions for multiple operations, parameterized queries

### Naming Conventions
- Files: kebab-case (user-profile.ts, api-handler.js)
- React Components: PascalCase file and component (UserProfile.tsx)
- Functions: camelCase (getUserProfile, calculateTotal)
- Constants: UPPER_SNAKE_CASE (MAX_RETRY_COUNT, API_BASE_URL)
- Database: snake_case for tables/columns (user_accounts, created_at)
- CSS/SCSS: kebab-case for classes (user-profile-card)
- Environment vars: UPPER_SNAKE_CASE with prefix (REACT_APP_, NEXT_PUBLIC_)

## Common Commands & Scripts

### ALWAYS run these before marking any task complete:
```bash
# Backend work (Python/API)
./scripts/ops qa --backend    # Lint, format, typecheck, test backend

# Frontend work (UI/UX)
./scripts/ops qa --frontend   # Lint, typecheck, test frontend

# Full-stack changes
./scripts/ops qa --all        # Complete QA pipeline

# Individual commands (if ops not available)
ruff check src/ --fix         # Python linting
mypy src/                     # Python type checking
python3 run.py -m pytest backend-tests/  # Backend tests
npm run lint:frontend         # Frontend linting  
npm run test:frontend         # Frontend tests
```

### If commands are unknown:
- Check package.json scripts section
- Check README.md for commands
- Ask user for the correct commands
- Suggest adding them to this section

## Error Handling Patterns

### NEVER:
- Use empty try-catch blocks
- Catch errors without logging context
- Return generic "Something went wrong" messages
- Ignore Promise rejections
- Use catch without proper error handling

### ALWAYS:
- Log error with context (user ID, action, timestamp)
- Return specific, actionable error messages
- Use error boundaries in React applications
- Handle both sync and async errors
- Preserve error stack traces in development

### Error Pattern:
```javascript
try {
  // operation
} catch (error) {
  console.error('Specific context:', { userId, action, error });
  throw new Error(`Failed to [specific action]: ${error.message}`);
}
```

## Security Rules

### NEVER:
- Log passwords, tokens, API keys, or PII
- Commit .env files or any secrets
- Use eval(), Function(), or dynamic code execution
- Trust user input without validation
- Store credentials in code or comments
- Use innerHTML without sanitization
- Expose internal error details to users
- Use Math.random() for security purposes

### ALWAYS:
- Validate and sanitize ALL inputs
- Use parameterized queries/prepared statements
- Check file paths for directory traversal (../)
- Use environment variables for secrets
- Hash passwords with bcrypt/argon2
- Use crypto.randomBytes() for tokens
- Implement rate limiting for APIs
- Escape output in templates

## Performance Considerations

### AVOID:
- N+1 database queries (use joins/includes)
- Synchronous file operations in request handlers
- Large data processing in main thread
- Unnecessary re-renders in React
- Multiple sequential await calls (use Promise.all)
- Importing entire libraries (use specific imports)
- Inline function definitions in render methods

### PREFER:
- Batch database operations
- Pagination for large datasets (limit/offset)
- Lazy loading for heavy components
- useMemo/useCallback for expensive operations
- Virtual scrolling for long lists
- Web Workers for CPU-intensive tasks
- Debouncing/throttling for frequent events

## Git Workflow

### Working State Tracking
**CRITICAL**: Mark stable/working states directly in commit messages so they're visible in GitHub:

#### State Markers for Commit Messages:
- `[STABLE]` - Fully tested, production-ready state (create tag after this)
- `[WORKING]` - Everything functional but needs more testing  
- `[WIP]` - Work in progress, may have issues
- `[HOTFIX]` - Emergency fix applied to stable state

#### Commit Message Format with State Tracking:
```bash
# Format: [STATE] type: description
[STABLE] feat: Add todo viewer with project filtering
[WORKING] fix: Correct date timezone issues 
[WIP] feat: Implementing GitHub sync for todos

# With issue references:
[STABLE] fix: Complete todo-viewer fixes

Closes #155
```

#### Creating Version Tags for Rollback:
After any [STABLE] commit, create a descriptive tag:
```bash
git tag -a "v1.0-feature-stable" -m "Description of what's working"
git push origin --tags
```

Tag naming convention:
- `v1.0-feature-stable` - Production ready
- `v1.0-feature-working` - Functional but needs testing
- `hotfix-YYYYMMDD-issue` - Emergency fixes

### Branch Naming:
- feature/short-description
- fix/issue-number-description
- chore/task-description
- hotfix/critical-issue

### Commit Messages:
- Optionally start with state marker: [STABLE], [WORKING], [WIP]
- Then conventional prefix: feat:, fix:, docs:, chore:, refactor:
- Keep under 50 characters after prefix
- No period at end
- Reference issue: "Related to #123" or "Closes #123"
- Use "Closes #123" only once per issue (in final commit/PR)

### CRITICAL: Professional Commit Strategy for Rich Release Notes

**THE RULE: Accumulate commits locally, push batches for comprehensive releases**

#### ❌ WRONG - Immediate Push Pattern (Creates Sparse Releases):
```bash
# Do work, commit everything at once, push immediately
git add -A
git commit -m "fix: Restore DevOps system and fix AgentSwarm workflow issues"
git push  # ← CREATES SPARSE RELEASE WITH 1 BULLET POINT
```

#### ✅ CORRECT - Professional Accumulation Pattern (Creates Rich Releases):
```bash
# Make focused commits as you work (LOCALLY)
git commit -m "fix(devops): restore complete DevOps directory from source"
git commit -m "fix(agentswarm): remove duplicate agentswarm.sh file"  
git commit -m "fix(agentswarm): add exclusions for pytest.ini pollution"
git commit -m "fix(agentswarm): prevent .github directory sync"
git commit -m "feat(template): improve exclusion patterns"
git commit -m "docs(template): update sync documentation"

# Work for days/weeks building up commits locally...
# THEN push all accumulated work together
git push  # ← CREATES RICH RELEASE WITH 6+ ORGANIZED BULLET POINTS
```

#### Benefits of Accumulation Strategy:
- **Rich Release Notes**: 6+ detailed bullet points instead of 1
- **Professional Appearance**: Like Google, Microsoft, Meta releases
- **Better Organization**: Semantic-release groups by type (Features, Bug Fixes, etc.)
- **Easier Debugging**: Granular commit history for troubleshooting
- **Team Standards**: Follows industry best practices

#### When to Push:
- **Feature Complete**: All related work is done and tested
- **Sprint End**: Weekly/bi-weekly release cycles
- **Milestone Reached**: Major functionality implemented
- **Emergency**: Only for critical hotfixes

#### Example Professional Release Result:
```markdown
## Features
• improve exclusion patterns (abc123)
• add GitHub repository auto-creation (def456)

## Bug Fixes  
• restore complete DevOps directory from source (ghi789)
• remove duplicate agentswarm.sh file (jkl012)
• add exclusions for pytest.ini pollution (mno345)
• prevent .github directory sync (pqr678)

## Documentation
• update sync documentation (stu901)
```

**Remember**: Commits are LOCAL until pushed - accumulate significant work for professional releases!

### NEVER Commit:
- node_modules/, venv/, __pycache__/
- .env, .env.local, .env.*.local
- Build outputs (dist/, build/)
- IDE files (.idea/, .vscode/settings.json)
- OS files (.DS_Store, Thumbs.db)
- Log files (*.log, npm-debug.log*)
- Temporary files (*.tmp, *.swp)

## Testing Approach

### Before Writing Tests:
1. Check if test infrastructure exists
2. Look for existing test patterns
3. Use same test framework as existing tests
4. Never introduce new test framework

### Test File Naming:
- *.test.ts, *.spec.ts for unit tests
- *.e2e.ts for end-to-end tests
- Place next to file being tested or in __tests__/

### Never:
- Create test files if no test setup exists
- Write tests without running them
- Commit failing tests

## Debug & Development Helpers

### Before Marking Complete:
- Remove ALL console.log statements
- Remove debugger statements
- Remove commented-out code
- Remove TODO comments (unless intentional)
- Clean up temporary variables
- Remove development-only code

### Acceptable Logging:
- Error logging with context
- Warning for deprecated features
- Info for important state changes (in dev only)

## Project-Specific Context

### Tech Stack:
<!-- Current template includes -->
- Frontend: Next.js, React, TypeScript, Tailwind CSS
- Backend: Next.js API Routes
- Database: [Configure based on project needs]
- Authentication: [Configure based on project needs]
- Deployment: Vercel
- CI/CD: GitHub Actions
- Testing: Jest, React Testing Library

### Key Patterns in This Codebase:
<!-- Add patterns as discovered -->

### External Services:
<!-- Add as integrated -->

### Known Issues/Gotchas:
<!-- Add quirks as discovered -->

## Response Behavior

### Critical Thinking & Decision Making

**Don't Just Agree - Think Critically:**
- Question approaches that might have issues
- Point out potential problems BEFORE implementing
- Suggest alternatives when something seems wrong
- Explain tradeoffs between different approaches
- Push back on ideas that violate best practices

**When User Suggests Something:**
1. First analyze if it makes technical sense
2. Consider the implications and side effects
3. Check if it aligns with the established architecture
4. Propose alternatives if there's a better way
5. Explain WHY something might not work, don't just agree

**Examples of Healthy Pushback:**
- "That would work, but it might cause [specific problem]. What about [alternative]?"
- "I see the goal, but that approach breaks our principle of [X]. Could we instead [Y]?"
- "That's one way, but it would require changing [A, B, C]. A simpler approach might be..."
- "Let me make sure I understand the goal correctly before we proceed..."

### When Starting Tasks:
1. **Question the approach first** - Is this the right solution?
2. Use TodoWrite to plan if multiple steps
3. Search/read relevant files first
4. Understand existing patterns
5. Implement solution using **Professional Commit Strategy**:
   - Make focused commits as work progresses
   - Don't bundle everything into one commit
   - Accumulate commits locally before pushing
6. Run lint/typecheck
7. Remove debug code
8. Verify solution works
9. **ONLY PUSH when feature/milestone is complete** (not after every commit)

### When Task is Complete:
- Just stop after completing
- Don't explain what was done
- Don't summarize changes
- Don't suggest next steps (unless asked)

### Ops CLI Testing (CLI-first)
- Use `./project-sync/scripts/ops qa --backend` for backend tests (fast lane)
- Use `./project-sync/scripts/ops qa --cli` for CLI contract tests
- Use `./project-sync/scripts/ops qa --mcp` for MCP in-memory tests
- Set `RUN_MCP_TRANSPORT=1` to include transport/subprocess MCP tests
<!-- AUTO-CONTEXT-START -->

**Current Branch**: main
**Last Updated**: 2025-09-13 22:51:21

### Recent Commits
```
3d28ba5 [WORKING] feat: Major project-sync system implementation
2dd7a25 feat: Integrate spec-kit with test generation and implement commands
ec3fc88 docs: Consolidate documentation from 84 to ~60 files
47b50dc docs: Add quick copy commands to README
57b8533 docs: Add note about global vs project commands
```

<!-- AUTO-CONTEXT-END -->
