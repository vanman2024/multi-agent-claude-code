# Project Type Specific Tools & Workflows

## Core Tools (Used Across Multiple Project Types)

### API Testing & Documentation (ALL Projects)
```bash
npm install -g newman                    # Postman CLI for API testing
# MCP: claude mcp add postman

# Used for:
- Full-Stack: Testing your own API endpoints
- API/Integration: Testing external APIs and webhooks
- Static Sites: Testing serverless functions
```

### Hosting & Deployment
```bash
npm install -g @digitalocean/doctl      # DigitalOcean CLI
npm install -g vercel                   # Vercel CLI

# DigitalOcean used for:
- Backend APIs (full-stack apps)
- Webhook handlers (integration projects)
- Serverless functions (any project type)

# Vercel used for:
- Frontend hosting (full-stack & static)
- Edge functions
- API routes (Next.js)
```

### Development Tools
```bash
brew install ngrok                      # Webhook tunnel testing
# Used for ANY project that receives webhooks
```

## API/Integration Projects (Connecting Existing Systems)

**Key Difference**: These projects connect EXISTING systems that already have:
- Their own databases
- Their own authentication
- Their own APIs/webhooks

**What We Build**: 
- Middleware/adapters between systems
- Data transformation layers
- Webhook receivers/senders
- API aggregators

### Standard Workflow
1. **Discovery Phase**
   - Map existing system APIs
   - Document available webhooks
   - Identify data transformation needs
   
2. **Local Development**
   - Use ngrok to receive webhooks locally: `ngrok http 8891`
   - Test external APIs with Postman: `newman run external-apis.json`
   
3. **Integration Development**
   - Build adapters for each system
   - Create data transformation pipelines
   - Handle rate limits and retries
   
4. **Deployment (Minimal Infrastructure)**
   - Deploy ONLY webhook handlers/middleware to DigitalOcean
   - No database needed (using external systems)
   - No auth needed (using external systems)

### Infrastructure Issues Created (Much Lighter!)
- [ ] Setup webhook endpoints (if needed)
- [ ] Configure Postman collections for external APIs
- [ ] Setup basic monitoring
- [ ] Configure rate limiting
- [ ] NO database setup needed
- [ ] NO auth system needed
- [ ] NO storage buckets needed

## Full-Stack SaaS Projects

**Key Difference**: These projects need EVERYTHING:
- Our own database
- Our own authentication
- Our own API
- Frontend UI
- Payment processing
- Email sending

### Core Tools Required
```bash
# Database & Auth
- Supabase (database, auth, storage)

# Hosting
- Vercel (frontend)
- DigitalOcean (backend API)

# API Testing (YES, even for full-stack!)
- Postman/Newman (test your own APIs)
- ngrok (test webhooks from Stripe, etc.)

# Additional Services
- Stripe (payments)
- Resend (email)
```

### Standard Workflow
1. **Database First**
   - Design schema in Supabase Studio
   - Generate TypeScript types
   - Set up RLS policies
   
2. **API Development**
   - Build on DigitalOcean App Platform
   - Use Supabase client libraries
   
3. **Frontend**
   - Deploy to Vercel
   - Use Vercel Analytics
   
### Infrastructure Issues Created
- [ ] Setup Supabase project schema
- [ ] Configure authentication providers
- [ ] Setup storage buckets
- [ ] Configure Stripe integration
- [ ] Setup email service (Resend)

## Static Site/Marketing Projects

### Core Tools Required
```bash
- Vercel (hosting + edge functions)
- Contentful/Sanity (headless CMS)
- Plausible (privacy-first analytics)
```

### Standard Workflow
1. **Content Structure**
   - Define content models in CMS
   - Set up preview environments
   
2. **Build Process**
   - Static generation at build time
   - ISR for dynamic content
   
3. **Performance**
   - Image optimization via Cloudinary
   - Edge caching strategies

### Infrastructure Issues Created
- [ ] Setup CMS and content models
- [ ] Configure preview deployments
- [ ] Setup analytics tracking
- [ ] Configure CDN/caching

## CLI Tool Projects

### Core Tools Required
```bash
- npm/cargo/pip (package registry)
- GitHub Releases (binary distribution)
- No hosting infrastructure needed
```

### Standard Workflow
1. **Development**
   - Build with appropriate language toolchain
   - Package for multiple platforms
   
2. **Distribution**
   - Publish to package registry
   - Create GitHub releases with binaries
   
3. **Updates**
   - Auto-update mechanism
   - Version management

### Infrastructure Issues Created
- [ ] Setup package registry account
- [ ] Configure GitHub Actions for releases
- [ ] Setup code signing (if needed)
- [ ] Configure auto-update system

## Project Type Detection

The `/project-setup` command automatically detects project type based on:

1. **User Description**
   - "connect APIs" → API/Integration
   - "SaaS", "dashboard" → Full-Stack
   - "landing page", "marketing" → Static Site
   - "CLI", "command-line" → CLI Tool

2. **Technical Choices**
   - No frontend → API/Integration or CLI
   - No backend → Static Site
   - Full stack → SaaS

3. **Infrastructure Needs**
   - Webhooks needed → API/Integration
   - Database needed → SaaS
   - Just hosting → Static Site
   - No hosting → CLI Tool

## Tool Activation

Based on project type, the framework:
1. Enables specific MCP servers
2. Creates appropriate infrastructure issues
3. Configures relevant GitHub workflows
4. Sets up project-specific scripts in package.json
5. Activates appropriate specialist agents

This ensures each project type gets exactly the tools it needs, nothing more, nothing less.