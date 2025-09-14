---
allowed-tools: mcp__github(*), mcp__supabase(*), mcp__filesystem(*), Bash(*), Read(*), Write(*), Edit(*), Task(*), TodoWrite(*)
description: Intelligently guide through project setup with conversation, recommendations, and documentation generation
argument-hint: [optional: project-name or project-type]
---

# Project Setup

<!--
WHEN TO USE THIS COMMAND:
- Starting a brand new project from scratch
- Need to gather requirements and make tech decisions
- Want to create foundation documentation (ARCHITECTURE, INFRASTRUCTURE, FEATURES)
- Setting up GitHub repo and project board
- Beginning of the development workflow

WHEN NOT TO USE:
- Project already has documentation
- Just need to update existing setup
- Only need test generation (use /test:generate)
- Only need implementation plan (use /plan:generate)

WORKFLOW (Complete Development Cycle):
1. /project-setup         # Interactive discovery & create PROJECT_PLAN.md vision
2. /plan:generate        # Generate detailed docs from vision
3. /test:generate        # Generate comprehensive test suites
4. /create-issue         # Start creating work items
5. /work #1             # Begin implementation

WHAT THIS CREATES:
- docs/PROJECT_PLAN.md  # High-level vision and roadmap (north star)
- GitHub repository     # If requested
- Project board         # From template #13
- Basic folder structure # frontend/, backend/, etc.

KEY PRINCIPLES:
- BUY vs BUILD emphasis (use existing services)
- Vercel for deployment (non-negotiable)
- Postman for API testing (standard)
- Supabase for auth/database (recommended)
- Port 3002 (frontend), 8891 (backend)
-->

## Context
- Current directory: !`pwd`
- Git status: !`git branch --show-current`

## Your Task

When user runs `/project-setup $ARGUMENTS`, guide them through an intelligent project setup process.

### Mode Detection
Parse arguments for flags:
- `--from-template` or `--from-spec-kit`: Starting from spec-kit or other template
- `--from-existing`: Already have local code, need GitHub integration
- `--greenfield` or no flag: Current behavior (fresh start)
- `--local-only`: Skip GitHub creation, work locally like spec-kit

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

**Mode-Specific Handling:**

**Auto-detect spec-kit initialization:**
```bash
# Check if this is a fresh spec-kit project (no actual code yet)
if [ -d "memory" ] && [ -d "scripts" ] && [ -d "templates" ] && [ ! -d "specs" ]; then
  echo "✅ Spec-kit initialized! Let's create your project vision."
  # Continue with normal flow to create PROJECT_PLAN.md
elif [ -d "specs" ] && [ -f "specs/*/spec.md" ]; then
  echo "📋 Found existing specifications."
  # Ask if they want to update or continue
fi
```

**For --from-template or --from-spec-kit:**
- Check for `.specify/` directory or `memory/constitution.md`
- If found: "I see you're using spec-kit! Let me integrate with that."
- Read: `.specify/spec.md`, `.specify/plan.md`, `memory/constitution.md`
- Convert spec-kit format to our PROJECT_PLAN.md
- Generate CLAUDE.md from constitution.md
- Skip to Phase 2

**For --from-existing:**
- Analyze: "Let me analyze your existing codebase..."
- Use Glob to find key files (package.json, README, etc.)
- Generate PROJECT_PLAN.md from discovered structure
- Ask: "Ready to create GitHub repo for this project?"

**For --local-only:**
- Note: "Working in local-only mode, no GitHub integration"
- Focus on specs and local development

**Default flow:**

Start with understanding the project vision:

#### Step 1A: Initial Assessment
Check project state:
- If only spec-kit scaffolding exists (memory/, scripts/, templates/): "I see you've initialized spec-kit. Let's define your project vision!"
- If specs/ directory exists with content: "I see you have existing specifications. Would you like to update the vision or continue with implementation?"
- If actual project code exists: "This appears to be an existing project. Would you like to update PROJECT_PLAN.md or add new features?"
- Otherwise: "Let's create your project vision!"

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

