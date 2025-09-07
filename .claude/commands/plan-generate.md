---
allowed-tools: Read(*), Write(*), TodoWrite(*), Bash(*), Glob(*)
description: Generate detailed technical documentation from PROJECT_PLAN.md vision
argument-hint: [--from-vision | --fresh-analysis] [domain]
---

# Generate Detailed Documentation

<!--
WHEN TO USE THIS COMMAND:
- After running /project-setup to create PROJECT_PLAN.md
- When you need detailed technical documentation
- To create ARCHITECTURE, INFRASTRUCTURE, FEATURES docs
- To expand the vision into actionable technical specs

WHEN NOT TO USE:
- Before /project-setup (no vision to work from)
- If detailed docs already exist and are current
- For creating the vision (use /project-setup)

FLAGS:
--from-vision   : Read PROJECT_PLAN.md vision (default)
--fresh-analysis: Analyze codebase without vision doc
--domain [type] : Specify business domain for better specs

WORKFLOW:
1. /project-setup        # Create PROJECT_PLAN.md vision
2. /plan:generate        # Create detailed tech docs
3. /test:generate        # Generate test suites
4. /create-issue         # Start creating work items
-->

## Context
- Current directory: !`pwd`
- Project files: !`ls -la docs/*.md 2>/dev/null | head -10`

## Your Task

When user runs `/plan:generate $ARGUMENTS`, create detailed technical documentation from the PROJECT_PLAN.md vision.

### Step 1: Analyze Project Vision

#### If `--from-vision` flag (default) OR PROJECT_PLAN.md exists:
Read the vision document to understand the project:

```bash
# Check for vision document
if [ -f "docs/PROJECT_PLAN.md" ]; then
  echo "✅ Found PROJECT_PLAN.md vision document"
else
  echo "⚠️ No PROJECT_PLAN.md found. Run /project-setup first!"
  exit 1
fi
```

Extract from PROJECT_PLAN.md:
- **Tech Stack**: Framework and service decisions
- **Core Features**: What needs to be built
- **Target Users**: Who we're building for
- **Business Model**: How it makes money
- **Roadmap**: Implementation phases

#### If `--fresh-analysis` OR no docs:
Analyze existing codebase:
- Check package.json/requirements.txt for tech stack
- Look for .env.example for service integrations
- Scan src/ for application structure
- Infer business domain from code patterns

If context unclear, ask user:
- "What type of application is this?"
- "Who are the target users?"
- "What's the core value proposition?"

### Step 2: Generate Detailed Technical Documentation

Based on the PROJECT_PLAN.md vision, create comprehensive technical docs:

#### 1. ARCHITECTURE.md
Expand the tech stack into detailed architecture:
- Detailed framework configurations
- API design patterns (REST/GraphQL)
- Database schema and relationships
- Authentication flow details
- State management approach
- Error handling patterns
- Security considerations
- Performance optimizations

#### 2. INFRASTRUCTURE.md
Expand services into deployment specs:
- Detailed service configurations
- Environment variables needed
- CI/CD pipeline setup
- Monitoring and logging setup
- Backup and disaster recovery
- Cost breakdown per service
- Scaling strategies

#### 3. FEATURES.md
Expand core features into detailed specs:
- Complete user stories
- Detailed acceptance criteria
- User journey maps
- Data flow diagrams
- Business rules and validations
- Edge cases and error states
- Integration points

#### 4. DESIGN_SYSTEM.md (if UI exists)
Create comprehensive design specs:
- Component library structure
- Design tokens and variables
- Typography and color systems
- Spacing and layout grids
- Interaction patterns
- Accessibility requirements
- Responsive breakpoints

### Step 3: Write Documentation Files

Create each detailed document using the appropriate template:

