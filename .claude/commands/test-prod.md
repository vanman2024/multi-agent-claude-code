---
description: Generate tests to validate production readiness and mock replacements
argument-hint: [--integration] [--unit] [--api] [--all]
allowed-tools: Bash, Read, Write, Edit, Task
---

Generate comprehensive tests to validate that mock implementations have been properly replaced with real production code.

## Execution Process

### Step 1: Read Mock Detection Results
```bash
# Check if we have recent mock detection results
if [ -f "/tmp/mock_report.json" ]; then
    cat /tmp/mock_report.json
else
    echo "No recent mock detection results found. Run /prod-ready first."
    python .claude/scripts/mock_detector.py --format json --output /tmp/mock_report.json
fi
```

### Step 2: Generate Tests Based on Found Issues
Use the test-generator sub-agent to:
- Analyze the mock detection results
- Generate specific tests for each critical mock found
- Create integration tests for API endpoints  
- Generate unit tests for replaced implementations
- Create environment validation tests

### Step 3: Create Test Structure
The sub-agent should create:
- `tests/production/` directory structure
- Individual test files for each mock category
- Test fixtures and setup helpers
- CI/CD integration scripts

### Step 4: Handle Arguments
- `--integration`: Generate integration tests only
- `--unit`: Generate unit tests only  
- `--api`: Generate API endpoint tests only
- `--all`: Generate comprehensive test suite (default)

The test-generator sub-agent will create executable tests that can validate production readiness before deployment.