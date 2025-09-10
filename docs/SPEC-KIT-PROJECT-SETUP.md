# Spec-Kit Project Setup Guide (Linux/WSL)

## Proper Project Initialization with spec-kit

### Directory Structure Understanding (WSL-Specific)
- **Windows Path**: `C:\Users\angel\`
- **WSL Path**: `/mnt/c/Users/angel/`
- **WSL Home**: `/home/gotime2022/` (Linux-only, faster but not visible in Windows Explorer)

## Option 1: Windows Directory (WSL - Cross-Platform Access)

### ⚠️ CRITICAL: Proper Project Initialization

**WRONG WAY** (Creates nested git repo issues):
```bash
cd /mnt/c/Users/angel/Projects
git clone https://github.com/github/spec-kit.git
cd spec-kit  # ❌ DON'T go into spec-kit!
uvx --from git+https://github.com/github/spec-kit.git specify init my-app
# This creates: spec-kit/my-app/ (NESTED - scripts will break!)
```

**CORRECT WAY** (Creates independent project):
```bash
cd /mnt/c/Users/angel/Projects
# Stay in Projects directory, DO NOT cd into spec-kit
uvx --from git+https://github.com/github/spec-kit.git specify init my-app
cd my-app  # Now enter your new project
# This creates: Projects/my-app/ (INDEPENDENT - scripts work properly!)
```

### Full Correct Setup:
```bash
# Navigate to your Windows user directory from WSL
cd /mnt/c/Users/angel

# Create a Projects folder if it doesn't exist
mkdir -p Projects
cd Projects

# Option A: Use spec-kit tools WITHOUT cloning (RECOMMENDED)
uvx --from git+https://github.com/github/spec-kit.git specify init my-photo-app
cd my-photo-app

# Option B: If you need spec-kit source for reference
git clone https://github.com/github/spec-kit.git
# But DON'T cd into it before creating new projects!
```

**Benefits**:
- ✅ Accessible from Windows Explorer at `C:\Users\angel\Projects\my-photo-app`
- ✅ Can edit with Windows editors (VS Code, etc.)
- ✅ Works with both WSL and Windows tools
- ✅ Each project gets its own git repository
- ✅ Scripts use correct relative paths

**Drawbacks**:
- ⚠️ Slightly slower file operations due to WSL-Windows bridge
- ⚠️ May have line ending issues (use `.gitattributes`)

## Option 2: Pure Linux/WSL Home Directory (Better Performance)

### ⚠️ CRITICAL: Same Rule Applies Here!

**WRONG WAY**:
```bash
cd ~/Projects
git clone https://github.com/github/spec-kit.git
cd spec-kit  # ❌ DON'T do this!
uvx --from git+https://github.com/github/spec-kit.git specify init my-app
```

**CORRECT WAY**:
```bash
# Navigate to WSL home Projects
cd ~/Projects  # or /home/gotime2022/Projects

# Create new project directly (DON'T clone spec-kit first)
uvx --from git+https://github.com/github/spec-kit.git specify init my-photo-app
cd my-photo-app
```

**Benefits**:
- ✅ Much faster file operations
- ✅ Native Linux permissions
- ✅ Better for heavy development work

**Drawbacks**:
- ⚠️ Not directly visible in Windows Explorer
- ⚠️ Need to access via `\\wsl$\Ubuntu\home\gotime2022\Projects` in Windows

## Setting Up spec-kit with Claude Code

### 1. Prerequisites Check
```bash
# Check Python version (need 3.11+)
python3 --version

# Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh

# Check uv installation
uv --version
```

### 2. Initialize spec-kit Project
```bash
# From your chosen directory
uvx --from git+https://github.com/github/spec-kit.git specify init photo-organizer

# This creates:
# - photo-organizer/
#   ├── .specify/
#   │   ├── spec.md        # Your application specification
#   │   ├── plan.md        # Technical implementation plan
#   │   └── tasks.md       # Breakdown of implementation tasks
#   └── ... (implementation files)
```

### 3. Using with Claude Code

In Claude Code, use these commands:

```bash
# Create specification
/specify Build a photo organization app with albums grouped by date

# Create technical plan
/plan Use Vite, vanilla HTML/CSS/JS, SQLite for metadata

# Generate tasks
/tasks

# Implement features
# Claude Code will read the spec files and implement accordingly
```

## Directory Navigation Tips

### From WSL to Windows Directories:
```bash
# Go to Windows C: drive
cd /mnt/c/

# Go to your Windows user folder
cd /mnt/c/Users/angel/

# Go to Windows Desktop
cd /mnt/c/Users/angel/Desktop/

# Go to Windows Documents
cd /mnt/c/Users/angel/Documents/
```

### From Windows to WSL Directories:
In Windows Explorer, type in address bar:
- `\\wsl$` - See all WSL distributions
- `\\wsl$\Ubuntu\home\gotime2022` - Your WSL home
- `\\wsl$\Ubuntu\home\gotime2022\Projects` - Your WSL projects

### VS Code Integration:
```bash
# Open current directory in VS Code from WSL
code .

# Open specific project
code /mnt/c/Users/angel/Projects/spec-kit
```

## Best Practices

1. **For spec-kit specifically**: Use `/mnt/c/Users/angel/Projects/` 
   - Easier to access specs from Windows
   - Can use Windows tools alongside WSL

2. **Line Endings**: Create `.gitattributes`:
   ```
   * text=auto
   *.sh text eol=lf
   *.py text eol=lf
   ```

3. **Permissions**: If you get permission errors:
   ```bash
   # Fix permissions for Windows directories in WSL
   sudo chmod -R 755 /mnt/c/Users/angel/Projects/spec-kit
   ```

## Quick Start Commands

### ✅ CORRECT Complete Setup:
```bash
# Navigate to Projects directory
cd /mnt/c/Users/angel/
mkdir -p Projects && cd Projects

# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env  # or restart terminal

# Create your spec-driven project DIRECTLY (not inside spec-kit!)
uvx --from git+https://github.com/github/spec-kit.git specify init my-app
cd my-app

# Start developing with Claude Code
code .
```

### ❌ AVOID This Common Mistake:
```bash
# DON'T DO THIS:
cd Projects
git clone https://github.com/github/spec-kit.git
cd spec-kit  # ← THIS IS THE MISTAKE!
uvx specify init my-app  # Creates nested project with broken scripts
```

### 🔍 How to Check if You Did It Right:
```bash
# From your project directory, run:
git rev-parse --show-toplevel

# GOOD: Should show /mnt/c/Users/angel/Projects/my-app
# BAD:  If it shows /mnt/c/Users/angel/Projects/spec-kit, you nested it!
```

### 🔧 If You Already Made the Mistake:
The scripts will use the wrong paths. You'll need to either:
1. Move your project out of spec-kit and make it independent
2. Or update all scripts to use relative paths instead of git root

Now you can use `/specify`, `/plan`, and `/tasks` commands in Claude Code!