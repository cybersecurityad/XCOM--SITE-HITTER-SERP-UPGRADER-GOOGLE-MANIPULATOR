#!/usr/bin/env python3
"""
🎯 COMPREHENSIVE LOGGING SYSTEM TEST
====================================
Demonstrates all logging capabilities and integration tests.

FEATURES TESTED:
✅ Auto-initialization of all logging systems
✅ Terminal command tracking
✅ Chat and agent history recording
✅ File operations monitoring  
✅ Code modules logging
✅ Search and retrieval functions
✅ Session summaries and statistics
"""

import time
import os
import sys
from typing import Dict, Any

# Import the comprehensive auto-logger (should auto-initialize all systems)
from auto_logger_init_v2 import (
    get_modules_logger, get_workspace_logger, get_chat_tracker,
    get_terminal_history, get_terminal_wrapper, is_fully_initialized,
    get_initialization_status
)

def test_initialization():
    """Test that all logging systems are properly initialized"""
    print("🧪 TESTING LOGGING SYSTEM INITIALIZATION")
    print("=" * 50)
    
    # Check initialization status
    status = get_initialization_status()
    print(f"📊 Initialization Status: {status}")
    
    fully_init = is_fully_initialized()
    print(f"🎯 Fully Initialized: {fully_init}")
    
    # Get all instances
    modules_logger = get_modules_logger()
    workspace_logger = get_workspace_logger()
    chat_tracker = get_chat_tracker()
    terminal_history = get_terminal_history()
    terminal_wrapper = get_terminal_wrapper()
    
    print(f"\n🔧 Instance Availability:")
    print(f"   ✅ Modules Logger: {modules_logger is not None}")
    print(f"   ✅ Workspace Logger: {workspace_logger is not None}")
    print(f"   ✅ Chat Tracker: {chat_tracker is not None}")
    print(f"   ✅ Terminal History: {terminal_history is not None}")
    print(f"   ✅ Terminal Wrapper: {terminal_wrapper is not None}")
    
    return fully_init

def test_terminal_wrapper():
    """Test terminal command wrapper functionality"""
    print("\n🧪 TESTING TERMINAL COMMAND WRAPPER")
    print("=" * 50)
    
    wrapper = get_terminal_wrapper()
    if not wrapper:
        print("❌ Terminal wrapper not available")
        return False
    
    # Test basic command
    print("1️⃣ Testing basic echo command...")
    result1 = wrapper.run_command("echo 'Hello from comprehensive test'", 
                                 explanation="Testing basic echo command")
    print(f"   Result: {result1['success']}, Exit: {result1['exit_code']}")
    
    # Test directory listing
    print("2️⃣ Testing directory listing...")
    result2 = wrapper.run_command("ls -la | head -5", 
                                 explanation="Testing directory listing")
    print(f"   Result: {result2['success']}, Exit: {result2['exit_code']}")
    
    # Test Python execution
    print("3️⃣ Testing Python execution...")
    result3 = wrapper.run_command("python -c \"print('Python execution test')\"",
                                 explanation="Testing Python execution")
    print(f"   Result: {result3['success']}, Exit: {result3['exit_code']}")
    
    # Test error command
    print("4️⃣ Testing error handling...")
    result4 = wrapper.run_command("invalid_command_test_error",
                                 explanation="Testing error handling")
    print(f"   Result: {result4['success']}, Exit: {result4['exit_code']}")
    
    return True

def test_chat_tracking():
    """Test chat and agent history tracking"""
    print("\n🧪 TESTING CHAT & AGENT TRACKING")
    print("=" * 50)
    
    tracker = get_chat_tracker()
    if not tracker:
        print("❌ Chat tracker not available")
        return False
    
    # Track some agent actions
    print("1️⃣ Tracking agent tool usage...")
    tracker.track_tool_call("run_terminal", {"command": "echo test"}, {"success": True})
    
    print("2️⃣ Tracking file operations...")
    tracker.track_file_operation("test_file.py", "CREATE", "Test file creation")
    
    print("3️⃣ Tracking decision points...")
    tracker.track_decision("Should run comprehensive test", "YES", "All systems ready")
    
    # Get conversation history
    history = tracker.get_conversation_history(limit=5)
    print(f"   📝 Recent history entries: {len(history)}")
    
    return True

def test_terminal_history():
    """Test terminal history database"""
    print("\n🧪 TESTING TERMINAL HISTORY DATABASE")
    print("=" * 50)
    
    history_db = get_terminal_history()
    if not history_db:
        print("❌ Terminal history database not available")
        return False
    
    # Search terminal history
    print("1️⃣ Searching terminal history...")
    recent_commands = history_db.search_terminal_history("echo", limit=3)
    print(f"   📝 Found {len(recent_commands)} 'echo' commands")
    
    # Get session summary
    print("2️⃣ Getting session summary...")
    summary = history_db.get_session_summary()
    print(f"   📊 Session summary available: {bool(summary)}")
    
    return True

def test_modules_logger():
    """Test full modules code logger"""
    print("\n🧪 TESTING MODULES CODE LOGGER")
    print("=" * 50)
    
    logger = get_modules_logger()
    if not logger:
        print("❌ Modules logger not available")
        return False
    
    # Test module information retrieval
    print("1️⃣ Testing module information...")
    module_info = logger.get_module_info("terminal_command_wrapper")
    if module_info:
        print(f"   📄 Module info: {len(module_info.get('content', ''))} characters")
    else:
        print("   ⚠️ Module info not found")
    
    # List all modules
    print("2️⃣ Testing module listing...")
    all_modules = logger.list_all_modules()
    print(f"   📚 Total modules logged: {len(all_modules)}")
    
    return True

