# Claude Code Documentation - Multi-Agent Template Framework

## CRITICAL: GitHub Repository Information
**Repository Owner**: vanman2024 (NOT gotime2022)
**Repository Name**: multi-agent-claude-code
**Full Path**: github.com/vanman2024/multi-agent-claude-code

## THIS IS A TEMPLATE FRAMEWORK
**Important**: Template repository for creating new projects. Provides pre-configured automation, agent orchestration, slash commands, and CI/CD.

## CRITICAL: Project Constitution
**ALWAYS check `.specify/memory/constitution.md`** - Contains project-specific principles, tech stack constraints, testing requirements, and governance rules that override general instructions.

## Working Modes

### Template Mode (Building Framework)
- **Direct commits allowed** for template improvements
- **Flexible workflow** - no CI/CD constraints
- **Use for**: Slash commands, docs, workflow automation, agent configs

### Application Mode (Using Framework)
- **STRICT workflow**: Issue → PR → Review → Merge
- **No direct commits** to main
- **Full CI/CD validation** required
- **Use for**: Production applications, team development

**Key**: Template Mode = flexible framework building, Application Mode = strict app development

## 🤖 @Symbol Multi-Agent Coordination System

### Agent Roles
- **@claude**: Full subagent system for complex tasks
- **@copilot**: Simple tasks (Complexity ≤2, Size XS-S)
- **@qwen**: Local CLI for everyday coding (FREE)
- **@gemini**: Large document analysis (2M context, ~$0.075/M tokens)
- **@codex**: Interactive development

### Claude Code Subagents
- **@claude/general-purpose**: Complex multi-step tasks
- **@claude/code-refactorer**: Large-scale refactoring
- **@claude/pr-reviewer**: Code review
- **@claude/backend-tester**: API testing
- **@claude/integration-architect**: Multi-service integrations
- **@claude/system-architect**: Database/API architecture
- **@claude/security-auth-compliance**: Authentication/security
- **@claude/frontend-playwright-tester**: E2E testing

### Primary Slash Commands

#### Main Commands (90% usage)
1. **`/create-issue "Description"`** - Universal issue creation with auto-routing
   - Auto-assigns simple tasks to Copilot (Complexity ≤2, Size XS/S)
   - Routes complex work to Claude Code agents

2. **`/work #123`** - Universal work implementation
   - Creates branches and PRs automatically
   - Supports: `/work` (auto-pick), `/work --deploy`, `/work --test`

#### Other Commands
- `/hotfix` - Emergency fixes
- `/deploy` - Deploy to production
- `/copilot-review` - Request Copilot review
- `/discussions` - Manage GitHub Discussions
- `/add-mcp` - Add MCP servers
- `/project-setup` - Initialize from template

### CRITICAL: Slash Command Rules
**ALWAYS use templates in `/templates/slash-command-templates.md`**

**Key Principles:**
- Keep SIMPLE - just run, no complex logic
- Use `!` for bash, `@` for files, `$ARGUMENTS` for input
- Use MCP functions directly

**NEVER use:**
- Template placeholders (`<pattern>`)
- Complex bash substitutions
- Variables needing state
- Multi-step logic

**Structure:**
```markdown
---
allowed-tools: Bash(*), Read(*)
description: Brief description
---
Run: !git [command]
```

### /discussions Examples
- `/discussions` - Interactive menu
- `/discussions "Topic"` - Quick create
- `/discussions 125` - View specific
- **Conversion**: Analyzes content → suggests type → creates issue → links discussion

## 🚀 Ops CLI Automation System

### Core Commands
```bash
# Daily Development
ops qa                    # All quality checks
ops qa --backend          # Python/pytest only
ops qa --frontend         # Playwright/TypeScript only
ops build --target PATH  # Production build
ops verify-prod          # Test build
ops status                # Current state

# Release
ops release patch/minor/major  # Semantic versioning

# Environment
ops env doctor       # Check WSL/Windows issues
ops setup TARGET     # Setup operations
ops sync             # Sync to targets
```

### Agent Integration

**@claude**: `ops qa --backend` for Python/API, `ops qa --all` for full-stack
**@copilot**: `ops qa --frontend` for UI/UX
**@gemini/@qwen**: Reference `ops status`, validate with `ops env doctor`

