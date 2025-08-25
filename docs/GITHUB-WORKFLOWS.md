# GitHub Workflows Documentation

## Overview
This repository uses 7 focused GitHub Actions workflows to automate the complete software development lifecycle from issue creation to production deployment.

## Core Philosophy: The Plumbing Layer 🔧

**"Automation = Plumbing, Not Decision Making"**

Think of GitHub workflows as the plumbing in a house:
- **Plumbing carries water** → Workflows move data (issues, code, deployments)
- **Plumbing doesn't decide water temperature** → Workflows don't decide priority
- **Plumbing just follows pipes** → Workflows follow predefined paths
- **The homeowner (Claude Code) decides** → AI agents make intelligent decisions

### The House Architecture Applied:
- **Foundation:** Your database and core data models
- **Plumbing (These Workflows):** Move things without thinking
- **Framing:** Your API and backend services  
- **Electrical (Claude Code/Agents):** The intelligence that makes decisions
- **Finishes:** Your frontend that users see
- **Smart Home (Project Board):** Monitors everything but doesn't control

Workflows are the plumbing - they move issues to boards, run tests, deploy code. They should NEVER try to be smart about it. The intelligence comes from the electrical system (Claude Code and agents).

## Workflow Files

### 1. **project-automation.yml**
**Trigger:** Issues and PRs (opened, edited, closed, converted, milestoned)  
**Purpose:** Manages comprehensive project board integration  
**Key Features:**
- Automatically adds issues/PRs to project board
- Sets initial Status field to "Todo"
- Sets Component field based on labels/content
- Manages Milestone assignments
- Tracks Sprint/Iteration assignments
- Updates Story Points from issue body
- Manages parent-child issue relationships
- Tracks blocked status and dependencies
- Uses PROJECT_TOKEN for authentication (requires project scope)
- Handles issue ↔ PR conversions

**Required Secrets:**
- `PROJECT_TOKEN`: Personal access token with `project` scope
- `PROJECT_ID`: Your project board ID
- Field IDs for Status, Priority, Component, Milestone, Iteration, Points, Blocked, Parent

### 2. **auto-assign.yml**
**Trigger:** Issue created  
**Purpose:** Auto-assigns issues to their creator  
**Logic:** Simple assignment to encourage ownership

### 3. **issue-to-implementation.yml**
**Trigger:** Issue created or labeled  
**Purpose:** Prepares development environment  
**Features:**
- Creates feature branch (format: `{type}/{issue-number}-{title}`)
- Generates implementation checklist
- Adds development instructions comment
- Creates draft PR if requested

### 4. **ci-cd-pipeline.yml**
**Trigger:** Pull requests and pushes to main  
**Purpose:** Complete CI/CD pipeline with strict quality gates  
**Stages:**
1. **Quality Check** - Linting and formatting
2. **Unit Tests** - Component/function tests  
3. **Integration Tests** - API and service tests
4. **Security Scan** - Vulnerability detection
5. **Build** - Production build verification
6. **Deploy** - Conditional deployment based on all gates passing

**Key Feature:** Strict gate enforcement - if ANY stage fails, deployment stops

### 5. **test-runner.yml**
**Trigger:** Pull requests, manual dispatch  
**Purpose:** Auto-detects project type and runs appropriate tests  
**Supported Languages:**
- JavaScript/TypeScript (npm, yarn, pnpm)
- Python (pytest, unittest)
- Go (go test)
- Rust (cargo test)

**Features:**
- Automatic language detection
- Coverage reporting
- Test result summaries

### 6. **deploy-frontend.yml**
**Trigger:** 
- Push to main (frontend paths)
- Pull requests (frontend paths)
- Manual dispatch

**Purpose:** Deploy frontend to Vercel  
**Path Filters:**
- `frontend/**`, `client/**`, `src/**`
- `components/**`, `pages/**`, `app/**`
- Excludes backend paths

**Environments:**
- **Preview:** Automatic on PRs
- **Production:** Automatic on main branch

**Features:**
- Framework auto-detection (Next.js, React, Vue, Angular)
- Preview URLs on PRs
- Environment-specific variables

### 7. **deploy-backend.yml**
**Trigger:**
- Push to main (backend paths)
- Pull requests (backend paths)  
- Manual dispatch

**Purpose:** Deploy backend to DigitalOcean  
**Path Filters:**
- `backend/**`, `api/**`, `server/**`
- `src/api/**`
- Excludes frontend paths

**Environments:**
- **Staging:** On PRs or manual trigger
- **Production:** On main branch push

