---
allowed-tools: Task(*), mcp__github(*), Bash(*), Read(*), Write(*), Edit(*), TodoWrite(*), Glob(*), Grep(*)
description: Enhance existing code or features using specialized agents based on the Multi-Agent Development Framework
argument-hint: [component-or-file-to-enhance] [enhancement-type]
---

# Enhance

## Context
- Current branch: !`git branch --show-current`
- Project structure: @docs/Multi-Agent-Development-Framework.md
- Enhancement template: @templates/local_dev/enhancement-template.md
- Git status: !`git status --short`

## Your Task

When user runs `/enhance $ARGUMENTS`, coordinate intelligent enhancement of existing code or features.

### Step 1: Find Enhancement Issues
Check for existing issues with enhancement label:

```javascript
// Find issues with enhancement label
const enhancementIssues = mcp__github__list_issues({
  owner: "vanman2024",
  repo: !`basename $(pwd)`,
  labels: ["enhancement"],
  state: "open"
});

// If $ARGUMENTS contains an issue number, use that specific issue
// Otherwise, find the most relevant enhancement issue or first available
let targetIssue;
if ($ARGUMENTS.match(/#(\d+)/)) {
  const issueNumber = $ARGUMENTS.match(/#(\d+)/)[1];
  targetIssue = mcp__github__get_issue({
    owner: "vanman2024",
    repo: !`basename $(pwd)`,
    issue_number: issueNumber
  });
  
  // Verify it has enhancement label
  if (!targetIssue.labels.some(label => label.name === "enhancement")) {
    // Add enhancement label if missing
    mcp__github__update_issue({
      owner: "vanman2024",
      repo: !`basename $(pwd)`,
      issue_number: issueNumber,
      labels: [...targetIssue.labels.map(l => l.name), "enhancement"]
    });
  }
} else if (enhancementIssues.length > 0) {
  // Use first available enhancement issue or find most relevant based on $ARGUMENTS
  targetIssue = enhancementIssues[0];
} else {
  // No enhancement issues found
  console.log("No enhancement issues found. Please create an issue with 'enhancement' label first.");
  return;
}
```

### Step 2: Analyze Enhancement Requirements
Parse the issue to understand what needs to be enhanced:
- Read issue body using the enhancement template structure from @templates/local_dev/enhancement-template.md
- Extract target component/file from issue description
- Identify enhancement type and acceptance criteria
- Determine component type for agent routing

### Step 3: Route to Appropriate Enhancement Agent

Based on the detected component from the Multi-Agent Development Framework routing:

#### For Frontend Components (React/UI)
Use Task tool with:
- subagent_type: refactor
- description: Enhance frontend component
- prompt: `Analyze and enhance ${target}. Focus on:
  - Component optimization and performance
  - Accessibility improvements (WCAG 2.1 AA)
  - Design system compliance
  - React best practices and hooks optimization
  - Code splitting opportunities
  File to enhance: @${target}`

#### For Backend Components (API/Services)
Use Task tool with:
- subagent_type: refactor  
- description: Enhance backend service
- prompt: `Analyze and enhance ${target}. Focus on:
  - API performance and caching strategies
  - Security hardening
  - Error handling improvements
  - Database query optimization
  - Rate limiting and validation
  File to enhance: @${target}`

#### For Database Components
Use Task tool with:
- subagent_type: refactor
- description: Enhance database layer
- prompt: `Analyze and enhance ${target}. Focus on:
  - Query performance and indexing
  - Data integrity constraints
  - Migration safety
  - Connection pooling
  - Backup strategies
  File to enhance: @${target}`

#### For DevOps/CI-CD Components
Use Task tool with:
- subagent_type: refactor
- description: Enhance DevOps configuration
- prompt: `Analyze and enhance ${target}. Focus on:
  - Pipeline optimization
  - Security scanning integration
  - Deployment rollback mechanisms
  - Environment configuration
  - Monitoring and alerting
  File to enhance: @${target}`

