---
allowed-tools: Task(*), mcp__github(*), Bash(*), Read(*), Write(*), TodoWrite(*), Edit(*), MultiEdit(*), Grep(*), Glob(*)
description: Create a complete feature with specification, GitHub issue, and project tracking
argument-hint: [feature-name] [priority:P0/P1/P2] [effort:XS/S/M/L/XL] [project-number:optional]
---

# Create Feature

## Context
- Current branch: !`git branch --show-current`
- Project info: @package.json
- Git status: !`git status --short`
- Repository: !`git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/'`

## Your Task

When user runs `/create-feature $ARGUMENTS`, orchestrate the complete feature creation process:

### Phase 1: Feature Specification & Planning

#### Step 1: Create Feature Specification
1. Read the template: @templates/feature-specification-card.md (or fallback to @/home/gotime2022/Projects/mcp-kernel-new/.claude/templates/feature-specification-card.md)
2. Ask the user: 
   - "What feature do you want to build? Please describe what it should do, who will use it, and what problem it solves."
   - "What priority is this? (P0=Critical, P1=High, P2=Medium, P3=Low)"
   - "When should this be worked on? (current sprint/next sprint/future)" - optional, defaults based on priority
3. Fill in the template based on the user's requirements and your technical analysis
4. Save the completed specification to `docs/features/FEAT-{timestamp}-{feature-name}.md`
5. Show the user the key sections for review before creating the issue

#### Step 2: Determine Complexity and Size
Ask the user to assess:
- "What's the complexity? (1=Trivial, 2=Simple, 3=Moderate, 4=Complex, 5=Very Complex)"
  - 1: Following exact patterns, no decisions
  - 2: Minor variations, clear requirements  
  - 3: Multiple components, some design decisions
  - 4: Architectural decisions, system interactions
  - 5: Novel solutions, performance challenges
- "What's the size/effort? (XS=<1 day, S=1-2 days, M=3-5 days, L=1-2 weeks, XL=>2 weeks)"

Assignment decision based on BOTH complexity and size:
- **Complexity 1-2 AND Size XS/S**: Will assign to GitHub Copilot
- **Complexity 3+ OR Size M/L/XL**: Will be handled by Claude Code/agents

(Even simple tasks need orchestration if they're medium or larger)

#### Step 3: Create GitHub Issue with MCP
Use mcp__github__create_issue to create the issue:
```javascript
const issueData = {
  owner: "vanman2024",
  repo: "multi-agent-claude-code", 
  title: featureName,
  body: featureSpecification + "\n\n**Complexity:** " + complexity + "\n**Size:** " + size,
  labels: ["feature"],
  assignees: ["@me"],
  milestone: determineMilestone(priority)
};

const issue = await mcp__github__create_issue(issueData);
const issueNumber = issue.number;
```

#### Step 4: Assign Based on Complexity AND Size
Check both complexity and size to determine assignment:
```javascript
// Copilot can only handle small, simple tasks
const isSmallAndSimple = (complexity <= 2) && (size === 'XS' || size === 'S');

if (isSmallAndSimple) {
  // Small AND simple task - assign to Copilot
  await mcp__github__assign_copilot_to_issue({
    owner: "vanman2024",
    repo: "multi-agent-claude-code",
    issueNumber: issueNumber
  });
  
  // Add comment with Copilot instructions
  await mcp__github__add_issue_comment({
    owner: "vanman2024",
    repo: "multi-agent-claude-code",
    issue_number: issueNumber,
    body: `🤖 **Assigned to GitHub Copilot** (Complexity: ${complexity}, Size: ${size})

This is a small, simple task suitable for Copilot implementation.

@copilot Please implement this feature following the specifications above.

### Key Requirements:
- Follow the acceptance criteria exactly
- Use existing patterns from the codebase  
- Add proper error handling and validation
- Include unit tests for new functionality
- Ensure mobile responsiveness for UI components`
  });
} else {
  // Complex OR medium/large task - needs Claude Code/agents
  const reason = complexity >= 3 
    ? `high complexity (${complexity})` 
    : `size ${size} requires orchestration`;
    
  await mcp__github__add_issue_comment({
    owner: "vanman2024",
    repo: "multi-agent-claude-code", 
    issue_number: issueNumber,
    body: `🧠 **Requires Advanced Implementation** (Complexity: ${complexity}, Size: ${size})

This feature needs Claude Code orchestration due to ${reason}.

Tasks of size M/L/XL require:
- Breaking down into subtasks
- Coordination across components
- Progress tracking
- Comprehensive testing

Next step: Run \`/build-feature ${issueNumber}\` when ready to begin implementation.`
  });
}
```

The GitHub workflows will automatically:
- Assign issue to creator (auto-assign.yml)
- Create feature branch: `feature/{issue-number}-{feature-name}` (issue-to-implementation.yml)

#### Step 5: Set Project Board Fields
After issue creation, set all project fields intelligently:
```bash
# Get issue number from creation output
ISSUE_NUMBER={number}

