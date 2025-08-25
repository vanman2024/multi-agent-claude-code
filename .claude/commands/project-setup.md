---
allowed-tools: mcp__github(*), mcp__supabase(*), mcp__filesystem(*), Bash(*), Read(*), Write(*), Edit(*), Task(*), TodoWrite(*)
description: Intelligently guide through project setup with conversation, recommendations, and documentation generation
argument-hint: [optional: project-name or project-type]
---

# Project Setup

## Context
- Current directory: !`pwd`
- Git status: !`git branch --show-current`

## Your Task

When user runs `/project-setup $ARGUMENTS`, guide them through an intelligent project setup process.

### Phase 1: Discovery Conversation

Start with understanding the project vision:

1. **Ask about the project**:
   - "What are we building? Give me the elevator pitch."
   - "Who is this for? (individual developers, teams, enterprises?)"
   - "What specific problem are you solving?"

2. **Classify project type** based on their answers:
   - SaaS Application (full stack with auth, payments)
   - Integration/Connector (connects systems)
   - Internal Tool (team utility)
   - AI Agent/Bot (LLM-powered)
   - API Service (backend only)
   - Static Site (marketing/docs)

3. **Understand constraints**:
   - "How many users do you expect? (10, 1K, 10K, 100K+)"
   - "What's your monthly infrastructure budget? ($0-100, $100-500, $500+)"
   - "Timeline for MVP? (weeks vs months)"
   - "Team size and expertise?"

### Phase 2: Technical Stack Recommendations (BUY VS BUILD)

Based on Phase 1, recommend a stack emphasizing EXISTING SOLUTIONS:

1. **Core Framework & Hosting (STANDARD STACK)**
   - Frontend: Next.js 14 → **ALWAYS Vercel** (no alternatives)
   - Backend: FastAPI/Express → **ALWAYS DigitalOcean Droplets** (for all testing)
   - Webhooks/Testing: **ALWAYS Postman + DigitalOcean**
   - These are NON-NEGOTIABLE for consistency

2. **CRITICAL: Services to BUY, Not Build**
   
   **Always ask**: "Before we build X, what existing service solves this?"
   
   - **Authentication**: NEVER build custom auth
     - Supabase Auth (free tier, includes social login)
     - Auth0, Clerk, or Firebase Auth
     - Time saved: 3-4 weeks
   
   - **Payments**: NEVER build payment processing
     - Stripe (subscriptions, invoices, portal)
     - Paddle (handles taxes globally)
     - Time saved: 6-8 weeks
   
   - **Email**: NEVER build email infrastructure
     - Resend, SendGrid, or Postmark
     - Time saved: 1-2 weeks
   
   - **File Storage**: NEVER build file handling
     - Supabase Storage, S3, or Cloudinary
     - Time saved: 2-3 weeks
   
   - **Database**: Use managed services
     - Supabase (PostgreSQL + extras)
     - PlanetScale, Neon, or Railway
     - Time saved: Infinite (maintenance)

3. **Calculate Time & Cost Savings**
   - "Using Supabase Auth saves 3 weeks ($12,000 dev time)"
   - "Stripe costs 2.9% but saves 2 months of development"
   - Show total: "External services: $200/month, Time saved: 4 months"

### Phase 3: External Resources & GitHub Setup

Ask about existing resources:
- "Do you have existing code to migrate?"
- "Any templates you'd like to use? (I can search Vercel templates)"
- "Existing architecture docs or design systems?"
- "API specifications to follow?"

GitHub project template (using default template):
- Default template: Project #13 from vanman2024
- Ask: "What should we name the new project board? (default: PROJECT_NAME Board)"
- Ask: "Target organization/owner? (default: vanman2024)"

### Phase 4: Generate Documentation

Create the foundational documents using templates and guides:

1. **ARCHITECTURE.md**
   - Read guide: @.claude/templates/guides/architecture-guide.md (structure reference)
   - Read example: @.claude/templates/architecture.md (full example)
   - Fill in decisions from conversation
   - Lock in ports (3002 frontend, 8891 backend)
   - Document the "why" behind each choice
   - Adapt sections based on project type (skip database for API-only)
   - Write to: docs/ARCHITECTURE.md

