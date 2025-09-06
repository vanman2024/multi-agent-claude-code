# Setting Up CLAUDE.md for Your Project

## What is CLAUDE.md?

CLAUDE.md is a project-specific instruction file that tells Claude Code:
- Your project's conventions and patterns
- Technology stack and architecture
- Security and quality requirements
- How to respond to requests

## Quick Setup

1. **Copy the template:**
```bash
cp templates/CLAUDE.md.template CLAUDE.md
```

2. **Fill in your project details:**
- Replace [PROJECT NAME] with your project name
- Update tech stack section
- Define your file structure
- Add project-specific conventions

3. **Key sections to customize:**

### Project Overview
Brief description helps Claude understand the application's purpose.

### Tech Stack
List all major technologies so Claude uses the right patterns.

### Code Conventions
Your team's specific rules for naming, formatting, and structure.

### Security Rules
Project-specific security requirements (authentication, data handling, etc.)

### External Services
APIs and services Claude needs to know about.

### Response Guidelines
How you want Claude to approach different tasks.

## Best Practices

1. **Keep it updated** - As your project evolves, update CLAUDE.md
2. **Be specific** - Vague instructions lead to inconsistent results
3. **Include examples** - Show the patterns you want followed
4. **Document quirks** - Any non-standard approaches or gotchas
5. **List commands** - Include the actual commands for testing, building, etc.

## What NOT to Include

- Passwords, API keys, or secrets
- Temporary workarounds (fix the root cause instead)
- Personal preferences that conflict with team standards
- Outdated information

## Example Customizations

### For a Next.js App:
```markdown
## Tech Stack
- Frontend: Next.js 14, React 18, TypeScript 5
- Styling: Tailwind CSS
- State: Zustand
- API: Next.js API Routes
- Database: Prisma with PostgreSQL
```

### For a Python API:
```markdown
## Tech Stack
- Backend: FastAPI
- Database: PostgreSQL with SQLAlchemy
- Testing: pytest
- Validation: Pydantic
```

## Maintaining CLAUDE.md

As your project grows:
1. Add new patterns as they're established
2. Remove outdated instructions
3. Update when major refactoring happens
4. Include lessons learned from bugs
5. Document decided architectural patterns

## Testing Your CLAUDE.md

Ask Claude to:
- "Explain our code conventions"
- "What's our tech stack?"
- "How should I implement [feature]?"

If responses don't match expectations, clarify instructions.