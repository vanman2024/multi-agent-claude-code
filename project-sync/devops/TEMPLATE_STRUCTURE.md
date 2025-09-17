# DevOps Template Structure Guide

**Standardized structure for consistent DevOps + Testing integration across projects.**

## 🎯 **Template Standard Structure**

When copying this DevOps system to new projects, use this **standardized structure**:

```
your-project/
├── src/                       # Application source code
├── devops/                    # DevOps system (copy entire folder)
│   ├── ops/                   # LOCAL: Development workflow
│   ├── deploy/                # LOCAL: Deployment system
│   └── ci/                    # AUTOMATED: Future automation (triggers LOCAL)
└── tests/                     # Testing system (standardized)
    ├── backend/               # Backend tests (STANDARD)
    │   ├── unit/              # Unit tests (functions, classes)
    │   ├── integration/       # Integration tests (APIs, databases)
    │   ├── contract/          # Contract tests (external services)
    │   ├── performance/       # Performance tests (load, stress)
    │   └── smoke/             # Smoke tests (basic functionality)
    └── frontend/              # Frontend tests (STANDARD)
        ├── unit/              # Unit tests (components, hooks, utils)
        ├── integration/       # Integration tests (component interaction)
        ├── e2e/               # End-to-end tests (user journeys)
        ├── visual/            # Visual regression tests (screenshots)
        └── accessibility/     # Accessibility tests (WCAG compliance)
```

## 🔧 **DevOps + Testing Integration**

### **How `ops qa` Works with Testing**

The DevOps `ops qa` command automatically detects and runs your test structure:

```bash
./devops/ops/ops qa --backend
# → Detects tests/backend/ structure
# → Runs: pytest tests/backend/ -m "not slow"

./devops/ops/ops qa --frontend  
# → Detects tests/frontend/ structure
# → Runs: npm run test:frontend

./devops/ops/ops qa --all
# → Runs both backend and frontend tests
```

### **Testing Flow → DevOps Flow**

```bash
# Complete workflow: Testing → OPS → Deploy
./devops/ops/ops qa              # 1. Run tests (unit, integration, etc.)
./devops/ops/ops build           # 2. Build production (if tests pass)
./devops/ops/ops verify-prod     # 3. Verify build works
./devops/deploy/deploy production # 4. Deploy to production
./devops/ops/ops release patch   # 5. Create release
```

## 📋 **Migration Guide**

### **From Legacy Structure** (e.g., SignalHire current)
```bash
# Current SignalHire structure:
tests/
├── backend/
│   ├── unit/
│   ├── integration/
│   └── ...
└── frontend/

# Already compatible! ✅
# DevOps ops qa will detect tests/backend/ automatically
```

### **From Flat Structure** (e.g., tests/unit/, tests/integration/)
```bash
# Legacy flat structure:
tests/
├── unit/
├── integration/
└── contract/

# Migration option 1: Reorganize (recommended)
mkdir -p tests/backend
mv tests/unit tests/backend/
mv tests/integration tests/backend/
mv tests/contract tests/backend/

# Migration option 2: DevOps handles both (automatic fallback)
# DevOps ops qa will detect legacy structure and run both
```

## 🎨 **Customization by Project Type**

### **Backend-Only Projects** (APIs, CLI tools)
```bash
your-project/
├── src/
├── devops/
└── tests/
    └── backend/               # Only backend tests needed
        ├── unit/
        ├── integration/
        └── contract/
```

### **Frontend-Only Projects** (React, Vue apps)
```bash
your-project/
├── src/
├── devops/
└── tests/
    └── frontend/              # Only frontend tests needed
        ├── e2e/
        ├── integration/
        └── visual/
```

### **Full-Stack Projects**
```bash
your-project/
├── src/
├── devops/
└── tests/
    ├── backend/               # Backend API tests
    └── frontend/              # Frontend UI tests
```

## 🔗 **DevOps Configuration**

The DevOps system automatically adapts to your test structure:

### **Backend Testing** (`devops/ops/ops qa --backend`)
- **Python**: Uses `pytest` with your existing test structure
- **Node.js**: Can be customized to use `jest`, `mocha`, etc.
- **Rust**: Can be customized to use `cargo test`
- **Go**: Can be customized to use `go test`

### **Frontend Testing** (`devops/ops/ops qa --frontend`)
- **React**: Uses `npm run test:frontend` (customize in package.json)
- **Vue**: Uses `npm run test:frontend` 
- **Angular**: Uses `npm run test:frontend`
- **Playwright**: Integrated frontend testing suite included

### **Configuration File** (`devops/ops/config.yml`)
```yaml
# Template: Customize for your project
qa:
  lint: true                   # Enable linting
  typecheck: true              # Enable type checking
  tests: "not slow"            # Test selection (customize)
  backend_test_path: "tests/backend"     # Backend test path
  frontend_test_path: "tests/frontend"   # Frontend test path
```

## ✅ **Template Checklist**

When copying DevOps to a new project:

### **1. Copy DevOps System**
```bash
cp -r signalhireagent/devops/ your-project/devops/
```

### **2. Standardize Test Structure**
```bash
# Ensure tests/ follows standard structure
mkdir -p tests/backend tests/frontend
```

### **3. Update Configuration**
```bash
# Edit devops/ops/config.yml for your project
vim devops/ops/config.yml
```

### **4. Customize for Your Stack**
```bash
# Update QA commands in devops/ops/ops
vim devops/ops/ops
```

### **5. Test Integration**
```bash
# Verify DevOps + Testing works
./devops/ops/ops qa
./devops/ops/ops build
./devops/ops/ops verify-prod
```

---

**🎯 Key Principle**: The DevOps system **integrates with** your testing structure rather than **replacing** it. Your tests continue to work exactly as they do now, while DevOps provides the **workflow orchestration** around them.