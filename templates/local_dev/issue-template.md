# 📋 Issue Template Guide

## Choose the Right Template

This directory contains specialized templates for different types of work:

| Template | Use When | Complexity |
|----------|----------|------------|
| **feature-template.md** | Building new functionality | High |
| **bug-template.md** | Reporting and fixing bugs | Variable |
| **refactor-template.md** | Improving existing code | Medium |
| **task-template.md** | Simple, one-off tasks | Low |

## Generic Issue Format (if none fit)

If your issue doesn't fit the above templates, use this format:

```markdown
## Description
[What needs to be done]

## Why
[Business or technical justification]

## Acceptance Criteria
- [ ] Clear success criteria
- [ ] Measurable outcomes

## Technical Notes
[Any implementation details]
```

## Quick Decision Tree

```
Is it broken? → bug-template.md
Is it new? → feature-template.md  
Is it messy? → refactor-template.md
Is it simple? → task-template.md
```

## Remember

- **Complexity** and **Size** determine agent assignment
- **Labels** trigger specific workflows
- **Clear titles** help with routing