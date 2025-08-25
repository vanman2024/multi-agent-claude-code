---
allowed-tools: Bash(*), Read(*), Write(*), mcp__github(*)
description: Deploy application to staging or production using DigitalOcean and Vercel
argument-hint: [environment] [--skip-tests]
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
- Environment: staging (default) or production
- Options: --skip-tests flag

### Step 2: Pre-deployment Checks
1. Check for uncommitted changes:
   ```bash
   git status --porcelain
   ```
   If changes exist, warn user and ask to commit or stash.

2. Verify on correct branch:
   - staging: any branch allowed
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

### Step 4: Detect Project Components
Read package.json and check for:
- Frontend: presence of react, vue, next, etc.
- Backend: presence of express, fastapi, server scripts
- API/Webhooks: presence of webhook handlers

### Step 5: Deploy Backend/Webhooks to DigitalOcean
If backend or webhooks exist:

#### For App Platform Apps:
```bash
# Check if app exists
doctl apps list --format ID,Name

# Deploy to existing app
doctl apps create-deployment <app-id>

# Get deployment status
doctl apps get-deployment <app-id> <deployment-id>

# Get app URL
doctl apps get <app-id> --format DefaultIngress
```

#### For Serverless Functions (Webhooks):
```bash
# Deploy functions
doctl serverless deploy

# Get function URL
doctl serverless functions get <function-name> --url

# View recent logs
doctl serverless activations logs --last 5
```

### Step 6: Deploy Frontend to Vercel
If frontend exists:

#### For Staging:
```bash
# Deploy to preview
vercel --token=$VERCEL_TOKEN

# Get preview URL from output
```

#### For Production:
```bash
# Deploy to production
vercel --prod --token=$VERCEL_TOKEN

# Get production URL
```

### Step 7: Update Environment Variables
Based on deployment URLs:

#### Update Backend with Frontend URL:
```bash
doctl apps update <app-id> --spec - <<EOF
env:
  - key: FRONTEND_URL
    value: <vercel-url>
    scope: RUN_TIME
EOF
```

#### Update Frontend with Backend URL:
```bash
vercel env add NEXT_PUBLIC_API_URL <digitalocean-url> production
```

### Step 8: Health Checks
```bash
# Check backend health
curl -f https://<backend-url>/health || echo "Backend health check failed"

# Check frontend
curl -f https://<frontend-url> || echo "Frontend check failed"
```

### Step 9: Create GitHub Deployment Record
Use mcp__github__create_deployment to record:
- Environment name
- Deployment URL
- Commit SHA
- Status

### Step 10: Output Summary
```
🚀 Deployment Complete!

Environment: $ENVIRONMENT
Frontend URL: https://...
Backend URL: https://...
Webhook URLs: https://...

View logs:
- Backend: doctl apps logs <app-id>
- Functions: doctl serverless activations logs
- Frontend: vercel logs <deployment-url>
```

## Error Handling
- If tests fail: Stop deployment
- If deployment fails: Show rollback instructions
- If health checks fail: Alert but continue

## Environment-Specific Settings

### Staging
- Allow deployment from any branch
- Use preview URLs
- Enable debug logging
- Skip certain health checks

### Production
- Require main branch
- Require all tests passing
- Use production domains
- Full health checks
- Create GitHub release

## Project Type Handling

### API/Integration Projects
- Only deploy webhooks/functions to DigitalOcean
- No frontend deployment
- Focus on API endpoint availability

### Full-Stack Projects
- Deploy both frontend and backend
- Ensure environment variables are synced
- Run full integration tests

### Static Sites
- Only deploy to Vercel
- No backend deployment needed

## Notes
- NO NGROK! All testing via DigitalOcean public URLs
- Deployment URLs are immediately available
- Use DigitalOcean for ALL backend/webhook hosting
- Use Vercel for ALL frontend hosting