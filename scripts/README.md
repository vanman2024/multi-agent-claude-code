# Scripts Directory Organization

All project scripts organized by purpose, independent of their execution context.

## Structure

```
scripts/
├── automation/           # GitHub Actions and CI/CD scripts
│   ├── orchestrate.sh   # Issue/PR orchestration
│   ├── detect-project-type.sh
│   └── run-tests.sh
│
├── development/         # Local development helpers
│   ├── setup-project.sh
│   ├── create-feature.sh
│   └── build-feature.sh
│
├── testing/            # Test execution scripts
│   ├── run-all-tests.sh
│   ├── test-hooks.sh
│   ├── test-agents.sh
│   └── test-integration.sh
│
└── utilities/          # Shared utilities
    ├── json-helpers.sh
    ├── git-helpers.sh
    └── github-api.sh
```

## Usage

### From GitHub Actions
```yaml
- name: Run orchestration
  run: ./scripts/automation/orchestrate.sh
```

### From Claude Code Hooks
```json
{
  "command": "$CLAUDE_PROJECT_DIR/scripts/development/sync-to-github.sh"
}
```

### From Tests
```bash
./scripts/testing/run-all-tests.sh
```

## Important Notes

- Scripts are independent of their location
- GitHub Actions can call scripts from anywhere
- Claude hooks reference scripts via full path
- All scripts should be executable (`chmod +x`)

## Moving Scripts Here

When moving a script to this directory:
1. Move the file to appropriate subdirectory
2. Update all references (workflows, hooks, docs)
3. Test that it still works from new location
4. Remove old location

## Script Standards

- All scripts must have shebang (`#!/bin/bash`)
- All scripts must be executable
- Include usage comments at top
- Use error handling (`set -e`)
- Validate inputs