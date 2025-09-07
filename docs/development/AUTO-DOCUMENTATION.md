# Auto-Documentation System

## Overview

The auto-documentation system keeps your documentation in sync with your codebase automatically. It uses markers in documentation files that get updated by the `doc-updater.sh` hook.

## How It Works

1. **Markers**: Place special HTML comments in your docs where you want auto-updated content
2. **Hook**: The `doc-updater.sh` hook runs on PostToolUse events
3. **Updates**: Content between markers is automatically replaced with current data

## Available Auto-Sections

### Command List
Automatically generates a list of all available slash commands from `.claude/commands/`:

```markdown
<!-- AUTO-SECTION:COMMANDS -->
<!-- END-AUTO-SECTION:COMMANDS -->
```

### Tech Stack
Pulls the technology stack from `docs/PROJECT_PLAN.md`:

```markdown
<!-- AUTO-SECTION:TECH-STACK -->
<!-- END-AUTO-SECTION:TECH-STACK -->
```

### Test Coverage
Updates test coverage badges:

```markdown
<!-- AUTO-SECTION:COVERAGE -->
<!-- END-AUTO-SECTION:COVERAGE -->
```

### Feature List
Extracts features from `docs/FEATURES.md`:

```markdown
<!-- AUTO-SECTION:FEATURES -->
<!-- END-AUTO-SECTION:FEATURES -->
```

## Setup

### 1. Install the Hook

Add to your Claude Code hooks configuration:

```json
{
  "hooks": [
    {
      "type": "PostToolUse",
      "matcher": "Edit|Write|MultiEdit",
      "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/doc-updater.sh"
    }
  ]
}
```

### 2. Add Markers to Your Docs

Edit your README.md or other documentation:

```markdown
## Available Commands

<!-- AUTO-SECTION:COMMANDS -->
(This will be auto-populated)
<!-- END-AUTO-SECTION:COMMANDS -->

## Technology Stack

<!-- AUTO-SECTION:TECH-STACK -->
(This will be auto-populated)
<!-- END-AUTO-SECTION:TECH-STACK -->
```

### 3. Manual Trigger

You can also run the updater manually:

```bash
./.claude/hooks/doc-updater.sh
```

## Benefits

- **Always Current**: Documentation updates automatically as you work
- **Single Source of Truth**: Pull data from actual source files
- **No Manual Sync**: Eliminates the "update the docs" task
- **Preserve Manual Content**: Only updates between markers
- **Selective Updates**: Only files with markers are touched

## Example: README.md

```markdown
# My Project

## 🚀 Quick Start

[Manual content here - won't be touched]

## 📝 Available Commands

<!-- AUTO-SECTION:COMMANDS -->
- `/project-setup` - Interactive discovery & create vision document
- `/plan:generate` - Generate detailed technical documentation from vision
- `/test:generate` - Generate comprehensive test suites
- `/create-issue` - Create any type of work item
- `/work` - Implement issues intelligently
<!-- END-AUTO-SECTION:COMMANDS -->

## 🛠️ Tech Stack

<!-- AUTO-SECTION:TECH-STACK -->
### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS

### Backend
- FastAPI
- PostgreSQL
<!-- END-AUTO-SECTION:TECH-STACK -->

[More manual content]
```

## Extending the System

To add new auto-sections:

1. **Add function to doc-updater.sh**:
```bash
update_my_section() {
    local target_file="$1"
    # Extract or generate content
    local content="..."
    update_between_markers "$target_file" "MY-SECTION" "$content"
}
```

2. **Add markers to docs**:
```markdown
<!-- AUTO-SECTION:MY-SECTION -->
<!-- END-AUTO-SECTION:MY-SECTION -->
```

3. **Call function in main()**:
```bash
if grep -q "<!-- AUTO-SECTION:MY-SECTION -->" "$file"; then
    update_my_section "$file"
fi
```

## Triggers

The doc-updater runs automatically when:

- **Command files change**: Updates command list
- **PROJECT_PLAN.md changes**: Updates tech stack
- **Test files change**: Updates coverage badges
- **FEATURES.md changes**: Updates feature list

## Best Practices

1. **Use sparingly**: Only auto-update truly dynamic content
2. **Preserve readability**: Keep markers subtle
3. **Test locally**: Run manually before setting up hook
4. **Version control**: Commit both manual and auto content
5. **Document markers**: Tell others about auto-sections

## Troubleshooting

### Content not updating?
- Check if markers are exactly correct (case-sensitive)
- Ensure source file exists (e.g., PROJECT_PLAN.md)
- Run manually to see error messages: `./.claude/hooks/doc-updater.sh`

### Hook not running?
- Verify hook is registered in Claude Code
- Check hook permissions: `chmod +x .claude/hooks/doc-updater.sh`
- Look for errors in Claude Code output

### Wrong content?
- Review the extraction logic in doc-updater.sh
- Check source file format hasn't changed
- Ensure markers haven't been corrupted

## Future Enhancements

Potential improvements to the system:

- **JSON manifest**: Define all auto-sections in a config file
- **Template support**: Use templates for generated content
- **Dependency tracking**: Only update when dependencies change
- **Dry-run mode**: Preview changes before applying
- **Rollback**: Keep backup of previous auto-content
- **CI/CD integration**: Run in GitHub Actions too

## Summary

The auto-documentation system eliminates the tedious task of keeping documentation in sync with code. By marking sections for auto-update, you ensure your docs always reflect the current state of your project without manual intervention.