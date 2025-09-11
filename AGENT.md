# Codex CLI Context

You are being called via the Codex CLI to assist with code implementation in this project.

## Project Overview
This is a multi-agent development framework that combines spec-kit methodology with GitHub automation and AI assistance.

## Current Tech Stack
- Frontend: Next.js, React, TypeScript, Tailwind CSS
- Backend: Next.js API Routes, Serverless Functions
- Database: Supabase (when needed)
- Deployment: Vercel
- Testing: Jest, Playwright, Newman/Postman

## Key Directories
- `specs/` - Spec-kit generated specifications and tasks
- `scripts/` - Automation scripts
- `.claude/commands/` - Slash commands
- `spec-kit-docs/` - Reference documentation

## Your Role
When called via `codex exec "command"`:
- Focus on code implementation
- Follow existing patterns in the codebase
- Use TypeScript with strict mode
- Include error handling
- Follow TDD when tests exist

## Common Tasks You'll Handle
- Implementing infrastructure tasks (T001-T010)
- Creating API endpoints
- Building React components
- Writing database schemas
- Refactoring for performance
- Debugging and fixing errors

## Code Style
- Use async/await over callbacks
- Prefer functional components in React
- Use proper TypeScript types
- Follow existing naming conventions
- Add JSDoc comments for public APIs

## Available Commands
You can suggest running:
- `npm test` - Run tests
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Check code style

## Current Workflow
We follow spec-kit methodology:
1. /specify - Define requirements
2. /plan - Choose tech stack
3. /tasks - Generate task list
4. /implement - Execute tasks (you help here)

When implementing, reference task numbers (T001, T002, etc.) from the specs/*/tasks.md files.