#!/bin/bash

# Multi-Agent Workflow Automation
# Automated workflows for common development tasks using the MCP router

set -euo pipefail

# Load environment variables
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
  echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
  echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
  echo -e "${RED}❌ $1${NC}"
}

# Check if MCP router is available
check_mcp_router() {
  if [ ! -f "scripts/mcp-router.js" ]; then
    log_error "MCP router not found. Please ensure scripts/mcp-router.js exists."
    exit 1
  fi
}

# Feature development workflow
workflow_feature() {
  local feature_name="$1"
  local description="${2:-Complete feature implementation}"
  
  log_info "Starting feature development workflow for: $feature_name"
  
  # Phase 1: Architecture Planning
  log_info "Phase 1: Architecture Planning"
  local arch_task="Design architecture for $feature_name feature: $description"
  node scripts/mcp-router.js execute "$arch_task"
  
  # Phase 2: Code Generation
  log_info "Phase 2: Code Generation"
  local code_task="Implement $feature_name with $description"
  node scripts/mcp-router.js execute "$code_task"
  
  # Phase 3: Test Generation
  log_info "Phase 3: Test Generation"
  local test_task="Generate comprehensive tests for $feature_name feature"
  node scripts/mcp-router.js execute "$test_task"
  
  # Phase 4: Documentation
  log_info "Phase 4: Documentation"
  local doc_task="Generate API documentation for $feature_name feature"
  node scripts/mcp-router.js execute "$doc_task"
  
  log_success "Feature development workflow completed for: $feature_name"
}

# Bug fix workflow
workflow_bugfix() {
  local bug_description="$1"
  local file_path="${2:-}"
  
  log_info "Starting bug fix workflow for: $bug_description"
  
  # Phase 1: Analysis
  if [ -n "$file_path" ]; then
    log_info "Phase 1: Code Analysis"
    local analysis_task="Analyze code for bugs and issues in $file_path: $bug_description"
    node scripts/mcp-router.js execute "$analysis_task"
  fi
  
  # Phase 2: Reproduction Tests
  log_info "Phase 2: Generate Reproduction Tests"
  local repro_task="Generate test to reproduce bug: $bug_description"
  node scripts/mcp-router.js execute "$repro_task"
  
  # Phase 3: Fix Implementation
  log_info "Phase 3: Bug Fix Implementation"
  local fix_task="Fix bug: $bug_description"
  node scripts/mcp-router.js execute "$fix_task"
  
  # Phase 4: Validation Tests
  log_info "Phase 4: Generate Validation Tests"
  local validation_task="Generate tests to validate bug fix: $bug_description"
  node scripts/mcp-router.js execute "$validation_task"
  
  log_success "Bug fix workflow completed for: $bug_description"
}

# API development workflow
workflow_api() {
  local api_name="$1"
  local endpoints="${2:-CRUD operations}"
  
  log_info "Starting API development workflow for: $api_name"
  
  # Phase 1: API Design
  log_info "Phase 1: API Design"
  local design_task="Design REST API for $api_name with $endpoints"
  node scripts/mcp-router.js execute "$design_task"
  
  # Phase 2: Implementation
  log_info "Phase 2: API Implementation"
  local impl_task="Implement $api_name API endpoints for $endpoints"
  node scripts/mcp-router.js execute "$impl_task"
  
  # Phase 3: Database Schema
  log_info "Phase 3: Database Schema"
  local db_task="Generate SQL schema for $api_name API"
  node scripts/mcp-router.js execute "$db_task"
  
  # Phase 4: API Tests
  log_info "Phase 4: API Testing"
  local test_task="Generate integration tests for $api_name API endpoints"
  node scripts/mcp-router.js execute "$test_task"
  
  # Phase 5: API Documentation
  log_info "Phase 5: API Documentation"
  local doc_task="Generate OpenAPI documentation for $api_name API"
  node scripts/mcp-router.js execute "$doc_task"
  
  log_success "API development workflow completed for: $api_name"
}

