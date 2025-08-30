# Issue vs PR Checkbox Strategy

## Core Principle: Different Stages, Different Checks

### Issue Checkboxes = "WHAT to build"
**Purpose**: Planning and implementation tracking
**When checked**: During development
**Who checks**: Developer implementing the feature

### PR Checkboxes = "QUALITY gates"
**Purpose**: Ensure code is production-ready
**When checked**: During review
**Who checks**: Developer AND reviewer

## Issue Checkboxes (Implementation Tasks)

### For Features
```markdown
## Planning
- [ ] Requirements clear and documented
- [ ] Design approach decided
- [ ] Breaking changes identified

## Implementation
- [ ] Core functionality implemented
- [ ] Edge cases handled
- [ ] Error handling added
- [ ] Input validation added

## Testing Strategy
- [ ] Unit tests planned
- [ ] Integration tests planned
- [ ] Manual test cases defined
```

### For Bugs
```markdown
## Investigation
- [ ] Root cause identified
- [ ] Reproduction steps documented
- [ ] Impact assessed

## Fix
- [ ] Bug fixed
- [ ] Regression test added
- [ ] Related code reviewed for similar issues
```

### For Refactoring
```markdown
## Planning
- [ ] Current behavior documented
- [ ] Target architecture defined
- [ ] Migration path planned

## Implementation
- [ ] Code refactored
- [ ] Backwards compatibility maintained (or breaking changes documented)
- [ ] Performance impact measured
```

## PR Checkboxes (Quality Gates)

### ALWAYS Required (Cannot Merge Without)
```markdown
## Required Checks ✅
- [ ] All tests pass (automated by CI)
- [ ] Lint passes (automated by CI)
- [ ] Type checking passes (automated by CI)
- [ ] Linked issue checkboxes complete
- [ ] Code works locally (manual verification)
- [ ] No console.logs or debug code
```

### Feature-Specific Additions
```markdown
## Feature Validation
- [ ] Feature works as specified in issue
- [ ] UI/UX matches design (if applicable)
- [ ] Documentation updated
- [ ] Migration guide written (if breaking changes)
```

### Bug Fix Additions
```markdown
## Bug Fix Validation
- [ ] Original bug no longer reproduces
- [ ] Regression test prevents future occurrence
- [ ] No new bugs introduced
```

## The Workflow

### 1. Issue Created
```markdown
## Implementation Tasks
- [ ] Design the feature       ← Developer works on these
- [ ] Write the code
- [ ] Add tests
- [ ] Update docs
```

### 2. PR Created (Linked to Issue)
```markdown
## Required Checks
- [ ] Tests pass              ← CI verifies these
- [ ] Lint passes
- [ ] Types correct
- [ ] Code works locally      ← Developer verifies
- [ ] Issue tasks complete    ← Links back to issue
```

### 3. Review Process
- Reviewer checks PR checkboxes
- CI automatically validates some
- Manual testing for "works locally"
- Cannot merge until ALL checked

## Preventing "Checked but Broken"

### Automated Safeguards
1. **CI must pass** - Tests run automatically
2. **Branch protection** - Can't bypass checks
3. **Required reviews** - Someone else must verify

### Manual Safeguards
1. **"Code works locally"** - Developer must actually run it
2. **"Feature works as specified"** - Must match requirements
3. **Reviewer testing** - Second person verifies

### The Key Separation

**Issue Checkboxes:**
- "I built the login form" ✅
- "I added password validation" ✅
- "I created the database table" ✅

**PR Checkboxes:**
- "Login actually works when tested" ✅
- "Passwords are properly hashed" ✅
- "Database migrations run cleanly" ✅

## Standard Templates

### Feature Issue Template
```markdown
## 📋 Implementation Tasks

### Planning
- [ ] Requirements reviewed and understood
- [ ] Technical approach documented
- [ ] Dependencies identified

### Core Implementation
- [ ] Main functionality implemented
- [ ] Edge cases handled
- [ ] Error states managed
- [ ] Loading states added (if UI)

### Quality
- [ ] Unit tests written
- [ ] Integration tests written
- [ ] Documentation updated
- [ ] Code commented where needed

### Final Checks
- [ ] Self-review completed
- [ ] Works in development environment
- [ ] No TODOs or debug code left
```

### PR Template
```markdown
## 🔍 Quality Checklist

### Automated Checks (CI)
- [ ] All tests pass
- [ ] Lint passes
- [ ] Type checking passes
- [ ] Build succeeds

### Manual Verification
- [ ] Code runs locally without errors
- [ ] Feature/fix works as described in issue #XX
- [ ] No console.logs or debug statements
- [ ] No commented-out code

### Documentation
- [ ] Code is self-documenting or commented
- [ ] README updated (if needed)
- [ ] API docs updated (if applicable)

### Security & Performance
- [ ] No secrets or keys in code
- [ ] No obvious performance issues
- [ ] Input validation in place
```

## The Safety Net

Even with all checkboxes checked, we have:

1. **Staging environment** - Deploy there first
2. **Feature flags** - Roll out gradually
3. **Rollback plan** - Can revert quickly
4. **Monitoring** - Catch issues early
5. **Post-deploy verification** - Check production

## Key Rules

1. **Issue checkboxes** = Tasks to complete
2. **PR checkboxes** = Quality to verify
3. **Both must be 100%** = Ready to merge
4. **CI must pass** = Non-negotiable
5. **"Works locally"** = Developer must test
6. **Review required** = Second pair of eyes

This separation ensures:
- Issues track WHAT we're building
- PRs verify it ACTUALLY WORKS
- Nothing broken gets merged
- Clear accountability at each stage