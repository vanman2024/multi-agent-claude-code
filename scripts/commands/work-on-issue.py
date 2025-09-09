#!/usr/bin/env python3
"""
Start work on a GitHub issue with proper branching and PR creation.
Handles the complete workflow from issue to implementation.
"""

import json
import subprocess
import sys
import re
from typing import Optional, Dict, Tuple

def run_command(cmd: str, check: bool = True) -> Tuple[int, str, str]:
    """Run a shell command and return exit code, stdout, and stderr."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(f"Error: {result.stderr}")
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def get_issue_details(issue_number: int) -> Optional[Dict]:
    """Get issue details from GitHub."""
    cmd = f"gh issue view {issue_number} --json title,body,labels,state,assignees"
    code, output, _ = run_command(cmd, check=False)
    
    if code != 0:
        print(f"❌ Failed to get issue #{issue_number}")
        return None
    
    return json.loads(output)

def extract_complexity_from_body(body: str) -> Dict[str, any]:
    """Extract complexity and size from issue metadata."""
    complexity = 3  # Default
    size = "M"      # Default
    
    # Look for metadata section
    if "## Metadata" in body:
        # Extract complexity
        complexity_match = re.search(r'\*\*Complexity\*\*:\s*(\d+)/5', body)
        if complexity_match:
            complexity = int(complexity_match.group(1))
        
        # Extract size
        size_match = re.search(r'\*\*Size\*\*:\s*(XS|S|M|L|XL)', body)
        if size_match:
            size = size_match.group(1)
    
    return {"complexity": complexity, "size": size}

def create_branch(issue_number: int, issue_title: str) -> str:
    """Create a feature branch for the issue."""
    # Sanitize branch name
    branch_suffix = re.sub(r'[^a-z0-9-]', '-', issue_title.lower())[:50]
    branch_name = f"{issue_number}-{branch_suffix}"
    
    print(f"🌿 Creating branch: {branch_name}")
    
    # Ensure we're on main and up to date
    run_command("git checkout main")
    run_command("git pull origin main")
    
    # Create and checkout new branch
    code, _, _ = run_command(f"git checkout -b {branch_name}", check=False)
    
    if code != 0:
        # Branch might already exist
        print(f"⚠️  Branch already exists, checking out...")
        run_command(f"git checkout {branch_name}")
    
    return branch_name

def create_draft_pr(issue_number: int, branch_name: str, issue_title: str) -> Optional[int]:
    """Create a draft PR for the issue."""
    pr_title = f"feat: {issue_title}"
    pr_body = f"""## Description
Implementation for #{issue_number}

## Changes
- [ ] Implementation complete
- [ ] Tests added/updated
- [ ] Documentation updated

## Testing
- [ ] Manual testing completed
- [ ] Automated tests pass

Closes #{issue_number}"""
    
    # Push the branch first (even if empty)
    run_command(f"git push -u origin {branch_name}")
    
    # Create draft PR
    cmd = f"""gh pr create \
        --draft \
        --title "{pr_title}" \
        --body '{pr_body}' \
        --base main \
        --head {branch_name}"""
    
    code, output, _ = run_command(cmd, check=False)
    
    if code != 0:
        print(f"⚠️  Could not create PR (might already exist)")
        # Try to find existing PR
        cmd = f"gh pr list --head {branch_name} --json number"
        _, output, _ = run_command(cmd, check=False)
        if output:
            pr_data = json.loads(output)
            if pr_data:
                pr_number = pr_data[0]["number"]
                print(f"📝 Found existing PR #{pr_number}")
                return pr_number
        return None
    
    # Extract PR number from output
    pr_number = int(output.split("/")[-1])
    print(f"📝 Created draft PR #{pr_number}")
    return pr_number

def select_next_issue() -> Optional[int]:
    """Select the next issue to work on based on priority."""
    print("🔍 Finding next issue to work on...")
    
    # Get open issues assigned to me or unassigned
    cmd = """gh issue list \
        --state open \
        --limit 50 \
        --json number,title,labels,body \
        --jq '.[] | select(.labels | map(.name) | contains(["blocked"]) | not)'"""
    
    _, output, _ = run_command(cmd, check=False)
    
    if not output:
        print("❌ No open issues found")
        return None
    
    issues = []
    for line in output.split("\n"):
        if line:
            issue_data = json.loads(line)
            # Extract priority from body if available
            priority = "P3"  # Default
            if issue_data.get("body"):
                priority_match = re.search(r'\*\*Priority\*\*:\s*(P\d)', issue_data["body"])
                if priority_match:
                    priority = priority_match.group(1)
            
            issues.append({
                "number": issue_data["number"],
                "title": issue_data["title"],
                "priority": priority
            })
    
    # Sort by priority
    issues.sort(key=lambda x: x["priority"])
    
    if issues:
        selected = issues[0]
        print(f"📋 Selected issue #{selected['number']}: {selected['title']}")
        return selected["number"]
    
    return None

def main():
    """Main entry point."""
    # Parse arguments
    args = sys.argv[1:]
    
    issue_number = None
    
    # Check for issue number in arguments
    if args and args[0].startswith("#"):
        issue_number = int(args[0][1:])
    elif args and args[0].isdigit():
        issue_number = int(args[0])
    elif not args or args[0] == "--auto":
        # Auto-select next issue
        issue_number = select_next_issue()
        if not issue_number:
            sys.exit(1)
    
    if not issue_number:
        print("❌ Please provide an issue number or use --auto")
        sys.exit(1)
    
    # Get issue details
    issue = get_issue_details(issue_number)
    if not issue:
        sys.exit(1)
    
    print(f"\n🎯 Working on issue #{issue_number}: {issue['title']}")
    
    # Extract complexity
    assessment = extract_complexity_from_body(issue.get("body", ""))
    print(f"📊 Complexity: {assessment['complexity']}/5, Size: {assessment['size']}")
    
    # Check if Copilot is already assigned
    assignees = issue.get("assignees", [])
    if any("copilot" in a.get("login", "").lower() for a in assignees):
        print("🤖 Copilot is already working on this issue")
        print("Check the PR progress on GitHub")
        sys.exit(0)
    
    # Create branch and PR
    branch_name = create_branch(issue_number, issue["title"])
    pr_number = create_draft_pr(issue_number, branch_name, issue["title"])
    
    if pr_number:
        pr_url = f"https://github.com/vanman2024/multi-agent-claude-code/pull/{pr_number}"
        print(f"\n✅ Ready to work!")
        print(f"🌿 Branch: {branch_name}")
        print(f"📝 PR: #{pr_number}")
        print(f"🔗 {pr_url}")
        print(f"\n💡 Next steps:")
        print(f"1. Implement the feature")
        print(f"2. Run tests: npm test")
        print(f"3. Update PR from draft to ready")
        print(f"4. Request review if needed")
    
    sys.exit(0)

if __name__ == "__main__":
    main()