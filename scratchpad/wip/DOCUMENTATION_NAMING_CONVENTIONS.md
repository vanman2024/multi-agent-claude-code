# Documentation Naming Conventions & Organization

## Document Types & Naming Patterns

### 1. STRATEGY Documents
**Pattern:** `*_STRATEGY.md`
**Purpose:** Planning and decision documents for architectural choices
**Location:** `/docs/strategies/` (when finalized), `/scratchpad/` (when in development)
**Examples:**
- `BRANCHING_STRATEGY.md` - How we handle git branches
- `DEPLOYMENT_STRATEGY.md` - How we deploy applications
- `TESTING_STRATEGY.md` - Our testing approach

### 2. GUIDE Documents
**Pattern:** `*_GUIDE.md`
**Purpose:** How-to instructions for specific tasks
**Location:** `/docs/guides/` (always definitive)
**Examples:**
- `MCP_SERVERS_GUIDE.md` - How to set up MCP servers
- `DEPLOYMENT_GUIDE.md` - How to deploy the application
- `CONTRIBUTING_GUIDE.md` - How to contribute to the project

### 3. WORKFLOW Documents
**Pattern:** `*_WORKFLOW.md` or `*_WORKFLOWS.md`
**Purpose:** Definitive process documentation
**Location:** `/docs/` or `.github/` (for GitHub-specific)
**Examples:**
- `GITHUB_WORKFLOWS.md` - GitHub Actions automation
- `DEVELOPMENT_WORKFLOW.md` - Development process
- `RELEASE_WORKFLOW.md` - Release process

### 4. SUMMARY Documents
**Pattern:** `*_SUMMARY.md`
**Purpose:** High-level overviews and quick references
**Location:** `/docs/`
**Examples:**
- `ARCHITECTURE_SUMMARY.md` - System architecture overview
- `API_SUMMARY.md` - API endpoint overview

### 5. IDEAS Documents (Scratchpad)
**Pattern:** `*_IDEAS.md`
**Purpose:** Brainstorming and unfinalized thoughts
**Location:** `/scratchpad/` (ALWAYS)
**Examples:**
- `FEATURE_IDEAS.md` - Potential features
- `OPTIMIZATION_IDEAS.md` - Performance improvements to consider

## Document Lifecycle & Graduation

### Phase 1: Scratchpad (Ideas)
- **Location:** `/scratchpad/`
- **Naming:** Can be informal, but prefer `*_IDEAS.md`
- **Content:** Rough thoughts, questions, possibilities
- **Status:** Not committal, just exploring

### Phase 2: Draft Strategy
- **Location:** `/scratchpad/`
- **Naming:** `*_STRATEGY.md` (but still in scratchpad)
- **Content:** More structured, comparing options
- **Status:** Deciding between approaches

### Phase 3: Approved Strategy
- **Location:** `/docs/strategies/`
- **Naming:** `*_STRATEGY.md`
- **Content:** Chosen approach with rationale
- **Status:** This is what we're doing

### Phase 4: Implemented Workflow
- **Location:** `/docs/` or `.github/`
- **Naming:** `*_WORKFLOW.md`
- **Content:** Step-by-step process documentation
- **Status:** This is HOW we do it

## Graduation Criteria

**From Scratchpad → Strategy:**
- Team/user has reviewed and chosen an approach
- Document has clear recommendations
- Trade-offs are documented

**From Strategy → Workflow:**
- Strategy has been implemented in code
- Process has been tested and validated
- Steps are clear and reproducible

## Directory Structure

```
project-root/
├── docs/
│   ├── strategies/          # Finalized strategy documents
│   │   ├── DEPLOYMENT_STRATEGY.md
│   │   └── TESTING_STRATEGY.md
│   ├── guides/              # How-to guides
│   │   └── MCP_SERVERS_GUIDE.md
│   ├── GITHUB_WORKFLOWS.md  # Definitive workflow docs
│   └── API_SUMMARY.md       # Summaries
├── scratchpad/              # Ideas and drafts
│   ├── *_IDEAS.md          # Brainstorming
│   └── *_STRATEGY.md       # Draft strategies
└── .github/
    └── COPILOT_WORKFLOW.md  # GitHub-specific workflows
```

## Key Rules

1. **NEVER create two scratchpad folders** - Use only `/scratchpad/`
2. **IDEAS stay in scratchpad** - Don't move to docs until finalized
3. **STRATEGIES graduate** - Move from scratchpad to `/docs/strategies/` when approved
4. **GUIDES are always definitive** - No draft guides, only complete ones
5. **WORKFLOWS document reality** - Only create after implementation

## Special Files (Always UPPERCASE, Always Root)
- `README.md` - Project overview
- `CLAUDE.md` - AI assistant instructions
- `LICENSE` - License information
- `CHANGELOG.md` - Version history

## When to Create Each Type

- **Create IDEAS**: When brainstorming or exploring
- **Create STRATEGY**: When comparing approaches to make a decision
- **Create GUIDE**: When teaching someone HOW to do something specific
- **Create WORKFLOW**: When documenting an established process
- **Create SUMMARY**: When providing overview of complex system

---

*Note: This document itself should graduate from scratchpad to `/docs/` once reviewed and approved.*