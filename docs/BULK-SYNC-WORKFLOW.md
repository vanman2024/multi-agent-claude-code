# Bulk Sync Workflow Guide

## Recommended Workflow: Single-Issue Focus

### Morning Sync (Start of Work Session)
```bash
# 1. Sync todos for the issue you're working on
/bulk-sync 158

# 2. Review what needs to be done
/view-todos  # Shows your current todo list

# 3. Start working through the todos
/work 158
```

### During Work Session
- Work through todos locally using TodoWrite
- Mark items as completed as you go
- Commit changes with issue references

### Evening Push (End of Work Session)
```bash
# 1. Push completed todos back to GitHub
/push-todos 158

# 2. Commit and push any remaining work
git add -A && git commit -m "feat: Progress on #158"
git push
```

## Best Practices

### ✅ DO:
- Use single-issue syncing: `/bulk-sync 158`
- Focus on one issue at a time
- Sync at start of work session
- Push completed todos back at end

### ❌ DON'T:
- Use `/bulk-sync --all` (83+ todos is overwhelming)
- Try to work on multiple issues simultaneously
- Forget to push completed todos back to GitHub

## Common Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/bulk-sync 158` | Sync single issue | Start of work session |
| `/bulk-sync --assigned` | Sync your assigned issues | Weekly planning |
| `/bulk-sync --all` | Sync ALL issues | Rarely - project overview only |
| `/push-todos 158` | Update GitHub checkboxes | End of work session |
| `/view-todos` | See current todos | Anytime |

## Workflow Example

### Day 1: Starting Fresh
```bash
# Morning
/bulk-sync 158           # Get todos from GitHub issue #158
# Result: 20 todos loaded (5 completed, 15 pending)

# Work through todos...
# Mark 3 todos complete in TodoWrite

# Evening
/push-todos 158          # Update GitHub with 3 completed checkboxes
git push                 # Push code changes
```

### Day 2: Continuing Work
```bash
# Morning
/bulk-sync 158           # Sync again
# Result: 0 new todos (deduplication works!)
# Your 3 completed todos from yesterday are still marked complete

# Continue working...
```

## Pain Points & Solutions

| Pain Point | Impact | Solution |
|------------|--------|----------|
| `--all` pulls 83+ todos | Overwhelming, loses focus | Use single-issue sync |
| No issue number tracking | Can't tell which todo belongs where | Script prefixes with `#158:` |
| Duplicates on re-sync | Todo list grows infinitely | Deduplication built-in |
| Manual JSON copying | Tedious and error-prone | Direct TodoWrite integration |

## Integration with /work Command

The bulk-sync works seamlessly with `/work`:

1. `/bulk-sync 158` - Get todos from GitHub
2. `/work 158` - Start implementation
3. Work through TodoWrite items
4. `/push-todos 158` - Update GitHub when done

This creates a complete feedback loop between GitHub issues and local development.