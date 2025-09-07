# Slash Command Flags Reference

## Overview
This document provides a comprehensive reference for all flags available in slash commands. Flags modify command behavior and provide specialized functionality.

## /create-issue Command Flags

### Type Flags
These flags determine the type of issue and the workflow to follow:

#### `--feature`
**Purpose**: Create a new feature issue with full planning  
**Usage**: `/create-issue --feature "Add user authentication"`  
**Template**: `templates/local_dev/feature-template.md`  
**Behavior**:
- Uses full feature template with checkboxes
- Requires complexity and size assessment
- Creates detailed acceptance criteria
- May auto-assign to Copilot if simple enough

#### `--enhancement`
**Purpose**: Improve existing functionality  
**Usage**: `/create-issue --enhancement "Update project-setup with Vercel steps"`  
**Template**: `templates/local_dev/feature-template.md` (lighter sections)  
**Behavior**:
- Uses feature template but lighter process
- Simple description with what and why
- Fewer checkboxes than full features
- For improving something that already exists

#### `--bug`
**Purpose**: Report something broken  
**Usage**: `/create-issue --bug "Login fails on mobile devices"`  
**Template**: `templates/local_dev/bug-template.md`  
**Behavior**:
- Uses bug report template
- Requires reproduction steps
- Includes environment details
- Adds regression test requirements

#### `--refactor`
**Purpose**: Code improvement without changing functionality  
**Usage**: `/create-issue --refactor "Extract common API logic"`  
**Template**: `templates/local_dev/task-template.md`  
**Behavior**:
- Technical debt reduction
- No user-visible changes
- Code quality improvements
- Architecture updates

#### `--chore`
**Purpose**: Maintenance tasks and routine updates  
**Usage**: `/create-issue --chore "Update dependencies"`  
**Template**: `templates/local_dev/task-template.md`  
**Behavior**:
- Minimal template
- Config changes, dependency updates
- Build process improvements
- Routine maintenance

#### `--docs`
**Purpose**: Documentation updates  
**Usage**: `/create-issue --docs "Update README examples"`  
**Template**: `templates/local_dev/task-template.md` (minimal)  
**Behavior**:
- Documentation-only changes
- May auto-merge if no code changes
- Lighter review process

### Workflow Modifier Flags

#### `--quick`
**Purpose**: Minimal process for simple fixes  
**Usage**: `/create-issue --quick "Fix typo in header"`  
**Behavior**:
- Skips complexity/size assessment
- Creates minimal issue (title + description)
- Auto-sets complexity=1, size=XS
- No templates or checkboxes

#### `--hotfix`
**Purpose**: Emergency fixes that need immediate attention  
**Usage**: `/create-issue --hotfix "Critical security vulnerability"`  
**Behavior**:
- Skips similarity check
- Creates issue with HOTFIX: prefix
- May create branch immediately
- Bypasses some workflow requirements

### Auto-Detection (No Flag)
When no flag is provided, keywords in the title trigger smart routing:
- "Add/Create/Implement/Build" → `--feature`
- "Update/Improve/Enhance" → `--enhancement`
- "Fix/Broken/Error/Fails" → `--bug`
- "Refactor/Reorganize/Clean" → `--refactor`
- "Dependencies/Config/Setup" → `--chore`
- "Document/README/Docs" → `--docs`

## /work Command Flags

### Core Workflow Flags

#### `--resume`
**Purpose**: Resume the most recent incomplete work  
**Usage**: `/work --resume`  
**Behavior**: 
- Automatically finds your most recently modified issue branch
- Checks for existing worktrees or branches
- Handles WIP commits by soft resetting them
- Syncs with main branch if needed

#### `--status`  
**Purpose**: Display a triage view of all your active work  
**Usage**: `/work --status`  
**Behavior**:
- Shows all issue branches with recent activity
- Displays WIP commit indicators
- Lists active worktrees
- Prompts for which issue to resume

#### `--discussion <number>`
**Purpose**: Create an issue from a GitHub Discussion  
**Usage**: `/work --discussion 125`  
**Behavior**:
- Fetches discussion content from GitHub
- Creates a properly formatted issue
- Links back to the original discussion
- Continues with normal work implementation

