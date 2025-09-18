# Operations System (ops)

**Unified operations management template for development projects.**

> **Note**: This ops system is designed as a reusable template. When copied to other projects, customize the commands and targets for your specific project needs.

## 🎯 **Main Command**

```bash
./ops/ops <command> [options]
```

## 📋 **Available Commands**

```bash
# Development & Quality
ops qa                    # Run quality checks (lint, format, typecheck, tests)
ops build                 # Build production version
ops verify-prod           # Verify production build works

# Releases & Versions
ops release patch         # Create patch release (0.4.9 → 0.4.10)
ops release minor         # Create minor release (0.4.9 → 0.5.0)
ops release major         # Create major release (0.4.9 → 1.0.0)
ops rollback <version>    # Rollback to previous version

# Deployment & Sync
ops sync                  # Sync to all configured targets
ops status                # Show current status and configuration

# Environment & Setup
ops setup <target>        # Setup operations config and target directory
ops env doctor            # Diagnose environment issues
ops hooks install         # Install auto-sync git hooks
```

## 🚀 **Setup**

```bash
# One-time setup with target directory
ops setup ~/deploy/your-project        # Customize path for your project

# Check current status
ops status
```

## 📊 **Semantic Versioning**

```
MAJOR.MINOR.PATCH format:

ops release patch    # 0.4.9 → 0.4.10 (bug fixes)
ops release minor    # 0.4.9 → 0.5.0  (new features)
ops release major    # 0.4.9 → 1.0.0  (breaking changes)
```

## 🔧 **Environment**

```bash
# Diagnose environment issues
ops env doctor

# Check WSL/Windows compatibility
# Check virtual environment setup
# Check dependency availability
```

## 📁 **File Structure**

```
ops/
├── README.md              # This file
├── ops                    # Main command
├── config.yml             # Configuration
└── docs/                  # Documentation
    ├── legacy-readme.md   # Legacy automation docs
    └── scripts-legacy-readme.md  # Legacy scripts docs
```

## ⚙️ **Configuration**

Settings in `ops/config.yml`:

```yaml
versioning:
  strategy: conventional_commits
  source: pyproject.toml

targets:
  - ~/deploy/your-project

release:
  changelog: true
  tag_prefix: v

qa:
  lint: true
  typecheck: true
  tests: "not slow"
```

## � **Rollback System**

The ops system includes comprehensive rollback capabilities for production deployments:

### **Quick Rollback**
```bash
# Rollback to specific version
ops rollback v1.2.3

# Rollback with custom target directory
ops rollback v1.2.3 ~/deploy/signalhire-prod
```

### **Standalone Rollback Script**
```bash
# Use the dedicated rollback script
./devops/deploy/commands/rollback.sh v1.2.3 ~/deploy/signalhire

# Show available versions
./devops/deploy/commands/rollback.sh --help
```

### **Rollback Safety Features**
- ✅ **Automatic backups** - Creates timestamped backup before rollback
- ✅ **Stash handling** - Safely stashes uncommitted changes
- ✅ **Version validation** - Verifies target version exists
- ✅ **Deployment verification** - Tests deployment after rollback
- ✅ **Detailed logging** - Shows rollback summary and recovery options

### **Rollback Process**
1. **Safety Check**: Validates target version and shows impact
2. **Backup Creation**: Backs up current deployment state
3. **Git Checkout**: Switches to target version
4. **Rebuild**: Rebuilds production deployment
5. **Verification**: Tests the rolled-back deployment
6. **Summary**: Shows rollback details and recovery options

### **Recovery Options**
```bash
# If rollback fails, restore from backup
cp -r /tmp/signalhire-backup-*/current-deployment/* ~/deploy/signalhire/

# Restore stashed changes
git stash pop

# Roll forward to newer version
ops rollback v1.2.4
```

## 📋 **Template Customization**

When copying this ops system to a new project:

1. **Update target paths**: Change `~/deploy/your-project` to your actual deployment path
2. **Customize QA commands**: Modify linting, testing, and type checking commands for your stack
3. **Update build script**: Customize `deploy/commands/build-production.sh` for your project structure
4. **Adjust version source**: Update to read version from your project's version file (package.json, Cargo.toml, etc.)

## 🏷️ **Release Process**

1. **Development**: Make changes and commit
2. **Quality**: Run `ops qa` to validate
3. **Build**: Run `ops build` for production build
4. **Verify**: Run `ops verify-prod` to test build
5. **Release**: Run `ops release [patch|minor|major]` to version and tag

This creates:
- Updated `pyproject.toml` version
- Git tag with proper semantic versioning
- GitHub release (if configured)
- Changelog from conventional commits
