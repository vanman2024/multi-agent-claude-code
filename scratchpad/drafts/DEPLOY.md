# 🚀 Deployment Guide

## Overview

This guide covers the complete deployment pipeline from development to production using Vercel for hosting and GitHub for CI/CD.

## 📋 Deployment Workflow Chain

```
Issue → PR → Merge → Tag → Deploy → Release
```

### The Complete Flow:
1. **Development** (Issue → PR → Merge)
2. **Versioning** (Tag after merge)
3. **Deployment** (Deploy from main)
4. **Release** (Create GitHub release)

## 🔄 Deployment Environments

### 1. **Preview Deployments** (Automatic)
- **Trigger**: Every PR automatically
- **URL**: Unique preview URL per PR
- **Purpose**: Test changes before merge
- **Lifetime**: Deleted when PR closed/merged

### 2. **Staging Deployment** (Manual)
- **Trigger**: `/deploy staging` from main
- **URL**: staging-{project}.vercel.app
- **Purpose**: Final testing before production
- **Data**: Uses staging database

### 3. **Production Deployment** (Protected)
- **Trigger**: `/deploy production` from main only
- **URL**: {project}.vercel.app or custom domain
- **Purpose**: Live user-facing application
- **Requirements**: All tests pass, PR approved

## 📝 Pre-Deployment Checklist

### Before ANY Deployment:
```bash
# 1. Ensure on correct branch
git branch --show-current

# 2. Pull latest changes
git pull origin main

# 3. Check for uncommitted changes
git status

# 4. Run tests locally
npm test

# 5. Run linting
npm run lint

# 6. Check environment variables
cat .env.example  # Ensure all vars documented
```

## 🎯 Deployment Strategies

### Strategy 1: Feature Branch → Preview → Staging → Production

```bash
# 1. Work on feature branch
git checkout -b feature/new-feature
# ... make changes ...

# 2. Push for preview deployment (automatic)
git push origin feature/new-feature
# PR created → Preview URL generated automatically

# 3. After PR merged to main
git checkout main
git pull

# 4. Deploy to staging
/deploy staging

# 5. After staging validation
/deploy production
```

### Strategy 2: Hotfix → Direct to Production

```bash
# 1. Create hotfix from main
git checkout -b hotfix/critical-fix

# 2. Push and create PR
git push origin hotfix/critical-fix
gh pr create --title "Hotfix: Critical issue"

# 3. After fast-track review and merge
git checkout main
git pull

# 4. Deploy immediately to production
/deploy production --skip-staging
```

## 🛠️ Vercel Configuration

### Initial Setup (One-time)

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login to Vercel
vercel login

# 3. Link project
vercel link

# 4. Configure project settings
vercel env pull  # Pull environment variables
```

### vercel.json Configuration

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "regions": ["iad1"],
  "functions": {
    "api/**/*.ts": {
      "maxDuration": 10
    }
  },
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/api"
    }
  ],
  "env": {
    "NODE_ENV": "production"
  }
}
```

## 🔐 Environment Variables

### Variable Categories:

1. **Public Variables** (Safe to expose)
   - `NEXT_PUBLIC_API_URL`
   - `VITE_APP_NAME`
   - Prefix with framework convention

2. **Secret Variables** (Never expose)
   - `DATABASE_URL`
   - `API_SECRET_KEY`
   - `GITHUB_TOKEN`

### Setting Variables:

```bash
# Via CLI
vercel env add DATABASE_URL production
vercel env add API_KEY preview staging production

# Via Dashboard
# https://vercel.com/[org]/[project]/settings/environment-variables
```

### Environment-Specific Config:

```bash
# .env.preview
API_URL=https://preview-api.example.com
DATABASE_URL=postgresql://preview-db

# .env.staging
API_URL=https://staging-api.example.com
DATABASE_URL=postgresql://staging-db

# .env.production
API_URL=https://api.example.com
DATABASE_URL=postgresql://prod-db
```

## 🚦 Deployment Commands

### Using /deploy Slash Command

```bash
# Deploy to preview (default)
/deploy

# Deploy to staging
/deploy staging

# Deploy to production
/deploy production

# Skip tests (emergency only)
/deploy production --skip-tests

# With specific commit
/deploy production --commit abc123
```

### Using Vercel CLI Directly

```bash
# Preview deployment
vercel

# Production deployment
vercel --prod

# Deploy specific branch
vercel --scope team-name

# Deploy with environment
vercel --env NODE_ENV=production

# Deploy and alias
vercel --prod --alias myapp.com
```

