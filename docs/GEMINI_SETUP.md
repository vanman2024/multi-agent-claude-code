# 🔧 Gemini AI Integration Setup Guide

Complete setup instructions for integrating Google's Gemini AI with your Multi-Agent Development Framework repository.

## Prerequisites Checklist

### 1️⃣ Google Cloud Setup
- [ ] Create a Google Cloud Project (or use existing)
- [ ] Enable the Gemini/Vertex AI API in the project
- [ ] Set up billing (Gemini API may have costs after free tier)
- [ ] Note your Project ID for later

### 2️⃣ Gemini API Key
- [ ] Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
- [ ] Click "Create API Key"
- [ ] Select your Google Cloud project
- [ ] Copy the API key (keep it secure!)

### 3️⃣ GitHub Repository Secrets
Add these secrets in Settings → Secrets and variables → Actions:
- [ ] `GEMINI_API_KEY` - Your API key from AI Studio
- [ ] `GOOGLE_CLOUD_PROJECT` - Your GCP project ID (if using Vertex AI)

### 4️⃣ GitHub Variables (Optional)
Add these in Settings → Variables:
- [ ] `GCP_WIF_PROVIDER` - Workload Identity Federation provider (if using)
- [ ] `GOOGLE_CLOUD_LOCATION` - Region (e.g., `us-central1`)
- [ ] `SERVICE_ACCOUNT_EMAIL` - Service account (if using Vertex AI)
- [ ] `GOOGLE_GENAI_USE_VERTEXAI` - Set to `true` for Vertex AI
- [ ] `GOOGLE_GENAI_USE_GCA` - Set to `true` for Code Assist

## 💡 Quick Setup (Simplest Path)

If you just want to get started quickly:

1. **Get API Key from AI Studio**:
   ```bash
   # Visit: https://makersuite.google.com/app/apikey
   # Create API key and copy it
   ```

2. **Add to GitHub Secrets**:
   ```bash
   gh secret set GEMINI_API_KEY --body "your-api-key-here"
   ```

3. **Set Required Variables**:
   ```bash
   gh variable set GEMINI_MODEL --body "gemini-1.5-pro"
   gh variable set GEMINI_CLI_VERSION --body "latest"
   ```

4. **Test the Integration**:
   - Merge this PR
   - Go to Issue #104 or create a new issue
   - Comment: `@gemini help`
   - Check Actions tab for workflow execution
   - Look for Gemini's response comment

## 🏢 Advanced Setup (For Production)

For enterprise environments or production use:

### Workload Identity Federation (Recommended)
1. Set up Workload Identity Federation for keyless authentication
2. Use Vertex AI instead of direct API calls
3. Configure rate limiting and quotas in GCP Console
4. Set up monitoring and alerts for usage

### Service Account Setup
```bash
# Create service account
gcloud iam service-accounts create gemini-github-actions

# Grant necessary permissions
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:gemini-github-actions@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# Configure Workload Identity
gcloud iam service-accounts add-iam-policy-binding \
  --role roles/iam.workloadIdentityUser \
  --member "principal://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/subject/repo:OWNER/REPO:ref:refs/heads/main" \
  gemini-github-actions@PROJECT_ID.iam.gserviceaccount.com
```

## 💰 Cost Considerations

⚠️ **Important**: Understand Gemini API pricing before setup:

### Free Tier
- **60 requests per minute** (may be sufficient for testing)
- **15 requests per minute** for free tier users
- **1,500 requests per day** limit

### Paid Pricing (Gemini 1.5 Flash)
- **Input**: ~$0.075 per 1M tokens (~$0.00007 per 1K characters)
- **Output**: ~$0.30 per 1M tokens (~$0.0003 per 1K characters)
- **Estimated cost**: $1-5 per month for typical repository

### Vertex AI Pricing
- Different pricing model, usage-based
- May be more cost-effective for high-volume usage
- Includes additional enterprise features

### Cost Management Tips
```bash
# Set quotas in Google Cloud Console to prevent unexpected charges
# Monitor usage in AI Studio or GCP Console
# Consider using scheduled triage sparingly in high-traffic repos
```

## What Gemini Does

### 🤖 Automatic Triggers
- **New PR opened** → Automatic code review
- **New issue created** → Automatic triage and labeling
- **PR updated** → Re-reviews changes
- **Scheduled triage** → Every 4 hours, processes unlabeled issues

### 💬 Manual Commands
```bash
# In any PR or issue comment:
@gemini /review                    # Full code review
@gemini /review security          # Security-focused review
@gemini /triage                   # Triage and label issue
@gemini help                      # Show available commands
@gemini explain this code         # Ask questions about code
@gemini check for bugs            # Custom analysis
@gemini suggest improvements      # Code optimization suggestions

# Both formats work identically:
@gemini-cli /review               # Alternative format
```

## 🔄 Workflows Included

The integration includes 6 coordinated workflows:

### Core Workflows
1. **`gemini-dispatch.yml`** - Main router for all Gemini commands
2. **`gemini-invoke.yml`** - Handles general `@gemini` requests
3. **`gemini-triage.yml`** - Analyzes and labels individual issues  
4. **`gemini-pr-review.yml`** - Provides code review for pull requests

### Automation Workflows
5. **`gemini-scheduled-triage.yml`** - Automatically processes unlabeled issues every 4 hours

### Testing Workflows  
6. **`gemini-test-mode.yml`** - Safe testing environment with no production impact

## ✅ Testing After Setup

### Safe Testing (Recommended)
1. **Create a test issue** in your repository
2. **Add the `test-gemini` label** to the issue
3. **Watch the automated test run** in the Actions tab
4. **Check issue comments for results**
5. **Review test logs** for any configuration issues

### Manual Testing via Actions
```bash
# Go to: Actions tab → Gemini Test Mode → Run workflow
# Enter parameters:
#   - Issue number: (test issue number)
#   - Test command: "help" or "are you there?"
#   - Enable debug: true (for detailed logs)
```

### Production Testing
1. **Verify secrets are configured**:
   ```bash
   gh secret list | grep GEMINI
   ```

2. **Create a real test**:
   ```bash
   # Create new issue or go to existing one
   # Comment: @gemini help
   # Wait 2-3 minutes for response
   ```

3. **Check Actions logs** if no response:
   ```bash
   gh run list --workflow=gemini-dispatch.yml --limit=5
   gh run view [RUN_ID] --log
   ```

## 🔧 Troubleshooting

### Common Issues

**❌ "GEMINI_API_KEY not found" error**
```bash
# Check if secret exists
gh secret list

# Set the secret
gh secret set GEMINI_API_KEY --body "your-api-key"

# Verify in repository Settings → Secrets and variables
```

**❌ "API quota exceeded" error**
- Check quotas in [Google Cloud Console](https://console.cloud.google.com/quotas)
- Wait for quota reset (typically per minute/day)
- Consider upgrading to paid tier
- Reduce scheduled triage frequency

**❌ "Authentication failed" error**
- Verify API key is correct and active
- Check if billing is enabled in Google Cloud
- Ensure Gemini API is enabled in your GCP project

**❌ Workflows not triggering**
```bash
# Check repository permissions
# Go to: Settings → Actions → General
# Ensure "Read and write permissions" is enabled

# Verify workflow files exist
ls .github/workflows/gemini-*.yml

# Run diagnostic script
bash scripts/check-gemini.sh
```

**❌ No response from @gemini mentions**
- Check that the comment format is correct: `@gemini help` (not `@gemini: help`)
- Verify workflows have proper GitHub token permissions
- Check Actions tab for failed workflow runs
- Review workflow logs for error details

### Debug Mode
Enable detailed logging by setting repository variables:
```bash
gh variable set DEBUG --body "true"
gh variable set ACTIONS_STEP_DEBUG --body "true"
```

### Rate Limiting
If you hit rate limits:
- **Free tier**: 15 requests/minute, 1,500/day
- **Paid tier**: 60 requests/minute
- **Solution**: Wait for reset or upgrade billing

### Diagnostic Script
Run the built-in diagnostic tool:
```bash
bash scripts/check-gemini.sh
```

This script checks:
- Required workflow files
- GitHub secrets configuration  
- Recent workflow runs
- Repository permissions
- Provides quick test instructions

## 🔒 Security Features

The integration includes several security measures:
- **Input validation** on all user requests
- **Restricted shell commands** (read-only operations only)
- **No write access** to repository files via shell commands
- **Safe command allowlist** (echo, ls, grep, find, cat, etc.)
- **No network access** from shell commands
- **Request sanitization** to prevent injection attacks

## 📚 Additional Resources

### Documentation
- **Setup**: `docs/GEMINI_SETUP.md` (this file)
- **Usage**: `docs/GEMINI_USER_GUIDE.md`
- **Troubleshooting**: `docs/GEMINI_TROUBLESHOOTING.md`
- **Main Integration**: `GEMINI.md`

### Official Resources
- [Google AI Studio](https://makersuite.google.com/)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Google GitHub Actions](https://github.com/google-github-actions/run-gemini-cli)
- [Vertex AI Console](https://console.cloud.google.com/vertex-ai)

### Support
- Create an issue in this repository with the `question` label
- Check existing issues with `gemini` label
- Run `bash scripts/check-gemini.sh` for automated diagnostics

---

## 🚀 Quick Start Summary

1. **Get API key** from [AI Studio](https://makersuite.google.com/app/apikey)
2. **Set secret**: `gh secret set GEMINI_API_KEY --body "your-key"`
3. **Set variables**: `gh variable set GEMINI_MODEL --body "gemini-1.5-pro"`
4. **Test safely**: Create issue → Add `test-gemini` label → Check results
5. **Go live**: Comment `@gemini help` in any issue/PR

**Need help?** Run `bash scripts/check-gemini.sh` for automated diagnosis!