**Features:**
- Framework detection (Express, Fastify, NestJS, Python, Go)
- Docker or App Platform deployment
- Database migration support
- Health checks

## Environment Variables & Secrets

### Required GitHub Secrets

#### Core Automation
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions
- `PROJECT_TOKEN`: Personal access token with `project` scope
- `PROJECT_ID`: GraphQL ID of your project board

#### Project Board Field IDs
- `FIELD_STATUS_ID`: ID of Status field
- `FIELD_PRIORITY_ID`: ID of Priority field  
- `FIELD_COMPONENT_ID`: ID of Component field
- `FIELD_MILESTONE_ID`: ID of Milestone field
- `FIELD_ITERATION_ID`: ID of Iteration/Sprint field
- `FIELD_POINTS_ID`: ID of Story Points field
- `FIELD_BLOCKED_ID`: ID of Blocked field
- `FIELD_PARENT_ID`: ID of Parent Issue field
- `STATUS_TODO`, `STATUS_IN_PROGRESS`, `STATUS_REVIEW`, `STATUS_DONE`, `STATUS_BLOCKED`: Option IDs
- `PRIORITY_P0`, `PRIORITY_P1`, `PRIORITY_P2`, `PRIORITY_P3`: Option IDs
- `COMPONENT_FRONTEND`, `COMPONENT_BACKEND`, `COMPONENT_INFRA`, `COMPONENT_DOCS`: Option IDs

#### Deployment - Vercel
- `VERCEL_TOKEN`: Vercel authentication token
- `VERCEL_ORG_ID`: Organization ID
- `VERCEL_PROJECT_ID`: Project ID
- `PREVIEW_API_URL`: API URL for preview environment
- `PRODUCTION_API_URL`: API URL for production

#### Deployment - DigitalOcean
- `DIGITALOCEAN_ACCESS_TOKEN`: DO API token
- `DO_APP_ID`: App Platform application ID
- `DO_STAGING_APP_ID`: Staging app ID
- `DO_REGISTRY_NAME`: Container registry name
- `STAGING_FRONTEND_URL`: Frontend URL for staging

## Workflow Triggers & Events

### Issue Events
```yaml
on:
  issues:
    types: [opened, edited, labeled, closed]
```
**Triggered by:** Creating, editing, labeling, or closing issues  
**Workflows:** project-automation, auto-assign, issue-to-implementation

### Pull Request Events
```yaml
on:
  pull_request:
    types: [opened, edited, synchronize, closed]
```
**Triggered by:** Creating, updating, or merging PRs  
**Workflows:** project-automation, ci-cd-pipeline, test-runner, deploy-frontend, deploy-backend

### Push Events
```yaml
on:
  push:
    branches: [main]
    paths: [specific paths]
```
**Triggered by:** Direct pushes or PR merges to main  
**Workflows:** ci-cd-pipeline, deploy-frontend, deploy-backend

### Manual Dispatch
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        type: choice
```
**Triggered by:** Manual workflow runs from GitHub UI  
**Workflows:** test-runner, deploy-frontend, deploy-backend

## Complete Flow: Issue → Production

### Step 1: Issue Creation
User creates issue → 3 workflows trigger in parallel:
- `project-automation.yml` → Adds to project board
- `auto-assign.yml` → Assigns to creator
- `issue-to-implementation.yml` → Creates branch

### Step 2: Development
Developer/Agent:
1. Checks out auto-created branch
2. Implements solution
3. Commits and pushes changes
4. Creates pull request

### Step 3: PR Testing & Review
PR created → Workflows trigger:
- `ci-cd-pipeline.yml` → Runs all quality gates
- `test-runner.yml` → Runs project-specific tests
- `label-sync.yml` → Validates and enforces allowed labels

### Step 4: Merge & Deploy
PR approved and merged → After CI passes:
- `project-automation.yml` → Updates issue status to "Done"
- `deploy-frontend.yml` → Deploys to Vercel if frontend files changed
- `deploy-backend.yml` → Deploys to DigitalOcean if backend files changed

## Getting Field IDs for Project Board

### 1. Get Project ID
```bash
gh api graphql -f query='
  query {
    user(login: "YOUR_USERNAME") {
      projectV2(number: YOUR_PROJECT_NUMBER) {
        id
      }
    }
  }'
```

### 2. Get Field IDs
```bash
gh api graphql -f query='
  query {
    user(login: "YOUR_USERNAME") {
      projectV2(number: YOUR_PROJECT_NUMBER) {
        fields(first: 20) {
          nodes {
            ... on ProjectV2SingleSelectField {
              id
              name
              options {
                id
                name
              }
            }
          }
        }
      }
    }
  }'
