#!/usr/bin/env python3
"""
🧪 MULTIPLE BROWSER STARTUP TEST
===============================
Test creating multiple browsers in sequence to find where crashes occur.
"""

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

def create_single_browser(browser_number):
    """Create a single browser instance"""
    try:
        print(f"\n{browser_number}️⃣ CREATING BROWSER {browser_number}...")
        
        # Minimal Chrome options
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Create service
        service = Service()
        
        # Create browser
        print(f"🚀 Starting Chrome {browser_number}...")
        browser = webdriver.Chrome(service=service, options=options)
        
        print(f"✅ Browser {browser_number} created successfully!")
        
        # Test basic functionality
        browser.get(f"data:text/html,<html><body><h1>Browser {browser_number} Test</h1></body></html>")
        
        if f"Browser {browser_number} Test" in browser.page_source:
            print(f"✅ Browser {browser_number} is functional!")
        else:
            print(f"❌ Browser {browser_number} functionality test failed")
        
        # Keep browser open briefly
        print(f"👀 Browser {browser_number} running for 5 seconds...")
        time.sleep(5)
        
        # Close browser
        print(f"🧹 Closing browser {browser_number}...")
        browser.quit()
        print(f"✅ Browser {browser_number} closed successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ BROWSER {browser_number} FAILED!")
        print(f"❌ Error: {e}")
        return False

def test_multiple_browsers():
    """Test creating multiple browsers in sequence"""
    print("=" * 50)
    print("🧪 MULTIPLE BROWSER STARTUP TEST")
    print("=" * 50)
    print("🎯 Testing sequential browser creation")
    print("🚫 NO Tor, just multiple browsers")
    print("=" * 50)
    
    # Clean slate
    kill_all_chrome()
    
    results = []
    
    # Test 3 browsers in sequence
    for i in range(1, 4):
        print(f"\n{'='*30}")
        print(f"TESTING BROWSER {i}")
        print(f"{'='*30}")
        
        success = create_single_browser(i)
        results.append(success)
        
        if not success:
            print(f"❌ Browser {i} failed - stopping test")
            break
        
        # Wait between browsers
        print(f"⏳ Waiting 3 seconds before next browser...")
        time.sleep(3)
    
    # Results summary
    print(f"\n{'='*50}")
    print("📊 TEST RESULTS SUMMARY")
    print(f"{'='*50}")
    
    for i, success in enumerate(results, 1):
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"Browser {i}: {status}")
    
    successful_browsers = sum(results)
    print(f"\nSuccessful browsers: {successful_browsers}/{len(results)}")
    
    if all(results):
        print("\n💡 CONCLUSION:")
        print("✅ All browsers work in sequence")
        print("✅ Issue must be specifically with Tor integration")
    else:
        first_failure = results.index(False) + 1 if False in results else None
        print(f"\n💡 CONCLUSION:")
        print(f"❌ Browser {first_failure} failed")
        print(f"❌ Multiple browser creation has issues")

def main():
    """Run the multiple browser test"""
    try:
        test_multiple_browsers()
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
    finally:
        kill_all_chrome()

if __name__ == "__main__":
    main()
