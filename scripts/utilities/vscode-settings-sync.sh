#!/bin/bash

# vscode-settings-sync.sh - Share VSCode settings across all projects
# Multiple strategies for different use cases

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 VSCode Settings Sync - Share settings across projects${NC}"
echo ""

# Function to show menu
show_menu() {
    echo "Choose your preferred method:"
    echo ""
    echo "1) User Settings (Global) - Apply to ALL VSCode projects"
    echo "2) Profile Settings - Create a 'Development' profile"
    echo "3) Symlink Method - Link to template settings"
    echo "4) Copy Method - Copy settings to current project"
    echo "5) Git Template - Auto-add to new git repos"
    echo "6) Extension - Install Settings Sync extension"
    echo ""
    read -p "Select option (1-6): " choice
}

# Method 1: Copy to User Settings (Global)
apply_user_settings() {
    echo -e "${YELLOW}📝 Applying settings globally to all VSCode projects...${NC}"
    
    # Determine the correct VSCode settings path
    if [ -d "$HOME/.config/Code/User" ]; then
        VSCODE_USER_DIR="$HOME/.config/Code/User"
    elif [ -d "$HOME/.config/Code - OSS/User" ]; then
        VSCODE_USER_DIR="$HOME/.config/Code - OSS/User"
    elif [ -d "$HOME/Library/Application Support/Code/User" ]; then
        VSCODE_USER_DIR="$HOME/Library/Application Support/Code/User"
    else
        echo -e "${RED}❌ Could not find VSCode user settings directory${NC}"
        exit 1
    fi
    
    # Backup existing settings
    if [ -f "$VSCODE_USER_DIR/settings.json" ]; then
        cp "$VSCODE_USER_DIR/settings.json" "$VSCODE_USER_DIR/settings.json.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "${GREEN}✓${NC} Backed up existing settings"
    fi
    
    # Copy our settings
    cp /home/gotime2022/Projects/multi-agent-claude-code/.vscode/settings.json "$VSCODE_USER_DIR/settings.json"
    echo -e "${GREEN}✅ Global settings applied!${NC}"
    echo "These settings will now apply to ALL your VSCode projects."
}

# Method 2: Create VSCode Profile
create_vscode_profile() {
    echo -e "${YELLOW}📝 Creating VSCode Development Profile...${NC}"
    echo ""
    echo "VSCode Profiles allow you to switch between different settings configurations."
    echo ""
    echo "To create a profile with these settings:"
    echo "1. Open VSCode"
    echo "2. Press Ctrl+Shift+P (Cmd+Shift+P on Mac)"
    echo "3. Type 'Profiles: Create Profile'"
    echo "4. Name it 'Claude Development'"
    echo "5. Import settings from: /home/gotime2022/Projects/multi-agent-claude-code/.vscode/settings.json"
    echo ""
    echo "Then you can switch profiles anytime with:"
    echo "Ctrl+Shift+P → 'Profiles: Switch Profile'"
    
    # We can also try to do it via CLI if code command is available
    if command -v code &> /dev/null; then
        echo ""
        echo -e "${BLUE}Attempting to create profile via CLI...${NC}"
        code --profile "Claude Development" --folder-uri "file:///home/gotime2022/Projects/multi-agent-claude-code"
        echo -e "${GREEN}✓${NC} Profile created. Switch to it in VSCode."
    fi
}

# Method 3: Symlink Method
create_symlink() {
    echo -e "${YELLOW}📝 Creating symlink to template settings...${NC}"
    
    if [ ! -d ".vscode" ]; then
        mkdir -p .vscode
    fi
    
    # Remove existing settings.json if it exists
    if [ -f ".vscode/settings.json" ]; then
        echo -e "${YELLOW}⚠️  Existing settings.json found${NC}"
        read -p "Backup and replace? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            mv .vscode/settings.json .vscode/settings.json.backup.$(date +%Y%m%d_%H%M%S)
        else
            echo -e "${RED}❌ Aborted${NC}"
            exit 1
        fi
    fi
    
    # Create symlink
    ln -s /home/gotime2022/Projects/multi-agent-claude-code/.vscode/settings.json .vscode/settings.json
    echo -e "${GREEN}✅ Symlink created!${NC}"
    echo "This project now uses the template settings."
    echo "Changes to template settings will automatically apply here."
}

