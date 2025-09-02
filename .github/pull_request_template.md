## 📋 Pull Request Checklist

### Required Checks ✅
**ALL checkboxes must be checked before merge:**

- [ ] **Local Pre-Commit Testing**
  - [ ] Ran `./scripts/testing/local-pre-commit.sh` successfully
  - [ ] All critical stages passed (0 failed stages)
  - [ ] Addressed any critical warnings found
  - [ ] Local testing matches GitHub Actions pipeline

- [ ] **Code Quality**
  - [ ] Lint passes (`npm run lint` or equivalent)
  - [ ] Type checking passes (`npm run typecheck` or equivalent)
  - [ ] No console.log or debug statements left
  - [ ] No commented-out code

- [ ] **Testing**
  - [ ] All existing tests pass
  - [ ] New tests added for new features (if applicable)
  - [ ] Manual testing completed

- [ ] **Documentation**
  - [ ] Code comments added where needed
  - [ ] README updated if needed
  - [ ] API documentation updated if endpoints changed

- [ ] **Security**
  - [ ] No secrets or API keys in code
  - [ ] Input validation added
  - [ ] No security warnings from tools

## 🎯 What This PR Does

**Closes:** #[issue_number]

**Type of Change:**
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] ♻️ Code refactoring
- [ ] 🎨 Style/UI update

## 📝 Implementation Summary
<!-- Brief description of HOW the changes were implemented -->

## 🏗️ Implementation Phases Completed
<!-- Check off the phases that were completed in this PR -->
- [ ] **Phase 1: Foundation**
  - [ ] Database schema changes
  - [ ] Basic API endpoints
  - [ ] Component structure setup
  - [ ] Routing configuration

- [ ] **Phase 2: Core Functionality**
  - [ ] Business logic implementation
  - [ ] Frontend-backend integration
  - [ ] Input validation
  - [ ] State management

- [ ] **Phase 3: Polish & Quality**
  - [ ] Error handling
  - [ ] Loading states
  - [ ] Performance optimization
  - [ ] User experience enhancements

- [ ] **Phase 4: Deployment Readiness**
  - [ ] Environment configuration
  - [ ] Database migrations
  - [ ] Feature flags (if applicable)
  - [ ] Monitoring/logging setup

## 🧪 Testing Completed

### Unit Tests
- [ ] New components tested
- [ ] API endpoints tested
- [ ] Utility functions tested
- [ ] State management tested

### Integration Tests
- [ ] User flow testing completed
- [ ] Database integration tested
- [ ] External API mocking verified
- [ ] Error scenarios handled

### Manual Testing
- [ ] Happy path tested
- [ ] Edge cases verified
- [ ] Cross-browser compatibility (if applicable)
- [ ] Mobile responsiveness (if applicable)
- [ ] Performance tested under load

### Local Pre-Commit Testing
- [ ] **Local testing script completed**: `./scripts/testing/local-pre-commit.sh`
- [ ] **All GitHub Actions checks verified locally**:
  - [ ] Code quality (linting, type checking, formatting)
  - [ ] Unit tests passed
  - [ ] Security scanning completed
  - [ ] Build test passed
  - [ ] Git status verified
- [ ] **Warnings addressed**: Any non-critical warnings were reviewed and addressed if necessary

### Test Results
<!-- Describe specific test results and any issues found/resolved -->

## 📸 Screenshots (if applicable)
<!-- Add screenshots to help explain your changes -->

## ⚠️ Breaking Changes & Migration
<!-- List any breaking changes and required migration steps -->

### Database Changes
- [ ] No database changes
- [ ] Schema migrations included
- [ ] Data migration required
- [ ] Backward compatibility maintained

### API Changes
- [ ] No API changes
- [ ] New endpoints added
- [ ] Existing endpoints modified
- [ ] Deprecation notices added

### Configuration Changes
- [ ] No config changes required
- [ ] New environment variables needed
- [ ] Updated deployment scripts
- [ ] Documentation updated

## 🔄 Related Issues
<!-- Link any related issues besides the one being closed -->

---

### Merge Requirements
**This PR cannot be merged until:**
1. ✅ All checkboxes above are checked
2. ✅ CI/CD pipeline passes
3. ✅ At least one approval received
4. ✅ No unresolved conversations

> **Note:** GitHub Actions will verify checkbox completion before allowing merge.