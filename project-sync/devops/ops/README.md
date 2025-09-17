# Operations System (ops)

**Unified operations management template for development projects.**

> **Note**: This ops system is designed as a reusable template. When copied to other projects, customize the commands and targets for your specific project needs.

## 🎯 **Main Command**

```bash
./ops/ops <command> [options]
```

## 📋 **Daily Workflow**

```bash
# Complete development workflow
ops qa                    # Quality checks (lint, format, typecheck, tests)
ops build                 # Build production to configured target
ops verify-prod          # Verify production build works
ops release patch         # Create patch release (bug fixes)
ops release minor         # Create minor release (new features)  
ops release major         # Create major release (breaking changes)
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

## 🔗 **Integration**

- **Deploy System**: Use `./deploy/deploy` for deployment-specific tasks
- **GitHub Actions**: Automatic releases on version tags
- **Local Development**: Complete local-first workflow

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