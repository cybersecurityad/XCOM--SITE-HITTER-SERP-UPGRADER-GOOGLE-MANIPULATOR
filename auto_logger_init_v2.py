#!/usr/bin/env python3
"""
🚀 AUTO LOGGER INITIALIZATION SYSTEM
=====================================
Comprehensive workspace logging system auto-initialization.
Activates ALL logging databases and tracking systems automatically on import.

FEATURES:
✅ Full modules code logger
✅ Workspace activity logger
✅ Chat & agent history database
✅ Terminal history database
✅ Terminal command wrapper
✅ Silent initialization (minimal output)
✅ Error handling and fallback
"""

import sys
import os
import time
from typing import Dict, Any, Optional, List

# Track initialization status
_initialization_status = {
    'full_modules_logger': False,
    'workspace_logger': False,
    'chat_agent_tracker': False,
    'terminal_history': False,
    'terminal_wrapper': False,
    'auto_init_completed': False
}

# Global instances
_logger_instances = {}

def initialize_full_modules_logger(verbose: bool = False, read_existing: bool = False) -> bool:
    """Initialize the full modules code logger"""
    try:
        from full_modules_code_logger import FullModulesCodeLogger
        logger = FullModulesCodeLogger()
        
        if read_existing:
            if verbose:
                print("📖 Reading existing modules log...")
            existing_log = logger.read_existing_log()
            if existing_log and verbose:
                print(f"   Found {existing_log['metadata']['total_modules']} existing modules")
        
        # Always do a fresh scan to update with any changes
        logger.scan_and_log_all_modules()
        _logger_instances['full_modules_logger'] = logger
        _initialization_status['full_modules_logger'] = True
        if verbose:
            print("✅ Full modules logger initialized")
        return True
    except Exception as e:
        if verbose:
            print(f"⚠️ Full modules logger failed: {e}")
        return False

def initialize_workspace_logger(verbose: bool = False) -> bool:
    """Initialize the workspace activity logger"""
    try:
        from workspace_logger import WorkspaceLogger
        logger = WorkspaceLogger()
        _logger_instances['workspace_logger'] = logger
        _initialization_status['workspace_logger'] = True
        if verbose:
            print("✅ Workspace logger initialized")
        return True
    except Exception as e:
        if verbose:
            print(f"⚠️ Workspace logger failed: {e}")
        return False

def initialize_chat_agent_tracker(verbose: bool = False, read_existing: bool = False) -> bool:
    """Initialize the chat & agent history tracker"""
    try:
        from auto_chat_tracker import get_auto_tracker
        tracker = get_auto_tracker()
        
        if read_existing and verbose:
            # Show existing conversation count
            try:
                if tracker.db:
                    history = tracker.db.search_history("", limit=5)
                    if history:
                        print(f"📖 Found {len(history)} recent chat history entries")
            except:
                pass
        
        if not tracker.conversation_active:
            tracker.start_conversation("Auto-initialized workspace session")
        _logger_instances['chat_agent_tracker'] = tracker
        _initialization_status['chat_agent_tracker'] = True
        if verbose:
            print("✅ Chat & agent tracker initialized")
        return True
    except Exception as e:
        if verbose:
            print(f"⚠️ Chat & agent tracker failed: {e}")
        return False

def initialize_terminal_history(verbose: bool = False, read_existing: bool = False) -> bool:
    """Initialize the terminal history database"""
    try:
        from terminal_history_db import get_terminal_history_db
        db = get_terminal_history_db(verbose=verbose)
        
        if read_existing and verbose:
            # Show existing terminal commands count
            try:
                recent_commands = db.search_terminal_history("", limit=5)
                if recent_commands:
                    print(f"📖 Found {len(recent_commands)} recent terminal commands")
            except:
                pass
        
        _logger_instances['terminal_history'] = db
        _initialization_status['terminal_history'] = True
        if verbose:
            print("✅ Terminal history database initialized")
        return True
    except Exception as e:
        if verbose:
            print(f"⚠️ Terminal history database failed: {e}")
        return False

def initialize_terminal_wrapper(verbose: bool = False) -> bool:
    """Initialize the terminal command wrapper"""
    try:
        from terminal_command_wrapper import get_terminal_wrapper
        wrapper = get_terminal_wrapper(verbose=verbose)
        _logger_instances['terminal_wrapper'] = wrapper
        _initialization_status['terminal_wrapper'] = True
        if verbose:
            print("✅ Terminal command wrapper initialized")
        return True
    except Exception as e:
        if verbose:
            print(f"⚠️ Terminal command wrapper failed: {e}")
        return False

