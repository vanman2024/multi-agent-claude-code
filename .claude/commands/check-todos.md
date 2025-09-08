---
allowed-tools: Bash(*), Read(*), TodoWrite(*)
description: Load todos from this project's archive into current TodoWrite session
argument-hint: [optional: 'load' to import into TodoWrite]
---

# Check and Load Project Todos

## Your Task
Use the Python todo-manager to get todos for THIS specific project and load them into TodoWrite.

First, get the project's todos from the master archive:
!python3 .claude/scripts/todo-manager.py --project . stats

Get the actual todo data in JSON format:
!cat ~/.claude/projects/-home-gotime2022-Projects-multi-agent-claude-code/todo-archive/master-todos.json

Now use TodoWrite to load these project-specific todos into the current session.