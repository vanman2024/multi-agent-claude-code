# DevOps System

**Complete DevOps template for any development project.**

> **Template Usage**: Copy this entire `devops/` folder to new projects and customize for your specific stack and deployment needs.

## 🎯 **System Overview**

This DevOps system provides everything needed for modern development workflow:

## **🖥️ LOCAL SYSTEMS** (Active Now)
- **Development Operations** (`ops/`) - LOCAL: Daily workflow, QA, releases
- **Deployment Management** (`deploy/`) - LOCAL: Production builds and deployments  

## **☁️ AUTOMATION SYSTEMS** (Future)
- **Cross-Platform CI/CD** (`ci/`) - AUTOMATED: Multi-OS testing and automation that will TRIGGER local systems

## 🚀 **Quick Start**

### **🖥️ LOCAL WORKFLOW** (Current - Active Now)
```bash
# LOCAL: Daily development workflow (you run these)
./devops/ops/ops qa                    # LOCAL: Quality checks
./devops/ops/ops build                 # LOCAL: Build production version
./devops/ops/ops verify-prod          # LOCAL: Verify build works
./devops/ops/ops release patch        # LOCAL: Create release

# LOCAL: Production deployment (you run this)
./devops/deploy/deploy production ~/deploy/your-project
```

### Portable Configuration (`config/devops.toml`)
When you copy this DevOps folder into a new project, create or edit `config/devops.toml` so the CLI knows which package to manage, how to run tests, and where to deploy.

```toml
[versioning]
package = "example_package"
source = "src/config/package.toml"

[package]
name = "example_package"
path = "src"
test_command = "pytest tests/backend"

[package.manifest]
version = "VERSION"
requirements = "requirements.txt"
install = "install.sh"
cli = "example-cli"

[deploy]
target = "/abs/path/to/project-sync"
subdirectory = "project-sync/agentswarm"
```

Once this file is set, `./devops/ops/ops qa` and `./devops/deploy/deploy` automatically use the package-specific commands—no script edits required.

### **☁️ AUTOMATED WORKFLOW** (Future - Will Trigger Local)
```bash
# AUTOMATED: GitHub Actions will trigger your local commands
git push origin main                   # AUTOMATED: Triggers CI/CD
# → GitHub Actions runs ./devops/ops/ops qa
# → GitHub Actions runs ./devops/ops/ops build  
# → GitHub Actions runs ./devops/deploy/deploy production
```

## 📁 **System Structure**

```
devops/
├── README.md              # This overview
│
├── 🖥️ LOCAL SYSTEMS (Active Now - You Run These)
├── ops/                   # LOCAL: Development workflow system
│   ├── ops               # LOCAL: Main CLI (qa, build, release, etc.)
│   ├── config.yml        # LOCAL: Configuration
│   ├── README.md         # LOCAL: Ops documentation
│   └── commands/         # LOCAL: Complete utility library
│       ├── development/  # LOCAL: Development tools
│       ├── testing/      # LOCAL: Testing utilities
│       ├── git/         # LOCAL: Git helpers
│       ├── agents/      # LOCAL: Agent management
│       └── data-processing/ # LOCAL: Data processing tools
├── deploy/               # LOCAL: Deployment system
│   ├── deploy           # LOCAL: Main CLI (production, simple, build)
│   ├── README.md        # LOCAL: Deploy documentation
│   └── commands/        # LOCAL: Deployment scripts
│
└── ☁️ AUTOMATION SYSTEMS (Future - Will Trigger Local)
    └── ci/               # AUTOMATED: Cross-platform CI/CD (Future)
        ├── README.md     # AUTOMATED: CI/CD overview
        ├── docs/         # AUTOMATED: Implementation plans
        ├── workflows/    # AUTOMATED: GitHub Actions (future)
        ├── automation/   # AUTOMATED: CD automation (future)
        ├── platform-builds/ # AUTOMATED: OS-specific builds (future)
        └── test-matrix/  # AUTOMATED: Multi-platform testing (future)
```

## 🔧 **System Components**

## **🖥️ LOCAL SYSTEMS** (Active Now)

### **Development Operations** (`ops/`) - LOCAL
- **Quality Assurance**: Linting, formatting, type checking, testing
- **Build Management**: Production builds with version tracking
- **Release Management**: Semantic versioning, git tagging, changelog
- **Environment**: Setup, diagnostics, WSL compatibility
- **Status Monitoring**: Project status, targets, environment health

### **Deployment Management** (`deploy/`) - LOCAL
- **Production Builds**: Clean, optimized deployments
- **File Management**: Preserves user files, updates system files
- **Environment Setup**: Virtual environments, dependencies, configuration
- **Multi-target Support**: Deploy to multiple environments

### **Utility Library** (`ops/commands/`) - LOCAL
- **Development Tools**: Feature creation, daily workflows, common utilities
- **Testing Tools**: API testing, test runners, validation scripts
- **Git Tools**: Commit helpers, workflow automation
- **Agent Tools**: AI agent context management, shared memory
- **Data Tools**: CSV processing, contact management, validation

## **☁️ AUTOMATION SYSTEMS** (Future)

### **Cross-Platform CI/CD** (`ci/`) - AUTOMATED
- **Triggers Local Systems**: GitHub Actions will call your local ops/deploy commands
- **Multi-OS Testing**: Linux, macOS, Windows validation
- **Automated Deployment**: CD pipelines that orchestrate local workflow
- **Platform Builds**: OS-specific builds using local deploy system

## **🔗 LOCAL ↔ AUTOMATED Relationship**

**Key Principle**: AUTOMATED systems TRIGGER and ORCHESTRATE LOCAL systems, never replace them.

