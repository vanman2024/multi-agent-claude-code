#!/usr/bin/env python3
"""
Orchestrate multiple agents to work on different aspects of a task in parallel.
This demonstrates the power of agent delegation vs sequential commands.
"""

import json
import sys
from typing import List, Dict

def create_agent_tasks(issue_title: str) -> List[Dict]:
    """
    Break down an issue into tasks for different specialized agents.
    Returns a list of agent task definitions.
    """
    tasks = []
    
    # Analyze what types of work are needed
    title_lower = issue_title.lower()
    
    # Always start with research
    tasks.append({
        "agent": "code-analyzer",
        "description": "Analyze codebase structure",
        "prompt": f"Analyze the codebase to understand how to implement: {issue_title}. Focus on: 1) Existing patterns, 2) Files to modify, 3) Dependencies"
    })
    
    # If it's a feature, add design task
    if "feature" in title_lower or "add" in title_lower:
        tasks.append({
            "agent": "system-architect",
            "description": "Design the architecture",
            "prompt": f"Design the architecture for: {issue_title}. Include: 1) Component structure, 2) Data flow, 3) API contracts"
        })
    
    # If it mentions testing
    if "test" in title_lower:
        tasks.append({
            "agent": "backend-tester",
            "description": "Create comprehensive tests",
            "prompt": f"Create test cases for: {issue_title}. Include: 1) Unit tests, 2) Integration tests, 3) Edge cases"
        })
    
    # If it mentions security
    if "security" in title_lower or "auth" in title_lower:
        tasks.append({
            "agent": "security-auth-compliance",
            "description": "Review security implications",
            "prompt": f"Review security for: {issue_title}. Check: 1) Authentication, 2) Authorization, 3) Input validation, 4) OWASP compliance"
        })
    
    # If it mentions UI/frontend
    if "ui" in title_lower or "frontend" in title_lower or "component" in title_lower:
        tasks.append({
            "agent": "frontend-playwright-tester",
            "description": "Test UI functionality",
            "prompt": f"Test UI for: {issue_title}. Verify: 1) User interactions, 2) Responsive design, 3) Accessibility"
        })
    
    # If it mentions refactoring
    if "refactor" in title_lower or "optimize" in title_lower:
        tasks.append({
            "agent": "code-refactorer",
            "description": "Refactor and optimize code",
            "prompt": f"Refactor code for: {issue_title}. Focus on: 1) Performance, 2) Code reuse, 3) Design patterns"
        })
    
    return tasks

def generate_slash_command(tasks: List[Dict]) -> str:
    """
    Generate a slash command that runs multiple agents in parallel.
    This would be executed by Claude Code.
    """
    command = """---
allowed-tools: Task(*), TodoWrite(*)
description: Multi-agent orchestration
---

# Multi-Agent Task Execution

## Agent Tasks to Run in Parallel

"""
    
    for i, task in enumerate(tasks, 1):
        command += f"""
### Task {i}: {task['description']}
Agent: @{task['agent']}
<task_{i}_prompt>
{task['prompt']}
</task_{i}_prompt>

"""
    
    command += """
## Your Task

Run all agent tasks in parallel using the Task tool:
"""
    
    for i, task in enumerate(tasks, 1):
        command += f"""
- Task(subagent_type="{task['agent']}", prompt=<task_{i}_prompt>)"""
    
    command += """

After all agents complete, synthesize their outputs and proceed with implementation.
"""
    
    return command

def main():
    """Main entry point."""
    # Get issue title from arguments
    if len(sys.argv) < 2:
        print("Usage: python multi-agent-task.py 'issue title'")
        sys.exit(1)
    
    issue_title = " ".join(sys.argv[1:])
    
    print(f"🎯 Analyzing task: {issue_title}")
    print("-" * 50)
    
    # Break down into agent tasks
    tasks = create_agent_tasks(issue_title)
    
    if not tasks:
        print("❌ No specialized agents needed for this task")
        sys.exit(1)
    
    print(f"\n📋 Identified {len(tasks)} agent tasks:")
    for task in tasks:
        print(f"  • {task['agent']}: {task['description']}")
    
    print("\n🚀 Agent Orchestration Plan:")
    print("-" * 50)
    
    # Generate the slash command
    command = generate_slash_command(tasks)
    
    # Save to file for execution
    with open("/tmp/multi-agent-command.md", "w") as f:
        f.write(command)
    
    print("Generated multi-agent slash command saved to: /tmp/multi-agent-command.md")
    print("\nThis would execute all agents in parallel for maximum efficiency!")
    print("\nExample execution flow:")
    print("1. All agents start simultaneously")
    print("2. Each works on their specialized area")
    print("3. Results are synthesized by Claude Code")
    print("4. Implementation proceeds with full context")
    
    # Show the actual Task tool calls that would be made
    print("\n📡 Parallel Task Calls:")
    print("-" * 50)
    for task in tasks:
        print(f'Task(subagent_type="{task["agent"]}", ')
        print(f'     description="{task["description"]}",')
        print(f'     prompt="{task["prompt"][:100]}...")')
        print()

if __name__ == "__main__":
    main()