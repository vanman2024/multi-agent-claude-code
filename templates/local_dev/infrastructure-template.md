# Infrastructure Task: [Task Name]

## Overview
**Type**: Infrastructure/DevOps
**Priority**: P0/P1/P2
**Complexity**: Low/Medium/High
**Estimated Time**: X hours

## Description
[Clear description of what infrastructure needs to be set up or configured]

## Objectives
<!-- Goals this infrastructure change aims to achieve -->
- [Specific objective 1]
- [Specific objective 2]
- [Specific objective 3]

## Technical Requirements

### Environment
- **Local Development**: [Requirements for local setup]
- **CI/CD**: [Pipeline requirements]
- **Production**: [Production environment needs]

### Services/Tools
- [Service 1]: [How it's used]
- [Service 2]: [Configuration needed]
- [Tool]: [Purpose]

## Implementation Steps

1. **Setup/Configuration**
   - [ ] [Step 1 with specific command/action]
   - [ ] [Step 2 with configuration details]
   - [ ] [Step 3 with verification method]

2. **Integration**
   - [ ] [Connect to existing systems]
   - [ ] [Configure environment variables]
   - [ ] [Set up secrets management]

3. **Testing**
   - [ ] [Test in development]
   - [ ] [Test in staging/preview]
   - [ ] [Verify production readiness]

## Configuration Files

### Example: `.env.example`
```env
# Service Configuration
SERVICE_API_KEY=
SERVICE_URL=
```

### Example: `docker-compose.yml`
```yaml
version: '3.8'
services:
  app:
    # Configuration
```

### Example: `.github/workflows/ci.yml`
```yaml
name: CI Pipeline
on: [push, pull_request]
jobs:
  # Job configuration
```

## Verification Checklist
<!-- Verify these items are complete before considering done -->
- Service is accessible locally
- Environment variables are documented
- CI/CD pipeline runs successfully
- Monitoring/alerts are configured
- Documentation is updated
- Team has access/credentials

## Security Considerations
<!-- Ensure these security measures are in place -->
- Secrets are properly managed (not in code)
- Access controls are configured
- Security headers/policies applied
- Backup strategy defined

## Dependencies
- **Depends on**: [Other infrastructure that must exist first]
- **Blocks**: [Features that need this infrastructure]

## Resources
- [Documentation link]
- [Service dashboard]
- [Configuration guide]

---

## Metadata
*For automation parsing - DO NOT REMOVE*

**Priority**: P0
**Size**: M
**Points**: 5
**Component**: Infrastructure
**Layer**: Plumbing (CI/CD)