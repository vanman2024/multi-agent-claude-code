---
allowed-tools: Bash(gh api *, gh issue *), mcp__github(*), Read(*), TodoWrite(*)
description: Create and manage ideas using GitHub Discussions
argument-hint: "[create|list|convert|view] [topic or discussion number]"
---

# Idea - GitHub Discussions Integration

## Purpose
Manage ideas through GitHub Discussions to keep the codebase clean and enable team collaboration.

## Command Flow

When user runs `/idea $ARGUMENTS`:

### Smart Argument Detection
The command intelligently detects what the user wants to do:
- If no arguments → Show interactive menu
- If argument is a number → View that discussion
- If argument is text → Create new discussion with that topic

Execute: !bash scripts/idea/smart-detect.sh "$ARGUMENTS"

## Menu Options

### Option 1: Create New Discussion
Creates a new discussion in the Ideas category with a structured template.

Execute: !bash scripts/idea/create.sh

### Option 2: List All Discussions  
Shows all discussions in the Ideas category with metadata.

Execute: !bash scripts/idea/list.sh

### Option 3: Convert Discussion to Issue
Converts a discussion to an actionable issue for implementation.

**Note**: GitHub API doesn't support native conversion. This creates a linked issue while the discussion remains open for reference.

Execute: !bash scripts/idea/convert.sh

### Option 4: View Specific Discussion
Shows details of a specific discussion including comments.

Execute: !bash scripts/idea/view.sh

## Key Principles

1. **No code blocks** - Keep discussions readable as plain text
2. **Simple format** - Problem, approach, steps, decision
3. **GitHub native** - Use Discussions API, not local files
4. **Clean codebase** - No scratchpad folders or temp files
5. **Team visibility** - All ideas visible in GitHub

## Examples

### Interactive menu:
```
/idea
→ Shows menu with 4 options
→ User selects action
```

### Quick create:
```
/idea "Add user dashboard with analytics"  
→ Skips menu, creates Discussion directly
```

### Quick view:
```
/idea 125
→ Skips menu, shows Discussion #125 directly
```

### Convert workflow:
```
/idea
→ Choose option 3 (Convert)
→ Shows list of discussions
→ Select discussion to convert
→ Creates issue from Discussion
```

## API Limitations

- GitHub doesn't expose native "Convert to Issue" functionality via API
- Discussions cannot be automatically closed when converted
- The conversion creates a new linked issue, not a true conversion
- Manual UI interaction required for native conversion

## Error Handling

- If Discussions not enabled: "❌ GitHub Discussions must be enabled for this repository"
- If Ideas category missing: "❌ Please create an 'Ideas' category in GitHub Discussions"
- If discussion not found: "❌ Discussion #XXX not found"
- If GraphQL fails: Show error and suggest using GitHub web UI

## Script Structure

All implementation logic is in separate scripts:
- `scripts/idea/menu.sh` - Interactive menu
- `scripts/idea/create.sh` - Create new discussion
- `scripts/idea/list.sh` - List all discussions
- `scripts/idea/convert.sh` - Convert to issue
- `scripts/idea/view.sh` - View specific discussion
- `scripts/idea/smart-detect.sh` - Smart argument detection