#### `--deploy`
**Purpose**: Deploy current branch to Vercel  
**Usage**: `/work --deploy`  
**Behavior**:
- Runs Vercel deployment for current branch
- Shows deployment URL when complete

### Copilot Integration Flags

#### `--copilot-first`
**Purpose**: Try Copilot first for simple tasks, Claude as backup  
**Usage**: `/work #150 --copilot-first`  
**Token Savings**: ~80% for simple tasks  
**Behavior**:
- Assigns simple tasks to Copilot
- Claude monitors progress
- Claude takes over if Copilot gets stuck

#### `--copilot-review`
**Purpose**: Get Copilot's code review on current work  
**Usage**: `/work --copilot-review`  
**Behavior**:
- Requests Copilot review on current PR
- Pulls in Copilot's suggestions
- Claude can implement the suggestions

#### `--copilot-only`
**Purpose**: Only use Copilot, no Claude involvement  
**Usage**: `/work #142 --copilot-only`  
**Token Savings**: 100% - No Claude tokens used  
**Behavior**:
- Assigns to Copilot
- Monitors status only
- No Claude implementation

#### `--no-copilot`
**Purpose**: Bypass Copilot entirely, use Claude directly  
**Usage**: `/work #142 --no-copilot`  
**Behavior**:
- Skips Copilot assignment check
- Claude handles everything
- Useful for complex tasks Copilot can't handle

#### `--parallel`
**Purpose**: Claude and Copilot work simultaneously  
**Usage**: `/work #142 --parallel`  
**Behavior**:
- Splits work between Claude and Copilot
- Both work on different aspects
- Merges results when complete

## /plan:generate Command Flags

### Mode Flags

#### `--from-vision`
**Purpose**: Generate detailed docs from PROJECT_PLAN.md vision (default)  
**Usage**: `/plan:generate --from-vision`  
**Behavior**:
- Reads docs/PROJECT_PLAN.md vision document
- Creates detailed technical documentation
- Expands vision into ARCHITECTURE, INFRASTRUCTURE, FEATURES docs
- Default behavior after `/project-setup`

#### `--fresh-analysis`
**Purpose**: Analyze existing codebase without vision doc  
**Usage**: `/plan:generate --fresh-analysis`  
**Behavior**:
- Analyzes code structure and files
- Infers tech stack from package.json
- Creates documentation from scratch
- Use for existing projects without PROJECT_PLAN.md

### Domain Flags

#### `--domain [type]`
**Purpose**: Specify business domain for better planning  
**Usage**: `/plan:generate --domain e-commerce`  
**Options**: e-commerce, saas, skilled-trades, healthcare, fintech  
**Behavior**:
- Generates domain-specific features
- Applies industry best practices
- Includes compliance requirements

## /test:generate Command Flags

### Scope Flags

#### `--all`
**Purpose**: Generate complete test suite (default)  
**Usage**: `/test:generate --all`  
**Behavior**:
- Creates unit, integration, and E2E tests
- Generates Postman collections for API
- Sets up mock infrastructure
- ~90% test coverage from start

#### `--unit`
**Purpose**: Generate only unit tests  
**Usage**: `/test:generate --unit`  
**Behavior**:
- Business logic tests
- Component tests
- Utility function tests
- No API or E2E tests

#### `--integration` or `--api`
**Purpose**: Generate API contract tests  
**Usage**: `/test:generate --integration`  
**Behavior**:
- Creates Postman collection
- Newman test runner scripts
- Mock API responses
- No database required

#### `--e2e`
**Purpose**: Generate end-to-end tests  
**Usage**: `/test:generate --e2e`  
**Behavior**:
- Playwright test scenarios
- Critical user journeys
- Mock backend with MSW
- Cross-browser tests

### Domain Flags

#### `--domain [type]`
**Purpose**: Generate domain-specific test scenarios  
**Usage**: `/test:generate --all --domain e-commerce`  
**Options**: e-commerce, saas, skilled-trades, healthcare, fintech  
**Behavior**:
- Industry-specific test cases
- Compliance tests if needed
- Domain workflow tests

