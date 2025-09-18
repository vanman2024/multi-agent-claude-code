#!/bin/bash
# Production Build Script for SignalHire Agent
# 
# PURPOSE: Creates clean production deployment with version tracking
# USAGE: ./build-production.sh <target_directory> [--version TAG] [--latest] [--force]
# PART OF: Build and deployment system
# CONNECTS TO: GitHub Actions workflow (.github/workflows/release.yml)
# 
# This script creates production-ready deployments by:
# - Copying only essential application files (src/, docs/, agent instructions)
# - Auto-creating .env with development credentials
# - Removing development files (tests/, specs/, version.py)
# - Creating install.sh with virtual environment support
# - Generating CLI wrapper for easy execution

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[BUILD]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [[ ! -f "CLAUDE.md" ]]; then
    print_error "Must run from signalhireagent repository root"
    exit 1
fi

# Parse command line arguments
TARGET_DIR=""
VERSION_TAG=""
FORCE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --version)
            VERSION_TAG="$2"
            shift 2
            ;;
        --latest)
            VERSION_TAG="latest"
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 <target_directory> [options]"
            echo ""
            echo "Options:"
            echo "  --version TAG    Deploy specific version tag (e.g., v0.2.1)"
            echo "  --latest         Deploy latest version tag"
            echo "  --force          Overwrite existing target directory"
            echo "  -h, --help       Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 ~/Projects/signalhireagenttests2/signalhireagent/"
            echo "  $0 /path/to/staging --version v0.2.1"
            echo "  $0 /path/to/staging --latest --force"
            exit 0
            ;;
        *)
            if [[ -z "$TARGET_DIR" ]]; then
                TARGET_DIR="$1"
            else
                print_error "Unknown option: $1"
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate target directory
if [[ -z "$TARGET_DIR" ]]; then
    print_error "Target directory is required"
    echo "Usage: $0 <target_directory> [--version TAG] [--latest] [--force]"
    exit 1
fi

# Get version information
if [[ "$VERSION_TAG" == "latest" ]]; then
    # Read version from pyproject.toml
    if [[ -f "pyproject.toml" ]]; then
        PYPROJECT_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
        VERSION_TAG="v$PYPROJECT_VERSION"
        print_status "Using version from pyproject.toml: $VERSION_TAG"
        
        # Auto-create/update git tag if it doesn't exist
        if ! git rev-parse "$VERSION_TAG" >/dev/null 2>&1; then
            print_status "Creating git tag: $VERSION_TAG"
            git tag "$VERSION_TAG" 2>/dev/null || print_warning "Could not create git tag (this is okay)"
        fi
    else
        VERSION_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0-dev")
        print_status "No pyproject.toml found, using latest git tag: $VERSION_TAG"
    fi
elif [[ -n "$VERSION_TAG" ]]; then
    # Validate that the version tag exists, or read from pyproject.toml
    if ! git rev-parse "$VERSION_TAG" >/dev/null 2>&1; then
        if [[ -f "pyproject.toml" ]]; then
            PYPROJECT_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
            VERSION_TAG="v$PYPROJECT_VERSION"
            print_status "Version tag not found, using pyproject.toml: $VERSION_TAG"
            
            # Auto-create git tag
            print_status "Creating git tag: $VERSION_TAG"
            git tag "$VERSION_TAG" 2>/dev/null || print_warning "Could not create git tag (this is okay)"
        else
            print_error "Version tag '$VERSION_TAG' does not exist and no pyproject.toml found"
            exit 1
        fi
    fi
    print_status "Using specified version: $VERSION_TAG"
else
    # Read version from pyproject.toml first, fallback to git
    if [[ -f "pyproject.toml" ]]; then
        PYPROJECT_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
        VERSION_TAG="v$PYPROJECT_VERSION"
        print_status "Using version from pyproject.toml: $VERSION_TAG"
        
        # Auto-create git tag if it doesn't exist
        if ! git rev-parse "$VERSION_TAG" >/dev/null 2>&1; then
            print_status "Creating git tag: $VERSION_TAG"
            git tag "$VERSION_TAG" 2>/dev/null || print_warning "Could not create git tag (this is okay)"
        fi
    else
        # Fallback to git describe
        VERSION_TAG=$(git describe --tags --dirty 2>/dev/null || echo "v0.0.0-dev-$(git rev-parse --short HEAD)")
        print_status "No pyproject.toml found, using git describe: $VERSION_TAG"
    fi
