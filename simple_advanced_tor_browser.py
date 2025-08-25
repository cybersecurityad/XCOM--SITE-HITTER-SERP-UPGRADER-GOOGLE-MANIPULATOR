#!/usr/bin/env python3
"""
Simple Advanced Tor Browser - No Auto-Logging
============================================

Advanced browser automation without comprehensive logging system.
Uses the working Homebrew Tor configuration with all advanced features.
"""

import time
import random
import subprocess
import socket
import signal
import sys
import json
import os
import glob
import shutil
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from contextlib import closing
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import requests


@dataclass
class SimpleTorConfig:
    """Simple configuration for advanced Tor browser automation"""
    # Tor settings
    tor_port: int = 9050
    auto_start_tor: bool = True
    verify_tor_ip: bool = True
    use_dutch_exit_nodes_only: bool = False  # NEW: Force Dutch exit nodes only
    
    # Browser settings
    page_load_timeout: int = 30
    implicit_wait: int = 10
    window_size: tuple = (1920, 1080)
    headless: bool = False
    
    # Human behavior simulation
    min_delay: float = 1.0
    max_delay: float = 3.0
    simulate_mouse_movements: bool = True
    
    # Advanced features
    save_screenshots: bool = False
    extract_data: bool = True
    rotate_user_agents: bool = True


