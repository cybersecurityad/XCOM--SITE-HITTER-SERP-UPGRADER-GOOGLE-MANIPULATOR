#!/usr/bin/env python3
"""
🎯 WORKSPACE ACTIVITY LOGGER
===========================
Dedicated logging system that captures ALL activity in the SEO crawler workspace:
- File operations and changes
- Process creation and termination
- Network connections
- System resource usage
- Error events and exceptions
- User interactions and commands

Creates a separate database file for comprehensive workspace monitoring.
"""

import sqlite3
import time
import os
import sys
import json
import threading
import subprocess
import psutil
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import atexit

class WorkspaceLogger:
    """Comprehensive workspace activity logging system"""
    
    def __init__(self, workspace_path: Optional[str] = None, db_file: str = "workspace_activity.db"):
        self.workspace_path = workspace_path or os.getcwd()
        self.db_file = db_file
        self.session_id = f"ws_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.getpid()}"
        self.running = True
        
        # Initialize database
        self.init_database()
        
        # Start monitoring threads
        self.start_monitoring()
        
        # Register cleanup
        atexit.register(self.cleanup)
        
        self.log_activity("WORKSPACE", "LOGGER_START", f"Workspace logger initialized", {
            "workspace_path": self.workspace_path,
            "session_id": self.session_id,
            "db_file": self.db_file
        })
        
        print(f"🔍 Workspace Logger Started")
        print(f"📁 Monitoring: {self.workspace_path}")
        print(f"🗄️ Database: {self.db_file}")
        print(f"🔗 Session: {self.session_id}")
    
    def init_database(self):
        """Initialize comprehensive logging database"""
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self.lock = threading.Lock()
        
        with self.lock:
            cursor = self.conn.cursor()
            
            # Activity log - captures all events
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    category TEXT NOT NULL,
                    action TEXT NOT NULL,
                    description TEXT,
                    details TEXT,
                    file_path TEXT,
                    process_id INTEGER,
                    user_id TEXT,
                    success BOOLEAN,
                    duration_ms INTEGER
                )
            ''')
            
            # File operations tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS file_operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    operation TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_size INTEGER,
                    file_hash TEXT,
                    old_hash TEXT,
                    modification_time DATETIME,
                    created_by TEXT
                )
            ''')
            
            # Process monitoring
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS process_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    event_type TEXT NOT NULL,
                    process_name TEXT NOT NULL,
                    process_id INTEGER,
                    parent_id INTEGER,
                    command_line TEXT,
                    cpu_percent REAL,
                    memory_mb REAL,
                    status TEXT
                )
            ''')
            
            # Network activity
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS network_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    connection_type TEXT,
                    local_address TEXT,
                    remote_address TEXT,
                    port INTEGER,
                    status TEXT,
                    process_name TEXT,
                    bytes_sent INTEGER,
                    bytes_received INTEGER
                )
            ''')
            
            # System performance snapshots
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    cpu_percent REAL,
                    memory_total_gb REAL,
                    memory_used_gb REAL,
                    memory_percent REAL,
                    disk_total_gb REAL,
                    disk_used_gb REAL,
                    disk_percent REAL,
                    load_average TEXT,
                    active_processes INTEGER,
                    network_connections INTEGER
                )
            ''')
            
            # Error tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS error_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    error_type TEXT NOT NULL,
                    error_message TEXT NOT NULL,
                    stack_trace TEXT,
                    source_file TEXT,
                    line_number INTEGER,
                    function_name TEXT,
                    severity TEXT DEFAULT 'ERROR'
                )
            ''')
            
            # Session metadata
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    workspace_path TEXT NOT NULL,
                    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ended_at DATETIME,
                    total_activities INTEGER DEFAULT 0,
                    total_files_changed INTEGER DEFAULT 0,
                    total_processes INTEGER DEFAULT 0,
                    total_errors INTEGER DEFAULT 0,
                    python_version TEXT,
                    os_info TEXT,
                    final_status TEXT
                )
            ''')
            
            self.conn.commit()
            
            # Insert session record
            cursor.execute('''
                INSERT OR REPLACE INTO sessions (
                    session_id, workspace_path, python_version, os_info
                ) VALUES (?, ?, ?, ?)
            ''', (
                self.session_id, 
                self.workspace_path,
                sys.version,
                f"{os.name} {os.uname().sysname} {os.uname().release}"
            ))
            self.conn.commit()
    
    def log_activity(self, category: str, action: str, description: str = "",
                    details: Optional[Dict[str, Any]] = None, file_path: Optional[str] = None,
                    success: Optional[bool] = None, duration_ms: Optional[int] = None):
        """Log any workspace activity"""
        
        with self.lock:
            cursor = self.conn.cursor()
            
            details_json = json.dumps(details) if details else None
            
            cursor.execute('''
                INSERT INTO activity_log (
                    session_id, category, action, description, details, 
                    file_path, process_id, success, duration_ms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.session_id, category, action, description, details_json,
                file_path, os.getpid(), success, duration_ms
            ))
            
            # Update session counter
            cursor.execute('''
                UPDATE sessions SET total_activities = total_activities + 1
                WHERE session_id = ?
            ''', (self.session_id,))
            
            self.conn.commit()
            
            # Console output
            status = "✅" if success is True else "❌" if success is False else "🔄"
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"{timestamp} | {status} [{category}] {action}: {description}")
    
    def log_file_operation(self, operation: str, file_path: str):
        """Log file operations"""
        try:
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                file_size = stat.st_size
                mod_time = datetime.fromtimestamp(stat.st_mtime)
                
                # Calculate file hash for change detection
                file_hash = None
                if file_size < 10 * 1024 * 1024:  # Only hash files < 10MB
                    try:
                        with open(file_path, 'rb') as f:
                            file_hash = hashlib.md5(f.read()).hexdigest()
                    except:
                        pass
            else:
                file_size = None
                mod_time = None
                file_hash = None
            
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO file_operations (
                        session_id, operation, file_path, file_size, 
                        file_hash, modification_time
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (self.session_id, operation, file_path, file_size, file_hash, mod_time))
                
                # Update session counter
                cursor.execute('''
                    UPDATE sessions SET total_files_changed = total_files_changed + 1
                    WHERE session_id = ?
                ''', (self.session_id,))
                
                self.conn.commit()
            
            self.log_activity("FILE", operation, f"File {operation.lower()}: {os.path.basename(file_path)}", {
                "file_path": file_path,
                "file_size": file_size,
                "file_hash": file_hash[:8] if file_hash else None
            }, file_path=file_path, success=True)
            
        except Exception as e:
            self.log_error("FILE_OPERATION", str(e), file_path)
    
    def log_process_event(self, event_type: str, process_name: str, pid: Optional[int] = None,
                         command_line: Optional[str] = None, parent_id: Optional[int] = None):
        """Log process events"""
        try:
            if pid:
                try:
                    process = psutil.Process(pid)
                    cpu_percent = process.cpu_percent()
                    memory_mb = process.memory_info().rss / 1024 / 1024
                    status = process.status()
                except:
                    cpu_percent = None
                    memory_mb = None
                    status = "unknown"
            else:
                cpu_percent = None
                memory_mb = None
                status = None
            
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO process_activity (
                        session_id, event_type, process_name, process_id,
                        parent_id, command_line, cpu_percent, memory_mb, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (self.session_id, event_type, process_name, pid, parent_id,
                      command_line, cpu_percent, memory_mb, status))
                
                # Update session counter
                cursor.execute('''
                    UPDATE sessions SET total_processes = total_processes + 1
                    WHERE session_id = ?
                ''', (self.session_id,))
                
                self.conn.commit()
            
            self.log_activity("PROCESS", event_type, f"Process {event_type.lower()}: {process_name}", {
                "process_name": process_name,
                "pid": pid,
                "parent_id": parent_id,
                "cpu_percent": cpu_percent,
                "memory_mb": memory_mb
            }, success=True)
            
        except Exception as e:
            self.log_error("PROCESS_EVENT", str(e))
    
    def log_error(self, error_type: str, error_message: str, source_file: Optional[str] = None):
        """Log errors"""
        import traceback
        
        stack_trace = traceback.format_exc() if sys.exc_info()[0] else None
        
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO error_log (
                    session_id, error_type, error_message, stack_trace, source_file
                ) VALUES (?, ?, ?, ?, ?)
            ''', (self.session_id, error_type, error_message, stack_trace, source_file))
            
            # Update session error count
            cursor.execute('''
                UPDATE sessions SET total_errors = total_errors + 1
                WHERE session_id = ?
            ''', (self.session_id,))
            
            self.conn.commit()
        
        self.log_activity("ERROR", error_type, error_message, {
            "source_file": source_file,
            "has_stack_trace": bool(stack_trace)
        }, success=False)
    
    def capture_system_snapshot(self):
        """Capture current system state"""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage(self.workspace_path)
            
            # Process count
            active_processes = len(psutil.pids())
            
            # Network connections
            try:
                network_connections = len(psutil.net_connections())
            except:
                network_connections = 0
            
            # Load average (Unix systems)
            try:
                load_avg = os.getloadavg()
                load_average = f"{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"
            except:
                load_average = "N/A"
            
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO system_snapshots (
                        session_id, cpu_percent, memory_total_gb, memory_used_gb,
                        memory_percent, disk_total_gb, disk_used_gb, disk_percent,
                        load_average, active_processes, network_connections
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    self.session_id, cpu_percent,
                    memory.total / 1024**3, memory.used / 1024**3, memory.percent,
                    disk.total / 1024**3, disk.used / 1024**3, (disk.used / disk.total) * 100,
                    load_average, active_processes, network_connections
                ))
                self.conn.commit()
                
        except Exception as e:
            self.log_error("SYSTEM_SNAPSHOT", str(e))
    
    def monitor_processes(self):
        """Monitor process creation/termination"""
        known_pids = set(psutil.pids())
        
        while self.running:
            try:
                current_pids = set(psutil.pids())
                
                # New processes
                new_pids = current_pids - known_pids
                for pid in new_pids:
                    try:
                        process = psutil.Process(pid)
                        self.log_process_event("CREATED", process.name(), pid, 
                                             " ".join(process.cmdline()) if process.cmdline() else "",
                                             process.ppid())
                    except:
                        pass
                
                # Terminated processes
                dead_pids = known_pids - current_pids
                for pid in dead_pids:
                    self.log_process_event("TERMINATED", f"PID_{pid}", pid)
                
                known_pids = current_pids
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                self.log_error("PROCESS_MONITOR", str(e))
                time.sleep(5)
    
    def monitor_files(self):
        """Monitor file changes in workspace"""
        file_states = {}
        
        while self.running:
            try:
                # Scan workspace files
                for root, dirs, files in os.walk(self.workspace_path):
                    # Skip hidden directories and common build/temp directories
                    dirs[:] = [d for d in dirs if not d.startswith('.') and 
                              d not in ['__pycache__', 'node_modules', '.venv', 'venv']]
                    
                    for file in files:
                        if file.startswith('.'):
                            continue
                            
                        file_path = os.path.join(root, file)
                        
                        try:
                            stat = os.stat(file_path)
                            current_mtime = stat.st_mtime
                            
                            if file_path in file_states:
                                if current_mtime > file_states[file_path]:
                                    self.log_file_operation("MODIFIED", file_path)
                                    file_states[file_path] = current_mtime
                            else:
                                # New file or first scan
                                if len(file_states) > 0:  # Not first scan
                                    self.log_file_operation("CREATED", file_path)
                                file_states[file_path] = current_mtime
                                
                        except:
                            pass
                
                # Check for deleted files
                existing_files = set()
                for root, dirs, files in os.walk(self.workspace_path):
                    dirs[:] = [d for d in dirs if not d.startswith('.') and 
                              d not in ['__pycache__', 'node_modules', '.venv', 'venv']]
                    for file in files:
                        if not file.startswith('.'):
                            existing_files.add(os.path.join(root, file))
                
                deleted_files = set(file_states.keys()) - existing_files
                for file_path in deleted_files:
                    self.log_file_operation("DELETED", file_path)
                    del file_states[file_path]
                
                time.sleep(3)  # Check every 3 seconds
                
            except Exception as e:
                self.log_error("FILE_MONITOR", str(e))
                time.sleep(5)
    
    def monitor_system(self):
        """Monitor system performance"""
        while self.running:
            try:
                self.capture_system_snapshot()
                time.sleep(10)  # Snapshot every 10 seconds
            except Exception as e:
                self.log_error("SYSTEM_MONITOR", str(e))
                time.sleep(10)
    
    def start_monitoring(self):
        """Start all monitoring threads"""
        self.threads = []
        
        # Process monitoring
        process_thread = threading.Thread(target=self.monitor_processes, daemon=True)
        process_thread.start()
        self.threads.append(process_thread)
        
        # File monitoring
        file_thread = threading.Thread(target=self.monitor_files, daemon=True)
        file_thread.start()
        self.threads.append(file_thread)
        
        # System monitoring
        system_thread = threading.Thread(target=self.monitor_system, daemon=True)
        system_thread.start()
        self.threads.append(system_thread)
        
        self.log_activity("WORKSPACE", "MONITORING_STARTED", "All monitoring threads started", {
            "thread_count": len(self.threads)
        }, success=True)
    
    def get_activity_summary(self):
        """Get comprehensive activity summary"""
        with self.lock:
            cursor = self.conn.cursor()
            
            # Get session info
            cursor.execute('SELECT * FROM sessions WHERE session_id = ?', (self.session_id,))
            session = cursor.fetchone()
            
            # Activity by category
            cursor.execute('''
                SELECT category, COUNT(*) as count 
                FROM activity_log WHERE session_id = ? 
                GROUP BY category ORDER BY count DESC
            ''', (self.session_id,))
            activity_by_category = cursor.fetchall()
            
            # Recent activities
            cursor.execute('''
                SELECT timestamp, category, action, description 
                FROM activity_log WHERE session_id = ? 
                ORDER BY timestamp DESC LIMIT 10
            ''', (self.session_id,))
            recent_activities = cursor.fetchall()
            
            # File operations summary
            cursor.execute('''
                SELECT operation, COUNT(*) as count 
                FROM file_operations WHERE session_id = ? 
                GROUP BY operation
            ''', (self.session_id,))
            file_ops = cursor.fetchall()
            
            # Process summary
            cursor.execute('''
                SELECT event_type, COUNT(*) as count 
                FROM process_activity WHERE session_id = ? 
                GROUP BY event_type
            ''', (self.session_id,))
            process_events = cursor.fetchall()
            
            # Error summary
            cursor.execute('''
                SELECT error_type, COUNT(*) as count 
                FROM error_log WHERE session_id = ? 
                GROUP BY error_type
            ''', (self.session_id,))
            errors = cursor.fetchall()
            
            return {
                "session": session,
                "activity_by_category": dict(activity_by_category),
                "recent_activities": recent_activities,
                "file_operations": dict(file_ops),
                "process_events": dict(process_events),
                "errors": dict(errors)
            }
    
    def cleanup(self):
        """Stop monitoring and close database"""
        self.running = False
        
        # Wait for threads to finish
        for thread in getattr(self, 'threads', []):
            thread.join(timeout=2)
        
        # Update session end time
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE sessions SET 
                    ended_at = CURRENT_TIMESTAMP,
                    final_status = 'COMPLETED'
                WHERE session_id = ?
            ''', (self.session_id,))
            self.conn.commit()
        
        # Print summary
        summary = self.get_activity_summary()
        
        print("\n" + "=" * 80)
        print("📊 WORKSPACE ACTIVITY SUMMARY")
        print("=" * 80)
        print(f"Session: {self.session_id}")
        print(f"Workspace: {self.workspace_path}")
        print(f"Activities by Category: {summary['activity_by_category']}")
        print(f"File Operations: {summary['file_operations']}")
        print(f"Process Events: {summary['process_events']}")
        print(f"Errors: {summary['errors']}")
        print("=" * 80)
        
        self.log_activity("WORKSPACE", "LOGGER_STOP", "Workspace logger shutdown completed")
        self.conn.close()

# Global logger instance
_workspace_logger = None

def start_workspace_logging(workspace_path: Optional[str] = None):
    """Start workspace logging"""
    global _workspace_logger
    if _workspace_logger is None:
        _workspace_logger = WorkspaceLogger(workspace_path)
    return _workspace_logger

def get_workspace_logger():
    """Get workspace logger instance"""
    global _workspace_logger
    return _workspace_logger

def log_workspace_activity(category: str, action: str, description: str = "", **kwargs):
    """Log workspace activity"""
    logger = get_workspace_logger()
    if logger:
        logger.log_activity(category, action, description, **kwargs)

if __name__ == "__main__":
    # Start workspace logging
    logger = start_workspace_logging()
    
    print("Workspace logger running... Press Ctrl+C to stop")
    
    try:
        # Test some activities
        logger.log_activity("TEST", "MANUAL_TEST", "Testing workspace logger")
        
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping workspace logger...")
        logger.cleanup()