2. **INFRASTRUCTURE.md**
   - Read guide: @.claude/templates/guides/infrastructure-guide.md (what to include)
   - Read example: @.claude/templates/infrastructure.md (full example)
   - Check off services based on project type
   - Calculate monthly costs
   - Mark implementation priorities
   - Only include relevant services (no payments for internal tools)
   - Write to: docs/INFRASTRUCTURE.md

3. **FEATURES.md** (if features discussed)
   - List MVP features appropriate to project type
   - Create phase plan
   - Set priorities
   - Write to: docs/FEATURES.md

### Phase 5: Project Scaffolding

1. **Create directory structure**:
   ```bash
   mkdir -p frontend backend database docs .github .claude scripts/setup .claude/templates/guides
   ```

2. **Initialize configuration files**:
   - Create package.json with correct ports
   - Create requirements.txt or pyproject.toml
   - Create .env.example
   - Create .gitignore

3. **Setup GitHub Integration**:
   
   Using GitHub CLI (gh):
   ```bash
   # Create repository (if needed)
   gh repo create PROJECT_NAME --private
   
   # COPY project board from template #13
   gh project copy 13 \
     --source-owner vanman2024 \
     --target-owner vanman2024 \
     --title "PROJECT_NAME Board"
   
   # Get the new project number from output
   # Update workflow files with new project number
   
   # Create initial issue
   gh issue create --title "[SETUP] Project initialization" --body "Set up PROJECT_NAME"
   ```
   
   Using GitHub MCP for issue details:
   - Use mcp__github__create_issue for detailed issue creation
   - Use mcp__github__update_issue to add labels and assignees

### Phase 6: Future Agent Integration (Placeholders)

When these agents are built, integrate them:

```
### Step 1: Template Research (Future)
Use Task tool with:
- subagent_type: general-purpose
- description: Find relevant project templates
- prompt: Search for $PROJECT_TYPE templates with $TECH_STACK

### Step 2: Workflow Generation (Future)
Use Task tool with:
- subagent_type: general-purpose  
- description: Create GitHub Actions workflows
- prompt: Generate CI/CD for $PROJECT_TYPE using $TECH_STACK

### Step 3: Documentation Enhancement (Future)
Use Task tool with:
- subagent_type: general-purpose
- description: Enhance project documentation
- prompt: Add detailed setup instructions for $PROJECT_TYPE
```

## Example Conversation Flow

```
User: /project-setup

You: Let's set up your project! First, tell me - what are we building? 
     Give me the elevator pitch.

User: I want to build a tool that helps developers track their API usage

You: Interesting! A developer tool for API monitoring. Who's the target user - 
     individual developers, teams, or enterprises? And what specific problem 
     are you solving that existing tools don't address?

[Continue conversation...]

You: Based on our discussion, here's my BUY vs BUILD recommendation:

     **Services to BUY (not build):**
     ✓ Supabase Auth - saves 3 weeks, free tier
     ✓ Stripe billing - saves 6 weeks, handles taxes
     ✓ Resend email - saves 1 week, great deliverability
     ✓ Supabase database - managed, includes realtime
     
     **What we'll BUILD:**
     - API usage tracking logic (your core value)
     - Custom dashboard (your differentiator)
     
     Total: $150/month in services, saves 10+ weeks of development
     
     Any concerns or preferences?

[After confirmation, generate docs and structure]

You: ✅ Project setup complete! 
     - Architecture documented in docs/ARCHITECTURE.md
     - Infrastructure checklist in docs/INFRASTRUCTURE.md
     - Repository created: github.com/user/project
     - First issue created: #1
     
     Next steps:
     1. cd frontend && npm install
     2. Set up environment variables
     3. Start development!
```

## Important Notes

- **ALWAYS emphasize BUY vs BUILD** - Calculate time/cost savings
- **ALWAYS use Vercel for frontend hosting** (no exceptions)
- **ALWAYS use DigitalOcean Droplets for backend/testing** (no exceptions)
- **ALWAYS use Postman for webhook testing** (standard tool)
- **Reference CLAUDE.md** for project configuration when it exists
- Be conversational and explain reasoning
- Allow users to override features BUT NOT hosting choices
- Always use port 3002 for frontend, 8891 for backend
- List specific services with free tiers when possible
- Show total development time saved by using external services
- Default to Supabase for most projects
- Use TodoWrite to track setup progress
- Create actual files and directories
- Use gh CLI for project board operations
- Use mcp__github for issue operations