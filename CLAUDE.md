# Claude Code Documentation - Multi-Agent Template Framework

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

When creating issues via `/create-feature`:
```javascript
const isSmallAndSimple = (complexity <= 2) && (size === 'XS' || size === 'S');
if (isSmallAndSimple) {
  // Automatically assign to Copilot via MCP
  await mcp__github__assign_copilot_to_issue({...});
}
```

**See full workflow details:** [.github/COPILOT-WORKFLOW.md](./.github/COPILOT-WORKFLOW.md)

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

### Core Documentation Only
During development, maintain ONLY these essential documents:
- **README.md** - Project overview, setup, and quick start
- **CLAUDE.md** - AI assistant instructions (this file)
- **MCP_SERVERS_GUIDE.md** - MCP server reference (if using MCP)
- **API.md** - API endpoints (only if building an API)
- **CONTRIBUTING.md** - Contribution guidelines (only for open source)

### Documentation Principles
- **NO SPRAWL**: Do not create multiple documentation files
- **NO NOTES FILES**: Never create TODO.md, NOTES.md, thoughts.md, ideas.md
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
- Keep all docs in root directory during development
- Only create /docs folder when transitioning to production
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
<!-- Add your stack when known -->
- Frontend: [TBD]
- Backend: [TBD]
- Database: [TBD]
- Authentication: [TBD]

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