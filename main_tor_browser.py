#!/usr/bin/env python3
"""
Main Tor Browser Implementation - Homebrew Tor Integration
========================================================

Simple, reliable browser automation with Homebrew Tor service integration.
This resolves all exit code 15 issues by using the stable Homebrew Tor approach.
"""

import time
import random
import subprocess
import socket
import signal
import sys
from typing import List, Optional
from dataclasses import dataclass
from contextlib import closing
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


@dataclass
class TorBrowserConfig:
    """Configuration for Tor browser automation"""
    tor_port: int = 9050
    auto_start_tor: bool = True
    page_load_timeout: int = 30
    implicit_wait: int = 10
    min_delay: float = 2.0
    max_delay: float = 5.0
    user_agent: str = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


class MainTorBrowser:
    """Main Tor browser implementation using Homebrew Tor service"""
    
    def __init__(self, config: Optional[TorBrowserConfig] = None):
        self.config = config or TorBrowserConfig()
        self.driver = None
        self.tor_running = False
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n⚠️  Signal {signum} received - shutting down...")
        self.cleanup()
        sys.exit(0)
    
    def check_homebrew_tor(self) -> bool:
        """Check if Homebrew Tor service is running"""
        try:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                sock.settimeout(5)
                result = sock.connect_ex(('127.0.0.1', self.config.tor_port))
                if result == 0:
                    self.tor_running = True
                    return True
                return False
        except Exception:
            return False
    
    def start_homebrew_tor(self) -> bool:
        """Start Homebrew Tor service if needed"""
        if self.check_homebrew_tor():
            print("✅ Homebrew Tor service is already running")
            return True
            
        print("🔄 Starting Homebrew Tor service...")
        try:
            result = subprocess.run(['brew', 'services', 'start', 'tor'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("✅ Homebrew Tor service started")
                time.sleep(3)  # Give Tor time to start
                return self.check_homebrew_tor()
            else:
                print(f"❌ Failed to start Tor: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error starting Tor: {e}")
            return False
    
    def get_tor_ip(self) -> Optional[str]:
        """Get current Tor IP address"""
        if not self.tor_running:
            return None
            
        proxies = {
            'http': f'socks5://127.0.0.1:{self.config.tor_port}',
            'https': f'socks5://127.0.0.1:{self.config.tor_port}'
        }
        
        try:
            response = requests.get('https://httpbin.org/ip', 
                                  proxies=proxies, timeout=15)
            return response.json()['origin']
        except Exception:
            return None
    
    def create_browser(self) -> bool:
        """Create Chrome browser with Tor proxy"""
        if not self.tor_running:
            print("❌ Tor service not running")
            return False
        
        try:
            print("🔄 Creating Chrome browser with Tor proxy...")
            
            # Chrome options for Tor
            options = Options()
            options.add_argument(f'--proxy-server=socks5://127.0.0.1:{self.config.tor_port}')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'--user-agent={self.config.user_agent}')
            
            # Create browser
            self.driver = uc.Chrome(options=options)
            
            # Configure timeouts
            self.driver.set_page_load_timeout(self.config.page_load_timeout)
            self.driver.implicitly_wait(self.config.implicit_wait)
            
            print("✅ Chrome browser created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error creating browser: {e}")
            return False
    
    def setup(self) -> bool:
        """Setup Tor and browser"""
        print("🚀 Setting up Tor browser...")
        
        # Step 1: Check/start Tor
        if self.config.auto_start_tor:
            if not self.start_homebrew_tor():
                print("❌ Failed to start Tor service")
                return False
        else:
            if not self.check_homebrew_tor():
                print("❌ Tor service not running")
                return False
        
        # Step 2: Verify Tor connectivity
        tor_ip = self.get_tor_ip()
        if not tor_ip:
            print("❌ Could not verify Tor connectivity")
            return False
        print(f"✅ Tor IP verified: {tor_ip}")
        
        # Step 3: Create browser
        if not self.create_browser():
            print("❌ Failed to create browser")
            return False
        
        print("✅ Tor browser setup completed successfully!")
        return True
    
    def navigate(self, url: str) -> bool:
        """Navigate to a URL with human-like behavior"""
        if not self.driver:
            print("❌ Browser not initialized")
            return False
        
        try:
            print(f"🌐 Navigating to: {url}")
            self.driver.get(url)
            
            # Human-like delay
            delay = random.uniform(self.config.min_delay, self.config.max_delay)
            time.sleep(delay)
            
            print(f"✅ Successfully loaded: {self.driver.title}")
            return True
            
        except Exception as e:
            print(f"❌ Error navigating to {url}: {e}")
            return False
    
    def scroll_page(self, scrolls: int = 3) -> bool:
        """Scroll page with human-like behavior"""
        if not self.driver:
            return False
        
        try:
            for i in range(scrolls):
                # Scroll to different positions
                if i == 0:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
                elif i == 1:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                else:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Human-like pause
                delay = random.uniform(1.0, 3.0)
                time.sleep(delay)
            
            return True
        except Exception as e:
            print(f"❌ Error scrolling: {e}")
            return False
    
    def get_page_info(self) -> dict:
        """Get basic page information"""
        if not self.driver:
            return {}
        
        try:
            return {
                'title': self.driver.title,
                'url': self.driver.current_url,
                'page_source_length': len(self.driver.page_source)
            }
        except Exception:
            return {}
    
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
    
    def test_connectivity(self) -> bool:
        """Test basic connectivity"""
        test_urls = [
            "https://httpbin.org/ip",
            "https://httpbin.org/user-agent"
        ]
        
        for url in test_urls:
            if not self.navigate(url):
                return False
            
            # Get page info
            info = self.get_page_info()
            print(f"📄 Page info: {info}")
            
            # Scroll the page
            self.scroll_page(2)
            
        return True


def main():
    """Main function for testing"""
    config = TorBrowserConfig(auto_start_tor=True)
    browser = MainTorBrowser(config)
    
    try:
        # Setup
        if not browser.setup():
            print("❌ Setup failed!")
            return False
        
        # Test connectivity
        if not browser.test_connectivity():
            print("❌ Connectivity test failed!")
            return False
        
        print("✅ All tests passed!")
        print("🔄 Browser will stay open for 30 seconds...")
        time.sleep(30)
        
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        browser.cleanup()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
