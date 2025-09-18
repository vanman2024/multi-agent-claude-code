# Gemini Agent Instructions

## Agent Identity: @gemini (Google Gemini - Large-Scale Analysis)

### 🚀 DUAL MODEL CONFIGURATION - BOTH FREE!

#### Terminal 1: Gemini 2.5 Pro (Google OAuth)
- **Cost**: FREE on personal accounts (1000 requests/day)
- **Access**: Login with Google account
- **Best for**: Complex reasoning, advanced analysis

#### Terminal 2: Gemini 2.0 Flash Experimental (API Key)
- **Cost**: FREE during experimental phase
- **Access**: API key authentication
- **Best for**: Fast responses, bulk processing, agentic tasks

### 🔄 Checkpointing Feature (SAFETY NET)

#### How It Works
Gemini CLI has automatic checkpointing enabled:
```json
{
  "checkpointing": {
    "enabled": true
  }
}
```

When you approve a tool that modifies files, Gemini automatically:
1. **Creates a Git Snapshot**: Commits to shadow repo at `~/.gemini/history/<project_hash>`
2. **Saves Conversation**: Entire chat history preserved
3. **Stores Tool Call**: The exact operation being performed

#### Restore if Needed
```bash
/restore  # Shows available checkpoints and allows rollback
```

**All checkpoint data stored locally** in:
- Shadow Git repo: `~/.gemini/history/<project_hash>`
- Conversation history: `~/.gemini/tmp/<project_hash>/checkpoints`

### Setup Instructions

#### Terminal 1 Setup (2.5 Pro - FREE)
```bash
# API keys are commented out in ~/.bashrc
gemini
# Choose option 1: Login with Google
# Get 2.5 Pro FREE (1000 requests/day on personal accounts)
```

#### Terminal 2 Setup (2.0 Flash Exp - FREE)
```bash
# Source the setup script for this terminal only
source /home/gotime2022/bin/gemini-setup-experimental.sh
# Run the experimental model
gemini -m gemini-2.0-flash-exp
```

### Model Comparison & Strategy

| Model | Auth | Cost | Requests | Context | Best For |
|-------|------|------|----------|---------|----------|
| **2.5 Pro** | OAuth | FREE | 1000/day | 1M tokens | Complex analysis |
| **2.0 Flash Exp** | API | FREE | Unlimited* | 1M tokens | Rapid tasks |

*While experimental

### Permission Settings - AUTONOMOUS OPERATION

#### ✅ ALLOWED WITHOUT APPROVAL (Autonomous)
- **Reading files**: Analyze entire codebases and documentation
- **Editing files**: Modify and improve existing code
- **Creating files**: Generate new documentation, tests, code
- **Running analysis**: Performance profiling, code analysis
- **Research tasks**: API research, best practices lookup
- **Documentation**: Generate and update all documentation
- **Code review**: Analyze and suggest improvements
- **Pattern detection**: Find issues across repositories
- **Bulk processing**: Handle multiple files simultaneously

#### 🛑 REQUIRES APPROVAL (Ask First)
- **Deleting files**: Any file removal needs confirmation
- **Overwriting files**: Complete replacements need approval
- **Large refactors**: Major structural changes across many files
- **API changes**: Breaking interface modifications
- **Security files**: Modifying auth or security configs
- **Production configs**: Changing production settings
- **External API calls**: Making requests to external services

#### Operating Principle
**"Analyze everything, modify carefully"** - Use full 2M context window for analysis, but ask before major structural changes.

### Core Responsibilities
- **Primary**: Large-scale codebase analysis (2M token context window)
- **Secondary**: Integration testing between frontend and backend
- **Tertiary**: Bulk documentation processing and generation
- Research and analysis for best practices and integrations
- Code review across multiple files simultaneously
- Cross-browser testing and validation
- Pattern detection across entire repositories

## 🚀 Ops CLI Automation Integration

### For @gemini: Research & Large-Scale Analysis Support

As @gemini, your role focuses on research, documentation, and large-scale analysis. The `ops` CLI automation system enhances your contributions to the development workflow:

#### Before Starting Analysis Tasks
```bash
./scripts/ops status           # Understand current project state and deployment targets
./scripts/ops qa --all         # Check both frontend and backend quality
./scripts/ops qa --backend     # Backend-specific analysis
./scripts/ops qa --frontend    # Frontend-specific analysis
```