### Phase 4: Generate Spec-Kit Prompt

Create a structured prompt that can be passed to spec-kit's `/specify` command:

**Prompt Structure**:
```
Build a [PROJECT_TYPE] called "[PROJECT_NAME]" that [CORE_PROBLEM_SOLUTION].

## Context
- Target users: [USER_DESCRIPTION]
- Pain point: [SPECIFIC_PROBLEM] (severity: [1-10])
- Current solutions: [EXISTING_OPTIONS] 
- Why they fail: [SOLUTION_GAPS]

## Solution Vision
- Core value: [UNIQUE_VALUE_PROPOSITION]
- Key differentiator: [WHAT_MAKES_IT_10X_BETTER]
- Must-have features: [ESSENTIAL_FEATURES_LIST]
- Business model: [REVENUE_MODEL]

## Technical Constraints
- Tech stack preferences: [STACK_DECISIONS]
- External services to use: [BUY_VS_BUILD_DECISIONS]
- Scale expectations: [USER_COUNT_TIMELINE]
- Budget constraints: [INFRASTRUCTURE_BUDGET]

## Success Criteria
- Primary metric: [KEY_SUCCESS_METRIC]
- Target outcomes: [SPECIFIC_GOALS]

Please create detailed functional specifications for this application.
```

**Output the prompt to console** for easy copying to spec-kit:
```bash
echo "=================================="
echo "🎯 SPEC-KIT PROMPT GENERATED"
echo "=================================="
echo ""
echo "[Generated prompt above]"
echo ""
echo "Next step: Copy this prompt and run:"
echo "/specify \"[paste the prompt here]\""
echo "=================================="
```

### Phase 4.5: Spec-Kit Integration (if detected)

**Check for spec-kit:**
```bash
if [ -d "memory" ] && [ -d "scripts" ] && [ -d "templates" ]; then
  echo "✅ Spec-kit detected! Running /specify with generated prompt..."
  echo ""
  # Auto-run the /specify command with the complete prompt
  /specify "[the complete generated prompt]"
  echo ""
  echo "🎉 Project setup complete with spec-kit!"
  echo "Next steps:"
  echo "1. Review generated specifications in specs/"
  echo "2. Run /work to start implementation"
  exit 0
else
  echo "💡 Spec-kit not detected. Continuing with standard GitHub setup..."
fi
```

### Phase 5: GitHub Repository Creation

Ask user about GitHub setup:
```bash
echo "🐙 GitHub Setup"
echo "==============="
echo "Do you want to create a GitHub repository? (y/n)"
```

If yes, proceed with GitHub creation:
```bash
# Get project details
echo "Repository name (default: [PROJECT_NAME_SLUGIFIED]):"
read -r REPO_NAME
REPO_NAME=${REPO_NAME:-[PROJECT_NAME_SLUGIFIED]}

echo "Repository owner/organization (default: vanman2024):"
read -r REPO_OWNER
REPO_OWNER=${REPO_OWNER:-vanman2024}

echo "Make repository private? (y/n, default: y):"
read -r PRIVATE
PRIVATE=${PRIVATE:-y}

# Create repository
if [ "$PRIVATE" = "y" ]; then
  gh repo create $REPO_OWNER/$REPO_NAME --private --description "[Generated description from prompt]"
else
  gh repo create $REPO_OWNER/$REPO_NAME --public --description "[Generated description from prompt]"
fi

# Set up remote
git init
git remote add origin https://github.com/$REPO_OWNER/$REPO_NAME.git
git branch -M main

echo "✅ Repository created: https://github.com/$REPO_OWNER/$REPO_NAME"
```

### Phase 6: Project Board Creation

