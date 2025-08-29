# GitHub Secrets Setup Guide

When you create a new repository from this template, you'll need to configure GitHub Secrets for the automation to work. Secrets are never copied from templates for security reasons.

## Required Secrets (Minimum for Basic Operation)

### 1. Core AI Services
```bash
# Claude API for local agents
gh secret set ANTHROPIC_API_KEY --body "your-api-key-here"

# GitHub automation token (needs repo, workflow, project scopes)
gh secret set PROJECT_TOKEN --body "your-github-pat-here"
```

### 2. Database (Supabase)
```bash
# From your Supabase project settings
gh secret set SUPABASE_URL --body "https://your-project.supabase.co"
gh secret set SUPABASE_ANON_KEY --body "your-anon-key"
gh secret set SUPABASE_SERVICE_KEY --body "your-service-key"
```

### 3. Deployment (Vercel)
```bash
# From Vercel account settings
gh secret set VERCEL_TOKEN --body "your-vercel-token"
gh secret set VERCEL_ORG_ID --body "your-org-id"
gh secret set VERCEL_PROJECT_ID --body "your-project-id"
```

## Optional Secrets (Add as Needed)

### Additional AI Services
```bash
gh secret set OPENAI_API_KEY --body "your-openai-key"
gh secret set GEMINI_API_KEY --body "your-gemini-key"
```

### Search Services
```bash
gh secret set BRAVE_API_KEY --body "your-brave-key"
gh secret set SERPAPI_API_KEY --body "your-serpapi-key"
```

### Communication
```bash
gh secret set SLACK_BOT_TOKEN --body "your-slack-token"
gh secret set SLACK_TEAM_ID --body "your-team-id"
```

### Testing & Automation
```bash
gh secret set BROWSERBASE_API_KEY --body "your-browserbase-key"
gh secret set POSTMAN_COLLECTION_ID --body "your-collection-id"
```

### Caching
```bash
gh secret set REDIS_URL --body "redis://your-redis-url"
```

## Quick Setup Script

Create a `.env.secrets` file (DO NOT COMMIT THIS):

```bash
ANTHROPIC_API_KEY=sk-ant-...
PROJECT_TOKEN=ghp_...
SUPABASE_URL=https://...
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...
VERCEL_TOKEN=...
VERCEL_ORG_ID=...
VERCEL_PROJECT_ID=...
```

Then run this script to set all secrets at once:

```bash
#!/bin/bash
# setup-secrets.sh
while IFS='=' read -r key value; do
  if [[ ! -z "$key" && ! "$key" =~ ^# ]]; then
    echo "Setting $key..."
    echo "$value" | gh secret set "$key"
  fi
done < .env.secrets

echo "✅ All secrets configured!"
```

## Verification

Check that your secrets are set:
```bash
gh secret list
```

## Getting API Keys

### Anthropic (Required)
1. Go to https://console.anthropic.com/
2. Navigate to API Keys
3. Create new key

### GitHub PAT (Required)
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Create token with scopes: `repo`, `workflow`, `project`, `admin:org` (if using projects)

### Supabase (Required)
1. Create project at https://supabase.com
2. Go to Settings → API
3. Copy URL and keys

### Vercel (For Frontend)
1. Go to https://vercel.com/account/tokens
2. Create new token

### DigitalOcean (For Backend)
1. Go to https://cloud.digitalocean.com/account/api/tokens
2. Generate new token

## Important Notes

- **Never commit secrets** to the repository
- **Use strong tokens** with minimal required scopes
- **Rotate secrets regularly** for security
- **Different environments** may need different secrets (staging vs production)
- **Some workflows** will fail until secrets are configured

## Troubleshooting

If workflows are failing:
1. Check Actions tab for error messages
2. Verify secret names match exactly (case-sensitive)
3. Ensure tokens have required permissions
4. Check secret values don't have extra spaces or quotes

## Auto-Generated Secrets

These are created automatically:
- `GITHUB_TOKEN` - Created by GitHub for each workflow run
- `CLAUDE_CODE_OAUTH_TOKEN` - Set up when you install Claude Code GitHub App

## Environment-Specific Setup

For production deployments, you may also need:
```bash
gh secret set PRODUCTION_API_URL --body "https://api.yourapp.com"
gh secret set STAGING_FRONTEND_URL --body "https://staging.yourapp.com"
```

Remember: Start with the required secrets, then add optional ones as you need specific features!