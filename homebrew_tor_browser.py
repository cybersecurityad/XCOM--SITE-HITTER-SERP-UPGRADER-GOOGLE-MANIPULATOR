#!/usr/bin/env python3
"""
Homebrew Tor Browser - Uses existing Homebrew Tor service
====================================================

This version connects to an existing Homebrew Tor service instead of managing its own Tor process.

Usage:
    brew services start tor  # Start Tor service first
    python homebrew_tor_browser.py
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

class HomebrewTorBrowser:
    """Browser that uses existing Homebrew Tor service"""
    
    def __init__(self, tor_port=9050, control_port=9051):
        self.tor_port = tor_port
        self.control_port = control_port
        self.driver = None
        self.tor_service_running = False
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        print("🔄 HOMEBREW TOR BROWSER - Initializing...")
        
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n⚠️  Signal {signum} received - shutting down...")
        self.cleanup()
        sys.exit(0)
        
    def check_tor_service(self):
        """Check if Homebrew Tor service is running"""
        print("🔍 Checking Homebrew Tor service status...")
        
        try:
            # Check if Tor service is listed as started
            result = subprocess.run(['brew', 'services', 'list'], 
                                  capture_output=True, text=True, timeout=10)
            
            if 'tor' in result.stdout and 'started' in result.stdout:
                print("✅ Homebrew Tor service is running")
                
                # Double-check by testing the port
                if self._test_tor_port():
                    self.tor_service_running = True
                    return True
                else:
                    print("❌ Tor service listed as started but port not accessible")
                    return False
            else:
                print("❌ Homebrew Tor service is not started")
                print("💡 Run: brew services start tor")
                return False
                
        except Exception as e:
            print(f"❌ Error checking Tor service: {e}")
            return False
    
    def _test_tor_port(self):
        """Test if Tor SOCKS port is accessible"""
        print(f"🔍 Testing Tor SOCKS port {self.tor_port}...")
        
        try:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                sock.settimeout(5)
                result = sock.connect_ex(('127.0.0.1', self.tor_port))
                if result == 0:
                    print(f"✅ Tor SOCKS port {self.tor_port} is accessible")
                    return True
                else:
                    print(f"❌ Tor SOCKS port {self.tor_port} is not accessible")
                    return False
        except Exception as e:
            print(f"❌ Error testing Tor port: {e}")
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
        """Create Chrome browser with Tor proxy"""
        print("🔄 Creating Chrome browser with Tor proxy...")
        
        if not self.tor_service_running:
            print("❌ Tor service not running - cannot create browser")
            return False
        
        try:
            # Chrome options for Tor
            options = Options()
            options.add_argument(f'--proxy-server=socks5://127.0.0.1:{self.tor_port}')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--enable-javascript')
            
            # Human-like user agent
            options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            print("🔄 Starting Chrome with undetected-chromedriver...")
            self.driver = uc.Chrome(options=options, version_main=None)
            
            # Configure timeouts
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            
            print("✅ Chrome browser created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error creating browser: {e}")
            return False
    
    def test_browser(self):
        """Test browser functionality"""
        if not self.driver:
            print("❌ No browser available for testing")
            return False
        
        print("🔄 Testing browser functionality...")
        
        try:
            # Test 1: Check IP via Tor
            print("📍 Test 1: Checking IP address...")
            self.driver.get('https://httpbin.org/ip')
            time.sleep(3)
            
            ip_element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            ip_text = ip_element.text
            print(f"✅ Browser IP response: {ip_text}")
            
            # Test 2: Check Tor Browser detection
            print("🔍 Test 2: Checking Tor detection...")
            self.driver.get('https://check.torproject.org/')
            time.sleep(5)
            
            # Look for Tor confirmation
            page_source = self.driver.page_source.lower()
            if 'congratulations' in page_source and 'tor' in page_source:
                print("✅ Tor detected successfully!")
            else:
                print("⚠️  Tor may not be properly detected")
            
            # Test 3: Basic navigation
            print("🔍 Test 3: Testing basic navigation...")
            self.driver.get('https://httpbin.org/user-agent')
            time.sleep(3)
            
            ua_element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print(f"✅ User Agent: {ua_element.text}")
            
            print("✅ All browser tests passed!")
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
        
        # Note: We don't stop the Homebrew Tor service since it's managed externally
        print("ℹ️  Homebrew Tor service left running (managed externally)")
        print("💡 To stop: brew services stop tor")
    
    def run_full_test(self):
        """Run complete test suite"""
        print("=" * 60)
        print("🚀 HOMEBREW TOR BROWSER - FULL TEST")
        print("=" * 60)
        
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
        if not self.test_browser():
            print("❌ Browser testing failed")
            self.cleanup()
            return False
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("🔄 Browser will stay open for 30 seconds...")
        print("💡 Press Ctrl+C to close early")
        
        try:
            time.sleep(30)
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")
        
        self.cleanup()
        return True

def main():
    """Main function"""
    browser = HomebrewTorBrowser()
    
    try:
        success = browser.run_full_test()
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
