# Proposed Documentation Structure

## Core Principle: Minimal Essential Docs Only

### What Stays in `/docs/` (Essential Only)
1. **GITHUB_WORKFLOWS.md** - Definitive workflow automation
2. **ARCHITECTURE.md** - System design (when finalized)
3. **INFRASTRUCTURE.md** - Deployment and setup (when finalized)

### What Goes in `/.github/templates/` (AI Uses These)
Templates that agents/AI use to create consistent structures:
- Issue templates
- PR templates  
- Guides that are actually templates for creating things

### What Goes in `/scratchpad/` (Everything Else)
- All strategies (until approved)
- All ideas and brainstorming
- All drafts and proposals
- Feature explorations
- Meeting notes

## Current Status

### Keep in /docs/:
- `GITHUB_WORKFLOWS.md` - This is definitive

### Move to /scratchpad/:
- Everything else that isn't truly definitive yet

### Guides Question:
- Are HOOKS_GUIDE, RELEASE_GUIDE actually templates?
- Or are they just documentation that should be in scratchpad?
- If they're templates AI uses, they go to .github/templates/
- If they're just docs, they go to scratchpad/

## Proposed Structure:
```
/docs/
├── GITHUB_WORKFLOWS.md     # Definitive
└── (that's it for now)

/.github/templates/
├── issue_templates/
├── pr_templates/
└── guides/                 # If these are templates

/scratchpad/
├── strategies/             # All strategy docs
├── ideas/                  # All brainstorming
├── guides/                 # If these are just docs
└── everything else
```