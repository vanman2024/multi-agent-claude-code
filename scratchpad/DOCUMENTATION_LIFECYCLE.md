# Documentation Lifecycle & Graduation Path

## Current State: NOTHING IS DEFINITIVE YET

Everything is still being developed, tested, and refined. The `/docs/` folder should be EMPTY until things are truly production-ready.

## The Lifecycle Stages

### 1. 🧠 SCRATCHPAD (Ideas)
**Location:** `/scratchpad/ideas/`
**Status:** Brainstorming, exploring
**Example:** "What if we had automatic PR reviews?"
**Graduation:** When approach is decided → Strategy

### 2. 📋 STRATEGY (Decisions Made)
**Location:** `/scratchpad/strategies/`
**Status:** Approach chosen, not implemented
**Example:** "We WILL enforce checkboxes using these workflows"
**Graduation:** When implementation starts → WIP

### 3. 🚧 WORK IN PROGRESS (Being Built)
**Location:** `/scratchpad/wip/`
**Status:** Actively implementing and testing
**Example:** GITHUB_WORKFLOWS.md (still debugging)
**Graduation:** When 100% working and stable → Definitive

### 4. ✅ DEFINITIVE (Production Ready)
**Location:** `/docs/`
**Status:** Fully implemented, tested, stable
**Example:** NONE YET - nothing is production ready
**Requirement:** 
- Fully merged
- Battle-tested
- No known issues
- Used in production

## Current Document Status

### In WIP (Still Being Fixed):
- `GITHUB_WORKFLOWS.md` - Workflows exist but still debugging
- Checkbox enforcement - Implemented but not battle-tested
- Hooks system - Partially working, needs testing

### In Strategies (Decided but Not Built):
- `CHECKBOX_STRATEGY.md` - Implemented but not proven
- `MILESTONE_STRATEGY.md` - Approach defined, not implemented
- `BRANCHING_STRATEGY_IDEAS.md` - Still just ideas

### In Ideas:
- Various dated discussion files

### In Definitive Docs:
- **NOTHING** - The `/docs/` folder should be empty

## Graduation Criteria

### Idea → Strategy
- [ ] Problem clearly defined
- [ ] Solution approach chosen
- [ ] Team/user agrees with approach

### Strategy → WIP
- [ ] Implementation started
- [ ] Actively being coded
- [ ] Testing in progress

### WIP → Definitive
- [ ] 100% implemented
- [ ] All tests passing
- [ ] Used successfully in production
- [ ] No outstanding bugs
- [ ] Documentation accurate
- [ ] Been stable for at least 1 week

## Why This Matters

**Problem:** We keep treating work-in-progress as if it's done
**Solution:** Clear stages showing what's actually ready

If it's in `/docs/`, it means:
- You can rely on it
- It won't change suddenly  
- It's been proven to work
- It's the official way

If it's anywhere else, it's still evolving.

## Action Items

1. Keep `/docs/` empty until things are TRULY ready
2. Move everything to appropriate scratchpad subfolder
3. Only graduate when criteria are met
4. Be honest about what's actually working

## The Anchor Points

When something IS ready, it becomes:
- **README.md** - For user-facing features
- **Wiki pages** - For detailed guides
- **`/docs/` folder** - For technical documentation

But ONLY when it's actually working, not aspirational.