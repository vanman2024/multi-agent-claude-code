# Project Context - Multi-Agent Development Framework

## Current Project State
**Status**: Active Development - MVP Phase  
**Last Updated**: 2024-12-07  
**Current Goals**: Building Multi-Agent AI System with MCP Server Integration  

## High-Level Overview
Multi-Agent Development Framework that orchestrates AI agents, human developers, and automated workflows to achieve 10x productivity gains in software development. GitHub serves as the central data layer and coordination hub, with Claude Code CLI as the primary orchestrator and GitHub Copilot as an autonomous development agent.

## Current Milestone: MVP
Building core multi-agent system with specialized AI model delegation to optimize Claude Code usage and leverage free tier models effectively.

### Active Features in Development
- **MCP Server Integration**: Together AI, Gemini 1.5 Pro, HuggingFace Inference servers
- **Task Delegation System**: Automatic routing of tasks to appropriate AI models
- **File Access System**: Enhanced file read/write capabilities for all MCP servers
- **Project Context Sharing**: Centralized context management across all agents

## Architecture Overview
- **GitHub**: Central data layer and coordination hub
- **Claude Code CLI**: Primary orchestrator for complex tasks
- **GitHub Copilot**: Autonomous agent for simple tasks (Complexity ≤2, Size ≤S)
- **MCP Servers**: Specialized AI model interfaces with file access
- **Project Templates**: Standardized framework for rapid project setup

## Technology Stack
- **Framework Type**: Documentation and template repository
- **Primary Language**: Markdown (documentation), Shell scripts (automation)
- **Core Tools**: Claude Code CLI, GitHub CLI, MCP Protocol
- **Agent Architecture**: Multi-agent with automatic task routing

## Component Status
- ✅ **GitHub Integration**: Complete via MCP server
- ✅ **Agent Assignment**: Automatic routing based on complexity/size
- ✅ **Documentation Framework**: Templates and guides established
- 🔄 **MCP Server Extension**: In progress - adding specialized AI models
- 🔄 **File Access System**: In development
- 📋 **Task Delegation**: Planned

## Free Tier Limits (Target Usage)
- **Together AI**: 3000 requests/month (complex code generation)
- **Gemini 1.5 Pro**: 1500 requests/day (testing & documentation) 
- **HuggingFace**: 30k characters/month (specialized models)
- **Claude Code**: Reduced usage via delegation (primary orchestrator only)

## Key Directories
- `/docs/` - Framework documentation and architecture guides
- `/.github/workflows/` - CI/CD pipelines and automation workflows
- `/.claude/commands/` - Claude Code slash commands
- `/templates/` - Issue and feature specification templates
- `/scripts/` - Automation and utility scripts

## Current Sprint Focus
1. Build new MCP servers with file access
2. Implement project context sharing system  
3. Create task delegation commands
4. Test file operations and API integrations

## Dependencies & Blockers
- **API Keys Required**: Together AI, HuggingFace (for new MCP servers)
- **Prerequisites**: Node.js/Python for MCP server implementations
- **Integration Points**: Existing MCP protocol structure

## Success Metrics
- 60% reduction in Claude Code usage
- <500ms response time for all MCP servers
- 90% task delegation success rate
- Zero file corruption incidents

---
*This file is automatically updated by the multi-agent system to maintain current project state visibility across all agents.*