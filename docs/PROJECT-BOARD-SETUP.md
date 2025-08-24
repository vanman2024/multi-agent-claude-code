# GitHub Project Board Setup Guide

## Current Setup

### Active Project (Project #11)
- **Name**: Multi-Agent Claude Code Development
- **Repo**: vanman2024/multi-agent-claude-code
- **Status**: Currently connected and in use
- **Components**: 4 basic components (Frontend, Backend, Database, DevOps)
- **Purpose**: Managing the actual multi-agent Claude Code development

### Template Project (Project #13)
- **Name**: [Template Project Name]
- **Status**: Template for future projects
- **Components**: Full 20 components with descriptions
- **Purpose**: Will be copied when creating new projects

## How Projects Work

### For THIS Repository (multi-agent-claude-code)
- Uses Project #11 with hardcoded IDs in `.github/workflows/project-automation.yml`
- Workflow automatically:
  - Adds issues to project board
  - Sets priority based on labels or title ([P0], [P1], [P2], [P3])
  - Sets status (Todo → In Progress → Done)
  - Creates feature branches
  - Updates status when work begins/completes

### For NEW Projects (Future)
1. Copy Project #13 template using:
   ```bash
   gh project copy 13 --source-owner vanman2024 --target-owner vanman2024 --title "New Project Name"
   ```

2. Connect to new repository

3. Update workflow with new project IDs

## Project #11 Field IDs (Current)

```yaml
env:
  PROJECT_ID: PVT_kwHOCu1OR84BA3ip
  PROJECT_NUMBER: 11
  
  # Field IDs
  STATUS_FIELD: PVTSSF_lAHOCu1OR84BA3ipzgziw9A
  PRIORITY_FIELD: PVTSSF_lAHOCu1OR84BA3ipzgzixBc
  COMPONENT_FIELD: PVTSSF_lAHOCu1OR84BA3ipzgzixC0
  
  # Status options
  STATUS_TODO: f75ad846
  STATUS_IN_PROGRESS: 47fc9ee4
  STATUS_DONE: 98236657
  
  # Priority options
  PRIORITY_P0: 272850f8
  PRIORITY_P1: 257f709e
  PRIORITY_P2: 5041f9b5
  PRIORITY_P3: e6ae2685
  
  # Component options (only 4 in Project #11)
  COMPONENT_FRONTEND: 83954b68
  COMPONENT_BACKEND: 8aa84839
  COMPONENT_DATABASE: eea4cd61
  COMPONENT_DEVOPS: 82f4b58a
```

## Project #13 Components (Template)

The template project includes all 20 components with descriptions:

1. **Frontend** - User interface and client-side logic
2. **Backend** - Server-side application logic
3. **Database** - Data storage and management
4. **API** - External and internal API interfaces
5. **Authentication** - User identity and access control
6. **Testing** - Automated testing and quality assurance
7. **Documentation** - Technical and user documentation
8. **Security** - Security features and vulnerability management
9. **Performance** - Optimization and performance monitoring
10. **Monitoring** - System health and observability
11. **Analytics** - Data analysis and insights
12. **Payments** - Payment processing and billing
13. **Messaging** - Communication and notification systems
14. **Search** - Search functionality and indexing
15. **Storage** - File and object storage solutions
16. **CDN** - Content delivery and caching
17. **ML/AI** - Machine learning and AI features
18. **Mobile** - Mobile application development
19. **Desktop** - Desktop application development
20. **DevOps** - CI/CD and infrastructure automation

## Important Notes

- **DO NOT** confuse Project #11 (current) with Project #13 (template)
- **DO NOT** try to dynamically discover projects - use hardcoded IDs
- The workflow in this repo is specifically configured for Project #11
- When setting up a new project, you'll need to:
  1. Copy Project #13 as template
  2. Get the new project's IDs
  3. Update the workflow with those IDs

## Testing the Workflow

To test if the project automation is working:

```bash
# Create a test issue
gh issue create --title "[TEST] Priority Test [P1]" --body "Testing project automation" --label "type:feature"

# Check if it was added to project
gh api graphql -f query='
{
  repository(owner: "vanman2024", name: "multi-agent-claude-code") {
    issue(number: ISSUE_NUMBER) {
      projectsV2(first: 10) {
        nodes {
          number
          title
        }
      }
    }
  }
}'

# View workflow runs
gh run list --workflow="project-automation.yml" --limit 5
```

## Troubleshooting

If issues aren't being added to the project:
1. Check that PROJECT_TOKEN secret is set
2. Verify the workflow is enabled
3. Check workflow run logs for errors
4. Ensure issue has proper labels/format

## Future Improvements

When we implement the dynamic workflow for NEW projects:
1. The workflow will discover the project connected to the repo
2. It will find all field IDs dynamically
3. It will work with any project copied from template #13