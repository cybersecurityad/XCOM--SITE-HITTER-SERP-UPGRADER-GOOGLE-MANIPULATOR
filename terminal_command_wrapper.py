#!/usr/bin/env python3
"""
🔄 TERMINAL COMMAND WRAPPER
===========================
Automatic terminal command tracking and integration wrapper.
Captures all terminal activity and integrates with the comprehensive logging system.

FEATURES:
✅ Automatic command tracking on execution
✅ Real-time output capture (stdout/stderr)
✅ Error detection and verbose logging
✅ Integration with chat & agent history
✅ Process monitoring and resource tracking
✅ Command pattern analysis
✅ Search and debugging capabilities
"""

import subprocess
import threading
import time
import os
import sys
import json
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

# Import terminal history and chat tracking
try:
    from terminal_history_db import (
        get_terminal_history_db, log_terminal_command, 
        log_terminal_output, log_terminal_completion, log_terminal_error
    )
    TERMINAL_DB_AVAILABLE = True
except ImportError:
    TERMINAL_DB_AVAILABLE = False
    print("⚠️ Terminal history database not available")

try:
    from auto_chat_tracker import get_auto_tracker, track_terminal_execution
    CHAT_TRACKER_AVAILABLE = True
except ImportError:
    CHAT_TRACKER_AVAILABLE = False
    print("⚠️ Chat tracker not available")

