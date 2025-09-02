# Gemini AI Setup Guide

## Quick Setup (API Key Method)

1. **Get Gemini API Key**:
   - Visit: https://makersuite.google.com/app/apikey
   - Create new API key
   - Copy the key

2. **Add to GitHub Repository**:
   ```bash
   gh secret set GEMINI_API_KEY --body "your-api-key-here"
   ```

3. **Test It**:
   - Create a PR
   - Comment: `@gemini-cli /review`
   - Gemini will respond with code review

## What Gemini Does

### Automatic Triggers
- **New PR opened** → Automatic code review
- **New issue opened** → Automatic triage and labeling
- **PR updated** → Re-reviews changes

### Manual Commands
```bash
# In any PR or issue comment:
@gemini-cli /review              # Full code review
@gemini-cli /review security     # Security-focused review
@gemini-cli /triage              # Triage and label issue
@gemini-cli check for bugs       # Custom prompt
```

## Workflows Included

1. **gemini-dispatch.yml** - Main router for all Gemini commands
2. **gemini-review.yml** - Code review logic
3. **gemini-triage.yml** - Issue triage logic
4. **gemini-invoke.yml** - Custom prompt handler
5. **gemini-scheduled-triage.yml** - Scheduled triage runs

## Cost
- **Free tier**: 60 requests/minute
- **Paid**: Very affordable ($0.00025 per 1K chars)

## Troubleshooting

**Not responding?**
```bash
# Check secret is set
gh secret list

# Check workflow runs
gh run list --workflow=gemini-dispatch.yml
```

**Rate limited?**
- Wait a minute (60 req/min limit)
- Or upgrade to paid tier