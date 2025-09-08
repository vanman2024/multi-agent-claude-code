#!/usr/bin/env python3

"""
Todo Manager - Intelligent todo persistence system
Works around TodoWrite's deletion behavior by maintaining a proper persistent store
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib

class TodoManager:
    def __init__(self, project_path: str = None):
        self.project_path = project_path or os.getcwd()
        self.project_name = os.path.basename(self.project_path)
        self.project_hash = self.project_path.replace('/', '-')
        
        # Directories
        self.todo_dir = Path.home() / '.claude' / 'todos'
        self.project_dir = Path.home() / '.claude' / 'projects' / self.project_hash
        self.archive_dir = self.project_dir / 'todo-archive'
        
        # Files
        self.master_file = self.archive_dir / 'master-todos.json'
        self.state_file = self.archive_dir / 'todo-state.json'
        
        # Ensure directories exist
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize master file if needed
        if not self.master_file.exists():
            self.master_file.write_text('[]')
        
        # Load state
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """Load or initialize state tracking"""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            'last_session': None,
            'last_sync': None,
            'todo_hashes': {}
        }
    
    def _save_state(self):
        """Save state tracking"""
        self.state_file.write_text(json.dumps(self.state, indent=2))
    
    def _hash_todo(self, todo: Dict) -> str:
        """Generate unique hash for a todo based on content"""
        return hashlib.md5(todo.get('content', '').encode()).hexdigest()[:8]
    
    def get_current_session(self) -> Optional[Path]:
        """Find the current session file"""
        sessions = sorted(self.todo_dir.glob('*.json'), key=lambda p: p.stat().st_mtime, reverse=True)
        for session in sessions:
            # Check if this session belongs to our project
            session_id = session.stem
            session_reg = self.project_dir / f"{session_id}.jsonl"
            if session_reg.exists():
                return session
        return sessions[0] if sessions else None
    
    def sync_from_session(self):
        """Sync todos from current session to master file"""
        session_file = self.get_current_session()
        if not session_file:
            print("No session file found")
            return
        
        # Load session todos
        try:
            session_todos = json.loads(session_file.read_text())
        except:
            session_todos = []
        
        if not session_todos:
            print("Session has no todos")
            return
        
        # Load master todos
        master_todos = json.loads(self.master_file.read_text())
        
        # Create lookup map for existing todos
        master_map = {self._hash_todo(t): t for t in master_todos}
        
        # Process session todos
        updated = 0
        added = 0
        for todo in session_todos:
            todo_hash = self._hash_todo(todo)
            
            # Add metadata if missing
            if 'id' not in todo:
                todo['id'] = todo_hash
            if 'created_at' not in todo:
                todo['created_at'] = datetime.now().isoformat()
            if 'session_id' not in todo:
                todo['session_id'] = session_file.stem
            
            # Update or add
            if todo_hash in master_map:
                # Update existing todo (status might have changed)
                old_status = master_map[todo_hash].get('status')
                new_status = todo.get('status')
                if old_status != new_status:
                    master_map[todo_hash] = todo
                    todo['updated_at'] = datetime.now().isoformat()
                    updated += 1
            else:
                # New todo
                master_map[todo_hash] = todo
                added += 1
        
        # Save back to master
        master_todos = list(master_map.values())
        self.master_file.write_text(json.dumps(master_todos, indent=2))
        
        # Update state
        self.state['last_sync'] = datetime.now().isoformat()
        self.state['last_session'] = session_file.stem
        self._save_state()
        
        print(f"✅ Synced: {added} new, {updated} updated, {len(master_todos)} total")
    
    def restore_to_session(self, include_completed: bool = True):
        """Restore todos from master to current session"""
        session_file = self.get_current_session()
        if not session_file:
            print("No session file found")
            return
        
        # Check if session already has todos
        try:
            current_todos = json.loads(session_file.read_text())
            if len(current_todos) > 3:  # Has meaningful content
                print(f"Session already has {len(current_todos)} todos")
                return
        except:
            pass
        
        # Load master todos
        master_todos = json.loads(self.master_file.read_text())
        
        # Filter todos to restore
        todos_to_restore = []
        for todo in master_todos:
            # Always include pending and in_progress
            if todo.get('status') in ['pending', 'in_progress']:
                todos_to_restore.append(todo)
            # Include completed if requested (default is now True)
            elif include_completed and todo.get('status') == 'completed':
                # Include ALL completed todos, not just recent ones
                todos_to_restore.append(todo)
        
        # Add anchor todo to prevent deletion
        todos_to_restore.append({
            'content': '📌 [System] Keep todos persistent',
            'status': 'pending',
            'activeForm': 'Maintaining todo persistence',
            'id': 'anchor',
            'created_at': datetime.now().isoformat()
        })
        
        # Write to session
        session_file.write_text(json.dumps(todos_to_restore, indent=2))
        print(f"✅ Restored {len(todos_to_restore)} todos to session")
    
    def auto_manage(self):
        """Intelligently sync or restore based on current state"""
        session_file = self.get_current_session()
        if not session_file:
            print("No session file")
            return
        
        try:
            session_todos = json.loads(session_file.read_text())
            todo_count = len(session_todos)
        except:
            todo_count = 0
        
        if todo_count > 1:  # Has todos (more than just anchor)
            print(f"Session has {todo_count} todos - syncing to master")
            self.sync_from_session()
        else:
            print("Session empty - restoring from master")
            self.restore_to_session()
    
    def stats(self):
        """Show statistics"""
        master_todos = json.loads(self.master_file.read_text())
        
        stats = {
            'total': len(master_todos),
            'pending': sum(1 for t in master_todos if t.get('status') == 'pending'),
            'in_progress': sum(1 for t in master_todos if t.get('status') == 'in_progress'),
            'completed': sum(1 for t in master_todos if t.get('status') == 'completed')
        }
        
        print(f"""