def initialize_all_loggers(verbose: bool = False, read_existing: bool = False) -> Dict[str, bool]:
    """Initialize all logging systems"""
    
    if _initialization_status['auto_init_completed']:
        if verbose:
            print("🔄 Auto-logger already initialized, skipping...")
        return _initialization_status.copy()
    
    if verbose:
        print("🚀 INITIALIZING COMPREHENSIVE LOGGING SYSTEM")
        if read_existing:
            print("📖 Reading existing logs during initialization...")
        print("=" * 55)
    
    # Initialize each logging system
    results = {}
    
    # 1. Full modules code logger
    results['full_modules_logger'] = initialize_full_modules_logger(verbose, read_existing)
    
    # 2. Workspace activity logger
    results['workspace_logger'] = initialize_workspace_logger(verbose)
    
    # 3. Chat & agent history tracker
    results['chat_agent_tracker'] = initialize_chat_agent_tracker(verbose, read_existing)
    
    # 4. Terminal history database
    results['terminal_history'] = initialize_terminal_history(verbose, read_existing)
    
    # 5. Terminal command wrapper
    results['terminal_wrapper'] = initialize_terminal_wrapper(verbose)
    
    # Mark initialization as completed
    _initialization_status['auto_init_completed'] = True
    
    # Summary
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    if verbose:
        print("=" * 55)
        print(f"📊 INITIALIZATION COMPLETE: {successful}/{total} systems active")
        if read_existing:
            print("📖 Existing logs have been read and loaded")
        if successful == total:
            print("✅ ALL LOGGING SYSTEMS OPERATIONAL")
        else:
            print("⚠️ Some systems failed to initialize")
        print("=" * 55)
    
    return results

def get_logger_instance(logger_name: str) -> Optional[Any]:
    """Get a specific logger instance"""
    return _logger_instances.get(logger_name)

def get_initialization_status() -> Dict[str, bool]:
    """Get the current initialization status"""
    return _initialization_status.copy()

def is_fully_initialized() -> bool:
    """Check if all logging systems are initialized"""
    return all([
        _initialization_status['full_modules_logger'],
        _initialization_status['workspace_logger'],
        _initialization_status['chat_agent_tracker'],
        _initialization_status['terminal_history'],
        _initialization_status['terminal_wrapper']
    ])

# Convenience functions to get specific loggers
def get_modules_logger():
    """Get the full modules logger instance"""
    return get_logger_instance('full_modules_logger')

def get_workspace_logger():
    """Get the workspace logger instance"""
    return get_logger_instance('workspace_logger')

def get_chat_tracker():
    """Get the chat & agent tracker instance"""
    return get_logger_instance('chat_agent_tracker')

def get_terminal_history():
    """Get the terminal history database instance"""
    return get_logger_instance('terminal_history')

def get_terminal_wrapper():
    """Get the terminal command wrapper instance"""
    return get_logger_instance('terminal_wrapper')

# New functions for reading existing logs
def read_all_existing_logs(verbose: bool = True) -> Dict[str, Any]:
    """Read all existing logs from all systems"""
    logs = {}
    
    if verbose:
        print("📖 READING ALL EXISTING LOGS")
        print("=" * 40)
    
    # Read modules log
    try:
        modules_logger = get_modules_logger()
        if modules_logger:
            existing_log = modules_logger.read_existing_log()
            if existing_log:
                logs['modules'] = existing_log
                if verbose:
                    print(f"📚 Modules: {existing_log['metadata']['total_modules']} files")
    except Exception as e:
        if verbose:
            print(f"⚠️ Modules log read failed: {e}")
    
    # Read terminal history
    try:
        terminal_history = get_terminal_history()
        if terminal_history:
            recent_commands = terminal_history.search_terminal_history("", limit=100)
            if recent_commands:
                logs['terminal'] = recent_commands
                if verbose:
                    print(f"💻 Terminal: {len(recent_commands)} recent commands")
    except Exception as e:
        if verbose:
            print(f"⚠️ Terminal history read failed: {e}")
    
    # Read chat history
    try:
        chat_tracker = get_chat_tracker()
        if chat_tracker and chat_tracker.db:
            chat_history = chat_tracker.db.search_history("", limit=100)
            if chat_history:
                logs['chat'] = chat_history
                if verbose:
                    print(f"💬 Chat: {len(chat_history)} history entries")
    except Exception as e:
        if verbose:
            print(f"⚠️ Chat history read failed: {e}")
    
    # Read workspace activity
    try:
        workspace_logger = get_workspace_logger()
        if workspace_logger and hasattr(workspace_logger, 'get_recent_activity'):
            activity = workspace_logger.get_recent_activity(limit=100)
            if activity:
                logs['workspace'] = activity
                if verbose:
                    print(f"🔍 Workspace: {len(activity)} recent activities")
    except Exception as e:
        if verbose:
            print(f"⚠️ Workspace activity read failed: {e}")
    
    if verbose:
        print("=" * 40)
        print(f"📊 Total log categories read: {len(logs)}")
    
    return logs