## 📊 Post-Deployment Validation

### Health Checks

```bash
# 1. Check deployment status
curl https://your-app.vercel.app/api/health

# 2. Run smoke tests
npm run test:e2e -- --url=https://your-app.vercel.app

# 3. Check critical user flows
- Login/logout
- Core feature functionality
- Payment processing (if applicable)
- API endpoints
```

### Monitoring

```bash
# View logs
vercel logs --follow

# Check function logs
vercel logs --scope functions

# View build output
vercel inspect [deployment-url]
```

## 🔄 Rollback Procedures

### Quick Rollback

```bash
# List recent deployments
vercel ls

# Rollback to previous
vercel rollback

# Promote specific deployment
vercel promote [deployment-url]

# Alias to previous version
vercel alias [old-deployment] [production-url]
```

### Git-based Rollback

```bash
# Revert merge commit
git revert -m 1 [merge-commit]
git push origin main

# This triggers new deployment with reverted code
```

## 📦 Release Process (After Deployment)

### Creating a Release

```bash
# 1. After successful production deployment
git tag -a v1.2.3 -m "Release: Feature name"
git push origin v1.2.3

# 2. Create GitHub release
gh release create v1.2.3 \
  --title "v1.2.3: Feature Release" \
  --notes "## What's New
  - Feature 1
  - Feature 2
  
  ## Bug Fixes
  - Fixed issue #123"
```

### Versioning Strategy

Following semantic versioning (MAJOR.MINOR.PATCH):

- **PATCH** (1.2.3 → 1.2.4): Bug fixes only
- **MINOR** (1.2.3 → 1.3.0): New features, backward compatible
- **MAJOR** (1.2.3 → 2.0.0): Breaking changes

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   # Check build logs
   vercel logs --scope build
   
   # Run build locally
   npm run build
   ```

2. **Environment Variable Issues**
   ```bash
   # List all env vars
   vercel env ls
   
   # Pull to local
   vercel env pull
   ```

3. **Function Timeouts**
   - Check function duration in vercel.json
   - Optimize database queries
   - Use Edge Functions for faster response

4. **Domain Issues**
   ```bash
   # Check domain config
   vercel domains ls
   
   # Add domain
   vercel domains add example.com
   ```

## 🔒 Security Considerations

### Pre-deployment Security Checks

```bash
# 1. Check for exposed secrets
git secrets --scan

# 2. Audit dependencies
npm audit

# 3. Check for sensitive data in code
grep -r "password\|secret\|key\|token" --exclude-dir=node_modules

# 4. Validate CORS settings
# Ensure proper origins in production
```

### Production Security

- Enable Vercel's DDoS protection
- Use Vercel's Edge Network for CDN
- Configure CSP headers
- Enable rate limiting on API routes
- Use Vercel's secret storage for sensitive data

## 📈 Performance Optimization

### Before Production Deploy

```bash
# 1. Run Lighthouse audit
npm run lighthouse

# 2. Check bundle size
npm run analyze

# 3. Optimize images
vercel build --prod --debug

# 4. Enable caching headers
# Configure in vercel.json
```

### Vercel Optimizations

```json
{
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

## 🎯 Best Practices

### DO:
- ✅ Always deploy from main to production
- ✅ Use preview deployments for testing
- ✅ Tag releases after successful deployment
- ✅ Monitor deployments for 15 minutes post-deploy
- ✅ Keep staging in sync with production data structure
- ✅ Document all environment variables
- ✅ Use GitHub releases for changelog

### DON'T:
- ❌ Deploy directly from feature branches to production
- ❌ Skip staging for major changes
- ❌ Deploy on Fridays (unless critical)
- ❌ Ignore failed health checks
- ❌ Keep old preview deployments active
- ❌ Store secrets in code or vercel.json
- ❌ Deploy without running tests

## 📱 Integration with GitHub Actions

### Auto-deploy on Merge to Main

```yaml
name: Deploy to Production
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm ci
      - run: npm test
      - run: vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

### Deploy on Release

```yaml
name: Deploy on Release
on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
      - run: |
          echo "Deployed version ${{ github.event.release.tag_name }}"
```

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel CLI Reference](https://vercel.com/docs/cli)
- [GitHub Deployments API](https://docs.github.com/en/rest/deployments)
- Project-specific deploy command: `/deploy`
- Emergency hotline: Check CLAUDE.md for escalation

---

**Remember**: Deployment is the final step in our workflow:
`Issue → PR → Merge → Deploy → Release`

Each step has checks and balances. Never skip steps unless it's a critical hotfix!