```

### 3. Set Secrets
```bash
# Set PROJECT_TOKEN (use your personal access token)
gh secret set PROJECT_TOKEN

# Set field IDs
gh secret set PROJECT_ID --body "PVT_..."
gh secret set FIELD_STATUS_ID --body "PVTSSF_..."
gh secret set STATUS_TODO --body "option-id"
# ... etc
```

## Testing Workflows

### Test Issue Creation Flow
```bash
# Create test issue
gh issue create --title "[TEST] Feature request" \
  --body "Test issue for workflow validation" \
  --label "type:feature"

# Watch workflows
gh run list --limit 5

# Check project board
gh project view YOUR_PROJECT_NUMBER --owner YOUR_USERNAME --web
```

### Test PR Flow
```bash
# Create test branch
git checkout -b test/workflow-validation

# Make changes and push
echo "test" > test.txt
git add . && git commit -m "Test workflows"
git push origin test/workflow-validation

# Create PR
gh pr create --title "Test PR" --body "Testing workflows"

# Monitor workflow runs
gh run watch
```

### Manual Workflow Trigger
```bash
# Trigger test runner
gh workflow run test-runner.yml

# Trigger deployment with specific environment
gh workflow run deploy-frontend.yml -f environment=preview
```

## Troubleshooting

### Common Issues

#### 1. Project Board Not Updating
**Error:** "Could not resolve to a ProjectV2"  
**Solution:** Ensure PROJECT_TOKEN has `project` scope and is from the project owner

#### 2. Multiple Workflow Runs
**Issue:** Same workflow firing multiple times  
**Solution:** Check for overlapping triggers in workflow files

#### 3. Deployment Failing
**Issue:** Environment variables not set  
**Solution:** Verify all required secrets are configured in repository settings

#### 4. Test Detection Failing
**Issue:** Tests not running automatically  
**Solution:** Ensure package.json has "test" script or appropriate test files exist

### Debug Commands

```bash
# View recent workflow runs
gh run list --limit 10

# View specific run details
gh run view RUN_ID

# View workflow logs
gh run view RUN_ID --log

# Re-run failed workflow
gh run rerun RUN_ID

# Check secret existence (not values)
gh secret list
```

## Best Practices

### 1. Workflow Design
- Keep workflows focused on single responsibilities
- Use path filters to prevent unnecessary runs
- Implement proper error handling and continue-on-error where appropriate

### 2. Security
- Never log sensitive information
- Use GitHub Secrets for all credentials
- Implement least-privilege principle for tokens

### 3. Performance
- Use caching for dependencies (node_modules, pip packages)
- Run jobs in parallel when possible
- Use matrix builds for multiple versions/platforms

### 4. Maintenance
- Document all required secrets
- Keep workflow files versioned and reviewed
- Test workflows in separate branches before merging

## Future Enhancements

### Planned Improvements
1. **Intelligent Priority Setting**: Claude Code analyzes issues and sets priority
2. **Auto-generated Test Cases**: AI creates tests based on implementation
3. **Performance Monitoring**: Automatic performance regression detection
4. **Dependency Updates**: Automated dependency PR creation
5. **Release Automation**: Semantic versioning and changelog generation

### Agent Integration Points
- Claude Code hooks for intelligent decision making
- GitHub Copilot for code suggestions
- Custom agents for specialized tasks

---

## Quick Reference

### Workflow Files Location
```
.github/workflows/
├── auto-assign.yml            # Issue assignment
├── ci-cd-pipeline.yml         # Testing & quality checks
├── deploy-backend.yml         # Backend deployment (after CI)
├── deploy-frontend.yml        # Frontend deployment (after CI)
├── issue-to-implementation.yml # Development setup
├── label-sync.yml            # Label management
├── project-automation.yml     # Project board sync
└── test-runner.yml           # Test automation
```

### Key Commands
```bash
# Check workflow status
gh workflow list

# View runs
gh run list

# Trigger manual run
gh workflow run WORKFLOW_NAME

# View project board
gh project view PROJECT_NUMBER --owner USERNAME --web
```

### Required Setup Checklist
- [ ] Create GitHub Project Board
- [ ] Get all field IDs using GraphQL
- [ ] Set PROJECT_TOKEN secret with project scope
- [ ] Configure all field ID secrets
- [ ] Set deployment platform credentials
- [ ] Test with sample issue

---

*Last Updated: 2025-08-23*
*Version: 1.0*