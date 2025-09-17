#!/bin/bash
# Rollback Script for SignalHire Agent
#
# PURPOSE: Safely rollback to a previous version
# USAGE: ./rollback.sh <version> [target_dir]
# PART OF: Deployment system
# CONNECTS TO: Git tags, production deployment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[ROLLBACK]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

cd "$PROJECT_ROOT"

# Function to show available versions
show_available_versions() {
    echo "Available versions:"
    git tag --list "v*" --sort=-version:refname | head -10
}

# Main rollback logic
main() {
    local target_version="$1"
    local target_dir="$2"

    if [[ -z "$target_version" ]]; then
        print_error "Usage: $0 <version> [target_dir]"
        echo ""
        show_available_versions
        exit 1
    fi

    # Validate version exists
    if ! git tag --list | grep -q "^${target_version}$"; then
        if ! git tag --list | grep -q "^v${target_version}$"; then
            print_error "Version $target_version not found"
            echo ""
            show_available_versions
            exit 1
        else
            target_version="v${target_version}"
        fi
    fi

    # Get current version for comparison
    local current_version=$(git describe --tags --abbrev=0 2>/dev/null || echo "unknown")

    print_status "Current version: $current_version"
    print_status "Rolling back to: $target_version"

    # Safety check - don't rollback to same version
    if [[ "$current_version" == "$target_version" ]]; then
        print_warning "Already at version $target_version"
        exit 0
    fi

    # Show what will happen
    print_warning "This will:"
    print_warning "  - Checkout $target_version"
    print_warning "  - Rebuild production deployment"
    print_warning "  - Update target directory"

    if [[ -n "$target_dir" ]]; then
        print_warning "  - Deploy to: $target_dir"
    fi

    echo ""
    read -p "Continue with rollback? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Rollback cancelled"
        exit 0
    fi

    # Create backup of current state
    print_status "Creating backup of current state..."
    local backup_dir="/tmp/signalhire-backup-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$backup_dir"

    if [[ -d "$target_dir" ]]; then
        cp -r "$target_dir" "$backup_dir/current-deployment"
        print_status "Backup created: $backup_dir"
    fi

    # Stash any uncommitted changes
    if [[ -n "$(git status --porcelain)" ]]; then
        print_status "Stashing uncommitted changes..."
        git stash push -m "Pre-rollback stash $(date)"
    fi

    # Checkout the target version
    print_status "Checking out $target_version..."
    git checkout "$target_version"

    # Rebuild if target directory specified
    if [[ -n "$target_dir" ]]; then
        print_status "Rebuilding to $target_dir..."
        ./devops/deploy/commands/build-production.sh "$target_dir" --force

        # Verify the deployment
        print_status "Verifying deployment..."
        if [[ -f "$target_dir/signalhire-agent" ]]; then
            print_success "Deployment verified"
        else
            print_error "Deployment verification failed"
            print_status "Backup available: $backup_dir"
            exit 1
        fi
    fi

    print_success "Rollback to $target_version complete"

    # Show rollback summary
    echo ""
    echo "📋 Rollback Summary:"
    echo "   Previous version: $current_version"
    echo "   Current version:  $target_version"
    echo "   Target directory: ${target_dir:-Not specified}"
    echo "   Backup location:  $backup_dir"
    echo "   Timestamp:        $(date)"

    # Check if we stashed changes
    if git stash list | grep -q "Pre-rollback stash"; then
        print_warning "Uncommitted changes were stashed"
        echo "   To restore: git stash pop"
    fi

    echo ""
    print_status "To undo this rollback:"
    echo "   git checkout $current_version"
    echo "   ./rollback.sh $current_version $target_dir"
}

# Show help if requested
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    echo "SignalHire Agent Rollback Script"
    echo ""
    echo "USAGE:"
    echo "    $0 <version> [target_dir]"
    echo ""
    echo "ARGUMENTS:"
    echo "    version     Git tag to rollback to (e.g., v1.2.3 or 1.2.3)"
    echo "    target_dir  Production deployment directory (optional)"
    echo ""
    echo "EXAMPLES:"
    echo "    $0 v1.2.3"
    echo "    $0 1.2.3 ~/deploy/signalhire"
    echo ""
    show_available_versions
    exit 0
fi

main "$@"
