---
allowed-tools: Task(*), mcp__github(*), Bash(*), Read(*), Write(*), Edit(*), MultiEdit(*), TodoWrite(*), Glob(*), Grep(*)
description: Refactor existing code to improve quality, maintainability, and performance based on the Multi-Agent Development Framework
argument-hint: [issue-number-or-target] [refactor-type]
---

# Refactor

## Context
- Current branch: !`git branch --show-current`
- Project structure: @docs/Multi-Agent-Development-Framework.md
- Refactor template: @templates/local_dev/refactor-template.md
- Git status: !`git status --short`

## Your Task

When user runs `/refactor $ARGUMENTS`, coordinate intelligent code refactoring using specialized agents.

### Step 1: Find or Identify Refactor Target

```javascript
// Check if $ARGUMENTS contains an issue number
if ($ARGUMENTS.match(/#(\d+)/)) {
  const issueNumber = $ARGUMENTS.match(/#(\d+)/)[1];
  
  // Get the issue and verify it has refactor label
  targetIssue = mcp__github__get_issue({
    owner: "vanman2024",
    repo: !`basename $(pwd)`,
    issue_number: issueNumber
  });
  
  // Ensure refactor label is present
  if (!targetIssue.labels.some(label => label.name.includes("refactor"))) {
    mcp__github__update_issue({
      owner: "vanman2024",
      repo: !`basename $(pwd)`,
      issue_number: issueNumber,
      labels: [...targetIssue.labels.map(l => l.name), "type:refactor", "technical-debt"]
    });
  }
} else {
  // Find refactor issues or analyze code for refactoring opportunities
  const refactorIssues = mcp__github__list_issues({
    owner: "vanman2024",
    repo: !`basename $(pwd)`,
    labels: ["refactor"],
    state: "open"
  });
  
  if (refactorIssues.length > 0) {
    targetIssue = refactorIssues[0];
  } else {
    // No refactor issues - analyze code for opportunities
    console.log("No refactor issues found. Analyzing codebase for refactoring opportunities...");
  }
}
```

### Step 2: Analyze Refactor Requirements

Parse the issue using the refactor template structure from @templates/local_dev/refactor-template.md:
- Extract current problems (duplication, performance, maintainability)
- Identify affected files and components
- Assess risk level and breaking changes
- Determine testing strategy

### Step 3: Create Refactor Plan with TodoWrite

```javascript
TodoWrite({
  todos: [
    {
      content: "Analyze current code structure",
      activeForm: "Analyzing current code structure",
      status: "pending"
    },
    {
      content: "Identify refactoring patterns",
      activeForm: "Identifying refactoring patterns",
      status: "pending"
    },
    {
      content: "Create backup branch",
      activeForm: "Creating backup branch",
      status: "pending"
    },
    {
      content: "Implement refactoring",
      activeForm: "Implementing refactoring",
      status: "pending"
    },
    {
      content: "Update tests",
      activeForm: "Updating tests",
      status: "pending"
    },
    {
      content: "Validate no breaking changes",
      activeForm: "Validating no breaking changes",
      status: "pending"
    }
  ]
});
```

### Step 4: Route to Refactor Specialist Agent

Based on the Multi-Agent Development Framework, use the appropriate refactor approach:

#### For General Refactoring
Use Task tool with:
- subagent_type: refactor
- description: Analyze and refactor code
- prompt: `Refactor the code in ${target} following these principles:
  
  ## Refactor Goals (from issue #${targetIssue.number})
  ${extracted_refactor_goals}
  
  ## Current Problems to Address
  - Code duplication
  - Poor performance patterns
  - Complex nested logic
  - Missing abstractions
  - Technical debt
  
  ## Refactoring Patterns to Apply
  - Extract Method for duplicated code
  - Replace Conditionals with Polymorphism
  - Introduce Parameter Object for method signatures
  - Extract Class for cohesive functionality
  - Replace Magic Numbers with Named Constants
  
  ## Requirements
  1. Maintain all existing functionality (no breaking changes)
  2. Improve code readability and maintainability
  3. Add JSDoc/docstrings for all public methods
  4. Ensure all tests still pass
  5. Follow project coding standards
  
  ## Files to Refactor
  ${affected_files_list}
  
  Read and analyze: @${target}`

#### For Performance-Focused Refactoring
Use Task tool with:
- subagent_type: refactor
- description: Performance optimization refactor
- prompt: `Optimize performance in ${target}:
  
  ## Performance Issues to Address
  - N+1 queries
  - Synchronous operations that could be async
  - Inefficient algorithms (O(n²) → O(n log n))
  - Memory leaks
  - Unnecessary re-renders (React)
  
  ## Optimization Strategies
  - Implement caching where appropriate
  - Use batch operations for database queries
  - Add pagination for large datasets
  - Implement lazy loading
  - Use memoization for expensive computations
  
  Target files: @${target}`