fi

# Get commit hash for version tracking
COMMIT_HASH=$(git rev-parse HEAD)
BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

print_status "Building production deployment..."
print_status "  Version: $VERSION_TAG"
print_status "  Commit:  $COMMIT_HASH"
print_status "  Target:  $TARGET_DIR"

# Check if target directory exists
# Preserve selected files/directories before overwriting target
preserve_backup=""
preserve_paths=(
  "CLAUDE.md"
  "AGENTS.md"
  "MULTI_AGENT_INTEGRATION_SUMMARY.md"
  "QUICK_DEPLOYMENT_GUIDE.md"
  "docs"
  ".claude"
  ".codex"
  ".gemini"
  ".qwen"
)

if [[ -d "$TARGET_DIR" ]]; then
    if [[ "$FORCE" == "true" ]]; then
        print_warning "Backing up agent documentation before overwrite"
        preserve_backup=$(mktemp -d)
        for path in "${preserve_paths[@]}"; do
            if [[ -d "$TARGET_DIR/$path" ]]; then
                rsync -a "$TARGET_DIR/$path/" "$preserve_backup/$path/"
            elif [[ -f "$TARGET_DIR/$path" ]]; then
                mkdir -p "$(dirname "$preserve_backup/$path")"
                cp -a "$TARGET_DIR/$path" "$preserve_backup/$path"
            fi
        done

        print_warning "Removing existing target directory"
        rm -rf "$TARGET_DIR"
    else
        print_error "Target directory already exists. Use --force to overwrite."
        exit 1
    fi
fi

# Create target directory
mkdir -p "$TARGET_DIR"

# Determine source directory (src/ for SignalHire, agentswarm/ for AgentSwarm package)
SOURCE_DIR="src"
if [[ ! -d "src" && -d "agentswarm" ]]; then
    SOURCE_DIR="agentswarm"
fi
if [[ "$SOURCE_DIR" == "src" ]]; then
    PACKAGE_MODULE="src"
else
    PACKAGE_MODULE="agentswarm"
fi

print_status "Copying application files from $SOURCE_DIR..."

# Core application code (excluding development metadata)
print_status "Copying source code (excluding development files)..."
if command -v rsync >/dev/null 2>&1; then
    rsync -av --exclude='tests/' --exclude='*.egg-info' --exclude='__pycache__' --exclude='*.pyc' --exclude='*.pyo' "$SOURCE_DIR"/ "$TARGET_DIR/$SOURCE_DIR/"
else
    # Fallback to cp if rsync not available
    cp -r "$SOURCE_DIR"/ "$TARGET_DIR/$SOURCE_DIR/"
    print_warning "rsync not available, using cp (will clean up development files afterward)"
fi

# Clean up any development files that might exist in target
print_status "Cleaning up development files from target..."
find "$TARGET_DIR/$SOURCE_DIR" -name "tests" -type d -exec rm -rf {} + 2>/dev/null || true
find "$TARGET_DIR/$SOURCE_DIR" -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
find "$TARGET_DIR/$SOURCE_DIR" -name "*.egg-info" -type d -exec rm -rf {} + 2>/dev/null || true
find "$TARGET_DIR/$SOURCE_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$TARGET_DIR/$SOURCE_DIR" -name "*.pyc" -delete 2>/dev/null || true
find "$TARGET_DIR/$SOURCE_DIR" -name "*.pyo" -delete 2>/dev/null || true

# Essential configuration and documentation
cp README.md "$TARGET_DIR/" 2>/dev/null || true
cp QUICKSTART.md "$TARGET_DIR/" 2>/dev/null || true
cp LICENSE "$TARGET_DIR/" 2>/dev/null || true

# AI agent instruction files (required for multi-agent workflows)
print_status "Copying agent instruction files..."
mkdir -p "$TARGET_DIR/.github"
cp -r .github/copilot-instructions.md "$TARGET_DIR/.github/" 2>/dev/null || true

