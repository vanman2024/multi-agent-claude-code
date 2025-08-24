---
allowed-tools: Task(*), Bash(*), Read(*), Write(*), TodoWrite(*), mcp__supabase(*)
description: Build a feature from an existing specification document
argument-hint: [feature-name or spec-file-path]
---

# Build Feature from Sprint

## Context
- Current sprint items: ![gh project item-list PROJECT_NUMBER --limit 20 --format json | jq '.items[] | select(.iteration == "Current Sprint")'
- Current branch: ![git branch --show-current]
- Project structure: @package.json

## Your Task

When user runs `/build-feature $ARGUMENTS`, implement the feature from the sprint board:

If $ARGUMENTS is provided:
- Build the specific issue number or feature name

If NO $ARGUMENTS (recommended for sprint work):
- Pick the highest priority item from current sprint automatically

### Step 0: Select Work Item from Sprint (if no argument)
If no $ARGUMENTS provided, select from sprint:
```bash
# Find the connected project
PROJECT_DATA=$(gh api graphql -f query='
{
  repository(owner: "'$(gh repo view --json owner -q .owner.login)'", name: "'$(gh repo view --json name -q .name)'") {
    projectsV2(first: 1) {
      nodes {
        id
        number
        items(first: 100) {
          nodes {
            id
            content {
              ... on Issue {
                number
                title
                state
              }
            }
            fieldValues(first: 10) {
              nodes {
                ... on ProjectV2ItemFieldIterationValue {
                  field { ... on ProjectV2IterationField { name } }
                  title
                  startDate
                }
                ... on ProjectV2ItemFieldSingleSelectValue {
                  field { ... on ProjectV2SingleSelectField { name } }
                  name
                }
              }
            }
          }
        }
      }
    }
  }
}')

# Find current sprint items with Status=Todo, sorted by Priority
CURRENT_DATE=$(date +%Y-%m-%d)
NEXT_ITEM=$(echo "$PROJECT_DATA" | jq -r '
  .data.repository.projectsV2.nodes[0].items.nodes[] |
  select(.content.state == "OPEN") |
  select(.fieldValues.nodes[] | select(.field.name == "Status" and .name == "Todo")) |
  select(.fieldValues.nodes[] | select(.field.name == "Iteration" and .startDate <= "'$CURRENT_DATE'")) |
  {
    number: .content.number,
    title: .content.title,
    priority: (.fieldValues.nodes[] | select(.field.name == "Priority").name // "P3")
  }' | sort -t: -k3 | head -1)

ISSUE_NUMBER=$(echo "$NEXT_ITEM" | jq -r '.number')
echo "Selected issue #$ISSUE_NUMBER from current sprint"
```

### Step 1: Load Feature from Issue
Use GitHub issue as specification:
```bash
# Get issue details
gh issue view $ISSUE_NUMBER --json title,body,labels,milestone

# Update issue status to In Progress
gh api graphql -f query='
mutation {
  updateProjectV2ItemFieldValue(input: {
    projectId: "'$PROJECT_ID'"
    itemId: "'$ITEM_ID'"
    fieldId: "'$STATUS_FIELD'"
    value: { singleSelectOptionId: "'$IN_PROGRESS_ID'" }
  }) {
    projectV2Item { id }
  }
}'
```

### Step 2: Setup Feature Branch
Use Task tool with:
- subagent_type: workspace-manager
- description: Create feature branch and setup
- prompt: |
  Setup workspace for feature: $ARGUMENTS
  
  Tasks:
  1. Create feature branch: git checkout -b feat/$ARGUMENTS
  2. Create feature directory structure
  3. Setup initial files and folders
  4. Configure any needed dependencies
  5. Update package.json if needed
  
  Prepare clean workspace for implementation.

### Step 3: Build Database Layer
Use Task tool with:
- subagent_type: database-build
- description: Implement database schema from spec
- prompt: |
  Implement database layer for feature: $ARGUMENTS
  
  Using the specification, execute:
  1. Create migration files
  2. Apply database migrations
  3. Create indexes and constraints
  4. Setup RLS policies if needed
  5. Insert seed data if specified
  6. Verify schema matches specification
  
  Follow the exact schema design from the feature spec.

### Step 4: Build Backend Services
Use Task tool with:
- subagent_type: backend-build
- description: Implement backend services and APIs
- prompt: |
  Build backend services for feature: $ARGUMENTS
  
  Following the API specification:
  1. Create service layer classes
  2. Implement business logic
  3. Build API endpoints (REST or GraphQL)
  4. Add validation and error handling
  5. Implement authentication/authorization
  6. Add logging and monitoring
  
  Ensure all endpoints match the specification exactly.

### Step 5: Build Frontend Components
Use Task tool with:
- subagent_type: frontend-build
- description: Implement UI components from spec
- prompt: |
  Build frontend components for feature: $ARGUMENTS
  
  Following the UI specification:
  1. Create React components hierarchy
  2. Implement state management
  3. Build forms and validations
  4. Add API integrations
  5. Implement error handling UI
  6. Ensure responsive design
  7. Add accessibility features
  
  Match the component structure from the specification.

### Step 6: Write Tests
Use Task tool with:
- subagent_type: test-writer
- description: Implement test suite from spec
- prompt: |
  Write tests for feature: $ARGUMENTS
  
  Following the test specification:
  1. Write unit tests for services
  2. Write component tests for UI
  3. Create integration tests for APIs
  4. Build E2E tests for user flows
  5. Add performance tests if specified
  6. Ensure minimum 80% coverage
  
  Implement all test scenarios from the specification.

### Step 7: Run Tests and Validate
Use Task tool with:
- subagent_type: test-runner
- description: Execute all tests and validate
- prompt: |
  Run complete test suite for feature: $ARGUMENTS
  
  Execute:
  1. Run unit tests: npm test
  2. Run integration tests
  3. Run E2E tests
  4. Check code coverage
  5. Run linting and type checking
  6. Performance benchmarks if specified
  
  Fix any failing tests and ensure all pass.

### Step 8: Documentation and Integration
Use Task tool with:
- subagent_type: documentation-agent
- description: Update documentation and integrate
- prompt: |
  Complete documentation for feature: $ARGUMENTS
  
  Tasks:
  1. Update API documentation
  2. Add code comments and JSDoc
  3. Update README with new feature
  4. Create user guide if needed
  5. Update CHANGELOG.md
  6. Add feature to main navigation/menu
  
  Ensure feature is fully integrated and documented.

### Step 9: Create Pull Request
Use Task tool with:
- subagent_type: pr-creator
- description: Create PR for feature
- prompt: |
  Create pull request for feature: $ARGUMENTS
  
  Using GitHub CLI:
  1. Stage all changes: git add .
  2. Commit with message: git commit -m "feat: implement $ARGUMENTS"
  3. Push branch: git push -u origin feat/$ARGUMENTS
  4. Create PR: gh pr create --title "feat: $ARGUMENTS" --body "..."
  5. Link to original specification issue
  6. Add reviewers if configured
  
  Include implementation notes and test results in PR description.

### Step 10: Update Tracking
Use Task tool with:
- subagent_type: database-build
- description: Update feature status in database
- prompt: |
  Update feature tracking for: $ARGUMENTS
  
  Update in Supabase:
  1. Mark feature status as "implemented"
  2. Record PR number and URL
  3. Add implementation metrics
  4. Update completion timestamp
  5. Record test coverage percentage
  6. Link all created files
  
  This completes the feature implementation cycle.

## Success Criteria
- All components match specification exactly
- Tests achieve minimum 80% coverage
- All tests pass
- Code follows project conventions
- Documentation is complete
- PR is created and ready for review
- Feature is fully functional

## Notes
- This command requires an existing feature specification
- Run `/create-feature-spec` first if no spec exists
- The implementation strictly follows the specification
- Each agent focuses on their specialized area
- The workflow ensures complete implementation