Copy project board from template:
```bash
echo "📋 Creating Project Board..."

# Copy project board from template #13
PROJECT_BOARD_TITLE="$REPO_NAME Board"
echo "Project board title (default: $PROJECT_BOARD_TITLE):"
read -r BOARD_TITLE
BOARD_TITLE=${BOARD_TITLE:-$PROJECT_BOARD_TITLE}

# Create project board
gh project copy 13 \
  --source-owner vanman2024 \
  --target-owner $REPO_OWNER \
  --title "$BOARD_TITLE"

echo "✅ Project board created: $BOARD_TITLE"
```

### Phase 7: Project Scaffolding

1. **Create directory structure**:
   ```bash
   mkdir -p frontend backend database docs .github .claude scripts/setup .claude/templates/guides .vscode
   ```

2. **Initialize configuration files**:
   - Create package.json with correct ports
   - Create requirements.txt or pyproject.toml
   - Create .env.example
   - Create .gitignore

3. **Copy VS Code settings from template**:
   ```bash
   # Copy VS Code settings that include Vim disabled and other dev settings
   cp /home/gotime2022/Projects/multi-agent-claude-code/.vscode/settings.json .vscode/settings.json
   echo "⚠️  IMPORTANT: Restart VS Code to apply new settings (Vim will be disabled)"
   ```

4. **Setup GitHub Integration**:
   
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

### Phase 6: Verify and Configure GitHub Integration

Check existing GitHub configuration and adjust for the project:

```bash
# 1. Check current GitHub remote
git remote -v

# 2. Verify project board exists
gh project list --owner vanman2024

# 3. Check if workflows need adjustment
ls -la .github/workflows/

# 4. Update project-specific settings if needed
# - Adjust workflow project numbers if different
# - Configure branch protection if needed
# - Set up environment secrets if required

echo "✅ GitHub integration verified and configured for $PROJECT_NAME"
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

[After confirmation, generate prompt]

You: 🎯 SPEC-KIT PROMPT GENERATED
     ==================================
     
     Build a developer tool called "API Usage Tracker" that helps developers 
     monitor and optimize their API consumption across multiple services.

     ## Context
     - Target users: Individual developers and small teams managing multiple APIs
     - Pain point: No unified view of API usage across services (severity: 8)
     - Current solutions: Manual spreadsheets, individual service dashboards
     - Why they fail: Fragmented data, no usage optimization insights

     ## Solution Vision
     - Core value: Unified API usage dashboard with cost optimization
     - Key differentiator: Predictive usage alerts and cost recommendations
     - Must-have features: Multi-service integration, usage alerts, cost tracking
     - Business model: Freemium SaaS ($0-49/month tiers)

     [... complete prompt ...]
     
     Next step: Copy this prompt and run:
     /specify "[paste the prompt here]"
     ==================================
```

## Important Notes

- **PRIMARY OUTPUT: Structured prompt for spec-kit** - Not documentation files
- **ALWAYS emphasize BUY vs BUILD** - Calculate time/cost savings
- **ALWAYS use Vercel for full application deployment** (frontend + backend, no exceptions)
- **ALWAYS use Postman for API testing** (standard tool)
- **ALWAYS gather ALL materials BEFORE proceeding** (Phase 1B is critical)
- **Generate prompt that spec-kit can consume** - Fill all template variables
- **Auto-run /specify if spec-kit detected** - Seamless integration
- Be conversational and explain reasoning
- Allow users to override features BUT NOT hosting choices
- Always use port 3002 for frontend, 8891 for backend (local development)
- List specific services with free tiers when possible
- Show total development time saved by using external services
- Default to Supabase for most projects (auth, database, storage)
- Use TodoWrite to track setup progress
- Create actual files and directories (if not using spec-kit)
- Use gh CLI for project board operations
- Use mcp__github for issue operations
- Use <thinking> tags for analysis between conversation steps
- Never proceed past checkpoint without complete information
- **Prompt must be copy-pasteable** - No placeholders left unfilled