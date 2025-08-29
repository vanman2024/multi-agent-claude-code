# Claude Code Hooks Integration with Multi-Agent Framework

## Overview
This document summarizes the integration strategy for Claude Code hooks within our multi-agent development framework, clarifying how local automation complements GitHub's remote automation without overlap.

## The Architecture: Local vs Remote Automation

### The House Metaphor Applied to Hooks
Following our system architecture metaphor:
- **GitHub Workflows = Plumbing** (Remote): Moves things without intelligence
- **Claude Code Hooks = Personal Electrical** (Local): Smart automation for individual developer workflows
- **Key Principle**: Hooks provide intelligence locally, GitHub provides team coordination remotely

## Division of Responsibilities

### GitHub Automation (Remote/Team Layer)
**Runs on GitHub servers | Public to team | Official workflow**
- CI/CD pipelines and deployments
- Issue routing to project boards
- Agent assignment based on complexity/size
- Team-wide quality gates
- Pull request automation
- Production deployments

### Claude Code Hooks (Local/Personal Layer)  
**Runs on developer machine | Private to individual | Personal assistant**
- Pre-flight validation before pushing
- Local environment management
- Personal coding standards enforcement
- Context injection for Claude
- Development workflow optimization
- Real-time code validation

## Why Hooks Weren't Firing: Technical Issues Found

### Problem 1: Incorrect Matcher Pattern
- **Issue**: Used `"Bash.*git push"` as matcher
- **Reality**: Matchers match tool names only, not commands
- **Fix**: Changed to `"Bash"` and let script check for git push

### Problem 2: Session Loading
- **Issue**: Hooks are captured at session start
- **Reality**: Changes to `.claude/settings.json` don't apply mid-session
- **Fix**: Requires either restart or `/hooks` command to reload

### Problem 3: Visibility
- **Issue**: Hook execution not visible in normal mode
- **Fix**: Use transcript mode (Ctrl+R) to see hook execution

## Integration Opportunities

### 1. Agent Coordination
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Task",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/log-agent-task.sh"
      }]
    }],
    "SubagentStop": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/sync-agent-results.py"
      }]
    }]
  }
}
```

### 2. MCP Server Integration
Hooks can intercept MCP tool calls for validation:
```json
{
  "matcher": "mcp__github__create_issue",
  "hooks": [{
    "type": "command",
    "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-issue-template.py"
  }]
}
```

### 3. Context Loading
Use `SessionStart` hooks to inject project state:
- Current sprint issues
- Recent PR statuses  
- Team context and conventions
- Project-specific guidelines

### 4. Smart Pre-Push Validation
Before expensive GitHub Actions run:
- Check for secrets/keys locally
- Run quick smoke tests
- Validate commit message format
- Ensure branch naming conventions

## What NOT to Do with Hooks

### Never Duplicate GitHub's Role
❌ **DON'T**:
- Deploy from hooks (GitHub Actions handles this)
- Run full CI suite locally (too expensive)
- Manage team permissions (GitHub's responsibility)
- Create official documentation (team process)

### Use Hooks for What GitHub Can't
✅ **DO**:
- Set up local development environment
- Apply personal preferences beyond team standards
- Validate before expensive remote operations
- Load context Claude needs for YOUR workflow
- Auto-format to your personal style
- Create local backups before major changes

## Current Implementation Status

### Configured Hooks
1. **current-work.sh** - Injects GitHub issue context (UserPromptSubmit)
2. **auto-commit.sh** - Auto-commits on file changes (PostToolUse) 
3. **test-before-push.sh** - Validates before push (PreToolUse)

### Required Actions
- [x] Fix matcher pattern from `"Bash.*git push"` to `"Bash"`
- [ ] Reload hooks in current session (`/hooks` command)
- [ ] Test in transcript mode (Ctrl+R) to see execution
- [ ] Implement additional coordination hooks for agents

## Key Insights

### The "Personal Assistant" Layer
Hooks create a programmable interface to Claude's actions where you can:
- Intercept and validate operations
- Augment with additional context
- Coordinate multi-agent workflows
- Maintain personal standards
- Optimize your specific workflow

### Complementary, Not Competitive
- GitHub automation handles team coordination
- Claude hooks handle personal productivity
- No overlap, no conflict, just enhancement
- Each layer has its specific role and responsibility

## Next Steps

1. **Immediate**: Restart Claude Code or use `/hooks` to activate fixed configuration
2. **Short-term**: Implement agent coordination hooks
3. **Medium-term**: Build context injection for SessionStart
4. **Long-term**: Create library of reusable hook patterns

## Conclusion

Claude Code hooks provide the "personal electrical system" for our development framework - intelligent, local automation that prepares work before it enters the team's GitHub "plumbing." When properly configured and understood, hooks become a powerful productivity multiplier without interfering with team processes.

The key is understanding that hooks are YOUR layer of the system - customizable, personal, and intelligent - while GitHub remains the team's shared, standardized workflow.