# Find THE project connected to THIS repository
PROJECT_DATA=$(gh api graphql -f query='
{
  repository(owner: "'$(gh repo view --json owner -q .owner.login)'", name: "'$(gh repo view --json name -q .name)'") {
    projectsV2(first: 10) {
      nodes {
        id
        number
        title
        fields(first: 30) {
          nodes {
            ... on ProjectV2Field {
              id
              name
              dataType
            }
            ... on ProjectV2SingleSelectField {
              id
              name
              options {
                id
                name
              }
            }
            ... on ProjectV2IterationField {
              id
              name
              configuration {
                iterations {
                  id
                  title
                  startDate
                }
              }
            }
          }
        }
      }
    }
  }
}')

# Get the FIRST (and usually only) project connected to this repo
PROJECT_ID=$(echo "$PROJECT_DATA" | jq -r '.data.repository.projectsV2.nodes[0].id')
PROJECT_NUMBER=$(echo "$PROJECT_DATA" | jq -r '.data.repository.projectsV2.nodes[0].number')

if [ -z "$PROJECT_ID" ]; then
  echo "ERROR: No project connected to this repository!"
  echo "Run 'gh project link' to connect a project first"
  exit 1
fi

echo "Using project: #$PROJECT_NUMBER"

# Get field IDs from the connected project
STATUS_FIELD=$(echo "$PROJECT_DATA" | jq -r '.data.repository.projectsV2.nodes[0].fields.nodes[] | select(.name == "Status") | .id')
PRIORITY_FIELD=$(echo "$PROJECT_DATA" | jq -r '.data.repository.projectsV2.nodes[0].fields.nodes[] | select(.name == "Priority") | .id')
COMPONENT_FIELD=$(echo "$PROJECT_DATA" | jq -r '.data.repository.projectsV2.nodes[0].fields.nodes[] | select(.name == "Component") | .id')
SIZE_FIELD=$(echo "$PROJECT_DATA" | jq -r '.data.repository.projectsV2.nodes[0].fields.nodes[] | select(.name == "Size") | .id')
COMPLEXITY_FIELD=$(echo "$PROJECT_DATA" | jq -r '.data.repository.projectsV2.nodes[0].fields.nodes[] | select(.name == "Complexity") | .id')
ITERATION_FIELD=$(echo "$PROJECT_DATA" | jq -r '.data.repository.projectsV2.nodes[0].fields.nodes[] | select(.name == "Iteration") | .id')
CREATED_DATE_FIELD=$(echo "$PROJECT_DATA" | jq -r '.data.repository.projectsV2.nodes[0].fields.nodes[] | select(.name == "Created Date") | .id')
DUE_DATE_FIELD=$(echo "$PROJECT_DATA" | jq -r '.data.repository.projectsV2.nodes[0].fields.nodes[] | select(.name == "Due Date") | .id')

# Add issue to project if not already added
ISSUE_NODE_ID=$(gh api repos/$(gh repo view --json nameWithOwner -q .nameWithOwner)/issues/$ISSUE_NUMBER --jq .node_id)

gh api graphql -f query='
mutation {
  addProjectV2ItemById(input: {
    projectId: "'$PROJECT_ID'"
    contentId: "'$ISSUE_NODE_ID'"
  }) {
    item {
      id
    }
  }
}'

# Get the project item ID for this issue
ITEM_ID=$(gh api graphql -f query='
{
  node(id: "'$PROJECT_ID'") {
    ... on ProjectV2 {
      items(first: 100) {
        nodes {
          id
          content {
            ... on Issue {
              number
            }
          }
        }
      }
    }
  }
}' --jq '.data.node.items.nodes[] | select(.content.number == '$ISSUE_NUMBER') | .id')

# Set Status to Todo (get option ID dynamically)
STATUS_TODO=$(echo "$PROJECT_DATA" | jq -r '.data.repository.projectsV2.nodes[0].fields.nodes[] | select(.name == "Status") | .options[] | select(.name == "Todo") | .id')
gh api graphql -f query='
mutation {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: "'$PROJECT_ID'"
      itemId: "'$ITEM_ID'"
      fieldId: "'$STATUS_FIELD'"
      value: { singleSelectOptionId: "'$STATUS_TODO'" }
    }
  ) { projectV2Item { id } }
}'

