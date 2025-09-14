# Gemini CLI - Dual Terminal Configuration

## 🚀 CRITICAL: We Have TWO FREE Gemini Models!

### Terminal Setup - Run Both Models Simultaneously
1. **Terminal 1**: Google OAuth → **Gemini 2.5 Pro** (FREE on personal accounts!)
2. **Terminal 2**: API Key → **Gemini 2.0 Flash Experimental** (FREE during experimental phase!)

## Quick Start

### Terminal 1: Gemini 2.5 Pro (Google OAuth)
```bash
# API keys are commented out in ~/.bashrc by default
gemini
# Choose option 1: Login with Google
# You get Gemini 2.5 Pro FREE on personal accounts!
```

### Terminal 2: Gemini 2.0 Flash Experimental (API Key)
```bash
# Source the setup script for this terminal session only
source /home/gotime2022/bin/gemini-setup-experimental.sh
# Run the experimental model
gemini -m gemini-2.0-flash-exp
```

## Model Comparison

| Model | Auth | Cost | Context | Speed | Best For |
|-------|------|------|---------|-------|----------|
| **2.5 Pro** | Google OAuth | FREE (personal) / $1.25+$10/M (business) | 1M tokens | Slower | Complex reasoning, analysis |
| **2.0 Flash Exp** | API Key | FREE (experimental) | 1M tokens | Fast | Rapid prototyping, agentic tasks |

## Strategic Usage - Maximize Both Models

### Use Gemini 2.0 Flash Experimental For:
- **Rapid iterations** - It's faster and agentic
- **Bulk processing** - Free means no cost concerns
- **Quick questions** - Get instant responses
- **Code generation** - Fast prototyping
- **Testing ideas** - Experiment freely

### Use Gemini 2.5 Pro For:
- **Complex analysis** - When Flash Exp struggles
- **Advanced reasoning** - Sophisticated logic
- **Quality checks** - Verify Flash Exp outputs
- **Critical decisions** - When accuracy matters most
- **Long context** - Full 1M token analysis

### Combine with Claude Code For:
- **Architecture decisions** - Overall system design
- **Multi-file refactoring** - Complex code changes
- **Debugging** - When both Geminis can't solve it
- **Project coordination** - Managing the overall workflow

## Configuration Details

### File Locations
- **Setup Script**: `/home/gotime2022/bin/gemini-setup-experimental.sh`
- **Bashrc**: `~/.bashrc` (lines 192-193 commented out for OAuth)
- **API Key**: `AIzaSyC4mL5xX7DjXVCTDM84SL2DhfU5__JnKTU` (used only in Terminal 2)

### How It Works
1. **Default behavior**: No API keys set → Google OAuth login
2. **Terminal 2 override**: Source script sets API key for that session only
3. **No conflicts**: Each terminal runs independently

## Cost Reality Check

If you were paying for these models:
- **Gemini 2.5 Pro**: $1.25/M input + $10/M output = EXPENSIVE!
- **Gemini 2.0 Flash**: $0.10/M input + $0.40/M output = Still adds up
- **Current cost**: $0.00 - BOTH ARE FREE!

**USE THEM TO THE MAX WHILE THEY'RE FREE!**

## Common Workflows

### Parallel Processing
```bash
# Terminal 1: Complex analysis with 2.5 Pro
gemini -p "Analyze the architecture and suggest improvements"

# Terminal 2: Quick implementation with Flash Exp
gemini -m gemini-2.0-flash-exp -p "Generate the code for this feature"
```

### Sequential Enhancement
1. Start with Flash Exp for rapid prototype
2. Refine with 2.5 Pro for quality
3. Finalize with Claude Code for integration

### Bulk Operations
- Use Flash Exp for all repetitive tasks (it's free!)
- Save 2.5 Pro for complex reasoning tasks
- Let Claude Code handle the orchestration

## Tips & Tricks

### Avoiding Auth Issues
- Never set API keys globally in .bashrc
- Always use the setup script for Terminal 2
- Keep Terminal 1 clean for OAuth

### Maximizing Free Usage
1. Run both terminals simultaneously
2. Use Flash Exp for everything possible
3. Escalate to 2.5 Pro only when needed
4. Save Claude Code for critical tasks

### Error Messages
Those `[ERROR] [ImportProcessor]` messages are harmless - just Gemini looking for optional config files. The CLI still works perfectly.

## When Free Period Ends

Eventually these models won't be free. When that happens:
1. **Gemini 1.5 Flash**: ~$0.075/M tokens (cheapest stable model)
2. **Gemini 1.5 Flash-8b**: ~$0.037/M tokens (even cheaper, smaller)
3. **API keys**: Get your own from https://aistudio.google.com/apikey

But for now - **USE BOTH FREE MODELS TO THE MAXIMUM!**
<!-- AUTO-CONTEXT-START -->

**Current Branch**: main
**Last Updated**: 2025-09-13 22:51:21

### Recent Commits
```
3d28ba5 [WORKING] feat: Major project-sync system implementation
2dd7a25 feat: Integrate spec-kit with test generation and implement commands
ec3fc88 docs: Consolidate documentation from 84 to ~60 files
47b50dc docs: Add quick copy commands to README
57b8533 docs: Add note about global vs project commands
```

<!-- AUTO-CONTEXT-END -->
