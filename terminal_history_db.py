#!/usr/bin/env python3
"""
💻 TERMINAL HISTORY DATABASE
===========================
Comprehensive database system that records all terminal activity:
- Complete command history with timestamps
- Full input/output capture including errors
- Environment context and working directories
- Process information and execution times
- Exit codes and signal handling
- Verbose error logging and debugging info
- Session management and search capabilities

FEATURES:
✅ Complete terminal session recording
✅ Command input/output with full context
✅ Error capture with stack traces
✅ Process monitoring and resource usage
✅ Environment variable tracking
✅ Working directory changes
✅ Command completion and success rates
✅ Search and analysis tools
"""

import sqlite3
import json
import time
import os
import sys
import threading
import subprocess
import signal
import psutil
import shlex
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import atexit

class TerminalHistoryDB:
    """Comprehensive terminal history and activity database"""
    
    def __init__(self, db_file: str = "terminal_history.db", verbose: bool = True):
        self.db_file = db_file
        self.verbose = verbose
        self.session_id = f"term_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.getpid()}"
        self.lock = threading.Lock()
        self.active_commands = {}  # Track running commands
        
        # Initialize database
        self.init_database()
        
        # Start session
        self.start_session()
        
        # Register cleanup
        atexit.register(self.cleanup)
        
        print(f"💻 Terminal History DB Started")
        print(f"🗄️ Database: {self.db_file}")
        print(f"🔗 Session: {self.session_id}")
        print(f"🔍 Verbose mode: {'ON' if verbose else 'OFF'}")
    
    def init_database(self):
        """Initialize comprehensive terminal history database"""
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        
        with self.lock:
            cursor = self.conn.cursor()
            
            # Terminal sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS terminal_sessions (
                    session_id TEXT PRIMARY KEY,
                    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ended_at DATETIME,
                    shell_type TEXT,
                    shell_version TEXT,
                    user_name TEXT,
                    hostname TEXT,
                    initial_working_dir TEXT,
                    environment_vars TEXT,  -- JSON of key environment variables
                    total_commands INTEGER DEFAULT 0,
                    successful_commands INTEGER DEFAULT 0,
                    failed_commands INTEGER DEFAULT 0,
                    total_execution_time_ms INTEGER DEFAULT 0,
                    session_status TEXT DEFAULT 'ACTIVE'
                )
            ''')
            
            # Command executions table - main terminal activity
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS command_executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    command_id TEXT UNIQUE,  -- Unique ID for each command
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    working_directory TEXT NOT NULL,
                    command_line TEXT NOT NULL,
                    command_args TEXT,  -- JSON array of parsed arguments
                    environment_vars TEXT,  -- JSON of environment at execution time
                    process_id INTEGER,
                    parent_process_id INTEGER,
                    user_id INTEGER,
                    group_id INTEGER,
                    is_background BOOLEAN DEFAULT FALSE,
                    started_at DATETIME,
                    completed_at DATETIME,
                    execution_time_ms INTEGER,
                    exit_code INTEGER,
                    signal_received INTEGER,
                    memory_peak_mb REAL,
                    cpu_time_ms INTEGER,
                    FOREIGN KEY (session_id) REFERENCES terminal_sessions (session_id)
                )
            ''')
            
            # Command outputs table - capture all stdout/stderr
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS command_outputs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    output_type TEXT NOT NULL,  -- 'STDOUT', 'STDERR', 'STDIN'
                    sequence_number INTEGER,  -- Order of output chunks
                    content TEXT NOT NULL,
                    content_length INTEGER,
                    is_binary BOOLEAN DEFAULT FALSE,
                    encoding TEXT DEFAULT 'utf-8',
                    FOREIGN KEY (command_id) REFERENCES command_executions (command_id),
                    FOREIGN KEY (session_id) REFERENCES terminal_sessions (session_id)
                )
            ''')
            
            # Terminal errors table - detailed error information
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS terminal_errors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command_id TEXT,
                    session_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    error_type TEXT NOT NULL,  -- 'COMMAND_NOT_FOUND', 'PERMISSION_DENIED', 'SYNTAX_ERROR', etc.
                    error_category TEXT,  -- 'SYSTEM', 'USER', 'NETWORK', 'PERMISSION'
                    error_message TEXT NOT NULL,
                    error_code INTEGER,
                    stack_trace TEXT,
                    context_info TEXT,  -- JSON with additional error context
                    resolution_attempted TEXT,
                    resolution_successful BOOLEAN,
                    severity TEXT DEFAULT 'ERROR',  -- 'WARNING', 'ERROR', 'CRITICAL'
                    FOREIGN KEY (command_id) REFERENCES command_executions (command_id),
                    FOREIGN KEY (session_id) REFERENCES terminal_sessions (session_id)
                )
            ''')
            
            # Directory changes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS directory_changes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    command_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    old_directory TEXT,
                    new_directory TEXT,
                    change_method TEXT,  -- 'cd', 'pushd', 'popd', 'auto'
                    success BOOLEAN,
                    FOREIGN KEY (command_id) REFERENCES command_executions (command_id),
                    FOREIGN KEY (session_id) REFERENCES terminal_sessions (session_id)
                )
            ''')
            
            # Environment changes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS environment_changes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    command_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    variable_name TEXT NOT NULL,
                    old_value TEXT,
                    new_value TEXT,
                    change_type TEXT,  -- 'SET', 'UNSET', 'MODIFY', 'EXPORT'
                    scope TEXT DEFAULT 'SESSION',  -- 'SESSION', 'GLOBAL', 'LOCAL'
                    FOREIGN KEY (command_id) REFERENCES command_executions (command_id),
                    FOREIGN KEY (session_id) REFERENCES terminal_sessions (session_id)
                )
            ''')
            
            # Process monitoring table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS process_monitoring (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    process_id INTEGER NOT NULL,
                    cpu_percent REAL,
                    memory_mb REAL,
                    memory_percent REAL,
                    open_files INTEGER,
                    network_connections INTEGER,
                    status TEXT,
                    threads INTEGER,
                    FOREIGN KEY (command_id) REFERENCES command_executions (command_id),
                    FOREIGN KEY (session_id) REFERENCES terminal_sessions (session_id)
                )
            ''')
            
            # File operations table - track file system operations
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS file_operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command_id TEXT,
                    session_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    operation_type TEXT NOT NULL,  -- 'CREATE', 'DELETE', 'MODIFY', 'MOVE', 'COPY'
                    file_path TEXT NOT NULL,
                    old_path TEXT,  -- For move/rename operations
                    file_size INTEGER,
                    file_permissions TEXT,
                    file_owner TEXT,
                    detected_by TEXT,  -- 'COMMAND_ANALYSIS', 'FS_MONITOR', 'EXPLICIT'
                    FOREIGN KEY (command_id) REFERENCES command_executions (command_id),
                    FOREIGN KEY (session_id) REFERENCES terminal_sessions (session_id)
                )
            ''')
            
            # Command patterns table - for analysis and suggestions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS command_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    command_pattern TEXT NOT NULL,
                    usage_count INTEGER DEFAULT 1,
                    success_rate REAL,
                    average_execution_time_ms REAL,
                    common_errors TEXT,  -- JSON array of common errors
                    suggestions TEXT,  -- JSON array of improvement suggestions
                    last_used DATETIME,
                    FOREIGN KEY (session_id) REFERENCES terminal_sessions (session_id)
                )
            ''')
            
            self.conn.commit()
            print("✅ Terminal History database initialized")
    
    def start_session(self):
        """Start a new terminal session"""
        try:
            # Get shell information
            shell_type = os.environ.get('SHELL', 'unknown').split('/')[-1]
            shell_version = self._get_shell_version(shell_type)
            
            # Get user and system info
            user_name = os.environ.get('USER', 'unknown')
            hostname = os.uname().nodename
            
            # Get environment variables (important ones)
            important_env_vars = {
                'PATH': os.environ.get('PATH', ''),
                'HOME': os.environ.get('HOME', ''),
                'PWD': os.environ.get('PWD', ''),
                'SHELL': os.environ.get('SHELL', ''),
                'TERM': os.environ.get('TERM', ''),
                'LANG': os.environ.get('LANG', ''),
                'USER': os.environ.get('USER', ''),
                'PYTHONPATH': os.environ.get('PYTHONPATH', ''),
                'VIRTUAL_ENV': os.environ.get('VIRTUAL_ENV', '')
            }
            
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO terminal_sessions (
                        session_id, shell_type, shell_version, user_name, 
                        hostname, initial_working_dir, environment_vars
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    self.session_id, shell_type, shell_version, user_name,
                    hostname, os.getcwd(), json.dumps(important_env_vars)
                ))
                self.conn.commit()
                
        except Exception as e:
            print(f"⚠️ Session start warning: {e}")
    
    def _get_shell_version(self, shell_type: str) -> str:
        """Get shell version information"""
        try:
            if shell_type in ['bash', 'zsh', 'fish']:
                result = subprocess.run([shell_type, '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return result.stdout.split('\n')[0][:100]  # First line, truncated
        except:
            pass
        return 'unknown'
    
    def log_command_start(self, command: str, working_dir: Optional[str] = None,
                         is_background: bool = False, process_id: Optional[int] = None) -> str:
        """Log the start of a command execution"""
        command_id = f"cmd_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]}_{os.getpid()}"
        working_dir = working_dir or os.getcwd()
        
        try:
            # Parse command arguments
            try:
                command_args = shlex.split(command)
            except:
                command_args = command.split()
            
            # Get current environment (subset)
            current_env = {}
            for key in ['PATH', 'PWD', 'VIRTUAL_ENV', 'PYTHONPATH']:
                if key in os.environ:
                    current_env[key] = os.environ[key]
            
            # Get process info if available
            parent_pid = os.getppid() if hasattr(os, 'getppid') else None
            user_id = os.getuid() if hasattr(os, 'getuid') else None
            group_id = os.getgid() if hasattr(os, 'getgid') else None
            
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO command_executions (
                        command_id, session_id, working_directory, command_line,
                        command_args, environment_vars, process_id, parent_process_id,
                        user_id, group_id, is_background, started_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    command_id, self.session_id, working_dir, command,
                    json.dumps(command_args), json.dumps(current_env),
                    process_id, parent_pid, user_id, group_id, is_background,
                    datetime.now()
                ))
                
                # Update session counters
                cursor.execute('''
                    UPDATE terminal_sessions SET total_commands = total_commands + 1
                    WHERE session_id = ?
                ''', (self.session_id,))
                
                self.conn.commit()
            
            # Track active command
            self.active_commands[command_id] = {
                'command': command,
                'start_time': time.time(),
                'process_id': process_id
            }
            
            if self.verbose:
                print(f"🚀 Command started: {command_id}")
                print(f"   Command: {command}")
                print(f"   Working dir: {working_dir}")
                print(f"   Background: {is_background}")
            
            return command_id
            
        except Exception as e:
            print(f"❌ Error logging command start: {e}")
            return command_id
    
    def log_command_output(self, command_id: str, output_type: str, content: str,
                          sequence_number: int = 0):
        """Log command output (stdout/stderr)"""
        try:
            # Check if content is binary
            is_binary = False
            encoding = 'utf-8'
            try:
                content.encode('utf-8')
            except UnicodeEncodeError:
                is_binary = True
                encoding = 'binary'
                # Convert binary to hex representation for storage
                content = content.encode('unicode_escape').decode('ascii')
            
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO command_outputs (
                        command_id, session_id, output_type, sequence_number,
                        content, content_length, is_binary, encoding
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    command_id, self.session_id, output_type, sequence_number,
                    content, len(content), is_binary, encoding
                ))
                self.conn.commit()
            
            if self.verbose and output_type == 'STDERR':
                print(f"⚠️ Command error output: {command_id}")
                print(f"   Content: {content[:200]}{'...' if len(content) > 200 else ''}")
                
        except Exception as e:
            print(f"❌ Error logging command output: {e}")
    
    def log_command_completion(self, command_id: str, exit_code: Optional[int] = None,
                             signal_received: Optional[int] = None, error_message: Optional[str] = None):
        """Log command completion"""
        try:
            completion_time = datetime.now()
            execution_time_ms = None
            memory_peak = None
            cpu_time = None
            
            # Calculate execution time
            if command_id in self.active_commands:
                start_time = self.active_commands[command_id]['start_time']
                execution_time_ms = int((time.time() - start_time) * 1000)
                process_id = self.active_commands[command_id].get('process_id')
                
                # Get process info if available
                if process_id:
                    try:
                        process = psutil.Process(process_id)
                        memory_info = process.memory_info()
                        memory_peak = memory_info.rss / 1024 / 1024  # MB
                        cpu_times = process.cpu_times()
                        cpu_time = int((cpu_times.user + cpu_times.system) * 1000)  # ms
                    except:
                        pass
                
                del self.active_commands[command_id]
            
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    UPDATE command_executions SET
                        completed_at = ?, execution_time_ms = ?, exit_code = ?,
                        signal_received = ?, memory_peak_mb = ?, cpu_time_ms = ?
                    WHERE command_id = ?
                ''', (
                    completion_time, execution_time_ms, exit_code,
                    signal_received, memory_peak, cpu_time, command_id
                ))
                
                # Update session counters
                if exit_code == 0:
                    cursor.execute('''
                        UPDATE terminal_sessions SET successful_commands = successful_commands + 1,
                               total_execution_time_ms = total_execution_time_ms + ?
                        WHERE session_id = ?
                    ''', (execution_time_ms or 0, self.session_id))
                else:
                    cursor.execute('''
                        UPDATE terminal_sessions SET failed_commands = failed_commands + 1,
                               total_execution_time_ms = total_execution_time_ms + ?
                        WHERE session_id = ?
                    ''', (execution_time_ms or 0, self.session_id))
                
                self.conn.commit()
            
            # Log error if command failed
            if exit_code != 0 and error_message:
                self.log_terminal_error(command_id, "COMMAND_FAILED", error_message,
                                      error_code=exit_code)
            
            if self.verbose:
                status = "✅" if exit_code == 0 else "❌"
                print(f"{status} Command completed: {command_id}")
                print(f"   Exit code: {exit_code}")
                print(f"   Execution time: {execution_time_ms}ms")
                if memory_peak:
                    print(f"   Peak memory: {memory_peak:.1f}MB")
                    
        except Exception as e:
            print(f"❌ Error logging command completion: {e}")
    
    def log_terminal_error(self, command_id: Optional[str] = None, error_type: str = "GENERAL",
                          error_message: str = "", error_code: Optional[int] = None,
                          error_category: str = "USER", stack_trace: Optional[str] = None,
                          context_info: Optional[Dict] = None, severity: str = "ERROR"):
        """Log terminal error with detailed information"""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO terminal_errors (
                        command_id, session_id, error_type, error_category,
                        error_message, error_code, stack_trace, context_info, severity
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    command_id, self.session_id, error_type, error_category,
                    error_message, error_code, stack_trace,
                    json.dumps(context_info) if context_info else None, severity
                ))
                self.conn.commit()
            
            if self.verbose:
                print(f"❌ Terminal error logged: {error_type}")
                print(f"   Message: {error_message}")
                print(f"   Category: {error_category}")
                print(f"   Severity: {severity}")
                
        except Exception as e:
            print(f"❌ Error logging terminal error: {e}")
    
    def log_directory_change(self, old_dir: str, new_dir: str, 
                           command_id: Optional[str] = None, method: str = "cd"):
        """Log directory change"""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO directory_changes (
                        session_id, command_id, old_directory, new_directory,
                        change_method, success
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    self.session_id, command_id, old_dir, new_dir, method,
                    os.path.exists(new_dir)
                ))
                self.conn.commit()
            
            if self.verbose:
                print(f"📁 Directory change: {old_dir} → {new_dir}")
                
        except Exception as e:
            print(f"❌ Error logging directory change: {e}")
    
    def log_environment_change(self, variable_name: str, old_value: Optional[str] = None,
                             new_value: Optional[str] = None, change_type: str = "SET",
                             command_id: Optional[str] = None):
        """Log environment variable change"""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO environment_changes (
                        session_id, command_id, variable_name, old_value,
                        new_value, change_type
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    self.session_id, command_id, variable_name, old_value,
                    new_value, change_type
                ))
                self.conn.commit()
            
            if self.verbose:
                print(f"🔧 Environment change: {variable_name}={new_value}")
                
        except Exception as e:
            print(f"❌ Error logging environment change: {e}")
    
    def monitor_process(self, command_id: str, process_id: int, duration: int = 10):
        """Monitor process during execution"""
        try:
            process = psutil.Process(process_id)
            
            for _ in range(duration):
                try:
                    cpu_percent = process.cpu_percent(interval=1)
                    memory_info = process.memory_info()
                    memory_mb = memory_info.rss / 1024 / 1024
                    memory_percent = process.memory_percent()
                    
                    # Get additional process info
                    open_files = len(process.open_files()) if hasattr(process, 'open_files') else 0
                    connections = len(process.connections()) if hasattr(process, 'connections') else 0
                    status = process.status()
                    threads = process.num_threads()
                    
                    with self.lock:
                        cursor = self.conn.cursor()
                        cursor.execute('''
                            INSERT INTO process_monitoring (
                                command_id, session_id, process_id, cpu_percent,
                                memory_mb, memory_percent, open_files,
                                network_connections, status, threads
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            command_id, self.session_id, process_id, cpu_percent,
                            memory_mb, memory_percent, open_files,
                            connections, status, threads
                        ))
                        self.conn.commit()
                    
                    if self.verbose and cpu_percent > 50:
                        print(f"⚡ High CPU usage: {cpu_percent:.1f}% (PID: {process_id})")
                    
                except psutil.NoSuchProcess:
                    break
                except Exception as e:
                    if self.verbose:
                        print(f"⚠️ Process monitoring error: {e}")
                    break
                    
        except Exception as e:
            print(f"❌ Error in process monitoring: {e}")
    
    def detect_file_operations(self, command: str, command_id: str):
        """Detect file operations from command analysis"""
        try:
            file_ops = []
            
            # Simple detection based on common commands
            if command.startswith(('touch ', 'echo ')):
                # Look for file creation
                parts = command.split()
                for part in parts[1:]:
                    if not part.startswith('-') and '/' in part or '.' in part:
                        file_ops.append(('CREATE', part))
            
            elif command.startswith(('rm ', 'del ')):
                # File deletion
                parts = command.split()
                for part in parts[1:]:
                    if not part.startswith('-'):
                        file_ops.append(('DELETE', part))
            
            elif command.startswith(('mv ', 'cp ')):
                # Move/copy operations
                parts = command.split()
                if len(parts) >= 3:
                    file_ops.append(('MOVE' if command.startswith('mv') else 'COPY', parts[-1]))
            
            elif command.startswith('mkdir '):
                # Directory creation
                parts = command.split()
                for part in parts[1:]:
                    if not part.startswith('-'):
                        file_ops.append(('CREATE', part))
            
            # Log detected operations
            for op_type, file_path in file_ops:
                with self.lock:
                    cursor = self.conn.cursor()
                    cursor.execute('''
                        INSERT INTO file_operations (
                            command_id, session_id, operation_type, file_path,
                            detected_by
                        ) VALUES (?, ?, ?, ?, ?)
                    ''', (
                        command_id, self.session_id, op_type, file_path,
                        'COMMAND_ANALYSIS'
                    ))
                    self.conn.commit()
                
                if self.verbose:
                    print(f"📄 Detected file operation: {op_type} {file_path}")
                    
        except Exception as e:
            print(f"❌ Error detecting file operations: {e}")
    
    def get_session_summary(self) -> Dict:
        """Get comprehensive session summary"""
        with self.lock:
            cursor = self.conn.cursor()
            
            # Session info
            cursor.execute('SELECT * FROM terminal_sessions WHERE session_id = ?', (self.session_id,))
            session = cursor.fetchone()
            
            # Recent commands
            cursor.execute('''
                SELECT timestamp, command_line, exit_code, execution_time_ms
                FROM command_executions WHERE session_id = ? 
                ORDER BY timestamp DESC LIMIT 10
            ''', (self.session_id,))
            recent_commands = cursor.fetchall()
            
            # Error summary
            cursor.execute('''
                SELECT error_type, error_category, COUNT(*) as count 
                FROM terminal_errors WHERE session_id = ? 
                GROUP BY error_type, error_category
            ''', (self.session_id,))
            errors = cursor.fetchall()
            
            # Command patterns
            cursor.execute('''
                SELECT command_line, COUNT(*) as usage_count,
                       AVG(execution_time_ms) as avg_time,
                       SUM(CASE WHEN exit_code = 0 THEN 1 ELSE 0 END) as success_count
                FROM command_executions WHERE session_id = ? 
                GROUP BY SUBSTR(command_line, 1, 20)  -- Group by command prefix
                ORDER BY usage_count DESC LIMIT 5
            ''', (self.session_id,))
            patterns = cursor.fetchall()
            
            return {
                "session": session,
                "recent_commands": recent_commands,
                "errors": errors,
                "top_command_patterns": patterns
            }
    
    def search_terminal_history(self, query: str, limit: int = 20) -> List[Dict]:
        """Search through terminal history"""
        with self.lock:
            cursor = self.conn.cursor()
            
            results = []
            
            # Search commands
            cursor.execute('''
                SELECT 'COMMAND' as type, timestamp, command_line, exit_code, execution_time_ms
                FROM command_executions 
                WHERE command_line LIKE ? 
                ORDER BY timestamp DESC LIMIT ?
            ''', (f'%{query}%', limit//2))
            
            for row in cursor.fetchall():
                results.append({
                    'type': row[0],
                    'timestamp': row[1],
                    'command': row[2],
                    'exit_code': row[3],
                    'execution_time': row[4]
                })
            
            # Search outputs
            cursor.execute('''
                SELECT 'OUTPUT' as type, co.timestamp, ce.command_line, co.output_type, co.content
                FROM command_outputs co
                JOIN command_executions ce ON co.command_id = ce.command_id
                WHERE co.content LIKE ? 
                ORDER BY co.timestamp DESC LIMIT ?
            ''', (f'%{query}%', limit//2))
            
            for row in cursor.fetchall():
                results.append({
                    'type': row[0],
                    'timestamp': row[1],
                    'command': row[2],
                    'output_type': row[3],
                    'content': row[4][:200] + '...' if len(row[4]) > 200 else row[4]
                })
            
            return sorted(results, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def cleanup(self):
        """Clean up and finalize session"""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    UPDATE terminal_sessions SET 
                        ended_at = CURRENT_TIMESTAMP,
                        session_status = 'COMPLETED'
                    WHERE session_id = ?
                ''', (self.session_id,))
                self.conn.commit()
            
            # Print summary
            summary = self.get_session_summary()
            
            print("\n" + "="*80)
            print("💻 TERMINAL HISTORY SESSION SUMMARY")
            print("="*80)
            print(f"Session: {self.session_id}")
            if summary['session']:
                session = summary['session']
                print(f"Commands: {session[6]} total, {session[7]} successful, {session[8]} failed")
                print(f"Total execution time: {session[9]}ms")
            print(f"Errors: {len(summary['errors'])}")
            print(f"Top commands: {len(summary['top_command_patterns'])}")
            print("="*80)
            
            self.conn.close()
            
        except Exception as e:
            print(f"⚠️ Terminal cleanup warning: {e}")

