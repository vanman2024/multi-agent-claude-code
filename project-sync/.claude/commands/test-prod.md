---
description: Run production readiness tests to validate mock replacements
argument-hint: [--verbose] [--fix]
allowed-tools: Bash, Read, Write, Edit
---

# Production Readiness Testing

Run comprehensive production readiness tests using the integrated testing framework.

## Your Task

Run the production readiness tests that are now integrated into our backend testing structure:

```bash
!./scripts/ops qa --production --verbose
```

## Additional Options

If `--fix` argument is provided, also run the mock detector and suggest fixes:

```bash
!python ../.claude/scripts/mock_detector.py --target testing/backend-tests/production --format json
```

## What This Tests

The production readiness tests validate:
- No mock implementations in production code
- Environment variables are configured
- Debug flags are disabled
- Authentication uses secure implementations
- API endpoints use real implementations
- Integration with mock detector script

All tests are located in `testing/backend-tests/production/` and run via pytest as part of our standard testing pipeline.