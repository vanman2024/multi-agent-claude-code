# Multi-Agent Development Framework: System Context

## What We're Building

This repository (`multi-agent-claude-code`) IS a **complete development framework** that gets **cloned into each new project**. It's not a tool that manages external projects - it's a framework that BECOMES each project, bringing all automation capabilities with it. This framework automates software development lifecycles through Claude Code CLI, with specialized components that work together to take any project from concept to production.

## Framework Deployment Model

This repository is a **template framework** that:

1. **Gets cloned entirely** into each new project
2. **Brings all automation** (workflows, agents, templates) with it
3. **Shares infrastructure** across all projects using the same tokens

### How Projects Are Created:
```bash
# Clone the framework
git clone vanman2024/multi-agent-claude-code my-new-project
cd my-new-project
rm -rf .git && git init

# Customize for this specific project
claude /project-setup

# Framework is now configured for THIS project's needs
```

### Infrastructure Sharing Model:
All projects created from this framework share:
- **Single Supabase Instance** (different schemas per project)
- **Single Vercel Account** (different projects)
- **Single GitHub Organization** (different repos)
- **Same MCP Servers** (configured once, used everywhere)

### What Gets Customized Per Project:
- Architecture decisions (via `/project-setup`)
- Database schema (project-specific tables)
- Feature set (via generated issues)
- Active agents (based on project type)
- Active tools (based on project type)

## Project-Type Specific Tooling

### Core Tools (Used Across Project Types)
- **Postman/Newman** - API testing (external APIs or your own)
- **DigitalOcean CLI** - Backend hosting, webhooks, serverless
- **ngrok** - Webhook testing (Stripe, external systems, etc.)
- **GitHub Actions** - CI/CD for all project types

### For API/Integration Projects (Connecting Existing Systems):
**Characteristics:**
- No need for own database (using external systems)
- No need for auth (using external systems)
- Focus on middleware/adapters
- Minimal infrastructure

**Infrastructure Created:**
- Webhook endpoints (if needed)
- API transformation layers
- Rate limiting
- Basic monitoring

### For Full-Stack SaaS Projects:
**Characteristics:**
- Need complete infrastructure
- Own database, auth, storage
- Frontend + Backend + API
- Payment processing

**Infrastructure Created:**
- **Supabase** - Database, Auth, Storage
- **Vercel** - Frontend hosting
- **DigitalOcean** - Backend API hosting
- **Stripe** - Payments
- **Resend** - Transactional email
- **Postman** - API testing (yes, even for your own APIs!)

### For Static Sites/Marketing:
**Always Used:**
- **Vercel** - Hosting with edge functions
- **Contentful/Sanity** - CMS
- **Plausible** - Analytics
- **Cloudinary** - Image optimization

### For CLI Tools:
**Always Used:**
- **npm/cargo/pip** - Package distribution
- **GitHub Releases** - Binary distribution
- **No hosting needed** - Runs locally

## Framework Components Overview

### Core Architecture
- **GitHub Integration**: Issues and project boards serve as the data layer and workflow engine
- **Agent System**: 13 specialized AI agents handle different development phases
- **Command System**: 10 orchestration commands that coordinate agents and workflows
- **Hook System**: 7 automation hooks that provide real-time coordination
- **MCP Integration**: HTTP servers for consistent external service APIs
- **GitHub Workflows**: 7 automation workflows handle the "plumbing layer" (CI/CD, deployment, project management)
- **Deployment Pipeline**: Vercel + DigitalOcean automation with quality gate enforcement

### Component Relationships
```
Commands → Route work to → Agents → Coordinate via → Hooks → Sync with → GitHub → Trigger → MCP Servers
                                                                    ↓
                                                            GitHub Workflows → Deploy to → Vercel/DigitalOcean
```

**The Plumbing Layer**: GitHub workflows handle automation without intelligence - they move data, run tests, and deploy code following predefined paths. The intelligence comes from Claude Code agents and hooks.

**Agent Routing**: Work is routed to appropriate agents based on:

