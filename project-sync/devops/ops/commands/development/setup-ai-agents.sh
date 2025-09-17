#!/bin/bash
# Setup script for AI coding agents (Qwen, DeepSeek)

set -e

echo "🤖 Setting up AI Coding Agents for SignalHire Agent Project"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "📦 Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    
    echo "🚀 Starting Ollama service..."
    ollama serve &
    sleep 5
else
    echo "✅ Ollama already installed"
fi

# Install recommended models
echo "📥 Installing AI coding models..."

models=(
    "qwen2.5-coder:1.5b"  # Fast, good for quick tasks
    "qwen2.5-coder:7b"    # Balanced performance
    "deepseek-coder:1.3b" # Ultra-fast
    "deepseek-coder:6.7b" # Good performance
)

for model in "${models[@]}"; do
    echo "Installing $model..."
    if ollama list | grep -q "$model"; then
        echo "✅ $model already installed"
    else
        ollama pull "$model" && echo "✅ $model installed" || echo "❌ Failed to install $model"
    fi
done

# Make CLI executable
chmod +x src/cli/ai_agents.py

# Install required Python packages if not present
echo "📦 Installing required packages..."
python3 -c "import httpx, click" 2>/dev/null || pip install httpx click

echo ""
echo "🎉 AI Agents setup complete!"
echo ""
echo "Usage examples:"
echo "  python3 src/cli/ai_agents.py qwen 'Create a function to validate email addresses'"
echo "  python3 src/cli/ai_agents.py deepseek 'Optimize this algorithm' --file src/services/browser_client.py"
echo "  python3 src/cli/ai_agents.py analyze src/lib/common.py 'Find potential performance improvements'"
echo ""
echo "Integration with @symbol system:"
echo "  - [ ] T060 @qwen Optimize search algorithm performance"
echo "  - [ ] T061 @deepseek Refactor browser automation code"