# Agent Roster & Capabilities

> **Architecture**: 7 specialized agents + GitHub Copilot orchestration = Complete development coverage

## 🤖 Full Agent Specifications

### 1. Frontend Testing Agent
```yaml
name: frontend-tester
category: quality
complexity: moderate
github-integration: ✅
```

**Specialization:** End-to-end UI testing and visual validation

**Triggers:**
- Pull requests with frontend changes (`*.tsx`, `*.jsx`, `*.css`, `*.scss`)
- Issues labeled: `frontend`, `UI`, `needs-testing`
- Visual regression testing requirements
- Accessibility compliance checks

**Tools & MCP Servers:**
- Playwright MCP for browser automation
- BrowserBase for cross-browser testing
- Read, Write, Edit for test files
- TodoWrite for test scenario tracking

**Key Capabilities:**
- E2E user flow testing
- Visual regression detection
- Cross-browser compatibility
- Mobile responsive testing
- Accessibility (WCAG) validation
- Performance metrics (Lighthouse)

**Outputs:**
- Detailed test reports with screenshots
- Video recordings of failures
- Coverage metrics
- PR comments with results

---

### 2. Backend Testing Agent
```yaml
name: backend-tester
category: quality
complexity: moderate-high
github-integration: ✅
```

**Specialization:** API testing, database validation, integration testing

**Triggers:**
- Pull requests with backend changes (`*.py`, `*/api/*`, `*.sql`)
- Database schema modifications
- Issues labeled: `backend`, `API`, `database`
- Microservice changes

**Tools & MCP Servers:**
- Postman MCP for API testing
- Supabase MCP for database operations
- Bash for test execution
- Docker MCP for containerized testing

**Key Capabilities:**
- REST/GraphQL API testing
- Database integrity validation
- Load and stress testing
- Integration testing
- Contract testing
- Mock service generation

**Outputs:**
- API test results with response times
- Database validation reports
- Performance benchmarks
- Test coverage reports

---

### 3. System Architect
```yaml
name: architect
category: design
complexity: high
github-integration: ✅
```

**Specialization:** System design, database architecture, technical planning

**Triggers:**
- Issues labeled: `architecture`, `design`, `RFC`
- New feature requests requiring design
- Database schema planning
- Major refactoring proposals

**Tools & MCP Servers:**
- Figma MCP for design diagrams
- Notion MCP for documentation
- All file operations
- Database design tools

**Key Capabilities:**
- Database schema design
- API contract definition
- System architecture diagrams
- Technology selection
- Scalability planning
- Design pattern implementation

**Outputs:**
- Architecture Decision Records (ADRs)
- Database ERD diagrams
- API specifications (OpenAPI)
- System design documents
- Technology evaluation matrix

---

### 4. Security Agent
```yaml
name: security
category: protection
complexity: high
github-integration: ✅
```

**Specialization:** Security auditing, vulnerability detection, compliance

**Triggers:**
- Any authentication/authorization changes
- Dependabot security alerts
- Issues labeled: `security`, `vulnerability`
- Secrets or encryption in code
- OWASP compliance checks

**Tools & MCP Servers:**
- GitHub MCP for security scanning
- Code analysis tools
- Grep for pattern detection
- Secret detection tools

**Key Capabilities:**
- Vulnerability scanning (SAST)
- Dependency auditing
- Secret detection
- OWASP compliance checking
- Authentication flow review
- Security header validation

**Outputs:**
- Security audit report
- Vulnerability assessment with CVE scores
- Remediation guidelines
- Compliance checklist
- Auto-created security issues

**Special Powers:**
- Can BLOCK all PRs if critical vulnerability found
- Escalates to human for zero-day vulnerabilities

---

### 5. Code Refactoring Agent
```yaml
name: refactor
category: optimization
complexity: moderate-high
github-integration: ✅
```

**Specialization:** Code optimization, technical debt reduction, modernization

**Triggers:**
- Issues labeled: `tech-debt`, `performance`, `refactor`
- Code complexity threshold exceeded
- Performance bottlenecks identified
- Legacy code modernization

**Tools & MCP Servers:**
- MultiEdit for large-scale changes
- Code analysis tools
- Performance profiling
- AST manipulation

