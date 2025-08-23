# Complete Workflow Testing Checklist

## Prerequisites
- [ ] Add Start Date and End Date fields to project board (manual)
- [ ] Configure project views properly
- [ ] Ensure PROJECT_TOKEN is working
- [ ] Clean up excess test issues

---

## Test Scenario 1: Feature Request Flow (User → Claude → Agent)

### Setup
- User requests: "We need a user authentication system"
- No existing infrastructure for auth

### Test Steps
1. **User → Claude Code**
   - [ ] User describes feature need
   - [ ] Claude understands requirements
   - [ ] Claude identifies missing infrastructure

2. **Claude → GitHub Issue**
   - [ ] Claude creates properly formatted issue
   - [ ] Title includes type (e.g., "[FEATURE]")
   - [ ] Body includes:
     - [ ] Description
     - [ ] Acceptance criteria
     - [ ] Component detection text
     - [ ] Priority indicators

3. **GitHub Automation**
   - [ ] Issue automatically added to project board
   - [ ] Status set to "Todo"
   - [ ] Priority field populated (based on impact)
   - [ ] Component field populated
   - [ ] Branch created (feature/{issue-number}-{title})

4. **Claude → Task Tool (Simulating Sub-Agent)**
   - [ ] Claude uses Task tool to break down work
   - [ ] Task tool acts as sub-agent would
   - [ ] Creates implementation plan
   - [ ] Identifies dependencies

5. **Development Phase**
   - [ ] Pull branch locally
   - [ ] Implement basic structure
   - [ ] Create tests
   - [ ] Push changes

6. **PR → Testing**
   - [ ] Create PR
   - [ ] CI pipeline triggers
   - [ ] Tests run
   - [ ] Linting passes
   - [ ] Type checking passes

7. **Deployment**
   - [ ] PR approved
   - [ ] Merges to main
   - [ ] Deploy to staging triggers
   - [ ] Status updates to "Done"

---

## Test Scenario 2: Bug Report Flow (External → GitHub → Agent)

### Setup
- User submits bug via GitHub issue template
- Bug: "Login button not working on mobile"

### Test Steps
1. **External User → GitHub**
   - [ ] User creates issue using template
   - [ ] Labels added: type:bug

2. **GitHub Automation**
   - [ ] Issue added to project
   - [ ] Priority set based on impact
   - [ ] Status: Todo
   - [ ] Branch created: bug/{issue-number}-{title}

3. **Claude Sees Issue**
   - [ ] Claude checks project board
   - [ ] Identifies bug in queue
   - [ ] Analyzes issue

4. **Claude → Task Tool (Sub-Agent)**
   - [ ] Task: Investigate bug
   - [ ] Task: Fix implementation
   - [ ] Task: Add test coverage
   - [ ] Task: Verify on mobile

5. **Fix → Test → Deploy**
   - [ ] Implementation
   - [ ] Tests pass
   - [ ] PR created
   - [ ] Deployed

---

## Test Scenario 3: Claude-Initiated Feature

### Setup
- Claude identifies need during development
- Example: "Need error logging system"

### Test Steps
1. **Claude Identifies Need**
   - [ ] During work, realizes gap
   - [ ] Creates issue programmatically

2. **Issue Creation**
   - [ ] Proper format
   - [ ] Links to parent issue if applicable
   - [ ] Sets appropriate priority

3. **Handoff Decision**
   - [ ] Claude decides: self or sub-agent
   - [ ] If simple: handle directly
   - [ ] If complex: prepare for sub-agent

4. **Sub-Agent Simulation**
   - [ ] Task tool gets context
   - [ ] Works on specific task
   - [ ] Returns results to Claude

---

## Test Scenario 4: Complex Multi-Agent Flow

### Setup
- Large feature requiring multiple agents
- Example: "Add real-time chat system"

### Test Steps
1. **Break Down**
   - [ ] Frontend agent: UI components
   - [ ] Backend agent: WebSocket server
   - [ ] Database agent: Message storage
   - [ ] DevOps agent: Infrastructure

2. **Coordination**
   - [ ] Claude assigns to each "agent" (Task tool)
   - [ ] Each works independently
   - [ ] Results collected by Claude
   - [ ] Integration phase

---

## Test Scenario 5: YAML Configuration Submission

### Setup
- User provides config file
- Needs to be integrated

### Test Steps
1. **User Provides File**
   - [ ] YAML validation
   - [ ] Issue created with file reference

2. **Processing**
   - [ ] File analyzed
   - [ ] Changes identified
   - [ ] Implementation planned

---

## Validation Points

### For Each Test:
- [ ] Issue appears on project board within 30 seconds
- [ ] All fields properly populated
- [ ] Branch creation successful
- [ ] Workflow runs complete without errors
- [ ] No duplicate workflow runs
- [ ] Status transitions work
- [ ] Comments added appropriately

### Agent Handoff Validation:
- [ ] Context passed correctly
- [ ] Agent (Task tool) has enough info
- [ ] Results returned properly
- [ ] Claude can continue from results

### Pipeline Validation:
- [ ] Tests actually run
- [ ] Failures block deployment
- [ ] Success allows progression
- [ ] Staging deployment works
- [ ] Production requires approval

---

## Metrics to Track

For each scenario:
- Time from issue → project board
- Time from issue → branch
- Number of workflow runs triggered
- Success/failure rate
- Manual interventions needed

---

## Notes Section

### What's Working:
- 

### What's Broken:
- 

### What Needs Manual Steps:
- 

### Surprises/Discoveries:
- 

---

## Sign-off

- [ ] Scenario 1 Complete
- [ ] Scenario 2 Complete  
- [ ] Scenario 3 Complete
- [ ] Scenario 4 Complete
- [ ] Scenario 5 Complete

**Ready for Agent Implementation:** [ ]

---

*Last Updated: [Date]*
*Tested By: [Your Name] & Claude Code*