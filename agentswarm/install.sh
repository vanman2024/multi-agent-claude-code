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
chmod +x 'agentswarm/cli/main.py' || true

echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Environment is already configured (.env created from your development settings)"
if [ -d "venv" ]; then
    echo "2. Activate virtual environment: source venv/bin/activate"
    echo "3. Run: python3 -m agentswarm.cli.main --help"
    echo ""
    echo "Or use the CLI wrapper (automatically handles venv): ./signalhire-agent --help"
else
    echo "2. Run: python3 -m agentswarm.cli.main --help"
    echo ""
    echo "Or use the CLI wrapper: ./signalhire-agent --help"
fi

