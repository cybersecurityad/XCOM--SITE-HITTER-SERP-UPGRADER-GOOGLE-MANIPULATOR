#!/usr/bin/env python3
"""
🔍 VS CODE CRASH DIAGNOSIS
=========================
Diagnose what's causing VS Code to crash with exit code 15
"""

import subprocess
import time
import os
import psutil
import signal

def check_vscode_extensions():
    """Check what VS Code extensions might be causing issues"""
    print("🔍 Checking VS Code environment...")
    
    # Check if we're running inside VS Code
    if 'VSCODE_IPC_HOOK' in os.environ:
        print("✅ Running inside VS Code")
        print(f"📍 VS Code IPC: {os.environ.get('VSCODE_IPC_HOOK', 'N/A')}")
    else:
        print("❌ Not running inside VS Code")
    
    # Check VS Code related processes
    print("\n🔍 VS Code related processes:")
    vscode_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            name = proc.info['name'].lower()
            if any(keyword in name for keyword in ['code', 'electron', 'pylance', 'python']):
                vscode_processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cmdline': ' '.join(proc.info['cmdline'][:3]) if proc.info['cmdline'] else 'N/A'
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    for proc in vscode_processes[:10]:  # Limit to first 10
        print(f"  PID {proc['pid']}: {proc['name']} - {proc['cmdline']}")
    
    return len(vscode_processes)

def test_subprocess_safety():
    """Test if subprocess creation is safe"""
    print("\n🧪 Testing subprocess safety...")
    
    try:
        # Test 1: Simple echo
        result = subprocess.run(['echo', 'test'], capture_output=True, timeout=5)
        if result.returncode == 0:
            print("✅ Basic subprocess: OK")
        else:
            print("❌ Basic subprocess: FAILED")
        
        # Test 2: Background process
        print("🔍 Testing background process...")
        proc = subprocess.Popen(['sleep', '2'], stdout=subprocess.DEVNULL)
        time.sleep(1)
        
        if proc.poll() is None:
            print("✅ Background process: RUNNING")
            proc.terminate()
            proc.wait(timeout=5)
            print("✅ Background process: TERMINATED")
        else:
            print("❌ Background process: FAILED")
        
        return True
        
    except Exception as e:
        print(f"❌ Subprocess test failed: {e}")
        return False

def test_memory_pressure():
    """Check memory usage"""
    print("\n💾 Memory usage check...")
    
    try:
        memory = psutil.virtual_memory()
        print(f"📊 Total RAM: {memory.total / (1024**3):.1f} GB")
        print(f"📊 Available: {memory.available / (1024**3):.1f} GB")
        print(f"📊 Used: {memory.percent}%")
        
        if memory.percent > 90:
            print("⚠️ HIGH MEMORY USAGE - This could cause crashes!")
            return False
        else:
            print("✅ Memory usage: OK")
            return True
            
    except Exception as e:
        print(f"❌ Memory check failed: {e}")
        return False

def test_selenium_safety():
    """Test if Selenium can be imported safely"""
    print("\n🌐 Testing Selenium safety...")
    
    try:
        # Try importing selenium
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        print("✅ Selenium import: OK")
        
        # Try creating options (this is usually where crashes happen)
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        print("✅ Chrome options: OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Selenium test failed: {e}")
        return False

def main():
    """Main diagnosis function"""
    print("🔍 VS CODE CRASH DIAGNOSIS")
    print("=" * 40)
    print("🎯 Investigating exit code 15 crashes")
    print("=" * 40)
    
    results = {}
    
    # Run all tests
    results['vscode_procs'] = check_vscode_extensions()
    results['subprocess'] = test_subprocess_safety()
    results['memory'] = test_memory_pressure()
    results['selenium'] = test_selenium_safety()
    
    # Summary
    print("\n📊 DIAGNOSIS SUMMARY")
    print("=" * 30)
    
    if results['vscode_procs'] > 20:
        print("⚠️ HIGH VS Code process count - possible extension conflict")
    
    if not results['subprocess']:
        print("❌ SUBPROCESS ISSUE - This could cause exit code 15")
    
    if not results['memory']:
        print("❌ MEMORY PRESSURE - This could cause crashes")
    
    if not results['selenium']:
        print("❌ SELENIUM ISSUE - Browser automation may be problematic")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    
    if all(results.values()):
        print("✅ All tests passed - VS Code should be stable")
        print("💭 If crashes still occur, try:")
        print("   1. Restart VS Code")
        print("   2. Disable Pylance extension temporarily")
        print("   3. Use external terminal for browser automation")
    else:
        print("⚠️ Issues detected - try these fixes:")
        if not results['selenium']:
            print("   🔧 Use Firefox instead of Chrome")
        if not results['memory']:
            print("   🔧 Close other applications to free memory")
        if not results['subprocess']:
            print("   🔧 Run scripts outside VS Code terminal")

if __name__ == "__main__":
    main()