def search_all_logs(query: str, limit: int = 20, verbose: bool = True) -> Dict[str, List]:
    """Search across all logging systems"""
    results = {}
    
    if verbose:
        print(f"🔍 SEARCHING ALL LOGS FOR: '{query}'")
        print("=" * 50)
    
    # Search terminal history
    try:
        terminal_history = get_terminal_history()
        if terminal_history:
            terminal_results = terminal_history.search_terminal_history(query, limit)
            if terminal_results:
                results['terminal'] = terminal_results
                if verbose:
                    print(f"💻 Terminal: {len(terminal_results)} matches")
    except Exception as e:
        if verbose:
            print(f"⚠️ Terminal search failed: {e}")
    
    # Search chat history
    try:
        chat_tracker = get_chat_tracker()
        if chat_tracker and chat_tracker.db:
            chat_results = chat_tracker.db.search_history(query, limit)
            if chat_results:
                results['chat'] = chat_results
                if verbose:
                    print(f"💬 Chat: {len(chat_results)} matches")
    except Exception as e:
        if verbose:
            print(f"⚠️ Chat search failed: {e}")
    
    # Search modules
    try:
        modules_logger = get_modules_logger()
        if modules_logger:
            module_list = modules_logger.list_all_modules()
            module_matches = [m for m in module_list if query.lower() in m.lower()]
            if module_matches:
                results['modules'] = module_matches
                if verbose:
                    print(f"📚 Modules: {len(module_matches)} matches")
    except Exception as e:
        if verbose:
            print(f"⚠️ Module search failed: {e}")
    
    if verbose:
        print("=" * 50)
        total_matches = sum(len(matches) for matches in results.values())
        print(f"📊 Total matches found: {total_matches}")
    
    return results

def get_comprehensive_summary(verbose: bool = True) -> Dict[str, Any]:
    """Get a comprehensive summary of all logging systems"""
    summary = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'systems': {},
        'totals': {}
    }
    
    if verbose:
        print("📊 COMPREHENSIVE LOGGING SUMMARY")
        print("=" * 45)
    
    # Modules summary
    try:
        modules_logger = get_modules_logger()
        if modules_logger:
            existing_log = modules_logger.read_existing_log()
            if existing_log:
                summary['systems']['modules'] = existing_log['metadata']
                if verbose:
                    print(f"📚 Modules: {existing_log['metadata']['total_modules']} files, {existing_log['metadata']['total_lines']} lines")
    except:
        pass
    
    # Terminal summary
    try:
        terminal_history = get_terminal_history()
        if terminal_history:
            terminal_summary = terminal_history.get_session_summary()
            if terminal_summary:
                summary['systems']['terminal'] = terminal_summary
                if verbose:
                    print(f"💻 Terminal: {terminal_summary.get('total_commands', 0)} commands")
    except:
        pass
    
    # Chat summary
    try:
        chat_tracker = get_chat_tracker()
        if chat_tracker and chat_tracker.db:
            chat_summary = chat_tracker.db.get_session_summary()
            if chat_summary:
                summary['systems']['chat'] = chat_summary
                if verbose:
                    print(f"💬 Chat: {chat_summary.get('total_entries', 0)} entries")
    except:
        pass
    
    # Calculate totals
    summary['totals']['active_systems'] = len(summary['systems'])
    summary['totals']['fully_initialized'] = is_fully_initialized()
    
    if verbose:
        print("=" * 45)
        print(f"🎯 Active systems: {summary['totals']['active_systems']}/5")
        print(f"✅ Fully initialized: {summary['totals']['fully_initialized']}")
    
    return summary

# Auto-initialize when module is imported
try:
    # Silent initialization by default
    _auto_init_results = initialize_all_loggers(verbose=False)
    
    # Only show status if there are failures
    failed_systems = [name for name, success in _auto_init_results.items() if not success]
    if failed_systems:
        print(f"⚠️ Auto-logger: {len(failed_systems)} systems failed: {', '.join(failed_systems)}")
    
except Exception as e:
    print(f"❌ Auto-logger initialization failed: {e}")

if __name__ == "__main__":
    # Verbose test when run directly
    print("🧪 TESTING AUTO LOGGER INITIALIZATION")
    print("=" * 50)
    
    # Test initialization
    results = initialize_all_loggers(verbose=True)
    
    # Test status checks
    status = get_initialization_status()
    print(f"\n📊 Status check: {status}")
    
    fully_init = is_fully_initialized()
    print(f"🎯 Fully initialized: {fully_init}")
    
    # Test instance retrieval
    modules_logger = get_modules_logger()
    workspace_logger = get_workspace_logger()
    chat_tracker = get_chat_tracker()
    terminal_history = get_terminal_history()
    terminal_wrapper = get_terminal_wrapper()
    
    print(f"\n🔧 Instance availability:")
    print(f"   Modules logger: {modules_logger is not None}")
    print(f"   Workspace logger: {workspace_logger is not None}")
    print(f"   Chat tracker: {chat_tracker is not None}")
    print(f"   Terminal history: {terminal_history is not None}")
    print(f"   Terminal wrapper: {terminal_wrapper is not None}")
    
    print("\n✅ Auto-logger initialization test completed")
