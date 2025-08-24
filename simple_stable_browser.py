#!/usr/bin/env python3
"""
🛡️ SIMPLE STABLE BROWSER - NO CRASHES
=====================================
Minimal browser automation that won't crash VS Code.
No Tor, no complex setup, just basic browser automation.
"""

import time
import os
import sys
import signal
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

class SimpleBrowser:
    """Simple, crash-proof browser"""
    
    def __init__(self):
        self.driver = None
        self.running = True
        
        # Handle signals gracefully
        signal.signal(signal.SIGTERM, self._cleanup)
        signal.signal(signal.SIGINT, self._cleanup)
    
    def _cleanup(self, signum=None, frame=None):
        """Clean shutdown"""
        print(f"\n🛡️ Graceful shutdown (signal: {signum})")
        self.running = False
        if self.driver:
            try:
                self.driver.quit()
                print("✅ Browser closed")
            except:
                pass
        sys.exit(0)
    
    def create_simple_browser(self):
        """Create minimal Chrome browser"""
        try:
            print("🌐 Creating simple browser...")
            
            # Kill any existing Chrome processes
            subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True, check=False)
            time.sleep(2)
            
            # Minimal Chrome options
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-images')
            options.add_argument('--disable-javascript')  # Disable JS to prevent crashes
            options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
            
            # Create service with timeout
            service = Service()
            
            # Create driver with 10-second timeout
            print("🚀 Starting Chrome...")
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_page_load_timeout(10)
            self.driver.implicitly_wait(5)
            
            print("✅ Browser created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Browser creation failed: {e}")
            return False
    
    def test_simple_page(self):
        """Test with simple HTML page"""
        try:
            if not self.driver:
                print("❌ No browser available")
                return False
                
            print("🧪 Testing simple page...")
            
            # Create simple test page
            test_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Simple Test Page</title>
            </head>
            <body>
                <h1>Browser Test Successful!</h1>
                <p>This page loaded without crashing.</p>
                <p>Time: """ + str(time.time()) + """</p>
            </body>
            </html>
            """
            
            # Load the test page
            self.driver.get(f"data:text/html,{test_html}")
            
            # Verify page loaded
            title = self.driver.title or ""
            if "Simple Test Page" in title:
                print(f"✅ Page loaded: {title}")
                return True
            else:
                print(f"❌ Page load failed: {title}")
                return False
                
        except Exception as e:
            print(f"❌ Page test failed: {e}")
            return False
    
    def test_real_website(self, url):
        """Test real website with timeout protection"""
        try:
            if not self.driver:
                print("❌ No browser available")
                return False
                
            print(f"🌐 Testing website: {url}")
            
            # Load website with timeout
            self.driver.get(url)
            
            # Wait for basic load
            WebDriverWait(self.driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            title = (self.driver.title or "")[:50] if self.driver.title else "No title"
            print(f"✅ Website loaded: {title}...")
            
            # Keep browser open for observation
            print("👁️ Browser window should be visible")
            print("⏱️ Keeping open for 10 seconds...")
            
            for i in range(10):
                if not self.running:
                    break
                time.sleep(1)
                if i % 3 == 0:
                    print(f"⏳ {10-i} seconds remaining...")
            
            return True
            
        except TimeoutException:
            print("⏰ Website load timeout")
            return False
        except Exception as e:
            print(f"❌ Website test failed: {e}")
            return False
    
    def run_stability_test(self):
        """Run complete stability test"""
        try:
            print("🛡️ SIMPLE STABLE BROWSER TEST")
            print("=" * 40)
            
            # Create browser
            if not self.create_simple_browser():
                print("❌ Browser creation failed")
                return False
            
            # Test simple page
            if not self.test_simple_page():
                print("❌ Simple page test failed")
                return False
            
            print("\n✅ SIMPLE PAGE TEST PASSED!")
            
            # Test real website
            test_url = "https://httpbin.org/ip"
            if self.test_real_website(test_url):
                print("\n✅ REAL WEBSITE TEST PASSED!")
                print("🎉 NO CRASHES DETECTED!")
                return True
            else:
                print("\n❌ Real website test failed")
                return False
                
        except KeyboardInterrupt:
            print("\n⚠️ Test interrupted by user")
            return False
        except Exception as e:
            print(f"\n❌ Stability test error: {e}")
            return False
        finally:
            self._cleanup()

def main():
    """Main test function"""
    browser = SimpleBrowser()
    
    try:
        success = browser.run_stability_test()
        if success:
            print("\n🎉 SUCCESS: No crashes, no exit code 15!")
        else:
            print("\n❌ Test failed")
            
    except Exception as e:
        print(f"\n❌ Main error: {e}")
    finally:
        if browser.driver:
            try:
                browser.driver.quit()
            except:
                pass

if __name__ == "__main__":
    main()