## /test Command Flags

### Test Execution Flags

#### `--quick`
**Purpose**: Run existing tests without creating new ones (minimal tokens)  
**Usage**: `/test --quick`  
**Token Usage**: ~50-100 tokens  
**Behavior**:
- Runs npm test or equivalent
- No agent involvement
- Fast execution

#### `--create`
**Purpose**: Create new test files using agents  
**Usage**: `/test --create`  
**Token Usage**: ~5000+ tokens  
**Behavior**:
- Triggers testing agents
- Creates comprehensive test coverage
- All tests go in __tests__/ directory

#### `--update`  
**Purpose**: Update existing tests using agents  
**Usage**: `/test --update`  
**Token Usage**: ~2000+ tokens  
**Behavior**:
- Modifies existing test files
- Uses agents for intelligent updates

### Test Scope Flags

#### `--frontend`
**Purpose**: Run only frontend tests  
**Usage**: `/test --frontend`  
**Behavior**:
- Component tests
- E2E tests with Playwright
- React/Vue/Angular specific

#### `--backend`
**Purpose**: Run only backend tests  
**Usage**: `/test --backend`  
**Behavior**:
- API endpoint tests
- Service layer tests
- Database operation tests

#### `--unit`
**Purpose**: Run only unit tests  
**Usage**: `/test --unit`  
**Behavior**:
- Isolated component tests
- No integration tests

#### `--e2e`
**Purpose**: Run only end-to-end tests  
**Usage**: `/test --e2e`  
**Behavior**:
- Full user flow tests
- Browser automation tests

#### `--ci`
**Purpose**: Trigger CI/CD pipeline  
**Usage**: `/test --ci`  
**Behavior**:
- Triggers GitHub Actions
- Monitors pipeline status
- Prevents duplicate runs

#### `--coverage`
**Purpose**: Generate test coverage report  
**Usage**: `/test --coverage`  
**Behavior**:
- Runs tests with coverage
- Shows coverage metrics

## /hotfix Command Flags

#### `--skip-tests`
**Purpose**: Skip test execution for emergency fixes  
**Usage**: `/hotfix --skip-tests`  
**Behavior**:
- Bypasses normal test requirements
- Use only for critical production issues

## /deploy Command Flags

#### `--production`
**Purpose**: Deploy to production environment  
**Usage**: `/deploy --production`  
**Behavior**:
- Runs production deployment
- May trigger additional checks

#### `--preview`
**Purpose**: Create preview deployment  
**Usage**: `/deploy --preview`  
**Behavior**:
- Creates temporary preview URL
- Useful for review before production

## Flag Combinations

Some commands support multiple flags:

### Examples
- `/test --backend --coverage` - Run backend tests with coverage
- `/work --status` then select issue to resume
- `/test --create --frontend` - Create new frontend tests only

## Best Practices

### When to Use Flags
1. **Use flags to modify behavior**, not as primary commands
2. **Explicit is better** - Use flags to be clear about intent
3. **Check token usage** - Some flags trigger high-token operations

### Flag Priority
When multiple flags are provided, they're processed in order:
1. Status/triage flags first
2. Action flags second  
3. Modifier flags last

### Common Patterns
- **No flags** = Smart defaults (auto-detect best action)
- **Single flag** = Specific behavior modification
- **Multiple flags** = Combined behaviors (where supported)

## Token Efficiency Guide

### Low Token Usage (~50-500)
- `/work --resume`
- `/work --status`
- `/test --quick`
- All flags that don't trigger agents

### High Token Usage (2000+)
- `/test --create`
- `/test --update`
- Any flag that triggers agent usage

## Future Flags (Planned)

### /work Command
- `--wip` - Create WIP commit before switching
- `--stash` - Stash changes before switching
- `--parallel` - Create worktree for parallel work

### /test Command  
- `--watch` - Run tests in watch mode
- `--debug` - Run with debug output
- `--only <pattern>` - Run specific test files

## Notes
- Flags must be prefixed with `--`
- Some flags accept values (e.g., `--discussion 125`)
- Flags are case-sensitive
- Unknown flags are ignored with a warning