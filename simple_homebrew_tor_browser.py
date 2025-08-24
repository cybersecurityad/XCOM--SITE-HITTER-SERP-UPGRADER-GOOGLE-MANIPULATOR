#!/usr/bin/env python3
"""
Simple Homebrew Tor Browser - Minimal working version
================================================

Uses Homebrew Tor service with minimal Chrome options for maximum compatibility.
"""

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import signal
import sys
import requests
import subprocess
import socket
from contextlib import closing

class SimpleHomebrewTorBrowser:
    """Simple browser that uses existing Homebrew Tor service"""
    
    def __init__(self, tor_port=9050):
        self.tor_port = tor_port
        self.driver = None
        self.tor_service_running = False
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        print("🔄 SIMPLE HOMEBREW TOR BROWSER - Initializing...")
        
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n⚠️  Signal {signum} received - shutting down...")
        self.cleanup()
        sys.exit(0)
        
    def check_tor_service(self):
        """Check if Homebrew Tor service is running"""
        print("🔍 Checking Homebrew Tor service status...")
        
        try:
            # Test the port directly
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                sock.settimeout(5)
                result = sock.connect_ex(('127.0.0.1', self.tor_port))
                if result == 0:
                    print(f"✅ Tor SOCKS port {self.tor_port} is accessible")
                    self.tor_service_running = True
                    return True
                else:
                    print(f"❌ Tor SOCKS port {self.tor_port} is not accessible")
                    return False
                    
        except Exception as e:
            print(f"❌ Error checking Tor service: {e}")
            return False
    
    def get_tor_ip(self):
        """Get current Tor IP address"""
        print("🔍 Getting Tor IP address...")
        
        proxies = {
            'http': f'socks5://127.0.0.1:{self.tor_port}',
            'https': f'socks5://127.0.0.1:{self.tor_port}'
        }
        
        try:
            response = requests.get('https://httpbin.org/ip', 
                                  proxies=proxies, timeout=15)
            tor_ip = response.json()['origin']
            print(f"✅ Tor IP: {tor_ip}")
            return tor_ip
        except Exception as e:
            print(f"❌ Error getting Tor IP: {e}")
            return None
    
    def create_browser(self):
        """Create Chrome browser with minimal options"""
        print("🔄 Creating Chrome browser with Tor proxy...")
        
        if not self.tor_service_running:
            print("❌ Tor service not running - cannot create browser")
            return False
        
        try:
            # Minimal Chrome options for maximum compatibility
            options = Options()
            options.add_argument(f'--proxy-server=socks5://127.0.0.1:{self.tor_port}')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            print("🔄 Starting Chrome with minimal options...")
            self.driver = uc.Chrome(options=options)
            
            # Set basic timeouts
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            
            print("✅ Chrome browser created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error creating browser: {e}")
            return False
    
    def test_browser_simple(self):
        """Simple browser test"""
        if not self.driver:
            print("❌ No browser available for testing")
            return False
        
        print("🔄 Testing browser functionality...")
        
        try:
            # Test 1: Navigate to a simple page
            print("📍 Test 1: Basic navigation...")
            self.driver.get('data:text/html,<html><body><h1>Test</h1></body></html>')
            time.sleep(2)
            print("✅ Basic navigation successful")
            
            # Test 2: Try to get IP through Tor
            print("📍 Test 2: Testing Tor proxy...")
            self.driver.get('https://httpbin.org/ip')
            time.sleep(5)
            
            # Check if page loaded
            body = self.driver.find_element(By.TAG_NAME, "body")
            if body and body.text:
                print(f"✅ Tor proxy test response: {body.text}")
            else:
                print("⚠️  Tor proxy test - no response")
            
            print("✅ Browser tests completed!")
            return True
            
        except Exception as e:
            print(f"❌ Browser test failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up browser resources"""
        print("🔄 Cleaning up...")
        
        if self.driver:
            try:
                self.driver.quit()
                print("✅ Browser closed")
            except Exception as e:
                print(f"⚠️  Error closing browser: {e}")
        
        print("ℹ️  Homebrew Tor service left running")
    
    def run_test(self):
        """Run simple test"""
        print("=" * 50)
        print("🚀 SIMPLE HOMEBREW TOR BROWSER TEST")
        print("=" * 50)
        
        # Step 1: Check Tor service
        if not self.check_tor_service():
            print("❌ Tor service check failed")
            return False
        
        # Step 2: Test Tor connectivity
        tor_ip = self.get_tor_ip()
        if not tor_ip:
            print("❌ Tor connectivity test failed")
            return False
        
        # Step 3: Create browser
        if not self.create_browser():
            print("❌ Browser creation failed")
            return False
        
        # Step 4: Test browser
        if not self.test_browser_simple():
            print("❌ Browser testing failed")
            self.cleanup()
            return False
        
        print("=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
        print("🔄 Browser staying open for 30 seconds...")
        
        try:
            time.sleep(30)
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")
        
        self.cleanup()
        return True

def main():
    """Main function"""
    browser = SimpleHomebrewTorBrowser()
    
    try:
        success = browser.run_test()
        if success:
            print("🎉 Test completed successfully!")
        else:
            print("❌ Test failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        browser.cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        browser.cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main()
