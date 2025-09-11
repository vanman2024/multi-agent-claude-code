---
allowed-tools: Bash(*), Read(*), Write(*)
description: Use multiple AI CLIs for specialized code review
argument-hint: [file-path or pattern]
---

# AI Multi-Agent Review

## Your Task

Use different AI CLIs for specialized review tasks on the code.

## Step 1: Get the file(s) to review
Read the file: @$ARGUMENTS

## Step 2: Run specialized reviews

### Code Quality Review (Codex)
Run: !codex "Review this code for best practices and potential bugs: $(cat $ARGUMENTS)"

### Documentation Review (Gemini)  
Run: !gemini -p "Review the documentation and comments in this code: $(cat $ARGUMENTS)"

### Security Review (OpenAI)
Run: !openai "Review this code for security vulnerabilities: $(cat $ARGUMENTS)"

## Step 3: Consolidate feedback
Combine all three reviews into a summary report and save to `reviews/ai-review-$(date +%Y%m%d).md`