```bash
# LOCAL: You run these directly (current workflow)
./devops/ops/ops qa
./devops/ops/ops build
./devops/deploy/deploy production

# AUTOMATED: GitHub Actions runs the SAME commands (future workflow)
# GitHub Actions → ./devops/ops/ops qa
# GitHub Actions → ./devops/ops/ops build  
# GitHub Actions → ./devops/deploy/deploy production
```

**Benefits**:
- ✅ **LOCAL systems keep working** exactly as they do now
- ✅ **AUTOMATED systems enhance** rather than replace
- ✅ **Consistent behavior** between manual and automated workflows
- ✅ **Easy testing** - if local works, automated will work

## 📋 **Template Customization**

When copying to a new project:

### 1. Update Configuration
```bash
# Edit target paths and project settings
vim devops/ops/config.yml
```

### 2. Customize for Your Stack
```bash
# Python project: Update QA commands for ruff, mypy, pytest
# Node.js project: Update for eslint, tsc, jest
# Rust project: Update for clippy, cargo test
vim devops/ops/ops
```

### 3. Adapt Build Scripts
```bash
# Customize for your project structure and dependencies
vim devops/deploy/commands/build-production.sh
```

### 4. Configure Deployment Targets
```bash
# Set up your deployment paths
./devops/ops/ops setup ~/deploy/your-project
```

## 🌟 **Key Features**

- **Template-First Design**: Copy entire system to any project
- **Stack Agnostic**: Works with Python, Node.js, Rust, Go, etc.
- **WSL Compatible**: Handles Windows/WSL development environments
- **CI/CD Ready**: Integrates with GitHub Actions and other CI systems
- **Agent Friendly**: Designed for collaboration with AI development agents
- **Solo Founder Optimized**: Simple, powerful, easy to maintain

## 🔗 **Integration Examples**

### Python Project
```bash
# Customize for Python
# - Update QA: ruff, black, mypy, pytest
# - Build: pyproject.toml, requirements.txt
# - Deploy: pip install, .venv setup
```

### Node.js Project  
```bash
# Customize for Node.js
# - Update QA: eslint, prettier, tsc, jest
# - Build: package.json, npm/yarn
# - Deploy: node_modules, pm2 setup
```

### Rust Project
```bash
# Customize for Rust
# - Update QA: clippy, rustfmt, cargo test
# - Build: Cargo.toml, cargo build --release
# - Deploy: target/release, systemd setup
```

## 📚 **Documentation**

- **[ops/README.md](ops/README.md)**: Complete ops system documentation
- **[deploy/README.md](deploy/README.md)**: Deployment system documentation
- **Individual command help**: `./devops/ops/ops help`, `./devops/deploy/deploy help`

## 🎯 **Complete DevOps Workflow**

### **🖥️ LOCAL Workflow** (Current - Active Now)
```bash
# 1. LOCAL: Setup (one time)
./devops/ops/ops setup ~/deploy/your-project

# 2. LOCAL: Daily development
./devops/ops/ops qa          # LOCAL: Quality checks
./devops/ops/ops build       # LOCAL: Build production
./devops/ops/ops verify-prod # LOCAL: Verify build
./devops/ops/ops status      # LOCAL: Check status

# 3. LOCAL: Release
./devops/ops/ops release patch   # LOCAL: Create patch release
./devops/ops/ops release minor   # LOCAL: Create minor release  
./devops/ops/ops release major   # LOCAL: Create major release

# 4. LOCAL: Deploy
./devops/deploy/deploy production ~/deploy/your-project

# 5. LOCAL: Monitor
./devops/ops/ops status      # LOCAL: Project status
./devops/ops/ops env doctor  # LOCAL: Environment diagnostics
```

### **☁️ AUTOMATED Workflow** (Future - Will Trigger Local)
```bash
# AUTOMATED: GitHub Actions will orchestrate your LOCAL commands
git push origin main
# → AUTOMATED: Triggers ./devops/ops/ops qa
# → AUTOMATED: Triggers ./devops/ops/ops build
# → AUTOMATED: Triggers ./devops/deploy/deploy production
# → AUTOMATED: Triggers ./devops/ops/ops release patch

# You still have full LOCAL control when needed
./devops/ops/ops status      # LOCAL: Check what automation did
./devops/ops/ops env doctor  # LOCAL: Diagnose any issues
```

---

**🤖 Template System**: This DevOps system is designed as a reusable template. Copy the entire `devops/` folder to new projects and customize for your specific technology stack and deployment requirements.

### Exporting Example Package
After deploying to the staging target, run:
```
./devops/deploy/deploy export /path/to/multi-agent-template
```
This copies only `agentswarm/` (no tests, caches) into the template repository.

### Portable Configuration (`config/devops.toml`)
When you copy this DevOps folder into a new project, create or edit `config/devops.toml` so the CLI knows which package to manage, how to run tests, and where to deploy:

```toml
[versioning]
package = "example_package"
source = "src/config/package.toml"

[package]
name = "example_package"
path = "src"
test_command = "pytest tests/backend"

[package.manifest]
version = "VERSION"
requirements = "requirements.txt"
install = "install.sh"
cli = "example-cli"

[deploy]
target = "/abs/path/to/project-sync"
subdirectory = "project-sync/agentswarm"
```

The CLI commands (`ops qa`, `ops release`, `deploy production`) now read this file automatically—no script changes required when moving to a new codebase.

After a staging deploy, export the production bundle with the Example Package version:
```
./devops/deploy/deploy export /tmp/multi-agent-template
cat /tmp/multi-agent-template/VERSION  # prints the Example Package version from agentswarm.toml
```
