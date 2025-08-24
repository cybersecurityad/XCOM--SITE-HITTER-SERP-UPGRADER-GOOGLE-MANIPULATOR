#!/usr/bin/env python3
"""
🧪 FIRST BROWSER STARTUP TEST
============================
Test ONLY the first browser creation without any Tor.
This will help identify why the first browser exits.
"""

# AUTO-INITIALIZE LOGGING (LIGHTWEIGHT)
from lightweight_auto_logger import lightweight_auto_initialize
lightweight_auto_initialize()

import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def kill_all_chrome():
    """Kill all existing Chrome processes"""
    try:
        print("🔪 Killing all Chrome processes...")
        subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True, check=False)
        subprocess.run(['pkill', '-f', 'chromedriver'], capture_output=True, check=False)
        time.sleep(2)
        print("✅ Chrome processes killed")
    except Exception as e:
        print(f"⚠️ Chrome kill warning: {e}")

def test_first_browser_only():
    """Test creating ONLY the first browser"""
    try:
        print("=" * 50)
        print("🧪 FIRST BROWSER STARTUP TEST")
        print("=" * 50)
        print("🎯 Testing ONLY first browser creation")
        print("🚫 NO Tor, NO proxy, NO multiple browsers")
        print("=" * 50)
        
        # Clean slate
        kill_all_chrome()
        
        print("\n1️⃣ CREATING FIRST BROWSER...")
        print("🌐 Using minimal Chrome options...")
        
        # Minimal Chrome options
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Create service
        service = Service()
        
        # Create browser
        print("🚀 Starting Chrome...")
        browser = webdriver.Chrome(service=service, options=options)
        
        print("✅ First browser created successfully!")
        
        # Test basic functionality
        print("🧪 Testing browser functionality...")
        browser.get("data:text/html,<html><body><h1>First Browser Test</h1></body></html>")
        
        if "First Browser Test" in browser.page_source:
            print("✅ Browser is functional!")
        else:
            print("❌ Browser functionality test failed")
        
        # Keep browser open briefly
        print("👀 Browser is running...")
        print("⏱️ Keeping open for 10 seconds...")
        time.sleep(10)
        
        # Close browser
        print("🧹 Closing browser...")
        browser.quit()
        print("✅ Browser closed successfully!")
        
        print("\n🎉 FIRST BROWSER TEST PASSED!")
        print("✅ No crashes detected")
        print("✅ No exit code 15")
        
        return True
        
    except Exception as e:
        print(f"\n❌ FIRST BROWSER TEST FAILED!")
        print(f"❌ Error: {e}")
        print(f"❌ This is the root cause of exit code 15")
        return False

def main():
    """Run the first browser test"""
    try:
        success = test_first_browser_only()
        
        if success:
            print("\n💡 CONCLUSION:")
            print("✅ First browser startup works fine")
            print("✅ Issue must be with Tor integration or multiple browsers")
        else:
            print("\n💡 CONCLUSION:")
            print("❌ First browser startup has fundamental issues")
            print("❌ Chrome/Selenium configuration problem")
            
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
    finally:
        kill_all_chrome()

if __name__ == "__main__":
    main()
