#!/usr/bin/env python3
"""
🎯 AUTOMATIC CHAT & AGENT TRACKER
=================================
Automatically tracks all chat interactions and agent tool calls.
This module wraps around the chat_agent_history_db to provide seamless logging.

FEATURES:
✅ Auto-tracks user messages and agent responses
✅ Monitors all tool calls and results
✅ Captures file operations and terminal commands
✅ Records conversation context and timeline
✅ Provides search and analysis capabilities
"""

import functools
import time
import json
import os
from typing import Any, Dict, List, Optional, Callable, Union
from datetime import datetime

# Import the chat history database
try:
    from chat_agent_history_db import (
        get_chat_agent_db, log_user_message, log_agent_message, 
        log_tool_usage, log_file_change, log_terminal_activity
    )
    CHAT_DB_AVAILABLE = True
except ImportError:
    CHAT_DB_AVAILABLE = False
    print("⚠️ Chat history database not available")

class AutoChatTracker:
    """Automatic chat and agent interaction tracker"""
    
    def __init__(self):
        self.conversation_active = False
        self.current_user_message = None
        self.agent_response_start = None
        
        if CHAT_DB_AVAILABLE:
            self.db = get_chat_agent_db()
            print("🎯 Auto Chat Tracker initialized")
        else:
            self.db = None
            print("⚠️ Auto Chat Tracker disabled (no database)")
    
    def start_conversation(self, topic: Optional[str] = None):
        """Start tracking a new conversation"""
        if self.db:
            self.conversation_active = True
            self.db.start_conversation(topic or "Auto-tracked conversation")
            print(f"🗨️ Started tracking conversation: {topic or 'General'}")
    
    def track_user_message(self, content: str, attachments: Optional[List[str]] = None):
        """Track a user message"""
        if self.db and self.conversation_active:
            self.current_user_message = content
            log_user_message(content, attachments)
            print(f"👤 Tracked user message ({len(content)} chars)")
    
    def start_agent_response(self):
        """Mark the start of an agent response"""
        if self.db and self.conversation_active:
            self.agent_response_start = time.time()
    
    def track_agent_response(self, content: str):
        """Track an agent response"""
        if self.db and self.conversation_active:
            response_time = None
            if self.agent_response_start:
                response_time = int((time.time() - self.agent_response_start) * 1000)
                self.agent_response_start = None
            
            log_agent_message(content, response_time)
            print(f"🤖 Tracked agent response ({len(content)} chars, {response_time}ms)")
    
    def track_tool_call(self, tool_name: str, parameters: Optional[Dict] = None, 
                       result: Optional[str] = None, success: bool = True, 
                       error: Optional[str] = None, files: Optional[List[str]] = None):
        """Track a tool call"""
        if self.db and self.conversation_active:
            log_tool_usage(tool_name, parameters, result, success, error, files)
    
    def track_file_operation(self, operation: str, file_path: str, 
                           tool: Optional[str] = None, summary: Optional[str] = None):
        """Track a file operation"""
        if self.db and self.conversation_active:
            log_file_change(operation, file_path, tool, summary)
    
    def track_terminal_command(self, command: str, explanation: Optional[str] = None, 
                             output: Optional[str] = None, exit_code: Optional[int] = None):
        """Track a terminal command"""
        if self.db and self.conversation_active:
            log_terminal_activity(command, explanation, output, exit_code)

# Global tracker instance
_auto_tracker = None

def get_auto_tracker() -> AutoChatTracker:
    """Get the global auto tracker instance"""
    global _auto_tracker
    if _auto_tracker is None:
        _auto_tracker = AutoChatTracker()
    return _auto_tracker

def track_user_input(content: str, attachments: Optional[List[str]] = None):
    """Track user input"""
    tracker = get_auto_tracker()
    if not tracker.conversation_active:
        tracker.start_conversation("Auto-detected conversation")
    tracker.track_user_message(content, attachments)

def track_agent_output(content: str):
    """Track agent output"""
    tracker = get_auto_tracker()
    tracker.track_agent_response(content)

def track_function_call(func_name: str, args: Optional[Dict] = None, result: Any = None, 
                       success: bool = True, error: Optional[str] = None):
    """Track a function call"""
    tracker = get_auto_tracker()
    
    # Convert result to string for logging
    result_str = None
    if result is not None:
        try:
            if isinstance(result, (dict, list)):
                result_str = json.dumps(result, indent=2)[:1000]  # Limit size
            else:
                result_str = str(result)[:1000]  # Limit size
        except:
            result_str = f"<{type(result).__name__} object>"
    
    tracker.track_tool_call(func_name, args, result_str, success, error)

