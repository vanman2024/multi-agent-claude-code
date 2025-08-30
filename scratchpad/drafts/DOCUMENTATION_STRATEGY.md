# Complete Documentation Strategy

## Documentation Lifecycle & Graduation Path

### Current State: NOTHING IS DEFINITIVE YET
Everything is still being developed, tested, and refined. The `/docs/` folder should be EMPTY until things are truly production-ready.

## The Three-Stage Workflow

### 1. 📝 DRAFTS (Brainstorming)
**Location:** `/scratchpad/drafts/`
**Status:** Ideas, exploring, brainstorming
**Example:** "What if we had automatic PR reviews?"
**Content:** Raw thoughts, questions, possibilities

### 2. ✅ APPROVED (Decisions Made)
**Location:** `/scratchpad/approved/`
**Status:** Approach chosen, ready to build
**Example:** "We WILL enforce checkboxes using these workflows"
**Content:** Structured docs, clear approach, waiting for implementation

### 3. 🚧 WORK IN PROGRESS (Being Built)
**Location:** `/scratchpad/wip/`
**Status:** Actively implementing and testing
**Example:** GITHUB_WORKFLOWS.md (still debugging)
**Content:** Tied to GitHub issues, being validated

### 4. 🏆 PRODUCTION (Fully Ready)
**Location:** `/docs/` or project root
**Status:** Fully implemented, tested, stable
**Example:** NONE YET - nothing is production ready
**Requirement:** Battle-tested, no known issues, stable for 1+ week

## Document Types & Naming Patterns

### STRATEGY Documents
**Pattern:** `*_STRATEGY.md`
**Purpose:** Planning and decision documents for architectural choices
**Examples:**
- `BRANCHING_STRATEGY.md` - How we handle git branches
- `DEPLOYMENT_STRATEGY.md` - How we deploy applications
- `TESTING_STRATEGY.md` - Our testing approach

### GUIDE Documents
**Pattern:** `*_GUIDE.md`
**Purpose:** How-to instructions for specific tasks
**Examples:**
- `MCP_SERVERS_GUIDE.md` - How to set up MCP servers
- `DEPLOYMENT_GUIDE.md` - How to deploy the application
- `CONTRIBUTING_GUIDE.md` - How to contribute to the project

### WORKFLOW Documents
**Pattern:** `*_WORKFLOW.md` or `*_WORKFLOWS.md`
**Purpose:** Definitive process documentation
**Examples:**
- `GITHUB_WORKFLOWS.md` - GitHub Actions automation
- `DEVELOPMENT_WORKFLOW.md` - Development process
- `RELEASE_WORKFLOW.md` - Release process

### SUMMARY Documents
**Pattern:** `*_SUMMARY.md`
**Purpose:** High-level overviews and quick references
**Examples:**
- `ARCHITECTURE_SUMMARY.md` - System architecture overview
- `API_SUMMARY.md` - API endpoint overview

## Graduation Criteria

### drafts → approved
- [ ] Problem clearly defined
- [ ] Solution approach chosen
- [ ] Team/user agrees with approach
- [ ] Trade-offs documented

### approved → wip
- [ ] GitHub issue created
- [ ] Implementation started
- [ ] Actively being coded
- [ ] Testing in progress

### wip → production
- [ ] 100% implemented
- [ ] All tests passing
- [ ] Used successfully in practice
- [ ] No outstanding bugs
- [ ] Documentation accurate
- [ ] Been stable for at least 1 week

## Directory Structure

```
project-root/
├── /docs/                    # EMPTY until production-ready
│   └── (nothing yet)
├── /scratchpad/
│   ├── drafts/               # Initial ideas, brainstorming
│   │   └── COPILOT_STRATEGY.md
│   ├── approved/             # Approved concepts, ready to build
│   │   ├── AGENT_ORCHESTRATION.md
│   │   └── MILESTONE_STRATEGY.md
│   └── wip/                  # Actively being worked on
│       ├── GITHUB_WORKFLOWS.md
│       └── HOOKS_INTEGRATION_SUMMARY.md
├── CLAUDE.md                 # AI instructions (production)
├── README.md                 # Project overview (production)
└── WORKFLOW.md               # Strict workflow (production)
```

## Core Principles

### Minimal Essential Docs Only
- Don't create documentation for the sake of it
- Every doc must serve a real purpose
- Delete obsolete documentation regularly

### Clear Status Indication
- If it's in `/docs/`, you can rely on it 100%
- If it's in scratchpad, it's still evolving
- Never pretend something is ready when it's not

### Proper Graduation
- Documents must EARN their way to production
- Being in `/docs/` is a privilege, not a right
- Better to keep in scratchpad than promote prematurely

## Key Rules

1. **NEVER create duplicate scratchpad folders** - Use only `/scratchpad/`
2. **NEVER skip stages** - Always go drafts → approved → wip → production
3. **ALWAYS tie wip docs to issues** - No work without tracking
4. **DELETE obsolete drafts** - Don't let them accumulate
5. **KEEP /docs/ sacred** - Only truly production-ready content

## Special Files (Always UPPERCASE, Always Root)
- `README.md` - Project overview (GitHub standard)
- `CLAUDE.md` - AI assistant instructions
- `LICENSE` - License information
- `CHANGELOG.md` - Version history (if maintained)
- `WORKFLOW.md` - The strict development workflow

## When to Create Each Type

- **Create in DRAFTS**: When brainstorming or exploring
- **Move to APPROVED**: When approach is decided and agreed upon
- **Move to WIP**: When implementation starts with GitHub issue
- **Move to PRODUCTION**: When fully tested and stable for 1+ week

## Current Document Status

### In WIP (Still Being Fixed):
- `GITHUB_WORKFLOWS.md` - Workflows exist but still debugging
- `HOOKS_INTEGRATION_SUMMARY.md` - Partially working, needs testing

### In Approved (Ready to Build):
- Various agent and strategy documents
- Waiting for issue assignment and implementation

### In Drafts:
- `COPILOT_STRATEGY.md` - Still planning how to use Copilot

### In Production (/docs/):
- **NOTHING** - The `/docs/` folder should be empty until things are truly ready

## Why This Matters

**Problem:** We keep treating work-in-progress as if it's done
**Solution:** Clear stages showing what's actually ready

This prevents:
- Confusion about what's actually working
- Following incomplete documentation
- Building on unstable foundations
- Wasting time on aspirational features

## Action Items

1. Keep `/docs/` empty until things are TRULY ready
2. Move everything through proper stages
3. Only graduate when criteria are met
4. Be honest about what's actually working
5. Delete old drafts regularly
6. Tie all WIP to GitHub issues