# Frontend component workflow
workflow_component() {
  local component_name="$1"
  local framework="${2:-react}"
  local styling="${3:-tailwind}"
  
  log_info "Starting component development workflow for: $component_name"
  
  # Phase 1: Component Design
  log_info "Phase 1: Component Design"
  local design_task="Design $framework component architecture for $component_name"
  node scripts/mcp-router.js execute "$design_task"
  
  # Phase 2: Component Implementation
  log_info "Phase 2: Component Implementation"
  local impl_task="Generate $framework component $component_name with $styling styling"
  node scripts/mcp-router.js execute "$impl_task"
  
  # Phase 3: Component Tests
  log_info "Phase 3: Component Testing"
  local test_task="Generate unit tests for $framework component $component_name"
  node scripts/mcp-router.js execute "$test_task"
  
  # Phase 4: Component Stories/Examples
  log_info "Phase 4: Component Documentation"
  local doc_task="Generate usage examples and documentation for $component_name component"
  node scripts/mcp-router.js execute "$doc_task"
  
  log_success "Component development workflow completed for: $component_name"
}

# Refactoring workflow
workflow_refactor() {
  local file_path="$1"
  local focus="${2:-readability}"
  
  log_info "Starting refactoring workflow for: $file_path"
  
  # Phase 1: Code Analysis
  log_info "Phase 1: Code Analysis"
  local analysis_task="Analyze code quality and issues in $file_path focusing on $focus"
  node scripts/mcp-router.js execute "$analysis_task"
  
  # Phase 2: Refactoring Plan
  log_info "Phase 2: Generate Refactoring Plan"
  local plan_task="Create refactoring plan for $file_path to improve $focus"
  node scripts/mcp-router.js execute "$plan_task"
  
  # Phase 3: Pre-refactor Tests
  log_info "Phase 3: Generate Baseline Tests"
  local baseline_task="Generate comprehensive tests for current behavior of $file_path"
  node scripts/mcp-router.js execute "$baseline_task"
  
  # Phase 4: Refactoring Implementation
  log_info "Phase 4: Refactoring Implementation"
  local refactor_task="Refactor code in $file_path to improve $focus while preserving functionality"
  node scripts/mcp-router.js execute "$refactor_task"
  
  # Phase 5: Post-refactor Validation
  log_info "Phase 5: Validation Tests"
  local validation_task="Generate validation tests to ensure refactored $file_path maintains original behavior"
  node scripts/mcp-router.js execute "$validation_task"
  
  log_success "Refactoring workflow completed for: $file_path"
}

# Database workflow
workflow_database() {
  local entity_name="$1"
  local database="${2:-postgresql}"
  
  log_info "Starting database workflow for: $entity_name"
  
  # Phase 1: Schema Design
  log_info "Phase 1: Schema Design"
  local schema_task="Design $database database schema for $entity_name entity"
  node scripts/mcp-router.js execute "$schema_task"
  
  # Phase 2: Migration Scripts
  log_info "Phase 2: Migration Scripts"
  local migration_task="Generate database migration scripts for $entity_name in $database"
  node scripts/mcp-router.js execute "$migration_task"
  
  # Phase 3: Query Generation
  log_info "Phase 3: Query Generation"
  local query_task="Generate common SQL queries for $entity_name CRUD operations in $database"
  node scripts/mcp-router.js execute "$query_task"
  
  # Phase 4: Data Access Layer
  log_info "Phase 4: Data Access Layer"
  local dal_task="Generate data access layer code for $entity_name entity"
  node scripts/mcp-router.js execute "$dal_task"
  
  log_success "Database workflow completed for: $entity_name"
}

