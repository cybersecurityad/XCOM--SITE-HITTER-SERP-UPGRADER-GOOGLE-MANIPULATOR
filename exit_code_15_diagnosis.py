#!/usr/bin/env python3
"""
🔍 EXIT CODE 15 DIAGNOSIS - BIT BY BIT ANALYSIS
==============================================
Testing each import and component individually to find the crash cause.
"""

import sys
import time
import os
import subprocess

def test_basic_imports():
    """Test basic Python imports"""
    try:
        print("🧪 Testing basic imports...")
        import time
        import random
        import json
        import os
        import sys
        import signal
        import subprocess
        import tempfile
        import shutil
        from datetime import datetime
        from typing import List, Dict, Optional
        from urllib.parse import urlparse, urljoin
        print("✅ Basic imports: OK")
        return True
    except Exception as e:
        print(f"❌ Basic imports failed: {e}")
        return False

def test_selenium_imports():
    """Test Selenium imports"""
    try:
        print("🧪 Testing Selenium imports...")
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException, WebDriverException
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        print("✅ Selenium imports: OK")
        return True
    except Exception as e:
        print(f"❌ Selenium imports failed: {e}")
        return False

def test_requests_import():
    """Test requests import"""
    try:
        print("🧪 Testing requests import...")
        import requests
        print("✅ Requests import: OK")
        return True
    except Exception as e:
        print(f"❌ Requests import failed: {e}")
        return False

def test_psutil_import():
    """Test psutil import"""
    try:
        print("🧪 Testing psutil import...")
        import psutil
        print("✅ Psutil import: OK")
        return True
    except Exception as e:
        print(f"❌ Psutil import failed: {e}")
        return False

def test_fake_useragent_import():
    """Test fake_useragent import"""
    try:
        print("🧪 Testing fake_useragent import...")
        from fake_useragent import UserAgent
        print("✅ Fake_useragent import: OK")
        return True
    except Exception as e:
        print(f"❌ Fake_useragent import failed: {e}")
        return False

def test_threading_import():
    """Test threading import"""
    try:
        print("🧪 Testing threading import...")
        import threading
        print("✅ Threading import: OK")
        return True
    except Exception as e:
        print(f"❌ Threading import failed: {e}")
        return False

def test_chrome_availability():
    """Test Chrome availability"""
    try:
        print("🧪 Testing Chrome availability...")
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(chrome_path):
            print("✅ Chrome found")
            return True
        else:
            print("❌ Chrome not found")
            return False
    except Exception as e:
        print(f"❌ Chrome test failed: {e}")
        return False

def test_tor_availability():
    """Test Tor availability"""
    try:
        print("🧪 Testing Tor availability...")
        result = subprocess.run(['which', 'tor'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Tor found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Tor not found")
            return False
    except Exception as e:
        print(f"❌ Tor test failed: {e}")
        return False

def test_minimal_selenium():
    """Test minimal Selenium WebDriver creation"""
    try:
        print("🧪 Testing minimal Selenium WebDriver...")
        
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        
        # Kill any existing Chrome
        subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True, check=False)
        time.sleep(2)
        
        # Minimal options
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')  # Run headless to avoid window issues
        
        # Create service
        service = Service()
        
        # Create driver with timeout
        print("🚀 Creating WebDriver...")
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(10)
        
        # Test simple navigation
        print("🌐 Testing navigation...")
        driver.get("data:text/html,<html><body><h1>Test</h1></body></html>")
        
        # Check title
        title = driver.title
        print(f"📄 Page title: {title}")
        
        # Clean up
        driver.quit()
        print("✅ Minimal Selenium: OK")
        return True
        
    except Exception as e:
        print(f"❌ Minimal Selenium failed: {e}")
        try:
            driver.quit()
        except:
            pass
        return False

def test_process_management():
    """Test process management functions"""
    try:
        print("🧪 Testing process management...")
        
        import psutil
        
        # Test process enumeration
        process_count = 0
        for proc in psutil.process_iter(['pid', 'name']):
            process_count += 1
            if process_count > 10:  # Just test first 10
                break
        
        print(f"✅ Process enumeration: Found {process_count} processes")
        return True
        
    except Exception as e:
        print(f"❌ Process management failed: {e}")
        return False

def test_signal_handling():
    """Test signal handling"""
    try:
        print("🧪 Testing signal handling...")
        
        import signal
        
        def dummy_handler(signum, frame):
            pass
        
        # Test signal registration
        signal.signal(signal.SIGTERM, dummy_handler)
        signal.signal(signal.SIGINT, dummy_handler)
        
        print("✅ Signal handling: OK")
        return True
        
    except Exception as e:
        print(f"❌ Signal handling failed: {e}")
        return False

def run_full_diagnosis():
    """Run complete bit-by-bit diagnosis"""
    print("🔍 EXIT CODE 15 DIAGNOSIS")
    print("=" * 50)
    print("Testing each component to find the crash cause...")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Selenium Imports", test_selenium_imports),
        ("Requests Import", test_requests_import),
        ("Psutil Import", test_psutil_import),
        ("Fake UserAgent Import", test_fake_useragent_import),
        ("Threading Import", test_threading_import),
        ("Chrome Availability", test_chrome_availability),
        ("Tor Availability", test_tor_availability),
        ("Process Management", test_process_management),
        ("Signal Handling", test_signal_handling),
        ("Minimal Selenium", test_minimal_selenium),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        
        try:
            result = test_func()
            results[test_name] = result
            
            if not result:
                print(f"🚨 POTENTIAL ISSUE FOUND: {test_name}")
                
        except Exception as e:
            print(f"💥 CRASH in {test_name}: {e}")
            results[test_name] = False
        
        # Small delay between tests
        time.sleep(1)
    
    # Summary
    print("\n" + "=" * 50)
    print("🔍 DIAGNOSIS SUMMARY")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    
    if failed > 0:
        print("\n🚨 ISSUES FOUND:")
        for test_name, result in results.items():
            if not result:
                print(f"   - {test_name}")
    else:
        print("\n✅ All tests passed - issue might be in combination")
    
    return results

if __name__ == "__main__":
    try:
        results = run_full_diagnosis()
        
        print("\n🎯 NEXT STEPS:")
        if any(not result for result in results.values()):
            print("   1. Fix the failed components above")
            print("   2. Re-run this diagnosis")
            print("   3. Test the main application")
        else:
            print("   1. All individual components work")
            print("   2. Issue is likely in component interaction")
            print("   3. Test with simplified main application")
            
    except KeyboardInterrupt:
        print("\n⚠️ Diagnosis interrupted")
    except Exception as e:
        print(f"\n💥 Diagnosis crashed: {e}")