agent_files=(
  "CLAUDE.md"
  "AGENTS.md"
  "MULTI_AGENT_INTEGRATION_SUMMARY.md"
  "QUICK_DEPLOYMENT_GUIDE.md"
  "docs/cli-commands.md"
)

agent_directories=(
  ".claude"
  ".codex"
  ".gemini"
  ".qwen"
)

for agent_file in "${agent_files[@]}"; do
    if [[ -e "$agent_file" ]]; then
        target_path="$TARGET_DIR/$agent_file"
        mkdir -p "$(dirname "$target_path")"
        cp "$agent_file" "$target_path"
    fi
done

for agent_dir in "${agent_directories[@]}"; do
    if [[ -d "$agent_dir" ]]; then
        rsync -a "$agent_dir/" "$TARGET_DIR/$agent_dir/" 2>/dev/null || cp -r "$agent_dir" "$TARGET_DIR/$agent_dir"
    fi
done

# Restore preserved files/directories if they existed in the target
if [[ -n "$preserve_backup" && -d "$preserve_backup" ]]; then
    print_status "Restoring preserved agent documentation..."
    for path in "${preserve_paths[@]}"; do
        if [[ -d "$preserve_backup/$path" ]]; then
            mkdir -p "$TARGET_DIR/$path"
            cp -a "$preserve_backup/$path/." "$TARGET_DIR/$path/"
        elif [[ -f "$preserve_backup/$path" ]]; then
            mkdir -p "$(dirname "$TARGET_DIR/$path")"
            cp -a "$preserve_backup/$path" "$TARGET_DIR/$path"
        fi
    done
    rm -rf "$preserve_backup"
fi

# Create production requirements.txt (without dev dependencies)
print_status "Creating production requirements.txt..."
if [[ "$SOURCE_DIR" == "src" ]]; then
cat > "$TARGET_DIR/requirements.txt" << EOF
# SignalHire Agent Production Dependencies
# Generated on $BUILD_DATE

# Core async HTTP client
httpx>=0.25.0

# Data validation and models
pydantic>=2.0.0
pydantic-settings>=2.0.0

# Web framework for callback server
fastapi>=0.100.0
uvicorn>=0.20.0

# Data processing and CSV export
pandas>=2.0.0

# CLI framework
click>=8.1.0
rich>=13.0.0

# Configuration management
python-dotenv>=1.0.0

# Logging and monitoring
structlog>=23.0.0

# Async utilities
anyio>=3.6.0

# Email validation
email-validator>=2.0.0
EOF
else
cat > "$TARGET_DIR/requirements.txt" << EOF
# AgentSwarm Production Dependencies
# Generated on $BUILD_DATE

click>=8.1.0
pyyaml>=6.0
psutil>=5.9.0
rich>=13.0.0
asyncio-mqtt>=0.11.0
tomli>=2.0.0
EOF
fi

# Create version information file
print_status "Creating version information..."
cat > "$TARGET_DIR/VERSION" << EOF
{
  "version": "$VERSION_TAG",
  "commit": "$COMMIT_HASH", 
  "build_date": "$BUILD_DATE",
  "build_type": "production"
}
EOF

# Create production .env template with actual values from source
print_status "Creating .env template..."

# Check if source .env exists and copy actual values
if [[ -f ".env" ]]; then
    print_status "Found source .env file, copying actual values to template..."
    
    # Extract actual values from source .env
    ACTUAL_API_KEY=$(grep "^SIGNALHIRE_API_KEY=" .env 2>/dev/null | cut -d'=' -f2- || echo "your_api_key_here")
    ACTUAL_EMAIL=$(grep "^SIGNALHIRE_EMAIL=" .env 2>/dev/null | cut -d'=' -f2- || echo "your_email@example.com")
    ACTUAL_PASSWORD=$(grep "^SIGNALHIRE_PASSWORD=" .env 2>/dev/null | cut -d'=' -f2- || echo "your_password_here")
    ACTUAL_BASE_URL=$(grep "^SIGNALHIRE_API_BASE_URL=" .env 2>/dev/null | cut -d'=' -f2- || echo "https://www.signalhire.com")
    ACTUAL_PREFIX=$(grep "^SIGNALHIRE_API_PREFIX=" .env 2>/dev/null | cut -d'=' -f2- || echo "/api/v1")
    ACTUAL_RATE_LIMIT=$(grep "^RATE_LIMIT_REQUESTS_PER_MINUTE=" .env 2>/dev/null | cut -d'=' -f2- || echo "600")
    ACTUAL_REVEAL_LIMIT=$(grep "^DAILY_REVEAL_LIMIT=" .env 2>/dev/null | cut -d'=' -f2- || echo "5000")
    ACTUAL_SEARCH_LIMIT=$(grep "^DAILY_SEARCH_PROFILE_LIMIT=" .env 2>/dev/null | cut -d'=' -f2- || echo "5000")
    
    # Create .env.example as template
    cat > "$TARGET_DIR/.env.example" << EOF