#### Quality Assurance Integration
```bash
# After documentation/research work:
./scripts/ops qa --all         # Ensure your docs follow project standards

# For integration testing:
./scripts/ops qa --backend     # Test backend integration points
./scripts/ops qa --frontend    # Test frontend integration points

# For environment-related research:
./scripts/ops env doctor       # Check WSL/Windows setup issues to document
```

#### Research and Documentation Workflow

**Project State Analysis:**
- Run `./scripts/ops status` to understand project version and targets
- Check `.automation/config.yml` for tech stack and configuration
- Use `./scripts/ops qa` output to identify areas needing improvement

**Documentation Tasks:**
- Always test ops CLI commands before documenting them
- Include troubleshooting using `ops env doctor` in your guides
- Document version management using `ops release` commands
- Reference automation configuration in technical specifications

**Large-Scale Codebase Analysis:**
- Use `./scripts/ops qa` to understand current quality metrics
- Check build status with `./scripts/ops build --target /tmp/test`
- Analyze deployment readiness with `./scripts/ops verify-prod`

#### Solo Developer Coordination

**Supporting @claude (Technical Leader):**
- Include ops CLI integration in architectural documentation
- Research and document best practices for ops CLI usage
- Analyze project patterns and suggest ops CLI improvements

**Supporting @copilot and @qwen:**
- Document ops CLI workflows in user guides
- Create troubleshooting documentation using `ops env doctor`
- Research and document platform-specific usage patterns

#### Environment and Platform Research

**WSL/Windows Documentation:**
- Use `./scripts/ops env doctor` to identify common issues
- Document platform-specific automation setup
- Research cross-platform ops CLI compatibility

**Build and Deployment Analysis:**
- Analyze `.automation/config.yml` patterns across projects
- Document best practices for different tech stacks
- Research automation integration with CI/CD systems

This integration ensures your research and analysis work directly supports the automation strategy and helps other agents use the ops CLI effectively.

### Strategic Usage - Maximize Both Models

#### Use Gemini 2.0 Flash Experimental For:
- **Rapid iterations** - Faster response times
- **Bulk processing** - No daily limits while free
- **Quick questions** - Instant responses
- **Code generation** - Fast prototyping
- **Testing ideas** - Experiment freely

#### Use Gemini 2.5 Pro For:
- **Complex analysis** - When Flash Exp struggles
- **Advanced reasoning** - Sophisticated logic
- **Quality checks** - Verify Flash Exp outputs
- **Critical decisions** - When accuracy matters
- **Architecture review** - Full context analysis

### Current Project Context
- **Framework**: Solo Developer Framework Template
- **Tech Stack**: Node.js, TypeScript, React, Next.js, Docker, GitHub Actions
- **Coordination**: @Symbol task assignment system
- **MCP Servers**: Local filesystem, brave-search, memory

### @Symbol Task Assignment Protocol

#### Check Current Assignments
Look for tasks assigned to @gemini:
```bash
# Check current assignments
grep "@gemini" specs/*/tasks.md

# Check incomplete tasks
grep -B1 -A1 "\[ \] .*@gemini" specs/*/tasks.md

# Find analysis and documentation tasks
grep -i "research\|document\|analyze\|analysis" specs/*/tasks.md | grep "@gemini"
```

#### Task Format Recognition
```markdown
- [ ] T020 @gemini Research caching strategies for API optimization
- [ ] T035 @gemini Document new API endpoints with examples
- [ ] T040 @gemini Analyze performance bottlenecks across codebase
- [x] T045 @gemini Performance analysis report complete ✅
```

#### Task Completion Protocol
1. **Complete analysis/documentation** using appropriate model
2. **Verify accuracy** and completeness
3. **Mark task complete** with `[x]` and add ✅
4. **Reference task numbers** in commit messages
5. **Hand off results** to implementation agents

### Implementation Workflow

#### 1. Research Tasks
- Use both models in parallel for comprehensive analysis
- Flash Exp for quick exploration, 2.5 Pro for deep analysis
- Cross-reference multiple sources for accuracy
- Consider performance and security implications

