# Template Separation: Planning vs Implementation

## Summary of Changes

Updated GitHub issue and PR templates to properly separate planning concerns (issues) from implementation concerns (pull requests).

## Key Principle: Issues = WHAT, PRs = HOW

### Issues Should Define:
- **WHAT** needs to be done
- **WHY** it's needed (business value)
- **WHO** will use it (target users)
- **ACCEPTANCE CRITERIA** (definition of done)
- **REQUIREMENTS** and constraints
- **SCOPE** and areas affected

### Pull Requests Should Define:
- **HOW** it was implemented
- **WHAT PHASES** were completed
- **HOW IT WAS TESTED**
- **WHAT CHANGED** technically

## Changes Made

### 1. Feature Template (`feature-template.md`)

**REMOVED (moved to PR template):**
- ❌ "Implementation Phases" section with day-by-day development steps
- ❌ Detailed testing implementation steps
- ❌ Specific deployment steps and rollback procedures
- ❌ "How to Use This Template" with development commands

**REFINED (kept planning-focused):**
- ✅ Testing Requirements → High-level testing needs
- ✅ Deployment Considerations → Planning considerations only
- ✅ Dependencies & Risks → Combined into planning section
- ✅ Added "Planning Guidelines" → Clear separation explanation

### 2. Enhancement Template (`enhancement-template.md`)

**REFINED:**
- ✅ "Technical Approach" → "Technical Scope" (what areas affected)
- ✅ "Changes Required" → "Areas Affected" (scope, not implementation)
- ✅ "Testing Strategy" → "Testing Requirements" (needs, not implementation)
- ✅ "Rollback Plan" → "Risk Assessment" (planning consideration)

### 3. Refactor Template (`refactor-template.md`)

**REFINED:**
- ✅ "Testing Strategy" → "Testing Requirements" (requirements, not steps)
- ✅ "Success Metrics" → "Success Criteria" (what success looks like)
- ✅ Removed specific rollback implementation steps

### 4. PR Template (`.github/pull_request_template.md`)

**ADDED (from issue templates):**
- ✅ "Implementation Phases Completed" checklist
- ✅ Detailed testing sections (Unit, Integration, Manual)
- ✅ "Breaking Changes & Migration" with specific steps
- ✅ Database, API, and Configuration change tracking

## Benefits of This Separation

### For Issues:
- **Clearer planning** - Focus on requirements and acceptance criteria
- **Better agent routing** - Complexity/size estimation more accurate
- **Reduced scope creep** - Implementation details don't leak into planning
- **Better stakeholder communication** - Business value is clear

### For Pull Requests:
- **Implementation accountability** - Clear what was actually built
- **Better code review** - Reviewers know what to expect
- **Deployment confidence** - Migration and testing steps documented
- **Rollback readiness** - Clear understanding of changes made

### For AI Agents:
- **GitHub Copilot** gets clear, simple tasks from well-scoped issues
- **Claude Code** gets implementation freedom while meeting acceptance criteria
- **Routing accuracy** improved by separating planning complexity from implementation complexity

## Usage Guidelines

### When Creating Issues:
1. Focus on the **problem** and **desired outcome**
2. Define **acceptance criteria** clearly
3. Avoid specifying **implementation details**
4. Use templates to ensure all planning aspects are covered

### When Creating PRs:
1. Reference the issue being solved
2. Document **how** the solution was implemented
3. Check off completed implementation phases
4. Provide detailed testing evidence
5. Clearly document any breaking changes

## Template Decision Matrix

| Need | Use Template | Focus |
|------|-------------|-------|
| New functionality | `feature-template.md` | Requirements & scope |
| Improve existing | `enhancement-template.md` | Current vs desired state |
| Code quality | `refactor-template.md` | Problems & benefits |
| Simple task | `task-template.md` | Clear deliverable |
| Something broken | `bug-template.md` | Reproduction & impact |
| Any implementation | PR template | How it was built |

## Examples

### ❌ Bad Issue (implementation details):
```markdown
## Feature: User Authentication
- [ ] Install bcrypt library
- [ ] Create users table with these columns...
- [ ] Write API endpoint at /api/auth/login
- [ ] Add React form component
```

### ✅ Good Issue (planning focused):
```markdown
## Feature: User Authentication
**User Story:** As a user, I want to create an account and log in securely
**Acceptance Criteria:**
- [ ] Users can register with email/password
- [ ] Users can log in with credentials
- [ ] Passwords are securely hashed
- [ ] Session management works across page refreshes
```

### ✅ Good PR (implementation details):
```markdown
## Implementation: User Authentication
**Closes:** #123

**Implementation Phases Completed:**
- [x] Database schema (users table with email, password_hash)
- [x] API endpoints (/register, /login, /logout)
- [x] React components (LoginForm, RegisterForm)
- [x] Session management with JWT tokens

**Testing Completed:**
- [x] Unit tests for auth API endpoints
- [x] Integration tests for login/logout flow
- [x] Manual testing across browsers
```

This separation ensures that issues remain focused on planning and requirements, while PRs document the actual implementation and provide accountability for what was built.