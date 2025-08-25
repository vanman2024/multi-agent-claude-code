# Copilot Instructions for Multi-Agent Development Framework

## Project Overview
This is a sophisticated Multi-Agent Development Framework that orchestrates AI agents, human developers, and automated workflows to achieve 10x productivity gains in software development. The framework uses GitHub as the central data layer and coordination hub, with Claude Code CLI as the primary orchestrator and GitHub Copilot as an autonomous development agent.

## Repository Structure
- `/docs/` - Framework documentation and architecture guides
- `/.github/workflows/` - CI/CD pipelines and automation workflows
- `/.github/` - GitHub configuration and this instructions file
- `/templates/` - Issue and feature specification templates
- `/agents/` - Agent configurations (when implemented)
- `/commands/` - Custom slash commands for Claude Code (when implemented)
- `/hooks/` - Automation hooks for real-time coordination (when implemented)

## Architecture & Key Concepts

### Component-Based Routing
Issues are automatically routed to appropriate specialists based on labels:
- `component/frontend` → UI/React components
- `component/backend` → API endpoints, server logic
- `component/database` → Schema, migrations
- `component/devops` → CI/CD, deployment
- `component/testing` → Test suites, QA

### Work Type Classification
- `type/feature` → New functionality
- `type/bug` → Issue resolution
- `type/refactor` → Code improvement
- `type/deploy` → Deployment operations

### Priority Levels
- `priority/P0` → Critical, immediate attention
- `priority/P1` → High priority
- `priority/P2` → Medium priority
- `priority/P3` → Low priority

## Development Workflow

### ALWAYS follow this sequence:
1. Read the GitHub issue completely for acceptance criteria
2. Check for blocking dependencies in issue description
3. Verify prerequisites before implementation
4. Run tests after making changes
5. Ensure CI/CD pipeline passes

### Build and Test Commands
```bash
# Always run these in order:
npm install          # Install dependencies first
npm run lint         # Check code quality
npm run typecheck    # Verify TypeScript types
npm run test         # Run test suite
npm run build        # Build the project
```

### Git Workflow
- Create branches with pattern: `copilot/feature-name`
- Commit messages format: `type: description` (e.g., `feat: add user auth`)
- Always create draft PRs initially
- Link PRs to original issues

## Issue Structure Standards

### Feature Issues Include:
- **Project Metadata**: Priority, Component, Complexity, Points
- **Executive Summary**: Clear problem statement
- **User Story**: As a/I want to/So that format
- **Acceptance Criteria**: Checklist of requirements
- **Dependencies**: Blocking issues listed explicitly

### When You See These Patterns:
- `Blocked by: #XX` → DO NOT start work until blocker is resolved
- `Component: Frontend` → Focus on React/UI implementation
- `Component: Backend` → Focus on API/server implementation
- `Complexity: XL` → Break into smaller subtasks

## Code Standards

### Frontend Development
- Use functional React components with hooks
- Apply Tailwind CSS for styling
- Implement responsive design
- Follow existing component patterns in `/src/components`

### Backend Development
- RESTful API design
- Proper error handling with specific messages
- Input validation on all endpoints
- Follow existing patterns in `/src/api`

### Testing Requirements
- Unit tests for all new functions
- Integration tests for API endpoints
- Maintain 80% code coverage minimum
- Use existing test patterns

## Quality Gates

### Before Marking Any Task Complete:
1. All acceptance criteria checked
2. Tests written and passing
3. Linting passes without errors
4. Type checking passes
5. Documentation updated if needed

### CI/CD Pipeline Checks
The pipeline runs automatically and checks:
- Code quality (ESLint, Prettier)
- Type safety (TypeScript)
- Test coverage (Jest)
- Build success
- Security scanning

## Integration with Multi-Agent System

### You Are Part of a Larger System:
- Claude Code orchestrates complex tasks
- You handle well-defined implementation tasks
- GitHub Actions handle deployment
- Project boards track progress

### Coordination Points:
- Update issue status when starting work
- Create draft PR immediately
- Request review when complete
- Respond to review feedback via @copilot mentions

## Important Patterns to Follow

### Database Changes
Always create migrations, never modify schema directly:
```bash
npm run migration:create -- --name descriptive-name
npm run migration:run
```

### API Endpoints
Follow RESTful conventions:
- GET /api/resources - List
- GET /api/resources/:id - Get one
- POST /api/resources - Create
- PUT /api/resources/:id - Update
- DELETE /api/resources/:id - Delete

### Error Handling
Always use specific error messages:
```javascript
throw new Error(`Failed to process ${resourceType}: ${specificReason}`);
```

## What NOT to Do

### NEVER:
- Start work on issues with unresolved blockers
- Skip testing "to save time"
- Ignore CI/CD failures
- Modify main branch directly
- Create PRs without linking to issues
- Ignore acceptance criteria

### ALWAYS:
- Check dependencies first
- Write tests for new code
- Follow existing patterns
- Update documentation
- Link PRs to issues
- Respond to review feedback

## Debugging Common Issues

### If Tests Fail:
1. Run tests locally first: `npm test`
2. Check test output for specific failures
3. Fix issues before pushing

### If CI/CD Fails:
1. Check GitHub Actions tab for details
2. Common issues: lint errors, type errors, test failures
3. Fix locally and push updates

### If Blocked:
1. Check issue for blocking dependencies
2. Verify all prerequisites are met
3. Ask for clarification in issue comments

## Trust These Instructions
These instructions are specifically tailored for this Multi-Agent Development Framework. Trust them over generic patterns. Only search for additional information if these instructions are incomplete or incorrect for your specific task.

## Framework-Specific Context
This repository IS the Multi-Agent Development Framework - you're helping build the system that orchestrates development work. When implementing features, consider how they fit into the larger agent orchestration system.