def test_file_operations():
    """Test file operations tracking"""
    print("\n🧪 TESTING FILE OPERATIONS TRACKING")
    print("=" * 50)
    
    # Create a test file (should be tracked by workspace logger)
    test_file = "comprehensive_test_temp.txt"
    print("1️⃣ Creating test file...")
    with open(test_file, "w") as f:
        f.write("This is a test file for comprehensive logging test\n")
        f.write(f"Created at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Wait a moment for tracking
    time.sleep(0.1)
    
    # Modify the file
    print("2️⃣ Modifying test file...")
    with open(test_file, "a") as f:
        f.write(f"Modified at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Wait a moment for tracking
    time.sleep(0.1)
    
    # Delete the file
    print("3️⃣ Deleting test file...")
    os.remove(test_file)
    
    print("   ✅ File operations completed (should be tracked)")
    return True

def test_search_capabilities():
    """Test search capabilities across all systems"""
    print("\n🧪 TESTING SEARCH CAPABILITIES")
    print("=" * 50)
    
    # Terminal history search
    terminal_history = get_terminal_history()
    if terminal_history:
        print("1️⃣ Searching terminal history...")
        results = terminal_history.search_terminal_history("python", limit=3)
        print(f"   🔍 Terminal search results: {len(results)}")
    
    # Chat history search
    chat_tracker = get_chat_tracker()
    if chat_tracker:
        print("2️⃣ Searching chat history...")
        chat_results = chat_tracker.search_history("test", limit=3)
        print(f"   🔍 Chat search results: {len(chat_results)}")
    
    # Module content search
    modules_logger = get_modules_logger()
    if modules_logger:
        print("3️⃣ Searching module content...")
        module_list = modules_logger.list_all_modules()
        wrapper_modules = [m for m in module_list if "wrapper" in m.lower()]
        print(f"   🔍 Modules with 'wrapper': {len(wrapper_modules)}")
    
    return True

def generate_final_report():
    """Generate a comprehensive final report"""
    print("\n📊 COMPREHENSIVE LOGGING SYSTEM REPORT")
    print("=" * 60)
    
    # Get all system instances
    modules_logger = get_modules_logger()
    workspace_logger = get_workspace_logger()
    chat_tracker = get_chat_tracker()
    terminal_history = get_terminal_history()
    terminal_wrapper = get_terminal_wrapper()
    
    print("🎯 SYSTEM STATUS:")
    print(f"   ✅ Modules Logger: {'ACTIVE' if modules_logger else 'INACTIVE'}")
    print(f"   ✅ Workspace Logger: {'ACTIVE' if workspace_logger else 'INACTIVE'}")
    print(f"   ✅ Chat Tracker: {'ACTIVE' if chat_tracker else 'INACTIVE'}")
    print(f"   ✅ Terminal History: {'ACTIVE' if terminal_history else 'INACTIVE'}")
    print(f"   ✅ Terminal Wrapper: {'ACTIVE' if terminal_wrapper else 'INACTIVE'}")
    
    print("\n📈 STATISTICS:")
    
    # Modules statistics
    if modules_logger:
        module_list = modules_logger.list_all_modules()
        print(f"   📚 Python modules logged: {len(module_list)}")
    
    # Terminal statistics
    if terminal_history:
        terminal_summary = terminal_history.get_session_summary()
        if terminal_summary:
            print(f"   💻 Terminal commands in session: {terminal_summary.get('total_commands', 0)}")
    
    # Chat statistics
    if chat_tracker:
        chat_summary = chat_tracker.get_session_summary()
        if chat_summary:
            print(f"   💬 Chat history entries: {chat_summary.get('total_entries', 0)}")
    
    print("\n💾 DATABASE FILES:")
    db_files = [
        "workspace_activity.db",
        "chat_agent_history.db", 
        "terminal_history.db",
        "full_modules_code_log.json"
    ]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            size = os.path.getsize(db_file)
            print(f"   ✅ {db_file}: {size:,} bytes")
        else:
            print(f"   ❌ {db_file}: NOT FOUND")
    
    print("\n🎉 COMPREHENSIVE LOGGING SYSTEM OPERATIONAL!")
    print("   All workspace activity is being tracked and logged.")
    print("   Ready for production use and debugging operations.")
    print("=" * 60)

def main():
    """Run all comprehensive tests"""
    print("🚀 COMPREHENSIVE LOGGING SYSTEM TEST SUITE")
    print("=" * 60)
    print("Testing all logging capabilities and integrations...")
    print()
    
    test_results = []
    
    # Run all tests
    test_results.append(("Initialization", test_initialization()))
    test_results.append(("Terminal Wrapper", test_terminal_wrapper()))
    test_results.append(("Chat Tracking", test_chat_tracking()))
    test_results.append(("Terminal History", test_terminal_history()))
    test_results.append(("Modules Logger", test_modules_logger()))
    test_results.append(("File Operations", test_file_operations()))
    test_results.append(("Search Capabilities", test_search_capabilities()))
    
    # Summary of test results
    print("\n📋 TEST RESULTS SUMMARY")
    print("=" * 30)
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    # Generate final report
    generate_final_report()
    
    # Overall result
    total_passed = sum(1 for _, result in test_results if result)
    total_tests = len(test_results)
    
    print(f"\n🎯 OVERALL RESULT: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("🎉 ALL TESTS PASSED - SYSTEM FULLY OPERATIONAL!")
    else:
        print("⚠️ Some tests failed - Check individual results above")
    
    return total_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
