#!/usr/bin/env python3
"""
💬 CHAT & AGENT HISTORY DATABASE
===============================
Comprehensive database system that records all chat interactions and agent actions.
Provides complete audit trail of conversations, tool usage, and development history.

FEATURES:
✅ Complete chat conversation logging
✅ Agent tool usage tracking
✅ Code changes and file operations
✅ Terminal commands and outputs
✅ Error tracking and debugging info
✅ Session management and timeline
✅ Search and analysis capabilities
"""

import sqlite3
import json
import time
import os
import sys
import hashlib
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import atexit

class ChatAgentHistoryDB:
    """Comprehensive chat and agent history database"""
    
    def __init__(self, db_file: str = "chat_agent_history.db"):
        self.db_file = db_file
        self.session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.getpid()}"
        self.conversation_id = None
        self.lock = threading.Lock()
        
        # Initialize database
        self.init_database()
        
        # Start session
        self.start_session()
        
        # Register cleanup
        atexit.register(self.cleanup)
        
        print(f"💬 Chat & Agent History DB Started")
        print(f"🗄️ Database: {self.db_file}")
        print(f"🔗 Session: {self.session_id}")
    
    def init_database(self):
        """Initialize comprehensive chat and agent history database"""
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        
        with self.lock:
            cursor = self.conn.cursor()
            
            # Sessions table - track each chat session
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ended_at DATETIME,
                    workspace_path TEXT,
                    python_version TEXT,
                    os_info TEXT,
                    total_messages INTEGER DEFAULT 0,
                    total_tool_calls INTEGER DEFAULT 0,
                    total_file_operations INTEGER DEFAULT 0,
                    total_terminal_commands INTEGER DEFAULT 0,
                    total_errors INTEGER DEFAULT 0,
                    session_status TEXT DEFAULT 'ACTIVE'
                )
            ''')
            
            # Conversations table - group related interactions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    conversation_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ended_at DATETIME,
                    topic TEXT,
                    summary TEXT,
                    total_exchanges INTEGER DEFAULT 0,
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
            ''')
            
            # Chat messages - all user and agent messages
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    message_type TEXT NOT NULL,  -- 'USER', 'AGENT', 'SYSTEM'
                    role TEXT,  -- 'user', 'assistant', 'system'
                    content TEXT NOT NULL,
                    content_hash TEXT,
                    message_length INTEGER,
                    attachments TEXT,  -- JSON array of attachments
                    context_info TEXT,  -- JSON with additional context
                    response_time_ms INTEGER,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id),
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
            ''')
            
            # Agent tool calls - track all tool usage
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_tool_calls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    session_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    tool_name TEXT NOT NULL,
                    tool_description TEXT,
                    parameters TEXT,  -- JSON parameters
                    result TEXT,  -- Tool execution result
                    success BOOLEAN,
                    execution_time_ms INTEGER,
                    error_message TEXT,
                    file_paths TEXT,  -- JSON array of affected files
                    FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id),
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
            ''')
            
            # File operations - detailed file change tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS file_operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    conversation_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    operation_type TEXT NOT NULL,  -- 'CREATE', 'EDIT', 'DELETE', 'READ'
                    file_path TEXT NOT NULL,
                    tool_used TEXT,
                    old_content_hash TEXT,
                    new_content_hash TEXT,
                    lines_added INTEGER,
                    lines_removed INTEGER,
                    lines_modified INTEGER,
                    file_size_before INTEGER,
                    file_size_after INTEGER,
                    change_summary TEXT,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id),
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
            ''')
            
            # Terminal commands - all terminal activity
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS terminal_commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    conversation_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    command TEXT NOT NULL,
                    explanation TEXT,
                    working_directory TEXT,
                    is_background BOOLEAN,
                    exit_code INTEGER,
                    execution_time_ms INTEGER,
                    output TEXT,
                    error_output TEXT,
                    terminal_id TEXT,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id),
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
            ''')
            
            # Code changes - track specific code modifications
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS code_changes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    conversation_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    file_path TEXT NOT NULL,
                    change_type TEXT,  -- 'FUNCTION_ADD', 'CLASS_ADD', 'IMPORT_ADD', 'REFACTOR', etc.
                    old_code TEXT,
                    new_code TEXT,
                    line_start INTEGER,
                    line_end INTEGER,
                    description TEXT,
                    purpose TEXT,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id),
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
            ''')
            
            # Error tracking - comprehensive error logging
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS error_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    conversation_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    error_type TEXT NOT NULL,
                    error_category TEXT,  -- 'TOOL_ERROR', 'CODE_ERROR', 'SYSTEM_ERROR', etc.
                    error_message TEXT NOT NULL,
                    stack_trace TEXT,
                    context_info TEXT,  -- JSON with error context
                    resolution TEXT,
                    severity TEXT DEFAULT 'ERROR',  -- 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
                    FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id),
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
            ''')
            
            # Agent decisions - track reasoning and decision making
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_decisions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    conversation_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    decision_type TEXT,  -- 'TOOL_SELECTION', 'APPROACH', 'STRATEGY', etc.
                    context TEXT,
                    reasoning TEXT,
                    chosen_action TEXT,
                    alternatives_considered TEXT,  -- JSON array
                    outcome TEXT,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id),
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
            ''')
            
            # Workspace snapshots - periodic state captures
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workspace_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    total_files INTEGER,
                    total_lines_code INTEGER,
                    file_list TEXT,  -- JSON array of files
                    git_status TEXT,
                    active_processes TEXT,  -- JSON array
                    memory_usage_mb REAL,
                    disk_usage_mb REAL,
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
            ''')
            
            self.conn.commit()
            print("✅ Chat & Agent History database initialized")
    
    def start_session(self):
        """Start a new session"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO sessions (
                    session_id, workspace_path, python_version, os_info
                ) VALUES (?, ?, ?, ?)
            ''', (
                self.session_id,
                os.getcwd(),
                sys.version,
                f"{os.name} {os.uname().sysname} {os.uname().release}"
            ))
            self.conn.commit()
    
    def start_conversation(self, topic: Optional[str] = None) -> str:
        """Start a new conversation within the session"""
        self.conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]}"
        
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO conversations (
                    conversation_id, session_id, topic
                ) VALUES (?, ?, ?)
            ''', (self.conversation_id, self.session_id, topic))
            self.conn.commit()
        
        print(f"🗨️ Started conversation: {self.conversation_id}")
        return self.conversation_id
    
    def log_chat_message(self, message_type: str, role: str, content: str,
                        attachments: Optional[List[str]] = None, context_info: Optional[Dict] = None,
                        response_time_ms: Optional[int] = None):
        """Log a chat message"""
        if not self.conversation_id:
            self.start_conversation("General Chat")
        
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO chat_messages (
                    conversation_id, session_id, message_type, role, content,
                    content_hash, message_length, attachments, context_info, response_time_ms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.conversation_id, self.session_id, message_type, role, content,
                content_hash, len(content),
                json.dumps(attachments) if attachments else None,
                json.dumps(context_info) if context_info else None,
                response_time_ms
            ))
            
            # Update session and conversation counters
            cursor.execute('''
                UPDATE sessions SET total_messages = total_messages + 1
                WHERE session_id = ?
            ''', (self.session_id,))
            
            cursor.execute('''
                UPDATE conversations SET total_exchanges = total_exchanges + 1
                WHERE conversation_id = ?
            ''', (self.conversation_id,))
            
            self.conn.commit()
        
        print(f"💬 Logged {message_type} message ({len(content)} chars)")
    
    def log_tool_call(self, tool_name: str, tool_description: Optional[str] = None,
                     parameters: Optional[Dict] = None, result: Optional[str] = None,
                     success: bool = True, execution_time_ms: Optional[int] = None,
                     error_message: Optional[str] = None, file_paths: Optional[List[str]] = None):
        """Log an agent tool call"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO agent_tool_calls (
                    conversation_id, session_id, tool_name, tool_description,
                    parameters, result, success, execution_time_ms,
                    error_message, file_paths
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.conversation_id, self.session_id, tool_name, tool_description,
                json.dumps(parameters) if parameters else None,
                json.dumps(result) if result else None, success, execution_time_ms, error_message,
                json.dumps(file_paths) if file_paths else None
            ))
            
            # Update session counter
            cursor.execute('''
                UPDATE sessions SET total_tool_calls = total_tool_calls + 1
                WHERE session_id = ?
            ''', (self.session_id,))
            
            self.conn.commit()
        
        status = "✅" if success else "❌"
        print(f"🔧 {status} Tool call: {tool_name}")
    
    def log_file_operation(self, operation_type: str, file_path: str,
                          tool_used: Optional[str] = None, old_content_hash: Optional[str] = None,
                          new_content_hash: Optional[str] = None, change_summary: Optional[str] = None,
                          lines_added: Optional[int] = None, lines_removed: Optional[int] = None):
        """Log a file operation"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO file_operations (
                    session_id, conversation_id, operation_type, file_path,
                    tool_used, old_content_hash, new_content_hash,
                    lines_added, lines_removed, change_summary
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.session_id, self.conversation_id, operation_type, file_path,
                tool_used, old_content_hash, new_content_hash,
                lines_added, lines_removed, change_summary
            ))
            
            # Update session counter
            cursor.execute('''
                UPDATE sessions SET total_file_operations = total_file_operations + 1
                WHERE session_id = ?
            ''', (self.session_id,))
            
            self.conn.commit()
        
        print(f"📄 File {operation_type}: {os.path.basename(file_path)}")
    
    def log_terminal_command(self, command: str, explanation: Optional[str] = None,
                           working_directory: Optional[str] = None, is_background: bool = False,
                           exit_code: Optional[int] = None, output: Optional[str] = None,
                           error_output: Optional[str] = None, terminal_id: Optional[str] = None,
                           execution_time_ms: Optional[int] = None):
        """Log a terminal command"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO terminal_commands (
                    session_id, conversation_id, command, explanation,
                    working_directory, is_background, exit_code,
                    execution_time_ms, output, error_output, terminal_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.session_id, self.conversation_id, command, explanation,
                working_directory, is_background, exit_code,
                execution_time_ms, output, error_output, terminal_id
            ))
            
            # Update session counter
            cursor.execute('''
                UPDATE sessions SET total_terminal_commands = total_terminal_commands + 1
                WHERE session_id = ?
            ''', (self.session_id,))
            
            self.conn.commit()
        
        print(f"💻 Terminal: {command[:50]}{'...' if len(command) > 50 else ''}")
    
    def log_code_change(self, file_path: str, change_type: str,
                       old_code: Optional[str] = None, new_code: Optional[str] = None,
                       line_start: Optional[int] = None, line_end: Optional[int] = None,
                       description: Optional[str] = None, purpose: Optional[str] = None):
        """Log a specific code change"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO code_changes (
                    session_id, conversation_id, file_path, change_type,
                    old_code, new_code, line_start, line_end,
                    description, purpose
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.session_id, self.conversation_id, file_path, change_type,
                old_code, new_code, line_start, line_end,
                description, purpose
            ))
            self.conn.commit()
        
        print(f"🔄 Code change: {change_type} in {os.path.basename(file_path)}")
    
    def log_error(self, error_type: str, error_message: str,
                 error_category: str = "GENERAL", stack_trace: Optional[str] = None,
                 context_info: Optional[Dict] = None, resolution: Optional[str] = None,
                 severity: str = "ERROR"):
        """Log an error"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO error_log (
                    session_id, conversation_id, error_type, error_category,
                    error_message, stack_trace, context_info, resolution, severity
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.session_id, self.conversation_id, error_type, error_category,
                error_message, stack_trace,
                json.dumps(context_info) if context_info else None,
                resolution, severity
            ))
            
            # Update session counter
            cursor.execute('''
                UPDATE sessions SET total_errors = total_errors + 1
                WHERE session_id = ?
            ''', (self.session_id,))
            
            self.conn.commit()
        
        print(f"❌ Error logged: {error_type}")
    
    def log_agent_decision(self, decision_type: str, context: str,
                          reasoning: str, chosen_action: str,
                          alternatives_considered: Optional[List[str]] = None,
                          outcome: Optional[str] = None):
        """Log an agent decision"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO agent_decisions (
                    session_id, conversation_id, decision_type, context,
                    reasoning, chosen_action, alternatives_considered, outcome
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.session_id, self.conversation_id, decision_type, context,
                reasoning, chosen_action,
                json.dumps(alternatives_considered) if alternatives_considered else None,
                outcome
            ))
            self.conn.commit()
        
        print(f"🤔 Agent decision: {decision_type}")
    
    def capture_workspace_snapshot(self):
        """Capture current workspace state"""
        try:
            # Count files and lines
            total_files = 0
            total_lines = 0
            file_list = []
            
            for root, dirs, files in os.walk('.'):
                dirs[:] = [d for d in dirs if not d.startswith('.') and 
                          d not in ['__pycache__', 'node_modules', '.venv', 'venv']]
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r') as f:
                                lines = len(f.readlines())
                                total_files += 1
                                total_lines += lines
                                file_list.append({
                                    'path': file_path,
                                    'lines': lines,
                                    'size': os.path.getsize(file_path)
                                })
                        except:
                            pass
            
            # Memory usage
            try:
                import psutil
                process = psutil.Process()
                memory_mb = process.memory_info().rss / 1024 / 1024
            except:
                memory_mb = None
            
            # Disk usage
            try:
                disk_usage = sum(f['size'] for f in file_list) / 1024 / 1024
            except:
                disk_usage = None
            
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO workspace_snapshots (
                        session_id, total_files, total_lines_code,
                        file_list, memory_usage_mb, disk_usage_mb
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    self.session_id, total_files, total_lines,
                    json.dumps(file_list), memory_mb, disk_usage
                ))
                self.conn.commit()
            
            print(f"📸 Workspace snapshot: {total_files} files, {total_lines} lines")
            
        except Exception as e:
            self.log_error("SNAPSHOT_ERROR", str(e), "SYSTEM")
    
    def get_session_summary(self) -> Dict:
        """Get comprehensive session summary"""
        with self.lock:
            cursor = self.conn.cursor()
            
            # Session info
            cursor.execute('SELECT * FROM sessions WHERE session_id = ?', (self.session_id,))
            session = cursor.fetchone()
            
            # Recent messages
            cursor.execute('''
                SELECT timestamp, message_type, role, content 
                FROM chat_messages WHERE session_id = ? 
                ORDER BY timestamp DESC LIMIT 10
            ''', (self.session_id,))
            recent_messages = cursor.fetchall()
            
            # Tool usage
            cursor.execute('''
                SELECT tool_name, COUNT(*) as count, 
                       SUM(CASE WHEN success THEN 1 ELSE 0 END) as success_count
                FROM agent_tool_calls WHERE session_id = ? 
                GROUP BY tool_name ORDER BY count DESC
            ''', (self.session_id,))
            tool_usage = cursor.fetchall()
            
            # File operations
            cursor.execute('''
                SELECT operation_type, COUNT(*) as count 
                FROM file_operations WHERE session_id = ? 
                GROUP BY operation_type
            ''', (self.session_id,))
            file_ops = cursor.fetchall()
            
            # Errors
            cursor.execute('''
                SELECT error_type, error_category, COUNT(*) as count 
                FROM error_log WHERE session_id = ? 
                GROUP BY error_type, error_category
            ''', (self.session_id,))
            errors = cursor.fetchall()
            
            return {
                "session": session,
                "recent_messages": recent_messages,
                "tool_usage": tool_usage,
                "file_operations": file_ops,
                "errors": errors
            }
    
    def search_history(self, query: str, limit: int = 20) -> List[Dict]:
        """Search through chat and agent history"""
        with self.lock:
            cursor = self.conn.cursor()
            
            results = []
            
            # Search chat messages
            cursor.execute('''
                SELECT 'CHAT_MESSAGE' as type, timestamp, message_type, content
                FROM chat_messages 
                WHERE content LIKE ? 
                ORDER BY timestamp DESC LIMIT ?
            ''', (f'%{query}%', limit//2))
            
            for row in cursor.fetchall():
                results.append({
                    'type': row[0],
                    'timestamp': row[1],
                    'message_type': row[2],
                    'content': row[3][:200] + '...' if len(row[3]) > 200 else row[3]
                })
            
            # Search tool calls
            cursor.execute('''
                SELECT 'TOOL_CALL' as type, timestamp, tool_name, result
                FROM agent_tool_calls 
                WHERE tool_name LIKE ? OR result LIKE ?
                ORDER BY timestamp DESC LIMIT ?
            ''', (f'%{query}%', f'%{query}%', limit//2))
            
            for row in cursor.fetchall():
                results.append({
                    'type': row[0],
                    'timestamp': row[1],
                    'tool_name': row[2],
                    'result': row[3][:200] + '...' if row[3] and len(row[3]) > 200 else row[3]
                })
            
            return sorted(results, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def cleanup(self):
        """Clean up and finalize session"""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    UPDATE sessions SET 
                        ended_at = CURRENT_TIMESTAMP,
                        session_status = 'COMPLETED'
                    WHERE session_id = ?
                ''', (self.session_id,))
                self.conn.commit()
            
            # Print summary
            summary = self.get_session_summary()
            
            print("\n" + "="*80)
            print("💬 CHAT & AGENT HISTORY SESSION SUMMARY")
            print("="*80)
            print(f"Session: {self.session_id}")
            print(f"Tool Usage: {dict((t[0], t[1]) for t in summary['tool_usage'])}")
            print(f"File Operations: {dict((f[0], f[1]) for f in summary['file_operations'])}")
            print(f"Errors: {len(summary['errors'])}")
            print("="*80)
            
            self.conn.close()
            
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")

# Global instance
_chat_agent_db = None

def get_chat_agent_db() -> ChatAgentHistoryDB:
    """Get or create chat agent history database"""
    global _chat_agent_db
    if _chat_agent_db is None:
        _chat_agent_db = ChatAgentHistoryDB()
    return _chat_agent_db

def log_user_message(content: str, attachments: Optional[List[str]] = None, context: Optional[Dict] = None):
    """Log a user message"""
    db = get_chat_agent_db()
    db.log_chat_message("USER", "user", content, attachments, context)

def log_agent_message(content: str, response_time_ms: Optional[int] = None):
    """Log an agent message"""
    db = get_chat_agent_db()
    db.log_chat_message("AGENT", "assistant", content, response_time_ms=response_time_ms)

def log_tool_usage(tool_name: str, parameters: Optional[Dict] = None, result: Optional[str] = None, 
                  success: bool = True, error: Optional[str] = None, files: Optional[List[str]] = None):
    """Log tool usage"""
    db = get_chat_agent_db()
    db.log_tool_call(tool_name, parameters=parameters, result=result, 
                     success=success, error_message=error, file_paths=files)

def log_file_change(operation: str, file_path: str, tool: Optional[str] = None, summary: Optional[str] = None):
    """Log file change"""
    db = get_chat_agent_db()
    db.log_file_operation(operation, file_path, tool_used=tool, change_summary=summary)

def log_terminal_activity(command: str, explanation: Optional[str] = None, output: Optional[str] = None, 
                         exit_code: Optional[int] = None):
    """Log terminal activity"""
    db = get_chat_agent_db()
    db.log_terminal_command(command, explanation, output=output, exit_code=exit_code)

if __name__ == "__main__":
    # Test the system
    print("🧪 TESTING CHAT & AGENT HISTORY DATABASE")
    print("="*50)
    
    db = ChatAgentHistoryDB()
    
    # Test logging
    db.start_conversation("Testing Chat History Database")
    db.log_chat_message("USER", "user", "Test user message")
    db.log_chat_message("AGENT", "assistant", "Test agent response")
    db.log_tool_call("test_tool", parameters={"test": "value"}, result="Success", success=True)
    db.log_file_operation("CREATE", "test_file.py", "create_file", change_summary="Created test file")
    db.log_terminal_command("echo 'test'", "Testing echo command", output="test")
    
    # Test search
    results = db.search_history("test")
    print(f"Search results: {len(results)}")
    
    # Capture snapshot
    db.capture_workspace_snapshot()
    
    print("✅ Chat & Agent History Database test completed")
