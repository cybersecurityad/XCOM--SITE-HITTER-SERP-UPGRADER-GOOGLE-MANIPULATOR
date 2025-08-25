#!/usr/bin/env python3
"""
Advanced Dutch-only Tor Browser with IP rotation and User Agent rotation
Uses httpbin.org for testing IP and user agent changes
"""

import random
import time
import json
import os
import sys
import subprocess
import tempfile
import glob
import shutil
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException

@dataclass
class DutchRotationConfig:
    """Configuration for Dutch-only rotating Tor browser"""
    tor_port: int = 9050
    control_port: int = 9051
    min_delay: float = 3.0
    max_delay: float = 8.0
    headless: bool = False
    save_screenshots: bool = True
    rotation_interval: int = 5  # Rotate IP every N requests
    max_retries: int = 3
    user_agent_rotation: bool = True
    verify_dutch_ip: bool = True
    
    # Dutch-specific settings
    use_dutch_exit_nodes_only: bool = True
    verify_geolocation: bool = True

class DutchRotationBrowser:
    """Advanced Dutch-only Tor browser with rotation capabilities"""
    
    def __init__(self, config: Optional[DutchRotationConfig] = None):
        self.config = config or DutchRotationConfig()
        self.driver: Optional[webdriver.Chrome] = None
        self.tor_process: Optional[subprocess.Popen] = None
        self.tor_data_dir: Optional[str] = None
        self.session_data = {
            'start_time': datetime.now().isoformat(),
            'requests': [],
            'ip_changes': [],
            'user_agents': [],
            'errors': []
        }
        self.request_count = 0
        self.current_ip: Optional[str] = None
        self.current_user_agent: Optional[str] = None
        
        # Dutch user agents
        self.dutch_user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
        ]
    
    def setup(self) -> bool:
        """Setup Dutch-only Tor browser with rotation capabilities"""
        try:
            print("🇳🇱 Setting up Dutch-only Tor browser with rotation...")
            
            # Use Homebrew Tor service instead of starting our own
            if not self._setup_homebrew_tor():
                return False
            
            # Wait for Tor to be ready
            time.sleep(3)
            
            # Setup browser
            if not self._setup_browser():
                return False
            
            # Verify Dutch IP
            if self.config.verify_dutch_ip:
                if not self._verify_dutch_ip():
                    print("⚠️  Warning: IP might not be from Netherlands")
            
            print("✅ Dutch rotation browser setup complete!")
            return True
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False
    
    def _setup_homebrew_tor(self) -> bool:
        """Setup Homebrew Tor service with Dutch-only configuration"""
        try:
            print("🍺 Setting up Homebrew Tor service...")
            
            # Stop any existing Tor service
            subprocess.run(['brew', 'services', 'stop', 'tor'], 
                         capture_output=True, text=True)
            time.sleep(2)
            
            # Create custom torrc in user directory
            self.tor_data_dir = tempfile.mkdtemp(prefix="dutch_tor_homebrew_")
            
            torrc_content = f"""
# Dutch-only exit nodes configuration
DataDirectory {self.tor_data_dir}
SocksPort {self.config.tor_port}
ControlPort {self.config.control_port}

# Force Dutch exit nodes only
ExitNodes {{nl}}
StrictNodes 1

# Additional security settings
ExcludeNodes {{??}}
ExcludeExitNodes {{??}}

# Performance settings
CircuitBuildTimeout 30
LearnCircuitBuildTimeout 0
MaxCircuitDirtiness 300

# Logging
Log notice stdout
"""
            
            # Write custom torrc
            torrc_path = os.path.join(self.tor_data_dir, "torrc")
            with open(torrc_path, 'w') as f:
                f.write(torrc_content)
            
            print(f"🔧 Created Dutch-only torrc: {torrc_path}")
            
            # Start Tor with custom config using subprocess
            cmd = ['/opt/homebrew/bin/tor', '-f', torrc_path]
            self.tor_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            print("✅ Started Tor with Dutch-only configuration!")
            
            # Wait for Tor to bootstrap
            print("⏳ Waiting for Tor to bootstrap...")
            time.sleep(8)
            
            # Check if Tor is still running
            if self.tor_process.poll() is not None:
                stdout, stderr = self.tor_process.communicate()
                print(f"❌ Tor failed: {stderr}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup Homebrew Tor: {e}")
            return False
    
    def _start_dutch_tor(self) -> bool:
        """Start Tor with Dutch-only exit nodes"""
        try:
            # Create temporary directory for Tor data
            self.tor_data_dir = tempfile.mkdtemp(prefix="dutch_tor_")
            
            # Create custom torrc for Dutch-only exits
            torrc_content = f"""
# Dutch-only exit nodes configuration
DataDirectory {self.tor_data_dir}
SocksPort {self.config.tor_port}
ControlPort {self.config.control_port}

# Force Dutch exit nodes only
ExitNodes {{nl}}
StrictNodes 1

# Additional security
ExcludeNodes {{??}}
ExcludeExitNodes {{??}}

# Performance settings
CircuitBuildTimeout 30
LearnCircuitBuildTimeout 0
MaxCircuitDirtiness 300

# Logging
Log notice stdout
"""
            
            torrc_path = os.path.join(self.tor_data_dir, "torrc")
            with open(torrc_path, 'w') as f:
                f.write(torrc_content)
            
            print(f"🔧 Starting Dutch-only Tor with config: {torrc_path}")
            
            # Start Tor process
            cmd = ['tor', '-f', torrc_path]
            self.tor_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Wait for Tor to bootstrap
            print("⏳ Waiting for Tor to bootstrap...")
            time.sleep(10)
            
            if self.tor_process.poll() is not None:
                stdout, stderr = self.tor_process.communicate()
                print(f"❌ Tor failed to start: {stderr}")
                return False
            
            print("✅ Dutch-only Tor started successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Dutch Tor: {e}")
            return False
    
    def _setup_browser(self) -> bool:
        """Setup Chrome with Tor proxy and random user agent"""
        try:
            # Select random user agent
            if self.config.user_agent_rotation:
                self.current_user_agent = random.choice(self.dutch_user_agents)
            else:
                self.current_user_agent = self.dutch_user_agents[0]
            
            print(f"🎭 Using user agent: {self.current_user_agent[:50]}...")
            
            # Chrome options
            options = uc.ChromeOptions()
            
            # Tor proxy settings
            options.add_argument(f'--proxy-server=socks5://127.0.0.1:{self.config.tor_port}')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-images')
            options.add_argument(f'--user-agent={self.current_user_agent}')
            
            if self.config.headless:
                options.add_argument('--headless=new')
            
            # Create driver without experimental options that cause issues
            self.driver = uc.Chrome(options=options)
            
            # Set webdriver property after creation
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Browser setup complete!")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
    
    def _verify_dutch_ip(self) -> bool:
        """Verify that we're using a Dutch IP"""
        try:
            if not self.driver:
                print("❌ No browser driver available")
                return False
                
            print("🇳🇱 Verifying Dutch IP address...")
            
            # Get IP info from httpbin
            self.driver.get("http://httpbin.org/ip")
            time.sleep(3)
            
            # Extract IP
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            ip_data = json.loads(body_text)
            self.current_ip = ip_data.get('origin', 'Unknown')
            
            print(f"🌐 Current IP: {self.current_ip}")
            
            # Check geolocation
            self.driver.get("http://ip-api.com/json/")
            time.sleep(3)
            
            geo_text = self.driver.find_element(By.TAG_NAME, "body").text
            geo_data = json.loads(geo_text)
            
            country = geo_data.get('country', 'Unknown')
            country_code = geo_data.get('countryCode', 'Unknown')
            city = geo_data.get('city', 'Unknown')
            
            print(f"🗺️  Location: {city}, {country} ({country_code})")
            
            # Record IP change
            self.session_data['ip_changes'].append({
                'timestamp': datetime.now().isoformat(),
                'ip': self.current_ip,
                'country': country,
                'country_code': country_code,
                'city': city
            })
            
            is_dutch = country_code.lower() == 'nl'
            if is_dutch:
                print("✅ Confirmed: Using Dutch IP address!")
            else:
                print(f"⚠️  Warning: IP appears to be from {country}, not Netherlands")
            
            return is_dutch
            
        except Exception as e:
            print(f"❌ IP verification failed: {e}")
            return False
    
    def rotate_identity(self) -> bool:
        """Rotate Tor identity and user agent"""
        try:
            print("🔄 Rotating identity...")
            
            # Close current browser
            if self.driver:
                self.driver.quit()
                time.sleep(2)
            
            # Stop current Tor and restart with new circuit
            if self.tor_process:
                self.tor_process.terminate()
                self.tor_process.wait()
                time.sleep(3)
            
            # Start new Tor session
            if not self._setup_homebrew_tor():
                return False
            
            time.sleep(5)
            
            # Setup new browser with new user agent
            if not self._setup_browser():
                return False
            
            # Verify new IP
            if self.config.verify_dutch_ip:
                self._verify_dutch_ip()
            
            print("✅ Identity rotation complete!")
            return True
            
        except Exception as e:
            print(f"❌ Identity rotation failed: {e}")
            return False
    
    def visit_with_rotation(self, url: str) -> bool:
        """Visit URL with automatic rotation based on request count"""
        try:
            # Check if rotation is needed
            if (self.request_count > 0 and 
                self.request_count % self.config.rotation_interval == 0):
                print(f"🔄 Auto-rotating after {self.request_count} requests...")
                if not self.rotate_identity():
                    print("⚠️  Rotation failed, continuing with current identity")
            
            return self._visit_url(url)
            
        except Exception as e:
            print(f"❌ Visit with rotation failed: {e}")
            return False
    
    def _visit_url(self, url: str) -> bool:
        """Visit a single URL"""
        try:
            if not self.driver:
                print("❌ No browser driver available")
                return False
                
            start_time = time.time()
            print(f"🌐 Visiting: {url}")
            
            self.driver.get(url)
            
            # Random delay
            delay = random.uniform(self.config.min_delay, self.config.max_delay)
            time.sleep(delay)
            
            # Take screenshot if enabled
            if self.config.save_screenshots:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"dutch_rotation_{timestamp}.png"
                self.driver.save_screenshot(screenshot_path)
                print(f"📸 Screenshot saved: {screenshot_path}")
            
            # Record request
            self.request_count += 1
            user_agent_display = self.current_user_agent[:100] if self.current_user_agent else "Unknown"
            self.session_data['requests'].append({
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'duration': time.time() - start_time,
                'ip': self.current_ip,
                'user_agent': user_agent_display,
                'request_number': self.request_count
            })
            
            print(f"✅ Successfully visited {url} (Request #{self.request_count})")
            return True
            
        except Exception as e:
            print(f"❌ Failed to visit {url}: {e}")
            self.session_data['errors'].append({
                'url': url,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return False
    
    def test_httpbin_features(self):
        """Test various httpbin endpoints to verify rotation"""
        print("🧪 Testing httpbin features with rotation...")
        
        test_urls = [
            "http://httpbin.org/ip",
            "http://httpbin.org/user-agent",
            "http://httpbin.org/headers",
            "http://httpbin.org/get",
            "http://httpbin.org/anything",
            "http://httpbin.org/status/200",
            "http://httpbin.org/delay/2",
            "http://httpbin.org/cache/60"
        ]
        
        for i, url in enumerate(test_urls):
            print(f"\n--- Test {i+1}/{len(test_urls)} ---")
            self.visit_with_rotation(url)
            
            # Show current status
            print(f"📊 Current IP: {self.current_ip}")
            ua_display = self.current_user_agent[:50] if self.current_user_agent else "Unknown"
            print(f"🎭 Current UA: {ua_display}...")
            print(f"📈 Total requests: {self.request_count}")
    
    def save_session_data(self):
        """Save session data to JSON file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dutch_rotation_session_{timestamp}.json"
            
            self.session_data['end_time'] = datetime.now().isoformat()
            self.session_data['total_requests'] = self.request_count
            self.session_data['total_ip_changes'] = len(self.session_data['ip_changes'])
            
            with open(filename, 'w') as f:
                json.dump(self.session_data, f, indent=2)
            
            print(f"💾 Session data saved: {filename}")
            
        except Exception as e:
            print(f"❌ Failed to save session data: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        try:
            print("🧹 Cleaning up Dutch rotation browser...")
            
            # Save session data
            self.save_session_data()
            
            # Close browser
            if self.driver:
                self.driver.quit()
                time.sleep(2)
            
            # Stop Tor process
            if self.tor_process:
                self.tor_process.terminate()
                self.tor_process.wait()
                print("🛑 Stopped Tor process")
            
            # Clean up Tor data directory
            if self.tor_data_dir and os.path.exists(self.tor_data_dir):
                shutil.rmtree(self.tor_data_dir)
                print("🧹 Cleaned up Tor data directory")
            
            print("✅ Cleanup complete!")
            
        except Exception as e:
            print(f"❌ Cleanup error: {e}")

def main():
    """Main demo function"""
    print("🇳🇱 Dutch Rotation Browser Demo")
    print("=" * 40)
    
    # Configure for rotation testing
    config = DutchRotationConfig(
        rotation_interval=3,  # Rotate every 3 requests
        user_agent_rotation=True,
        verify_dutch_ip=True,
        save_screenshots=True
    )
    
    browser = DutchRotationBrowser(config)
    
    try:
        if browser.setup():
            # Test httpbin features with rotation
            browser.test_httpbin_features()
            
            # Additional custom tests
            print("\n🎯 Testing custom URLs...")
            custom_urls = [
                "https://www.nu.nl/",
                "http://httpbin.org/json",
                "https://www.nos.nl/"
            ]
            
            for url in custom_urls:
                browser.visit_with_rotation(url)
        
    except KeyboardInterrupt:
        print("\n⏸️  Test interrupted by user")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    finally:
        browser.cleanup()

if __name__ == "__main__":
    main()
