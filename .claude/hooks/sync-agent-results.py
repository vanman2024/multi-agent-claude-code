#!/usr/bin/env python3
"""
Hook: Sync agent results after completion
Event: SubagentStop
Purpose: Capture and coordinate multi-agent workflow results
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def main():
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error parsing input: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Extract relevant information
    session_id = input_data.get("session_id", "")
    transcript_path = input_data.get("transcript_path", "")
    stop_hook_active = input_data.get("stop_hook_active", False)
    
    # Don't process if we're already in a stop hook loop
    if stop_hook_active:
        sys.exit(0)
    
    # Create results directory
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    results_dir = Path(project_dir) / ".claude" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Parse transcript to get agent results
    if transcript_path and os.path.exists(transcript_path):
        try:
            # Read last few lines of transcript for agent output
            with open(transcript_path, 'r') as f:
                lines = f.readlines()
                # Look for agent completion markers in last 50 lines
                recent_lines = lines[-50:] if len(lines) > 50 else lines
                
                # Save agent results
                result_file = results_dir / f"agent-result-{session_id[:8]}-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.txt"
                with open(result_file, 'w') as rf:
                    rf.writelines(recent_lines)
                
                print(f"✅ Agent results saved to: {result_file.relative_to(project_dir)}")
        except Exception as e:
            print(f"Warning: Could not parse transcript: {e}", file=sys.stderr)
    
    # Log completion
    log_dir = Path(project_dir) / ".claude" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    completion_log = log_dir / "agent-completions.jsonl"
    completion_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "session_id": session_id,
        "transcript_path": transcript_path
    }
    
    with open(completion_log, 'a') as f:
        f.write(json.dumps(completion_entry) + "\n")
    
    print("📊 Agent completion logged and results synced")
    
    # Success - allow continuation
    sys.exit(0)

if __name__ == "__main__":
    main()