# Multi-Agent Coordination System v2.0

## 🎯 CURRENT SYSTEM: @Symbol Coordination (Game-Changer!)

Revolutionary Discovery: The @symbol agent coordination system has proven to be incredibly effective and scalable. This simple markdown-based approach outperforms complex orchestration systems.

## Core Innovation: @Symbol Task Assignment

### How It Works

In tasks.md - Simple, clear, effective:
```markdown
- [ ] T029 @copilot Configuration management commands
- [x] T031 @claude FastAPI callback server ✅ 
- [ ] T035 @codex Unit tests for data model validation
- [ ] T037 @gemini Performance tests for bulk operations
- [ ] T040 @qwen Optimize search performance algorithms
```

### Why This is Revolutionary

1. **Universal Pattern**: Uses familiar @mention syntax from GitHub/social media
2. **Zero Infrastructure**: Just markdown files - works anywhere
3. **Self-Documenting**: The system explains itself
4. **Tool Agnostic**: Works with any agent or human
5. **Instantly Scalable**: Add new agents by just using @newagent

## 🤖 Current Agent Ecosystem

### 🏗️ CTO-Level Review & Architecture
**@claude (Claude Code - Strategic Reviewer)**
- **NEW ROLE**: CTO-level engineering reviewer & strategic guide
- **Primary Functions**:
  - Review & validate work from other agents
  - Make architecture decisions
  - Resolve complex integration issues
  - Ensure code quality and consistency
  - Strategic technical direction
- **Subagents Available When Needed**: 
  - general-purpose, code-refactorer, pr-reviewer
  - backend-tester, integration-architect, system-architect
  - security-auth-compliance, frontend-playwright-tester
- **Used For**: Critical decisions, complex problems, quality gates
- **Cost**: Via subscription (use strategically)

### ⚡ Bulk & Fast Implementation
**@copilot (GitHub Copilot with Grok Model)**
- **Role**: Simple, fast bulk implementation
- **Model**: Powered by Grok AI
- **Speed**: VERY FAST (Grok-powered)
- **Best For**: 
  - Bulk code generation
  - Simple tasks (Complexity ≤2, Size XS/S)
  - Repetitive implementations
  - Rapid prototyping
  - Bulk file generation
- **Cost**: FREE with GitHub Pro

### 🎨 Frontend Development
**@codex (OpenAI Codex)**
- **Role**: FRONTEND ONLY
- **Focus**: 
  - React components
  - UI/UX implementation
  - Frontend state management
  - CSS/Tailwind styling
  - Frontend testing
- **Best For**: All frontend development tasks
- **Cost**: Via API

### 🔍 Analysis & Documentation
**@gemini (Google Gemini - Dual Models)**
- **2.5 Pro (OAuth)**: 1000 req/day FREE on personal
  - Complex analysis, advanced reasoning
- **2.0 Flash Exp (API)**: ~1000+ req/day FREE experimental
  - Fast bulk processing, rapid documentation
  - May have separate quota from 2.5 Pro
- **Combined Capacity**: ~2000+ requests/day between both models
- **Best For**: 
  - Large codebase analysis (2M context)
  - Documentation generation
  - Research tasks

### ⚡ Performance Optimization & Daily Coding
**@qwen (Qwen CLI)**
- **Role**: Performance specialist & everyday development
- **Capacity**: 2000 req/day FREE (OAuth)
- **Best For**:
  - Algorithm optimization
  - Database performance
  - Memory optimization
  - Query optimization
  - Daily coding tasks
- **Cost**: FREE (via OAuth login)

### Agent Context Files (Living Documentation)

Each agent has their own "job description" that stays current:

- **agents/CLAUDE.md** - @claude instructions and current assignments
- **agents/COPILOT_SUMMARY.md** - @copilot specific guidance and priorities
- **agents/GEMINI.md** - @gemini responsibilities and workflow
- **agents/QWEN.md** - @qwen optimization tasks and patterns
- **.github/copilot-instructions.md** - GitHub Copilot integration

## 🔄 Agent Coordination Workflow

### 1. Task Assignment Protocol

**Create Tasks with @Symbol Assignment:**
```markdown
## In specs/001-feature/tasks.md:

### Backend Tasks
- [ ] T010 @claude Design database schema architecture
- [ ] T011 @copilot Implement user authentication endpoints
- [ ] T012 @codex Create unit tests for auth module

### Performance Tasks  
- [ ] T020 @qwen Optimize database query performance
- [ ] T022 @gemini Research and document performance improvements

### Integration Tasks
- [ ] T030 @claude Coordinate API integration testing
- [ ] T031 @copilot Implement error handling patterns
```

### 2. Agent Task Execution

**Check Current Assignments:**
```bash
# Check what @qwen is working on
grep "@qwen" specs/*/tasks.md

# Check all incomplete tasks for an agent  
grep -B1 -A1 "\[ \] .*@claude" specs/*/tasks.md
```

