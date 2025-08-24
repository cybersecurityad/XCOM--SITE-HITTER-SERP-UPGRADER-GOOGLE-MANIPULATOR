#!/usr/bin/env python3
"""
🔍 DEEP ENVIRONMENT ANALYSIS
============================
Deep dive into environment variables and settings that might cause exit code 15
"""

import os
import sys
import subprocess
import psutil
import tempfile
import shutil

def check_problematic_env_vars():
    """Check for environment variables that might cause issues"""
    print("🔍 CHECKING PROBLEMATIC ENVIRONMENT VARIABLES")
    print("=" * 50)
    
    # Check for VS Code related variables
    vscode_vars = [k for k in os.environ.keys() if 'VSCODE' in k.upper()]
    if vscode_vars:
        print("📝 VS Code environment variables found:")
        for var in vscode_vars:
            print(f"   {var}={os.environ[var]}")
    else:
        print("✅ No VS Code environment variables")
    
    # Check for Chrome/browser variables
    browser_vars = [k for k in os.environ.keys() if any(x in k.upper() for x in ['CHROME', 'BROWSER', 'DISPLAY'])]
    if browser_vars:
        print("🌐 Browser-related environment variables:")
        for var in browser_vars:
            print(f"   {var}={os.environ[var]}")
    else:
        print("✅ No browser environment variables")
    
    # Check TMPDIR and temp settings
    print(f"📁 TMPDIR: {os.environ.get('TMPDIR', 'Not set')}")
    print(f"📁 TEMP: {os.environ.get('TEMP', 'Not set')}")
    print(f"📁 TMP: {os.environ.get('TMP', 'Not set')}")
    
    # Check PATH
    path = os.environ.get('PATH', '')
    if '/usr/local/bin' in path:
        print("✅ /usr/local/bin in PATH")
    else:
        print("⚠️ /usr/local/bin not in PATH")
    
    print("-" * 50)

def check_system_limits():
    """Check system resource limits"""
    print("🔧 CHECKING SYSTEM LIMITS")
    print("=" * 30)
    
    try:
        # Check memory
        memory = psutil.virtual_memory()
        print(f"💾 Memory: {memory.available / 1024**3:.1f}GB available / {memory.total / 1024**3:.1f}GB total")
        
        # Check disk space
        disk = psutil.disk_usage('/')
        print(f"💽 Disk: {disk.free / 1024**3:.1f}GB free / {disk.total / 1024**3:.1f}GB total")
        
        # Check running processes
        processes = len(list(psutil.process_iter()))
        print(f"⚙️ Running processes: {processes}")
        
        # Check file descriptor limits
        try:
            import resource
            soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
            print(f"📂 File descriptors: {soft} soft limit, {hard} hard limit")
        except:
            print("📂 Could not check file descriptor limits")
            
    except Exception as e:
        print(f"❌ System check failed: {e}")
    
    print("-" * 30)

def check_chrome_conflicts():
    """Check for Chrome processes that might conflict"""
    print("🌐 CHECKING CHROME CONFLICTS")
    print("=" * 35)
    
    try:
        chrome_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'chrome' in proc.info['name'].lower():
                    chrome_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if chrome_processes:
            print(f"⚠️ Found {len(chrome_processes)} Chrome processes:")
            for proc in chrome_processes[:5]:  # Show first 5
                print(f"   PID {proc['pid']}: {proc['name']}")
        else:
            print("✅ No Chrome processes running")
            
    except Exception as e:
        print(f"❌ Chrome check failed: {e}")
    
    print("-" * 35)

def check_tor_conflicts():
    """Check for Tor processes"""
    print("🧅 CHECKING TOR CONFLICTS")
    print("=" * 30)
    
    try:
        tor_processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'tor' in proc.info['name'].lower():
                    tor_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if tor_processes:
            print(f"⚠️ Found {len(tor_processes)} Tor processes:")
            for proc in tor_processes:
                print(f"   PID {proc['pid']}: {proc['name']}")
        else:
            print("✅ No Tor processes running")
            
    except Exception as e:
        print(f"❌ Tor check failed: {e}")
    
    print("-" * 30)

def test_subprocess_stability():
    """Test if subprocess operations are stable"""
    print("🔄 TESTING SUBPROCESS STABILITY")
    print("=" * 40)
    
    try:
        # Test multiple subprocess calls
        for i in range(5):
            result = subprocess.run(['echo', f'test{i}'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=2)
            if result.returncode != 0:
                print(f"❌ Subprocess {i} failed with code {result.returncode}")
                return False
            print(f"✅ Subprocess {i}: OK")
        
        print("✅ All subprocess tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Subprocess stability test failed: {e}")
        return False

def test_temp_dir_creation():
    """Test temporary directory creation and cleanup"""
    print("📁 TESTING TEMP DIRECTORY OPERATIONS")
    print("=" * 45)
    
    try:
        temp_dirs = []
        
        # Create multiple temp directories
        for i in range(3):
            temp_dir = tempfile.mkdtemp(prefix=f"envtest_{i}_")
            temp_dirs.append(temp_dir)
            print(f"✅ Created temp dir {i}: {temp_dir}")
        
        # Clean them up
        for i, temp_dir in enumerate(temp_dirs):
            shutil.rmtree(temp_dir)
            print(f"✅ Cleaned temp dir {i}")
        
        print("✅ Temp directory operations stable")
        return True
        
    except Exception as e:
        print(f"❌ Temp directory test failed: {e}")
        return False

def main():
    """Run comprehensive environment analysis"""
    print("🔍 DEEP ENVIRONMENT ANALYSIS FOR EXIT CODE 15")
    print("=" * 60)
    
    check_problematic_env_vars()
    check_system_limits()
    check_chrome_conflicts()
    check_tor_conflicts()
    
    stability_tests = [
        test_subprocess_stability,
        test_temp_dir_creation
    ]
    
    print("🧪 RUNNING STABILITY TESTS")
    print("=" * 30)
    
    all_passed = True
    for test in stability_tests:
        if not test():
            all_passed = False
        print("-" * 30)
    
    if all_passed:
        print("✅ ENVIRONMENT ANALYSIS COMPLETE")
        print("Environment appears stable for browser automation")
    else:
        print("❌ ENVIRONMENT ISSUES DETECTED")
        print("Instability may cause exit code 15")

if __name__ == "__main__":
    main()