# Quality assurance workflow
workflow_qa() {
  local target="${1:-all}"
  
  log_info "Starting quality assurance workflow for: $target"
  
  # Phase 1: Code Analysis
  log_info "Phase 1: Code Quality Analysis"
  local quality_task="Analyze code quality across $target focusing on maintainability and best practices"
  node scripts/mcp-router.js execute "$quality_task"
  
  # Phase 2: Security Analysis
  log_info "Phase 2: Security Analysis"
  local security_task="Perform security analysis on $target to identify vulnerabilities"
  node scripts/mcp-router.js execute "$security_task"
  
  # Phase 3: Performance Analysis
  log_info "Phase 3: Performance Analysis"
  local perf_task="Analyze performance bottlenecks and optimization opportunities in $target"
  node scripts/mcp-router.js execute "$perf_task"
  
  # Phase 4: Test Coverage Analysis
  log_info "Phase 4: Test Coverage Analysis"
  local coverage_task="Analyze test coverage and generate additional tests for $target"
  node scripts/mcp-router.js execute "$coverage_task"
  
  log_success "Quality assurance workflow completed for: $target"
}

# Usage report
show_usage() {
  log_info "Getting MCP usage report..."
  node scripts/mcp-router.js usage
}

# Help function
show_help() {
  cat << EOF
Multi-Agent Workflow Automation

Usage: $0 <workflow> [arguments...]

Available Workflows:
  feature <name> [description]           - Complete feature development
  bugfix <description> [file_path]       - Bug fix workflow
  api <name> [endpoints]                 - API development workflow
  component <name> [framework] [styling] - Frontend component workflow
  refactor <file_path> [focus]           - Code refactoring workflow
  database <entity> [database_type]      - Database development workflow
  qa [target]                           - Quality assurance workflow
  usage                                 - Show API usage report
  help                                  - Show this help message

Examples:
  $0 feature "user-authentication" "OAuth2 with JWT tokens"
  $0 bugfix "login button not working" "src/components/LoginButton.js"
  $0 api "user-management" "CRUD with role-based access"
  $0 component "UserProfile" "react" "tailwind"
  $0 refactor "src/utils/auth.js" "performance"
  $0 database "User" "postgresql"
  $0 qa "src/auth/"
  $0 usage

Each workflow automatically:
- Analyzes task complexity and requirements
- Routes to optimal AI service (Together AI, Gemini, HuggingFace)
- Falls back to alternatives if rate limits are hit
- Tracks API usage across all services
- Generates comprehensive documentation

EOF
}

# Main function
main() {
  local workflow="${1:-}"
  
  if [ -z "$workflow" ]; then
    show_help
    exit 1
  fi
  
  check_mcp_router
  
  case "$workflow" in
    "feature")
      if [ -z "${2:-}" ]; then
        log_error "Feature name is required"
        echo "Usage: $0 feature <name> [description]"
        exit 1
      fi
      workflow_feature "$2" "${3:-Complete feature implementation}"
      ;;
    "bugfix")
      if [ -z "${2:-}" ]; then
        log_error "Bug description is required"
        echo "Usage: $0 bugfix <description> [file_path]"
        exit 1
      fi
      workflow_bugfix "$2" "${3:-}"
      ;;
    "api")
      if [ -z "${2:-}" ]; then
        log_error "API name is required"
        echo "Usage: $0 api <name> [endpoints]"
        exit 1
      fi
      workflow_api "$2" "${3:-CRUD operations}"
      ;;
    "component")
      if [ -z "${2:-}" ]; then
        log_error "Component name is required"
        echo "Usage: $0 component <name> [framework] [styling]"
        exit 1
      fi
      workflow_component "$2" "${3:-react}" "${4:-tailwind}"
      ;;
    "refactor")
      if [ -z "${2:-}" ]; then
        log_error "File path is required"
        echo "Usage: $0 refactor <file_path> [focus]"
        exit 1
      fi
      workflow_refactor "$2" "${3:-readability}"
      ;;
    "database")
      if [ -z "${2:-}" ]; then
        log_error "Entity name is required"
        echo "Usage: $0 database <entity> [database_type]"
        exit 1
      fi
      workflow_database "$2" "${3:-postgresql}"
      ;;
    "qa")
      workflow_qa "${2:-all}"
      ;;
    "usage")
      show_usage
      ;;
    "help"|"--help"|"-h")
      show_help
      ;;
    *)
      log_error "Unknown workflow: $workflow"
      show_help
      exit 1
      ;;
  esac
}

# Run main function with all arguments
main "$@"