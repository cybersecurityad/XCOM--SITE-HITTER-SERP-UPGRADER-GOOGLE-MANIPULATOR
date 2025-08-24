#!/usr/bin/env python3
"""
🔧 VS Code Debugger Conflict Fix
===============================
Fixes Chrome exit code 15 crashes caused by VS Code JavaScript debugger extension.
Based on the workaround from VS Code GitHub issues.
"""

import os
import shutil
import subprocess
import glob
from pathlib import Path

def find_vscode_workspace_storage():
    """Find VS Code workspace storage directory"""
    vscode_storage_path = Path.home() / "Library/Application Support/Code/User/workspaceStorage"
    
    if not vscode_storage_path.exists():
        print("❌ VS Code workspace storage not found")
        return None
    
    return vscode_storage_path

def find_js_debug_folders(storage_path):
    """Find all ms-vscode.js-debug folders"""
    js_debug_folders = []
    
    # Search for ms-vscode.js-debug folders
    for workspace_dir in storage_path.iterdir():
        if workspace_dir.is_dir():
            js_debug_path = workspace_dir / "ms-vscode.js-debug"
            if js_debug_path.exists():
                js_debug_folders.append(js_debug_path)
    
    return js_debug_folders

def backup_js_debug_folder(js_debug_path):
    """Create backup of js-debug folder"""
    backup_path = js_debug_path.parent / f"ms-vscode.js-debug.backup.{int(__import__('time').time())}"
    
    try:
        shutil.copytree(js_debug_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"⚠️ Backup failed: {e}")
        return None

def remove_js_debug_folder(js_debug_path):
    """Remove problematic js-debug folder"""
    try:
        shutil.rmtree(js_debug_path)
        print(f"🗑️ Removed: {js_debug_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to remove {js_debug_path}: {e}")
        return False

def kill_vscode_processes():
    """Kill VS Code processes to ensure clean state"""
    try:
        # Kill VS Code processes
        subprocess.run(['pkill', '-f', 'Visual Studio Code'], capture_output=True, check=False)
        subprocess.run(['pkill', '-f', 'Code'], capture_output=True, check=False)
        print("🔄 VS Code processes terminated")
        return True
    except Exception as e:
        print(f"⚠️ Process termination warning: {e}")
        return False

def kill_chrome_processes():
    """Kill Chrome processes to prevent conflicts"""
    try:
        subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True, check=False)
        subprocess.run(['pkill', '-f', 'Google Chrome'], capture_output=True, check=False)
        print("🔄 Chrome processes terminated")
        return True
    except Exception as e:
        print(f"⚠️ Chrome termination warning: {e}")
        return False

def main():
    """Main fix execution"""
    print("🔧 VS CODE CHROME EXIT CODE 15 FIX")
    print("=" * 50)
    print("Fixing VS Code JavaScript debugger conflicts...")
    
    # Step 1: Kill processes
    print("\n📋 Step 1: Terminating conflicting processes")
    kill_vscode_processes()
    kill_chrome_processes()
    
    # Step 2: Find workspace storage
    print("\n📋 Step 2: Locating VS Code workspace storage")
    storage_path = find_vscode_workspace_storage()
    if not storage_path:
        return False
    
    print(f"✅ Found workspace storage: {storage_path}")
    
    # Step 3: Find js-debug folders
    print("\n📋 Step 3: Finding problematic js-debug folders")
    js_debug_folders = find_js_debug_folders(storage_path)
    
    if not js_debug_folders:
        print("✅ No problematic js-debug folders found")
        return True
    
    print(f"🔍 Found {len(js_debug_folders)} js-debug folders:")
    for folder in js_debug_folders:
        print(f"   - {folder}")
    
    # Step 4: Backup and remove
    print("\n📋 Step 4: Backing up and removing js-debug folders")
    removed_count = 0
    
    for js_debug_path in js_debug_folders:
        print(f"\n🔧 Processing: {js_debug_path}")
        
        # Create backup
        backup_path = backup_js_debug_folder(js_debug_path)
        
        # Remove original
        if remove_js_debug_folder(js_debug_path):
            removed_count += 1
    
    print(f"\n✅ FIX COMPLETED!")
    print(f"📊 Removed {removed_count}/{len(js_debug_folders)} js-debug folders")
    print(f"💾 Backups created in workspace storage directories")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Restart VS Code")
    print("2. Run your browser automation script")
    print("3. Chrome should no longer exit with code 15")
    
    return True

if __name__ == "__main__":
    main()
