# Global vs Project Commands Organization

## Global Commands (Work in ANY Project)

These should be available in all projects via Claude's global settings:

### Core Development Commands
- `/project-setup` - Interactive project vision creation
- `/specify` - Create functional requirements  
- `/plan` - Add technical details
- `/tasks` - Generate implementation tasks
- `/import-tasks` - Import to TodoWrite

### Utility Commands
- `/add-mcp` - Add MCP servers
- `/deploy` - Deploy to production
- `/test` - Run tests

## Project-Specific Commands (Template-Specific)

These stay in the template's `.claude/commands/`:

### GitHub Integration
- `/create-issue` - GitHub issue creation
- `/work` - Issue implementation  
- `/copilot-review` - Request reviews
- `/discussions` - Manage discussions

### Template-Specific
- `/hotfix` - Emergency fixes
- `/pr-comments` - PR management

## How to Make Commands Global

### Option 1: Add to Claude's Global Settings
```bash
# Copy command to global commands directory
cp .claude/commands/project-setup.md ~/.claude/commands/
```

### Option 2: Use with Multiple CLIs
Since you'll use Gemini and Codex too, consider:
```bash
# Gemini CLI (non-interactive)
gemini -p "Create project vision for task management app"

# Codex CLI (non-interactive)  
codex -p "Generate functional requirements"

# Claude Code (interactive)
/project-setup
```

## Simplified Structure Going Forward

```
spec-kit-project/
├── memory/          # Spec-kit's constitution
├── scripts/         # Execution scripts
├── templates/       # Templates for generation
├── specs/           # Generated specifications
└── .claude/         # Claude-specific (if needed)
    └── commands/    # Only project-specific commands
```

## Which Commands to Cherry-Pick

### MUST HAVE (Global):
- `/project-setup` - Vision creation
- `/import-tasks` - Bridge to TodoWrite

### NICE TO HAVE (Project):
- `/create-issue` - If using GitHub
- `/work` - If using our workflow

### SKIP (Too Complex):
- All the complex GitHub automation
- All the duplicate spec-kit wrappers

## Integration with Spec-Kit's Pattern

Spec-kit's clean pattern:
```
/command → scripts/script.sh → templates/template.md
```

Our commands should follow this too:
```
/project-setup → scripts/project-setup.sh → templates/project-plan-template.md
```

## Next Steps

1. **Simplify this template** - Remove redundant docs
2. **Extract global commands** - Move to Claude global settings
3. **Create minimal spec-kit integration** - Just the essentials
4. **Support multiple CLIs** - Make commands CLI-agnostic