class TerminalCommandWrapper:
    """Wrapper for terminal commands with comprehensive logging"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.active_commands = {}
        
        # Initialize terminal database
        if TERMINAL_DB_AVAILABLE:
            self.terminal_db = get_terminal_history_db(verbose=False)
            print("💻 Terminal Command Wrapper initialized")
        else:
            self.terminal_db = None
            print("⚠️ Terminal Command Wrapper disabled (no database)")
        
        # Initialize chat tracker
        if CHAT_TRACKER_AVAILABLE:
            self.chat_tracker = get_auto_tracker()
            if not self.chat_tracker.conversation_active:
                self.chat_tracker.start_conversation("Terminal session")
        else:
            self.chat_tracker = None
    
    def run_command(self, command: str, working_dir: Optional[str] = None,
                   capture_output: bool = True, timeout: Optional[float] = None,
                   explanation: Optional[str] = None, is_background: bool = False) -> Dict[str, Any]:
        """Run a command with comprehensive tracking"""
        
        working_dir = working_dir or os.getcwd()
        start_time = time.time()
        
        # Start command tracking
        command_id = None
        if self.terminal_db:
            command_id = self.terminal_db.log_command_start(
                command, working_dir, is_background
            )
        
        if self.verbose:
            print(f"🚀 Executing: {command}")
            print(f"📁 Working dir: {working_dir}")
            if explanation:
                print(f"💡 Purpose: {explanation}")
        
        try:
            # Prepare environment
            env = os.environ.copy()
            
            # Run command
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=working_dir,
                stdout=subprocess.PIPE if capture_output else None,
                stderr=subprocess.PIPE if capture_output else None,
                text=True,
                env=env
            )
            
            # Update command with process ID
            if self.terminal_db and command_id:
                self.terminal_db.active_commands[command_id]['process_id'] = process.pid
            
            stdout_output = ""
            stderr_output = ""
            output_sequence = 0
            
            if capture_output:
                # Real-time output capture
                stdout_lines = []
                stderr_lines = []
                
                def read_stdout():
                    nonlocal stdout_output, output_sequence
                    if process.stdout:
                        for line in iter(process.stdout.readline, ''):
                            stdout_lines.append(line)
                            stdout_output += line
                            
                            # Log output chunk
                            if self.terminal_db and command_id:
                                self.terminal_db.log_command_output(
                                    command_id, "STDOUT", line, output_sequence
                                )
                                output_sequence += 1
                            
                            if self.verbose and line.strip():
                                print(f"📤 {line.rstrip()}")
                
                def read_stderr():
                    nonlocal stderr_output, output_sequence
                    if process.stderr:
                        for line in iter(process.stderr.readline, ''):
                            stderr_lines.append(line)
                            stderr_output += line
                            
                            # Log error output
                            if self.terminal_db and command_id:
                                self.terminal_db.log_command_output(
                                    command_id, "STDERR", line, output_sequence
                                )
                                output_sequence += 1
                            
                            if self.verbose and line.strip():
                                print(f"⚠️ {line.rstrip()}")
                
                # Start output reading threads
                stdout_thread = threading.Thread(target=read_stdout)
                stderr_thread = threading.Thread(target=read_stderr)
                
                stdout_thread.start()
                stderr_thread.start()
                
                # Wait for completion
                try:
                    exit_code = process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    process.kill()
                    exit_code = -1
                    error_msg = f"Command timeout after {timeout} seconds"
                    
                    if self.terminal_db and command_id:
                        self.terminal_db.log_terminal_error(
                            command_id, "TIMEOUT", error_msg, -1, "SYSTEM"
                        )
                    
                    if self.verbose:
                        print(f"⏰ Command timed out after {timeout} seconds")
                
                # Wait for output threads
                stdout_thread.join(timeout=1)
                stderr_thread.join(timeout=1)
                
            else:
                # Just wait for completion without capturing output
                try:
                    exit_code = process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    process.kill()
                    exit_code = -1
            
            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Log command completion
            if self.terminal_db and command_id:
                error_message = stderr_output if stderr_output and exit_code != 0 else None
                self.terminal_db.log_command_completion(
                    command_id, exit_code, error_message=error_message
                )
                
                # Detect file operations
                self.terminal_db.detect_file_operations(command, command_id)
            
            # Track with chat system
            if self.chat_tracker:
                track_terminal_execution(
                    command, stdout_output + stderr_output, exit_code, explanation
                )
            
            # Create result
            result = {
                'command': command,
                'command_id': command_id,
                'exit_code': exit_code,
                'execution_time_ms': execution_time_ms,
                'stdout': stdout_output,
                'stderr': stderr_output,
                'working_dir': working_dir,
                'process_id': process.pid,
                'success': exit_code == 0,
                'explanation': explanation
            }
            
            if self.verbose:
                status = "✅" if exit_code == 0 else "❌"
                print(f"{status} Command completed: {exit_code} ({execution_time_ms}ms)")
                if stderr_output and exit_code != 0:
                    print(f"❌ Error: {stderr_output.strip()}")
            
            return result
            
        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            error_msg = str(e)
            
            # Log execution error
            if self.terminal_db and command_id:
                self.terminal_db.log_terminal_error(
                    command_id, "EXECUTION_ERROR", error_msg, -1, "SYSTEM"
                )
                self.terminal_db.log_command_completion(
                    command_id, -1, error_message=error_msg
                )
            
            if self.verbose:
                print(f"❌ Command execution failed: {error_msg}")
            
            return {
                'command': command,
                'command_id': command_id,
                'exit_code': -1,
                'execution_time_ms': execution_time_ms,
                'stdout': "",
                'stderr': error_msg,
                'working_dir': working_dir,
                'process_id': None,
                'success': False,
                'explanation': explanation,
                'error': error_msg
            }
    
    def run_background_command(self, command: str, working_dir: Optional[str] = None,
                             explanation: Optional[str] = None) -> Dict[str, Any]:
        """Run a command in the background with tracking"""
        return self.run_command(
            command, working_dir, capture_output=False, 
            explanation=explanation, is_background=True
        )
    
    def run_python_script(self, script_path: str, args: Optional[List[str]] = None,
                         working_dir: Optional[str] = None,
                         explanation: Optional[str] = None) -> Dict[str, Any]:
        """Run a Python script with tracking"""
        python_cmd = sys.executable
        args = args or []
        command = f"{python_cmd} {script_path} {' '.join(args)}"
        
        return self.run_command(
            command, working_dir, 
            explanation=explanation or f"Running Python script: {script_path}"
        )
    
    def run_with_input(self, command: str, input_data: str,
                      working_dir: Optional[str] = None,
                      explanation: Optional[str] = None) -> Dict[str, Any]:
        """Run a command with input data"""
        
        working_dir = working_dir or os.getcwd()
        start_time = time.time()
        
        # Start command tracking
        command_id = None
        if self.terminal_db:
            command_id = self.terminal_db.log_command_start(command, working_dir)
        
        if self.verbose:
            print(f"🚀 Executing with input: {command}")
            print(f"📝 Input data: {input_data[:100]}{'...' if len(input_data) > 100 else ''}")
        
        try:
            # Run command with input
            process = subprocess.run(
                command,
                shell=True,
                cwd=working_dir,
                input=input_data,
                capture_output=True,
                text=True
            )
            
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Log input
            if self.terminal_db and command_id:
                self.terminal_db.log_command_output(command_id, "STDIN", input_data, 0)
                self.terminal_db.log_command_output(command_id, "STDOUT", process.stdout, 1)
                if process.stderr:
                    self.terminal_db.log_command_output(command_id, "STDERR", process.stderr, 2)
                
                error_message = process.stderr if process.stderr and process.returncode != 0 else None
                self.terminal_db.log_command_completion(
                    command_id, process.returncode, error_message=error_message
                )
            
            result = {
                'command': command,
                'command_id': command_id,
                'exit_code': process.returncode,
                'execution_time_ms': execution_time_ms,
                'stdout': process.stdout,
                'stderr': process.stderr,
                'working_dir': working_dir,
                'success': process.returncode == 0,
                'explanation': explanation,
                'input_data': input_data
            }
            
            if self.verbose:
                status = "✅" if process.returncode == 0 else "❌"
                print(f"{status} Command with input completed: {process.returncode} ({execution_time_ms}ms)")
            
            return result
            
        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            error_msg = str(e)
            
            if self.terminal_db and command_id:
                self.terminal_db.log_terminal_error(
                    command_id, "EXECUTION_ERROR", error_msg, -1, "SYSTEM"
                )
            
            if self.verbose:
                print(f"❌ Command with input failed: {error_msg}")
            
            return {
                'command': command,
                'command_id': command_id,
                'exit_code': -1,
                'execution_time_ms': execution_time_ms,
                'stdout': "",
                'stderr': error_msg,
                'working_dir': working_dir,
                'success': False,
                'explanation': explanation,
                'input_data': input_data,
                'error': error_msg
            }
    
    def get_command_history(self, limit: int = 10) -> List[Dict]:
        """Get recent command history"""
        if not self.terminal_db:
            return []
        
        return self.terminal_db.search_terminal_history("", limit)
    
    def search_commands(self, query: str, limit: int = 20) -> List[Dict]:
        """Search command history"""
        if not self.terminal_db:
            return []
        
        return self.terminal_db.search_terminal_history(query, limit)
    
    def get_session_stats(self) -> Dict:
        """Get session statistics"""
        if not self.terminal_db:
            return {}
        
        return self.terminal_db.get_session_summary()

# Global terminal wrapper instance
_terminal_wrapper = None

def get_terminal_wrapper(verbose: bool = True) -> TerminalCommandWrapper:
    """Get the global terminal wrapper instance"""
    global _terminal_wrapper
    if _terminal_wrapper is None:
        _terminal_wrapper = TerminalCommandWrapper(verbose=verbose)
    return _terminal_wrapper

def run_terminal_command(command: str, working_dir: Optional[str] = None,
                        explanation: Optional[str] = None, timeout: Optional[float] = None) -> Dict[str, Any]:
    """Run a terminal command with full tracking"""
    wrapper = get_terminal_wrapper()
    return wrapper.run_command(command, working_dir, explanation=explanation, timeout=timeout)

def run_python_script(script_path: str, args: Optional[List[str]] = None, 
                     working_dir: Optional[str] = None) -> Dict[str, Any]:
    """Run a Python script with tracking"""
    wrapper = get_terminal_wrapper()
    return wrapper.run_python_script(script_path, args, working_dir)

def run_background_command(command: str, working_dir: Optional[str] = None,
                          explanation: Optional[str] = None) -> Dict[str, Any]:
    """Run a background command with tracking"""
    wrapper = get_terminal_wrapper()
    return wrapper.run_background_command(command, working_dir, explanation)

def search_terminal_history(query: str, limit: int = 20) -> List[Dict]:
    """Search terminal command history"""
    wrapper = get_terminal_wrapper()
    return wrapper.search_commands(query, limit)

if __name__ == "__main__":
    # Test the terminal wrapper
    print("🧪 TESTING TERMINAL COMMAND WRAPPER")
    print("="*50)
    
    wrapper = TerminalCommandWrapper(verbose=True)
    
    # Test basic command
    result1 = wrapper.run_command("echo 'Hello from terminal wrapper'", 
                                 explanation="Testing basic echo command")
    print(f"Result 1: {result1['success']}, Exit: {result1['exit_code']}")
    
    # Test command with error
    result2 = wrapper.run_command("invalid_command_test", 
                                 explanation="Testing error handling")
    print(f"Result 2: {result2['success']}, Exit: {result2['exit_code']}")
    
    # Test Python script
    test_script = "print('Hello from Python script')"
    with open("test_script.py", "w") as f:
        f.write(test_script)
    
    result3 = wrapper.run_python_script("test_script.py")
    print(f"Result 3: {result3['success']}, Exit: {result3['exit_code']}")
    
    # Clean up
    os.remove("test_script.py")
    
    # Test search
    history = wrapper.search_commands("echo")
    print(f"Search results: {len(history)}")
    
    # Get stats
    stats = wrapper.get_session_stats()
    print(f"Session stats available: {bool(stats)}")
    
    print("✅ Terminal Command Wrapper test completed")