**GitHub Project Components** → determine which specialist handles the work:
- **Frontend** → frontend-specialist (UI/UX components, client-side logic)
- **Backend** → backend-specialist (API endpoints, server-side logic)
- **Database** → backend-specialist or infrastructure-specialist (data models, migrations, queries)
- **DevOps** → infrastructure-specialist (CI/CD, deployment, infrastructure)
- **Auth** → backend-specialist or security focus (authentication and authorization systems)
- **API Gateway** → backend-specialist (request routing and middleware)
- **Testing** → test-specialist (test suites, coverage, QA)
- **Documentation** → documentation coordination across relevant specialists
- **Integration** → backend-specialist (third-party service connections)
- **Messaging** → backend-specialist (email, SMS, notifications)
- **Analytics** → monitoring-specialist (metrics, tracking, insights)
- **Storage** → infrastructure-specialist (file and media management)
- **CI/CD** → infrastructure-specialist or deployment-specialist (build and deployment pipelines)
- **Monitoring** → monitoring-specialist (logging and observability)
- **Security** → specialized security analysis and implementation
- **Configuration** → infrastructure-specialist (settings and environment management)
- **Core Logic** → fullstack-specialist or system-architect (main business functionality)
- **Workflow** → fullstack-specialist (business process automation)
- **Reporting** → backend-specialist or monitoring-specialist (reports and dashboards)
- **Admin** → fullstack-specialist (admin panels and tools)

**Work Types** → determine approach and priority:
- `enhance` → enhancement and feature development
- `refactor` → refactor-specialist for code improvement
- `bug` → debugger for issue resolution
- `deploy` → deployment-specialist for deployment operations

**Project Context** → ensure proper integration and coordination

## Project-First Mindset

### Everything Flows From Project Context
1. **Project Structure** dictates which agents are needed
2. **Project Type** determines command behavior
3. **Project Standards** guide agent decision-making
4. **Project State** (in GitHub) drives all automation
5. **Project Goals** define success criteria for quality gates

### Context Sources
When building any component, consistently reference:
- **Project documentation** in the current repository
- **Existing Claude Code patterns** from documentation
- **GitHub issue workflows** already established
- **MCP server capabilities** currently available
- **Hook coordination points** already defined

## Implementation Approach

### Use Existing Patterns
- Follow established Claude Code slash command patterns
- Use documented sub-agent template structures
- Apply proven hook integration methods
- Reference MCP server integration examples
- Follow GitHub workflow automation standards

### Build Incrementally
Each component should:
- **Integrate** with existing project structure
- **Reference** established documentation and patterns
- **Coordinate** with other framework components
- **Maintain** consistency with project standards
- **Extend** capabilities without breaking existing workflows

### Project Knowledge Integration
Always consider:
- **Current project context** from documentation
- **Established workflows** and their requirements
- **Existing agent capabilities** and coordination points
- **Available MCP servers** and their APIs
- **Deployment patterns** already configured

## Key Principles

### 1. Clone Once, Customize Once
Each project starts as a full framework clone that gets customized via `/project-setup` for that specific project's needs.

### 2. Shared Infrastructure
All projects use the same service accounts (Supabase, Vercel, GitHub) but maintain isolation through schemas, projects, and repos.

### 3. Project Isolation
Despite sharing services, projects are isolated:
- Different database schemas in same Supabase
- Different storage buckets
- Different Vercel projects
- Separate GitHub repositories

### 4. Zero Additional Setup
Cloning brings everything needed - all workflows, agents, templates, and automation are included from day one.

### 5. Framework Serves Projects
The framework adapts to project needs, not vice versa. Project requirements drive:
- Which agents are activated
- How commands behave
- What hooks coordinate
- Which MCP servers are needed

### 6. GitHub as Central Orchestrator
All framework state and coordination flows through GitHub:
- Issues define work to be done
- Project boards track progress
- Labels trigger automated workflows
- Status changes coordinate next steps

### 7. Consistent Integration Patterns
All components follow established patterns for:
- Claude Code integration
- GitHub API interactions
- MCP server communication
- Hook coordination
- Error handling and recovery

### 8. Modular but Coordinated
Components are built separately but designed to work together:
- Commands orchestrate agents
- Agents coordinate via hooks
- Hooks sync with GitHub
- GitHub triggers MCP operations
- MCP servers provide external capabilities

## Context Awareness Requirements

When building any component:

### Always Reference
- **Current project documentation** for context and requirements
- **Existing Claude Code patterns** for implementation standards
- **Established workflows** for integration requirements
- **Available resources** (agents, hooks, MCP servers)
- **Project-specific standards** for consistency

### Never Assume
- **Technology stack** - framework is application-agnostic
- **Deployment platforms** - framework provides capability, not requirements
- **Database needs** - GitHub serves as framework data layer
- **External dependencies** - beyond GitHub and Claude Code CLI

### Always Maintain
- **Project-first approach** in all decisions
- **Integration with existing components**
- **Consistency with established patterns**
- **Reference to documented standards**
- **Coordination with other framework parts**

## Success Criteria

### Framework Quality
- **Modular**: Components work independently
- **Integrated**: Components coordinate seamlessly
- **Consistent**: All parts follow same patterns
- **Documented**: Clear relationship to project context
- **Extensible**: Easy to add new capabilities