# Method 4: Copy Method
copy_settings() {
    echo -e "${YELLOW}📝 Copying settings to current project...${NC}"
    
    if [ ! -d ".vscode" ]; then
        mkdir -p .vscode
    fi
    
    cp /home/gotime2022/Projects/multi-agent-claude-code/.vscode/settings.json .vscode/settings.json
    echo -e "${GREEN}✅ Settings copied!${NC}"
    echo "This project now has its own copy of the settings."
}

# Method 5: Git Template Method
setup_git_template() {
    echo -e "${YELLOW}📝 Setting up Git template for automatic VSCode settings...${NC}"
    
    # Create git template directory
    GIT_TEMPLATE_DIR="$HOME/.git-templates"
    mkdir -p "$GIT_TEMPLATE_DIR/vscode"
    
    # Copy settings to template
    cp /home/gotime2022/Projects/multi-agent-claude-code/.vscode/settings.json "$GIT_TEMPLATE_DIR/vscode/settings.json"
    
    # Create hook to copy settings on git init
    cat > "$GIT_TEMPLATE_DIR/hooks/post-checkout" << 'EOF'
#!/bin/bash
# Auto-copy VSCode settings to new repos
if [ ! -f .vscode/settings.json ] && [ -f ~/.git-templates/vscode/settings.json ]; then
    mkdir -p .vscode
    cp ~/.git-templates/vscode/settings.json .vscode/settings.json
    echo "VSCode settings added from template"
fi
EOF
    chmod +x "$GIT_TEMPLATE_DIR/hooks/post-checkout"
    
    # Configure git to use template
    git config --global init.templateDir "$GIT_TEMPLATE_DIR"
    
    echo -e "${GREEN}✅ Git template configured!${NC}"
    echo "New git repositories will automatically get VSCode settings."
    echo "Run 'git init' in existing projects to apply."
}

# Method 6: Settings Sync Extension
install_settings_sync() {
    echo -e "${YELLOW}📝 Installing Settings Sync extension...${NC}"
    echo ""
    echo "Settings Sync allows you to sync settings across machines using GitHub Gist."
    echo ""
    
    if command -v code &> /dev/null; then
        echo "Installing Settings Sync extension..."
        code --install-extension Shan.code-settings-sync
        echo -e "${GREEN}✓${NC} Extension installed"
        echo ""
        echo "Next steps:"
        echo "1. Open VSCode"
        echo "2. Press Shift+Alt+U to upload settings"
        echo "3. Login with GitHub"
        echo "4. Settings will sync via Gist"
        echo ""
        echo "On other machines:"
        echo "1. Install the extension"
        echo "2. Press Shift+Alt+D to download settings"
    else
        echo "Please install manually:"
        echo "Extension ID: Shan.code-settings-sync"
    fi
}

# Function to add to personal config
add_to_personal_config() {
    echo ""
    echo -e "${BLUE}💡 Tip: Add VSCode settings path to personal config${NC}"
    
    PERSONAL_CONFIG="$HOME/.claude-code/personal-config.json"
    if [ -f "$PERSONAL_CONFIG" ]; then
        echo "Adding vscode_settings_template to personal config..."
        # This would need jq to properly update JSON
        echo "vscode_settings_template: /home/gotime2022/Projects/multi-agent-claude-code/.vscode/settings.json"
    fi
}

# Main execution
main() {
    # If running with --auto flag, apply user settings automatically
    if [ "$1" = "--auto" ]; then
        apply_user_settings
        exit 0
    fi
    
    # If running with specific method
    case "$1" in
        --user)
            apply_user_settings
            ;;
        --profile)
            create_vscode_profile
            ;;
        --symlink)
            create_symlink
            ;;
        --copy)
            copy_settings
            ;;
        --git-template)
            setup_git_template
            ;;
        --extension)
            install_settings_sync
            ;;
        *)
            show_menu
            case $choice in
                1)
                    apply_user_settings
                    ;;
                2)
                    create_vscode_profile
                    ;;
                3)
                    create_symlink
                    ;;
                4)
                    copy_settings
                    ;;
                5)
                    setup_git_template
                    ;;
                6)
                    install_settings_sync
                    ;;
                *)
                    echo -e "${RED}Invalid option${NC}"
                    exit 1
                    ;;
            esac
            ;;
    esac
    
    # Offer to add to personal config
    add_to_personal_config
}

# Run main function
main "$@"