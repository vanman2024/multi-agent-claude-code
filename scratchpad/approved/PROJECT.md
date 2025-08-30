# Project Setup & Configuration

## Overview
Comprehensive project setup system for quickly initializing new projects with the Multi-Agent Development Framework.

## /project-setup Slash Command

### Purpose
Initialize a new project with all required configurations, templates, and automations.

### Usage
```bash
/project-setup [project-type] [project-name]
```

### Interactive Flow
1. Select project type (React, Next.js, Node API, etc.)
2. Choose features to include
3. Configure integrations (Supabase, Auth, etc.)
4. Set up GitHub repository
5. Initialize development environment

## Project Types & Tools

### Frontend Projects

#### React SPA
**Tools Required:**
- Vite or Create React App
- React Router
- State management (Zustand/Redux)
- Tailwind CSS
- Testing (Vitest/Jest)

**Setup Commands:**
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
npm install -D tailwindcss postcss autoprefixer
npm install zustand react-router-dom
```

#### Next.js Full-Stack
**Tools Required:**
- Next.js 14+
- App Router
- Server Components
- Tailwind CSS
- Prisma or Drizzle

**Setup Commands:**
```bash
npx create-next-app@latest my-app --typescript --tailwind --app
cd my-app
npm install @supabase/supabase-js prisma
```

### Backend Projects

#### Node.js API
**Tools Required:**
- Express or Fastify
- TypeScript
- Database ORM (Prisma/Drizzle)
- Authentication (JWT/OAuth)
- Testing (Jest/Vitest)

**Setup Commands:**
```bash
mkdir my-api && cd my-api
npm init -y
npm install express cors helmet
npm install -D typescript @types/node @types/express
npm install prisma @prisma/client
```

#### Python FastAPI
**Tools Required:**
- FastAPI
- SQLAlchemy
- Alembic (migrations)
- Pytest
- Poetry or pip

**Setup Commands:**
```bash
mkdir my-api && cd my-api
poetry init
poetry add fastapi uvicorn sqlalchemy alembic
poetry add --dev pytest pytest-asyncio
```

### Full-Stack Templates

#### T3 Stack
- Next.js
- TypeScript
- Tailwind
- tRPC
- Prisma
- NextAuth

#### MEAN Stack
- MongoDB
- Express
- Angular
- Node.js

#### Django + React
- Django REST Framework
- React frontend
- PostgreSQL
- Docker compose

## Project Configuration

### Essential Files

#### For All Projects
```
.env.example           # Environment variables template
.gitignore            # Git ignore patterns
README.md             # Project documentation
CLAUDE.md             # AI assistant instructions
.claude/              # Claude Code configuration
  ├── settings.json   # Hooks configuration
  ├── commands/       # Slash commands
  └── hooks/          # Automation hooks
```

#### For GitHub Integration
```
.github/
├── workflows/        # GitHub Actions
├── ISSUE_TEMPLATE/   # Issue templates
└── pull_request_template.md
```

### Environment Configuration

#### Development
```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dev

# Auth
JWT_SECRET=dev-secret
OAUTH_CLIENT_ID=dev-client
OAUTH_CLIENT_SECRET=dev-secret

# APIs
API_URL=http://localhost:3000
```

#### Production
```env
# Use GitHub Secrets for production values
# Never commit production .env files
```

## Integration Setup

### Supabase Integration
```bash
# Install Supabase CLI
npm install -g supabase

# Initialize project
supabase init
supabase link --project-ref [project-id]

# Set up local development
supabase start
```

### GitHub Repository
```bash
# Create repository
gh repo create my-project --public --clone

# Set up branch protection
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["tests","lint"]}'

# Add secrets
gh secret set DATABASE_URL
gh secret set API_KEY
```

### CI/CD Pipeline
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm test
      - run: npm run lint
```

## Project Structure

### Standard Layout
```
my-project/
├── src/              # Source code
│   ├── components/   # UI components
│   ├── pages/        # Page components
│   ├── hooks/        # Custom hooks
│   ├── utils/        # Utilities
│   └── types/        # TypeScript types
├── public/           # Static assets
├── tests/            # Test files
├── docs/             # Documentation
├── scratchpad/       # Development notes
│   ├── drafts/
│   ├── approved/
│   └── wip/
└── .claude/          # Claude Code config
```

## Automation Features

### Auto-Setup Scripts
```bash
#!/bin/bash
# setup.sh - Project initialization script

# Install dependencies
npm install

# Set up database
npm run db:migrate
npm run db:seed

# Configure git hooks
npx husky install

# Start development
npm run dev
```

### Template Selection
Based on requirements:
- **Simple website** → Static site generator
- **Web app** → React/Next.js
- **API only** → Express/FastAPI
- **Full-stack** → Next.js or T3
- **Mobile** → React Native

## Best Practices

### DO
- ✅ Use TypeScript for type safety
- ✅ Set up linting and formatting
- ✅ Configure pre-commit hooks
- ✅ Add comprehensive README
- ✅ Include .env.example
- ✅ Set up CI/CD immediately

### DON'T
- ❌ Commit secrets or .env files
- ❌ Skip testing setup
- ❌ Ignore accessibility
- ❌ Forget error handling
- ❌ Mix concerns in components

## Quick Start Commands

### Create New Project
```bash
# React app
/project-setup react my-app

# Next.js app
/project-setup nextjs my-app

# Node API
/project-setup node-api my-api

# Full-stack
/project-setup t3 my-fullstack
```

### Add Features
```bash
# Add authentication
/project-setup add-auth

# Add database
/project-setup add-database postgres

# Add testing
/project-setup add-testing
```

## Future Enhancements
- Project template marketplace
- Custom template creation
- Automatic dependency updates
- Performance monitoring setup
- Security scanning integration