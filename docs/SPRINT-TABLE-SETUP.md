# Sprint Table Configuration

## Sprint View Setup

The Sprint table view in the GitHub Project board should be configured as follows:

### 1. Layout
- **View Type**: Table
- **Name**: Sprints

### 2. Grouping
- **Group by**: Iteration
- This will create sections for each sprint (Iteration 1, 2, 3, etc.)

### 3. Visible Fields (in order)
1. **Title** - Issue title
2. **Status** - Todo/In Progress/Done
3. **Priority** - P0/P1/P2/P3
4. **Component** - Frontend/Backend/Database/etc.
5. **Assignees** - Who's working on it
6. **Effort** - Story points (if using)
7. **Due Date** - When it needs to be done

### 4. Sorting
- **Primary Sort**: Priority (P0 → P1 → P2 → P3)
- **Secondary Sort**: Status (In Progress → Todo → Done)

### 5. Filtering
- **Show**: Open issues only (hide closed/done)
- **Iteration**: Current and Next sprint only

## Sprint Management Process

### During Sprint Planning
1. Move items from Backlog to appropriate Sprint (Iteration)
2. Set Priority based on business value
3. Assign team members
4. Set Due Dates within sprint boundaries

### During Sprint Execution
The `/build-feature` command will:
1. Find issues in current sprint (current Iteration)
2. Prioritize by P0 → P1 → P2 → P3
3. Update Status as work progresses
4. Move to Done when complete

### Sprint Boundaries
- **Sprint 1**: Aug 22 - Sep 4, 2025
- **Sprint 2**: Sep 5 - Sep 18, 2025  
- **Sprint 3**: Sep 19 - Oct 2, 2025
- Duration: 14 days (2 weeks)
- Start Day: Friday

## Using Sprint View with Commands

### /build-feature Command
When running `/build-feature`, it should:
```bash
# Find issues in current sprint
CURRENT_DATE=$(date +%Y-%m-%d)
CURRENT_SPRINT=$(gh api graphql -f query='
{
  user(login: "vanman2024") {
    projectV2(number: PROJECT_NUMBER) {
      field(name: "Iteration") {
        ... on ProjectV2IterationField {
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
}' | jq -r '.data.user.projectV2.field.configuration.iterations[] | 
  select(.startDate <= "'$CURRENT_DATE'") | 
  .title' | tail -1)

# Get all issues in current sprint
gh api graphql -f query='
{
  user(login: "vanman2024") {
    projectV2(number: PROJECT_NUMBER) {
      items(first: 100) {
        nodes {
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
                field {
                  ... on ProjectV2IterationField {
                    name
                  }
                }
                title
              }
              ... on ProjectV2ItemFieldSingleSelectValue {
                field {
                  ... on ProjectV2SingleSelectField {
                    name
                  }
                }
                name
              }
            }
          }
        }
      }
    }
  }
}' | jq '.data.user.projectV2.items.nodes[] | 
  select(.fieldValues.nodes[] | 
    select(.field.name == "Iteration" and .title == "'$CURRENT_SPRINT'"))'
```

### Priority-Based Work Selection
The build-feature command should:
1. Get all issues in current sprint
2. Filter by Status = "Todo" or "In Progress"
3. Sort by Priority (P0 first)
4. Pick the highest priority item to work on

## Manual Sprint View Configuration

To configure the Sprint view in GitHub:

1. Go to Project #13 (or your copied project)
2. Click on "Sprints" view tab
3. Click the ⚙️ icon to configure
4. Set up:
   - **Group by**: Iteration
   - **Sort**: Priority (descending), then Status
   - **Filter**: Status is not "Done"
   - **Fields**: Show Title, Status, Priority, Component, Assignees, Due Date

5. Save the view

## Sprint Metrics to Track

In the Sprint view, you can see:
- **Sprint Velocity**: How many items completed per sprint
- **Sprint Burndown**: Items remaining vs time left
- **Priority Distribution**: Balance of P0/P1/P2/P3 items
- **Component Coverage**: Which areas are being worked on

## Integration with Build Feature

The `/build-feature` command should:
1. Check current sprint items
2. Find highest priority "Todo" item
3. Move to "In Progress"
4. Create feature branch
5. Start implementation
6. Move to "Done" when PR is merged