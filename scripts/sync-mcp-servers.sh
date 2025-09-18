#!/bin/bash

# Sync MCP Servers Configuration Across AI Agents
# This script reads from a central MCP configuration and applies it to all agents

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../config/mcp-servers.json"

# Project-specific variables (can be overridden)
SUPABASE_PROJECT_REF="${SUPABASE_PROJECT_REF:-}"
SUPABASE_ACCESS_TOKEN="${SUPABASE_ACCESS_TOKEN:-}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"

# Function to check dependencies
check_dependencies() {
    if ! command -v jq &> /dev/null; then
        echo -e "${YELLOW}⚠️  jq not installed. Installing...${NC}"
        sudo apt-get update && sudo apt-get install -y jq
    fi
}

# Function to load project-specific environment
load_project_env() {
    local PROJECT_DIR="${1:-$(pwd)}"
    
    # Check for .env.mcp file
    if [ -f "$PROJECT_DIR/.env.mcp" ]; then
        echo -e "${BLUE}📋 Loading project-specific MCP configuration...${NC}"
        source "$PROJECT_DIR/.env.mcp"
    fi
    
    # Check for .env file as fallback
    if [ -f "$PROJECT_DIR/.env" ] && [ -z "$SUPABASE_PROJECT_REF" ]; then
        # Extract MCP-related vars from .env
        if grep -q "SUPABASE_PROJECT_REF" "$PROJECT_DIR/.env"; then
            export SUPABASE_PROJECT_REF=$(grep "SUPABASE_PROJECT_REF" "$PROJECT_DIR/.env" | cut -d'=' -f2 | tr -d '"')
        fi
        if grep -q "SUPABASE_ACCESS_TOKEN" "$PROJECT_DIR/.env"; then
            export SUPABASE_ACCESS_TOKEN=$(grep "SUPABASE_ACCESS_TOKEN" "$PROJECT_DIR/.env" | cut -d'=' -f2 | tr -d '"')
        fi
    fi
}

# Function to sync to Gemini (JSON format)
sync_gemini() {
    echo -e "${BLUE}📋 Configuring Gemini MCP servers...${NC}"
    
    mkdir -p ~/.gemini
    
    # Read existing settings or create new
    if [ -f ~/.gemini/settings.json ]; then
        cp ~/.gemini/settings.json ~/.gemini/settings.json.backup
        EXISTING_SETTINGS=$(cat ~/.gemini/settings.json)
    else
        EXISTING_SETTINGS='{"hasSeenIdeIntegrationNudge":true,"ideMode":true,"selectedAuthType":"gemini-oauth"}'
    fi
    
    # Extract MCP servers from central config and format for Gemini
    MCP_SERVERS=$(jq '.servers | to_entries | map(
        select(.value.transport == "stdio") | {
            key: .key,
            value: {
                command: .value.command,
                args: (
                    if .value.env_args then
                        .value.args + (.value.env_args | map(
                            gsub("\\$\\{SUPABASE_PROJECT_REF\\}"; env.SUPABASE_PROJECT_REF) |
                            gsub("\\$\\{SUPABASE_ACCESS_TOKEN\\}"; env.SUPABASE_ACCESS_TOKEN)
                        ))
                    else
                        .value.args
                    end
                )
            }
        }
    ) + (
        map(select(.value.transport == "http") | {
            key: .key,
            value: {
                httpUrl: .value.httpUrl
            }
        })
    ) | from_entries' "$CONFIG_FILE")
    
    # Merge with existing settings
    echo "$EXISTING_SETTINGS" | jq --argjson mcp "$MCP_SERVERS" '.mcpServers = $mcp' > ~/.gemini/settings.json
    
    echo -e "${GREEN}✅ Gemini MCP servers configured${NC}"
}

