# Claude Code Hooks

Strategic hooks that enhance your workflow at key points without overwhelming the context.

## The 6 Strategic Hooks (All Working ✅)

### 1. load-context.sh 
- **Event**: SessionStart
- **Purpose**: Loads git state, assigned issues, PRs, and previous session context
- **Benefit**: Instant context when you start working
- **Output**: Shows in session start message

### 2. verify-sync-before-claude.sh
- **Event**: UserPromptSubmit
- **Purpose**: Warns if you have unsynced changes when mentioning @claude
- **Benefit**: Prevents testing old code with GitHub bot
- **Output**: Warning message when local != GitHub

### 3. work-checkpoint.sh
- **Event**: Stop (after Claude responds)
- **Purpose**: Gentle reminders about uncommitted work (only if significant)
- **Benefit**: Never lose work between responses
- **Output**: 
  - Note at 5+ uncommitted changes
  - Reminder with `/git commit` at 15+ changes
  - Push reminder at 3+ unpushed commits

### 4. save-work-state.sh
- **Event**: SessionEnd
- **Purpose**: Emergency stash for large uncommitted work
- **Benefit**: Safety net for significant uncommitted changes
- **Output**: Creates emergency stash if >30 uncommitted files

## Hook Output Visibility

**Important**: Hooks output JSON to Claude Code, not to your terminal!
- ✅ You'll see their effects in Claude's responses
- ✅ SessionStart hooks show in the greeting message
- ✅ UserPromptSubmit hooks show as context warnings
- ❌ You won't see terminal output when testing manually

## Configuration

All hooks are configured in `.claude/settings.json`. The strategic hooks fire at:
- **Session boundaries**: Start/End for context
- **Natural pauses**: Stop event for reminders
- **Critical moments**: Before mentioning @claude

## Testing Hooks

To see if hooks are working:
1. Start a new session - should see context loaded
2. Type a message with @claude - should see sync warning if needed
3. Let Claude finish responding - may see work checkpoint reminder
4. End session - creates emergency stash if needed

## Philosophy

These hooks follow the "Strategic, Not Constant" principle:
- Fire at workflow boundaries, not every file change
- Provide context without overwhelming
- Save state without interrupting
- Warn only when it matters

## Additional Hooks

### 5. TodoWrite-post.sh
- **Event**: PostToolUse (when TodoWrite tool is used)
- **Purpose**: Automatically registers todo sessions with the current project
- **Benefit**: Ensures todos are visible in dashboard and CLI viewer
- **Output**: "✅ Todo list updated and session registered"

### 6. register-session.sh
- **Event**: Called by TodoWrite-post.sh
- **Purpose**: Links todo files to project directory for proper tracking
- **Benefit**: Fixes todo persistence and count discrepancies
- **Output**: Registers new sessions in ~/.claude/projects/

## Other Files in hooks/ Directory

- `doc-updater.sh` - Not a Claude hook, used by `/plan:generate` command for auto-documentation
- `todo-reminder.sh` - Legacy todo reminder (replaced by todo dashboard)
- `todo-update-trigger.sh` - Legacy todo trigger (replaced by TodoWrite-post)
- `fix-todo-session.sh` - Utility script to manually fix todo session registration