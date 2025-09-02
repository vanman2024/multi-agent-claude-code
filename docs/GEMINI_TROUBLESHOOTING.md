# Gemini AI Troubleshooting Guide

## ❗ Common Misconceptions

### "I don't see @gemini anywhere"

**This is expected behavior!** Gemini doesn't appear as a visible user or bot in GitHub's UI. Instead, it works behind the scenes through GitHub Actions.

**How to tell if Gemini is working:**
1. ✅ New issues get automatically labeled (like this one!)
2. ✅ Workflow runs show in the Actions tab
3. ✅ Comments may appear from "github-actions[bot]" acknowledging requests

## 🔍 How to Verify Gemini is Working

### Method 1: Check Recent Issues
Look at newly created issues - they should be automatically labeled by Gemini:

1. Go to your repository's Issues tab
2. Look for issues with labels like `bug`, `enhancement`, `documentation`, etc.
3. Check the issue's timeline - you should see labels added by automation

### Method 2: Check Workflow Runs
1. Go to your repository → Actions tab
2. Look for "🔀 Gemini Dispatch" workflow runs
3. Click on a recent run to see execution details
4. Look for successful "triage" or "review" jobs

### Method 3: Manual Test
Create a comment in any issue or PR:
```
@gemini-cli /triage
```

You should see:
1. A response from "github-actions[bot]" acknowledging the request
2. A new workflow run in the Actions tab
3. Labels applied to the issue (for triage commands)

## 🐛 Actual Problems to Look For

### Problem 1: Missing API Key
**Symptoms:**
- Workflow runs fail with authentication errors
- No response to @gemini-cli commands

**Solution:**
```bash
# Check if the secret exists
gh secret list

# If missing, add it:
gh secret set GEMINI_API_KEY --body "your-api-key-here"
```

### Problem 2: Workflow Permissions
**Symptoms:**
- Workflows run but can't add labels or comments
- Permission denied errors in logs

**Solution:**
1. Go to Settings → Actions → General
2. Ensure "Read and write permissions" is selected
3. Save the setting

### Problem 3: Rate Limiting
**Symptoms:**
- Gemini stops responding after multiple requests
- "Rate limit exceeded" in logs

**Solution:**
- Wait 1 minute (free tier: 60 requests/minute)
- Or upgrade to paid Gemini API tier

## 📋 Verification Checklist

Use this checklist to confirm Gemini is working:

- [ ] **API Key Set**: Run `gh secret list` and confirm `GEMINI_API_KEY` is present
- [ ] **Workflows Present**: Check `.github/workflows/` for gemini-*.yml files
- [ ] **Recent Workflow Runs**: Check Actions tab for recent "Gemini Dispatch" runs  
- [ ] **Auto-labeling Works**: Create a test issue and verify it gets labeled
- [ ] **Manual Commands Work**: Try `@gemini-cli /triage` in an issue comment
- [ ] **Permissions Correct**: Workflows can read repos and write issues/PRs

## 🔧 Debug Commands

### Check Gemini Workflow Status
```bash
# List recent Gemini workflow runs
gh run list --workflow=gemini-dispatch.yml --limit=5

# View logs for a specific run
gh run view [RUN_ID] --log

# Check for failures
gh run list --workflow=gemini-dispatch.yml --status=failure
```

### Test Manual Invocation
Try these commands in issue comments:
```bash
@gemini-cli /triage              # Should add appropriate labels
@gemini-cli /review              # In PRs, should provide code review
@gemini-cli help                 # Should respond with available commands
```

## 💡 Understanding Gemini's Behavior

### What Gemini Does Automatically
- **New Issues**: Analyzes content and applies relevant labels
- **New PRs**: Performs automatic code review
- **Issue Updates**: May re-triage if content changes significantly

### What Gemini Does On-Demand
When you comment `@gemini-cli [command]`:
- Triggers the gemini-dispatch workflow
- Routes to appropriate sub-workflow (review, triage, invoke)
- Executes the requested action
- Posts results as labels, comments, or reviews

### Expected Response Times
- **Immediate**: Acknowledgment comment from github-actions[bot]
- **30-60 seconds**: Workflow execution and results
- **If delayed**: Check Actions tab for queued/running workflows

## 📞 Still Having Issues?

If Gemini isn't working after following this guide:

1. **Check the Actions tab** for error messages in failed workflow runs
2. **Verify your API key** is valid at https://makersuite.google.com/app/apikey
3. **Review repository permissions** for GitHub Actions
4. **Check rate limits** - wait a minute and try again

**Pro tip**: The issue you're reading this from was automatically labeled by Gemini! If you see "bug" and "infra" labels on issue #95, that proves Gemini is working correctly.