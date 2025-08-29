# Project Setup Slash Command Documentation

## Command: `/project-setup`

### Purpose
Intelligently guide users through project initialization with a conversational approach, gathering requirements, making recommendations, and setting up the foundational architecture and infrastructure documentation.

---

## How It Should Work

### Phase 1: Discovery Conversation
The command initiates an interactive dialogue to understand:

1. **Project Vision**
   - "What are we building?" (open-ended)
   - "Who is this for?" (target users)
   - "What problem does it solve?"

2. **Project Type Classification**
   - Based on description, suggest type:
     - SaaS Application (full stack with auth, payments)
     - Integration/Connector (connects systems)
     - Internal Tool (team utility)
     - AI Agent/Bot (LLM-powered)
     - API Service (backend only)
     - Static Site (marketing/docs)
   - Confirm or adjust based on user feedback

3. **Scale & Constraints**
   - Expected users (10, 1K, 10K, 100K+)
   - Budget constraints ($0-100, $100-500, $500+/month)
   - Timeline (MVP in weeks vs months)
   - Team size

### Phase 2: Technical Recommendations
Based on Phase 1, Claude suggests a stack:

1. **Frontend Framework**
   - Analyze requirements
   - Suggest best fit (Next.js for SaaS, Vite for lightweight, etc.)
   - Explain WHY this choice
   - Allow override with discussion of tradeoffs

2. **Backend Framework**
   - Match to team expertise and requirements
   - FastAPI for Python teams, Express for Node teams
   - Discuss scaling considerations

3. **Database & Infrastructure**
   - Default to Supabase for most cases
   - Explain included features (auth, storage, realtime)
   - Discuss alternatives if specific needs

### Phase 3: External Resources & Templates
Claude asks about existing resources:

1. **Existing Codebases**
   - "Do you have any existing code to migrate?"
   - "Any templates you'd like to use as a starting point?"

2. **External Templates**
   - Search for relevant Vercel templates
   - Suggest GitHub starter repos
   - Recommend component libraries

3. **Documentation References**
   - "Any existing architecture docs?"
   - "Design system or brand guidelines?"
   - "API specifications to follow?"

### Phase 4: Document Generation
Create foundational documents:

1. **ARCHITECTURE.md**
   - Fill in all decisions from conversation
   - Lock in ports (3002 frontend, 8891 backend)
   - Document the "why" behind each choice
   - Set non-negotiable rules

2. **INFRASTRUCTURE.md**
   - Check off services needed based on project type
   - Calculate estimated monthly costs
   - Provide integration locations
   - Mark implementation priorities

3. **FEATURES.md** (optional, if discussed)
   - List MVP features from conversation
   - Create phase plan
   - Set priorities

### Phase 5: Project Scaffolding
Based on decisions:

1. **Create Directory Structure**
   ```
   project/
   ├── frontend/         # If needed
   ├── backend/          # If needed
   ├── database/         # Migrations/seeds
   ├── docs/            # Architecture, Infrastructure, Features
   ├── .github/         # Workflows
   ├── .claude/         # Claude configuration
   └── scripts/         # Setup scripts
   ```

2. **Initialize Configuration**
   - package.json with correct scripts
   - requirements.txt/pyproject.toml
   - .env.example with needed variables
   - .gitignore

3. **Setup GitHub Integration**
   - Create initial issue for project setup
   - Set up project board structure
   - Configure labels

---

## Conversational Flow Example

```
User: /project-setup

Claude: Let's set up your project! First, tell me - what are we building? 
        Give me the elevator pitch.

User: I want to build a tool that helps developers track their API usage 
      across different services

Claude: Interesting! A developer tool for API monitoring. Who's the target user - 
        individual developers, teams, or enterprises? And what specific problem 
        are you solving that existing tools don't address?

User: Individual developers and small teams who use multiple APIs but don't 
      have enterprise monitoring budgets

Claude: Got it. This sounds like a SaaS application with:
        - Dashboard for visualizing API usage
        - Multi-service integration
        - Affordable pricing for individuals
        
        How many users do you expect in the first year? And what's your 
        monthly budget for infrastructure?

User: Maybe 1000 users first year, trying to keep it under $100/month

Claude: Perfect. Based on our discussion, here's what I recommend:

        **Frontend**: Next.js 14 (great for dashboards, SEO for marketing pages)
        **Backend**: FastAPI (fast, great for handling API data)
        **Database**: Supabase (includes auth, very cost-effective)
        **Hosting**: Vercel (frontend) + DigitalOcean (backend) ~$48/month
        
        This gives you room to grow. Any concerns or would you prefer 
        different technologies? Do you have more experience with any 
        particular stack?

User: I'm more comfortable with Node/TypeScript everywhere

Claude: Let's adjust then:
        
        **Frontend**: Next.js 14 (TypeScript)
        **Backend**: Express with TypeScript (or NestJS for more structure)
        **Database**: Still Supabase (works great with Node)
        
        This keeps everything in TypeScript. NestJS would give you more 
        structure but has a learning curve. Express is simpler to start.
        Which sounds better for your needs?

User: Express is fine, keep it simple

Claude: Great choice. Now, do you have any existing code, templates, or 
        documentation we should reference? Any design system you want to follow?

User: No existing code, but I like the Vercel analytics dashboard design

Claude: I'll note that for the UI inspiration. Let me create your project 
        structure and documentation now...

        [Creates ARCHITECTURE.md with all decisions]
        [Creates INFRASTRUCTURE.md with SaaS checklist]
        [Creates initial directory structure]
        
        ✅ Project setup complete! Your architecture is documented in 
        docs/ARCHITECTURE.md. These decisions are now locked in.
        
        Next steps:
        1. Run: gh repo create api-usage-tracker --private
        2. Your first issue is ready: gh issue create --title "[FEATURE] User 
           dashboard" --body "Create main dashboard for API usage visualization"
        3. Start development: cd frontend && npm install && npm run dev
```

---

## Implementation Requirements

### The slash command should:

1. **Be Conversational**
   - Ask follow-up questions
   - Clarify ambiguities
   - Explain recommendations

2. **Be Intelligent**
   - Make smart defaults based on project type
   - Suggest optimal tech stacks
   - Consider budget and scale

3. **Be Flexible**
   - Allow overrides of any suggestion
   - Explain tradeoffs
   - Accommodate existing constraints

4. **Create Real Artifacts**
   - Generate actual documentation files
   - Create directory structure
   - Set up configuration files

5. **Integrate with Workflow**
   - Create first GitHub issue
   - Set up project board
   - Configure automation

---

## Template File Locations

- Architecture Template: `/home/gotime2022/Projects/mcp-kernel-new/.claude/templates/architecture.md`
- Infrastructure Template: `/home/gotime2022/Projects/mcp-kernel-new/.claude/templates/infrastructure.md`
- Feature Card Template: `/home/gotime2022/Projects/mcp-kernel-new/.claude/templates/feature-specification-card.md`

---

## Key Principles

1. **Guide, Don't Dictate** - Make recommendations but allow flexibility
2. **Explain Everything** - Users should understand WHY each choice
3. **Start Simple** - Can always add complexity later
4. **Lock Foundations** - Some decisions (ports, core stack) shouldn't change
5. **Buy vs Build** - Always prefer existing solutions for solved problems

---

## Success Metrics

A successful project setup should:
- Take 5-10 minutes of conversation
- Produce clear, complete documentation
- Make appropriate technical choices
- Set up immediate next actions
- Feel collaborative, not prescriptive