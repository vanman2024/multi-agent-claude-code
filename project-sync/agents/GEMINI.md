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

### Core Responsibilities
- **Primary**: Large-scale codebase analysis (2M token context window)
- **Secondary**: Bulk documentation processing and generation
- Research and analysis for best practices and integrations
- Code review across multiple files simultaneously
- Pattern detection across entire repositories

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
- **Framework**: Multi-Agent Development Framework Template
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

### Cost Reality Check

If you were paying:
- **Gemini 2.5 Pro**: $1.25/M input + $10/M output = EXPENSIVE!
- **Gemini 2.0 Flash**: $0.10/M input + $0.40/M output = Still adds up
- **Current cost**: $0.00 - BOTH ARE FREE!

**USE THEM TO THE MAX WHILE THEY'RE FREE!**

### Multi-Agent Coordination

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