**Complete Tasks:**
1. Receive assignment via @symbol
2. Execute task according to agent specialization
3. Mark complete: Change `[ ]` to `[x]` 
4. Add completion notes if needed

**Example Completion:**
```markdown
- [x] T020 @qwen Optimize database query performance ✅
  - Reduced query time from 2.3s to 0.4s
  - Implemented connection pooling
  - Added query result caching
```

### 3. Inter-Agent Handoffs

```markdown
- [x] T025 @claude Database schema design complete ✅
- [ ] T026 @copilot Implement schema in FastAPI models (depends on T025)
- [ ] T027 @qwen Optimize schema queries after implementation (depends on T026)
```

## 🎯 Agent Specializations & Task Assignment

### Task Assignment Strategy

| Task Type | Primary Agent | Notes |
|-----------|--------------|-------|
| **Frontend Development** | @codex | Owns ALL frontend work |
| **Simple Backend** | @copilot (Grok) | Fast implementation for Complexity ≤2, Size XS/S |
| **Complex Backend** | @claude | Architecture, integration, multi-file |
| **Performance** | @qwen | Optimization specialist |
| **Documentation** | @gemini | Bulk docs, analysis |
| **Security** | @claude/security | Security subagent |
| **Testing** | @claude/testers for E2E, @codex for frontend |
| **Bulk Generation** | @copilot (Grok) | Fastest for repetitive tasks |

### @claude (Architecture & Integration - 40-55% of work)
**Best For:**
- Multi-file refactoring & complex integration
- System architecture decisions
- Complex debugging across components
- Security implementation & reviews
- DevOps & infrastructure

**Subagent Specializations:**
- `@claude/general-purpose` - Research, multi-step tasks
- `@claude/code-refactorer` - Large-scale refactoring
- `@claude/pr-reviewer` - Code review & standards
- `@claude/backend-tester` - API testing
- `@claude/integration-architect` - Multi-service integration
- `@claude/system-architect` - Database & API design
- `@claude/security-auth-compliance` - Authentication & security
- `@claude/frontend-playwright-tester` - E2E UI testing

### @copilot (Fast Bulk Implementation - Grok-powered)  
**Best For:**
- Simple tasks ONLY (Complexity ≤2, Size XS/S)
- Bulk code generation
- Repetitive implementations
- Rapid prototyping
- Following established patterns

**Key Features:**
- Powered by Grok AI for speed
- FREE with GitHub Pro
- Auto-assigns via GitHub integration
- Fastest agent for simple bulk work

### @codex (FRONTEND ONLY Specialist)
**Best For:**
- React components & hooks
- UI/UX implementation
- CSS/Tailwind styling
- Frontend state management (Redux, Zustand, Context)
- Frontend testing (Jest, RTL)
- Accessibility (ARIA, WCAG)

**NEVER Use For:**
- Backend development (use @claude)
- API design (use @claude)
- Database work (use @claude)
- Performance optimization (use @qwen)

### @gemini (Analysis & Documentation - Dual Free Models)
**Best For:**
- Large codebase analysis (2M token context!)
- Bulk documentation generation
- Research & technical analysis
- Pattern finding across files

**Dual Model Strategy:**
- **Gemini 2.5 Pro (OAuth)**: 1000 req/day FREE on personal accounts
  - Complex analysis, advanced reasoning
  - Use in Terminal 1 with OAuth login
- **Gemini 2.0 Flash Exp (API)**: Unlimited FREE while experimental
  - Fast bulk processing, rapid documentation
  - Use in Terminal 2 with API key setup

**Setup for Dual Terminal Usage:**
```bash
# Terminal 1: OAuth for 2.5 Pro (default)
gemini -p "Complex analysis task"

# Terminal 2: API key for 2.0 Flash Exp
source ~/bin/gemini-setup-experimental.sh
gemini -m gemini-2.0-flash-exp -p "Bulk documentation task"
```

### @qwen (Performance Optimization - FREE via Ollama)
**Best For:**
- Algorithm optimization
- Database performance tuning
- Memory & CPU optimization
- Query optimization
- Code efficiency improvements

**Setup & Usage:**
```bash
# Install via Ollama
ollama pull qwen2.5:7b

# Use for optimization
ollama run qwen2.5:7b "optimize this function: $(cat slow_function.js)"
```

**Key Features:**
- Runs locally - no API costs
- Fast performance analysis
- Specialized in optimization
- Always provides before/after metrics

## 🔄 Workflow Patterns (With Claude as CTO Reviewer)

### Pattern 1: Feature Development
```
1. @gemini - Research requirements and constraints
2. @qwen - Implement backend logic
3. @copilot (Grok) - Bulk generation of boilerplate
4. @codex - Frontend components
5. @qwen - Performance optimization
6. @claude - REVIEW: Architecture & integration validation
7. @gemini - Documentation
```