def auto_track_tool_calls(func: Callable) -> Callable:
    """Decorator to automatically track tool calls"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        success = True
        error_msg = None
        result = None
        
        try:
            # Extract parameters
            params = {}
            if args:
                params['args'] = args
            if kwargs:
                params.update(kwargs)
            
            # Call the function
            result = func(*args, **kwargs)
            
        except Exception as e:
            success = False
            error_msg = str(e)
            raise
        finally:
            # Track the call
            execution_time = int((time.time() - start_time) * 1000)
            
            track_function_call(
                func.__name__, 
                params, 
                result, 
                success, 
                error_msg
            )
        
        return result
    return wrapper

# Common tool tracking functions
def track_create_file(file_path: str, content: str, success: bool = True):
    """Track file creation"""
    tracker = get_auto_tracker()
    tracker.track_file_operation("CREATE", file_path, "create_file", 
                                f"Created {len(content)} characters")
    tracker.track_tool_call("create_file", 
                           {"file_path": file_path, "content_length": len(content)},
                           f"File created successfully" if success else "File creation failed",
                           success)

def track_edit_file(file_path: str, old_content: str, new_content: str, success: bool = True):
    """Track file editing"""
    tracker = get_auto_tracker()
    tracker.track_file_operation("EDIT", file_path, "replace_string_in_file",
                                f"Changed {len(old_content)} to {len(new_content)} characters")
    tracker.track_tool_call("replace_string_in_file",
                           {"file_path": file_path, "old_length": len(old_content), "new_length": len(new_content)},
                           f"File edited successfully" if success else "File edit failed",
                           success)

def track_read_file(file_path: str, content_length: int, success: bool = True):
    """Track file reading"""
    tracker = get_auto_tracker()
    tracker.track_file_operation("READ", file_path, "read_file",
                                f"Read {content_length} characters")
    tracker.track_tool_call("read_file",
                           {"file_path": file_path},
                           f"Read {content_length} characters" if success else "File read failed",
                           success)

def track_terminal_execution(command: str, output: Optional[str] = None, exit_code: Optional[int] = None, 
                           explanation: Optional[str] = None):
    """Track terminal command execution"""
    tracker = get_auto_tracker()
    tracker.track_terminal_command(command, explanation, output, exit_code)
    tracker.track_tool_call("run_in_terminal",
                           {"command": command, "explanation": explanation},
                           f"Exit code: {exit_code}, Output length: {len(output) if output else 0}",
                           exit_code == 0 if exit_code is not None else True)

# Context manager for tracking conversations
class ConversationTracker:
    """Context manager for tracking conversations"""
    
    def __init__(self, topic: Optional[str] = None):
        self.topic = topic
        self.tracker = get_auto_tracker()
    
    def __enter__(self):
        self.tracker.start_conversation(self.topic)
        return self.tracker
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.tracker.track_agent_response(f"Conversation ended with error: {exc_val}")
        else:
            self.tracker.track_agent_response("Conversation completed successfully")

# Auto-detect and track based on current environment
def auto_detect_and_track():
    """Auto-detect current context and start tracking"""
    tracker = get_auto_tracker()
    
    # Check if we're in a VS Code environment
    if os.environ.get('VSCODE_PID'):
        tracker.start_conversation("VS Code session")
    
    # Check if we're running a specific script
    import sys
    if len(sys.argv) > 0:
        script_name = os.path.basename(sys.argv[0])
        if script_name != 'python':
            tracker.start_conversation(f"Script execution: {script_name}")
    
    # Default conversation
    if not tracker.conversation_active:
        tracker.start_conversation("General workspace activity")

if __name__ == "__main__":
    # Test the auto tracker
    print("🧪 TESTING AUTO CHAT TRACKER")
    print("="*40)
    
    tracker = get_auto_tracker()
    
    # Test conversation tracking
    with ConversationTracker("Testing Auto Tracker"):
        track_user_input("Test user message")
        tracker.start_agent_response()
        time.sleep(0.1)  # Simulate processing time
        track_agent_output("Test agent response")
        
        # Test tool tracking
        track_create_file("test_file.py", "print('hello')", True)
        track_terminal_execution("echo 'test'", "test", 0, "Testing echo command")
    
    print("✅ Auto Chat Tracker test completed")
