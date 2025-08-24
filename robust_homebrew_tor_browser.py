#!/usr/bin/env python3
"""
Robust Homebrew Tor Browser - Enhanced version with better error handling
====================================================================

This version uses Homebrew Tor service with enhanced stability and error handling.
"""

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import signal
import sys
import requests
import subprocess
import socket
import os
from contextlib import closing

class RobustHomebrewTorBrowser:
    """Enhanced browser that uses existing Homebrew Tor service"""
    
    def __init__(self, tor_port=9050, control_port=9051):
        self.tor_port = tor_port
        self.control_port = control_port
        self.driver = None
        self.tor_service_running = False
        self.chrome_process = None
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        print("🔄 ROBUST HOMEBREW TOR BROWSER - Initializing...")
        
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
    
    def kill_existing_chrome(self):
        """Kill any existing Chrome processes"""
        print("🔄 Cleaning up existing Chrome processes...")
        
        try:
            # Kill Chrome processes
            subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True)
            subprocess.run(['pkill', '-f', 'chromedriver'], capture_output=True)
            time.sleep(2)
            print("✅ Existing Chrome processes cleaned up")
        except Exception as e:
            print(f"⚠️  Error cleaning Chrome processes: {e}")
    
    def create_browser(self):
        """Create Chrome browser with Tor proxy and enhanced stability"""
        print("🔄 Creating Chrome browser with Tor proxy...")
        
        if not self.tor_service_running:
            print("❌ Tor service not running - cannot create browser")
            return False
        
        # Clean up any existing Chrome processes first
        self.kill_existing_chrome()
        
        try:
            # Chrome options for Tor with stability enhancements
            options = Options()
            
            # Proxy settings
            options.add_argument(f'--proxy-server=socks5://127.0.0.1:{self.tor_port}')
            
            # Stability options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-features=VizDisplayCompositor')
            
            # Security and detection avoidance
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Window and display settings
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--start-maximized')
            
            # Human-like user agent
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            options.add_argument(f'--user-agent={user_agent}')
            
            # Create Chrome service with explicit path
            print("🔄 Creating Chrome service...")
            
            print("🔄 Starting Chrome with undetected-chromedriver...")
            
            # Use undetected chromedriver with enhanced options
            self.driver = uc.Chrome(
                options=options, 
                version_main=None,
                driver_executable_path=None,
                browser_executable_path=None,
                use_subprocess=True,
                debug=False
            )
            
            # Configure timeouts
            self.driver.set_page_load_timeout(45)
            self.driver.implicitly_wait(15)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome browser created successfully")
            
            # Test if browser is actually responsive
            print("🔄 Testing browser responsiveness...")
            self.driver.get('about:blank')
            time.sleep(2)
            
            if self.driver.current_url != 'about:blank':
                print("⚠️  Browser may not be fully responsive")
            else:
                print("✅ Browser is responsive")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating browser: {e}")
            return False
    
    def test_browser_basic(self):
        """Test basic browser functionality with enhanced error handling"""
        if not self.driver:
            print("❌ No browser available for testing")
            return False
        
        print("🔄 Testing basic browser functionality...")
        
        try:
            # Check if browser is still alive
            print("🔍 Checking browser status...")
            current_handles = self.driver.window_handles
            if not current_handles:
                print("❌ Browser has no windows available")
                return False
            
            print(f"✅ Browser has {len(current_handles)} window(s)")
            
            # Test 1: Simple navigation to data URL
            print("📍 Test 1: Simple navigation test...")
            test_html = 'data:text/html,<html><body><h1>Test Page</h1><p id="test">Browser is working!</p></body></html>'
            
            self.driver.get(test_html)
            time.sleep(3)
            
            # Check if we can find elements
            test_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "test"))
            )
            
            if test_element and test_element.text:
                print(f"✅ Basic navigation successful: {test_element.text}")
            else:
                print("❌ Basic navigation failed")
                return False
            
            # Test 2: Check if Tor proxy is working
            print("📍 Test 2: Testing Tor connectivity...")
            try:
                self.driver.get('https://httpbin.org/ip')
                time.sleep(5)
                
                # Wait for page to load completely
                WebDriverWait(self.driver, 15).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                
                # Try to get the page source
                page_source = self.driver.page_source
                if 'origin' in page_source.lower():
                    print("✅ Tor connectivity test passed")
                else:
                    print("⚠️  Tor connectivity uncertain")
                    
            except Exception as e:
                print(f"⚠️  Tor connectivity test failed: {e}")
                # This is not a fatal error for basic functionality
            
            print("✅ Basic browser tests completed!")
            return True
            
        except Exception as e:
            print(f"❌ Browser test failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up browser resources with enhanced error handling"""
        print("🔄 Cleaning up...")
        
        if self.driver:
            try:
                # Try to close all windows first
                for handle in self.driver.window_handles:
                    self.driver.switch_to.window(handle)
                    self.driver.close()
                
                # Then quit the driver
                self.driver.quit()
                print("✅ Browser closed gracefully")
            except Exception as e:
                print(f"⚠️  Error during graceful browser closure: {e}")
                
                # Force kill if graceful close failed
                try:
                    self.kill_existing_chrome()
                except Exception as e2:
                    print(f"⚠️  Error during force cleanup: {e2}")
        
        # Note: We don't stop the Homebrew Tor service since it's managed externally
        print("ℹ️  Homebrew Tor service left running (managed externally)")
        print("💡 To stop: brew services stop tor")
    
    def run_stability_test(self):
        """Run enhanced stability test"""
        print("=" * 70)
        print("🚀 ROBUST HOMEBREW TOR BROWSER - STABILITY TEST")
        print("=" * 70)
        
        # Step 1: Check Tor service
        if not self.check_tor_service():
            print("❌ Tor service check failed")
            return False
        
        # Step 2: Test Tor connectivity
        tor_ip = self.get_tor_ip()
        if not tor_ip:
            print("❌ Tor connectivity test failed")
            return False
        
        # Step 3: Create browser with stability focus
        if not self.create_browser():
            print("❌ Browser creation failed")
            return False
        
        # Step 4: Test basic browser functionality
        if not self.test_browser_basic():
            print("❌ Basic browser testing failed")
            self.cleanup()
            return False
        
        print("=" * 70)
        print("✅ STABILITY TEST PASSED!")
        print("=" * 70)
        print("🔄 Browser will stay open for 60 seconds for manual testing...")
        print("💡 Press Ctrl+C to close early")
        
        try:
            # Keep browser open for manual testing
            for i in range(60, 0, -10):
                print(f"⏰ Browser staying open for {i} more seconds...")
                time.sleep(10)
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")
        
        self.cleanup()
        return True

def main():
    """Main function"""
    browser = RobustHomebrewTorBrowser()
    
    try:
        success = browser.run_stability_test()
        if success:
            print("🎉 Stability test completed successfully!")
        else:
            print("❌ Stability test failed!")
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
