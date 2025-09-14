---
allowed-tools: Bash(*), Read(*), mcp__github(*)
description: Quick deploy to Vercel (use /work --deploy for full workflow)
argument-hint: [production|preview]
---

# Deploy Command

## Context
- Current branch: !`git branch --show-current`
- Project type: @package.json
- Architecture: @docs/ARCHITECTURE.md
- Git status: !`git status --short`

## Your Task

When user runs `/deploy $ARGUMENTS`, deploy the application following these steps:

### Step 1: Parse Arguments
Extract from $ARGUMENTS:
- Environment: preview (default), staging, or production
- Options: --skip-tests flag

### Step 2: Pre-deployment Checks
1. Check for uncommitted changes:
   ```bash
   git status --porcelain
   ```
   If changes exist, warn user and ask to commit or stash.

2. Verify on correct branch:
   - preview/staging: any branch allowed
   - production: must be on main branch

### Step 3: Run Tests (unless --skip-tests)
```bash
# Check if tests exist and run them
if [ -f "package.json" ] && grep -q '"test"' package.json; then
  npm test
elif [ -f "requirements.txt" ] && [ -d "tests" ]; then
  pytest
fi
```

### Step 4: Detect Project Type
Read package.json and check for:
- Framework: Next.js, Vite, Express, FastAPI, etc.
- Full-stack: Frontend + API routes
- API endpoints: /api routes or serverless functions
- Static site: No backend logic

### Step 5: Deploy to Vercel

#### Install Vercel CLI if needed:
```bash
# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
  npm install -g vercel
fi
```

#### For Preview/Staging:
```bash
# Deploy to preview environment
vercel --token=$VERCEL_TOKEN

# Capture the preview URL
PREVIEW_URL=$(vercel --token=$VERCEL_TOKEN | tail -n 1)
echo "Preview URL: $PREVIEW_URL"
```

#### For Production:
```bash
# Deploy to production
vercel --prod --token=$VERCEL_TOKEN

# Get production URL
PROD_URL=$(vercel --prod --token=$VERCEL_TOKEN | tail -n 1)
echo "Production URL: $PROD_URL"
```

### Step 6: Configure API/Serverless Functions
If the project has API routes or webhooks:

```bash
# Vercel automatically detects and deploys:
# - /api folder as serverless functions
# - /pages/api for Next.js API routes
# - /app/api for Next.js App Router APIs

echo "API endpoints available at:"
echo "  ${DEPLOYMENT_URL}/api/*"
echo "  Webhook endpoint: ${DEPLOYMENT_URL}/api/webhooks"
```

### Step 7: Update Environment Variables
For sensitive environment variables:

```bash
# Set environment variables for the deployment
vercel env add DATABASE_URL production < .env.production
vercel env add API_KEY production < .env.production

# Or use Vercel dashboard for secrets management
echo "Update environment variables at:"
echo "https://vercel.com/${VERCEL_ORG}/${PROJECT_NAME}/settings/environment-variables"
```

### Step 8: Post-deployment Actions

1. **Run health checks:**
```bash
# Check if deployment is healthy
curl -f "${DEPLOYMENT_URL}/api/health" || echo "No health endpoint"
```

2. **Update GitHub deployment status:**
```bash
# Create deployment record
gh api repos/:owner/:repo/deployments \
  -f ref="$(git rev-parse HEAD)" \
  -f environment="${ENVIRONMENT}" \
  -f description="Deployed to Vercel" \
  -f production_environment=$([[ "$ENVIRONMENT" == "production" ]] && echo "true" || echo "false")
```

3. **Comment on PR (if applicable):**
```bash
# If on a PR branch
if [ -n "$PR_NUMBER" ]; then
  gh pr comment $PR_NUMBER --body "🚀 Deployed to ${ENVIRONMENT}: ${DEPLOYMENT_URL}"
fi
```

### Step 9: Provide Summary

Output deployment summary:
```
✅ Deployment Complete!

Environment: ${ENVIRONMENT}
URL: ${DEPLOYMENT_URL}
Branch: $(git branch --show-current)
Commit: $(git rev-parse --short HEAD)

Features deployed:
- Frontend: ${DEPLOYMENT_URL}
- API: ${DEPLOYMENT_URL}/api
- Webhooks: ${DEPLOYMENT_URL}/api/webhooks

Next steps:
1. Test the deployment: ${DEPLOYMENT_URL}
2. Check API health: ${DEPLOYMENT_URL}/api/health
3. Monitor logs: https://vercel.com/${VERCEL_ORG}/${PROJECT_NAME}/logs
```

## Error Handling

If deployment fails:
1. Check Vercel logs for errors
2. Verify environment variables are set
3. Ensure build command succeeds locally
4. Check for TypeScript or linting errors

## Rollback Instructions

To rollback:
```bash
# List recent deployments
vercel ls

# Rollback to previous version
vercel rollback

# Or promote a specific deployment to production
vercel promote [deployment-url]
```

## Special Cases

### Microservices or Complex APIs
For microservices that need special handling:
- Consider using Vercel Edge Functions for geo-distributed APIs
- Use Vercel's monorepo support for multiple services
- Configure custom builds in vercel.json

### Webhook Testing
```bash
# Vercel provides public URLs perfect for webhook testing
echo "Webhook URL for testing: ${DEPLOYMENT_URL}/api/webhooks"
echo "No ngrok needed - this is a public HTTPS endpoint!"
```

### Database Connections
- Use Vercel's Edge Config for configuration
- Consider Vercel Postgres or Vercel KV for data
- Or connect to external databases (Supabase, PlanetScale)

## Examples

```bash
# Deploy to preview (default)
/deploy

# Deploy to staging with tests
/deploy staging

# Deploy to production without tests
/deploy production --skip-tests

# Deploy from feature branch to preview
/deploy preview
```

## Important Notes

- Vercel handles both frontend and backend/API
- Automatic HTTPS and global CDN included
- Serverless functions scale automatically
- Preview deployments for every PR
- Instant rollbacks available
- Built-in analytics and monitoring