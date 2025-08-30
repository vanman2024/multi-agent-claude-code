# Branching Strategy Ideas & Considerations (DRAFT - NOT IMPLEMENTED)

> ⚠️ **DRAFT DOCUMENT**: These are ideas and proposals, not finalized decisions. The current system still creates branches at issue creation time.

## Current State (AS OF NOW)
- Branches are auto-created when issues are created (via issue-to-implementation.yml)
- This happens for ALL issues, regardless of whether they'll be worked on immediately
- **PROBLEM**: This has led to 72+ unused branches
- **CONFLICT**: Copilot also creates its own branches, leading to duplicates

## NEW UNDERSTANDING: Issue vs PR Separation

### The Fundamental Concept Shift
- **ISSUE = Planning Stage** (WHAT to do)
  - Requirements gathering
  - Discussion
  - Acceptance criteria
  - NO CODE YET
  - NO BRANCH NEEDED YET

- **PR = Implementation Stage** (HOW it's done)
  - Branch created WHEN work starts
  - Code written
  - Tests added
  - Review happens
  - This is where actual development occurs

## Concerns & Questions

### 1. Branch Creation Timing (CRITICAL DECISION NEEDED)
- **Current Problem**: Branch created immediately on issue creation → 72 unused branches
- **Root Cause**: Mixing planning (issue) with implementation (PR)
- **NEW PROPOSAL**: Branch should be created ONLY when:
  - Human developer runs `/work #123` command, OR
  - Copilot is assigned and starts immediately, OR  
  - Issue moves to "In Progress" on project board
- **Key Insight**: If we're not organized enough to use branches immediately, don't create them prematurely

### 2. Branch Visibility
- **Confusion Point**: Do auto-created branches show up in GitHub even if never checked out locally?
  - Answer: YES, they exist on remote immediately after creation
  - They show in branch list even if never pulled locally
- **Implication**: Could lead to many unused branches if issues are created but not worked on

### 3. PR Creation Strategy
- **Current Gap**: When should PRs be created as drafts vs open?
- **Proposal**: 
  - Draft PR when: Starting work, not ready for review
  - Open PR when: Code complete, ready for review
  - Auto-convert draft → open when: All checkboxes checked?

## Potential Improvements

### ⭐ PREFERRED OPTION: Project Board Status-Driven Branch Creation
**Trigger branch creation when issue moves to "In Progress" on project board**

**Why this makes sense:**
- Project board is already our source of truth for workflow status
- "In Progress" clearly indicates work is starting NOW
- Avoids creating branches for backlog items that may never be worked on
- Natural workflow: Pick up issue → Move to In Progress → Branch auto-creates

**Implementation approach:**
```yaml
# Trigger on project_card or project_v2_item events
on:
  project_card:
    types: [moved]
  issues:
    types: [assigned]  # Backup trigger

# Check if moved to "In Progress" status
# Then create branch only at that point
```

**Workflow benefits:**
- Todo → (no branch yet, just planning)
- In Progress → (branch created, work begins)
- In Review → (PR exists)
- Done → (merged and cleaned up)

### Option 1: Label-Based Branch Creation
Only create branches when issue gets specific labels:
- `ready-to-build`
- `assigned`
- `in-progress`

### Option 2: Manual Branch Creation
- Remove auto-branch creation
- Developer creates branch when actually starting work
- Use `/work` command to create branch + draft PR together

### Option 3: Smart PR State Management
- Always create as draft initially
- Auto-convert to "Ready for review" when:
  - All issue checkboxes checked
  - All PR checkboxes checked
  - CI passes

### Option 4: Branch Cleanup Automation
- Auto-delete branches for:
  - Closed issues with no PR
  - Stale branches (no commits in 30 days)
  - Merged PRs (already an option in GitHub)

## Questions to Resolve

1. **Should every issue get a branch?**
   - Pro: Consistency, always ready to work
   - Con: Branch clutter, confusion about what's active

2. **How to handle draft vs open PRs?**
   - When to create each type?
   - Should we auto-transition between states?
   - How does this interact with checkbox enforcement?

3. **Branch naming convention**
   - Current: `{type}/{issue-number}-{title}`
   - Good enough or need refinement?

4. **How to track "active" vs "dormant" branches?**
   - Use labels on issues?
   - Use project board status?
   - Regular cleanup jobs?

## Integration Points

- **Project Board**: Status field could drive branch/PR creation
  - "Todo" → No action needed
  - "In Progress" → Create branch automatically
  - "In Review" → Ensure PR exists
  - "Done" → Clean up after merge
- **Checkbox Enforcement**: Could trigger draft → ready transition
- **Agent Assignment**: Copilot/Claude could handle branch creation as part of their flow
- **Current project-automation.yml**: Already watches project board changes, could be extended

## How This Would Work

1. **Issue Created** → Goes to "Todo" on board → NO branch yet
2. **Developer/Agent picks it up** → Moves to "In Progress" → Branch auto-creates
3. **Work begins** → Developer pulls the newly created branch
4. **PR created** → Can be draft initially
5. **Ready for review** → Status changes, PR converts from draft
6. **Merged** → Branch deleted, issue closed

## Next Steps (NOT IMPLEMENTED YET)

These are ideas to consider, not decisions made:

1. Test current workflow with multiple issues to see pain points
2. Consider adding "ready-to-build" label requirement for branch creation
3. Explore GitHub's auto-merge and draft PR features more
4. Look into branch protection rules for automatic state transitions

---

*Note: This is a scratchpad document for ideas and considerations. Not official documentation or decided strategy.*