# Set Priority based on argument (get option IDs dynamically)
PRIORITY_OPTION=$(echo "$PROJECT_DATA" | jq -r '.data.repository.projectsV2.nodes[0].fields.nodes[] | select(.name == "Priority") | .options[] | select(.name == "'$PRIORITY'") | .id')
if [ ! -z "$PRIORITY_OPTION" ]; then
  gh api graphql -f query='
  mutation {
    updateProjectV2ItemFieldValue(
      input: {
        projectId: "'$PROJECT_ID'"
        itemId: "'$ITEM_ID'"
        fieldId: "'$PRIORITY_FIELD'"
        value: { singleSelectOptionId: "'$PRIORITY_OPTION'" }
      }
    ) { projectV2Item { id } }
  }'
fi

# Set Size (XS/S/M/L/XL) based on user input
SIZE_OPTION=$(echo "$PROJECT_DATA" | jq -r '.data.repository.projectsV2.nodes[0].fields.nodes[] | select(.name == "Size") | .options[] | select(.name == "'$SIZE'") | .id')
if [ ! -z "$SIZE_OPTION" ]; then
  gh api graphql -f query='
  mutation {
    updateProjectV2ItemFieldValue(
      input: {
        projectId: "'$PROJECT_ID'"
        itemId: "'$ITEM_ID'"
        fieldId: "'$SIZE_FIELD'"
        value: { singleSelectOptionId: "'$SIZE_OPTION'" }
      }
    ) { projectV2Item { id } }
  }'
fi

# Set Complexity (1/2/3/4/5) based on user input
COMPLEXITY_OPTION=$(echo "$PROJECT_DATA" | jq -r '.data.repository.projectsV2.nodes[0].fields.nodes[] | select(.name == "Complexity") | .options[] | select(.name == "'$COMPLEXITY'") | .id')
if [ ! -z "$COMPLEXITY_OPTION" ]; then
  gh api graphql -f query='
  mutation {
    updateProjectV2ItemFieldValue(
      input: {
        projectId: "'$PROJECT_ID'"
        itemId: "'$ITEM_ID'"
        fieldId: "'$COMPLEXITY_FIELD'"
        value: { singleSelectOptionId: "'$COMPLEXITY_OPTION'" }
      }
    ) { projectV2Item { id } }
  }'
fi

# Set Component based on labels (get option IDs dynamically)

# Set Iteration based on priority
# P0 -> Current iteration, P1 -> Next iteration, P2/P3 -> Future iterations
ITERATIONS=$(echo "$PROJECT_DATA" | jq -r '.data.user.projectsV2.nodes[0].fields.nodes[] | select(.name == "Iteration") | .configuration.iterations')

# Determine iteration based on priority
if [[ "$PRIORITY" == "P0" ]]; then
  ITERATION_ID=$(echo "$ITERATIONS" | jq -r '.[0].id')
elif [[ "$PRIORITY" == "P1" ]]; then
  ITERATION_ID=$(echo "$ITERATIONS" | jq -r '.[1].id // .[0].id')
else
  ITERATION_ID=$(echo "$ITERATIONS" | jq -r '.[2].id // .[1].id // .[0].id')
fi

# Set Iteration if field exists and iteration found
if [ ! -z "$ITERATION_FIELD" ] && [ ! -z "$ITERATION_ID" ]; then
  gh api graphql -f query='
  mutation {
    updateProjectV2ItemFieldValue(
      input: {
        projectId: "'$PROJECT_ID'"
        itemId: "'$ITEM_ID'"
        fieldId: "'$ITERATION_FIELD'"
        value: { iterationId: "'$ITERATION_ID'" }
      }
    ) { projectV2Item { id } }
  }'
fi

# Set Created Date to today (if date field exists)
DATE_FIELD=$(echo "$PROJECT_DATA" | jq -r '.data.user.projectsV2.nodes[0].fields.nodes[] | select(.name == "Created") | .id')
if [ ! -z "$DATE_FIELD" ]; then
  gh api graphql -f query='
  mutation {
    updateProjectV2ItemFieldValue(
      input: {
        projectId: "'$PROJECT_ID'"
        itemId: "'$ITEM_ID'"
        fieldId: "'$DATE_FIELD'"
        value: { date: "'$(date +%Y-%m-%d)'" }
      }
    ) { projectV2Item { id } }
  }'
fi

# Verify branch was created by automation
git fetch origin
git branch -r | grep "feature/$ISSUE_NUMBER"
```

### Phase 2: Ready for Implementation

#### Step 4: Feature is Ready for Build
At this point:
- Issue is created with full specification
- Status is "Todo" in project board  
- Feature branch was auto-created by GitHub workflow
- Everything is ready for `/build-feature` command

**Next Step**: Run `/build-feature {issue-number}` which will:
1. Checkout the auto-created feature branch
2. Set Status to "In Progress" in project board
3. Execute implementation based on specification
4. Create PR when complete

#### Step 5: Handoff Notes
Document in issue comment what's ready:
```bash
# Get iteration details for the comment
ITERATION_TITLE=$(echo "$ITERATIONS" | jq -r '.[] | select(.id == "'$ITERATION_ID'") | .title')
ITERATION_START=$(echo "$ITERATIONS" | jq -r '.[] | select(.id == "'$ITERATION_ID'") | .startDate')

