---
description: Run comprehensive production readiness scan and tests
argument-hint: [--fix] [--verbose] [--test-only]
allowed-tools: Bash, Read, Write, Task
---

# Production Readiness Scanner

Run comprehensive production readiness analysis using integrated testing and mock detection.

## Your Task

### Step 1: Run Integrated Production Tests
```bash
!./scripts/ops qa --production --verbose
```

### Step 2: Run Mock Detection Script
```bash
!python ../.claude/scripts/mock_detector.py --verbose --format markdown
```

### Step 3: Analyze Results
Use the production-specialist sub-agent to:
- Review both test results and mock detection output
- Identify critical production readiness issues
- Provide specific fixes for mock implementations
- Validate environment configurations

## Argument Handling
- If `--fix` provided: Use production-specialist to attempt auto-fixes
- If `--verbose` provided: Include detailed analysis in output
- If `--test-only` provided: Only run production tests, skip mock detection

## Integration Benefits
- Uses standardized testing pipeline (ops qa --production)
- Integrated with backend testing framework
- Consistent with other QA processes
- Results can be used in CI/CD automation

The production-specialist sub-agent will analyze the combined results for comprehensive production readiness assessment.