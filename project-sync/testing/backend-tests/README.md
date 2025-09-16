# Generic Backend Testing Framework

## Overview
Clean testing framework for backend APIs, CLI tools, and MCP servers.
This is a TEMPLATE - replace placeholders with your actual code when building projects.

## Structure

```
backend-tests/
├── unit/           # Test individual functions
├── integration/    # Test components working together  
├── contract/       # Test API contracts and schemas
├── e2e/           # Test complete workflows
├── performance/   # Test speed and resource usage
├── cli/           # Test CLI commands and output
├── mcp/           # Test MCP server implementations
└── live/          # Test against real external services
```

## Key Principles

1. **No Dependencies on src/**
   - All tests use mocks/placeholders until actual code exists
   - Comments show where real imports will go

2. **Contract Testing**
   - When src/ exists, contracts inherit from implementations
   - Ensures external interfaces remain stable

3. **Environment Gating**
   - Expensive tests marked with pytest markers
   - Skip tests without proper environment variables

## Running Tests

```bash
# All tests
pytest

# Specific category
pytest unit/
pytest integration/

# By markers
pytest -m "not slow"
pytest -m "not live"
pytest -m "mcp"

# With coverage
pytest --cov=src --cov-report=term-missing
```

## When You Add Real Code

1. Replace mock imports with actual imports from src/
2. Replace placeholder assertions with real tests
3. Keep the same test structure and patterns