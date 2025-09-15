#!/bin/bash
# Docker Development Scripts Template
# Consistent development workflows across all environments

set -e  # Exit on error

PROJECT_NAME=${PROJECT_NAME:-$(basename $(pwd))}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Development Environment Commands
dev_up() {
    log_info "Starting development environment..."
    check_docker
    docker-compose -f docker-compose.dev.yml up -d
    log_success "Development environment started!"
    log_info "VS Code: Open folder in dev container"
    log_info "Python: http://localhost:8000"
    log_info "Frontend: http://localhost:3000"
}

dev_down() {
    log_info "Stopping development environment..."
    docker-compose -f docker-compose.dev.yml down
    log_success "Development environment stopped!"
}

dev_restart() {
    log_info "Restarting development environment..."
    dev_down
    dev_up
}

dev_logs() {
    local service=${1:-python-dev}
    log_info "Showing logs for service: $service"
    docker-compose -f docker-compose.dev.yml logs -f "$service"
}

dev_shell() {
    local service=${1:-python-dev}
    log_info "Opening shell in service: $service"
    docker-compose -f docker-compose.dev.yml exec "$service" bash
}

dev_python() {
    log_info "Opening Python shell in development container..."
    docker-compose -f docker-compose.dev.yml exec python-dev python
}

dev_test() {
    log_info "Running tests in development container..."
    docker-compose -f docker-compose.dev.yml exec python-dev pytest "$@"
}

dev_lint() {
    log_info "Running linting in development container..."
    docker-compose -f docker-compose.dev.yml exec python-dev bash -c "
        black --check . &&
        isort --check-only . &&
        flake8 . &&
        mypy .
    "
}

dev_format() {
    log_info "Formatting code in development container..."
    docker-compose -f docker-compose.dev.yml exec python-dev bash -c "
        black . &&
        isort .
    "
    log_success "Code formatted!"
}

dev_install() {
    log_info "Installing dependencies in development container..."
    docker-compose -f docker-compose.dev.yml exec python-dev pip install -r requirements.txt
    if [ -f "requirements-dev.txt" ]; then
        docker-compose -f docker-compose.dev.yml exec python-dev pip install -r requirements-dev.txt
    fi
    log_success "Dependencies installed!"
}

dev_clean() {
    log_warning "This will remove all containers, images, and volumes for this project."
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Cleaning up Docker resources..."
        docker-compose -f docker-compose.dev.yml down -v --remove-orphans
        docker system prune -f
        log_success "Cleanup complete!"
    else
        log_info "Cleanup cancelled."
    fi
}

dev_rebuild() {
    log_info "Rebuilding development containers..."
    docker-compose -f docker-compose.dev.yml build --no-cache
    log_success "Containers rebuilt!"
}

dev_status() {
    log_info "Development environment status:"
    docker-compose -f docker-compose.dev.yml ps
}

# WSL-specific helpers
wsl_fix_permissions() {
    log_info "Fixing WSL file permissions..."
    find . -name "*.py" -exec chmod +x {} \;
    find . -name "*.sh" -exec chmod +x {} \;
    log_success "Permissions fixed!"
}

wsl_docker_desktop() {
    log_info "WSL Docker Desktop integration check..."
    if grep -q "docker-desktop" /proc/version; then
        log_success "Running in WSL with Docker Desktop integration"
    else
        log_warning "Not using Docker Desktop integration - consider enabling it"
    fi
}

# Production helpers
prod_build() {
    log_info "Building production image..."
    docker build -t "${PROJECT_NAME}:latest" --target production .
    log_success "Production image built!"
}

prod_run() {
    log_info "Running production container..."
    docker run -p 8000:8000 --env-file .env "${PROJECT_NAME}:latest"
}

# Help function
show_help() {
    cat << EOF
Docker Development Scripts for ${PROJECT_NAME}

Usage: ./docker-scripts.sh <command> [arguments]

Development Commands:
  dev-up           Start development environment
  dev-down         Stop development environment  
  dev-restart      Restart development environment
  dev-logs [service] Show logs (default: python-dev)
  dev-shell [service] Open shell (default: python-dev)
  dev-python       Open Python REPL
  dev-test [args]  Run tests with pytest
  dev-lint         Run all linting tools
  dev-format       Format code with black & isort
  dev-install      Install/update dependencies
  dev-clean        Remove all Docker resources
  dev-rebuild      Rebuild containers from scratch
  dev-status       Show container status

WSL Helpers:
  wsl-fix-permissions  Fix file permissions in WSL
  wsl-docker-desktop   Check Docker Desktop integration

Production:
  prod-build       Build production Docker image
  prod-run         Run production container

Examples:
  ./docker-scripts.sh dev-up
  ./docker-scripts.sh dev-shell python-dev
  ./docker-scripts.sh dev-test tests/
  ./docker-scripts.sh dev-logs postgres-dev

EOF
}

# Main script logic
case "${1:-}" in
    dev-up)         dev_up ;;
    dev-down)       dev_down ;;
    dev-restart)    dev_restart ;;
    dev-logs)       dev_logs "$2" ;;
    dev-shell)      dev_shell "$2" ;;
    dev-python)     dev_python ;;
    dev-test)       shift; dev_test "$@" ;;
    dev-lint)       dev_lint ;;
    dev-format)     dev_format ;;
    dev-install)    dev_install ;;
    dev-clean)      dev_clean ;;
    dev-rebuild)    dev_rebuild ;;
    dev-status)     dev_status ;;
    wsl-fix-permissions) wsl_fix_permissions ;;
    wsl-docker-desktop)  wsl_docker_desktop ;;
    prod-build)     prod_build ;;
    prod-run)       prod_run ;;
    help|--help|-h) show_help ;;
    "")             show_help ;;
    *)              log_error "Unknown command: $1"; show_help; exit 1 ;;
esac