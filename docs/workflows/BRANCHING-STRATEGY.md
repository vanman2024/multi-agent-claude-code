# Branching Strategy

> **Status**: 🔴 PLANNED (Not Implemented)
> **Last Updated**: 2025-09-02
> **Stability**: Under Discussion

## Current Problem

- Branches created at issue creation (via workflow)
- Results in many unused branches
- Copilot also creates its own branches
- Leads to duplication and confusion

## Proposed Solution

### Option 1: Just-In-Time Branches
- Create branch ONLY when work starts
- Use `/work` command to create branch
- Copilot creates its own when assigned

### Option 2: Keep Current System
- Continue creating at issue time
- Add cleanup for unused branches
- Accept some duplication

## Decision Pending

This needs team discussion. For now:
- Track 1 (manual): Use `/work` to create branches
- Track 2 (Copilot): Let Copilot create its own

## Branch Naming

Current convention:
```
{type}-{number}-{short-description}
```

Examples:
- `feature-123-user-auth`
- `fix-456-login-bug`
- `copilot/feature-789`