---
allowed-tools: Bash(*), TodoWrite(*)
description: View ALL todos (completed/pending/in-progress) across all sessions for projects
argument-hint: [current|all|summary|export]
---

# Project Todos - Comprehensive todo tracking across all sessions

<!--
WHEN TO USE THIS COMMAND:
- See todos for current project
- View summary of todos across all projects
- Export project todos to markdown
- Track work across multiple sessions

WHAT IT SHOWS:
- Project-specific todos from all sessions
- Summary of todos across all projects
- Never modifies the ~/.claude/todos folder
- Reads and organizes existing todos

NOTE: This command uses a custom script that organizes todos without
modifying Claude Code's todo storage structure.
-->

## Your Task

Show todos organized by project using the custom organization script.

### Handle Arguments

Check what argument was provided (default is "current"):
- `current` or no argument - Show todos for current project
- `summary` - Show summary of all projects with todo counts
- `export` - Export current project's todos to markdown

### Check for Web Viewer First

Check if the web viewer is available and running:
!`lsof -i:8080 2>/dev/null | grep -q LISTEN && echo "✅ Todo Dashboard is running at http://localhost:8080" || echo "💡 Start web viewer: cd todo-viewer && node server.js"`

If web viewer is running, remind user:
- Open http://localhost:8080 to see ALL todos across every session
- Real-time updates when todos change
- Beautiful visualization with filtering and search

### Execute the Enhanced Table Script

Run the table view script for terminal visualization:

For table view (default):
!`bash /home/gotime2022/Projects/multi-agent-claude-code/.claude/scripts/project-todos-table.sh table`

For markdown export:
!`bash /home/gotime2022/Projects/multi-agent-claude-code/.claude/scripts/project-todos-table.sh markdown`

For summary of all projects:
!`bash /home/gotime2022/Projects/multi-agent-claude-code/.claude/scripts/organize-todos-by-project.sh summary`

### Display Results

The enhanced table view shows:
- **Beautiful box-drawing table** with all todos organized by status
- **Color-coded statuses**: 🔄 In Progress (yellow), ⏳ Pending (cyan), ✅ Completed (green)
- **Statistics bar** showing counts for each status
- **All sessions** included - not just current session
- **Smart truncation** of long task descriptions
- **Markdown export** for GitHub-friendly format

### Additional Information

Tell the user:
- Todos are read from Claude Code's storage without modification
- Each todo is linked to its original session
- Todos persist across Claude Code sessions
- Export creates a file in ~/.claude/todo-exports/

### Options

Suggest these options to the user:
- `/project-todos` - View beautiful table of ALL project todos (default)
- `/project-todos markdown` - Export as GitHub-friendly markdown
- `/project-todos summary` - See todo counts across all projects
- `/todos` - Built-in command for current session only
- Use TodoWrite tool to create new todos in current session