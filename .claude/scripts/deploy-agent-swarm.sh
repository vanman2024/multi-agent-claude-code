#!/bin/bash
# Agent Swarm Deployment Script
#
# PURPOSE: Deploy parallel AI agent swarm with single command
# USAGE: ./deploy-agent-swarm.sh [target_directory] [feature_description]
# PART OF: Multi-Agent Claude Code Template - Parallel Agent Swarm Pattern v3.0
# CONNECTS TO: Gemini, Qwen, Codex CLIs with approval mode flags
#
# Deploys all agents simultaneously in background processes for true parallel execution

set -e

# Kill switch check first
if [ "$1" = "--kill" ]; then
    LOG_DIR="/tmp/agent-swarm-logs"
    echo -e "${RED}🛑 KILLING ALL AGENT PROCESSES${NC}"
    for pid_file in "$LOG_DIR"/*.pid; do
        if [ -f "$pid_file" ]; then
            pid=$(cat "$pid_file")
            agent=$(basename "$pid_file" .pid)
            echo -e "${YELLOW}Killing @${agent} (PID: $pid)${NC}"
            kill "$pid" 2>/dev/null || echo -e "${RED}Process $pid already terminated${NC}"
            rm "$pid_file"
        fi
    done
    echo -e "${GREEN}✅ All agents terminated${NC}"
    exit 0
fi

# Configuration
TARGET_DIR="${1:-$(pwd)}"
FEATURE_DESC="${2:-"Analyze and improve codebase"}"
LOG_DIR="/tmp/agent-swarm-logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create log directory
mkdir -p "$LOG_DIR"

echo -e "${BLUE}🚀 DEPLOYING PARALLEL AGENT SWARM${NC}"
echo -e "Target Directory: ${GREEN}$TARGET_DIR${NC}"
echo -e "Feature: ${GREEN}$FEATURE_DESC${NC}"
echo -e "Logs: ${GREEN}$LOG_DIR${NC}"
echo ""

# Validate target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}❌ Target directory does not exist: $TARGET_DIR${NC}"
    exit 1
fi

# Function to deploy agent in background
deploy_agent() {
    local agent_name="$1"
    local command="$2"
    local log_file="$LOG_DIR/${agent_name}.log"
    
    echo -e "${YELLOW}🤖 Deploying @${agent_name}...${NC}"
    
    # Change to target directory and run command in background
    (cd "$TARGET_DIR" && eval "$command" > "$log_file" 2>&1) &
    local pid=$!
    
    # Store PID for monitoring
    echo "$pid" > "$LOG_DIR/${agent_name}.pid"
    echo -e "${GREEN}✅ @${agent_name} deployed (PID: $pid)${NC}"
    
    return 0
}

# Deploy all agents simultaneously
echo -e "${BLUE}🔄 PARALLEL DEPLOYMENT PHASE${NC}"

# Gemini Analysis Engine
deploy_agent "gemini" "gemini -m gemini-2.0-flash-exp --approval-mode=auto_edit -p 'Analyze codebase structure and identify integration points for: $FEATURE_DESC. Focus on architecture, dependencies, and potential improvements.'"

# Qwen Optimization Engine  
deploy_agent "qwen" "qwen --approval-mode=auto_edit -p 'Review performance bottlenecks and optimization opportunities for: $FEATURE_DESC. Analyze algorithms, database queries, and resource usage.'"

# Codex Frontend Engine (if frontend directory exists)
if [ -d "$TARGET_DIR/src" ] || [ -d "$TARGET_DIR/frontend" ] || [ -d "$TARGET_DIR/app" ]; then
    deploy_agent "codex" "codex exec 'Analyze frontend components and suggest improvements for: $FEATURE_DESC. Focus on React patterns, state management, and user experience.'"
fi

echo ""
echo -e "${GREEN}🎯 ALL AGENTS DEPLOYED SUCCESSFULLY${NC}"
echo ""

# Monitor progress
echo -e "${BLUE}📊 MONITORING SWARM PROGRESS${NC}"
echo "Use these commands to monitor:"
echo ""
echo -e "${YELLOW}# Monitor all agent logs in real-time:${NC}"
echo "tail -f $LOG_DIR/*.log"
echo ""
echo -e "${YELLOW}# Check specific agent:${NC}"
echo "tail -f $LOG_DIR/gemini.log"
echo "tail -f $LOG_DIR/qwen.log" 
echo "tail -f $LOG_DIR/codex.log"
echo ""
echo -e "${YELLOW}# Check agent status:${NC}"
echo "ps aux | grep -E '(gemini|qwen|codex)'"
echo ""
echo -e "${YELLOW}# Kill all agents if needed:${NC}"
echo "$0 --kill"
echo ""


# Show initial logs
echo -e "${BLUE}📝 INITIAL OUTPUT PREVIEW${NC}"
sleep 2
for log_file in "$LOG_DIR"/*.log; do
    if [ -f "$log_file" ]; then
        agent=$(basename "$log_file" .log)
        echo -e "${YELLOW}--- @${agent} ---${NC}"
        head -10 "$log_file" 2>/dev/null || echo "No output yet..."
        echo ""
    fi
done

echo -e "${GREEN}🎉 SWARM DEPLOYMENT COMPLETE!${NC}"
echo -e "${BLUE}All agents are working in parallel on: ${FEATURE_DESC}${NC}"