**Key Capabilities:**
- Performance optimization
- Code deduplication
- Design pattern implementation
- Dead code elimination
- Dependency updates
- Code style standardization

**Outputs:**
- Refactored code with metrics
- Performance improvement reports
- Technical debt reduction summary
- Before/after comparisons

---

### 6. Integration Specialist
```yaml
name: integrations
category: connectivity
complexity: moderate-high
github-integration: ✅
```

**Specialization:** Third-party integrations, webhooks, event systems

**Triggers:**
- Issues labeled: `integration`, `webhook`, `external-api`
- Third-party service connections
- Event-driven architecture needs
- Webhook implementations

**Tools & MCP Servers:**
- WebFetch for API testing
- Postman MCP for endpoint validation
- Ngrok MCP for webhook testing
- Event system configuration

**Key Capabilities:**
- OAuth implementation
- Webhook setup and testing
- API client generation
- Event bus configuration
- Rate limiting implementation
- Circuit breaker patterns

**Outputs:**
- Integration documentation
- Webhook test results
- API client libraries
- Event flow diagrams
- Error handling strategies

---

### 7. PR Review Agent
```yaml
name: pr-reviewer
category: quality
complexity: moderate
github-integration: ✅
```

**Specialization:** Automated code review and standards enforcement

**Triggers:**
- ALL pull requests (automatic)
- After any agent completes work
- Manual review requests
- Pre-merge validation

**Tools & MCP Servers:**
- GitHub MCP for PR operations
- Code analysis tools
- Standards checking
- Documentation validation

**Key Capabilities:**
- Code style checking
- Best practices validation
- Security pattern review
- Documentation completeness
- Test coverage analysis
- Breaking change detection

**Outputs:**
- PR review comments
- Approval/change requests
- Code quality metrics
- Suggested improvements
- Standards compliance report

---

## ⚡ GitHub Copilot (Special Case)

```yaml
name: GitHub Copilot
category: simple-automation
complexity: 1-2 ONLY
size: XS-S ONLY
```

**The Rule:** Copilot handles tasks that are **BOTH** simple (1-2) **AND** small (XS-S)

**Examples of What Copilot Handles:**
- Fix typos and formatting
- Add simple comments
- Create basic validation
- Update configuration values
- Add single unit test
- Simple bug fixes

**Examples of What Agents Handle:**
- Any multi-file change
- Complex logic implementation
- Security-sensitive code
- Architecture decisions
- Performance optimization
- Integration with external services

## 🔄 Agent Collaboration Matrix

| Primary Agent | Commonly Works With | For Tasks Like |
|---------------|-------------------|----------------|
| frontend-tester | backend-tester | Full-stack features |
| frontend-tester | architect | Component design |
| backend-tester | security | API security |
| backend-tester | integrations | External services |
| security | ALL agents | Security validation |
| architect | refactor | System improvements |
| integrations | security | OAuth/auth flows |
| pr-reviewer | ALL agents | Final validation |

## 📊 Complexity Assignment Guide

| Complexity | Size | Examples | Who Handles |
|------------|------|----------|-------------|
| 1 | XS | Fix typo, add comment | Copilot |
| 2 | S | Simple validation | Copilot |
| 2 | M | Add form validation | Agent |
| 3 | M | Create API endpoint | Agent |
| 4 | L | Implement auth system | Multiple Agents |
| 5 | XL | Redesign architecture | All Agents + Human |

## 🚨 Agent Escalation Paths

```yaml
Level 1: Single Agent
  → Can handle independently
  
Level 2: Multi-Agent
  → Coordinates with other agents
  → Example: frontend + backend for full feature
  
Level 3: Security Block
  → Security agent finds critical issue
  → All work stops
  → Human intervention required
  
Level 4: Human Required
  → Major architecture changes
  → Production security incidents
  → Customer-facing critical paths
```

## 🎯 Quick Agent Selection

```bash
# The system automatically selects based on:
1. Issue labels
2. File changes in PR
3. Keywords in description
4. Complexity/Size matrix

# Manual override:
- Set agent in issue template
- Use 'assigned_agent' field
- Command: /assign-agent <name>
```