### Pattern 2: Performance Fix
```
1. @gemini - Analyze bottlenecks
2. @qwen - Optimize algorithms
3. @qwen - Implement improvements
4. @claude - REVIEW: Validate changes don't break architecture
5. @gemini - Document improvements
```

### Pattern 3: Frontend Feature
```
1. @codex - Component development
2. @codex - State management
3. @codex - Styling
4. @codex - Frontend tests
5. @claude - REVIEW: Integration with backend
6. @gemini - User documentation
```

### Pattern 4: Bulk Refactoring
```
1. @gemini - Analyze current code structure
2. @qwen - Plan refactoring approach
3. @copilot (Grok) - Bulk changes
4. @qwen - Performance check
5. @claude - REVIEW: Ensure architectural integrity
```

## 💰 Daily Capacity & Claude as CTO Reviewer

### Total FREE Daily Capacity
- **Qwen**: 2000 requests/day (OAuth)
- **Gemini 2.5 Pro**: 1000 requests/day (OAuth)
- **Gemini 2.0 Flash Exp**: ~1000+ requests/day (API)
- **Copilot**: Unlimited with GitHub Pro
- **TOTAL**: 4000+ FREE requests daily

### New Workflow: Claude as CTO-Level Reviewer
```
1. Other agents do the implementation work
2. @claude reviews critical pieces
3. @claude makes architecture decisions
4. @claude resolves integration issues
5. @claude ensures quality standards
```

### When to Engage @claude
- Architecture decisions needed
- Complex integration problems
- Security review required
- Quality gate before deployment
- Strategic technical decisions
- Reviewing work from multiple agents
- Resolving conflicts between agent outputs

## Cost Optimization Strategy

### FREE Tier Maximization
1. **Qwen**: 2000 req/day FREE (OAuth)
2. **Gemini 2.5 Pro**: 1000 req/day FREE (OAuth)
3. **Gemini 2.0 Flash Exp**: ~1000+ req/day FREE (API)
4. **Copilot**: FREE with GitHub Pro

### When to Use Paid Agents
- **Claude**: Complex architecture, critical reviews only
- **Codex**: All frontend work (specialized expertise)

### Speed vs Quality Trade-offs
**Need it FAST:**
1. @copilot (Grok) - Fastest bulk generation
2. @qwen - Fast optimization
3. @gemini/flash-exp - Fast analysis

**Need it RIGHT:**
1. @claude - Most accurate, thorough reviews
2. @gemini/2.5-pro - Complex reasoning
3. @codex - Frontend expertise

## 📋 Task Management Patterns

### Priority Task Assignment
```markdown
### HIGH PRIORITY 🔥
- [ ] T001 @claude Fix production authentication bug (URGENT)
- [ ] T002 @copilot Implement hotfix deployment

### NORMAL PRIORITY
- [ ] T010 @qwen Optimize search performance
- [ ] T012 @gemini Document new API endpoints

### LOW PRIORITY  
- [ ] T020 @codex Add comprehensive test coverage
- [ ] T021 @gemini Research alternative database solutions
```

### Dependency Management
```markdown
### Database Tasks (Sequential)
- [x] T100 @claude Design schema ✅
- [ ] T101 @copilot Implement models (depends on T100)
- [ ] T102 @codex Create model tests (depends on T101)  
- [ ] T103 @qwen Optimize queries (depends on T101)

### Parallel Tasks (Independent)
- [ ] T200 @gemini Research caching strategies
- [ ] T202 @codex Implement logging framework
```

### Agent Workload Balancing
```markdown
### Current Sprint Assignments

**@claude (3 tasks)**
- [ ] T001 Architecture review
- [ ] T015 Integration testing
- [ ] T030 Deployment coordination

**@copilot (5 tasks)**  
- [ ] T002 User endpoint implementation
- [ ] T003 Auth middleware
- [ ] T004 Validation logic
- [ ] T005 Error handling
- [ ] T006 Response formatting

**@qwen (2 tasks)**
- [ ] T020 Query optimization
- [ ] T025 Performance analysis

- [ ] T040 Code refactoring
- [ ] T045 Architecture cleanup
```

## 🚀 Setup & Configuration

### Environment Setup

```bash
# Install AI CLIs
pip install openai-cli anthropic-cli
npm install -g @google/gemini-cli

# Configure API keys in ~/.bashrc
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="AIzaSyC4mL5xX7DjXVCTDM84SL2DhfU5__JnKTU"
export GEMINI_API_KEY="AIzaSyC4mL5xX7DjXVCTDM84SL2DhfU5__JnKTU"

# Gemini cost management (force cheapest model)
alias gemini="/home/gotime2022/bin/gemini-cheap"
```

