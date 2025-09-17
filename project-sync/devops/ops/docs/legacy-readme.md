# 🚀 SignalHire Agent Automation System

**Simplified automation for solo development with AI CLI agents.**

## 🎯 What This Provides

- **Single Command Interface**: `ops` command with clear subcommands
- **Local-First Development**: Everything works locally before automation
- **Explicit Control**: No hidden hooks or automatic behavior
- **WSL/Windows Support**: Handles environment path issues automatically
- **Clean Production Builds**: Simple, reliable deployment process

## 📦 Package Contents

```
.automation/
├── README.md                    # This guide (simplified workflow)
└── config.yml                   # All settings in one place
```

## ⚡ Quick Start

### 1. Setup (One-time)
```bash
# The ops command will be available after setup
# (Claude is creating this)
```

### 2. Daily Development Workflow
```bash
# Quality assurance (lint, test, format)
ops qa

# Build production version locally
ops build --target ~/deploy/signalhire

# Test production build
ops verify-prod --target ~/deploy/signalhire

# Check everything is working
ops status
```

### 3. Release When Ready
```bash
# Only when you have functional changes
ops release patch    # For bug fixes
ops release minor    # For new features
ops release major    # For breaking changes
```

## 📋 Command Reference

### Core Commands
```bash
ops qa                    # Run quality checks (lint, test, format)
ops build [target]        # Build production version
ops verify-prod [target]  # Test production build works
ops status                # Show current state and versions
ops env doctor           # Check WSL/Windows environment issues
```

### Release Commands
```bash
ops release patch        # v0.4.2 → v0.4.3 (bug fixes)
ops release minor        # v0.4.2 → v0.5.0 (new features)
ops release major        # v0.4.2 → v1.0.0 (breaking changes)
```

### Sync Commands
```bash
ops sync                 # Sync to configured targets
ops sync --dry-run       # Preview what would be synced
```

## 🔧 Configuration

All settings in one file: `.automation/config.yml`

```yaml
versioning:
  strategy: conventional_commits
  source: pyproject.toml

targets:
  - ~/Projects/signalhireagenttests2/signalhireagent/

release:
  changelog: true
  tag_prefix: v

qa:
  lint: true
  typecheck: true
  tests: "not slow"
```

## 📊 When to Use Each Command

| Situation | Command | Purpose |
|-----------|---------|---------|
| Daily development | `ops qa` | Check code quality |
| Ready to deploy | `ops build` | Create production build |
| Test deployment | `ops verify-prod` | Validate production works |
| Made functional changes | `ops release` | Create version + tag |
| Check system state | `ops status` | See versions, targets, config |
| WSL path issues | `ops env doctor` | Diagnose environment problems |

## 🚫 What This Doesn't Do

- **No hidden automation**: Everything is explicit and visible
- **No automatic deployments**: You control when things deploy
- **No complex CI/CD**: Focus on local development first
- **No team coordination overhead**: Designed for solo development

## 🔄 Migration from Old System

If you have the old multi-script system:

```bash
# Old way (complex)
./scripts/build/auto-release-manager.sh
./scripts/build/auto-sync-config.sh
./scripts/build/continuous-deployment.sh

# New way (simple)
ops release patch
```

## 🐛 Troubleshooting

### WSL Path Issues
```bash
ops env doctor
# Shows exactly what's wrong and how to fix it
```

### Build Problems
```bash
ops build --target /tmp/test-build
cd /tmp/test-build
./install.sh
# Debug step by step
```

### Version Sync Issues
```bash
ops status
# Shows version in pyproject.toml vs git tags
```

## 📚 Advanced Usage

### Custom Targets
Edit `.automation/config.yml`:
```yaml
targets:
  - ~/deploy/staging
  - ~/deploy/production
  - /var/www/signalhire
```

### GitHub Integration
Enable in config:
```yaml
github:
  enabled: true
  create_releases: true
```

### Advanced QA
```bash
# Run only tests
ops qa --tests-only

# Skip slow tests
ops qa --fast-only

# Custom test pattern
ops qa --tests "integration"
```
