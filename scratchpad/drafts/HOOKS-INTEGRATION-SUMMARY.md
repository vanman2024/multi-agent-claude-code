# Deployment Integration with Slash Commands, Hooks & Sub-Agents

## How Deployment Flows Through the System

### 1. The Complete Pipeline

```
Issue → Work → Code → Test → Deploy → Release
  ↓       ↓      ↓      ↓       ↓        ↓
Commands Agents  Hooks  CI/CD  Vercel  GitHub
```

## Slash Command Integration

### Primary Commands in Deployment Flow

#### `/create-issue` → Planning Phase
- Creates GitHub issue with proper templates
- Auto-assigns to Copilot (simple) or flags for Claude Code (complex)
- **NO deployment yet** - just planning

#### `/work #123` → Implementation Phase  
- Creates feature branch from main
- Routes to appropriate agent based on complexity
- Updates issue status to "in-progress"
- **Triggers**: Hooks for context loading

#### `/deploy [environment]` → Deployment Phase
- Pre-deployment checks (uncommitted changes, branch status)
- Runs tests unless `--skip-tests`
- Deploys to Vercel (preview/staging/production)
- **Integration**: 
  - Uses Vercel CLI directly
  - Creates GitHub deployment records
  - Comments on PRs with deployment URLs
  - Triggers webhooks if configured

### The `/deploy` Command Specifically

Located in `.claude/commands/deploy.md`, it:

1. **Environment Routing**:
   - `preview` (default) - any branch
   - `staging` - typically from main
   - `production` - MUST be from main

2. **Vercel Integration**:
   ```bash
   # Preview/staging
   vercel --token=$VERCEL_TOKEN
   
   # Production
   vercel --prod --token=$VERCEL_TOKEN
   ```

3. **API/Webhook Support**:
   - Automatically detects `/api` folders
   - Configures serverless functions
   - Provides webhook URLs for testing

## Hooks System Integration

### Deployment-Related Hooks

#### `test-before-push.sh` (PreToolUse)
- **Triggers**: Before any `git push` command
- **Purpose**: Prevents broken code from reaching GitHub
- **Deployment Impact**: Ensures only tested code enters CI/CD pipeline
- Runs appropriate test suite (npm test, pytest, go test)
- Blocks push if tests fail (exit code 2)

#### `sync-to-github.sh` (Conceptual)
- Could sync deployment status back to GitHub
- Update issue/PR with deployment URLs
- Track deployment success/failure

### Hook Events in Deployment Context

```javascript
{
  "hooks": {
    // Before pushing code that triggers deployment
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "command": "test-before-push.sh"  // Validates before CI/CD
      }]
    }],
    
    // After deployment completes
    "PostToolUse": [{
      "matcher": "mcp__vercel",  // If using Vercel MCP
      "hooks": [{
        "command": "notify-deployment.sh"  // Update team
      }]
    }]
  }
}
```

## Sub-Agent Roles in Deployment

### `backend-tester` Agent
**Role in Deployment Pipeline**:
- Writes backend code with tests
- Validates locally BEFORE pushing
- Ensures CI/CD will pass
- **Key Actions**:
  - Runs test suites locally
  - Validates API endpoints
  - Checks database operations
  - Pushes only when all tests pass

### `frontend-playwright-tester` Agent  
**Role in Deployment Pipeline**:
- E2E testing of deployed previews
- Validates UI after deployment
- Tests cross-browser compatibility
- **Post-Deploy Actions**:
  - Tests against preview URLs
  - Validates user flows
  - Screenshots for visual regression

### `security-auth-compliance` Agent
**Role in Deployment Pipeline**:
- Pre-deployment security audit
- Validates no secrets in code
- Checks auth configurations
- **Security Gates**:
  - Scans for exposed credentials
  - Validates CORS settings
  - Reviews API security

### `system-architect` Agent
**Role in Deployment Pipeline**:
- Plans deployment architecture
- Configures environments
- Sets up CI/CD pipelines
- **Infrastructure Decisions**:
  - Environment variables
  - Database connections
  - CDN configuration

## The Integration Flow

### Typical Deployment Scenario

1. **Issue Created** (`/create-issue`)
   - Planning only, no deployment

2. **Work Begins** (`/work #123`)
   - Branch created
   - Agent selected based on complexity
   - Hooks load context

3. **Development**
   - Agent writes code
   - Hooks validate on save
   - Tests run locally

4. **Pre-Push Validation**
   - `test-before-push.sh` hook fires
   - Blocks if tests fail
   - Ensures quality gate

5. **Push to GitHub**
   - Triggers GitHub Actions
   - Automatic preview deployment on PR

6. **Manual Deployment** (`/deploy staging`)
   - Runs pre-flight checks
   - Deploys to Vercel
   - Updates GitHub status

7. **Production Release** (`/deploy production`)
   - Must be from main branch
   - Full test suite runs
   - Creates GitHub release

## Environment Variable Flow

### Handled by `/deploy` Command
```bash
# Sets Vercel environment variables
vercel env add DATABASE_URL production
vercel env add API_KEY production

# Different per environment
.env.preview   → Preview deployments
.env.staging   → Staging environment  
.env.production → Production only
```

## Webhook and API Configuration

### Automatic Detection
The `/deploy` command detects:
- `/api` folders → Serverless functions
- `/pages/api` → Next.js API routes
- `/app/api` → Next.js App Router

### Webhook URLs Generated
```
Preview: https://preview-xxx.vercel.app/api/webhooks
Staging: https://staging.vercel.app/api/webhooks
Production: https://app.com/api/webhooks
```

## CI/CD Integration Points

### GitHub Actions Triggers
- Push to main → Auto-deploy to staging
- PR created → Preview deployment
- Tag created → Production release

### Vercel Integration
- Every PR gets preview URL
- Main branch → Staging
- Tags → Production

## Key Insights

### 1. **Slash Commands Orchestrate**
- `/create-issue` → Planning
- `/work` → Implementation
- `/deploy` → Deployment
Each command has specific role in pipeline

### 2. **Hooks Provide Local Intelligence**
- Pre-validation before expensive CI/CD
- Context injection for agents
- Personal workflow optimization
- NOT deployment automation (GitHub does that)

### 3. **Agents Handle Complexity**
- Simple tasks → Direct implementation
- Complex tasks → Specialized agents
- Each agent understands deployment requirements
- Agents ensure deployment-ready code

### 4. **Vercel Simplifies Deployment**
- Automatic preview deployments
- Serverless functions from `/api`
- No complex configuration needed
- Instant rollbacks available

## The Key Separation

### Local (Your Machine)
- **Hooks**: Personal automation, pre-flight checks
- **Agents**: Code generation, local testing
- **Commands**: Workflow orchestration

### Remote (GitHub/Vercel)
- **GitHub Actions**: CI/CD pipelines
- **Vercel**: Hosting and deployment
- **GitHub**: Source of truth

This separation ensures:
- No duplicate automation
- Clear responsibilities
- Fast local feedback
- Reliable remote deployment