gh issue comment $ISSUE_NUMBER --body "✅ Feature specification complete
🌿 Branch: feature/$ISSUE_NUMBER-{feature-name}
📋 Status: Todo - Ready for implementation
🗓️ Iteration: $ITERATION_TITLE (starts $ITERATION_START)
⚡ Priority: $PRIORITY
🎯 Component: {component}
📊 Project: https://github.com/users/$GITHUB_REPOSITORY_OWNER/projects/$PROJECT_NUMBER
🚀 Next: Run /build-feature $ISSUE_NUMBER to start development"
```

### Phase 3: Full-Stack Implementation

#### Step 6: Database Layer
Use Task tool with:
- subagent_type: database-build
- description: Create database schema
- prompt: |
    Create database schema for feature: $ARGUMENTS
    Requirements from specification:
    - Tables needed: {from spec}
    - Relationships: {from spec}
    - RLS policies for multi-tenancy
    - Migration files in supabase/migrations/

#### Step 7: Backend API
Use Task tool with:
- subagent_type: backend-build
- description: Build API endpoints
- prompt: |
    Create API endpoints for feature: $ARGUMENTS
    Add to unified_backend.py:
    - Endpoints from specification
    - Validation and error handling
    - Multi-tenant data isolation
    - Response schemas

#### Step 8: Frontend Components
Use Task tool with:
- subagent_type: frontend-build
- description: Build UI components
- prompt: |
    Create React components for feature: $ARGUMENTS
    Requirements:
    - Page at route specified in spec
    - Components in /components/features/
    - State management with Zustand
    - Mobile responsive design
    - Loading and error states

#### Step 9: Integration & Testing
Use Task tool with:
- subagent_type: test-writer
- description: Create test suite
- prompt: |
    Write comprehensive tests for feature: $ARGUMENTS
    - Unit tests for components
    - API endpoint tests
    - Integration tests
    - E2E user flow tests

### Phase 4: Quality & Documentation

#### Step 10: Code Review & Enhancement
Use Task tool with:
- subagent_type: enhancement-agent
- description: Optimize implementation
- prompt: |
    Review and enhance feature: $ARGUMENTS
    - Performance optimization
    - Security review
    - Code quality improvements
    - Accessibility compliance

#### Step 11: Documentation
Use Task tool with:
- subagent_type: documentation-agent
- description: Create documentation
- prompt: |
    Document feature: $ARGUMENTS
    - API documentation
    - Component documentation
    - User guide
    - Update README if needed

### Phase 5: Deployment & Tracking

#### Step 12: Create Pull Request
Use mcp__github__create_pull_request with:
- Title: "feat: {feature-name} (closes #{issue_number})"
- Body: Implementation summary with checklist
- Base: main/master branch
- Head: feat/{feature-name}

#### Step 13: Update GitHub Project Status
Update the project item status to reflect implementation:
```bash
# Move to "In Review" column
gh project item-edit --project-id {project-number} --id {item-id} --field-id {status-field} --single-select-option-id "In Review"

# After PR merge, move to "Done"
gh project item-edit --project-id {project-number} --id {item-id} --field-id {status-field} --single-select-option-id "Done"
```

#### Step 14: Deploy & Monitor
Use Task tool with:
- subagent_type: deploy-manager
- description: Deploy feature
- prompt: |
    Deploy feature: $ARGUMENTS
    - Run CI/CD pipeline
    - Deploy to staging
    - Verify functionality
    - Monitor for issues

### Success Metrics Tracking

After deployment, track:
- User adoption rate
- Performance metrics
- Error rates
- Business impact

Update GitHub Project with metrics:
```bash
# Add metrics as comments or custom fields
gh issue comment {issue-number} --body "Deployment metrics: ..."
```

### Error Handling

If any step fails:
1. Document the error in GitHub issue comments using mcp__github__add_issue_comment
2. Update project status to "Blocked" if needed
3. Create recovery tasks in TodoWrite
4. Notify user of blockers

### Output Format

Provide user with:
```
✅ Feature Created: {feature-name}
📋 Specification: docs/features/FEAT-{timestamp}-{feature-name}.md
🎫 GitHub Issue: #{issue_number}
📊 GitHub Project: {project-name} (#{project-number})
🌿 Branch: feat/{feature-name}
🔗 PR: #{pr_number}

Next steps:
- Review PR at {pr_url}
- Monitor in GitHub Project at https://github.com/users/{owner}/projects/{project-number}
- Check deployment status
```