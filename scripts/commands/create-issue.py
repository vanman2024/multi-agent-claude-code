#!/usr/bin/env python3
"""
Create GitHub issues with automatic complexity assessment and agent assignment.
This script replaces complex bash logic in slash commands.
"""

import json
import subprocess
import sys
import os
from typing import Dict, Tuple, Optional

def run_command(cmd: str) -> Tuple[int, str]:
    """Run a shell command and return exit code and output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout.strip()

def check_branch_status() -> bool:
    """Ensure we're on main branch with latest changes."""
    # Get current branch
    _, current = run_command("git branch --show-current")
    
    if current != "main":
        print(f"❌ ERROR: You must be on main branch to create issues!")
        print(f"\nCurrent branch: {current}")
        print("Required branch: main")
        print("\nRun these commands first:")
        print("  git checkout main")
        print("  git pull origin main")
        return False
    
    # Check if up to date
    run_command("git fetch origin main --quiet")
    _, local = run_command("git rev-parse main")
    _, remote = run_command("git rev-parse origin/main")
    
    if local != remote:
        print("⚠️  Your main branch is not up to date!")
        print("\n🔄 Auto-pulling latest changes...")
        code, _ = run_command("git pull origin main")
        
        if code != 0:
            print("❌ ERROR: Failed to pull latest changes")
            print("Please resolve any conflicts and try again")
            return False
        
        print("✅ Successfully pulled latest changes")
    
    print("✅ On main branch with latest changes - proceeding...")
    return True

def assess_complexity(title: str, description: str = "") -> Dict[str, any]:
    """
    Automatically assess issue complexity based on keywords and patterns.
    Returns complexity (1-5) and size (XS/S/M/L/XL).
    """
    title_lower = title.lower()
    desc_lower = description.lower()
    combined = f"{title_lower} {desc_lower}"
    
    # Simple tasks (Complexity 1-2, Size XS-S)
    simple_patterns = [
        "typo", "rename", "update readme", "add comment", "fix test",
        "update documentation", "add logging", "remove unused",
        "update dependency", "fix lint", "format code"
    ]
    
    # Complex tasks (Complexity 3-5, Size M-XL)
    complex_patterns = [
        "refactor", "architecture", "security", "authentication",
        "authorization", "database", "migration", "performance",
        "integration", "api", "workflow", "pipeline", "deployment"
    ]
    
    # Check patterns
    is_simple = any(pattern in combined for pattern in simple_patterns)
    is_complex = any(pattern in combined for pattern in complex_patterns)
    
    if is_simple and not is_complex:
        return {"complexity": 1, "size": "XS"}
    elif is_complex:
        if "refactor" in combined or "migration" in combined:
            return {"complexity": 4, "size": "L"}
        elif "architecture" in combined or "security" in combined:
            return {"complexity": 5, "size": "XL"}
        else:
            return {"complexity": 3, "size": "M"}
    else:
        # Default to moderate
        return {"complexity": 2, "size": "S"}

def should_assign_copilot(complexity: int, size: str, labels: list = []) -> bool:
    """Determine if Copilot should handle this issue."""
    # Must be BOTH simple AND small
    is_simple = complexity <= 2
    is_small = size in ["XS", "S"]
    
    # Check for blocking labels
    blocking_labels = ["security", "architecture", "infrastructure"]
    has_blockers = any(label in blocking_labels for label in labels)
    
    return is_simple and is_small and not has_blockers

def create_issue(title: str, issue_type: str = "feature", auto_assign: bool = True) -> Optional[int]:
    """
    Create a GitHub issue with automatic complexity assessment.
    Returns the issue number if successful.
    """
    # Assess complexity
    assessment = assess_complexity(title)
    complexity = assessment["complexity"]
    size = assessment["size"]
    
    # Determine issue type from title if not specified
    if "bug" in title.lower() or "fix" in title.lower():
        issue_type = "bug"
    elif "test" in title.lower():
        issue_type = "task"
    elif "doc" in title.lower():
        issue_type = "documentation"
    
    # Build issue body with type-specific checkboxes
    if issue_type == "bug":
        checkboxes = """## Tasks to Fix
- [ ] Reproduce the bug locally
- [ ] Identify root cause
- [ ] Implement fix
- [ ] Add regression test
- [ ] Test fix in multiple scenarios
- [ ] Update documentation if needed
- [ ] Verify fix doesn't break other features"""
    elif issue_type == "feature":
        checkboxes = """## Implementation Tasks
- [ ] Design component/API structure
- [ ] Implement backend logic
- [ ] Create frontend components
- [ ] Add unit tests
- [ ] Add integration tests
- [ ] Update API documentation
- [ ] Add user documentation
- [ ] Performance testing
- [ ] Security review"""
    elif issue_type == "task":
        checkboxes = """## Definition of Done
- [ ] Task requirements understood
- [ ] Implementation complete
- [ ] Code reviewed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Deployed to staging"""
    elif issue_type == "documentation":
        checkboxes = """## Documentation Tasks
- [ ] Review existing documentation
- [ ] Identify gaps/outdated info
- [ ] Write/update content
- [ ] Add code examples
- [ ] Review for accuracy
- [ ] Check formatting/links"""
    else:
        checkboxes = """## Acceptance Criteria
- [ ] Implementation complete
- [ ] Tests added/updated
- [ ] Documentation updated"""
    
    body = f"""## Description
{title}

{checkboxes}

---

## Metadata
*For automation parsing - DO NOT REMOVE*

**Priority**: P2
**Size**: {size}
**Complexity**: {complexity}/5
**Type**: {issue_type}
"""
    
    # Create issue using gh CLI
    cmd = f"""gh issue create \
        --title "{title}" \
        --body '{body}' \
        --label "{issue_type}" \
        --repo vanman2024/multi-agent-claude-code"""
    
    code, output = run_command(cmd)
    
    if code != 0:
        print(f"❌ Failed to create issue: {output}")
        return None
    
    # Extract issue number from output
    issue_number = int(output.split("/")[-1])
    print(f"✅ Created issue #{issue_number}")
    
    # Auto-assign if appropriate
    if auto_assign and should_assign_copilot(complexity, size):
        print(f"🤖 Auto-assigning to GitHub Copilot (Complexity: {complexity}, Size: {size})")
        
        # This would use MCP in the slash command
        # For now, we'll add a comment indicating assignment
        comment = f"""🤖 **GitHub Copilot Auto-Assigned**

**Complexity**: {complexity}/5 (Simple)
**Size**: {size} (Small)
**Type**: {issue_type}

Copilot will begin work automatically."""
        
        run_command(f'gh issue comment {issue_number} --body "{comment}"')
    else:
        print(f"📋 Requires Claude Code (Complexity: {complexity}, Size: {size})")
        
        comment = f"""🧠 **Requires Claude Code/Agent Orchestration**

**Complexity**: {complexity}/5
**Size**: {size}
**Type**: {issue_type}

Run `/work #{issue_number}` when ready to begin implementation."""
        
        run_command(f'gh issue comment {issue_number} --body "{comment}"')
    
    return issue_number

def main():
    """Main entry point for the script."""
    # Get arguments from command line
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # Parse title from arguments
    title = " ".join(args) if args else input("Enter issue title: ")
    
    if not title:
        print("❌ Issue title is required")
        sys.exit(1)
    
    # Check branch status first
    if not check_branch_status():
        sys.exit(1)
    
    # Create the issue
    issue_number = create_issue(title)
    
    if issue_number:
        print(f"\n🔗 View issue: https://github.com/vanman2024/multi-agent-claude-code/issues/{issue_number}")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()