#!/usr/bin/env python3
"""
🚀 LIGHTWEIGHT AUTO LOGGER INITIALIZER
====================================
Lightweight version that only runs the full modules code logger.
For testing and quick initialization without workspace monitoring.
"""

import os
import sys
import subprocess
import threading

# Global flag to prevent multiple initializations
_logger_initialized = False
_initialization_lock = threading.Lock()

def run_full_modules_logger_only():
    """Run only the full modules code logger (lightweight)"""
    try:
        workspace_path = os.getcwd()
        logger_script = os.path.join(workspace_path, "full_modules_code_logger.py")
        
        if not os.path.exists(logger_script):
            print(f"⚠️ Logger script not found: {logger_script}")
            return False
        
        print("🚀 AUTO-INITIALIZING FULL MODULES LOGGER (LIGHTWEIGHT)...")
        
        # Run the logger script
        result = subprocess.run([
            sys.executable, logger_script
        ], capture_output=True, text=True, cwd=workspace_path)
        
        if result.returncode == 0:
            print("✅ Full modules logger initialized successfully")
            print("📋 Master log updated: full_modules_code_log.json")
            print("🗄️ Database updated: workspace_activity.db")
            return True
        else:
            print(f"❌ Logger initialization failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Auto-logger error: {e}")
        return False

def lightweight_auto_initialize():
    """Initialize only the full modules code logger (lightweight)"""
    global _logger_initialized
    
    with _initialization_lock:
        if _logger_initialized:
            return True
        
        print("🔄 LIGHTWEIGHT AUTO-INIT: Full modules logger only")
        
        success = run_full_modules_logger_only()
        
        if success:
            print("✅ LIGHTWEIGHT LOGGING INITIALIZED")
        else:
            print("⚠️ Lightweight logging failed")
        
        _logger_initialized = True
        return success

# Auto-initialize on import (lightweight version)
if __name__ != "__main__":
    # Only auto-initialize when imported, not when run directly
    try:
        lightweight_auto_initialize()
    except Exception as e:
        print(f"⚠️ Lightweight auto-initialization failed: {e}")

if __name__ == "__main__":
    # Manual test mode
    print("🧪 TESTING LIGHTWEIGHT AUTO LOGGER INITIALIZER")
    print("="*50)
    
    success = lightweight_auto_initialize()
    
    if success:
        print("✅ Lightweight test completed successfully")
    else:
        print("❌ Lightweight test failed")
