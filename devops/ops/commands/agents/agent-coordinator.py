#!/usr/bin/env python3
"""
Multi-Agent Coordinator for SignalHire Agent Development

This script coordinates multiple AI agents by:
1. Parsing tasks.md for @ assignments  
2. Calling agents programmatically based on assignments
3. Tracking task completion and updating checkboxes
4. Managing dependencies between tasks

Usage:
    python scripts/agent-coordinator.py [--dry-run] [--interval SECONDS]
"""

import argparse
import json
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Task:
    """Represents a single task with agent assignment."""
    id: str
    agent: str
    description: str
    file_path: str
    completed: bool
    parallel: bool
    dependencies: List[str]


class AgentCoordinator:
    """Coordinates multiple AI agents based on @ assignments in tasks.md"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.tasks_file = repo_root / "specs" / "001-looking-to-build" / "tasks.md"
        self.working_dir = repo_root
        
    def parse_tasks(self) -> List[Task]:
        """Parse tasks.md and extract @ assignments."""
        tasks = []
        
        if not self.tasks_file.exists():
            print(f"Tasks file not found: {self.tasks_file}")
            return tasks
            
        with open(self.tasks_file, 'r') as f:
            content = f.read()
            
        # Regex to match task lines: - [x] T001 @agent Description
        task_pattern = r'- \[([x ])\] (T\d+)(?:\s+\[P\])?\s*@(\w+)\s+(.+?)(?:\s+in\s+(.+?))?(?:\n|$)'
        
        for match in re.finditer(task_pattern, content):
            completed = match.group(1) == 'x'
            task_id = match.group(2)
            agent = match.group(3)
            description = match.group(4)
            file_path = match.group(5) or ""
            
            # Check if task is marked as parallel [P]
            parallel = '[P]' in match.group(0)
            
            # Extract dependencies from description or context (simplified)
            dependencies = self._extract_dependencies(task_id, content)
            
            task = Task(
                id=task_id,
                agent=agent,
                description=description.strip(),
                file_path=file_path.strip(),
                completed=completed,
                parallel=parallel,
                dependencies=dependencies
            )
            tasks.append(task)
            
        return tasks
    
    def _extract_dependencies(self, task_id: str, content: str) -> List[str]:
        """Extract task dependencies based on task number and context."""
        task_num = int(task_id[1:])  # Remove 'T' prefix
        dependencies = []
        
        # Simple dependency rules based on task structure
        if 14 <= task_num <= 19:  # Models depend on tests
            dependencies = [f"T{i:03d}" for i in range(4, 14)]
        elif 20 <= task_num <= 23:  # Services depend on models  
            dependencies = [f"T{i:03d}" for i in range(14, 20)]
        elif 24 <= task_num <= 30:  # CLI depends on services
            dependencies = [f"T{i:03d}" for i in range(20, 24)]
        elif 31 <= task_num <= 34:  # Integration depends on core
            dependencies = [f"T{i:03d}" for i in range(14, 31)]
        elif 35 <= task_num <= 40:  # Polish depends on implementation
            dependencies = [f"T{i:03d}" for i in range(14, 35)]
            
        return [dep for dep in dependencies if dep != task_id]
    
    def get_ready_tasks(self, tasks: List[Task]) -> List[Task]:
        """Get tasks that are ready to execute (dependencies completed)."""
        completed_tasks = {task.id for task in tasks if task.completed}
        ready_tasks = []
        
        for task in tasks:
            if task.completed:
                continue
                
            # Check if all dependencies are completed
            deps_ready = all(dep in completed_tasks for dep in task.dependencies)
            if deps_ready:
                ready_tasks.append(task)
                
        return ready_tasks
    
    def generate_agent_prompt(self, task: Task) -> str:
        """Generate a detailed prompt for the agent to execute the task."""
        
        # Load contract specifications for context
        contracts_dir = self.repo_root / "specs" / "001-looking-to-build" / "contracts"
        data_model_file = self.repo_root / "specs" / "001-looking-to-build" / "data-model.md"
        
        context_parts = [
            f"Task: {task.id} - {task.description}",
            f"File to create/edit: {task.file_path}",
            "",
            "Project Context:",
            "- This is a SignalHire lead generation automation tool",
            "- Using Python 3.11 + asyncio, Stagehand, FastAPI, pandas, pydantic", 
            "- Follow existing code patterns in src/ directory",
            "- Use proper typing, async/await patterns, and error handling",
            "",
        ]
        
        # Add specific context based on task type
        if "model" in task.description.lower():
            context_parts.extend([
                "Model Requirements:",
                "- Use Pydantic models with proper validation",
                "- Include type hints and docstrings", 
                "- Follow the data model specification in specs/001-looking-to-build/data-model.md",
                "- Add proper __str__ and __repr__ methods",
            ])
        elif "service" in task.description.lower():
            context_parts.extend([
                "Service Requirements:",
                "- Use async/await patterns for I/O operations",
                "- Implement proper error handling and logging",
                "- Follow the service contracts in specs/001-looking-to-build/contracts/",
                "- Include rate limiting and retry logic where appropriate",
            ])
        elif "CLI" in task.description or "command" in task.description.lower():
            context_parts.extend([
                "CLI Requirements:",
                "- Use Click framework for command structure",
                "- Add proper help text and argument validation",
                "- Follow the CLI interface contract in specs/001-looking-to-build/contracts/cli-interface.md",
                "- Include progress indicators for long operations",
            ])
        elif "test" in task.description.lower():
            context_parts.extend([
                "Test Requirements:",
                "- Write comprehensive tests using pytest",
                "- Include both positive and negative test cases",
                "- Use appropriate pytest markers (unit, integration, contract)",
                "- Mock external dependencies appropriately",
            ])
            
        return "\n".join(context_parts)
    
    def call_agent(self, task: Task, dry_run: bool = False) -> bool:
        """Call the appropriate agent to execute a task."""
        prompt = self.generate_agent_prompt(task)
        
        if dry_run:
            print(f"[DRY RUN] Would call {task.agent} for {task.id}:")
            print(f"Prompt: {prompt[:200]}...")
            return True
            
        try:
            if task.agent == "codex":
                return self._call_codex(task, prompt)
            elif task.agent == "gemini":
                return self._call_gemini(task, prompt)
            elif task.agent == "copilot":
                print(f"[INFO] Task {task.id} assigned to @copilot - requires manual execution in VS Code")
                return False  # Can't call Copilot programmatically
            elif task.agent == "claude":
                print(f"[INFO] Task {task.id} assigned to @claude - Worker Claude should handle this")
                return False  # Worker Claude handles these
            else:
                print(f"[ERROR] Unknown agent: {task.agent}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Failed to call {task.agent} for {task.id}: {e}")
            return False
    
    def _call_codex(self, task: Task, prompt: str) -> bool:
        """Call OpenAI Codex to execute a task."""
        cmd = [
            "codex", "exec", prompt,
            "--sandbox", "workspace-write", 
            "--cd", str(self.working_dir),
            "-a", "never"  # Never ask for approval
        ]
        
        print(f"[INFO] Calling Codex for {task.id}...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"[SUCCESS] Codex completed {task.id}")
            return True
        else:
            print(f"[ERROR] Codex failed {task.id}: {result.stderr}")
            return False
    
    def _call_gemini(self, task: Task, prompt: str) -> bool:
        """Call Google Gemini to execute a task."""
        cmd = [
            "gemini", "-p", prompt,
            "--yolo"  # Auto-approve all actions
        ]
        
        print(f"[INFO] Calling Gemini for {task.id}...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=self.working_dir)
        
        if result.returncode == 0:
            print(f"[SUCCESS] Gemini completed {task.id}")
            return True
        else:
            print(f"[ERROR] Gemini failed {task.id}: {result.stderr}")
            return False
    
    def mark_task_completed(self, task: Task) -> None:
        """Update tasks.md to mark a task as completed."""
        with open(self.tasks_file, 'r') as f:
            content = f.read()
            
        # Replace [ ] with [x] for this task
        pattern = f'(- \\[) \\] ({task.id}(?:\\s+\\[P\\])?\\s*@{task.agent}\\s+.+)'
        replacement = r'\1x] \2'
        
        updated_content = re.sub(pattern, replacement, content)
        
        if updated_content != content:
            with open(self.tasks_file, 'w') as f:
                f.write(updated_content)
            print(f"[INFO] Marked {task.id} as completed in tasks.md")
        else:
            print(f"[WARNING] Could not find task {task.id} to mark as completed")
    
    def coordinate_once(self, dry_run: bool = False) -> Dict[str, int]:
        """Run one coordination cycle."""
        print("[INFO] Starting coordination cycle...")
        
        tasks = self.parse_tasks()
        ready_tasks = self.get_ready_tasks(tasks)
        
        stats = {"total": len(tasks), "completed": 0, "ready": len(ready_tasks), "executed": 0}
        
        # Count completed tasks
        stats["completed"] = len([t for t in tasks if t.completed])
        
        print(f"[INFO] Found {stats['total']} tasks, {stats['completed']} completed, {stats['ready']} ready")
        
        # Execute ready tasks
        for task in ready_tasks:
            if task.agent in ["codex", "gemini"]:  # Only call programmable agents
                success = self.call_agent(task, dry_run)
                if success and not dry_run:
                    self.mark_task_completed(task)
                    stats["executed"] += 1
            else:
                print(f"[INFO] Skipping {task.id} - {task.agent} requires manual execution")
        
        return stats
    
    def coordinate_loop(self, interval: int = 60, dry_run: bool = False) -> None:
        """Run continuous coordination loop."""
        print(f"[INFO] Starting coordination loop (interval: {interval}s, dry_run: {dry_run})")
        
        try:
            while True:
                stats = self.coordinate_once(dry_run)
                
                if stats["completed"] == stats["total"]:
                    print("[INFO] All tasks completed! Exiting coordination loop.")
                    break
                    
                if stats["ready"] == 0:
                    print("[INFO] No tasks ready for execution. Waiting...")
                
                print(f"[INFO] Waiting {interval}s before next cycle...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n[INFO] Coordination loop interrupted by user")


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Task Coordinator")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without executing")
    parser.add_argument("--interval", type=int, default=60, help="Loop interval in seconds")
    parser.add_argument("--once", action="store_true", help="Run once instead of continuous loop")
    
    args = parser.parse_args()
    
    # Find repo root
    repo_root = Path.cwd()
    while repo_root != repo_root.parent and not (repo_root / ".git").exists():
        repo_root = repo_root.parent
        
    if not (repo_root / ".git").exists():
        print("ERROR: Not in a git repository")
        exit(1)
    
    coordinator = AgentCoordinator(repo_root)
    
    if args.once:
        stats = coordinator.coordinate_once(args.dry_run)
        print(f"[SUMMARY] Executed {stats['executed']} tasks")
    else:
        coordinator.coordinate_loop(args.interval, args.dry_run)


if __name__ == "__main__":
    main()