# Release System Documentation

## Overview

This project uses the integrated ops CLI automation system for managing releases across all AI agents. The release system ensures consistent versioning, quality gates, and deployment coordination.

## Core Release Commands

### Daily Development Workflow
```bash
# Quality assurance (run before any release)
./scripts/ops qa

# Build verification (test production readiness)
./scripts/ops build --target /tmp/test-build
./scripts/ops verify-prod /tmp/test-build

# Check current project state
./scripts/ops status
```

### Release Commands
```bash
# Patch release (bug fixes: v1.2.3 → v1.2.4)
./scripts/ops release patch

# Minor release (new features: v1.2.3 → v1.3.0)  
./scripts/ops release minor

# Major release (breaking changes: v1.2.3 → v2.0.0)
./scripts/ops release major
```

## Agent Responsibilities in Release Process

### @claude (Technical Leader) - Release Coordinator
**Strategic Release Decisions:**
- **Quality Gates**: Ensure `ops qa` passes before any release
- **Release Timing**: Decide when features are ready for release
- **Version Type**: Determine if changes are patch/minor/major
- **Build Verification**: Mandate `ops build` success before release
- **Final Approval**: Review all agent work before release

**Release Workflow for @claude:**
```bash
# Before coordinating release:
./scripts/ops status              # Check current state
./scripts/ops qa                  # Verify quality standards
./scripts/ops build --target /tmp/release-test
./scripts/ops verify-prod /tmp/release-test

# Coordinate release:
./scripts/ops release [patch|minor|major]
```

### @copilot - Implementation Quality
**Pre-Release Responsibilities:**
- Ensure all simple tasks (Complexity ≤2, Size XS-S) are complete
- Run `ops qa` on all implementation changes
- Verify PR submissions pass quality checks
- Document implementation changes for release notes

**Release Checklist for @copilot:**
```bash
# Before marking tasks complete:
./scripts/ops qa                  # Verify code quality
./scripts/ops build --target /tmp/test
./scripts/ops verify-prod /tmp/test
```

### @gemini - Documentation & Research
**Release Documentation:**
- Update documentation to reflect new features
- Ensure ops CLI commands are documented correctly
- Research and document any breaking changes
- Verify environment setup documentation

**Release Process for @gemini:**
```bash
# Before documentation release:
./scripts/ops qa                  # Check documentation standards
./scripts/ops status              # Document current version info
./scripts/ops env doctor          # Verify environment documentation
```

### @qwen - Performance Verification
**Performance Release Gates:**
- Verify optimizations don't break in production builds
- Ensure performance improvements are measurable
- Test performance in production-like environments
- Document performance gains in release notes

**Performance Release Workflow:**
```bash
# Before performance-related releases:
./scripts/ops qa                  # Baseline performance
./scripts/ops build --target /tmp/perf-test
./scripts/ops verify-prod /tmp/perf-test  # Verify performance holds
```

### @codex - Interactive Testing
**Release Testing:**
- Interactive testing of new features
- TDD verification for release candidates
- User experience validation
- Integration testing with real workflows

**Testing Release Process:**
```bash
# During release testing:
./scripts/ops qa                  # Test code quality
./scripts/ops build --target /tmp/interactive-test
./scripts/ops verify-prod /tmp/interactive-test
```

## Release Workflow Stages

### Stage 1: Pre-Release Quality Gates
**All agents must:**
1. Complete assigned tasks
2. Run `./scripts/ops qa` successfully
3. Verify `./scripts/ops build` works
4. Ensure `./scripts/ops verify-prod` passes
5. Update relevant documentation

### Stage 2: Release Coordination (@claude)
**@claude reviews and coordinates:**
1. Check all agent work is complete
2. Run comprehensive `ops qa` across project
3. Verify production build with `ops build`
4. Test production deployment with `ops verify-prod`
5. Determine appropriate version increment
6. Execute release with `ops release [type]`