### Project Integration
- **Context-Aware**: Understands current project needs
- **Pattern-Consistent**: Uses established approaches
- **Documentation-Referenced**: Builds on existing knowledge
- **Workflow-Integrated**: Fits existing development processes
- **Standard-Compliant**: Follows project requirements

This framework transforms any development project through intelligent automation while maintaining consistency with established patterns and project-specific requirements.

## Complete Project Lifecycle

### Phase 1: Framework Cloning
1. Clone `multi-agent-claude-code` repository
2. Remove git history, initialize new repo
3. All workflows, agents, templates are now in the project

### Phase 2: Project Customization (/project-setup)
1. Interactive conversation about project needs
2. **Detect project type** (API/Integration, SaaS, Static, CLI)
3. Generate ARCHITECTURE.md and INFRASTRUCTURE.md
4. Create blocking infrastructure issues
5. Configure which agents/workflows are active
6. **Enable project-type specific tools** (Postman for APIs, Supabase for SaaS, etc.)

### Phase 3: Infrastructure Build
1. Complete blocking infrastructure issues
2. Set up project schema in shared Supabase
3. Configure project-specific buckets/auth rules
4. Test infrastructure connections

### Phase 4: Feature Development
1. Infrastructure complete - features now allowed
2. Create feature issues
3. Auto-draft PR creation
4. Agent assignment and development
5. Shared workflows handle CI/CD

### Feature-Driven Development Flow (After Infrastructure)
```
GitHub Issue → Planning → Agent Assignment → Development → Testing → Deployment → Monitoring
```

### Infrastructure-First Approach
Agents MUST verify prerequisites before proceeding:
- Check design system exists before creating components
- Verify database schema before API development
- Confirm test framework setup before writing tests
- Validate deployment configuration before building



### 4. Parallel Development Coordination
- Git worktrees isolate feature development
- Hooks coordinate between parallel instances
- Automatic conflict detection and resolution
- Safe integration of concurrent work streams

### 5. Quality Gates Enforcement
Every progression through the lifecycle includes:
- **Code Quality**: Linting, formatting, type checking
- **Security**: Dependency scanning, secret detection
- **Testing**: Unit (80%+ coverage), integration, E2E
- **Performance**: Load testing, benchmarking
- **Accessibility**: WCAG 2.1 AA compliance

## Implementation Requirements

### Command Creation Standards
```markdown
---
allowed-tools: Read, Edit, Write, Bash, Glob, Grep
argument-hint: [feature-name] [priority]
description: Add new feature to existing project with full lifecycle automation
---

# Command Implementation
1. Extract feature requirements from input
2. Analyze existing codebase for integration points
3. Create GitHub issue with acceptance criteria
4. Route to appropriate specialist agent
5. Monitor progress via hooks
6. Coordinate quality gates
7. Trigger deployment when ready

# GitHub Integration
- Use GitHub MCP servers for all GitHub operations
- Maintain bidirectional sync with project boards
- Update issue status based on development progress
- Create PR automatically when feature complete

# Error Handling
- Graceful degradation if external services unavailable
- Rollback mechanisms for failed operations
- Clear error messages with recovery suggestions
```

### Agent Creation Standards
```markdown
---
name: frontend-specialist
description: React/UI development specialist with design system integration
tools: Read, Edit, Write, MultiEdit, Bash
---

# Agent Responsibilities
You are a frontend specialist working within the SynapseAI development system.

## Pre-Work Verification
Before starting any work, verify:
- Design system documentation exists: !`test -f docs/DESIGN_SYSTEM.md`
- Component library structure: !`test -d src/components`
- Testing framework configured: !`test -f jest.config.js`

## MCP Server Integration
You have access to:
- Design System MCP: Component specifications, design tokens
- GitHub Core MCP: Issue updates, PR creation
- Quality MCP: Testing, validation, performance checks

## Work Process
1. Extract acceptance criteria from GitHub issue
2. Analyze existing components for reuse opportunities
3. Implement following design system standards
4. Create comprehensive tests (unit + integration)
5. Update documentation automatically
6. Coordinate with backend-specialist if API changes needed

## Handoff Protocol
- Update GitHub issue with completion status
- Trigger appropriate hooks for next workflow step
- Provide clear documentation for testing/review
```