### Workflow
```bash
# Before Starting
git pull && ops status && ops qa

# Before Completing  
ops qa && ops build --target /tmp/test && ops verify-prod /tmp/test

# Release
ops release patch/minor/major
```

### Configuration
`.automation/config.yml` adapts to project type:
- **Python**: `pyproject.toml`, `ruff`, `mypy`, `pytest`
- **Node.js**: `package.json`, `npm run lint/typecheck/test`
- **Multi-Language**: Auto-detects tools

### Benefits
1. **Consistent Quality** - Same QA standards
2. **Reliable Builds** - Production readiness
3. **Clear State** - Deployment status
4. **Environment Safety** - WSL/path checks
5. **Simple Releases** - Semantic versioning

### Troubleshooting
- `ops env doctor` - Environment issues
- `ops status` - Configuration check
- `ops qa --help` - Available options

## System Architecture: House Metaphor 🏗️

### Layers
1. **Foundation** (Database) - Solid, unchanging schemas
2. **Plumbing** (GitHub/CI/CD) - Moves data, no intelligence
3. **Framing** (Backend/APIs) - Structural support, business logic
4. **Electrical** (Agents) - Intelligence, decisions (Claude = main panel)
5. **Finishes** (Frontend/UI) - User interface, easily changed
6. **Smart Home** (Project Board) - Monitoring, status display

### Key Principle
**Plumbing doesn't think** - it moves things. **Electrical makes decisions** - intelligent control. GitHub workflows = plumbing (route, test, deploy). Intelligence = Claude Code + agents.

## Agent Assignment Rules

### Golden Rule: Copilot Gets Small AND Simple
**Copilot**: Complexity ≤2 AND Size XS/S (both required)
**Claude**: Complexity >2 OR Size >S (either condition)

| Complexity | Size | Agent | Example |
|------------|------|-------|---------|
| 1-2 | XS-S | Copilot | Fix typo, simple endpoint |
| 1-2 | M-XL | Claude | Large simple refactor |
| 3-5 | Any | Claude | Architecture, security |

**Auto-assignment**: `/create-issue` automatically routes based on complexity/size analysis.

## CRITICAL WORKFLOW: Issue → PR → Merge → Deploy

### Golden Rule: ALWAYS create issue BEFORE PR

**EXCEPTIONS (direct commits OK):**
- Doc examples, typos, grammar, comments, formatting (no logic)

### 🔄 MANDATORY PULL POINTS
**ALWAYS `git pull` at:**
1. Before creating issues
2. After ANY PR merges
3. Before `/work`
4. Before commits
5. Start of work sessions

**Why**: Prevents working on old code, conflicts, duplicate work

### Workflow Steps
1. **Research** - TodoWrite for complex tasks, plan approach
2. **Issue Creation** - `git pull` → `/create-issue "Description"`
   - Planning only (NO code, branches, or PRs yet)
   - Auto-routes and assigns based on complexity
3. **Start Work** - `git pull` → `/work #123`
   - NOW creates branch + draft PR with "Closes #123"
   - All commits go in PR
4. **Complete** - Check PR boxes, run tests, convert to ready
5. **Merge** - `gh pr merge --squash --delete-branch`

### 📝 CRITICAL: All Commits Must Reference Issue

**GitHub requires explicit issue references** - branch names don't auto-link!

```bash
# ✅ CORRECT
git commit -m "feat: Add authentication

Related to #123"

# ❌ WRONG  
git commit -m "feat: Add authentication"  # No reference!
```

**Reference types:**
- `Related to #123`, `Part of #123`, `Updates #123`, `#123`
- `Closes #123` - ONLY final commit (use once!)

### Common Mistakes
**NEVER**: PR without issue, branches on issue creation, commits without PR
**ALWAYS**: Issue first, use `/work`, issues = planning only, commits in PRs

## GitHub Discussions

### Adding Comments
1. Get discussion ID via GraphQL query
2. Use ID with addDiscussionComment mutation

