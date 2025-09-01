# Workflow Charter - SIMPLIFIED

## Core Principle: Manual First, Automate Later

Start with zero automation. Run everything manually for 1-2 sprints. Only add automation after the workflow is proven.

## The Five Building Blocks

### 1. Milestones = Timeboxes (NOT features)
- **Sprint-based**: Sprint 1 (Jan 15-29), Sprint 2 (Jan 29-Feb 12)
- **Release-based**: MVP Release (March 1), v1.0 (April 1)
- **NEVER**: "Authentication System", "User Dashboard" (these are features, not milestones)

### 2. Issues = Work Units
- One chunk of work (1-3 days max)
- Contains: Problem, acceptance criteria, definition of done
- Assigned to ONE milestone
- Example: "#101 Create login endpoint", "#102 Build signup form"

### 3. Pull Requests = Delivery
- Every PR references issue: "Fixes #101" or "Closes #101"
- When PR merges → Issue auto-closes → Milestone updates
- One PR can close multiple issues

### 4. Labels = Type Only (5 labels total)
- `feature` - New functionality
- `bug` - Something broken
- `infra` - Infrastructure/DevOps
- `architecture` - Design decisions
- `chore` - Maintenance/cleanup

**DO NOT** create labels for status, priority, or size - use Project fields for those.

### 5. Project Fields = Workflow Tracking
- **Status**: Todo → In Progress → In Review → Done
- **Priority**: High, Medium, Low
- **Size**: XS (< 1 day), S (1-2 days), M (3-5 days), L (1 week+)
- **Sprint**: Sprint 1, Sprint 2, etc.

## The Workflow (Manual Steps)

### Step 1: Plan Sprint
```
1. Create milestone: "Sprint 3 (Feb 15-29)"
2. Add 10-15 issues to milestone
3. Each issue gets ONE type label (feature/bug/infra/etc)
```

### Step 2: Start Work
```
1. Move issue to "In Progress" in Project
2. Create branch: feature/101-login-endpoint
3. Work on implementation
```

### Step 3: Create PR
```
1. Push branch
2. Create PR with "Fixes #101" in description
3. Move issue to "In Review" in Project
```

### Step 4: Merge
```
1. Get approval
2. Merge PR
3. Issue auto-closes
4. Milestone progress updates
```

## What We're REMOVING

### Disable These Workflows:
- [ ] issue-to-implementation.yml (auto branch creation)
- [ ] project-automation.yml (too many fields)
- [ ] auto-assign.yml (do it manually)
- [ ] All sync hooks

### Remove These Labels:
- All priority labels (use Project field)
- All status labels (use Project field)
- All size labels (use Project field)
- All milestone-specific labels

### Stop Doing:
- Creating branches at issue creation
- Auto-creating draft PRs
- Complex routing logic
- Multiple automations per event

## Simple Rules

1. **Every piece of work has an issue**
2. **Every issue goes in ONE milestone**
3. **Every PR references its issue(s)**
4. **Use 5 labels only (type categorization)**
5. **Track workflow in Project fields**
6. **Run manually for 2 sprints before ANY automation**

## Example Sprint

**Milestone**: Sprint 1 (Feb 15-29)

**Issues**:
- #101 Create login endpoint (`feature`)
- #102 Build signup form (`feature`)
- #103 Fix password reset (`bug`)
- #104 Set up Supabase (`infra`)
- #105 Design user schema (`architecture`)

**Project Board**:
```
Todo         | In Progress | In Review | Done
#104 (High)  | #101 (Med)  | #102 (High) | #103
#105 (High)  |             |            |
```

## Slash Commands (Phase 2 - After Manual Works)

Only after 2 successful manual sprints:
- `/create-issue` - Create issue with template
- `/work #101` - Start work (create branch, update Project)
- `/ready #101` - Move to review, create PR

But NOT YET. Manual first.

## Success Metrics

After 2 sprints, we should have:
- ✅ Clear milestone burndown
- ✅ No orphaned branches
- ✅ Every PR closes an issue
- ✅ Project board matches reality
- ✅ Team understands the flow

ONLY THEN do we add automation back.