### Hook Creation Standards
```python
#!/usr/bin/env python3
"""
SubagentStop hook for GitHub project synchronization
Coordinates between GitHub Core and Projects MCP servers
"""
import json
import sys
import requests
from datetime import datetime

class MCPClient:
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
        }

    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        request_data = {
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments}
        }

        response = requests.post(
            f"{self.base_url}/mcp",
            json=request_data,
            headers=self.headers,
            timeout=30
        )

        return {
            "success": response.status_code == 200,
            "data": response.json() if response.status_code == 200 else None,
            "error": response.text if response.status_code != 200 else None
        }

def extract_context(hook_data: dict) -> dict:
    """Extract relevant context from hook data"""
    return {
        "session_id": hook_data.get("session_id"),
        "agent_type": determine_agent_type(hook_data),
        "issue_number": extract_issue_number(hook_data),
        "completion_status": analyze_completion(hook_data)
    }

def coordinate_github_updates(context: dict) -> dict:
    """Coordinate updates across GitHub Core and Projects MCP servers"""

    # Initialize MCP clients
    github_core = MCPClient(
        "https://mcp-github.yourdomain.com",
        os.getenv("GITHUB_TOKEN")
    )
    github_projects = MCPClient(
        "https://mcp-github-projects.yourdomain.com",
        os.getenv("GITHUB_TOKEN")
    )

    results = {}

    # Update issue via Core MCP
    results["issue_update"] = github_core.call_tool("update_issue", {
        "issue_number": context["issue_number"],
        "labels": [f"completed-by-{context['agent_type']}"],
        "assignee": determine_next_assignee(context),
        "comment": f"🤖 {context['agent_type']} completed their work"
    })

    # Update project board via Projects MCP
    results["project_update"] = github_projects.call_tool("update_project_item", {
        "issue_number": context["issue_number"],
        "status": determine_next_status(context),
        "custom_fields": {
            "Agent": context["agent_type"],
            "Completion": "100%",
            "Last Updated": datetime.now().isoformat()
        }
    })

    return results

try:
    hook_data = json.load(sys.stdin)
    context = extract_context(hook_data)
    results = coordinate_github_updates(context)

    # Check for failures
    failed_operations = [k for k, v in results.items() if not v["success"]]

    if failed_operations:
        error_msg = f"Failed operations: {', '.join(failed_operations)}"
        print(error_msg, file=sys.stderr)
        sys.exit(2)  # Block with feedback to Claude
    else:
        print(f"Successfully coordinated: {list(results.keys())}")
        sys.exit(0)

except Exception as e:
    print(f"Hook execution error: {e}", file=sys.stderr)
    sys.exit(1)
```

## GitHub Integration Patterns

### Issue Lifecycle Management
1. **Creation**: Via `/plan` or `/feature-add` commands
2. **Labeling**: Automatic routing labels based on content analysis
3. **Assignment**: Agents assigned based on labels and current workload
4. **Progress Tracking**: Real-time updates via hooks
5. **Completion**: Automatic status updates and next step triggers

### Project Board Automation
- Issues automatically added to appropriate project
- Custom fields updated in real-time
- Status changes trigger workflow progressions
- Dependencies tracked and enforced
- Sprint/milestone automation

### Deployment Coordination
- GitHub Actions triggered by hooks
- Multi-platform deployment (Vercel + DigitalOcean)
- Environment-specific configurations
- Rollback capabilities
- Health monitoring integration

## Modular Development Strategy

### Specialized Development Chats
Build framework components in focused conversations:

1. **Commands Chat**: Orchestration commands development
2. **Agents Chat**: Specialized agent creation and coordination
3. **Hooks Chat**: Real-time automation and synchronization
4. **Testing Chat**: Quality assurance and validation systems
5. **GitHub Chat**: GitHub workflow and project board automation
6. **MCP Chat**: External service integration and API management
7. **Git Chat**: Version control and branching strategies
8. **Documentation Chat**: System documentation and user guides

### Cross-Reference Approach
Each chat maintains detailed artifacts while referencing core concepts:
- **Commands** reference agent capabilities and hook coordination
- **Agents** reference hook integration and MCP service access
- **Hooks** reference GitHub workflows and MCP endpoints
- **All components** reference project context and established patterns

### Documentation Requirements
Every component must include:
- **Clear relationship** to overall framework architecture
- **Integration points** with other framework components
- **Reference to project context** and specific requirements
- **Consistency with established patterns** and conventions
- **Extension points** for project-specific customization

## Quality Standards

### Framework Integration
- **Modular Design**: Components work independently when needed
- **Seamless Coordination**: Components integrate without conflicts
- **Pattern Consistency**: All parts follow established approaches
- **Documentation Alignment**: Clear reference to project knowledge
- **Extensibility**: Easy addition of new capabilities

### Project Awareness
- **Context Understanding**: Comprehends current project needs and structure
- **Pattern Adherence**: Uses documented Claude Code approaches
- **Knowledge Integration**: Builds on existing project documentation
- **Workflow Compatibility**: Fits established development processes
- **Standard Compliance**: Follows project-specific requirements and conventions

This framework enables any development project through intelligent automation while maintaining full consistency with Claude Code patterns and project-specific requirements.