```bash
# Get ID
DISCUSSION_ID=$(gh api graphql -f query='query { repository(owner: "OWNER", name: "REPO") { discussion(number: NUMBER) { id } } }' --jq .data.repository.discussion.id)

# Add comment  
gh api graphql -f query='mutation($discussionId: ID!, $body: String!) { addDiscussionComment(input: {discussionId: $discussionId, body: $body}) { comment { id } } }' -F discussionId="$DISCUSSION_ID" -F body="Text"
```

## Gemini CLI - Dual Terminal Setup

### Two FREE Models
1. **Terminal 1**: Google OAuth → **Gemini 2.5 Pro** (FREE personal accounts)
2. **Terminal 2**: API Key → **Gemini 2.0 Flash Exp** (FREE experimental)

### Setup
```bash
# Terminal 1: OAuth
gemini  # Choose Google login

# Terminal 2: API Key  
source /home/gotime2022/bin/gemini-setup-experimental.sh
gemini -m gemini-2.0-flash-exp
```

### Usage Strategy
- **2.0 Flash Exp**: Rapid prototyping, quick questions
- **2.5 Pro**: Complex analysis
- **Claude Code**: Architecture, refactoring, debugging

**Both FREE** - maximize usage while available!

## MCP Servers

MCP allows Claude to interact with external tools. **See**: [MCP_SERVERS_GUIDE.md](./MCP_SERVERS_GUIDE.md)

### Quick Reference
```bash
# Add servers
claude mcp add <name> -- <command>              # Local
claude mcp add --transport http <name> <url>    # HTTP
claude mcp add --transport sse <name> <url>     # SSE

# Manage
claude mcp list/get/remove <name>
/mcp  # Check status in Claude Code
```

## WSL & Windows

### File Paths
Windows: `C:/Users/user/file.png` → WSL: `/mnt/c/Users/user/file.png`

### VS Code Settings
**ALWAYS restart VS Code** after modifying `.vscode/settings.json`

## File Naming Conventions

### Special Files (UPPERCASE)
- `README.md`, `CLAUDE.md`, `LICENSE`, `CHANGELOG.md`

### All Others (lowercase-with-hyphens)
- **Docs**: `design-specs.md`, `api-guide.md`
- **Config**: `package.json`, `tsconfig.json`
- **Code**: `user-profile.ts`, `api-handler.js`

### Rules
✅ **ALWAYS**: Consistent style, `.md` extension
❌ **NEVER**: Mixed styles, underscores in markdown, variations

## File Management Rules

### Prevent Bloat
**NEVER create**: Temp test files, duplicate docs, examples (unless requested), backups, scratch files
**ALWAYS**: Use existing files, clean up temp files, modify over create

### Before Creating Files
1. Check if similar exists
2. Verify active use
3. Ensure not one-time
4. Confirm user request

### Cleanup
- Remove unused imports, commented code, console.logs, debug statements

## Documentation Rules

### CRITICAL: Prevent Duplication
**BEFORE creating ANY docs:**
1. Search: `find . -name "*.md" | xargs grep -l -i "topic"`
2. Check existing: WORKFLOW.md, CLAUDE.md, MCP_SERVERS_GUIDE.md
3. UPDATE existing instead of creating new
4. CONSOLIDATE similar topics

### File Naming
- **Documentation**: UPPERCASE (README.md, CLAUDE.md)
- **Code/Config**: lowercase (package.json, index.js)

### Core Docs Only
- README.md (overview)
- CLAUDE.md (AI instructions)
- MCP_SERVERS_GUIDE.md (if using MCP)
- API.md (if building API)
- CONTRIBUTING.md (if open source)

### Principles
**NO**: Sprawl, notes files (TODO.md), drafts, examples, architecture docs, changelog
**USE**: Code comments, git history, wait for explicit requests
**LOCATION**: /docs folder (except README.md, CLAUDE.md in root)

## Testing & QA Standards

### Dual Architecture
**Backend** (`backend-tests/`): Python/pytest - API, integrations
**Frontend** (`frontend-tests/`): Playwright/TypeScript - UI, E2E, visual

### Commands
```bash
./scripts/ops qa --backend    # Python/API
./scripts/ops qa --frontend   # UI/UX
./scripts/ops qa --all        # Full-stack
```