# Function to sync to Qwen (JSON format like Gemini)
sync_qwen() {
    echo -e "${BLUE}📋 Configuring Qwen MCP servers...${NC}"
    
    mkdir -p ~/.qwen
    
    # Read existing settings or create new
    if [ -f ~/.qwen/settings.json ]; then
        cp ~/.qwen/settings.json ~/.qwen/settings.json.backup
        EXISTING_SETTINGS=$(cat ~/.qwen/settings.json)
    else
        EXISTING_SETTINGS='{"hasSeenIdeIntegrationNudge":true,"ideMode":true,"selectedAuthType":"qwen-oauth"}'
    fi
    
    # Use same MCP servers extraction as Gemini
    MCP_SERVERS=$(jq '.servers | to_entries | map(
        select(.value.transport == "stdio") | {
            key: .key,
            value: {
                command: .value.command,
                args: (
                    if .value.env_args then
                        .value.args + (.value.env_args | map(
                            gsub("\\$\\{SUPABASE_PROJECT_REF\\}"; env.SUPABASE_PROJECT_REF) |
                            gsub("\\$\\{SUPABASE_ACCESS_TOKEN\\}"; env.SUPABASE_ACCESS_TOKEN)
                        ))
                    else
                        .value.args
                    end
                )
            }
        }
    ) + (
        map(select(.value.transport == "http") | {
            key: .key,
            value: {
                httpUrl: .value.httpUrl
            }
        })
    ) | from_entries' "$CONFIG_FILE")
    
    # Merge with existing settings
    echo "$EXISTING_SETTINGS" | jq --argjson mcp "$MCP_SERVERS" '.mcpServers = $mcp' > ~/.qwen/settings.json
    
    echo -e "${GREEN}✅ Qwen MCP servers configured${NC}"
}

# Function to sync to Codex (TOML format)
sync_codex() {
    echo -e "${BLUE}📋 Configuring Codex MCP servers...${NC}"
    
    mkdir -p ~/.codex
    
    if [ -f ~/.codex/config.toml ]; then
        cp ~/.codex/config.toml ~/.codex/config.toml.backup
        # Remove existing MCP server configs
        sed -i '/# MCP Servers Configuration/,/^$/d' ~/.codex/config.toml 2>/dev/null || true
        sed -i '/\[mcp_servers/,/^$/d' ~/.codex/config.toml 2>/dev/null || true
    else
        touch ~/.codex/config.toml
    fi
    
    # Append MCP servers in TOML format
    echo "" >> ~/.codex/config.toml
    echo "# MCP Servers Configuration (auto-generated from central config)" >> ~/.codex/config.toml
    
    # Convert JSON to TOML format using jq
    jq -r '.servers | to_entries[] | 
        if .value.transport == "stdio" then
            "\n[mcp_servers.\(.key)]\n" +
            "command = \"\(.value.command)\"\n" +
            "args = \(.value.args | @json)\n" +
            (if .value.env_required then
                "env = { " + (.value.env_required | map("\(.) = \"$\(.)\"") | join(", ")) + " }\n"
            else "" end)
        elif .value.transport == "http" then
            "\n[mcp_servers.\(.key)]\n" +
            "# HTTP transport - Codex should handle this\n" +
            "url = \"\(.value.httpUrl)\"\n"
        else "" end
    ' "$CONFIG_FILE" | while IFS= read -r line; do
        # Replace environment variables
        line="${line//\$\{SUPABASE_PROJECT_REF\}/$SUPABASE_PROJECT_REF}"
        line="${line//\$\{SUPABASE_ACCESS_TOKEN\}/$SUPABASE_ACCESS_TOKEN}"
        line="${line//\$SUPABASE_PROJECT_REF/$SUPABASE_PROJECT_REF}"
        line="${line//\$SUPABASE_ACCESS_TOKEN/$SUPABASE_ACCESS_TOKEN}"
        echo "$line" >> ~/.codex/config.toml
    done
    
    echo -e "${GREEN}✅ Codex MCP servers configured${NC}"
}

# Function to sync to all agents
sync_all_agents() {
    echo "🔄 MCP Server Configuration Sync"
    echo "================================"
    
    check_dependencies
    
    # Check if central config exists
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}❌ Central MCP configuration not found at: $CONFIG_FILE${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}📖 Reading from central configuration: $CONFIG_FILE${NC}"
    
    # Load project environment if in a project directory
    load_project_env
    
    # Sync to each agent
    sync_gemini
    sync_qwen
    sync_codex
    
    echo -e "${GREEN}✅ All agents configured with MCP servers!${NC}"
    
    # Show which servers were configured
    echo ""
    echo "📋 Configured MCP Servers:"
    jq -r '.servers | keys[] | "  • \(.)"' "$CONFIG_FILE"
    
    if [ -n "$SUPABASE_PROJECT_REF" ]; then
        echo ""
        echo "🔧 Project-specific configuration applied:"
        echo "  • Supabase Project: $SUPABASE_PROJECT_REF"
    fi
}

# Function to add a new MCP server to central config
add_mcp_server() {
    local SERVER_NAME="$1"
    local SERVER_COMMAND="$2"
    shift 2
    local SERVER_ARGS="$@"
    
    echo -e "${BLUE}➕ Adding MCP server to central config: $SERVER_NAME${NC}"
    
    # Create args array in JSON format
    ARGS_JSON=$(printf '%s\n' $SERVER_ARGS | jq -R . | jq -s .)
    
    # Add to central config
    jq --arg name "$SERVER_NAME" \
       --arg cmd "$SERVER_COMMAND" \
       --argjson args "$ARGS_JSON" \
       '.servers[$name] = {
           "transport": "stdio",
           "command": $cmd,
           "args": $args
       }' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    
    echo -e "${GREEN}✅ Added $SERVER_NAME to central configuration${NC}"
    
    # Sync to all agents
    sync_all_agents
}

