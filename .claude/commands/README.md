# Slash Commands Guide

## Universal Features

### @ File References (Available in ALL Commands)

**Any slash command can use @ references to provide additional context:**

```bash
# Examples across different commands:
/work #123 @src/api/auth.ts @docs/api-spec.md
/create-issue --bug "Fix validation" @src/validators/user.ts
/hotfix "Critical security issue" @src/auth/token.ts
/test @src/components/UserProfile.tsx @tests/setup.ts
/deploy @config/production.yml @.env.example
/copilot-review @src/api/*.ts
```

**How @ References Work:**
1. Type `@` in Claude Code to bring up file selector
2. Select one or more files to include as context
3. Files are automatically provided to Claude when command runs
4. Claude analyzes the files to better understand the task

**Common Use Cases:**
- **Code files**: Provide implementation context
- **Documentation**: Include specs, requirements, or guides
- **Config files**: Show current settings or environment
- **Test files**: Understand testing requirements
- **Multiple files**: Provide complete context for complex tasks

**Benefits:**
- More accurate issue descriptions
- Better understanding of code dependencies
- Smarter sub-issue detection
- Context-aware recommendations
- Reduced back-and-forth clarification

## Available Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/create-issue` | Create GitHub issues with intelligent routing | `/create-issue --bug "Fix login" @src/auth.ts` |
| `/work` | Start working on issues | `/work #123 @related/files.ts` |
| `/hotfix` | Emergency fixes | `/hotfix "Security patch" @vulnerable/code.ts` |
| `/test` | Run tests with context | `/test @src/component.tsx` |
| `/deploy` | Deploy with configuration | `/deploy @config/prod.yml` |
| `/copilot-review` | Request code review | `/copilot-review @src/changes/*.ts` |
| `/pr-comments` | Manage PR comments | `/pr-comments @reviewed/files.ts` |
| `/discussions` | Manage GitHub Discussions | `/discussions @docs/proposal.md` |
| `/project-setup` | Initialize new project | `/project-setup @template/config.json` |
| `/add-mcp` | Add MCP servers | `/add-mcp @config/mcp-servers.json` |

## Best Practices

1. **Use @ references liberally** - More context = better results
2. **Include related files** - Not just the file with the issue
3. **Mix file types** - Code + docs + tests for complete picture
4. **Reference examples** - Show Claude what good looks like
5. **Include configs** - Help Claude understand constraints

## Note for Command Authors

When creating new slash commands, remember:
- Users can always add @ references for context
- Don't need explicit file parameters in your command
- Claude automatically receives referenced files
- Design commands assuming context might be provided
- Use provided context to make smarter decisions