### Agent Directory Structure
```
agents/
├── README.md                    # Agent overview and workflow
├── CLAUDE.md                   # @claude context and assignments  
├── COPILOT_SUMMARY.md          # @copilot guidance and priorities
├── GEMINI.md                   # @gemini research tasks
├── QWEN.md                     # @qwen optimization assignments
└── sync-project-template.sh     # Complete project sync script
```

### Task File Templates

**specs/001-feature/tasks.md:**
```markdown
# Feature Implementation Tasks

## Architecture & Planning
- [ ] T001 @claude Review requirements and design architecture
- [ ] T002 @gemini Research technology alternatives

## Implementation  
- [ ] T010 @copilot Implement core functionality
- [ ] T011 @codex Create comprehensive test suite
- [ ] T012 @copilot Add error handling and validation

## Optimization
- [ ] T020 @qwen Performance testing and optimization

## Documentation
- [ ] T030 @gemini Document API endpoints
- [ ] T031 @claude Create deployment guide
```

## 📊 Success Metrics

### System Performance
- **85% Task Completion Rate** - Agents successfully complete assigned tasks
- **Zero Coordination Conflicts** - Clear separation prevents overlap
- **Optimal Agent Utilization** - Each agent works within their specialization
- **Cost Efficiency** - Maximum use of free tiers before paid services

### Per Agent Metrics
- **@claude**: Architecture quality, integration success (40-55% of work)
- **@copilot (Grok)**: Task completion speed, bulk efficiency
- **@codex**: Frontend quality, UI/UX excellence (100% frontend ownership)
- **@gemini**: Documentation completeness, analysis depth (dual model usage)
- **@qwen**: Performance improvements, optimization metrics (always free)

### Coordination Efficiency
- No frontend work assigned to non-@codex agents
- Simple tasks (≤2 complexity) routed to @copilot
- Complex tasks automatically escalated to @claude
- Performance work exclusively handled by @qwen

## 🔧 Advanced Patterns

### Automated Task Creation
```bash
# Generate tasks from specs automatically
claude generate-tasks --spec="specs/001-feature/spec.md" --output="specs/001-feature/tasks.md"
```

### Agent Status Monitoring  
```bash
# Check agent workloads
./scripts/agent-status.sh

# Output:
# @claude: 3 active tasks, 1 blocked
# @copilot: 5 active tasks  
# @qwen: 2 active tasks
# @gemini: 2 active tasks
```

### Parallel Execution

**Can Run Simultaneously:**
- @gemini Terminal 1 (OAuth for 2.5 Pro)
- @gemini Terminal 2 (API for 2.0 Flash Exp)
- @qwen (local Ollama)
- @copilot (GitHub interface)
- @codex (separate frontend work)
- @claude (main terminal)

**Example Parallel Workflow:**
```bash
# Terminal 1: Gemini 2.5 Pro analysis
gemini -p "Analyze architecture patterns"

# Terminal 2: Gemini Flash Exp docs
source ~/bin/gemini-setup-experimental.sh
gemini -m gemini-2.0-flash-exp -p "Generate bulk documentation"

# Terminal 3: Qwen optimization
ollama run qwen2.5:7b "Optimize database queries"

# Terminal 4: Claude architecture
claude /work #123

# GitHub: Copilot working on simple tasks
# VS Code: Codex building frontend components
```

## 🎯 Key Insights

> **"Simple, universal patterns often outperform complex, custom solutions."**

The @symbol coordination system succeeds because:

1. **Cognitive Familiarity** - Everyone knows @mentions
2. **No Learning Curve** - Instant adoption by any team member
3. **Tool Independence** - Works with any AI agent or human
4. **Self-Organizing** - Teams naturally optimize their usage
5. **Failure Resistant** - No complex infrastructure to break

## 📚 Integration with Development Workflow

### With Spec-Kit
```bash
# After /specify
@gemini research technical constraints for: $(cat specs/001/spec.md)

# After /plan  
@claude validate architecture in: $(cat specs/001/plan.md)

# After /tasks
@copilot implement task T001 from: $(cat specs/001/tasks.md)
```

### With GitHub Issues
```markdown
## GitHub Issue #123
- [x] T001 @claude Investigate root cause ✅
- [ ] T002 @copilot Implement fix
- [ ] T003 @codex Add regression tests
- [ ] T004 @qwen Optimize performance impact
```

### With CI/CD
```yaml
# .github/workflows/ai-coordination.yml
- name: Check Agent Assignments
  run: |
    grep -r "@" specs/*/tasks.md | grep "\[ \]" > pending-tasks.txt
    if [ -s pending-tasks.txt ]; then
      echo "Pending AI agent tasks found"
      cat pending-tasks.txt
    fi
```

This coordination system transforms how teams work with AI agents, creating a seamless blend of human planning and AI execution that scales naturally with project complexity.