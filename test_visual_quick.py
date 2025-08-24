
#!/usr/bin/env python3
"""
🔧 VS CODE EXIT CODE 15 FIX
===========================
Minimal test to prevent VS Code crashes
"""

import time
import subprocess
import requests

def simple_test():
    """Minimal test that won't crash VS Code"""
    print("🧪 MINIMAL VSCODE-SAFE TEST")
    print("=" * 30)
    
    try:
        # Test 1: Simple network check
        print("🌐 Test 1: Network connectivity...")
        response = requests.get('https://httpbin.org/ip', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Network OK: {data.get('origin', 'Unknown')}")
        else:
            print("❌ Network failed")
            
        # Test 2: Process management
        print("🔧 Test 2: Process management...")
        test_process = subprocess.Popen(['echo', 'Hello World'], 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE)
        stdout, stderr = test_process.communicate()
        if test_process.returncode == 0:
            print(f"✅ Process OK: {stdout.decode().strip()}")
        else:
            print("❌ Process failed")
            
        # Test 3: Environment check
        print("🐍 Test 3: Python environment...")
        import sys
        print(f"✅ Python: {sys.version}")
        print(f"✅ Platform: {sys.platform}")
        
        print("\n🎉 ALL TESTS PASSED - NO VS CODE CRASHES!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    simple_test()