#### For Architecture Refactoring
Use Task tool with:
- subagent_type: refactor
- description: Architectural refactor
- prompt: `Refactor architecture in ${target}:
  
  ## Architectural Improvements
  - Separate concerns (business logic from presentation)
  - Implement proper layering (controller → service → repository)
  - Extract interfaces for dependency injection
  - Apply SOLID principles
  - Implement design patterns (Factory, Strategy, Observer)
  
  ## Module Structure
  - Create clear module boundaries
  - Reduce coupling between components
  - Increase cohesion within modules
  - Extract shared utilities
  
  Analyze and refactor: @${target}`

### Step 5: Validate Refactoring

After refactoring is complete, run validation:

```javascript
// Run tests to ensure no breaking changes
Use Task tool with:
- subagent_type: backend-tester
- description: Validate refactoring
- prompt: `Run all tests and validate:
  1. All existing tests pass
  2. No functionality broken
  3. Performance not degraded
  4. Code coverage maintained or improved
  
  Commands to run:
  - npm test
  - npm run lint
  - npm run typecheck (if TypeScript)
  
  Report any failures or regressions.`
```

### Step 6: Update GitHub Issue

```javascript
// Add detailed refactor report to issue
mcp__github__add_issue_comment({
  owner: "vanman2024",
  repo: !`basename $(pwd)`,
  issue_number: targetIssue.number,
  body: `## 🔧 Refactor Complete

### Changes Made
${refactor_summary}

### Improvements Achieved
✅ **Code Quality**
- Reduced duplication by ${duplication_reduction}%
- Improved maintainability score
- Better separation of concerns

✅ **Performance**
- ${performance_improvements}

✅ **Testing**
- All tests passing
- Coverage: ${old_coverage}% → ${new_coverage}%

### Files Refactored
${refactored_files_list}

### Metrics
- Lines of code: ${old_loc} → ${new_loc}
- Cyclomatic complexity: ${old_complexity} → ${new_complexity}
- Technical debt: ${debt_reduction} hours saved

### Risk Assessment
- Breaking changes: None
- Migration needed: No
- Rollback plan: Revert to branch ${backup_branch}

### Next Steps
- [ ] Code review
- [ ] Performance benchmarks
- [ ] Deploy to staging
- [ ] Monitor for issues`
});

// Update labels
mcp__github__update_issue({
  owner: "vanman2024",
  repo: !`basename $(pwd)`,
  issue_number: targetIssue.number,
  labels: [...targetIssue.labels.map(l => l.name), "refactor-complete", "ready-for-review"]
});
```

### Step 7: Create Pull Request

If on feature branch:
```javascript
mcp__github__create_pull_request({
  owner: "vanman2024",
  repo: !`basename $(pwd)`,
  title: `🔧 ${targetIssue.title}`,
  head: !`git branch --show-current`,
  base: "main",
  body: `## Refactor Implementation
  
  Fixes #${targetIssue.number}
  
  ### Summary
  This PR refactors code to improve maintainability, performance, and code quality.
  
  ### Changes
  ${refactor_changes_summary}
  
  ### Testing
  - [x] All existing tests pass
  - [x] No breaking changes
  - [x] Performance validated
  - [x] Code coverage maintained/improved
  
  ### Refactor Checklist
  - [x] Code duplication eliminated
  - [x] Performance optimized
  - [x] Complexity reduced
  - [x] Documentation updated
  - [x] Tests updated
  
  ### Risk Assessment
  - **Risk Level**: ${risk_level}
  - **Breaking Changes**: None
  - **Rollback Plan**: Available in branch ${backup_branch}`
});
```

## Refactor Types

### Code Quality Refactoring
- Extract methods/functions
- Reduce cyclomatic complexity
- Eliminate code duplication
- Improve naming conventions
- Add proper typing

### Performance Refactoring
- Optimize algorithms
- Implement caching
- Reduce database queries
- Optimize bundle size
- Improve render performance

### Architectural Refactoring
- Apply design patterns
- Improve module structure
- Implement dependency injection
- Separate concerns
- Extract services/utilities

### Testing Refactoring
- Extract test utilities
- Improve test organization
- Add missing test coverage
- Update test patterns
- Mock external dependencies

## Safety Measures

1. **Always create backup branch** before refactoring
2. **Run tests before and after** refactoring
3. **Use version control** to track all changes
4. **Document all changes** in PR description
5. **Gradual refactoring** for high-risk changes

## Success Criteria

- ✅ All tests passing
- ✅ No functionality broken
- ✅ Code quality metrics improved
- ✅ Performance maintained or improved
- ✅ Documentation updated
- ✅ Team can understand changes