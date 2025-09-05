# Claude Code Documentation - Multi-Agent Template Framework

## CRITICAL: GitHub Repository Information
**Repository Owner**: vanman2024 (NOT gotime2022)
**Repository Name**: multi-agent-claude-code
**Full Path**: github.com/vanman2024/multi-agent-claude-code

## THIS IS A TEMPLATE FRAMEWORK

**Important**: You are working in a template repository that will be cloned to create new projects. This is NOT the actual project - it's the framework for building projects.

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

## AI Agent Integration

### How AI Agents Work in This Framework
- **GitHub Copilot**: Handles simple tasks (Complexity 1-2, Size XS-S) directly in GitHub
- **Claude Code Agents**: Handle complex tasks locally with full MCP tool access
- **No @claude App**: We avoid the @claude GitHub App to prevent usage costs

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
**NEVER put code blocks inside slash command files!**
- Use the special `!` syntax for inline bash commands (e.g., `!git status`)
- Use MCP server functions directly (e.g., mcp__github__create_issue)
- Slash commands should only contain:
  - Documentation and task descriptions
  - Direct commands using `!` syntax
  - MCP function calls
  - Examples showing usage (not implementation code)
- Follow the templates in `/templates/slash-command-templates.md`
- Use `/work` to start local implementation

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
# Check if these commands exist first, then run if available:
npm run lint        # or: eslint, ruff, flake8, etc.
npm run typecheck   # or: tsc, mypy, etc.
npm test           # only if tests exist
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

### Branch Naming:
- feature/short-description
- fix/issue-number-description
- chore/task-description
- hotfix/critical-issue

### Commit Messages:
- Start with verb: Add, Fix, Update, Remove, Refactor
- Keep under 50 characters
- No period at end
- Reference issue: "Fix #123: Login error"

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
5. Implement solution
6. Run lint/typecheck
7. Remove debug code
8. Verify solution works

### When Task is Complete:
- Just stop after completing
- Don't explain what was done
- Don't summarize changes
- Don't suggest next steps (unless asked)