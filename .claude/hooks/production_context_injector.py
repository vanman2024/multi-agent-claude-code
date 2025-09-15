#!/usr/bin/env python3
"""
Production Context Injection Hook
Automatically injects production readiness context when deployment-related commands are detected
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

def should_inject_production_context(user_prompt: str) -> bool:
    """Determine if production context should be injected based on user prompt"""
    deployment_keywords = [
        'deploy', 'deployment', 'production', 'prod', 'live',
        'release', 'go live', 'launch', 'staging',
        'mock', 'api test', 'real data', 'production ready',
        'env', 'environment', 'config'
    ]
    
    prompt_lower = user_prompt.lower()
    return any(keyword in prompt_lower for keyword in deployment_keywords)

def run_mock_detection() -> dict:
    """Run mock detection script and return results"""
    try:
        # Path to the mock detector script
        script_path = Path('.claude/scripts/mock_detector.py')
        
        if not script_path.exists():
            return {"error": "Mock detection script not found"}
            
        # Run the script with JSON output
        result = subprocess.run([
            'python', str(script_path), 
            '--format', 'json', 
            '--output', '/tmp/mock_report'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return {"error": f"Mock detection failed: {result.stderr}"}
            
        # Read the JSON report
        report_path = Path('/tmp/mock_report.json')
        if report_path.exists():
            with open(report_path, 'r') as f:
                return json.load(f)
        else:
            return {"error": "Report file not generated"}
            
    except subprocess.TimeoutExpired:
        return {"error": "Mock detection timed out"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def get_project_context() -> dict:
    """Get current project context for production readiness"""
    context = {
        "timestamp": datetime.now().isoformat(),
        "working_directory": os.getcwd(),
        "git_branch": None,
        "environment_files": [],
        "config_files": [],
        "deployment_files": []
    }
    
    # Get git branch
    try:
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            context["git_branch"] = result.stdout.strip()
    except:
        pass
    
    # Check for common files
    common_files = [
        '.env', '.env.local', '.env.production', '.env.staging',
        'config.py', 'settings.py', 'next.config.js', 'nuxt.config.js',
        'docker-compose.yml', 'Dockerfile', 'vercel.json',
        'package.json', 'requirements.txt'
    ]
    
    for file_name in common_files:
        if Path(file_name).exists():
            if file_name.startswith('.env'):
                context["environment_files"].append(file_name)
            elif 'config' in file_name.lower() or file_name in ['settings.py']:
                context["config_files"].append(file_name)
            elif file_name in ['docker-compose.yml', 'Dockerfile', 'vercel.json']:
                context["deployment_files"].append(file_name)
    
    return context

def generate_production_context_message(mock_report: dict, project_context: dict) -> str:
    """Generate context message for Claude about production readiness"""
    
    # Start with project context
    message = f"""
## 🚨 PRODUCTION READINESS CONTEXT INJECTION

**Current Situation:**
- Working Directory: {project_context['working_directory']}
- Git Branch: {project_context.get('git_branch', 'unknown')}
- Environment Files: {', '.join(project_context['environment_files']) or 'None found'}
- Config Files: {', '.join(project_context['config_files']) or 'None found'}
- Deployment Files: {', '.join(project_context['deployment_files']) or 'None found'}

"""

    # Add mock detection results if available
    if "error" not in mock_report and "summary" in mock_report:
        summary = mock_report["summary"]
        message += f"""**Mock Detection Results:**
- Total Issues Found: {summary.get('total_issues', 0)}
- Critical Issues: {summary.get('critical_issues', 0)} 🚨
- Warning Issues: {summary.get('warning_issues', 0)} ⚠️
- API Endpoints: {summary.get('api_endpoints_ready', 0)}/{summary.get('api_endpoints_total', 0)} ready

"""
        
        # Add critical issues if any
        if mock_report.get("mock_issues"):
            critical_issues = [issue for issue in mock_report["mock_issues"] 
                             if issue.get("severity") == "critical"]
            if critical_issues:
                message += "**🚨 CRITICAL MOCK IMPLEMENTATIONS DETECTED:**\n"
                for issue in critical_issues[:5]:  # Limit to first 5
                    message += f"- {issue.get('file_path')}:{issue.get('line_number')} - {issue.get('category')} mock\n"
                if len(critical_issues) > 5:
                    message += f"- ... and {len(critical_issues) - 5} more critical issues\n"
                message += "\n"
        
        # Add API endpoint status
        if mock_report.get("api_endpoints"):
            message += "**API Endpoint Status:**\n"
            for endpoint, status in list(mock_report["api_endpoints"].items())[:10]:
                emoji = "✅" if status == "ready" else "🚨" if "mock" in status else "⚠️"
                message += f"- {emoji} `{endpoint}` - {status.replace('_', ' ')}\n"
            message += "\n"
    
    elif "error" in mock_report:
        message += f"**Mock Detection Status:** ⚠️ {mock_report['error']}\n\n"
    
    # Add recommendations
    message += """**🎯 PRODUCTION READINESS RECOMMENDATIONS:**

When working on deployment or production-related tasks:

1. **Use the production-specialist sub-agent** - It's specifically trained for production readiness
2. **Run `/prod-ready` command** - Get a comprehensive production readiness report  
3. **Replace ALL mock implementations** - Critical for production deployment
4. **Validate environment configurations** - Ensure production configs are set
5. **Test with real APIs and databases** - Mock data won't work in production

**Available Commands:**
- `/prod-ready` - Run complete production readiness scan
- `/prod-ready --fix` - Auto-fix simple production issues
- `/test-prod` - Generate tests to validate production readiness
- Use `production-specialist` sub-agent for detailed analysis and implementation guidance

"""

    return message

def main():
    """Main hook execution"""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
        
        # Extract user prompt
        user_prompt = input_data.get("prompt", "")
        
        # Check if we should inject production context
        if not should_inject_production_context(user_prompt):
            sys.exit(0)  # No context injection needed
        
        # Get project context
        project_context = get_project_context()
        
        # Run mock detection (with timeout to avoid blocking)
        mock_report = run_mock_detection()
        
        # Generate context message
        context_message = generate_production_context_message(mock_report, project_context)
        
        # Output as JSON for hook system
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context_message
            }
        }
        
        print(json.dumps(output))
        sys.exit(0)
        
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()