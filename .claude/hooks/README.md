# Claude Code Hooks

Strategic hooks that enhance your workflow at key points without overwhelming the context.

## The 4 Strategic Hooks (All Working ✅)

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
- **Output**: Reminder only when 5+ files changed

### 4. save-work-state.sh
- **Event**: SessionEnd
- **Purpose**: Saves session state to work journal
- **Benefit**: Resume exactly where you left off
- **Output**: Creates .claude/work-journal.json

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
4. End session - saves state to work journal

## Philosophy

These hooks follow the "Strategic, Not Constant" principle:
- Fire at workflow boundaries, not every file change
- Provide context without overwhelming
- Save state without interrupting
- Warn only when it matters

## Other Files in hooks/ Directory

- `doc-updater.sh` - Not a Claude hook, used by `/plan:generate` command for auto-documentation