#!/usr/bin/env python3
"""
Analyzer for GitHub issue creation - handles complex logic only.
Returns JSON for the slash command to use with MCP tools.
"""

import json
import subprocess
import sys
import re
from typing import Dict, List, Any

class IssueAnalyzer:
    """Analyzes issue requests and returns structured data."""
    
    def __init__(self):
        self.owner = "vanman2024"
        self.repo = "multi-agent-claude-code"
    
    def check_existing_issues(self, title: str) -> List[Dict]:
        """Check for similar existing issues."""
        try:
            cmd = f"gh issue list --repo {self.owner}/{self.repo} --state open --limit 30 --json number,title,labels"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout:
                issues = json.loads(result.stdout)
                
                # Find similar issues (simple keyword matching)
                title_words = set(title.lower().split())
                similar = []
                
                for issue in issues:
                    issue_words = set(issue['title'].lower().split())
                    overlap = len(title_words & issue_words)
                    
                    # If more than 30% words overlap, consider similar
                    if overlap > len(title_words) * 0.3:
                        similar.append({
                            'number': issue['number'],
                            'title': issue['title'],
                            'similarity': overlap / len(title_words)
                        })
                
                return sorted(similar, key=lambda x: x['similarity'], reverse=True)[:5]
        except Exception as e:
            print(f"Error checking existing issues: {e}", file=sys.stderr)
        
        return []
    
    def analyze_complexity(self, title: str, issue_type: str) -> Dict[str, Any]:
        """Analyze complexity and size based on keywords and patterns."""
        title_lower = title.lower()
        
        # Complexity indicators
        simple_keywords = [
            'typo', 'rename', 'update readme', 'add comment', 'fix test',
            'update documentation', 'add logging', 'remove unused',
            'update dependency', 'fix lint', 'format', 'cleanup'
        ]
        
        moderate_keywords = [
            'endpoint', 'api', 'component', 'feature', 'integrate',
            'implement', 'add support', 'new page', 'crud'
        ]
        
        complex_keywords = [
            'refactor', 'architecture', 'security', 'authentication',
            'authorization', 'database', 'migration', 'performance',
            'infrastructure', 'pipeline', 'deployment', 'scaling',
            'optimize', 'redesign', 'overhaul'
        ]
        
        # Calculate complexity
        has_simple = any(kw in title_lower for kw in simple_keywords)
        has_moderate = any(kw in title_lower for kw in moderate_keywords)
        has_complex = any(kw in title_lower for kw in complex_keywords)
        
        if has_complex:
            complexity = 4 if 'refactor' in title_lower or 'migration' in title_lower else 5
            size = 'L' if complexity == 4 else 'XL'
        elif has_moderate and not has_simple:
            complexity = 3
            size = 'M'
        elif has_simple and not has_moderate:
            complexity = 1
            size = 'XS'
        else:
            # Default based on issue type
            if issue_type == 'bug':
                complexity = 2
                size = 'S'
            elif issue_type == 'feature':
                complexity = 3
                size = 'M'
            else:
                complexity = 2
                size = 'S'
        
        # Points mapping
        points_map = {'XS': 1, 'S': 2, 'M': 5, 'L': 8, 'XL': 13}
        points = points_map.get(size, 5)
        
        return {
            'complexity': complexity,
            'size': size,
            'points': points,
            'copilot_eligible': complexity <= 2 and size in ['XS', 'S']
        }
    
    def determine_issue_type(self, title: str) -> str:
        """Determine issue type from title keywords."""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['bug', 'fix', 'broken', 'error', 'issue']):
            return 'bug'
        elif any(word in title_lower for word in ['feature', 'add', 'new', 'create']):
            return 'feature'
        elif any(word in title_lower for word in ['enhance', 'improve', 'update', 'upgrade']):
            return 'enhancement'
        elif any(word in title_lower for word in ['refactor', 'cleanup', 'reorganize']):
            return 'refactor'
        elif any(word in title_lower for word in ['test', 'testing', 'spec']):
            return 'task'
        elif any(word in title_lower for word in ['docs', 'documentation', 'readme']):
            return 'documentation'
        else:
            return 'task'
    
    def suggest_sub_issues(self, issue_type: str, complexity: int) -> List[str]:
        """Suggest sub-issues based on type and complexity."""
        if complexity <= 2:
            return []  # Simple issues don't need sub-issues
        
        if issue_type == 'feature':
            return [
                'Design and Architecture',
                'Backend Implementation', 
                'Frontend Implementation',
                'Testing and Validation',
                'Documentation'
            ]
        elif issue_type == 'bug':
            return [
                'Reproduce and Diagnose',
                'Implement Fix',
                'Add Regression Tests',
                'Verify No Side Effects'
            ]
        elif issue_type == 'enhancement':
            return [
                'Research Current Implementation',
                'Design Improvements',
                'Implementation',
                'Testing and Migration'
            ]
        elif issue_type == 'refactor':
            return [
                'Identify Refactor Targets',
                'Implement Changes',
                'Update Tests',
                'Verify No Regressions'
            ]
        
        return []
    
    def get_copilot_task_type(self, title: str, issue_type: str) -> str:
        """Determine specific task type for Copilot instructions."""
        title_lower = title.lower()
        
        if 'test' in title_lower:
            return 'write unit tests'
        elif issue_type == 'bug':
            return 'fix bug'
        elif 'document' in title_lower or 'readme' in title_lower:
            return 'update documentation'
        elif issue_type == 'refactor':
            return 'refactor code'
        else:
            return 'implement feature'
    
    def analyze(self, title: str) -> Dict[str, Any]:
        """Main analysis function that returns all recommendations."""
        # Determine issue type
        issue_type = self.determine_issue_type(title)
        
        # Analyze complexity
        complexity_data = self.analyze_complexity(title, issue_type)
        
        # Check for existing similar issues
        similar_issues = self.check_existing_issues(title)
        
        # Suggest sub-issues
        sub_issues = self.suggest_sub_issues(issue_type, complexity_data['complexity'])
        
        # Determine agent and task type
        if complexity_data['copilot_eligible']:
            agent = 'copilot'
            task_type = self.get_copilot_task_type(title, issue_type)
        else:
            agent = 'claude-code'
            task_type = 'complex implementation'
        
        # Build complete analysis
        analysis = {
            'title': title,
            'issue_type': issue_type,
            'complexity': complexity_data['complexity'],
            'size': complexity_data['size'],
            'points': complexity_data['points'],
            'copilot_eligible': complexity_data['copilot_eligible'],
            'agent': agent,
            'task_type': task_type,
            'similar_issues': similar_issues,
            'suggest_sub_issues': sub_issues,
            'priority': 'P2',  # Default, could be smarter
            'labels': [issue_type],
            'component': self.determine_component(title),
            'needs_security_review': any(word in title.lower() for word in ['auth', 'security', 'token', 'password']),
            'needs_architecture_review': any(word in title.lower() for word in ['architecture', 'refactor', 'redesign'])
        }
        
        return analysis
    
    def determine_component(self, title: str) -> str:
        """Determine which component this affects."""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['ui', 'frontend', 'react', 'component', 'page']):
            return 'Frontend'
        elif any(word in title_lower for word in ['api', 'backend', 'server', 'endpoint']):
            return 'Backend'
        elif any(word in title_lower for word in ['database', 'db', 'migration', 'schema']):
            return 'Database'
        elif any(word in title_lower for word in ['auth', 'login', 'user', 'permission']):
            return 'Auth'
        elif any(word in title_lower for word in ['deploy', 'ci', 'cd', 'pipeline', 'docker']):
            return 'Infrastructure'
        else:
            return 'General'

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'No title provided'}))
        sys.exit(1)
    
    title = ' '.join(sys.argv[1:])
    analyzer = IssueAnalyzer()
    analysis = analyzer.analyze(title)
    
    # Output as JSON for the slash command to consume
    print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    main()