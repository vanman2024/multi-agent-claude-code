# Scripts Directory Organization

All project scripts organized by purpose, independent of their execution context.

## Structure

```
scripts/
├── deployment/          # Deployment and CI/CD scripts
│   └── vercel-ignore-build.sh    # Controls Vercel deployments based on checkboxes
│
├── testing/            # Test execution and simulation scripts
│   ├── test-mimic.sh              # Simulates /test command behavior
│   └── test-frontend-agent-mimic.sh  # Shows frontend agent browser testing
│
└── utilities/          # General purpose utilities
    └── create-checkbox-status.sh  # Manually creates GitHub commit status
```

## Usage

### From GitHub Actions
```yaml
- name: Check checkboxes
  run: ./scripts/utilities/create-checkbox-status.sh
```

### From Vercel Settings
Configure in Vercel Dashboard → Project Settings → Git → Ignored Build Step Command:
```bash
./scripts/deployment/vercel-ignore-build.sh
```

### From Command Line (Testing)
```bash
# Test what /test command should do
./scripts/testing/test-mimic.sh

# Test frontend agent behavior
./scripts/testing/test-frontend-agent-mimic.sh

# Manually create checkbox status
./scripts/utilities/create-checkbox-status.sh
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