---
allowed-tools: Bash(*), Read(*), Write(*), Edit(*)
description: Enhance spec-kit specs with AI insights
argument-hint: [spec-file-path]
---

# AI Spec Enhancement

## Your Task

Use AI CLIs to enhance spec-kit generated specifications with additional insights.

## Context
- Spec file: @$ARGUMENTS
- Check if specs/ directory exists

## Process

### 1. Technical Architecture (Codex)
```bash
codex <<EOF
Based on this specification, suggest:
1. Database schema
2. API endpoints  
3. Key algorithms
Spec: $(cat $ARGUMENTS)
EOF
```

### 2. User Experience (Gemini)
```bash
gemini -p "Based on this spec, suggest UI/UX improvements and user flows: $(cat $ARGUMENTS | head -50)"
```

### 3. Business Logic (OpenAI)
```bash
openai "Identify business rules and edge cases from this spec: $(cat $ARGUMENTS | head -50)"
```

### 4. Update the spec
Append the AI insights to the original spec file under a new "## AI-Enhanced Recommendations" section.