#### ARCHITECTURE.md Template:
```markdown
# Technical Architecture

## System Overview
[Detailed technical description of the system]

## Technology Stack
### Frontend
- Framework: [From PROJECT_PLAN]
- State Management: [Decide based on scale]
- Styling: [From PROJECT_PLAN]
- Component Library: [From PROJECT_PLAN]

### Backend
- Framework: [From PROJECT_PLAN]
- ORM/Database Access: [Decide based on framework]
- Authentication: [From PROJECT_PLAN]
- Validation: [Framework-specific]

### Database
- Primary: [From PROJECT_PLAN]
- Caching: [If needed]
- Search: [If needed]

## API Design
[Detailed API structure, endpoints, authentication]

## Data Models
[Complete schema definitions, relationships]

## Security Architecture
[Authentication flows, authorization rules, data protection]

## Performance Strategy
[Caching, optimization, scaling approach]
```

#### INFRASTRUCTURE.md Template:
```markdown
# Infrastructure & Deployment

## Services Configuration
[Detailed setup for each service from PROJECT_PLAN]

## Environment Variables
[Complete list with descriptions]

## CI/CD Pipeline
[GitHub Actions workflows, deployment triggers]

## Monitoring & Logging
[Error tracking, performance monitoring, alerts]

## Cost Analysis
[Detailed breakdown per service and scale]
```

#### FEATURES.md Template:
```markdown
# Feature Specifications

## User Stories
[Detailed user stories for each feature from PROJECT_PLAN]

## Acceptance Criteria
[Specific, testable criteria for each feature]

## Business Rules
[Validations, constraints, workflows]

## Integration Points
[External services, APIs, webhooks]
```

### Step 4: Create Implementation Summary

After generating all documentation, provide summary:

```
✅ Generated detailed technical documentation from vision:
   
📄 Created Documents:
   - docs/ARCHITECTURE.md (Technical architecture)
   - docs/INFRASTRUCTURE.md (Services & deployment)
   - docs/FEATURES.md (Feature specifications)
   - docs/DESIGN_SYSTEM.md (UI/UX specs) [if applicable]
   
📊 Documentation Coverage:
   - API Endpoints: [X] defined
   - Database Schema: [X] tables
   - User Stories: [X] features
   - Infrastructure: [X] services configured
   
Next steps:
1. Review the detailed documentation
2. Run '/test:generate' to create test suites
3. Set up local development environment
4. Configure services as per INFRASTRUCTURE.md
5. Run '/create-issue' to start creating work items
6. Use '/work #1' to begin implementation

The detailed docs provide your implementation blueprint.
Start with infrastructure setup, then move to features.
```

## Important Guidelines

### Be Specific and Actionable
- ❌ Bad: "Set up authentication"
- ✅ Good: "Configure Supabase Auth with Google OAuth and email/password"

### Build From Vision
- PROJECT_PLAN.md is the north star
- All detailed docs must align with the vision
- Don't introduce new tech not in the plan
- Expand on decisions, don't change them

### Apply Domain Intelligence
- Skilled trades → Safety features, certification tracking
- Healthcare → HIPAA compliance, patient privacy
- E-commerce → Payment processing, inventory
- B2B SaaS → Multi-tenancy, team management

### Maintain Consistency
- All tasks should be GitHub issue-ready
- Use consistent naming patterns
- Include clear dependencies between tiers

### Progressive Enhancement
- Tier 1 must work before Tier 2
- Can't build UI (Tier 3) without architecture (Tier 2)
- Custom features (Tier 5) need standard features (Tier 4)

## Error Handling

If missing PROJECT_PLAN.md:
```
⚠️ Missing PROJECT_PLAN.md vision document!
   
You must run '/project-setup' first to create the vision.
The vision document provides the context needed to generate
detailed technical documentation.
   
Workflow:
1. /project-setup  → Creates PROJECT_PLAN.md
2. /plan:generate  → Creates detailed docs
3. /test:generate  → Creates test suites
```

## Usage Examples

```bash
# After running /project-setup (default)
/plan:generate

# Explicitly read from vision
/plan:generate --from-vision

# For existing project without vision
/plan:generate --fresh-analysis

# With domain context for better specs
/plan:generate --domain e-commerce
```