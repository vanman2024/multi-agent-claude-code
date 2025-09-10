# Infrastructure Requirements Template for Spec-Kit

When using spec-kit's `/specify` command, include these infrastructure requirements in your prompt to ensure comprehensive task generation:

## Essential Infrastructure Components

### 1. CI/CD Pipeline
```
The application must include:
- GitHub Actions workflow for CI/CD
- Automated testing on every PR
- Build and deployment pipeline
- Environment-specific deployments (dev/staging/prod)
- Automated version tagging and releases
```

### 2. Containerization
```
Full Docker support including:
- Dockerfile for each service
- Docker Compose for local development
- Container orchestration setup
- Multi-stage builds for optimization
- Container registry integration
```

### 3. Testing Infrastructure
```
Comprehensive testing setup:
- Unit test projects and framework
- Integration test infrastructure
- End-to-end test setup
- Test data seeding and fixtures
- Code coverage reporting
- Performance testing framework
```

### 4. Database & Migrations
```
Database infrastructure:
- Migration system setup
- Seed data scripts
- Backup and restore procedures
- Connection pooling configuration
- Database versioning
```

### 5. Monitoring & Observability
```
Production monitoring:
- Application Performance Monitoring (APM)
- Centralized logging setup
- Health check endpoints
- Metrics and dashboards
- Error tracking integration
- Distributed tracing
```

### 6. Security Infrastructure
```
Security components:
- Authentication and authorization system
- API rate limiting
- Security headers configuration
- Dependency vulnerability scanning
- Secret management setup
- CORS configuration
```

### 7. Development Tools
```
Developer experience:
- Pre-commit hooks
- Code formatting configuration
- Linting setup
- Hot reload configuration
- Debug configurations
- Environment variable management
```

### 8. Documentation
```
Documentation infrastructure:
- API documentation generation
- Architecture diagrams
- README templates
- Contributing guidelines
- Deployment guides
```

## Example Comprehensive Prompt

```
Develop [ApplicationName], a [description]. 

[Core features description...]

Infrastructure Requirements:
- Complete CI/CD pipeline using GitHub Actions with automated testing, building, and deployment
- Docker containerization for all services with docker-compose for local development
- Comprehensive test infrastructure including unit, integration, and e2e tests with coverage reporting
- Database migrations system with versioning and rollback capabilities
- Production monitoring with APM, centralized logging, and health checks
- Security infrastructure including authentication, rate limiting, and vulnerability scanning
- Developer tools including pre-commit hooks, linting, and hot reload
- Auto-generated API documentation and deployment guides
- Multi-environment support (development, staging, production) with environment-specific configs
- Automated dependency updates and security patches
- Performance testing and load testing capabilities
- Feature flags system for gradual rollouts
- Blue-green deployment support
- Database backup and disaster recovery procedures
- Kubernetes manifests for cloud deployment (if applicable)
```

## Expected Task Generation

With comprehensive requirements, spec-kit should generate:

### Infrastructure Tasks (T001-T020)
- T001: Create solution/project structure
- T002: Initialize version control
- T003: Setup Docker and docker-compose
- T004: Configure CI/CD pipeline
- T005: Setup testing infrastructure
- T006: Configure database and migrations
- T007: Setup monitoring and logging
- T008: Configure security components
- T009: Setup development tools
- T010: Create documentation structure
- T011: Configure environments
- T012: Setup deployment scripts
- T013: Configure container registry
- T014: Setup secret management
- T015: Configure backup procedures
- T016: Setup feature flags
- T017: Configure APM
- T018: Setup error tracking
- T019: Configure rate limiting
- T020: Setup API documentation

### Then Application Tasks (T021+)
- Tests
- Core features
- UI components
- etc.

## Using This Template

1. Copy relevant sections for your project
2. Include in your `/specify` prompt
3. Spec-kit will generate comprehensive infrastructure tasks
4. Import to Claude Code with `/import-tasks`
5. Execute systematically starting with infrastructure

This ensures your project has production-ready infrastructure from day one!