### API Testing
- **Postman MCP**: Pre-configured for contract testing
- **Newman CLI**: `newman run collection.json`
- **Mock Servers**: Frontend development

### Agent Responsibilities
- **@claude**: Backend/Python/pytest
- **@copilot**: Frontend/Playwright
- **@gemini**: Integration/cross-browser
- **@qwen**: Performance/accessibility

## Code Style & Conventions

### Language Rules
- **TypeScript**: Strict mode, interfaces over types, explicit returns
- **Python**: PEP 8, type hints, docstrings for public functions
- **React**: Functional components, hooks not classes, memo for expensive
- **Node.js**: async/await over callbacks, handle rejections
- **Database**: Transactions for multiple ops, parameterized queries

### Naming
- **Files**: kebab-case (`user-profile.ts`)
- **Components**: PascalCase (`UserProfile.tsx`)
- **Functions**: camelCase (`getUserProfile`)
- **Constants**: UPPER_SNAKE_CASE (`API_BASE_URL`)
- **Database**: snake_case (`user_accounts`)
- **CSS**: kebab-case (`user-profile-card`)
- **Env vars**: UPPER_SNAKE_CASE with prefix (`REACT_APP_`)

## Common Commands

### ALWAYS run before task completion:
```bash
./scripts/ops qa --backend    # Python/API
./scripts/ops qa --frontend   # UI/UX
./scripts/ops qa --all        # Full-stack

# Individual (if ops unavailable)
ruff check src/ --fix         # Python lint
mypy src/                     # Python types
python3 run.py -m pytest backend-tests/
npm run lint:frontend
npm run test:frontend
```

### Unknown Commands
Check: package.json scripts, README.md, ask user

## Error Handling

### NEVER
- Empty try-catch
- Generic messages
- Ignore Promise rejections
- Catch without handling

### ALWAYS
- Log with context (user, action, time)
- Specific actionable messages
- Error boundaries in React
- Handle sync/async
- Preserve stack traces in dev

### Pattern
```javascript
try {
  // operation
} catch (error) {
  console.error('Context:', { userId, action, error });
  throw new Error(`Failed to [action]: ${error.message}`);
}
```

## Security Rules

### NEVER
- Log secrets/PII
- Commit .env files
- Use eval(), dynamic execution
- Trust user input
- Store credentials in code
- Use innerHTML without sanitization
- Expose internal errors
- Use Math.random() for security

### ALWAYS
- Validate/sanitize ALL inputs
- Parameterized queries
- Check for directory traversal (../)
- Environment variables for secrets
- bcrypt/argon2 for passwords
- crypto.randomBytes() for tokens
- Rate limiting
- Escape template output

## Performance

### AVOID
- N+1 queries (use joins)
- Sync file ops in handlers
- Main thread processing
- Unnecessary React re-renders
- Sequential awaits (use Promise.all)
- Full library imports
- Inline render functions

### PREFER
- Batch operations
- Pagination (limit/offset)
- Lazy loading
- useMemo/useCallback
- Virtual scrolling
- Web Workers for CPU tasks
- Debouncing/throttling

## Git Workflow

### State Tracking
**Mark states in commit messages:**
- `[STABLE]` - Production-ready (create tag after)
- `[WORKING]` - Functional, needs testing
- `[WIP]` - In progress
- `[HOTFIX]` - Emergency fix

### Format
```bash
[STATE] type: description
[STABLE] feat: Add todo viewer
Related to #123
```

### Tags
```bash
git tag -a "v1.0-feature-stable" -m "Description"
git push origin --tags
```

### Branch Naming
- `feature/description`
- `fix/issue-description`
- `chore/task`
- `hotfix/critical`

### Commit Rules
- Optional state marker + conventional prefix
- Under 50 chars, no period
- Reference issues: "Related to #123"
- "Closes #123" only once per issue

### Professional Commit Strategy

**RULE: Accumulate commits locally, push batches for rich releases**

#### ❌ WRONG - Immediate Push
```bash
git add -A
git commit -m "fix: Restore DevOps and fix AgentSwarm issues"
git push  # ← Sparse release (1 bullet)
```

