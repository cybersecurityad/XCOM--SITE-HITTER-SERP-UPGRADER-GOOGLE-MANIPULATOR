#!/usr/bin/env python3
"""
🗄️ COMPREHENSIVE LOGGING DATABASE SYSTEM
========================================
Complete logging system with SQLite database storage for all operations:
- Browser creation and lifecycle
- Tor integration attempts
- GA tracking events
- System performance metrics
- Error tracking and debugging
- Session management

Initializes on startup and logs EVERYTHING for complete visibility.
"""

import sqlite3
import time
import os
import sys
import json
import traceback
import psutil
import subprocess
from datetime import datetime
from typing import Optional, Dict, Any
import logging

class LoggingDatabase:
    """Comprehensive logging system with SQLite database storage"""
    
    def __init__(self, db_path="seo_crawler_logs.db"):
        self.db_path = db_path
        self.session_id = self.generate_session_id()
        self.init_database()
        self.setup_file_logging()
        
        # Log system startup
        self.log_event("SYSTEM", "STARTUP", "Database logging system initialized", {
            "session_id": self.session_id,
            "db_path": self.db_path,
            "python_version": sys.version,
            "working_directory": os.getcwd()
        })
    
    def generate_session_id(self):
        """Generate unique session ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"session_{timestamp}_{os.getpid()}"
    
    def setup_file_logging(self):
        """Setup file logging in addition to database"""
        log_filename = f"crawler_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s.%(msecs)03d | %(levelname)8s | %(message)s',
            datefmt='%H:%M:%S',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger('SEOCrawler')
        self.logger.info(f"📊 Session logging started: {log_filename}")
    
    def init_database(self):
        """Initialize SQLite database with comprehensive tables"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.create_tables()
        
        # Log database initialization
        print(f"🗄️ Database initialized: {self.db_path}")
        print(f"🔗 Session ID: {self.session_id}")
    
    def create_tables(self):
        """Create all necessary database tables"""
        
        # Main events log
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                category TEXT NOT NULL,
                event_type TEXT NOT NULL,
                message TEXT NOT NULL,
                details TEXT,
                success BOOLEAN,
                duration_ms INTEGER,
                process_id INTEGER,
                memory_mb REAL,
                cpu_percent REAL
            )
        ''')
        
        # Browser lifecycle tracking
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS browsers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                browser_id TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                closed_at DATETIME,
                creation_duration_ms INTEGER,
                proxy_used TEXT,
                chrome_pid INTEGER,
                chrome_version TEXT,
                user_agent TEXT,
                status TEXT DEFAULT 'active',
                error_count INTEGER DEFAULT 0
            )
        ''')
        
        # Tor operations tracking
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tor_operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                operation TEXT NOT NULL,
                status TEXT NOT NULL,
                tor_pid INTEGER,
                tor_port INTEGER,
                control_port INTEGER,
                circuits_count INTEGER,
                bootstrap_percent INTEGER,
                exit_country TEXT,
                duration_ms INTEGER,
                error_message TEXT
            )
        ''')
        
        # GA tracking events
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ga_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                browser_id TEXT,
                event_name TEXT NOT NULL,
                event_data TEXT,
                tracking_id TEXT,
                page_url TEXT,
                success BOOLEAN,
                response_time_ms INTEGER
            )
        ''')
        
        # System performance metrics
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cpu_percent REAL,
                memory_mb REAL,
                memory_percent REAL,
                disk_usage_gb REAL,
                network_sent_mb REAL,
                network_recv_mb REAL,
                chrome_processes INTEGER,
                tor_processes INTEGER
            )
        ''')
        
        # Error tracking
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                error_type TEXT NOT NULL,
                error_message TEXT NOT NULL,
                stack_trace TEXT,
                context TEXT,
                component TEXT,
                severity TEXT DEFAULT 'ERROR'
            )
        ''')
        
        # Session metadata
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                ended_at DATETIME,
                total_browsers INTEGER DEFAULT 0,
                total_events INTEGER DEFAULT 0,
                total_errors INTEGER DEFAULT 0,
                tor_used BOOLEAN DEFAULT FALSE,
                ga_tracking_used BOOLEAN DEFAULT FALSE,
                final_status TEXT
            )
        ''')
        
        self.conn.commit()
        
        # Insert session record
        self.cursor.execute('''
            INSERT OR REPLACE INTO sessions (session_id)
            VALUES (?)
        ''', (self.session_id,))
        self.conn.commit()
    
    def log_event(self, category: str, event_type: str, message: str, 
                  details: Optional[Dict[str, Any]] = None, success: Optional[bool] = None,
                  duration_ms: Optional[int] = None):
        """Log an event to database and file"""
        
        # Get system metrics
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        cpu_percent = process.cpu_percent()
        
        # Prepare details as JSON
        details_json = json.dumps(details) if details else None
        
        # Log to database
        self.cursor.execute('''
            INSERT INTO events (
                session_id, category, event_type, message, details, 
                success, duration_ms, process_id, memory_mb, cpu_percent
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.session_id, category, event_type, message, details_json,
            success, duration_ms, os.getpid(), memory_mb, cpu_percent
        ))
        self.conn.commit()
        
        # Log to file
        status = "✅" if success is True else "❌" if success is False else "🔄"
        log_message = f"{status} [{category}] {event_type}: {message}"
        if details:
            log_message += f" | {details}"
        
        self.logger.info(log_message)
    
    def log_browser_created(self, browser_id: str, creation_duration_ms: int,
                           proxy_used: Optional[str] = None, chrome_pid: Optional[int] = None,
                           user_agent: Optional[str] = None):
        """Log browser creation"""
        self.cursor.execute('''
            INSERT INTO browsers (
                session_id, browser_id, creation_duration_ms, proxy_used,
                chrome_pid, user_agent, status
            ) VALUES (?, ?, ?, ?, ?, ?, 'active')
        ''', (self.session_id, browser_id, creation_duration_ms, proxy_used, chrome_pid, user_agent))
        self.conn.commit()
        
        # Update session stats
        self.cursor.execute('''
            UPDATE sessions SET total_browsers = total_browsers + 1
            WHERE session_id = ?
        ''', (self.session_id,))
        self.conn.commit()
        
        self.log_event("BROWSER", "CREATED", f"Browser {browser_id} created", {
            "browser_id": browser_id,
            "creation_time_ms": creation_duration_ms,
            "proxy": proxy_used,
            "chrome_pid": chrome_pid
        }, success=True, duration_ms=creation_duration_ms)
    
    def log_browser_closed(self, browser_id: str):
        """Log browser closure"""
        self.cursor.execute('''
            UPDATE browsers SET 
                closed_at = CURRENT_TIMESTAMP,
                status = 'closed'
            WHERE session_id = ? AND browser_id = ?
        ''', (self.session_id, browser_id))
        self.conn.commit()
        
        self.log_event("BROWSER", "CLOSED", f"Browser {browser_id} closed", {
            "browser_id": browser_id
        }, success=True)
    
    def log_tor_operation(self, operation: str, status: str, 
                         tor_pid: Optional[int] = None, tor_port: Optional[int] = None,
                         bootstrap_percent: Optional[int] = None, duration_ms: Optional[int] = None,
                         error_message: Optional[str] = None):
        """Log Tor operations"""
        self.cursor.execute('''
            INSERT INTO tor_operations (
                session_id, operation, status, tor_pid, tor_port,
                bootstrap_percent, duration_ms, error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.session_id, operation, status, tor_pid, tor_port, 
              bootstrap_percent, duration_ms, error_message))
        self.conn.commit()
        
        if operation == "START" and status == "SUCCESS":
            self.cursor.execute('''
                UPDATE sessions SET tor_used = TRUE WHERE session_id = ?
            ''', (self.session_id,))
            self.conn.commit()
        
        self.log_event("TOR", operation, f"Tor {operation.lower()}: {status}", {
            "tor_pid": tor_pid,
            "tor_port": tor_port,
            "bootstrap_percent": bootstrap_percent,
            "error": error_message
        }, success=(status == "SUCCESS"), duration_ms=duration_ms)
    
    def log_ga_event(self, browser_id: str, event_name: str, event_data: Dict[str, Any],
                     tracking_id: str, page_url: str, success: bool, response_time_ms: int):
        """Log Google Analytics events"""
        self.cursor.execute('''
            INSERT INTO ga_events (
                session_id, browser_id, event_name, event_data, tracking_id,
                page_url, success, response_time_ms
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.session_id, browser_id, event_name, json.dumps(event_data),
              tracking_id, page_url, success, response_time_ms))
        self.conn.commit()
        
        if event_name == "page_view":
            self.cursor.execute('''
                UPDATE sessions SET ga_tracking_used = TRUE WHERE session_id = ?
            ''', (self.session_id,))
            self.conn.commit()
        
        self.log_event("GA", event_name.upper(), f"GA event sent: {event_name}", {
            "browser_id": browser_id,
            "tracking_id": tracking_id,
            "page_url": page_url,
            "event_data": event_data
        }, success=success, duration_ms=response_time_ms)
    
    def log_error(self, error_type: str, error_message: str, 
                  context: Optional[str] = None, component: Optional[str] = None,
                  severity: str = "ERROR"):
        """Log errors with full context"""
        stack_trace = traceback.format_exc() if sys.exc_info()[0] else None
        
        self.cursor.execute('''
            INSERT INTO errors (
                session_id, error_type, error_message, stack_trace,
                context, component, severity
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.session_id, error_type, error_message, stack_trace,
              context, component, severity))
        self.conn.commit()
        
        # Update session error count
        self.cursor.execute('''
            UPDATE sessions SET total_errors = total_errors + 1
            WHERE session_id = ?
        ''', (self.session_id,))
        self.conn.commit()
        
        self.log_event("ERROR", error_type, error_message, {
            "component": component,
            "context": context,
            "severity": severity
        }, success=False)
    
    def log_performance_metrics(self):
        """Log current system performance metrics"""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            # Process counts
            chrome_processes = len([p for p in psutil.process_iter(['name']) 
                                  if 'chrome' in p.info['name'].lower()])
            tor_processes = len([p for p in psutil.process_iter(['name']) 
                               if 'tor' in p.info['name'].lower()])
            
            self.cursor.execute('''
                INSERT INTO performance (
                    session_id, cpu_percent, memory_mb, memory_percent,
                    disk_usage_gb, network_sent_mb, network_recv_mb,
                    chrome_processes, tor_processes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.session_id, cpu_percent, memory.used / 1024 / 1024,
                memory.percent, disk.used / 1024 / 1024 / 1024,
                network.bytes_sent / 1024 / 1024, network.bytes_recv / 1024 / 1024,
                chrome_processes, tor_processes
            ))
            self.conn.commit()
            
        except Exception as e:
            self.log_error("PERFORMANCE_METRICS", str(e), "Failed to collect performance metrics")
    
    def get_session_summary(self):
        """Get comprehensive session summary"""
        # Get session data
        self.cursor.execute('''
            SELECT * FROM sessions WHERE session_id = ?
        ''', (self.session_id,))
        session = self.cursor.fetchone()
        
        # Get event counts by category
        self.cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM events WHERE session_id = ? 
            GROUP BY category
        ''', (self.session_id,))
        event_counts = dict(self.cursor.fetchall())
        
        # Get error summary
        self.cursor.execute('''
            SELECT error_type, COUNT(*) as count 
            FROM errors WHERE session_id = ? 
            GROUP BY error_type
        ''', (self.session_id,))
        error_summary = dict(self.cursor.fetchall())
        
        # Get browser summary
        self.cursor.execute('''
            SELECT COUNT(*) as total, 
                   COUNT(CASE WHEN status = 'active' THEN 1 END) as active,
                   AVG(creation_duration_ms) as avg_creation_time
            FROM browsers WHERE session_id = ?
        ''', (self.session_id,))
        browser_stats = self.cursor.fetchone()
        
        return {
            "session_id": self.session_id,
            "session_data": session,
            "event_counts": event_counts,
            "error_summary": error_summary,
            "browser_stats": {
                "total": browser_stats[0],
                "active": browser_stats[1],
                "avg_creation_time_ms": browser_stats[2]
            }
        }
    
    def close_session(self, final_status: str = "COMPLETED"):
        """Close session and update final status"""
        self.cursor.execute('''
            UPDATE sessions SET 
                ended_at = CURRENT_TIMESTAMP,
                final_status = ?
            WHERE session_id = ?
        ''', (final_status, self.session_id))
        self.conn.commit()
        
        # Log session end
        summary = self.get_session_summary()
        self.log_event("SYSTEM", "SHUTDOWN", f"Session ended: {final_status}", summary)
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 SESSION SUMMARY")
        print("=" * 80)
        print(f"Session ID: {self.session_id}")
        print(f"Status: {final_status}")
        print(f"Total Events: {summary['event_counts']}")
        print(f"Browsers Created: {summary['browser_stats']['total']}")
        print(f"Errors: {len(summary['error_summary'])}")
        print("=" * 80)
        
        self.conn.close()

# Global logging instance
_logger_db = None

def init_logging_system():
    """Initialize global logging system"""
    global _logger_db
    _logger_db = LoggingDatabase()
    return _logger_db

def get_logger():
    """Get global logger instance"""
    global _logger_db
    if _logger_db is None:
        _logger_db = init_logging_system()
    return _logger_db

def log_event(category: str, event_type: str, message: str, **kwargs):
    """Convenience function for logging events"""
    logger = get_logger()
    logger.log_event(category, event_type, message, **kwargs)

def log_error(error_type: str, error_message: str, **kwargs):
    """Convenience function for logging errors"""
    logger = get_logger()
    logger.log_error(error_type, error_message, **kwargs)

if __name__ == "__main__":
    # Test the logging system
    logger = init_logging_system()
    
    # Test various log types
    logger.log_event("TEST", "STARTUP", "Testing logging system")
    logger.log_browser_created("test_browser_1", 1500, "socks5://127.0.0.1:9050")
    logger.log_tor_operation("START", "SUCCESS", tor_pid=12345, tor_port=9050, bootstrap_percent=100)
    logger.log_ga_event("test_browser_1", "page_view", {"page": "test"}, "G-TEST123", "https://test.com", True, 250)
    logger.log_performance_metrics()
    
    # Test error logging
    try:
        raise ValueError("Test error")
    except Exception:
        logger.log_error("TEST_ERROR", "This is a test error", component="test_module")
    
    # Show summary and close
    time.sleep(1)
    logger.close_session("TEST_COMPLETED")