# Global terminal history instance
_terminal_history = None

def get_terminal_history_db(verbose: bool = True) -> TerminalHistoryDB:
    """Get or create terminal history database"""
    global _terminal_history
    if _terminal_history is None:
        _terminal_history = TerminalHistoryDB(verbose=verbose)
    return _terminal_history

def log_terminal_command(command: str, working_dir: Optional[str] = None,
                        is_background: bool = False, process_id: Optional[int] = None) -> str:
    """Log start of a terminal command"""
    db = get_terminal_history_db()
    return db.log_command_start(command, working_dir, is_background, process_id)

def log_terminal_output(command_id: str, output_type: str, content: str, sequence: int = 0):
    """Log terminal output"""
    db = get_terminal_history_db()
    db.log_command_output(command_id, output_type, content, sequence)

def log_terminal_completion(command_id: str, exit_code: Optional[int] = None, error: Optional[str] = None):
    """Log terminal command completion"""
    db = get_terminal_history_db()
    db.log_command_completion(command_id, exit_code, error_message=error)

def log_terminal_error(error_type: str, error_message: str, command_id: Optional[str] = None,
                      error_code: Optional[int] = None, context: Optional[Dict] = None):
    """Log terminal error"""
    db = get_terminal_history_db()
    db.log_terminal_error(command_id, error_type, error_message, error_code, context_info=context)

if __name__ == "__main__":
    # Test the terminal history system
    print("🧪 TESTING TERMINAL HISTORY DATABASE")
    print("="*50)
    
    db = TerminalHistoryDB(verbose=True)
    
    # Test command logging
    cmd_id = db.log_command_start("echo 'Hello World'", os.getcwd())
    db.log_command_output(cmd_id, "STDOUT", "Hello World\n")
    db.log_command_completion(cmd_id, 0)
    
    # Test error logging
    error_cmd_id = db.log_command_start("invalid_command", os.getcwd())
    db.log_command_output(error_cmd_id, "STDERR", "command not found: invalid_command\n")
    db.log_command_completion(error_cmd_id, 127)
    db.log_terminal_error("COMMAND_NOT_FOUND", "invalid_command: command not found", 
                         error_cmd_id, 127)
    
    # Test directory change
    db.log_directory_change(os.getcwd(), "/tmp", method="cd")
    
    # Test environment change
    db.log_environment_change("TEST_VAR", None, "test_value", "SET")
    
    # Test search
    results = db.search_terminal_history("echo")
    print(f"Search results: {len(results)}")
    
    print("✅ Terminal History Database test completed")