# SignalHire Agent Configuration
# Copy this to .env and add your actual values

# SignalHire credentials
SIGNALHIRE_API_KEY=your_api_key_here
SIGNALHIRE_EMAIL=your_email@example.com
SIGNALHIRE_PASSWORD=your_password_here

# Optional: API Configuration
SIGNALHIRE_API_BASE_URL=https://www.signalhire.com
SIGNALHIRE_API_PREFIX=/api/v1

# Optional: Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=600
DAILY_REVEAL_LIMIT=5000
DAILY_SEARCH_PROFILE_LIMIT=5000
EOF

    # Create .env with actual values
    cat > "$TARGET_DIR/.env" << EOF
# SignalHire Agent Configuration
# Auto-generated from development environment

# SignalHire credentials
SIGNALHIRE_API_KEY=$ACTUAL_API_KEY
SIGNALHIRE_EMAIL=$ACTUAL_EMAIL
SIGNALHIRE_PASSWORD=$ACTUAL_PASSWORD

# Optional: API Configuration  
SIGNALHIRE_API_BASE_URL=$ACTUAL_BASE_URL
SIGNALHIRE_API_PREFIX=$ACTUAL_PREFIX

# Optional: Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=$ACTUAL_RATE_LIMIT
DAILY_REVEAL_LIMIT=$ACTUAL_REVEAL_LIMIT
DAILY_SEARCH_PROFILE_LIMIT=$ACTUAL_SEARCH_LIMIT
EOF

    # Remove .env.example after creating .env
    rm "$TARGET_DIR/.env.example"
else
    print_warning "No source .env file found, creating template with default values..."
    cat > "$TARGET_DIR/.env.example" << EOF
# SignalHire Agent Configuration
# Copy this to .env and add your actual values

# SignalHire credentials
SIGNALHIRE_API_KEY=your_api_key_here
SIGNALHIRE_EMAIL=your_email@example.com
SIGNALHIRE_PASSWORD=your_password_here

# Optional: API Configuration
SIGNALHIRE_API_BASE_URL=https://www.signalhire.com
SIGNALHIRE_API_PREFIX=/api/v1

# Optional: Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=600
DAILY_REVEAL_LIMIT=5000
DAILY_SEARCH_PROFILE_LIMIT=5000
EOF

    # Create .env with same template values (user will need to update)
    cp "$TARGET_DIR/.env.example" "$TARGET_DIR/.env"
    
    # Remove .env.example after creating .env
    rm "$TARGET_DIR/.env.example"
fi

CLI_MODULE="$PACKAGE_MODULE"

# Create simple deployment script
print_status "Creating deployment utilities..."
cat > "$TARGET_DIR/install.sh" << 'EOF'
#!/bin/bash
# SignalHire Agent Installation Script
#
# PURPOSE: Set up a working Python environment (venv if available) and install production dependencies
# USAGE: ./install.sh
# PART OF: Production deployment package
# CONNECTS TO: signalhire-agent CLI wrapper, requirements.txt

set -euo pipefail

echo "Installing SignalHire Agent..."

# Detect non-interactive/CI mode
NONINTERACTIVE=${NONINTERACTIVE:-}
if [ -n "${CI:-}" ] && [ "${CI}" = "true" ]; then
  NONINTERACTIVE=1
fi

