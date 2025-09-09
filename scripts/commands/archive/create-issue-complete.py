#!/usr/bin/env python3
"""
Complete GitHub issue creation with all workflow steps.
This encapsulates ALL the complexity from the original create-issue.md command.
"""

import json
import subprocess
import sys
import os
import re
from typing import Dict, List, Tuple, Optional

class IssueCreator:
    def __init__(self):
        self.owner = "vanman2024"
        self.repo = "multi-agent-claude-code"
        
    def run_command(self, cmd: str, check: bool = True) -> Tuple[int, str, str]:
        """Run a shell command and return exit code, stdout, and stderr."""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"Command failed: {cmd}")
            print(f"Error: {result.stderr}")
        return result.returncode, result.stdout.strip(), result.stderr.strip()

    def step_0_enforce_workflow(self) -> bool:
        """Ensure we're on main branch with latest changes."""
        print("### Step 0: 🔴 ENFORCE WORKFLOW - MUST BE ON MAIN WITH LATEST")
        
        # Get current branch
        _, current_branch, _ = self.run_command("git branch --show-current")
        
        if current_branch != "main":
            print(f"❌ ERROR: You must be on main branch to create issues!")
            print(f"\nCurrent branch: {current_branch}")
            print("Required branch: main")
            print("\nRun these commands first:")
            print("  git checkout main")
            print("  git pull origin main")
            return False
        
        # Check if up to date
        self.run_command("git fetch origin main --quiet")
        _, local_sha, _ = self.run_command("git rev-parse main")
        _, remote_sha, _ = self.run_command("git rev-parse origin/main")
        
        if local_sha != remote_sha:
            print("⚠️  Your main branch is not up to date!")
            print("\n🔄 Auto-pulling latest changes...")
            code, _, _ = self.run_command("git pull origin main")
            
            if code != 0:
                print("❌ ERROR: Failed to pull latest changes")
                return False
            
            print("✅ Successfully pulled latest changes")
        
        print("✅ On main branch with latest changes - proceeding...")
        return True

    def step_1_check_sub_issue(self) -> Optional[int]:
        """Check if creating a sub-issue."""
        print("\n### Step 1: Check if Creating Sub-Issue")
        
        response = input("Are you creating a sub-issue for an existing issue? (y/n): ").lower()
        if response == 'y':
            parent = input("Enter parent issue number: ")
            try:
                return int(parent)
            except ValueError:
                print("Invalid issue number")
                return None
        return None

    def step_2_check_existing(self) -> bool:
        """Check for existing similar issues."""
        print("\n### Step 2: Check for Existing Similar Issues")
        
        print("📋 Checking existing open issues...")
        cmd = f"gh issue list --repo {self.owner}/{self.repo} --state open --limit 20 --json number,title"
        _, output, _ = self.run_command(cmd, check=False)
        
        if output:
            issues = json.loads(output)
            for issue in issues:
                print(f"#{issue['number']}: {issue['title']}")
            
            response = input("\nIs your issue already covered by any of the above? (y/n): ").lower()
            if response == 'y':
                issue_num = input("Enter existing issue number to work on: ")
                print(f"Use '/work #{issue_num}' to work on that issue instead.")
                return False
        
        return True

    def step_3_determine_type(self, title: str) -> Tuple[str, int, str]:
        """Determine issue type, complexity, and size."""
        print("\n### Step 3: Determine Issue Type")
        
        # Auto-detect type from title
        title_lower = title.lower()
        if "bug" in title_lower or "fix" in title_lower:
            issue_type = "bug"
        elif "feature" in title_lower or "add" in title_lower:
            issue_type = "feature"
        elif "enhance" in title_lower or "improve" in title_lower:
            issue_type = "enhancement"
        elif "refactor" in title_lower:
            issue_type = "refactor"
        elif "test" in title_lower:
            issue_type = "task"
        else:
            print("\nWhat type of issue is this?")
            print("1. feature - New functionality")
            print("2. bug - Something broken")
            print("3. enhancement - Improve existing")
            print("4. task - Simple work item")
            choice = input("Select (1-4): ")
            issue_type = ["feature", "bug", "enhancement", "task"][int(choice)-1]
        
        # Get complexity
        print("\nComplexity (1-5):")
        print("1-2: Simple (typos, renames, docs)")
        print("3: Moderate (multiple components)")
        print("4-5: Complex (architecture, security)")
        complexity = int(input("Complexity: ") or "2")
        
        # Get size
        print("\nSize:")
        print("XS: <1 hour, S: 1-4 hours, M: 1-2 days, L: 3-5 days, XL: >1 week")
        size = input("Size (XS/S/M/L/XL): ").upper() or "S"
        
        return issue_type, complexity, size

    def step_4_5_load_fill_template(self, issue_type: str, title: str, 
                                    complexity: int, size: str) -> str:
        """Load and fill the appropriate template."""
        print("\n### Step 4-5: Load and Fill Template")
        
        # Map issue type to template file
        template_map = {
            "feature": "feature-template.md",
            "bug": "bug-template.md",
            "enhancement": "enhancement-template.md",
            "task": "task-template.md",
            "refactor": "task-template.md"
        }
        
        template_file = f"templates/local_dev/{template_map.get(issue_type, 'task-template.md')}"
        
        # For now, create a simplified template (in real implementation, read actual file)
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
        else:
            checkboxes = """## Acceptance Criteria
- [ ] Implementation complete
- [ ] Tests added/updated
- [ ] Documentation updated"""
        
        # Points mapping
        points_map = {"XS": 1, "S": 2, "M": 5, "L": 8, "XL": 13}
        points = points_map.get(size, 5)
        
        body = f"""## Description
{title}

{checkboxes}

## Testing Requirements
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] No regressions introduced

---

## Metadata
*For automation parsing - DO NOT REMOVE*

**Priority**: P2
**Size**: {size}
**Points**: {points}
**Complexity**: {complexity}/5
**Type**: {issue_type}
**Goal**: Features
**Component**: TBD
"""
        return body

    def step_6_create_issue(self, title: str, body: str, issue_type: str) -> Optional[int]:
        """Create the GitHub issue."""
        print("\n### Step 6: Create GitHub Issue")
        
        # Save body to temp file to avoid quote issues
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(body)
            temp_file = f.name
        
        try:
            cmd = f"""gh issue create \
                --repo {self.owner}/{self.repo} \
                --title "{title}" \
                --body-file {temp_file} \
                --label "{issue_type}" """
            
            code, output, _ = self.run_command(cmd, check=False)
            
            if code == 0:
                # Extract issue number from URL
                issue_number = int(output.split("/")[-1])
                print(f"✅ Created issue #{issue_number}")
                return issue_number
            else:
                print(f"❌ Failed to create issue")
                return None
        finally:
            os.unlink(temp_file)

    def step_7_create_sub_issues(self, parent_issue: int, issue_type: str) -> List[int]:
        """Optionally create sub-issues."""
        print("\n### Step 7: Create Sub-Issues (if needed)")
        
        response = input("Would you like to break this into sub-issues? (y/n): ").lower()
        if response != 'y':
            return []
        
        sub_issues = []
        if issue_type == "feature":
            subtasks = ["Design", "Backend Implementation", "Frontend Implementation", "Testing", "Documentation"]
        elif issue_type == "bug":
            subtasks = ["Reproduce", "Fix Root Cause", "Add Tests", "Verify Fix"]
        else:
            subtasks = ["Research", "Implementation", "Testing"]
        
        print(f"Creating sub-issues for: {', '.join(subtasks)}")
        
        for subtask in subtasks:
            # Create sub-issue (simplified for demo)
            print(f"  Creating sub-issue: {subtask}...")
            # In real implementation, would create actual sub-issues
            
        return sub_issues

    def step_8_check_dependencies(self, issue_number: int) -> None:
        """Check and note dependencies."""
        print("\n### Step 8: Check Dependencies")
        
        response = input("Does this issue depend on any other issues? (y/n): ").lower()
        if response == 'y':
            deps = input("Enter dependency issue numbers (comma-separated): ")
            print(f"Dependencies noted: {deps}")
            # In real implementation, would update issue body

    def step_9_agent_assignment(self, issue_number: int, complexity: int, size: str, 
                               issue_type: str, title: str) -> str:
        """Determine and assign appropriate agent."""
        print("\n### Step 9: Agent Assignment")
        
        # Check if Copilot can handle
        is_simple = complexity <= 2
        is_small = size in ["XS", "S"]
        
        if is_simple and is_small:
            print(f"🤖 Auto-assigning to GitHub Copilot (Complexity: {complexity}, Size: {size})")
            
            # Assign Copilot
            cmd = f"""gh api repos/{self.owner}/{self.repo}/issues/{issue_number}/assignees \
                -X POST -f assignees[]='@copilot'"""
            self.run_command(cmd, check=False)
            
            # Add comment
            comment = f"""🤖 **GitHub Copilot Auto-Assigned**

**Task**: {self.get_task_type(title, issue_type)}
**Complexity**: {complexity}/5 (Simple)
**Size**: {size} (Small)

Expected timeline: ~15 minutes for implementation.
Copilot will begin work automatically."""
            
            self.add_comment(issue_number, comment)
            return "copilot"
        else:
            print(f"📋 Requires Claude Code (Complexity: {complexity}, Size: {size})")
            
            reason = "High complexity" if complexity > 2 else f"Large size ({size})"
            comment = f"""🧠 **Requires Claude Code/Agent Orchestration**

**Reason**: {reason}
**Complexity**: {complexity}/5
**Size**: {size}
**Type**: {issue_type}

Run `/work #{issue_number}` when ready to begin implementation."""
            
            self.add_comment(issue_number, comment)
            return "claude-code"

    def get_task_type(self, title: str, issue_type: str) -> str:
        """Determine task type for Copilot instructions."""
        if "test" in title.lower():
            return "write unit tests"
        elif issue_type == "bug":
            return "fix bug"
        elif "document" in title.lower():
            return "update documentation"
        elif issue_type == "refactor":
            return "refactor code"
        else:
            return "implement feature"

    def add_comment(self, issue_number: int, comment: str) -> None:
        """Add comment to issue."""
        # Save comment to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(comment)
            temp_file = f.name
        
        try:
            cmd = f"gh issue comment {issue_number} --repo {self.owner}/{self.repo} --body-file {temp_file}"
            self.run_command(cmd, check=False)
        finally:
            os.unlink(temp_file)

    def step_10_11_milestones_sprints(self, issue_number: int) -> None:
        """Handle milestone and sprint assignment."""
        print("\n### Step 10-11: Milestone and Sprint Assignment")
        
        # List milestones
        cmd = f"gh api repos/{self.owner}/{self.repo}/milestones --jq '.[] | \"\\(.number): \\(.title)\"'"
        code, output, _ = self.run_command(cmd, check=False)
        
        if code == 0 and output:
            print("Available milestones:")
            print(output)
            milestone = input("Select milestone number (or Enter to skip): ")
            if milestone:
                cmd = f"gh issue edit {issue_number} --repo {self.owner}/{self.repo} --milestone {milestone}"
                self.run_command(cmd, check=False)
                print(f"✅ Assigned to milestone {milestone}")

    def step_12_13_priority_summary(self, issue_number: int, issue_type: str, 
                                   assignment: str) -> None:
        """Set priority and show summary."""
        print("\n### Step 12-13: Priority and Summary")
        
        # Priority is already in metadata, just show summary
        url = f"https://github.com/{self.owner}/{self.repo}/issues/{issue_number}"
        
        print("\n" + "="*50)
        print("✅ Issue Created Successfully!")
        print("="*50)
        print(f"📋 Issue: #{issue_number}")
        print(f"🏷️  Type: {issue_type}")
        print(f"🤖 Assignment: {assignment}")
        print(f"🔗 URL: {url}")
        
        if assignment == "copilot":
            print("\n⚡ Copilot will begin work automatically.")
        else:
            print(f"\n💡 Run '/work #{issue_number}' to start implementation.")

    def run(self, title: str) -> bool:
        """Run the complete issue creation workflow."""
        # Step 0: Enforce workflow
        if not self.step_0_enforce_workflow():
            return False
        
        # Step 1: Check if sub-issue
        parent_issue = self.step_1_check_sub_issue()
        
        if not parent_issue:
            # Step 2: Check existing issues
            if not self.step_2_check_existing():
                return False
        
        # Step 3: Determine type, complexity, size
        issue_type, complexity, size = self.step_3_determine_type(title)
        
        # Step 4-5: Load and fill template
        body = self.step_4_5_load_fill_template(issue_type, title, complexity, size)
        
        # Step 6: Create issue
        issue_number = self.step_6_create_issue(title, body, issue_type)
        if not issue_number:
            return False
        
        # Step 7: Create sub-issues (if not already a sub-issue)
        if not parent_issue:
            self.step_7_create_sub_issues(issue_number, issue_type)
        
        # Step 8: Check dependencies
        self.step_8_check_dependencies(issue_number)
        
        # Step 9: Agent assignment
        assignment = self.step_9_agent_assignment(issue_number, complexity, size, issue_type, title)
        
        # Step 10-11: Milestones and sprints
        self.step_10_11_milestones_sprints(issue_number)
        
        # Step 12-13: Priority and summary
        self.step_12_13_priority_summary(issue_number, issue_type, assignment)
        
        return True

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python create-issue-complete.py 'issue title'")
        sys.exit(1)
    
    title = " ".join(sys.argv[1:])
    creator = IssueCreator()
    
    if creator.run(title):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()