📊 Todo Statistics for {self.project_name}
────────────────────────────────
Total:       {stats['total']}
Pending:     {stats['pending']}
In Progress: {stats['in_progress']}
Completed:   {stats['completed']}

Last sync: {self.state.get('last_sync', 'Never')}
Last session: {self.state.get('last_session', 'Unknown')}
        """)
        
        # Show recent todos
        if master_todos:
            print("\n📝 Recent todos:")
            for todo in master_todos[-5:]:
                status = todo.get('status', 'unknown')[0].upper()
                content = todo.get('content', '')[:60]
                print(f"  [{status}] {content}")
    
    def fix_empty_sessions(self):
        """Fix the issue where TodoWrite empties completed sessions"""
        # Find all empty session files
        empty_sessions = []
        for session_file in self.todo_dir.glob('*.json'):
            try:
                todos = json.loads(session_file.read_text())
                if not todos or todos == []:
                    empty_sessions.append(session_file)
            except:
                pass
        
        if empty_sessions:
            print(f"Found {len(empty_sessions)} empty session files")
            
            # Check if we have backups
            for session_file in empty_sessions:
                session_id = session_file.stem
                backup_pattern = self.archive_dir / 'completed-todos' / f"*{session_id}.json"
                backups = list(self.archive_dir.glob(f"completed-todos/*{session_id}.json"))
                
                if backups:
                    # Restore from most recent backup
                    latest_backup = max(backups, key=lambda p: p.stat().st_mtime)
                    print(f"Restoring {session_id} from backup")
                    session_file.write_text(latest_backup.read_text())


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Smart Todo Manager')
    parser.add_argument('command', choices=['sync', 'restore', 'auto', 'stats', 'fix'],
                       help='Command to run')
    parser.add_argument('--project', default=os.getcwd(),
                       help='Project path (default: current directory)')
    parser.add_argument('--include-completed', action='store_true',
                       help='Include completed todos when restoring')
    
    args = parser.parse_args()
    
    manager = TodoManager(args.project)
    
    if args.command == 'sync':
        manager.sync_from_session()
    elif args.command == 'restore':
        manager.restore_to_session(args.include_completed)
    elif args.command == 'auto':
        manager.auto_manage()
    elif args.command == 'stats':
        manager.stats()
    elif args.command == 'fix':
        manager.fix_empty_sessions()


if __name__ == '__main__':
    main()