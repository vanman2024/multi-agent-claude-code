## 📋 Pull Request Checklist

### Required Checks ✅
**ALL checkboxes must be checked before merge:**

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

## 📝 Description
<!-- Provide a brief description of the changes -->

## 🧪 How Has This Been Tested?
<!-- Describe the tests you ran -->

## 📸 Screenshots (if applicable)
<!-- Add screenshots to help explain your changes -->

## ⚠️ Breaking Changes
<!-- List any breaking changes and migration steps -->

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