#### For Test Suites
Use Task tool with:
- subagent_type: backend-tester
- description: Enhance test coverage
- prompt: `Analyze and enhance ${target}. Focus on:
  - Increase test coverage to 80%+
  - Add edge case testing
  - Improve test performance
  - Add integration tests
  - Mock external dependencies properly
  File to enhance: @${target}`

### Step 4: Code Quality Analysis
After agent completes enhancement, use Task tool with:
- subagent_type: general-purpose
- description: Validate enhancement quality
- prompt: `Review the enhanced code for:
  1. No breaking changes introduced
  2. All tests still pass
  3. Documentation is updated
  4. Follows project coding standards
  5. Performance metrics improved
  Run: npm test && npm run lint`

### Step 5: Update GitHub Issue Progress
Update the existing enhancement issue with progress:
```javascript
// Add comment with enhancement results
mcp__github__add_issue_comment({
  owner: "vanman2024",
  repo: !`basename $(pwd)`,
  issue_number: targetIssue.number,
  body: `## ✅ Enhancement Complete

### Changes Made
${summary_of_changes}

### Improvements
- Performance: ${performance_metrics}
- Code Quality: ${quality_improvements}
- Test Coverage: ${coverage_change}
- Security: ${security_improvements}

### Files Modified
${modified_files_list}

### Next Steps
- Review changes in PR (if created)
- Run full test suite
- Deploy to staging for validation`
});

// Update issue labels to show completion
mcp__github__update_issue({
  owner: "vanman2024",
  repo: !`basename $(pwd)`,
  issue_number: targetIssue.number,
  labels: [...targetIssue.labels.map(l => l.name), "ready-for-review"],
  state: "open"  // Keep open until PR is merged
})
```

### Step 6: Create Pull Request if on Feature Branch
If not on main branch:
```javascript
mcp__github__create_pull_request({
  owner: "vanman2024",
  repo: !`basename $(pwd)`,
  title: targetIssue.title,
  head: !`git branch --show-current`,
  base: "main",
  body: `## Enhancement Implementation
  
  Fixes #${targetIssue.number}
  
  ### Enhancement Details
  From issue #${targetIssue.number}: ${targetIssue.title}
  
  ### Changes Made
  ${summary_of_changes}
  
  ### Testing
  - [ ] All tests pass
  - [ ] No breaking changes
  - [ ] Performance improved
  - [ ] Coverage increased
  
  ### Acceptance Criteria (from issue)
  ${extracted_acceptance_criteria}
  
  ### Checklist
  - [ ] Code quality verified
  - [ ] Documentation updated
  - [ ] Follows project standards
  - [ ] Ready for review`
})
```

## Enhancement Types Reference

### Performance Enhancement
- Algorithm optimization
- Caching implementation
- Database query optimization
- Bundle size reduction
- Lazy loading implementation

### Security Enhancement
- Input validation strengthening
- Authentication hardening
- SQL injection prevention
- XSS protection
- Rate limiting implementation

### UX Enhancement
- Accessibility improvements
- Loading state optimization
- Error message clarity
- Responsive design fixes
- Animation smoothing

### Code Quality Enhancement
- Refactoring for maintainability
- Design pattern implementation
- Technical debt reduction
- Test coverage improvement
- Documentation updates

## Component Detection Logic

Determine component type from file path/extension:
- `*.tsx, *.jsx, components/` → Frontend
- `*.py, api/, services/` → Backend
- `*.sql, migrations/, schemas/` → Database
- `.github/, *.yml, Dockerfile` → DevOps
- `*.test.*, *.spec.*` → Testing
- `*.md, docs/` → Documentation

## Error Handling

If enhancement fails:
1. Document failure reason in GitHub issue
2. Suggest manual intervention steps
3. Rollback any partial changes
4. Notify user with clear error message

## Success Metrics

Track and report:
- Lines of code improved
- Test coverage change
- Performance metrics (if applicable)
- Security issues resolved
- Accessibility score improvement