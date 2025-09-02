# Local Testing vs GitHub Actions Workflow

## Problem Statement

There has been confusion between local testing and GitHub Actions testing. Developers need to run the same tests locally that will run in CI/CD to reduce feedback loops and catch issues early.

## The Solution: Aligned Testing Workflow

### New Local Pre-Commit Script

We now have a local testing script that **mirrors exactly** what GitHub Actions will run:

```bash
./scripts/testing/local-pre-commit.sh
```

This script runs the same checks as the GitHub Actions CI/CD pipeline:

1. **Code Quality Check** - Linting, type checking, formatting
2. **Unit Tests** - All test suites including framework-specific tests  
3. **Integration Tests** - End-to-end testing scenarios
4. **Security Scanning** - Dependency vulnerabilities and common security issues
5. **Build Test** - Verify project builds successfully
6. **Git Status Check** - Verify branch and commit status

## Developer Workflow

### Before Creating/Updating a PR

1. **Make your changes** 
2. **Run local pre-commit testing**:
   ```bash
   ./scripts/testing/local-pre-commit.sh
   ```
3. **Address any failures** - Fix issues found by local testing
4. **Review warnings** - Consider addressing non-critical warnings
5. **Commit and push** your changes
6. **Create/update PR** - The local testing checkbox will be part of the PR template

### What the Local Script Checks

The local script runs **exactly the same checks** as GitHub Actions:

#### For JavaScript/TypeScript Projects:
- **Linting**: `npm run lint`
- **Type Checking**: `npm run typecheck` or `npx tsc --noEmit`
- **Unit Tests**: `npm test` with coverage
- **Build**: `npm run build`
- **Security**: `npm audit --audit-level=high`

#### For Python Projects:
- **Linting**: `flake8`
- **Type Checking**: `mypy`
- **Unit Tests**: `pytest --cov`
- **Security**: `safety check`

#### For This Project (Mixed Scripting):
- **Shell Linting**: `shellcheck` on all `.sh` files
- **Framework Tests**: Existing hook and agent tests
- **Security Patterns**: Check for common security issues
- **Git Status**: Verify branch and uncommitted changes

### Interpreting Results

#### ✅ Success (Exit Code 0)
```
🎉 All critical stages passed! Ready to create/update PR.

Next steps:
1. Review any warnings above
2. Commit your changes: git add . && git commit -m 'Your message'  
3. Push your changes: git push
4. Create or update your pull request
```

#### ❌ Failure (Exit Code 1)  
```
❌ Some critical stages failed. Fix issues before creating PR.

Common fixes:
- Run linter and fix issues: npm run lint -- --fix
- Fix type errors: npm run typecheck
- Fix failing tests: npm test
- Check build issues: npm run build
```

#### ⚠️ Warnings
Non-critical issues that you should consider addressing but won't block the PR.

## Benefits

### 1. **Reduced Feedback Loop**
- Catch issues **before** pushing to GitHub
- No waiting for CI/CD to fail and then fixing

### 2. **Consistency**  
- Local testing **exactly matches** GitHub Actions
- No surprises when CI/CD runs

### 3. **Faster Development**
- Fix issues immediately while context is fresh
- Avoid multiple commit/push cycles to fix CI failures

### 4. **Quality Gates**
- Enforced local testing via PR checklist
- Same standards for all contributors

## PR Requirements

The updated pull request template now requires:

- [ ] **Local Pre-Commit Testing**
  - [ ] Ran `./scripts/testing/local-pre-commit.sh` successfully
  - [ ] All critical stages passed (0 failed stages)  
  - [ ] Addressed any critical warnings found
  - [ ] Local testing matches GitHub Actions pipeline

## Integration with Existing Tools

### Framework-Specific Testing
The local pre-commit script includes existing framework tests:
- **Hooks testing**: `.claude/hooks` functionality
- **Agent coordination**: Multi-agent behavior 
- **Slash commands**: Command parsing and execution

### GitHub Actions
The script mirrors the exact same pipeline stages:
- **quality-check** job → Code Quality Check stage
- **unit-tests** job → Unit Tests stage  
- **integration-tests** job → Integration Tests stage
- **security-scan** job → Security Scanning stage
- **build** job → Build Test stage

### Git Hooks (Future Enhancement)
Could integrate with git pre-commit hooks:
```bash
# Optional: Set up git pre-commit hook
cp scripts/testing/local-pre-commit.sh .git/hooks/pre-commit
```

## Troubleshooting

### "shellcheck not found"
```bash
# Install shellcheck for shell script linting
sudo apt install shellcheck  # Ubuntu/Debian
brew install shellcheck      # macOS
```

### "npm/pip/pytest not found"
The script gracefully handles missing tools and will warn but not fail.

### "Framework tests timeout"  
Some tests may hang waiting for user input. The script times out after 60 seconds.

### "Permission denied"
```bash
chmod +x scripts/testing/local-pre-commit.sh
```

## Comparison: Before vs After

### Before
- ❌ Developers push code hoping it will pass CI/CD
- ❌ Multiple commit/push cycles to fix CI failures  
- ❌ Different local testing vs GitHub Actions
- ❌ Confusion about what to test locally

### After  
- ✅ Developers test locally before pushing
- ✅ Single commit/push cycle (issues caught locally)
- ✅ Identical local testing and GitHub Actions
- ✅ Clear workflow: local test → commit → push → PR

## Future Enhancements

1. **IDE Integration**: Run local testing from editor
2. **Watch Mode**: Auto-run tests on file changes
3. **Parallel Execution**: Speed up testing with parallel stages
4. **Custom Configurations**: Project-specific testing profiles
5. **Reporting**: Generate detailed test reports

## Questions & Answers

### Q: Do I still need to wait for GitHub Actions?
**A:** Yes, but they should pass immediately since you've tested locally with the same checks.

### Q: What if local testing passes but GitHub Actions fails?
**A:** This should be rare. Check for environment differences or update the local script to match.

### Q: Can I skip local testing for small changes?  
**A:** The PR template requires local testing for all changes. Small changes can still break things!

### Q: How long does local testing take?
**A:** Usually 1-3 minutes, much faster than waiting for CI/CD feedback loops.