### Stage 3: Post-Release Verification
**Automated by ops CLI:**
1. Version tags created in git
2. Changelog updated (if configured)
3. Production build artifacts generated
4. GitHub releases created (if configured)

## Version Management

### Semantic Versioning (SemVer)
- **Patch (1.0.1)**: Bug fixes, small optimizations
- **Minor (1.1.0)**: New features, major optimizations
- **Major (2.0.0)**: Breaking changes, API changes

### Version Source Configuration
**Python Projects:**
```yaml
# .automation/config.yml
versioning:
  source: pyproject.toml
```

**Node.js Projects:**
```yaml
# .automation/config.yml  
versioning:
  source: package.json
```

## Release Quality Standards

### Mandatory Quality Checks
**All releases must pass:**
- Linting: `ruff check .` (Python) or `eslint .` (Node.js)
- Type checking: `mypy src` (Python) or `tsc --noEmit` (Node.js)
- Testing: `pytest -m "not slow"` (Python) or `npm test` (Node.js)
- Build verification: Production build succeeds
- Production testing: `ops verify-prod` passes

### Build Standards
**Production builds must:**
- Include all necessary dependencies
- Work in clean environments
- Pass all quality checks
- Be deployable without development dependencies

## Environment Considerations

### WSL/Windows Development
```bash
# Check environment before release:
./scripts/ops env doctor

# Common issues and solutions documented
# Platform-specific build verification
```

### Cross-Platform Releases
- Test builds on multiple platforms
- Verify environment-specific configurations
- Document platform requirements
- Test installation procedures

## Release Automation Integration

### GitHub Actions Integration
```yaml
# Example workflow trigger
- name: Quality Checks
  run: ./scripts/ops qa

- name: Production Build  
  run: ./scripts/ops build --target dist/

- name: Verify Production
  run: ./scripts/ops verify-prod dist/
```

### Local Release Testing
```bash
# Test release process locally:
./scripts/ops qa
./scripts/ops build --target /tmp/release-test
./scripts/ops verify-prod /tmp/release-test

# Only then proceed with actual release:
./scripts/ops release patch
```

## Troubleshooting Releases

### Common Release Issues

**Build Failures:**
```bash
./scripts/ops env doctor          # Check environment
./scripts/ops qa                  # Identify quality issues
./scripts/ops build --target /tmp/debug  # Test build
```

**Version Conflicts:**
```bash
./scripts/ops status              # Check current versions
# Review git tags and source file versions
```

**Environment Issues:**
```bash
./scripts/ops env doctor          # Diagnose WSL/Windows problems
# Follow recommended fixes
```

### Release Recovery
**If release fails:**
1. Review `ops qa` output for quality issues
2. Check `ops build` output for build problems  
3. Verify `ops verify-prod` passes
4. Fix issues and retry release
5. Never bypass quality gates

## Best Practices

### Agent Coordination
- **@claude** always coordinates final releases
- All agents run `ops qa` before marking tasks complete
- Build verification is mandatory for all changes
- Documentation updates accompany feature releases

### Release Planning
- Plan releases around feature completion
- Coordinate breaking changes carefully
- Test extensively before major releases
- Document all changes thoroughly

### Quality Assurance
- Never bypass `ops qa` requirements
- Always verify production builds
- Test in production-like environments
- Maintain high code quality standards

## Release Notes Template

```markdown
## Version X.Y.Z - YYYY-MM-DD

### Added
- New features implemented by @agent

### Changed  
- Improvements and optimizations by @agent

### Fixed
- Bug fixes and issues resolved by @agent

### Performance
- Performance improvements by @qwen

### Documentation
- Documentation updates by @gemini

### Technical
- Build and infrastructure changes

### Quality Metrics
- Test coverage: X%
- Lint score: X/10
- Build time: X seconds
- Performance improvement: X%
```

This release system ensures consistent, high-quality releases across all AI agent contributions while maintaining production standards and coordinated development workflows.