#### ✅ CORRECT - Accumulation
```bash
# Focused commits locally
git commit -m "fix(devops): restore complete directory"
git commit -m "fix(agentswarm): remove duplicate file"
git commit -m "fix(agentswarm): add exclusions"
git commit -m "feat(template): improve patterns"
# ... accumulate work locally ...
git push  # ← Rich release (6+ bullets)
```

#### Benefits
- Rich release notes (6+ detailed bullets)
- Professional appearance
- Better organization (semantic-release groups)
- Granular debugging
- Industry standards

#### When to Push
- Feature complete
- Sprint end
- Milestone reached
- Emergency only

**Remember**: Commits are LOCAL until pushed!

### Smart Git Hook Automation

**Automated commit accumulation guidance** via `.git/hooks/pre-push`:

#### Features
- **Guidance Only**: Never blocks pushes (solo development friendly)
- **3-second countdown**: Cancel with Ctrl+C or continue immediately
- **Branch-aware**: Only guides on main branch
- **Bypass available**: `./scripts/push-bypass` for testing

#### When Hook Activates
- ≤1 commits to push on main branch
- Shows professional accumulation guidance
- Suggests building up 3-6 focused commits

#### Bypass for Testing
```bash
./scripts/push-bypass          # Quick push without guidance
git push --no-verify          # Standard git bypass
```

#### Example Output
```
🤖 Professional Commit Strategy Guidance
📊 Commits to push: 1
💡 For richer release notes, consider accumulating 3-6 commits
✅ Rich Release Pattern: [examples shown]
🚀 Continue anyway? Proceeding in 3 seconds...
```

**Perfect for solo founders working with AI agents** - guidance without friction.

### NEVER Commit
- `node_modules/`, `venv/`, `__pycache__/`
- `.env*` files
- Build outputs (`dist/`, `build/`)
- IDE files, OS files, logs, temps

## Testing Approach

### Before Writing Tests
1. Check existing infrastructure
2. Follow existing patterns
3. Use same framework
4. Never introduce new framework

### File Naming
- `*.test.ts`, `*.spec.ts` for unit
- `*.e2e.ts` for end-to-end
- Place next to tested file or in `__tests__/`

### Never
- Create tests without setup
- Write without running
- Commit failing tests

## Debug & Development

### Before Completion
- Remove console.logs, debugger, commented code
- Remove TODO comments (unless intentional)
- Clean temporary variables, dev-only code

### Acceptable Logging
- Error with context
- Deprecation warnings
- Important state changes (dev only)

## Project-Specific Context

### Tech Stack
- **Framework**: Multi-Agent Development Template
- **Components**: DevOps automation, AgentSwarm orchestration
- **Languages**: Python, Bash, TypeScript, YAML
- **Automation**: GitHub Actions, semantic-release
- **Testing**: pytest (backend), Playwright (frontend)
- **CLI**: ops automation system
- **Deployment**: Component-based auto-deploy system

### Key Patterns
<!-- Add as discovered -->

### External Services
<!-- Add as integrated -->

### Known Issues
<!-- Add quirks as discovered -->

## Response Behavior

### Critical Thinking
**Don't just agree - think critically:**
- Question approaches with issues
- Point out problems BEFORE implementing
- Suggest alternatives
- Explain tradeoffs
- Push back on bad practices

**When User Suggests:**
1. Analyze technical sense
2. Consider implications
3. Check architecture alignment
4. Propose better alternatives
5. Explain WHY something won't work

### Task Workflow
1. **Question approach first**
2. TodoWrite for complex tasks
3. Search/read relevant files
4. Understand patterns
5. Implement with **Professional Commit Strategy**
6. Run lint/typecheck
7. Remove debug code
8. Verify works
9. **PUSH only when complete** (not per commit)

### When Complete
- Stop after finishing
- No explanations/summaries
- No next step suggestions (unless asked)

### Ops CLI Testing
- `./project-sync/scripts/ops qa --backend` (fast)
- `./project-sync/scripts/ops qa --cli` (contract)
- `./project-sync/scripts/ops qa --mcp` (in-memory)
- `RUN_MCP_TRANSPORT=1` for transport tests
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