# Force WSL Python (avoid Windows Python in WSL)
PYTHON_CMD="python3"
if [ -n "${WSL_DISTRO_NAME:-}" ] && command -v /usr/bin/python3 >/dev/null 2>&1; then
    PYTHON_CMD="/usr/bin/python3"
    echo "WSL detected, using WSL Python: $PYTHON_CMD"
fi

# Check Python version
if ! $PYTHON_CMD --version | grep -E "3\.(9|10|11|12)" > /dev/null; then
    echo "Error: Python 3.9+ required"
    exit 1
fi

# Check if python3-venv is available by testing venv creation
if $PYTHON_CMD -m venv test_venv_check > /dev/null 2>&1; then
    rm -rf test_venv_check > /dev/null 2>&1
    VENV_AVAILABLE=1
else
    VENV_AVAILABLE=0
fi

if [ "$VENV_AVAILABLE" -eq 1 ]; then
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment with $PYTHON_CMD..."
        $PYTHON_CMD -m venv venv
    fi
    # Activate virtual environment and install dependencies
    echo "Installing dependencies in virtual environment..."
    # shellcheck disable=SC1091
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "python3-venv not available. Falling back to user installation."
    if [ -n "${NONINTERACTIVE:-}" ]; then
        echo "Non-interactive mode: installing dependencies with --user"
        pip3 install --upgrade --user pip || true
        if ! pip3 install --user -r requirements.txt; then
            echo "--user install failed; attempting system install with --break-system-packages"
            pip3 install -r requirements.txt --break-system-packages
        fi
    else
        echo "Please install python3-venv (e.g., sudo apt install python3.12-venv)"
        echo "Or rerun in non-interactive mode: NONINTERACTIVE=1 ./install.sh"
        exit 1
    fi
fi

# Make CLI executable (if using direct execution)
chmod +x '__SOURCE_DIR__/cli/main.py' || true

echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Environment is already configured (.env created from your development settings)"
if [ -d "venv" ]; then
    echo "2. Activate virtual environment: source venv/bin/activate"
    echo "3. Run: python3 -m __MODULE__.cli.main --help"
    echo ""
    echo "Or use the CLI wrapper (automatically handles venv): ./signalhire-agent --help"
else
    echo "2. Run: python3 -m __MODULE__.cli.main --help"
    echo ""
    echo "Or use the CLI wrapper: ./signalhire-agent --help"
fi

EOF

chmod +x "$TARGET_DIR/install.sh"
sed -i "s|__SOURCE_DIR__|$SOURCE_DIR|g" "$TARGET_DIR/install.sh"
sed -i "s|__MODULE__|$PACKAGE_MODULE|g" "$TARGET_DIR/install.sh"

# Version information is available via VERSION file (JSON format)
# No version.py utility needed in production deployment

# Create simple CLI wrapper (optional)
cat > "$TARGET_DIR/signalhire-agent" <<'EOF'
#!/bin/bash
# SignalHire Agent CLI Wrapper

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Force WSL Python (avoid Windows Python in WSL)
PYTHON_CMD="python3"
if [ -n "${WSL_DISTRO_NAME:-}" ] && command -v /usr/bin/python3 >/dev/null 2>&1; then
    PYTHON_CMD="/usr/bin/python3"
fi

# Check if virtual environment exists and use it
if [ -d "$SCRIPT_DIR/venv" ]; then
    # shellcheck disable=SC1091
    source "$SCRIPT_DIR/venv/bin/activate"
    # After activation, pick up the venv python
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_CMD="$(command -v python3)"
    fi
fi

export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Load .env if it exists
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

# Run the CLI with correct Python
$PYTHON_CMD -m __MODULE__.cli.main "$@"
EOF

chmod +x "$TARGET_DIR/signalhire-agent"
sed -i "s|__MODULE__|$PACKAGE_MODULE|g" "$TARGET_DIR/signalhire-agent"

if [[ "$SOURCE_DIR" != "src" ]]; then
    mkdir -p "$TARGET_DIR/$SOURCE_DIR"
    for file in VERSION BUILD_INFO.md install.sh requirements.txt; do
        if [[ -f "$TARGET_DIR/$file" ]]; then
            mv "$TARGET_DIR/$file" "$TARGET_DIR/$SOURCE_DIR/$file"
        fi
    done
    if [[ -f "$TARGET_DIR/signalhire-agent" ]]; then
        mv "$TARGET_DIR/signalhire-agent" "$TARGET_DIR/$SOURCE_DIR/agentswarm"
    fi
