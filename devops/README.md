# DevOps Template Toolbox

Drop this repository into a project when you want lightweight CLI helpers for:

- Running QA (`devops/ops/ops qa`, `ops/commands/test.sh`)
- Building production bundles (`devops/deploy/commands/build-production.sh`)
- Deploying bundles to a directory (`devops/deploy/deploy production <path>`)

## Quick Start
```bash
# Quality checks (pytest + optional linting)
./devops/ops/ops qa

# Build a production bundle locally
./devops/deploy/commands/build-production.sh ./build/your-app --force

# Deploy bundle to a target (defaults from config/devops.toml)
./devops/deploy/deploy production ~/deploy/your-app
```

Set project-specific defaults in `config/devops.toml`. Example:
```toml
[package]
name = "your_app"
path = "src"
test_command = "pytest tests/backend -m 'not slow'"

[package.manifest]
version = "VERSION"
requirements = "requirements.txt"
install = "install.sh"
cli = "your-app"

[deploy]
target = "~/deploy/your-app"
```

The tooling assumes a Python backend (pytest) but can be extended—edit `ops/ops`
and `ops/commands/testing/run_tests.py` to add categories or change defaults.
# Testing auto-deploy fixes
# Auto-deploy workflow fixed
# Auto-deploy workflow fully operational
# Restored working workflow
# Fixed auto-deploy: no deploy scripts in template, auto-merge enabled
# Test semantic-release versioning
# Git tag conflict resolved - testing v1.6.0 bump
