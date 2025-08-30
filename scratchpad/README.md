# Scratchpad Documentation Workflow

## Purpose
The scratchpad is where all documentation evolves from initial thoughts to production-ready docs.

## Three-Stage Workflow

### 1. `drafts/` - Initial Ideas & Brainstorming
- Raw thoughts and concepts
- Quick notes from discussions
- Untested ideas
- Brain dumps
- No structure required
- Exploring possibilities

### 2. `approved/` - Approved Concepts
- Reviewed and approved drafts
- Structured documentation
- Ready for development
- Waiting for issue assignment
- Concepts we commit to building
- Decisions made, approach chosen

### 3. `wip/` - Work In Progress
- Actively being developed
- Tied to specific GitHub issues
- Being tested/validated
- Almost ready for production
- Implementation in progress

## Workflow Process

```
drafts/ → approved/ → wip/ → root docs (production)
```

1. **New concept**: Create in `drafts/`
2. **Review & approve**: Move to `approved/`
3. **Start implementation**: Move to `wip/` with issue number
4. **Complete & merge**: Move to root `/docs` or project root

## Graduation Criteria

### drafts → approved
- [ ] Problem clearly defined
- [ ] Solution approach chosen
- [ ] Team/user agrees with approach
- [ ] Ready to build

### approved → wip
- [ ] GitHub issue created
- [ ] Implementation started
- [ ] Actively being coded
- [ ] Testing in progress

### wip → production (/docs or root)
- [ ] 100% implemented
- [ ] All tests passing
- [ ] Used successfully
- [ ] No outstanding bugs
- [ ] Documentation accurate
- [ ] Stable for at least 1 week

## Rules

- **NEVER** skip stages
- **ALWAYS** tie wip docs to issues
- **DELETE** obsolete drafts regularly
- **KEEP** only active work in wip/
- **MOVE** completed work out of scratchpad
- **NOTHING** goes to /docs until truly production-ready

## File Naming Conventions

### Document Types
- **STRATEGY**: Planning & architectural decisions (`*_STRATEGY.md`)
- **GUIDE**: How-to instructions (`*_GUIDE.md`)
- **WORKFLOW**: Process documentation (`*_WORKFLOW.md`)
- **SUMMARY**: High-level overviews (`*_SUMMARY.md`)

### Naming Rules
- Use UPPERCASE for all documentation files
- Use descriptive names: `GITHUB_WORKFLOWS.md`
- Include issue numbers in wip: `ISSUE_63_HOOKS.md`
- Keep names consistent and clear

## Why This Matters

If it's in `/docs/`, it means:
- You can rely on it
- It won't change suddenly
- It's been proven to work
- It's the official way

If it's in scratchpad, it's still evolving.