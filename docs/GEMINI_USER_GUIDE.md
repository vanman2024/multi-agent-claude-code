# Gemini AI User Guide

## 🤖 What is Gemini?

Gemini is an AI assistant integrated into this repository through GitHub Actions. It helps with:

- **Automatic issue triage** - Labels new issues based on content
- **Code review** - Analyzes pull requests for potential improvements  
- **On-demand assistance** - Responds to specific commands in comments

## 🚀 Quick Start

### Automatic Features (No Action Needed)

Gemini works automatically when you:
- **Create a new issue** → Gets labeled automatically
- **Open a pull request** → Gets reviewed automatically  
- **Update a PR** → Gets re-reviewed

### Manual Commands

Comment these in any issue or PR to invoke Gemini:

```bash
@gemini-cli /review              # Full code review (PRs only)
@gemini-cli /review security     # Security-focused review  
@gemini-cli /triage              # Triage and label issue
@gemini-cli analyze this code    # Custom analysis
@gemini-cli help                 # Show available commands
```

## 💡 How to Tell if Gemini is Working

### ✅ Signs Gemini is Active
- New issues automatically get labels (like `bug`, `enhancement`)
- PRs get review comments from automated analysis
- Comments show acknowledgment: "Hi @username, I've received your request"
- Actions tab shows "🔀 Gemini Dispatch" workflow runs

### ❌ Common Misunderstandings
- **"I don't see @gemini user"** - Gemini works through GitHub Actions, not as a visible user
- **"Nothing happens"** - Check the Actions tab for workflow runs
- **"No response"** - Responses appear as labels, comments, or reviews, not chat messages

## 📋 Examples

### Example 1: Issue Triage
1. Create an issue describing a bug
2. Gemini automatically analyzes it
3. Issue gets labeled with relevant tags (e.g., `bug`, `frontend`)

### Example 2: Manual Code Review
1. Comment in a PR: `@gemini-cli /review security`
2. GitHub Actions bot acknowledges the request
3. Gemini analyzes code and posts review comments
4. Check Actions tab to see workflow execution

### Example 3: Custom Analysis
1. Comment: `@gemini-cli check this function for potential memory leaks`
2. Gemini analyzes the code with your specific request
3. Results appear as a reply comment

## ⚡ Best Practices

### Effective Commands
- **Be specific**: `@gemini-cli check for SQL injection vulnerabilities`
- **Context matters**: Include relevant details in your request
- **One command per comment**: Don't mix multiple commands

### Timing
- **Allow 30-60 seconds** for responses
- **Check Actions tab** if no immediate response
- **Rate limit**: Max 60 requests per minute (free tier)

## 🔍 Troubleshooting

### No Response to Commands?
1. Check Actions tab for workflow runs
2. Verify command syntax: `@gemini-cli /command`
3. Wait 60 seconds and try again (rate limiting)

### Labels Not Applied?
1. Check if issue content is clear and descriptive
2. Look at Actions tab for failed workflow runs
3. Repository may need label setup

### Need Help?
- See `docs/GEMINI_TROUBLESHOOTING.md` for detailed debugging
- Check recent workflow runs in Actions tab
- Try the verification checklist in troubleshooting doc

## 🎯 Command Reference

| Command | Usage | Result |
|---------|-------|---------|
| `/review` | `@gemini-cli /review` | Full code review of PR |
| `/review security` | `@gemini-cli /review security` | Security-focused review |
| `/triage` | `@gemini-cli /triage` | Label and categorize issue |
| Custom prompt | `@gemini-cli analyze performance` | Custom analysis request |

---

**💡 Pro Tip**: This repository's issue #95 was automatically labeled by Gemini when it was created. That proves the system is working correctly!