# Function to configure project-specific settings
configure_project() {
    local PROJECT_DIR="${1:-$(pwd)}"
    
    echo -e "${BLUE}🔧 Configuring project-specific MCP settings...${NC}"
    
    # Interactive prompts for configuration
    if [ -z "$SUPABASE_PROJECT_REF" ] || [ "$SUPABASE_PROJECT_REF" = "YOUR_PROJECT_REF" ]; then
        echo -e "${YELLOW}Enter Supabase project ref (or press Enter to skip):${NC}"
        read -r SUPABASE_REF_INPUT
        if [ -n "$SUPABASE_REF_INPUT" ]; then
            SUPABASE_PROJECT_REF="$SUPABASE_REF_INPUT"
        fi
    fi
    
    if [ -z "$SUPABASE_ACCESS_TOKEN" ] || [ "$SUPABASE_ACCESS_TOKEN" = "YOUR_ACCESS_TOKEN" ]; then
        echo -e "${YELLOW}Enter Supabase access token (or press Enter to skip):${NC}"
        read -rs SUPABASE_TOKEN_INPUT
        echo
        if [ -n "$SUPABASE_TOKEN_INPUT" ]; then
            SUPABASE_ACCESS_TOKEN="$SUPABASE_TOKEN_INPUT"
        fi
    fi
    
    # Create project .env.mcp file
    cat > "$PROJECT_DIR/.env.mcp" << EOF
# MCP Server Configuration for this project
# This file is sourced by sync-mcp-servers.sh
SUPABASE_PROJECT_REF="$SUPABASE_PROJECT_REF"
SUPABASE_ACCESS_TOKEN="$SUPABASE_ACCESS_TOKEN"
GITHUB_TOKEN="$GITHUB_TOKEN"
EOF
    
    echo -e "${GREEN}✅ Project MCP configuration saved to .env.mcp${NC}"
    echo -e "${YELLOW}⚠️  Add .env.mcp to .gitignore to keep secrets safe${NC}"
    
    # Re-sync with new values
    sync_all_agents
}

# Function to list configured servers
list_servers() {
    echo -e "${BLUE}📋 Central MCP Server Configuration:${NC}"
    echo ""
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}No central configuration found${NC}"
        exit 1
    fi
    
    jq -r '.servers | to_entries[] | 
        "• " + .key + ":\n" +
        "  Transport: " + .value.transport + "\n" +
        if .value.command then "  Command: " + .value.command + "\n" else "" end +
        if .value.httpUrl then "  URL: " + .value.httpUrl + "\n" else "" end +
        if .value.env_required then "  Required Env: " + (.value.env_required | join(", ")) + "\n" else "" end
    ' "$CONFIG_FILE"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  sync-all                    Sync MCP servers to all agents (default)"
    echo "  sync-gemini                 Sync to Gemini only"
    echo "  sync-qwen                   Sync to Qwen only"
    echo "  sync-codex                  Sync to Codex only"
    echo "  add <name> <cmd> [args]     Add a new MCP server to central config"
    echo "  configure [dir]             Configure project-specific settings"
    echo "  list                        List all configured MCP servers"
    echo "  help                        Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  SUPABASE_PROJECT_REF        Supabase project reference"
    echo "  SUPABASE_ACCESS_TOKEN       Supabase access token"
    echo "  GITHUB_TOKEN                GitHub personal access token"
    echo ""
    echo "Examples:"
    echo "  $0                          # Sync all agents"
    echo "  $0 add sqlite npx -y @modelcontextprotocol/server-sqlite database.db"
    echo "  $0 configure .              # Configure project-specific settings"
    echo "  SUPABASE_PROJECT_REF=myproject $0 sync-all"
}

# Main execution
case "${1:-sync-all}" in
    sync-all)
        sync_all_agents
        ;;
    sync-gemini)
        check_dependencies
        load_project_env
        sync_gemini
        ;;
    sync-qwen)
        check_dependencies
        load_project_env
        sync_qwen
        ;;
    sync-codex)
        check_dependencies
        load_project_env
        sync_codex
        ;;
    add)
        shift
        add_mcp_server "$@"
        ;;
    configure)
        configure_project "$2"
        ;;
    list)
        list_servers
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        echo "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac