# Operations CLI

**Single command interface for all development operations.**

## 🎯 **Main Command: `ops`**

```bash
./scripts/ops <command> [options]
```

### **Daily Workflow Commands**
```bash
ops qa          # Quality checks (lint, format, typecheck, tests)
ops build       # Production build to target directory  
ops verify-prod # Verify production build works
ops release     # Create and push new release
```

### **Setup & Status Commands**
```bash
ops setup       # One-time setup with target directory
ops status      # Show current config, versions, targets
ops env doctor  # Diagnose WSL/environment issues
```

## 🚀 **Example Workflow**

```bash
# One-time setup
ops setup ~/deploy/signalhire

# Daily development  
git add . && git commit -m "feat: add awesome feature"
ops qa

# When ready to deploy
ops build && ops verify-prod && ops release patch
```

## 🔧 **Environment Notes**

- **Virtual Environment**: Uses `.venv` (standard Python convention)
- **Auto-Setup**: Creates `.venv` automatically if missing
- **WSL Compatible**: Detects and handles Windows/WSL path issues

## **Legacy Scripts**

The subdirectories contain older scripts that are being phased out in favor of the unified `ops` command.