class SimpleAdvancedTorBrowser:
    """Advanced Tor browser without comprehensive logging"""
    
    def __init__(self, config: Optional[SimpleTorConfig] = None):
        self.config = config or SimpleTorConfig()
        self.driver: Optional[uc.Chrome] = None
        self.tor_running = False
        self.tor_process = None  # For Dutch-only Tor process
        self.torrc_path = None   # For Dutch-only Tor config
        self.session_data = {
            'start_time': time.time(),
            'requests_made': 0,
            'tor_ip': None,
            'pages_visited': []
        }
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        mode = "🇳🇱 Dutch-only" if self.config.use_dutch_exit_nodes_only else "🌍 Global"
        print(f"🚀 Simple Advanced Tor Browser initialized ({mode} exit nodes)")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"⚠️  Signal {signum} received - shutting down...")
        self.cleanup()
        sys.exit(0)
    
    # ===== TOR MANAGEMENT =====
    
    def check_homebrew_tor(self) -> bool:
        """Check if Homebrew Tor service is running"""
        try:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                sock.settimeout(5)
                result = sock.connect_ex(('127.0.0.1', self.config.tor_port))
                if result == 0:
                    self.tor_running = True
                    print("✅ Homebrew Tor service detected")
                    return True
                return False
        except Exception as e:
            print(f"❌ Error checking Tor service: {e}")
            return False
    
    def start_homebrew_tor(self) -> bool:
        """Start Homebrew Tor service if needed"""
        if self.check_homebrew_tor():
            return True
        
        print("🔄 Starting Homebrew Tor service...")
        
        # Check if Dutch-only exit nodes are requested
        if self.config.use_dutch_exit_nodes_only:
            return self.start_dutch_only_tor()
        else:
            return self.start_default_tor()
    
    def start_default_tor(self) -> bool:
        """Start default Homebrew Tor service"""
        try:
            result = subprocess.run(['brew', 'services', 'start', 'tor'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("✅ Homebrew Tor service started (global exit nodes)")
                time.sleep(5)
                return self.check_homebrew_tor()
            else:
                print(f"❌ Failed to start Tor: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error starting Tor: {e}")
            return False
    
    def start_dutch_only_tor(self) -> bool:
        """Start Tor with Dutch exit nodes only"""
        try:
            print("🇳🇱 Starting Tor with Dutch exit nodes only...")
            
            # Stop existing Tor service
            subprocess.run(['brew', 'services', 'stop', 'tor'], 
                         capture_output=True)
            time.sleep(2)
            
            # Create temporary torrc for Dutch-only
            torrc_content = f"""
# Dutch-only Tor configuration
SocksPort {self.config.tor_port}
DataDirectory /tmp/tor_dutch_data_{os.getpid()}
ExitNodes {{nl}}
StrictNodes 1
Log notice stdout
"""
            
            # Write torrc file
            self.torrc_path = f"/tmp/torrc_dutch_{os.getpid()}"
            with open(self.torrc_path, 'w') as f:
                f.write(torrc_content)
            
            print(f"📝 Dutch-only torrc created: {self.torrc_path}")
            
            # Start Tor with custom config
            cmd = ['/opt/homebrew/bin/tor', '-f', self.torrc_path]
            print(f"🚀 Starting Dutch-only Tor: {' '.join(cmd)}")
            
            self.tor_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for Tor to start
            print("⏰ Waiting for Dutch-only Tor to start...")
            for i in range(30):  # 30 second timeout
                if self.check_homebrew_tor():
                    print("✅ Dutch-only Tor service started successfully")
                    return True
                time.sleep(1)
                print(f"   Waiting... {i+1}/30")
            
            print("❌ Dutch-only Tor failed to start within timeout")
            return False
            
        except Exception as e:
            print(f"❌ Error starting Dutch-only Tor: {e}")
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
            tor_ip = response.json()['origin']
            self.session_data['tor_ip'] = tor_ip
            print(f"✅ Tor IP verified: {tor_ip}")
            return tor_ip
        except Exception as e:
            print(f"❌ Error getting Tor IP: {e}")
            return None
    
    # ===== BROWSER MANAGEMENT =====
    
    def get_user_agent(self) -> str:
        """Get random user agent"""
        return random.choice(self.user_agents)
    
    def create_browser(self) -> bool:
        """Create Chrome browser with Tor proxy"""
        if not self.tor_running:
            print("❌ Tor service not running")
            return False
        
        try:
            print("🔄 Creating Chrome browser with Tor proxy...")
            
            # Chrome options (exact working config)
            options = Options()
            
            # Tor proxy
            options.add_argument(f'--proxy-server=socks5://127.0.0.1:{self.config.tor_port}')
            
            # Basic stability options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            # User agent
            user_agent = self.get_user_agent()
            options.add_argument(f'--user-agent={user_agent}')
            print(f"🔧 User agent: {user_agent[:50]}...")
            
            # Window settings
            if self.config.headless:
                options.add_argument('--headless')
            options.add_argument(f'--window-size={self.config.window_size[0]},{self.config.window_size[1]}')
            
            # Create driver
            self.driver = uc.Chrome(options=options)
            
            # Configure timeouts
            self.driver.set_page_load_timeout(self.config.page_load_timeout)
            self.driver.implicitly_wait(self.config.implicit_wait)
            
            # Anti-detection
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome browser created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error creating browser: {e}")
            return False
    
    def setup(self) -> bool:
        """Complete setup process"""
        print("🚀 Setting up advanced Tor browser...")
        
        # Step 1: Tor setup
        if self.config.auto_start_tor:
            if not self.start_homebrew_tor():
                print("❌ Failed to start Tor service")
                return False
        else:
            if not self.check_homebrew_tor():
                print("❌ Tor service not running")
                return False
        
        # Step 2: Verify Tor connectivity
        if self.config.verify_tor_ip:
            tor_ip = self.get_tor_ip()
            if not tor_ip:
                print("❌ Could not verify Tor connectivity")
                return False
        
        # Step 3: Create browser
        if not self.create_browser():
            print("❌ Failed to create browser")
            return False
        
        print("✅ Advanced Tor browser setup completed!")
        return True
    
    # ===== ADVANCED NAVIGATION =====
    
    def navigate_with_behavior(self, url: str) -> bool:
        """Navigate with human behavior simulation"""
        if not self.driver:
            print("❌ Browser not initialized")
            return False
        
        try:
            print(f"🌐 Navigating to: {url}")
            
            # Pre-navigation delay
            time.sleep(random.uniform(0.5, 2.0))
            
            # Navigate
            self.driver.get(url)
            self.session_data['requests_made'] += 1
            self.session_data['pages_visited'].append({
                'url': url,
                'timestamp': time.time()
            })
            
            # Wait for page load
            try:
                WebDriverWait(self.driver, self.config.page_load_timeout).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
            except TimeoutException:
                print(f"⚠️  Page load timeout for {url}")
            
            # Human behavior
            reading_time = random.uniform(self.config.min_delay, self.config.max_delay)
            print(f"📖 Reading for {reading_time:.1f}s")
            time.sleep(reading_time)
            
            # Mouse movements
            if self.config.simulate_mouse_movements:
                self.simulate_mouse_movements()
            
            print(f"✅ Successfully navigated to: {self.driver.title}")
            return True
            
        except Exception as e:
            print(f"❌ Error navigating to {url}: {e}")
            return False
    
    def simulate_mouse_movements(self):
        """Simulate realistic mouse movements"""
        if not self.driver:
            return
            
        try:
            actions = ActionChains(self.driver)
            
            # Random movements
            for _ in range(random.randint(2, 5)):
                x_offset = random.randint(-100, 100)
                y_offset = random.randint(-50, 50)
                actions.move_by_offset(x_offset, y_offset)
                actions.pause(random.uniform(0.1, 0.3))
            
            actions.perform()
            
        except Exception:
            pass  # Silent fail for mouse movements
    
    def scroll_page(self) -> bool:
        """Scroll page naturally"""
        if not self.driver:
            return False
        
        try:
            # Natural scrolling
            for _ in range(random.randint(3, 6)):
                scroll_amount = random.randint(200, 400)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(0.8, 2.0))
                
            return True
            
        except Exception as e:
            print(f"❌ Error scrolling: {e}")
            return False
    
    def extract_basic_data(self) -> Dict[str, Any]:
        """Extract basic page data"""
        if not self.driver:
            return {}
        
        try:
            data = {
                'title': self.driver.title,
                'url': self.driver.current_url,
                'timestamp': time.time()
            }
            
            if self.config.extract_data:
                # Basic counts
                data['stats'] = {
                    'links': len(self.driver.find_elements(By.TAG_NAME, "a")),
                    'images': len(self.driver.find_elements(By.TAG_NAME, "img")),
                    'forms': len(self.driver.find_elements(By.TAG_NAME, "form"))
                }
            
            return data
            
        except Exception as e:
            print(f"❌ Error extracting data: {e}")
            return {}
    
    def save_screenshot(self, filename: Optional[str] = None):
        """Save screenshot"""
        if not self.config.save_screenshots or not self.driver:
            return
            
        try:
            if not filename:
                timestamp = int(time.time())
                filename = f"screenshot_{timestamp}.png"
            
            self.driver.save_screenshot(filename)
            print(f"📸 Screenshot saved: {filename}")
            
        except Exception as e:
            print(f"⚠️  Could not save screenshot: {e}")
    
    def comprehensive_page_visit(self, url: str) -> Dict[str, Any]:
        """Visit page with all advanced features"""
        results = {
            'url': url,
            'success': False,
            'timestamp': time.time()
        }
        
        try:
            # Navigate
            if not self.navigate_with_behavior(url):
                return results
            
            # Scroll
            self.scroll_page()
            
            # Extract data
            page_data = self.extract_basic_data()
            results['page_data'] = page_data
            
            # Screenshot
            self.save_screenshot()
            
            results['success'] = True
            print(f"✅ Comprehensive visit completed: {url}")
            
        except Exception as e:
            print(f"❌ Error during comprehensive visit: {e}")
            results['error'] = str(e)
        
        return results
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get session summary"""
        duration = time.time() - self.session_data['start_time']
        
        return {
            'duration_minutes': round(duration / 60, 1),
            'requests_made': self.session_data['requests_made'],
            'tor_ip': self.session_data['tor_ip'],
            'pages_visited': len(self.session_data['pages_visited'])
        }
    
    def cleanup(self):
        """Clean shutdown"""
        print("🔄 Cleaning up...")
        
        # Print summary
        summary = self.get_session_summary()
        print("📊 SESSION SUMMARY:")
        for key, value in summary.items():
            print(f"   {key}: {value}")
        
        # Close browser
        if self.driver:
            try:
                self.driver.quit()
                print("✅ Browser closed")
            except Exception as e:
                print(f"⚠️  Error closing browser: {e}")
        
        # Clean up Dutch-only Tor if running
        if self.config.use_dutch_exit_nodes_only:
            self.cleanup_dutch_tor()
        
        print("✅ Cleanup completed")
    
    def cleanup_dutch_tor(self):
        """Clean up Dutch-only Tor process and files"""
        try:
            # Stop custom Tor process
            if self.tor_process:
                print("🔄 Stopping Dutch-only Tor process...")
                self.tor_process.terminate()
                try:
                    self.tor_process.wait(timeout=5)
                    print("✅ Dutch-only Tor process stopped")
                except subprocess.TimeoutExpired:
                    self.tor_process.kill()
                    print("⚠️  Dutch-only Tor process force killed")
            
            # Remove temporary torrc file
            if self.torrc_path and os.path.exists(self.torrc_path):
                os.remove(self.torrc_path)
                print(f"🗑️  Removed torrc: {self.torrc_path}")
            
            # Clean up data directory
            data_dirs = glob.glob(f"/tmp/tor_dutch_data_{os.getpid()}")
            for data_dir in data_dirs:
                shutil.rmtree(data_dir, ignore_errors=True)
                print(f"🗑️  Removed data dir: {data_dir}")
            
        except Exception as e:
            print(f"⚠️  Error cleaning up Dutch-only Tor: {e}")
        
        # Restart default Homebrew Tor service
        try:
            print("🔄 Restarting default Homebrew Tor service...")
            subprocess.run(['brew', 'services', 'start', 'tor'], 
                         capture_output=True, timeout=10)
            print("✅ Default Homebrew Tor service restored")
        except Exception as e:
            print(f"⚠️  Error restarting default Tor: {e}")


def main():
    """Demonstration without auto-logging"""
    print("🚀 SIMPLE ADVANCED TOR BROWSER")
    print("=" * 50)
    
    # Create configuration
    config = SimpleTorConfig(
        auto_start_tor=True,
        verify_tor_ip=True,
        save_screenshots=False,
        simulate_mouse_movements=True
    )
    
    # Create browser
    browser = SimpleAdvancedTorBrowser(config)
    
    try:
        # Setup
        if not browser.setup():
            print("❌ Setup failed!")
            return
        
        # Test URLs
        test_urls = [
            "https://httpbin.org/ip",
            "https://httpbin.org/headers",
            "https://check.torproject.org"
        ]
        
        # Visit each URL with advanced features
        for i, url in enumerate(test_urls):
            print(f"\n🔍 Test {i+1}/{len(test_urls)}: {url}")
            
            results = browser.comprehensive_page_visit(url)
            
            if results['success']:
                print(f"✅ Visit completed successfully")
            else:
                print(f"❌ Visit failed: {results.get('error', 'Unknown error')}")
            
            # Delay between pages
            if i < len(test_urls) - 1:
                delay = random.uniform(2, 5)
                print(f"⏰ Waiting {delay:.1f}s...")
                time.sleep(delay)
        
        print("\n✅ All tests completed!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        browser.cleanup()


if __name__ == "__main__":
    main()
