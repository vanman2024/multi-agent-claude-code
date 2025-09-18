#!/bin/bash
# Simple build script for signalhireagent
set -e

cd "$(dirname "$0")/.."

echo "🔨 Building signalhireagent..."

# Activate virtual environment
if [[ -f ".venv/bin/activate" ]]; then
    echo "📦 Activating .venv virtual environment..."
    source .venv/bin/activate
elif [[ -f "venv/bin/activate" ]]; then
    echo "📦 Activating venv virtual environment..."
    source venv/bin/activate
else
    echo "⚠️ No virtual environment found - creating .venv..."
    python3 -m venv .venv
    source .venv/bin/activate
fi

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -e .[dev]

# Lint and fix issues  
echo "🧹 Linting code..."
ruff check src/ --fix || true

# Type check
echo "🔍 Type checking..."
mypy src/ || true

# Basic import test using run.py (proper way)
echo "✅ Testing imports..."
python3 run.py -c "print('✅ Imports working!')"

echo "✅ Build complete!"