# Command Following Issue

## Problem
Claude is not following slash command steps systematically. Skips checks, jumps to conclusions.

## Example: /wip command failures
- Doesn't check for uncommitted changes
- Doesn't check for worktrees
- Doesn't ask about worktree creation
- Jumps straight to git checkout -b

## Potential Causes
1. Pattern matching instead of following instructions
2. Mixed format (instructions vs commands vs explanations)
3. Commands too long (100+ lines)
4. No enforcement mechanism
5. Training bias toward "quick help" over "systematic process"

## Potential Solutions
- Shorter, checklist-style commands
- Clear STOP points
- Explicit confirmations required
- Less explanation mixed with steps

## To Investigate Later
- Create separate branch for command redesign
- Test checklist format vs current format
- Add enforcement mechanisms