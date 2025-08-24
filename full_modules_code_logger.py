#!/usr/bin/env python3
"""
📋 FULL MODULES CODE LOGGER
==========================
Master logging system that captures ALL code modules in the workspace.
This file is updated on every initialization and serves as the primary
reference for all operations and debugging.

Purpose:
- Maintains complete snapshot of all Python modules
- Updates automatically on initialization
- Provides comprehensive code reference
- Enables full context debugging
- Tracks module changes over time
"""

import os
import sys
import time
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
import sqlite3

class FullModulesCodeLogger:
    """Comprehensive code logging system for all modules"""
    
    def __init__(self, workspace_path: str = ".", log_file: str = "full_modules_code_log.json"):
        self.workspace_path = os.path.abspath(workspace_path)
        self.log_file = log_file
        self.db_file = "workspace_activity.db"
        self.session_id = self.generate_session_id()
        
        print(f"📋 FULL MODULES CODE LOGGER")
        print(f"=" * 50)
        print(f"🔗 Session ID: {self.session_id}")
        print(f"📁 Workspace: {self.workspace_path}")
        print(f"📄 Log File: {self.log_file}")
        print(f"🗄️ Database: {self.db_file}")
        print(f"=" * 50)
        
        self.init_database()
        self.scan_and_log_all_modules()
    
    def generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"session_{timestamp}_{os.getpid()}"
    
    def init_database(self):
        """Initialize database for tracking module changes"""
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS module_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                module_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                line_count INTEGER,
                char_count INTEGER,
                last_modified DATETIME,
                file_size_bytes INTEGER
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions_modules (
                session_id TEXT PRIMARY KEY,
                started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                workspace_path TEXT,
                total_modules INTEGER,
                total_lines INTEGER,
                total_chars INTEGER,
                python_version TEXT,
                log_file_path TEXT
            )
        ''')
        
        self.conn.commit()
        print(f"🗄️ Database initialized: {self.db_file}")
    
    def get_file_hash(self, content: str) -> str:
        """Calculate SHA256 hash of file content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def scan_python_files(self) -> List[str]:
        """Scan workspace for all Python files"""
        python_files = []
        
        for root, dirs, files in os.walk(self.workspace_path):
            # Skip hidden directories and __pycache__
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    python_files.append(file_path)
        
        return sorted(python_files)
    
    def read_module_content(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Read and analyze module content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get file stats
            stat = os.stat(file_path)
            
            # Calculate metrics
            lines = content.split('\n')
            line_count = len(lines)
            char_count = len(content)
            content_hash = self.get_file_hash(content)
            
            # Get relative path
            rel_path = os.path.relpath(file_path, self.workspace_path)
            module_name = rel_path.replace('/', '.').replace('.py', '')
            
            return {
                'module_name': module_name,
                'file_path': rel_path,
                'absolute_path': file_path,
                'content': content,
                'content_hash': content_hash,
                'line_count': line_count,
                'char_count': char_count,
                'file_size_bytes': stat.st_size,
                'last_modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'lines': lines
            }
        
        except Exception as e:
            print(f"❌ Failed to read {file_path}: {e}")
            return None
    
    def scan_and_log_all_modules(self):
        """Scan all modules and create comprehensive log"""
        print(f"🔍 Scanning workspace for Python modules...")
        
        python_files = self.scan_python_files()
        print(f"📁 Found {len(python_files)} Python files")
        
        modules_data = {}
        total_lines = 0
        total_chars = 0
        successful_reads = 0
        
        for file_path in python_files:
            print(f"📄 Reading: {os.path.relpath(file_path, self.workspace_path)}")
            
            module_data = self.read_module_content(file_path)
            if module_data:
                modules_data[module_data['module_name']] = module_data
                total_lines += module_data['line_count']
                total_chars += module_data['char_count']
                successful_reads += 1
                
                # Log to database
                self.cursor.execute('''
                    INSERT INTO module_snapshots (
                        session_id, module_name, file_path, content_hash,
                        line_count, char_count, last_modified, file_size_bytes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    self.session_id, module_data['module_name'], module_data['file_path'],
                    module_data['content_hash'], module_data['line_count'], 
                    module_data['char_count'], module_data['last_modified'],
                    module_data['file_size_bytes']
                ))
        
        # Save session info
        self.cursor.execute('''
            INSERT OR REPLACE INTO sessions_modules (
                session_id, workspace_path, total_modules, total_lines,
                total_chars, python_version, log_file_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.session_id, self.workspace_path, successful_reads,
            total_lines, total_chars, sys.version, self.log_file
        ))
        
        self.conn.commit()
        
        # Create comprehensive log structure
        log_data = {
            'metadata': {
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat(),
                'workspace_path': self.workspace_path,
                'total_modules': successful_reads,
                'total_files_found': len(python_files),
                'total_lines': total_lines,
                'total_chars': total_chars,
                'python_version': sys.version,
                'scan_duration_seconds': 0  # Will be updated
            },
            'modules': modules_data,
            'file_list': [os.path.relpath(f, self.workspace_path) for f in python_files],
            'module_index': list(modules_data.keys())
        }
        
        # Save to JSON file
        self.save_log_file(log_data)
        
        # Print summary
        print(f"✅ Scan completed!")
        print(f"📊 SUMMARY:")
        print(f"   📁 Files found: {len(python_files)}")
        print(f"   ✅ Successfully read: {successful_reads}")
        print(f"   📄 Total lines: {total_lines:,}")
        print(f"   🔤 Total characters: {total_chars:,}")
        print(f"   💾 Log saved: {self.log_file}")
        
        return log_data
    
    def save_log_file(self, log_data: Dict[str, Any]):
        """Save comprehensive log to JSON file"""
        try:
            # Add timestamp
            log_data['metadata']['last_updated'] = datetime.now().isoformat()
            
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Log file saved: {self.log_file}")
            
        except Exception as e:
            print(f"❌ Failed to save log file: {e}")
    
    def read_existing_log(self) -> Optional[Dict[str, Any]]:
        """Read existing log file if it exists"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                
                print(f"📖 Existing log file read: {self.log_file}")
                print(f"   📅 Last updated: {log_data['metadata'].get('last_updated', 'Unknown')}")
                print(f"   📁 Modules: {log_data['metadata'].get('total_modules', 0)}")
                
                return log_data
                
            except Exception as e:
                print(f"❌ Failed to read existing log: {e}")
                return None
        else:
            print(f"ℹ️ No existing log file found: {self.log_file}")
            return None
    
    def get_module_content(self, module_name: str) -> Optional[str]:
        """Get content of specific module from log"""
        log_data = self.read_existing_log()
        if log_data and module_name in log_data.get('modules', {}):
            return log_data['modules'][module_name]['content']
        return None
    
    def list_all_modules(self) -> List[str]:
        """Get list of all modules in log"""
        log_data = self.read_existing_log()
        if log_data:
            return log_data.get('module_index', [])
        return []
    
    def get_module_info(self, module_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed info about specific module"""
        log_data = self.read_existing_log()
        if log_data and module_name in log_data.get('modules', {}):
            module_data = log_data['modules'][module_name]
            return {
                'module_name': module_data['module_name'],
                'file_path': module_data['file_path'],
                'line_count': module_data['line_count'],
                'char_count': module_data['char_count'],
                'last_modified': module_data['last_modified'],
                'content_hash': module_data['content_hash']
            }
        return None
    
    def close(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()
            print(f"🔒 Database connection closed")

def init_full_modules_logger(workspace_path: str = ".", log_file: str = "full_modules_code_log.json"):
    """Initialize and run full modules code logger"""
    logger = FullModulesCodeLogger(workspace_path, log_file)
    return logger

def read_full_modules_log(log_file: str = "full_modules_code_log.json") -> Optional[Dict[str, Any]]:
    """Read the full modules log file"""
    logger = FullModulesCodeLogger()
    return logger.read_existing_log()

def get_module_from_log(module_name: str, log_file: str = "full_modules_code_log.json") -> Optional[str]:
    """Get specific module content from log"""
    logger = FullModulesCodeLogger()
    return logger.get_module_content(module_name)

def list_modules_in_log(log_file: str = "full_modules_code_log.json") -> List[str]:
    """List all modules in log"""
    logger = FullModulesCodeLogger()
    return logger.list_all_modules()

if __name__ == "__main__":
    print("🚀 INITIALIZING FULL MODULES CODE LOGGER")
    print("=" * 60)
    
    # Always read existing log first
    print("1️⃣ READING EXISTING LOG...")
    logger = FullModulesCodeLogger()
    existing_log = logger.read_existing_log()
    
    if existing_log:
        print(f"📖 Found existing log with {existing_log['metadata']['total_modules']} modules")
        print(f"📅 Last updated: {existing_log['metadata'].get('last_updated', 'Unknown')}")
        
        # Ask if user wants to update
        print("\n🔄 Updating with fresh scan...")
    
    # Perform fresh scan
    print("\n2️⃣ PERFORMING FRESH SCAN...")
    logger.scan_and_log_all_modules()
    
    print("\n✅ FULL MODULES CODE LOGGER READY!")
    print("=" * 60)
    print("📋 Usage:")
    print("   - Log file: full_modules_code_log.json")
    print("   - Database: workspace_activity.db") 
    print("   - All Python modules captured and indexed")
    print("   - Ready for operations and debugging")
    print("=" * 60)
    
    logger.close()
