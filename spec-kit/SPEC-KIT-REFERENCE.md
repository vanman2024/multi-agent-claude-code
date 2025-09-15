# 🌱 Spec-Kit Reference Documentation

## What is Spec-Driven Development?

Spec-Driven Development **flips the script** on traditional software development. Instead of specifications being scaffolding we discard after coding, **specifications become executable**, directly generating working implementations.

## Core Philosophy

- **Intent-driven development**: Define the "_what_" before the "_how_"
- **Rich specification creation**: Using guardrails and organizational principles  
- **Multi-step refinement**: Not one-shot code generation from prompts
- **AI model capabilities**: Heavy reliance on advanced AI for specification interpretation

## The Spec-Kit Process

### Phase 1: Specification (`/specify`)
Focus on **WHAT** you want to build and **WHY**, not the tech stack.

Example:
```
/specify Build Taskify, a team productivity platform with projects, team members, 
tasks, comments, and Kanban-style boards. Include 5 predefined users (1 PM, 4 engineers), 
3 sample projects, standard Kanban columns (To Do, In Progress, In Review, Done).
```

**Output**: `specs/001-feature-name/spec.md` with user stories and functional requirements

### Phase 2: Technical Planning (`/plan`)
Now specify your tech stack and architecture.

Example:
```
/plan Use .NET Aspire with Postgres database. Frontend uses Blazor server with 
drag-and-drop task boards. Create REST APIs for projects, tasks, and notifications.
```

**Output**: 
- `specs/001-feature-name/plan.md` - Technical implementation plan
- `specs/001-feature-name/research.md` - Technology research
- `specs/001-feature-name/data-model.md` - Database schema
- `specs/001-feature-name/contracts/` - API specifications

### Phase 3: Task Breakdown (`/tasks`)
Generate actionable implementation tasks.

Example:
```
/tasks
```

**Output**: `specs/001-feature-name/tasks.md` with numbered tasks (T001-T050+)

### Phase 4: Implementation (No slash command)
Execute the tasks by instructing your AI agent:

```
"Implement the tasks from specs/001-feature/tasks.md"
"Start with T001-T010"
"Execute the infrastructure tasks first"
```

**Note**: There's no `/implement` command - you just tell the AI to build based on the generated tasks.

## Directory Structure

```
project-root/
├── memory/
│   ├── constitution.md          # Project principles & guidelines
│   └── constitution_update_checklist.md
├── scripts/
│   ├── create-new-feature.sh    # Create new spec branches
│   ├── setup-plan.sh            # Initialize planning phase
│   └── update-claude-md.sh      # Update AI instructions
├── specs/
│   └── 001-feature-name/
│       ├── spec.md              # Functional specification
│       ├── plan.md              # Technical implementation plan
│       ├── research.md          # Technology research notes
│       ├── data-model.md        # Database schema
│       ├── tasks.md             # Implementation tasks
│       ├── quickstart.md        # Getting started guide
│       └── contracts/           # API specifications
│           ├── api-spec.json
│           └── signalr-spec.md
└── templates/
    ├── spec-template.md         # Template for specifications
    ├── plan-template.md         # Template for planning
    ├── tasks-template.md        # Template for task lists
    └── CLAUDE-template.md       # Template for AI instructions
```

## Development Phases

| Phase | Focus | Key Activities |
|-------|-------|----------------|
| **0-to-1 Development** | Generate from scratch | Start with requirements → Generate specs → Plan → Build |
| **Creative Exploration** | Parallel implementations | Explore diverse solutions, multiple tech stacks |
| **Iterative Enhancement** | Brownfield modernization | Add features, modernize legacy, adapt processes |

## Key Commands

### Initialize Project
```bash
# Install spec-kit
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>

# Or with specific AI agent
specify init <PROJECT_NAME> --ai claude
specify init <PROJECT_NAME> --ai gemini
specify init <PROJECT_NAME> --ai copilot
```

### Core Workflow Commands
1. `/specify` - Create functional specification (what & why)
2. `/plan` - Add technical details (how & with what)
3. `/tasks` - Generate implementation tasks
4. `/implement` - Execute the plan

## Integration with Multi-Agent Framework

### Combining Spec-Kit with Our Tools

1. **Spec-Kit Generates Structure** → Our framework enhances with:
   - GitHub issue creation from tasks
   - AI agent routing (Copilot for simple, Claude for complex)
   - Automated PR workflows
   - CI/CD integration

2. **Enhanced Workflow**:
   ```
   /specify → /plan → /tasks → /import-tasks → /create-issue → /work
   ```

3. **AI CLI Integration**:
   - Use `codex` for code implementation
   - Use `gemini` for documentation
   - Use `openai` for architecture decisions

## Best Practices

### When Creating Specifications
- Be **explicit** about what you're building
- Focus on **user stories** and **functional requirements**
- Don't mention tech stack in `/specify` phase
- Include acceptance criteria

### When Planning
- Research rapidly changing technologies
- Validate against installed versions
- Check for over-engineering
- Reference the constitution.md

### During Implementation
- Validate each phase before proceeding
- Ask AI to check completion checklists
- Create PRs to track progress
- Test frequently

## Common Patterns

### Feature Development
```bash
# 1. Create specification
/specify Build a photo organization app with albums...

# 2. Technical planning  
/plan Use Vite with vanilla HTML/CSS/JS, SQLite for metadata...

# 3. Generate tasks
/tasks

### Iterative Refinement
```bash
# After initial spec
"Add requirement: each project should have 5-15 tasks randomly distributed"

# Check completeness
"Review the acceptance checklist and mark completed items"

# Research specifics
"Research .NET Aspire specifics for our implementation"
```

## Troubleshooting

### Common Issues
1. **Over-eager AI**: AI adds components you didn't request
   - Solution: Ask to clarify rationale and source
   
2. **Missing details**: Plan lacks specific implementation steps
   - Solution: Audit and cross-reference with implementation details
   
3. **Tech stack confusion**: Wrong versions or frameworks
   - Solution: Research specific versions before implementation

### Validation Steps
- Check review & acceptance checklist after each phase
- Validate tech stack matches local installations
- Ensure constitution.md principles are followed
- Test implementation frequently

## Quick Reference

### File Purposes
- `spec.md` - What we're building (functional requirements)
- `plan.md` - How we're building it (technical approach)
- `tasks.md` - Step-by-step implementation tasks
- `research.md` - Technology decisions and findings
- `data-model.md` - Database schema and relationships
- `constitution.md` - Project principles and constraints

### When to Use Each Command
- `/specify` - Starting new feature, defining requirements
- `/plan` - After spec is complete, choosing tech stack
- `/tasks` - After plan is complete, breaking down work

## Links and Resources

- [Spec-Kit GitHub Repository](https://github.com/github/spec-kit)
- [Complete Methodology Guide](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- [Specify CLI Documentation](https://github.com/github/spec-kit#-get-started)