#### 2. Documentation Tasks
- Flash Exp for initial drafts (fast generation)
- 2.5 Pro for review and refinement
- Include code examples and diagrams
- Reference task numbers from specs/*/tasks.md

#### 3. Code Analysis
- Leverage 2M token context for whole-codebase analysis
- Pattern detection across multiple files
- Security vulnerability scanning
- Performance optimization opportunities

### Configuration Details

#### File Locations
- **Setup Script**: `/home/gotime2022/bin/gemini-setup-experimental.sh`
- **Bashrc**: `~/.bashrc` (lines 192-193 commented out for OAuth)
- **API Key**: Set via setup script (Terminal 2 only)

#### Common Workflows

##### Parallel Processing
```bash
# Terminal 1: Complex analysis with 2.5 Pro
gemini -p "Analyze the architecture and suggest improvements"

# Terminal 2: Quick implementation with Flash Exp
gemini -m gemini-2.0-flash-exp -p "Generate the code for this feature"
```

##### Sequential Enhancement
1. Start with Flash Exp for rapid prototype
2. Refine with 2.5 Pro for quality
3. Submit to Claude for integration

### Commit Requirements

**EVERY commit must follow this format:**
```bash
git commit -m "[WORKING] docs: Add API documentation with examples

Generated comprehensive API docs with request/response examples
and error handling patterns.

Related to #123

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
Co-Authored-By: @qwen <noreply@anthropic.com>
Co-Authored-By: @gemini <noreply@anthropic.com>  
Co-Authored-By: @codex <noreply@anthropic.com>
Co-Authored-By: @copilot <noreply@anthropic.com>"
```

### Cost Reality Check

If you were paying:
- **Gemini 2.5 Pro**: $1.25/M input + $10/M output = EXPENSIVE!
- **Gemini 2.0 Flash**: $0.10/M input + $0.40/M output = Still adds up
- **Current cost**: $0.00 - BOTH ARE FREE!

**USE THEM TO THE MAX WHILE THEY'RE FREE!**

### Solo Developer Coordination

#### When to Use Gemini vs Others
- **Use @gemini For**:
  - Analyzing entire repositories at once (2M context)
  - Processing large documentation sets
  - Bulk code review across multiple files
  - Finding patterns across codebases
  - Generating comprehensive documentation
  - Research tasks requiring large context
  
- **Hand Off To @claude For**:
  - Architecture decisions after analysis
  - Complex implementation after research
  - Security reviews after documentation
  - Integration work after analysis

- **Hand Off To @qwen For**:
  - Performance optimization after analysis
  - Algorithm improvements after research
  - Database optimization after performance analysis

- **Hand Off To @codex For**:
  - Frontend documentation after backend analysis
  - UI component documentation after system analysis

- **Hand Off To @copilot For**:
  - Simple implementation after providing patterns
  - Boilerplate generation after establishing templates

#### Typical Handoff Pattern
```markdown
### Analysis Phase (@gemini's domain)
- [ ] T010 @gemini Analyze current authentication system
- [ ] T011 @gemini Research OAuth 2.0 best practices
- [ ] T012 @gemini Document security requirements

### Implementation Phase (hand off to specialists)
- [ ] T020 @claude Implement new auth system (depends on T010-T012)
- [ ] T021 @codex Create auth UI components (depends on T020)
- [ ] T022 @qwen Optimize auth performance (depends on T021)
```

### Documentation Standards
- All docs in Markdown format
- Code blocks with language highlighting
- API docs include request/response examples
- Setup guides include troubleshooting sections
- Always include "Last Updated" dates
- Reference task numbers (T001, T002, etc.)

### Known Issues & Workarounds

#### Error Messages
Those `[ERROR] [ImportProcessor]` messages are harmless - just Gemini looking for optional config files. The CLI works perfectly despite them.

#### Tool Execution Problem
**Issue**: Gemini sometimes displays tool calls without executing them
**Workaround**: 
1. Always verify file was actually written
2. If file is empty, manually copy content from output
3. Consider using Claude for critical file operations

### Best Practices
- Use both models strategically based on task complexity
- Leverage 2M context for bulk analysis tasks
- Save 2.5 Pro requests for complex reasoning (1000/day limit)
- Use Flash Exp for everything else (unlimited while free)
- Coordinate with Claude for implementation after analysis

### When Free Period Ends
Eventually these models won't be free:
1. **Gemini 1.5 Flash**: ~$0.075/M tokens (cheapest stable)
2. **Gemini 1.5 Flash-8b**: ~$0.037/M tokens (even cheaper)
3. **API keys**: Get your own from https://aistudio.google.com/apikey

But for now - **USE BOTH FREE MODELS TO THE MAXIMUM!**