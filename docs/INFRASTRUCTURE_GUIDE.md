# Infrastructure Guide - How The Framework Works

## 🏗️ The House Building Metaphor
This framework uses a house building metaphor to organize development work. Just like building a house, software has a natural order - you can't put up walls without a foundation, and you can't install electrical without framing. This guide explains how our infrastructure supports this systematic approach.

---

## 📋 How The Infrastructure Components Work

### 1. PROJECT BOARD AUTOMATION ❌
**Current State**: Not working properly
**Required State**: Automatic status transitions based on development events



#### Current Issues:
- Issue #91: Project automation not updating to In Progress on PR creation
- Copilot can move items but our automation cannot
- Reopened issues stay in "Done" column

---#### Requirements:
- [ ] When PR is created → Move issue to "In Progress" column
- [ ] When PR marked ready → Move to "In Review" column
- [ ] When PR merged → Move to "Done" column
- [ ] When issue reopened → Move back to appropriate column (not stuck in Done)
- [ ] Support backwards movement (Done → In Progress for reopened issues)
- [ ] Sync with GitHub labels (status:in-progress, etc.)

### 2. LABEL AUTOMATION ❌
**Current State**: Manual or missing
**Required State**: Automatic based on context

#### Requirements:
- [ ] Auto-apply type labels based on issue title prefix ([FEATURE], [BUG], etc.)
- [ ] Auto-apply priority labels based on metadata (P0, P1, P2, P3)
- [ ] Auto-apply size labels based on metadata (XS, S, M, L, XL)
- [ ] Auto-apply complexity labels based on metadata (1-5)
- [ ] Add status labels automatically (status:in-progress when work starts)
- [ ] Add sprint labels when added to sprint
- [ ] Remove conflicting labels (can't be both bug and feature)

---

### 3. MILESTONE USAGE ✅
**Current State**: Manual creation as needed
**Required State**: Feature/goal-based grouping

#### Proper Milestone Usage:
Milestones should group related issues by feature or goal, NOT by time periods.

**Good Examples:**
- "User Authentication" - all login/signup/password issues
- "Shopping Cart" - all cart-related features  
- "MVP" - everything needed for first release
- "Bug Fixes v1.1" - all bugs to fix after v1.0
- "Payment Integration" - all payment-related issues

**NOT for:**
- Sprint tracking (use project board columns instead)
- Time-based periods (Q1, Week 1, etc.)

**Implementation:**
- Teams create milestones manually for major features/releases
- Issues are assigned to milestones based on feature grouping
- No automation needed - keep it simple and flexible

---

### 4. ISSUE RELATIONSHIPS - The House Building Order ✅
**Current State**: Use GitHub's built-in mentions and task lists
**Required State**: Follow the house metaphor for natural dependencies

#### The House Building Order (Natural Dependencies):

**1. Foundation (Database & Data Layer)** 🏗️
- Must be built FIRST - everything depends on this
- Issues: Database schemas, tables, migrations
- Example: "Create users table", "Set up auth database"

**2. Plumbing (GitHub Automation & CI/CD)** 🔧
- Carries things but doesn't think
- Issues: Workflows, deployments, pipelines
- Depends on: Foundation
- Example: "Set up deployment pipeline", "Create test workflow"

**3. Framing (Backend Services & APIs)** 🏠
- The structural support
- Issues: API endpoints, services, business logic
- Depends on: Foundation (needs database)
- Example: "Create user API endpoint", "Build auth service"

**4. Electrical (Agent System & Intelligence)** ⚡
- Powers the smart features
- Issues: AI features, decision logic, agents
- Depends on: Framing (needs APIs to power)
- Example: "Add Copilot integration", "Create smart routing"

**5. Finishes (Frontend & UI)** 🎨
- What users see and touch
- Issues: UI components, pages, styling
- Depends on: Framing & Electrical (needs APIs and features)
- Example: "Build login page", "Create dashboard UI"

#### How to Express Dependencies:

**In Issue Body:**
```markdown
**Layer**: Finishes (Frontend)
**Depends on**: #45 (User API endpoint), #23 (User table)
**Blocked by**: Need the foundation and framing first
```

**Using Task Lists:**
```markdown
### Prerequisites
- [ ] #23 User database table must be created first
- [ ] #45 User API endpoint must be working
- [ ] #67 Auth service must be deployed
```

**Simple Mentions:**
- "Blocked by #123"
- "Depends on #456"
- "Must complete #789 first"

#### Why This Works:
- **Natural order** - You can't build walls without foundation
- **Clear dependencies** - Everyone understands house building
- **No complex automation** - GitHub already tracks mentions
- **Flexible** - Use whatever notation makes sense

#### What NOT to Do:
- Don't build UI before APIs exist
- Don't create APIs before database tables
- Don't add AI features before basic functionality
- Don't overthink it - follow the house order

---

### 5. AGENT ASSIGNMENT AUTOMATION ⚠️
**Current State**: Partially working
**Required State**: Intelligent routing based on complexity

#### Requirements:
- [ ] Auto-assign Copilot for: Complexity ≤2 AND Size ≤S
- [ ] Auto-assign Claude Code for: Complexity >2 OR Size >S
- [ ] Track agent assignments in issue
- [ ] Handle handoffs between agents
- [ ] Add agent labels (assigned:copilot, assigned:claude)
- [ ] Notify in comments when assigned
- [ ] Support manual override with reason

#### Current Issues:
- Issue #105: Confusion about agent assignments
- Copilot assignments work but aren't tracked properly

---

### 6. SLASH COMMAND COMPLETENESS ⚠️
**Current State**: Partially implemented
**Required State**: Full workflow automation

#### `/create-issue` Requirements:
- [x] Check for duplicates first
- [x] Create issue with template
- [ ] Auto-assign milestone
- [ ] Auto-assign agent based on complexity
- [ ] Add to project board
- [ ] Apply all relevant labels
- [ ] Set priority based on metadata

#### `/work` Requirements:
- [x] Verify on main branch
- [x] Pull latest changes
- [x] Create feature branch
- [ ] Push branch to GitHub
- [ ] Create draft PR with "Closes #XXX"
- [ ] Update issue status to in-progress
- [ ] Add PR link to issue comments
- [ ] Update project board

---

### 7. PR-ISSUE LINKING ⚠️
**Current State**: Mostly working
**Required State**: Bulletproof linking

#### Requirements:
- [x] Enforce "Closes #XXX" in PR body
- [x] Block merge without linked issue
- [ ] Handle multiple issues in one PR
- [ ] Support "Continues #XXX" for partial work
- [ ] Fix typos automatically (e.g., #107 → #108)
- [ ] Validate issue exists and is open
- [ ] Add bi-directional links in comments

---

### 8. TESTING INTEGRATION ❌
**Current State**: Confusing/incomplete
**Required State**: Clear testing requirements

#### Requirements:
- [ ] Define required local tests before PR ready
- [ ] Add test checklist to PR template
- [ ] Verify tests run locally (not just CI)
- [ ] Block PR ready without test confirmation
- [ ] Clear distinction: local tests vs CI tests
- [ ] Add test coverage requirements
- [ ] Enforce linting before commit

#### Current Issues:
- Issue #105: Local testing vs GitHub Actions confusion
- No clear testing requirements in PRs

---

### 9. SPRINT MANAGEMENT ❌
**Current State**: Manual
**Required State**: Automated sprint workflow

#### Requirements:
- [ ] Auto-create new sprints every 2 weeks
- [ ] Move incomplete items to next sprint
- [ ] Calculate velocity automatically
- [ ] Assign issues to sprint based on capacity
- [ ] Generate sprint summary reports
- [ ] Track burndown automatically
- [ ] Alert on sprint risks

---

### 10. DEPLOYMENT AUTOMATION ✅
**Current State**: Working
**Required State**: Already functional

#### Working Features:
- [x] Vercel preview on PR
- [x] Production deploy on merge
- [x] Deploy comments with URLs
- [x] Rollback capability

---

### 11. WORKFLOW VALIDATION ⚠️
**Current State**: Incomplete (Issue #108)
**Required State**: Fully validated

#### Remaining Validations:
- [ ] Phase 2: Issue creation flow (labels, board, no auto-branch)
- [ ] Phase 3: Local development workflow
- [ ] Phase 4: Implementation & testing
- [ ] Phase 6: PR management
- [ ] Phase 8: Rollback testing
- [ ] Local vs GitHub synchronization
- [ ] Multi-agent scenarios
- [ ] Documentation updates

---

### 12. GITHUB ACTIONS FIXES ❌
**Current State**: Multiple broken workflows
**Required State**: All workflows functional

#### Broken Workflows:
- [ ] auto-assign.yml - Not assigning correctly
- [ ] issue-to-implementation.yml - Not creating PRs properly
- [ ] pr-automation.yml - Not updating project board
- [ ] label-sync.yml - Not syncing labels
- [ ] claude-code-review.yml - Not triggering

#### Required Fixes:
- [ ] Audit all workflow permissions
- [ ] Fix GitHub token scopes
- [ ] Update deprecated actions
- [ ] Add error handling
- [ ] Add workflow debugging

---

### 13. BRANCH PROTECTION ✅
**Current State**: Working
**Required State**: Already functional

#### Working Features:
- [x] Require PR for main branch
- [x] Require issue checkboxes complete
- [x] Require CI checks to pass
- [x] Auto-delete head branches

---

### 14. NOTIFICATION SYSTEM ❌
**Current State**: Not implemented
**Required State**: Smart notifications

#### Requirements:
- [ ] Notify on issue assignment
- [ ] Alert on blocked dependencies resolved
- [ ] Sprint start/end notifications
- [ ] PR review requests
- [ ] Failed deployment alerts
- [ ] Stale issue warnings

---

### 15. METRICS & REPORTING ❌
**Current State**: Not implemented
**Required State**: Automated insights

#### Requirements:
- [ ] Cycle time tracking
- [ ] Lead time measurement
- [ ] Velocity calculations
- [ ] Bug escape rate
- [ ] Code review turnaround
- [ ] Deployment frequency
- [ ] Weekly/monthly reports

---

## 🚀 Implementation Priority

### Phase 1: Critical Fixes (Do First)
1. Fix project board automation (#91)
2. Complete `/work` command implementation
3. Fix PR-issue linking edge cases
4. Implement label automation

### Phase 2: Core Features (Do Second)
5. Implement issue relationships
6. Fix agent assignment routing
7. Add milestone automation
8. Implement sprint management

### Phase 3: Enhancement (Do Third)
9. Add testing integration
10. Implement metrics & reporting
11. Add notification system
12. Complete workflow validation (#108)

---

## 📊 Success Metrics

### Must Have (Before v1.0):
- ✅ All Phase 1 items complete
- ✅ 90% of Phase 2 items complete
- ✅ All workflows tested end-to-end
- ✅ Documentation reflects reality

### Should Have:
- ✅ 50% of Phase 3 items complete
- ✅ Metrics dashboard available
- ✅ Sprint automation working

### Could Have:
- ✅ Advanced reporting
- ✅ AI-powered insights
- ✅ Custom workflow builder

---

## 🔗 Issues Being Consolidated

### Will Be Closed/Consolidated:
- **#91**: Update project automation → Section 1: Project Board Automation
- **#105**: Local testing vs GitHub Actions → Section 8: Testing Integration
- **#108**: Complete workflow validation → Section 11: Workflow Validation
- **#110**: User Dashboard feature → Keep separate (actual feature, not infrastructure)
- **#113**: Fix checkbox validation → Section 7: PR-Issue Linking (COMPLETED)
- **#114**: Clean up documentation → COMPLETED
- **#116**: Simplify templates → COMPLETED
- **#118**: Add duplicate check → COMPLETED
- **#53**: PR Checkbox auto-sync → Section 6: Slash Commands
- **#104**: Gemini Integration Test → Keep separate (specific integration test)

### Issues to Keep Open:
- **#110**: User Dashboard (actual feature work)
- **#104**: Gemini Integration Test (specific test case)

---

## 📝 Implementation Strategy

### Using GitHub Task Lists
1. Create one mega-issue with all checkboxes
2. Use GitHub's "Convert to issue" feature for major sections
3. This creates sub-issues that track back to the parent
4. Progress automatically updates in the parent issue

### Workflow:
1. Work through items systematically
2. Check off completed items in the mega-issue
3. Create sub-issues only for complex multi-day tasks
4. Close consolidated issues with reference to mega-issue

**Next Step**: Create single mega-issue #120 and close issues #91, #105, #108, #53 with reference.