fi

# Generate build manifest
print_status "Creating build manifest..."
cat > "$TARGET_DIR/BUILD_INFO.md" << EOF
# SignalHire Agent Production Build

**Version:** $VERSION_TAG  
**Commit:** $COMMIT_HASH  
**Built:** $BUILD_DATE  
**Build Type:** Production

## Files Included
- \`$SOURCE_DIR/\` - Core application code
- \`$SOURCE_DIR/requirements.txt\` - Production dependencies only
- \`$SOURCE_DIR/VERSION\` - Version information (JSON)
- \`$SOURCE_DIR/install.sh\` - Installation script
- \`$SOURCE_DIR/agentswarm\` - CLI wrapper script
- \`.env\` - Production environment file (automatically created with your credentials)
- Essential documentation files only (README, QUICKSTART, etc.)
- \`.github/copilot-instructions.md\` - GitHub Copilot instructions
- \`docs/cli-commands.md\` - Complete CLI command reference for agents

## Files Excluded (Development Only)
- \`tests/\` - Test suite
- \`specs/\` - Development specifications  
- \`.pytest_cache/\` - Test cache
- \`pyproject.toml\` - Development configuration
- \`TESTING_AND_RELEASE.md\` - Development workflow guide
- \`version.py\` - Development version utility (not needed in production)
- \`*.egg-info/\` - Python package development metadata
- \`__pycache__/\` - Python bytecode cache
- \`*.pyc\`, \`*.pyo\` - Compiled Python files
- Development scripts and tools

## Installation
1. Run \`./install.sh\`
2. Environment is already configured (.env automatically created)
3. Test: \`./signalhire-agent --help\`

## Version Check
Check \`$SOURCE_DIR/VERSION\` file for build information (JSON format).
EOF

# Final verification
print_status "Verifying build..."

# Check that essential files exist
if [[ "$SOURCE_DIR" == "src" ]]; then
    ESSENTIAL_FILES=(
        "src/cli/main.py"
        "src/services/signalhire_client.py"
        "requirements.txt"
        "VERSION"
        "install.sh"
    )
else
    ESSENTIAL_FILES=(
        "$SOURCE_DIR/cli/main.py"
        "$SOURCE_DIR/core/orchestrator.py"
        "$SOURCE_DIR/config/agentswarm.toml"
        "$SOURCE_DIR/VERSION"
        "$SOURCE_DIR/install.sh"
    )
fi

for file in "${ESSENTIAL_FILES[@]}"; do
    if [[ ! -f "$TARGET_DIR/$file" ]]; then
        print_error "Missing essential file: $file"
        exit 1
    fi
done

# Get directory size
BUILD_SIZE=$(du -sh "$TARGET_DIR" | cut -f1)

print_success "Production build completed successfully!"
print_success "  Location: $TARGET_DIR"
print_success "  Version:  $VERSION_TAG"
print_success "  Size:     $BUILD_SIZE"
print_success ""
print_success "Next steps:"
print_success "  cd $TARGET_DIR"
print_success "  ./install.sh"
print_success "  ./signalhire-agent --help"
print_success ""
print_success "Environment is ready to use! (.env automatically created with your credentials)"

# Check if this directory is configured for auto-sync
AUTO_SYNC_CONFIG="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/auto-sync-config.sh"
if [[ -f "$AUTO_SYNC_CONFIG" ]]; then
    # Convert target to absolute path for comparison
    TARGET_ABS="$(realpath "$TARGET_DIR")"
    CONFIG_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/.auto-sync-targets"
    
    if [[ -f "$CONFIG_FILE" ]] && grep -q "^$TARGET_ABS$" "$CONFIG_FILE"; then
        print_success ""
        print_success "🔄 This directory is configured for auto-sync!"
        print_success "Future commits will automatically update this deployment."
    else
        print_success ""
        print_warning "💡 Want automatic updates? Add this directory to auto-sync:"
        print_warning "   $AUTO_SYNC_CONFIG add $TARGET_DIR"
    fi
fi
