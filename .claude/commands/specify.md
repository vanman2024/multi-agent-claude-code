---
allowed-tools: Bash(*), Read(*), Write(*), TodoWrite(*)
description: Wrapper for spec-kit's /specify command - creates functional requirements WITHOUT tech stack
argument-hint: [detailed requirements description - be explicit about WHAT not HOW]
---

# Specify - Functional Requirements

## Context
- Current directory: !`pwd`
- Check spec-kit: !`which specify || echo "spec-kit not installed"`

## Your Task

When user runs `/specify $ARGUMENTS`, create functional specifications using spec-kit.

### Phase 1: Check Prerequisites

```bash
# Check if spec-kit is initialized
if [ ! -d "memory" ] || [ ! -f "memory/constitution.md" ]; then
  echo "⚠️  Initializing spec-kit project..."
  specify init --ai claude
fi

# Check if commands are available
if ! specify --help | grep -q "/specify"; then
  echo "❌ spec-kit commands not configured properly"
  echo "Try running: specify init --ai claude"
  exit 1
fi
```

### Phase 2: Create Specification

**IMPORTANT**: At this stage, do NOT mention tech stack. Focus only on:
- What the application does
- Who uses it
- What problems it solves
- User workflows
- Business rules
- Constraints

Run the specify command with the user's requirements:
```bash
specify "$ARGUMENTS"
```

This should create:
- A new branch (e.g., `001-feature-name`)
- A spec directory under `specs/001-feature-name/`
- An initial `spec.md` with functional requirements

### Phase 3: Track in Todo

Use TodoWrite to track specification creation:
```
- [ ] Specification created: specs/XXX-feature/spec.md
- [ ] Functional requirements defined
- [ ] User stories captured
- [ ] Ready for clarification
```

### Phase 4: Report Results

Output:
```
✅ Specification created successfully!

📁 Location: specs/001-feature-name/spec.md
🌿 Branch: 001-feature-name

Next steps:
1. Review and clarify requirements
2. Validate acceptance checklist
3. Run '/plan' to add technical details
4. Run '/tasks' to generate implementation tasks
```

## Example Usage

```
User: /specify Develop Taskify, a team productivity platform. It should allow users to create projects, add team members, assign tasks, comment and move tasks between boards in Kanban style...

You: 
🔍 Checking spec-kit setup...
✅ spec-kit initialized

📝 Creating functional specification...
[spec-kit output]

✅ Specification created!
- Branch: 001-develop-taskify
- Spec: specs/001-develop-taskify/spec.md

The specification focuses on WHAT to build:
- Team productivity platform
- 5 predefined users (1 PM, 4 engineers)
- 3 sample projects
- Kanban board with drag-drop
- Comments system with permissions
- No authentication (initial phase)

Next: Review the spec and run '/plan' to add technical details
```

## Important Notes

- **NO TECH STACK** at this stage - pure functional requirements
- Be as explicit as possible about WHAT to build
- Focus on user stories and workflows
- This creates the foundation for all future work
- The spec should be tech-agnostic