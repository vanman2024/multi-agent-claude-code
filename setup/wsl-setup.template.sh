#!/bin/bash
# WSL Development Environment Setup Script
# Optimizes WSL for Docker and Python development

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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

# Check if running in WSL
check_wsl() {
    if ! grep -q microsoft /proc/version; then
        log_error "This script is designed for WSL environments only"
        exit 1
    fi
    log_success "Running in WSL environment"
}

# Update WSL and install essential packages
update_wsl() {
    log_info "Updating WSL packages..."
    sudo apt update && sudo apt upgrade -y
    
    log_info "Installing essential development packages..."
    sudo apt install -y \
        curl \
        wget \
        git \
        vim \
        nano \
        htop \
        tree \
        unzip \
        build-essential \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release
    
    log_success "Essential packages installed"
}

# Install Python and pip
setup_python() {
    log_info "Setting up Python development environment..."
    
    # Install Python 3.12 and related tools
    sudo apt install -y \
        python3.12 \
        python3.12-dev \
        python3.12-venv \
        python3-pip \
        python-is-python3
    
    # Upgrade pip and install common development tools
    python -m pip install --user --upgrade \
        pip \
        setuptools \
        wheel \
        virtualenv \
        pipenv \
        poetry
    
    # Add user bin to PATH if not already there
    if ! echo $PATH | grep -q "$HOME/.local/bin"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
        log_info "Added ~/.local/bin to PATH"
    fi
    
    log_success "Python environment setup complete"
}

# Setup Docker for WSL
setup_docker() {
    log_info "Setting up Docker for WSL..."
    
    # Check if Docker Desktop is installed on Windows
    if [ -f "/mnt/c/Program Files/Docker/Docker/Docker Desktop.exe" ]; then
        log_success "Docker Desktop detected on Windows"
        log_info "Make sure Docker Desktop has WSL integration enabled"
        log_info "Docker Desktop -> Settings -> Resources -> WSL Integration"
        return 0
    fi
    
    # Install Docker Engine directly in WSL
    log_info "Installing Docker Engine in WSL..."
    
    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Add Docker repository
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    
    # Start Docker service
    sudo service docker start
    
    log_success "Docker Engine installed"
    log_warning "Please log out and back in for docker group changes to take effect"
}

# Setup Node.js
setup_nodejs() {
    log_info "Setting up Node.js..."
    
    # Install Node Version Manager (nvm)
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    
    # Source nvm
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    
    # Install latest LTS Node.js
    nvm install --lts
    nvm use --lts
    nvm alias default node
    
    # Install global packages
    npm install -g \
        yarn \
        pnpm \
        @vue/cli \
        create-react-app \
        @angular/cli \
        typescript \
        nodemon
    
    log_success "Node.js environment setup complete"
}

# Configure Git
setup_git() {
    log_info "Configuring Git..."
    
    # Check if Git is already configured
    if git config --global user.name > /dev/null 2>&1; then
        log_info "Git already configured"
        return 0
    fi
    
    # Prompt for Git configuration
    read -p "Enter your Git username: " git_username
    read -p "Enter your Git email: " git_email
    
    git config --global user.name "$git_username"
    git config --global user.email "$git_email"
    git config --global init.defaultBranch main
    git config --global pull.rebase false
    
    # Setup SSH key if not exists
    if [ ! -f ~/.ssh/id_rsa ]; then
        log_info "Generating SSH key for Git..."
        ssh-keygen -t rsa -b 4096 -C "$git_email" -f ~/.ssh/id_rsa -N ""
        eval "$(ssh-agent -s)"
        ssh-add ~/.ssh/id_rsa
        
        log_success "SSH key generated: ~/.ssh/id_rsa.pub"
        log_info "Add this key to your GitHub account:"
        cat ~/.ssh/id_rsa.pub
    fi
    
    log_success "Git configuration complete"
}

# Fix WSL file permissions
fix_permissions() {
    log_info "Fixing WSL file permissions..."
    
    # Create or update /etc/wsl.conf
    sudo tee /etc/wsl.conf > /dev/null << EOF
[automount]
enabled = true
root = /mnt/
options = "metadata,umask=22,fmask=11"
mountFsTab = false

[network]
generateHosts = true
generateResolvConf = true

[interop]
enabled = true
appendWindowsPath = true
EOF
    
    log_success "WSL configuration updated"
    log_warning "Restart WSL for changes to take effect: wsl --shutdown"
}

# Setup VS Code integration
setup_vscode() {
    log_info "Setting up VS Code WSL integration..."
    
    # Install code command if not available
    if ! command -v code > /dev/null 2>&1; then
        log_info "Installing VS Code WSL command..."
        # This usually gets installed automatically when you open WSL from VS Code
        log_info "Please install VS Code on Windows and the Remote-WSL extension"
        log_info "Then run 'code .' from WSL to install the command"
    else
        log_success "VS Code command available"
    fi
}

# Performance optimizations
optimize_performance() {
    log_info "Applying WSL performance optimizations..."
    
    # Update .bashrc with useful aliases and settings
    cat >> ~/.bashrc << 'EOF'

# WSL Development Aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Docker aliases
alias dps='docker ps'
alias dpa='docker ps -a'
alias di='docker images'
alias dsp='docker system prune -f'
alias dcup='docker-compose up -d'
alias dcdown='docker-compose down'

# Python aliases
alias py='python'
alias pip='python -m pip'
alias venv='python -m venv'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline'

# Development shortcuts
alias cls='clear'
alias h='history'
alias reload='source ~/.bashrc'

# WSL shortcuts
alias windir='cd /mnt/c/Users/$USER'
alias desktop='cd /mnt/c/Users/$USER/Desktop'
alias downloads='cd /mnt/c/Users/$USER/Downloads'

EOF
    
    log_success "Bash aliases and optimizations added"
}

# Main setup function
run_setup() {
    log_info "Starting WSL development environment setup..."
    
    check_wsl
    update_wsl
    setup_python
    setup_docker
    setup_nodejs
    setup_git
    fix_permissions
    setup_vscode
    optimize_performance
    
    log_success "WSL development environment setup complete!"
    log_info "Next steps:"
    log_info "1. Restart WSL: wsl --shutdown (from Windows)"
    log_info "2. Reopen WSL terminal"
    log_info "3. Run: source ~/.bashrc"
    log_info "4. Test Docker: docker --version"
    log_info "5. Test Python: python --version"
    log_info "6. Test Node: node --version"
    log_info "7. Setup your first project with Docker development environment"
}

# Help function
show_help() {
    cat << EOF
WSL Development Environment Setup Script

Usage: ./wsl-setup.sh [command]

Commands:
  setup        Run complete WSL development setup
  python       Setup Python environment only
  docker       Setup Docker environment only  
  nodejs       Setup Node.js environment only
  git          Configure Git only
  permissions  Fix WSL permissions only
  vscode       Setup VS Code integration only
  optimize     Apply performance optimizations only
  help         Show this help message

Examples:
  ./wsl-setup.sh setup      # Full setup
  ./wsl-setup.sh python     # Python only
  ./wsl-setup.sh docker     # Docker only

EOF
}

# Command line interface
case "${1:-setup}" in
    setup)          run_setup ;;
    python)         setup_python ;;
    docker)         setup_docker ;;
    nodejs)         setup_nodejs ;;
    git)            setup_git ;;
    permissions)    fix_permissions ;;
    vscode)         setup_vscode ;;
    optimize)       optimize_performance ;;
    help|--help|-h) show_help ;;
    *)              log_error "Unknown command: $1"; show_help; exit 1 ;;
esac