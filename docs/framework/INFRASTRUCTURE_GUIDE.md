# Infrastructure Guide - How The Framework Works

## 🏗️ The House Building Metaphor
This framework uses a house building metaphor to organize development work. Just like building a house, software has a natural order - you can't put up walls without a foundation, and you can't install electrical without framing. This guide explains how our infrastructure supports this systematic approach.

---

## 📋 How The Infrastructure Components Work

### 1. PROJECT BOARD AUTOMATION ✅
**Current State**: Working - Automatic status transitions based on PR lifecycle
**Purpose**: Track work progress visually without manual board updates

#### How It Works:
- ✅ **Issue created** → Added to "Todo" column automatically
- ✅ **PR created** → Linked issue moves to "In Progress" 
- ✅ **PR marked ready** → Issue moves to "In Review"
- ✅ **PR merged** → Issue moves to "Done"
- ✅ **Issue reopened** → Moves back to "Todo" (needs PR lifecycle to progress again)

#### Key Points:
- **PR must link to issue** using "Closes #123" in PR body
- Board updates happen automatically via GitHub Actions
- No manual board management needed
- Status field in project tracks current state

#### Using the Board:
1. Create issue → Appears in Todo
2. Run `/work #123` → Creates PR, moves to In Progress
3. Mark PR ready → Moves to In Review
4. Merge PR → Moves to Done

The board is a visual representation - the PR lifecycle drives everything.

### 2. LABEL AUTOMATION ✅
**Current State**: Working - Labels from templates, metadata to project fields
**Purpose**: Visual categorization and project field organization

#### How Labels Work:
- ✅ **Type labels** (bug, enhancement, task, hotfix) → Applied by issue templates
- ✅ **Urgent label** → Applied for P0 priority or hotfix template
- ✅ **Documentation label** → Applied when docs-related
- ✅ **Needs-triage label** → Applied when no priority specified

#### How Project Fields Work (NOT Labels):
- **Priority** (P0, P1, P2, P3) → Parsed from metadata, set as project field
- **Size** (XS, S, M, L, XL) → Parsed from metadata, set as project field  
- **Component** (Frontend, Backend, etc.) → Parsed from metadata, set as project field
- **Points** (1-13) → Calculated from size, set as project field

#### Key Understanding:
- **Labels** = GitHub issue labels (visible everywhere)
- **Project Fields** = Board-specific data (only visible in project view)
- Don't confuse the two - they serve different purposes

#### Metadata Format in Issues:
```markdown
**Priority**: P2
**Size**: S
**Points**: 2
**Component**: Backend
```

This gets parsed and applied to the project board automatically.

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

### 5. AGENT ASSIGNMENT AUTOMATION ✅
**Current State**: Working - Smart routing via `/create-issue` command
**Purpose**: Automatically assign work to the right agent based on complexity

#### How Agent Assignment Works:
- ✅ **Simple tasks** (Complexity ≤2 AND Size ≤S) → GitHub Copilot
- ✅ **Complex tasks** (Complexity >2 OR Size >S) → Claude Code (you)
- ✅ Assignment happens during issue creation via `/create-issue`
- ✅ Copilot gets auto-assigned via GitHub API

#### The Golden Rule:
**Copilot ONLY gets tasks that are BOTH simple AND small:**
- Complexity 1-2 (simple logic)
- Size XS or S (< 2 hours)

**Everything else goes to Claude Code:**
- Any complex logic (3-5)
- Any larger tasks (M, L, XL)
- Architecture decisions
- Multi-file changes

#### How to Use:
1. Run `/create-issue "Task description"`
2. Command analyzes complexity and size
3. Automatically assigns to appropriate agent
4. Copilot tasks get `@copilot` mention in issue
5. Claude Code tasks stay for local work

---

### 6. SLASH COMMANDS ✅
**Current State**: Working - Full workflow automation
**Purpose**: Streamline development workflow with simple commands

#### Primary Commands That Drive Everything:

**`/create-issue`** - Universal issue creation with smart routing
- ✅ Searches for duplicates first
- ✅ Creates issue with proper template
- ✅ Auto-assigns to Copilot or Claude based on complexity
- ✅ Adds to project board automatically
- ✅ Applies type labels from templates
- ✅ Sets metadata as project fields

**`/work`** - Universal implementation command
- ✅ Pulls latest changes
- ✅ Creates feature branch
- ✅ Creates draft PR with "Closes #XXX"
- ✅ Links PR to issue
- ✅ Project board updates automatically via PR lifecycle

#### Other Useful Commands:
- `/wip` - Work without issues (exploration/experiments)
- `/wip-status` - See all work in progress
- `/deploy` - Deploy to Vercel
- `/discussions` - Manage GitHub Discussions
- `/project-setup` - Initialize new project from template
- `/add-mcp` - Add MCP servers

#### The Complete Workflow:
1. `/create-issue "Build user auth"` → Issue created, routed to agent
2. `/work #123` → Branch + PR created, board moves to In Progress
3. Implement the feature locally
4. Mark PR ready → Board moves to In Review
5. Merge PR → Issue closes, board moves to Done

---

### 7. PR-ISSUE LINKING ✅
**Current State**: Working - Enforced linking with checkbox validation
**Purpose**: Ensure every PR closes an issue (traceability)

#### How It Works:
- ✅ **PR must have "Closes #XXX"** in body or it can't merge
- ✅ **Checkbox enforcement** - All issue checkboxes must be checked
- ✅ **Auto-close on merge** - Issue closes when PR merges
- ✅ **Board automation** - Issue status tracks PR lifecycle

