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

### Phase 0: Load Personal Configuration

Check for personal config:
```bash
if [ -f "$HOME/.claude-code/personal-config.json" ]; then
  echo "🔑 Personal config found! Would you like to use your saved API keys? (y/n)"
  # If yes, run: ./scripts/utilities/load-personal-config.sh
  echo "✅ Loaded API keys from personal config"
else
  echo "💡 Tip: Run ./scripts/utilities/setup-personal-config.sh to save your API keys for reuse"
  echo "For now, copy .env.example to .env and add your keys manually"
fi
```

### Phase 1: Discovery Conversation

Start with understanding the project vision:

#### Step 1A: Initial Assessment
Ask: "Are you starting a brand new project or adding to existing code?"

#### Step 1B: Gather ALL Reference Materials
Ask: "Before we dive into details, let me gather any existing materials. Do you have:
- Screenshots or mockups to share?
- Documentation or requirements?
- API documentation or Postman collections?
- OpenAPI/Swagger specs?
- Similar projects or examples?
- Competitor sites to reference?
- Existing code to review?
- URLs of services you want to integrate with?

Please provide paths, URLs, or paste any materials you have, or say 'none' if starting from scratch."

<thinking>
Wait for response, then analyze EVERYTHING:
- If materials provided, read and analyze ALL of them
- If existing code mentioned, use Glob to explore structure
- If screenshots provided, understand the UI vision
- If URLs provided, use WebFetch to examine sites/APIs
- If competitor sites mentioned, analyze interfaces
- If API docs provided, understand integration capabilities
- If Postman collections exist, examine API structures
- Build comprehensive mental model from all materials
- Only proceed after gathering and analyzing everything
</thinking>

#### Step 1C: Core Discovery Questions
Ask all together: 
"Tell me about your project:
- What specific problem exists today?
- Who has this problem? (individual developers, teams, enterprises?)
- How painful is it (1-10)?
- What do they use today?
- Why doesn't it work?"

#### Step 1D: Vision & Solution
Ask: "Describe your ideal solution:
- What would it do?
- What are must-have features?
- What makes it 10x better than existing options?"

#### Step 1E: Classify Project Type
Based on their answers, classify as:
- SaaS Application (full stack with auth, payments)
- Integration/Connector (connects systems)
- Internal Tool (team utility)
- AI Agent/Bot (LLM-powered)
- API Service (backend only)
- Static Site (marketing/docs)

#### Step 1F: Business & Technical Context
Ask all together:
"Tell me about the business side:
- B2B or B2C?
- How will it make money?
- What's the pricing model?
- Expected users? (10, 1K, 10K, 100K+)
- Monthly infrastructure budget? ($0-100, $100-500, $500+)
- Timeline for MVP? (weeks vs months)
- Team size and expertise?
- What should we call this project?"

<thinking>
If no project name provided, generate 3 options based on everything learned
</thinking>

### Phase 2: Technical Stack Recommendations (BUY VS BUILD)

Based on Phase 1, recommend a stack emphasizing EXISTING SOLUTIONS:

1. **Core Framework & Hosting (STANDARD STACK)**
   - Frontend: Next.js 14 → **ALWAYS Vercel** (no alternatives)
   - Backend: FastAPI/Express → **ALWAYS Vercel** (serverless functions or edge)
   - Full Application: **Deploy entire app on Vercel** (frontend + backend)
   - Webhooks/Testing: **ALWAYS Postman for API testing**
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

## ⚠️ CHECKPOINT: DO NOT PROCEED UNTIL YOU HAVE ALL INFORMATION

**CRITICAL**: You CANNOT create documentation until you have gathered:
- ✅ Complete understanding of existing materials (Phase 1B)
- ✅ Clear problem definition and solution vision (Phase 1C-D)
- ✅ Specific tech stack decisions (Phase 2)
- ✅ Business model and target market (Phase 1F)
- ✅ Project name (Phase 1F)
- ✅ External resources and templates (Phase 3)

<thinking>
Review all information gathered:
- Verify every documentation section can be filled with specific details
- Ensure nothing is vague or incomplete
- Check that tech stack is fully decided
- Confirm project name and business model are clear
- If anything is missing, GO BACK and ask more questions
</thinking>

**If any of these are incomplete, GO BACK and ask more questions.**

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
- **ALWAYS use Vercel for full application deployment** (frontend + backend, no exceptions)
- **ALWAYS use Postman for API testing** (standard tool)
- **ALWAYS gather ALL materials BEFORE proceeding** (Phase 1B is critical)
- **Reference CLAUDE.md** for project configuration when it exists
- Be conversational and explain reasoning
- Allow users to override features BUT NOT hosting choices
- Always use port 3002 for frontend, 8891 for backend (local development)
- List specific services with free tiers when possible
- Show total development time saved by using external services
- Default to Supabase for most projects (auth, database, storage)
- Use TodoWrite to track setup progress
- Create actual files and directories
- Use gh CLI for project board operations
- Use mcp__github for issue operations
- Use <thinking> tags for analysis between conversation steps
- Never proceed past checkpoint without complete information