#!/usr/bin/env python3
"""
🧪 PYTHON ENVIRONMENT TEST
=========================
Test if the Python environment itself is causing exit code 15
"""

import sys
import os

def test_basic_python():
    """Test basic Python functionality"""
    print("🐍 PYTHON ENVIRONMENT TEST")
    print("=" * 30)
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Virtual environment: {os.environ.get('VIRTUAL_ENV', 'None')}")
    print("✅ Basic Python test passed")

def test_import_selenium():
    """Test Selenium import"""
    try:
        from selenium import webdriver
        print("✅ Selenium import: OK")
        return True
    except Exception as e:
        print(f"❌ Selenium import failed: {e}")
        return False

def test_import_requests():
    """Test requests import"""
    try:
        import requests
        print("✅ Requests import: OK")
        return True
    except Exception as e:
        print(f"❌ Requests import failed: {e}")
        return False

def test_subprocess():
    """Test subprocess functionality"""
    try:
        import subprocess
        result = subprocess.run(['echo', 'test'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Subprocess test: OK")
            return True
        else:
            print(f"❌ Subprocess failed with code: {result.returncode}")
            return False
    except Exception as e:
        print(f"❌ Subprocess test failed: {e}")
        return False

def test_signal_handling():
    """Test signal handling"""
    try:
        import signal
        def dummy_handler(signum, frame):
            pass
        signal.signal(signal.SIGTERM, dummy_handler)
        print("✅ Signal handling: OK")
        return True
    except Exception as e:
        print(f"❌ Signal handling failed: {e}")
        return False

def test_file_operations():
    """Test file operations"""
    try:
        import tempfile
        import shutil
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp(prefix="env_test_")
        
        # Write test file
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        
        # Read test file
        with open(test_file, 'r') as f:
            content = f.read()
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        if content == "test":
            print("✅ File operations: OK")
            return True
        else:
            print("❌ File operations: Content mismatch")
            return False
    except Exception as e:
        print(f"❌ File operations failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable handling"""
    try:
        # Set test env var
        os.environ['TEST_VAR'] = 'test_value'
        
        # Read it back
        if os.environ.get('TEST_VAR') == 'test_value':
            print("✅ Environment variables: OK")
            # Clean up
            del os.environ['TEST_VAR']
            return True
        else:
            print("❌ Environment variables: Value mismatch")
            return False
    except Exception as e:
        print(f"❌ Environment variables failed: {e}")
        return False

def main():
    """Run all environment tests"""
    print("🧪 TESTING PYTHON ENVIRONMENT FOR EXIT CODE 15 ISSUES")
    print("=" * 60)
    
    tests = [
        test_basic_python,
        test_import_selenium,
        test_import_requests,
        test_subprocess,
        test_signal_handling,
        test_file_operations,
        test_environment_variables
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
        print("-" * 30)
    
    print(f"\n📊 RESULTS: {passed} passed, {failed} failed")
    
    if failed > 0:
        print("❌ Environment issues detected!")
        print("Potential causes of exit code 15:")
        print("- Corrupted virtual environment")
        print("- Missing dependencies")
        print("- Permission issues")
        print("- System resource limits")
    else:
        print("✅ Environment appears healthy")
        print("Exit code 15 likely caused by browser/Tor processes")

if __name__ == "__main__":
    main()
