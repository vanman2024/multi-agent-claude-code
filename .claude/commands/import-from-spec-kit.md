---
allowed-tools: Read(*), Glob(*), mcp__github__create_issue(*), TodoWrite(*)
description: Import and group spec-kit tasks into GitHub issues
argument-hint: [optional: max-issues-to-create]
---

# Import From Spec-Kit

## Context
- Current directory: !`pwd`
- Spec-kit files: !`ls -la .specify/ 2>/dev/null || echo "No .specify directory found"`

## Your Task

When user runs `/import-from-spec-kit $ARGUMENTS`, intelligently import spec-kit generated tasks into our GitHub issue system.

### Phase 1: Analyze Spec-Kit Structure

Check for spec-kit project:
```bash
if [ ! -d ".specify" ]; then
  echo "❌ No .specify directory found. Run 'specify init' first."
  exit 1
fi
```

Read all spec files:
1. Use Glob to find `.specify/**/*.md` files
2. Read each spec file to understand structure
3. Identify task groupings and relationships

### Phase 2: Group Related Tasks

Analyze the tasks and group them by:
- **Feature area** (auth, tasks, projects, etc.)
- **Technical layer** (database, API, frontend)
- **Dependencies** (what must come first)

Target: 10-20 high-level issues (not 52 individual tasks)

Example groupings:
```
Authentication System (tasks 1-8)
├── User model and schema
├── JWT implementation
├── Login/logout endpoints
└── Session management

Task Management (tasks 9-20)
├── Task CRUD operations
├── Task assignments
├── Task status workflow
└── Task notifications
```

### Phase 3: Create GitHub Issues

For each group, create an issue with:

```markdown
# Issue Title: [Feature Area]

## Overview
[High-level description from grouped specs]

## Spec-Kit Tasks
This issue implements the following spec-kit tasks:
- [ ] Task #1: [Title from spec]
- [ ] Task #2: [Title from spec]
...

## Technical Specifications
[Combined details from all related specs]

## Acceptance Criteria
[Combined from all tasks in group]

## Dependencies
- Depends on: #[other issue numbers]
- Blocks: #[other issue numbers]

---
*Generated from spec-kit specifications in `.specify/`*
```

Use mcp__github__create_issue with:
- Appropriate labels (feature, enhancement, etc.)
- Complexity based on task count
- Size estimate (S/M/L/XL)

### Phase 4: Create Task Mapping

After creating issues, use TodoWrite to create a mapping:
```
Issue #1 (Authentication) → spec tasks 1-8
Issue #2 (Task Management) → spec tasks 9-20
...
```

This helps track which specs map to which GitHub issues.

### Phase 5: Summary Report

Output a summary:
```
✅ Imported 52 spec-kit tasks into 12 GitHub issues

Created Issues:
- #1: Authentication System (8 tasks)
- #2: Task Management (12 tasks)
- #3: Project Organization (6 tasks)
...

Next steps:
1. Review created issues in GitHub
2. Prioritize implementation order
3. Use '/work #1' to start implementing
```

## Special Handling

### If Too Many Tasks (>100)
Ask user: "Found 152 tasks. This seems like multiple projects. Should I:
1. Import all as-is (create 30+ issues)
2. Import only core features first
3. Let you select which features to import"

### If Tasks Already Imported
Check for existing issues with "spec-kit-generated" label.
Ask: "Spec-kit tasks already imported. Options:
1. Skip already imported tasks
2. Create duplicates anyway
3. Update existing issues with new specs"

### If No Clear Groupings
If tasks don't naturally group, fall back to:
- Technical layers (model, API, UI for each feature)
- Incremental features (MVP, Enhanced, Advanced)
- Priority levels (Must Have, Should Have, Nice to Have)

## Example Execution

```
User: /import-from-spec-kit

You: 🔍 Analyzing spec-kit project structure...
     Found 52 tasks across 5 feature areas
     
     📊 Grouping related tasks:
     - Authentication: 8 tasks
     - Task Management: 12 tasks
     - Projects: 6 tasks
     - Search & Filters: 4 tasks
     - Reports: 5 tasks
     - UI Components: 10 tasks
     - Testing: 7 tasks
     
     🎯 Creating GitHub issues...
     ✅ Created issue #1: Authentication System
     ✅ Created issue #2: Task Management
     ✅ Created issue #3: Project Organization
     ...
     
     📋 Summary: Imported 52 tasks → 7 GitHub issues
     
     Ready to implement! Start with: /work #1
```

## Important Notes

- Group aggressively - better to have fewer, larger issues
- Maintain traceability - always reference spec-kit task numbers
- Preserve specifications - include spec details in issue body
- Create logical dependencies between issues
- Use appropriate labels for routing (Copilot vs Claude)
- Consider creating one "Epic" issue that references all others