#### The Rules:
1. Every PR must link to an issue
2. Use "Closes #123" (not "Fixes" or "Resolves" for consistency)
3. Issue checkboxes must all be checked before merge
4. One PR per issue (keeps it simple)

#### Why This Matters:
- Complete traceability from idea → issue → PR → deployment
- Project board stays in sync automatically
- No orphaned PRs or forgotten issues

---

### 8. DEPLOYMENT AUTOMATION ✅
**Current State**: Working - Vercel integration
**Purpose**: Automatic deployments without manual intervention

#### How It Works:
- ✅ **PR created/updated** → Preview deployment
- ✅ **PR merged to main** → Production deployment
- ✅ **Deploy comments** → URLs posted to PR
- ✅ **Rollback** → Via Vercel dashboard

#### Using Deployments:
1. Create PR → Get preview URL automatically
2. Test in preview environment
3. Merge → Deploys to production
4. `/deploy` command for manual deploys

Simple, automatic, no configuration needed after initial setup.

---

## 🎯 Summary: How It All Works Together

### The Complete Development Flow:

1. **Start with an idea** → `/create-issue "Build user authentication"`
   - Issue created with proper template
   - Metadata parsed to project fields
   - Complexity analyzed, agent assigned
   - Added to project board in Todo

2. **Begin implementation** → `/work #123`
   - Creates feature branch
   - Creates draft PR with "Closes #123"
   - Board moves to In Progress automatically

3. **Build following the house order**:
   - Foundation first (database/data)
   - Then plumbing (workflows/CI)
   - Then framing (APIs/backend)
   - Then electrical (intelligence/agents)
   - Finally finishes (UI/frontend)

4. **Complete the work**:
   - Check all issue checkboxes
   - Run tests and linting
   - Mark PR ready for review
   - Board moves to In Review

5. **Merge and deploy**:
   - PR merged → Issue closes
   - Board moves to Done
   - Automatic deployment to production

### Key Principles:

- **Issues drive everything** - No PR without an issue
- **Automation is plumbing** - It moves things but doesn't think
- **Agents provide intelligence** - Copilot for simple, Claude for complex
- **The board reflects reality** - PR lifecycle updates it automatically
- **Follow the house order** - Can't build walls without foundation

### What You DON'T Need to Do:

- Manually update the project board
- Manually assign labels (templates do it)
- Manually link PRs to issues (`/work` does it)
- Manually deploy (merge triggers it)
- Think about sprint management (not needed)
- Complex testing setup (keep it simple)
- Notification systems (GitHub already notifies)
- Metrics tracking (use GitHub Insights)

---

## 🎬 Real-World Usage Examples

### Example 1: Starting a New Feature
```bash
# Monday morning, need to add user authentication
git pull origin main                          # Always start fresh
/create-issue "Add user authentication"       # Creates issue, analyzes complexity
# System responds: "Created issue #45, assigned to Claude Code (Complexity: 4)"

/work #45                                      # Creates branch, draft PR
# Now implement the feature...
# After implementation:
gh pr ready                                    # Mark PR ready for review
# Board automatically moves to "In Review"
```

### Example 2: Quick Bug Fix (Copilot Handles)
```bash
/create-issue --bug "Fix login button not clickable on mobile"
# System responds: "Created issue #46, auto-assigned to Copilot (Complexity: 2, Size: S)"
# Copilot starts work automatically within seconds
# Watch the magic happen - no further action needed!
```

### Example 3: Exploring Ideas Without Issues
```bash
/wip "experiment-with-websockets"             # Creates experimental branch
# Try things out, prototype, explore...
# If it works out:
/create-issue "Implement real-time updates"   # Formalize the work
/work #47                                      # Continue properly
```

### Example 4: Managing Dependencies
```markdown
# In issue #48 body:
**Layer**: Finishes (Frontend)
**Depends on**: #45 (Auth API), #44 (User table)

# System understands: Can't build login UI without auth backend
```

---

## 🏁 Quick Start Checklist

When cloning this template for a new project:

1. **Initial Setup**
   ```bash
   gh repo clone vanman2024/multi-agent-claude-code my-new-project
   cd my-new-project
   ./scripts/utilities/load-personal-config.sh  # Load your saved API keys
   /project-setup                                # Initialize project settings
   ```

2. **Start Building**
   ```bash
   /create-issue "Set up database schema"        # Foundation first!
   /work #1                                      # Begin implementation
   ```

3. **Let Automation Handle the Rest**
   - Board updates automatically
   - Copilot picks up simple tasks
   - Deployments trigger on merge
   - Everything just works!

---

## 🤝 Contributing

This framework is designed to evolve. If you find ways to improve it:

1. **For Template Improvements**: Direct commits to main are OK
2. **For Your Application**: Always use the full issue → PR → merge workflow
3. **Share Back**: If you create useful slash commands or workflows, consider contributing them back!

---

## 📚 Additional Resources

- **Detailed Workflows**: See [WORKFLOW.md](./WORKFLOW.md)
- **MCP Server Setup**: See [MCP_SERVERS_GUIDE.md](../../MCP_SERVERS_GUIDE.md)
- **Claude Instructions**: See [CLAUDE.md](../../CLAUDE.md)
- **Command Reference**: Check `.claude/commands/` directory

---

*This framework makes development systematic and predictable. Like building a house, when you follow the right order and use the right tools, everything comes together naturally.*
