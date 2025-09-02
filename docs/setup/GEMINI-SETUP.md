# Gemini AI Setup Guide

> **Status**: 🟡 AVAILABLE BUT OPTIONAL
> **Last Updated**: 2025-09-02
> **Stability**: Beta

## Quick Setup

### 1. Get API Key
- Visit: https://makersuite.google.com/app/apikey
- Create new API key
- Copy the key

### 2. Add to GitHub Secrets
```bash
gh secret set GEMINI_API_KEY --body "your-api-key-here"
```

### 3. Available Workflows
- `gemini-review.yml` - PR code review
- `gemini-triage.yml` - Issue triage
- `gemini-dispatch.yml` - Custom AI tasks

## Usage

### For PR Reviews
Comment on any PR:
```
@gemini review
```

### For Issue Triage
Automatically runs on new issues if API key is set.

## Notes
- Free tier: 15 requests/minute
- Works alongside Claude and Copilot
- Good for additional review perspective