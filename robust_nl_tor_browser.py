#!/usr/bin/env python3
"""
🇳🇱 ROBUST NETHERLANDS-ONLY TOR BROWSER
=====================================
Enhanced version with better error handling and process management

Features:
- Netherlands-only Tor exit nodes
- Robust browser process management
- Better error handling for process termination
- Automatic restart on crashes
- Enhanced logging
"""

import os
import sys
import time
import signal
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import random
import json
from datetime import datetime
import requests

class RobustNLTorBrowser:
    def __init__(self):
        self.tor_process = None
        self.driver = None
        self.socks_port = 9050
        self.control_port = 9051
        self.current_ip = None
        self.session_log = []
        self.crash_count = 0
        self.max_crashes = 5
        
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
            self.cleanup()
            sys.exit(0)
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def start_tor_service(self):
        """Start Tor service with Netherlands-only configuration"""
        try:
            print(f"🧅 Starting Tor with Netherlands-only exit nodes...")
            
            # Kill any existing Tor processes
            self.stop_tor_service()
            
            # Create torrc configuration
            torrc_content = f"""
# Netherlands-only Tor configuration
SocksPort {self.socks_port}
ControlPort {self.control_port}
ExitNodes {{nl}}
StrictNodes 1
DataDirectory /tmp/tor_data_{os.getpid()}
GeoIPFile /usr/local/share/tor/geoip
GeoIPv6File /usr/local/share/tor/geoip6
Log notice stdout
"""
            
            # Write torrc file
            torrc_path = f"/tmp/torrc_{os.getpid()}"
            with open(torrc_path, 'w') as f:
                f.write(torrc_content)
            
            # Start Tor process
            cmd = ['/opt/homebrew/bin/tor', '-f', torrc_path]
            
            self.tor_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid  # Create new process group
            )
            
            # Wait for Tor to be ready
            print(f"⏳ Waiting for Tor to initialize...")
            for i in range(30):  # Wait up to 30 seconds
                time.sleep(1)
                if self.is_tor_ready():
                    print(f"✅ Tor ready after {i+1} seconds!")
                    
                    # Get current IP
                    self.current_ip = self.get_tor_ip()
                    if self.current_ip:
                        print(f"🇳🇱 Netherlands IP: {self.current_ip}")
                        return True
                    else:
                        print(f"⚠️ Could not determine IP")
                        return False
                        
                print(f"   🔄 Initializing... {i+1}/30")
            
            print(f"❌ Tor failed to start within timeout")
            return False
            
        except Exception as e:
            print(f"❌ Failed to start Tor: {e}")
            return False
    
    def is_tor_ready(self):
        """Check if Tor is ready to accept connections"""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', self.socks_port))
            sock.close()
            return result == 0
        except:
            return False
    
    def get_tor_ip(self):
        """Get current Tor IP address"""
        try:
            proxies = {
                'http': f'socks5://127.0.0.1:{self.socks_port}',
                'https': f'socks5://127.0.0.1:{self.socks_port}'
            }
            
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('origin', 'Unknown')
            else:
                return None
                
        except Exception as e:
            print(f"⚠️ Could not get IP: {e}")
            return None
    
    def verify_netherlands_ip(self, ip):
        """Verify that the IP is from Netherlands"""
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                country_code = data.get('countryCode', '')
                country = data.get('country', '')
                city = data.get('city', '')
                
                if country_code.upper() == 'NL':
                    print(f"✅ Verified Netherlands IP: {city}, {country}")
                    return True
                else:
                    print(f"❌ NOT Netherlands IP: {city}, {country} ({country_code})")
                    return False
            else:
                print(f"⚠️ Could not verify IP location")
                return False
                
        except Exception as e:
            print(f"⚠️ IP verification error: {e}")
            return False
    
    def create_robust_browser(self):
        """Create browser with robust configuration to prevent signal 15 termination"""
        try:
            print(f"🎭 Creating robust browser with anti-termination settings...")
            
            # Chrome options for maximum stability and anti-termination
            chrome_options = uc.ChromeOptions()
            
            # Core stability options
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-software-rasterizer')
            chrome_options.add_argument('--disable-background-timer-throttling')
            chrome_options.add_argument('--disable-backgrounding-occluded-windows')
            chrome_options.add_argument('--disable-renderer-backgrounding')
            chrome_options.add_argument('--disable-features=TranslateUI')
            chrome_options.add_argument('--disable-ipc-flooding-protection')
            
            # Anti-termination options
            chrome_options.add_argument('--disable-hang-monitor')
            chrome_options.add_argument('--disable-prompt-on-repost')
            chrome_options.add_argument('--disable-domain-reliability')
            chrome_options.add_argument('--disable-component-update')
            chrome_options.add_argument('--disable-default-apps')
            chrome_options.add_argument('--disable-sync')
            chrome_options.add_argument('--disable-background-networking')
            chrome_options.add_argument('--disable-breakpad')
            chrome_options.add_argument('--disable-crash-reporter')
            chrome_options.add_argument('--no-crash-upload')
            chrome_options.add_argument('--disable-logging')
            chrome_options.add_argument('--silent')
            chrome_options.add_argument('--log-level=3')
            
            # Process isolation to prevent signal propagation
            chrome_options.add_argument('--no-zygote')
            chrome_options.add_argument('--single-process')
            chrome_options.add_argument('--disable-site-isolation-trials')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            
            # Memory and resource management
            chrome_options.add_argument('--memory-pressure-off')
            chrome_options.add_argument('--disable-background-mode')
            chrome_options.add_argument('--disable-plugins-discovery')
            chrome_options.add_argument('--disable-preconnect')
            
            # Tor proxy configuration
            chrome_options.add_argument(f'--proxy-server=socks5://127.0.0.1:{self.socks_port}')
            chrome_options.add_argument('--proxy-bypass-list=<-loopback>')
            
            # User agent randomization
            ua = UserAgent()
            user_agent = ua.random
            chrome_options.add_argument(f'--user-agent={user_agent}')
            
            # Window management
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-running-insecure-content')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-popup-blocking')
            
            # Experimental options for stability
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            # Create driver with extensive retry logic
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    print(f"🚀 Launching browser (attempt {attempt+1}/{max_retries})...")
                    
                    # Try different approaches based on attempt
                    if attempt == 0:
                        # Standard approach
                        self.driver = uc.Chrome(
                            options=chrome_options,
                            version_main=None,
                            driver_executable_path=None
                        )
                    elif attempt == 1:
                        # Try with headless mode
                        chrome_options.add_argument('--headless=new')
                        self.driver = uc.Chrome(
                            options=chrome_options,
                            version_main=None
                        )
                    elif attempt == 2:
                        # Try minimal options
                        minimal_options = uc.ChromeOptions()
                        minimal_options.add_argument('--no-sandbox')
                        minimal_options.add_argument('--disable-dev-shm-usage')
                        minimal_options.add_argument(f'--proxy-server=socks5://127.0.0.1:{self.socks_port}')
                        self.driver = uc.Chrome(options=minimal_options)
                    elif attempt == 3:
                        # Try with system Chrome
                        from selenium import webdriver
                        from selenium.webdriver.chrome.service import Service
                        from selenium.webdriver.chrome.options import Options
                        
                        # Convert to standard Chrome options
                        std_options = Options()
                        for arg in chrome_options.arguments:
                            std_options.add_argument(arg)
                        
                        service = Service()
                        self.driver = webdriver.Chrome(service=service, options=std_options)
                    else:
                        # Last resort - basic webdriver
                        from selenium import webdriver
                        from selenium.webdriver.chrome.options import Options
                        
                        # Convert to standard Chrome options
                        std_options = Options()
                        for arg in chrome_options.arguments:
                            std_options.add_argument(arg)
                            
                        self.driver = webdriver.Chrome(options=std_options)
                    
                    # Set timeouts
                    self.driver.set_page_load_timeout(30)
                    self.driver.implicitly_wait(10)
                    
                    # Test basic functionality
                    self.driver.get('data:text/html,<html><body><h1>Test Page</h1></body></html>')
                    
                    print(f"✅ Browser created successfully on attempt {attempt+1}!")
                    return True
                    
                except Exception as e:
                    print(f"❌ Browser creation attempt {attempt+1} failed: {e}")
                    
                    # Clean up failed attempt
                    try:
                        if hasattr(self, 'driver') and self.driver:
                            self.driver.quit()
                            self.driver = None
                    except:
                        pass
                    
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 2  # Increasing wait time
                        print(f"🔄 Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        print(f"❌ All browser creation attempts failed")
                        return False
            
            return False
            
        except Exception as e:
            print(f"❌ Browser creation error: {e}")
            return False
    
    def test_browser_connection(self):
        """Test browser connection and IP"""
        try:
            if not self.driver:
                print(f"❌ No browser available for testing")
                return False
                
            print(f"🔍 Testing browser connection...")
            
            # Navigate to IP check page
            self.driver.get('https://httpbin.org/ip')
            
            # Wait for page to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            
            # Get page content
            page_text = self.driver.find_element(By.TAG_NAME, 'body').text
            print(f"🌐 Browser IP check: {page_text}")
            
            # Try to extract IP
            try:
                import json
                data = json.loads(page_text)
                browser_ip = data.get('origin', 'Unknown')
                
                if browser_ip and browser_ip != 'Unknown':
                    print(f"🌐 Browser IP: {browser_ip}")
                    
                    # Verify it's Netherlands
                    if self.verify_netherlands_ip(browser_ip):
                        print(f"✅ Browser successfully using Netherlands IP!")
                        return True
                    else:
                        print(f"❌ Browser NOT using Netherlands IP!")
                        return False
                else:
                    print(f"⚠️ Could not extract IP from browser")
                    return False
                    
            except Exception as e:
                print(f"⚠️ Could not parse IP response: {e}")
                return False
                
        except TimeoutException:
            print(f"❌ Browser connection test timed out")
            return False
        except Exception as e:
            print(f"❌ Browser connection test error: {e}")
            return False
    
    def browse_website(self, url="https://httpbin.org/ip"):
        """Browse a website with error handling"""
        try:
            if not self.driver:
                print(f"❌ No browser available for browsing")
                return False
                
            print(f"🌐 Visiting: {url}")
            
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            
            print(f"✅ Page loaded successfully")
            
            # Simple interaction
            time.sleep(2)
            
            # Scroll a bit
            self.driver.execute_script("window.scrollTo(0, 200);")
            time.sleep(1)
            
            print(f"✅ Basic browsing completed")
            return True
            
        except Exception as e:
            print(f"❌ Browsing error: {e}")
            return False
    
    def monitor_browser_process(self):
        """Enhanced browser process health monitoring"""
        try:
            if not self.driver:
                print(f"⚠️ No driver available for monitoring")
                return False
            
            # Check if driver session is still valid
            try:
                # Try to get current URL - this will fail if browser is dead
                current_url = self.driver.current_url
                
                # Check if browser process still exists
                if hasattr(self.driver, 'service') and self.driver.service:
                    if hasattr(self.driver.service, 'process') and self.driver.service.process:
                        process = self.driver.service.process
                        
                        # Check process status
                        poll_result = process.poll()
                        if poll_result is not None:
                            # Process has terminated
                            if poll_result == -15:  # SIGTERM
                                print(f"⚠️ Browser process terminated by signal 15 (SIGTERM)")
                            elif poll_result == -9:   # SIGKILL
                                print(f"⚠️ Browser process killed by signal 9 (SIGKILL)")
                            else:
                                print(f"⚠️ Browser process terminated with exit code: {poll_result}")
                            return False
                        else:
                            # Process is still running
                            return True
                    else:
                        print(f"⚠️ Browser service process not available")
                        return False
                else:
                    print(f"⚠️ Browser service not available")
                    return False
                    
            except Exception as e:
                # If we can't get current URL, browser is likely dead
                error_msg = str(e).lower()
                if 'no such window' in error_msg or 'target window already closed' in error_msg:
                    print(f"⚠️ Browser window closed unexpectedly")
                elif 'chrome not reachable' in error_msg or 'session deleted' in error_msg:
                    print(f"⚠️ Browser session terminated")
                elif 'connection refused' in error_msg:
                    print(f"⚠️ Browser connection lost")
                else:
                    print(f"⚠️ Browser monitoring error: {e}")
                return False
                
        except Exception as e:
            print(f"⚠️ Process monitoring exception: {e}")
            return False
    
    def restart_on_crash(self):
        """Restart browser if it crashes"""
        if self.crash_count >= self.max_crashes:
            print(f"❌ Maximum crash limit reached ({self.max_crashes})")
            return False
        
        self.crash_count += 1
        print(f"🔄 Restarting browser after crash (attempt {self.crash_count}/{self.max_crashes})")
        
        # Cleanup old browser
        try:
            if self.driver:
                self.driver.quit()
        except:
            pass
        
        # Wait before restart
        time.sleep(5)
        
        # Create new browser
        return self.create_robust_browser()
    
    def run_robust_session(self, duration_minutes=5):
        """Run a robust browsing session"""
        print(f"🚀 Starting robust Netherlands-only Tor browsing session")
        print(f"⏱️ Duration: {duration_minutes} minutes")
        print(f"=" * 60)
        
        # Setup signal handlers
        self.setup_signal_handlers()
        
        # Start Tor
        if not self.start_tor_service():
            print(f"❌ Failed to start Tor service")
            return False
        
        # Create browser
        if not self.create_robust_browser():
            print(f"❌ Failed to create browser")
            return False
        
        # Test connection
        if not self.test_browser_connection():
            print(f"❌ Browser connection test failed")
            return False
        
        # Main browsing loop
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        print(f"🌐 Starting browsing loop...")
        
        while time.time() < end_time:
            try:
                # Check if browser is still alive
                if not self.monitor_browser_process():
                    print(f"⚠️ Browser process died, attempting restart...")
                    if not self.restart_on_crash():
                        print(f"❌ Could not restart browser, ending session")
                        break
                    
                    # Test connection after restart
                    if not self.test_browser_connection():
                        print(f"❌ Connection test failed after restart")
                        break
                
                # Browse different pages
                test_urls = [
                    "https://httpbin.org/ip",
                    "https://httpbin.org/user-agent",
                    "https://httpbin.org/headers",
                ]
                
                url = random.choice(test_urls)
                if not self.browse_website(url):
                    print(f"⚠️ Browsing failed, but continuing...")
                
                # Wait between requests
                wait_time = random.uniform(5, 15)
                print(f"⏱️ Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
                
            except KeyboardInterrupt:
                print(f"\n⚠️ Session interrupted by user")
                break
            except Exception as e:
                print(f"⚠️ Session error: {e}")
                time.sleep(5)
                continue
        
        elapsed = time.time() - start_time
        print(f"\n✅ Session completed after {elapsed/60:.1f} minutes")
        print(f"🔄 Crash restarts: {self.crash_count}")
        
        return True
    
    def stop_tor_service(self):
        """Stop Tor service"""
        try:
            if self.tor_process:
                print(f"🛑 Stopping Tor service...")
                
                # Try graceful shutdown first
                try:
                    os.killpg(os.getpgid(self.tor_process.pid), signal.SIGTERM)
                    self.tor_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if graceful shutdown fails
                    os.killpg(os.getpgid(self.tor_process.pid), signal.SIGKILL)
                
                self.tor_process = None
                print(f"✅ Tor service stopped")
        except Exception as e:
            print(f"⚠️ Error stopping Tor: {e}")
    
    def cleanup(self):
        """Clean up all resources"""
        print(f"🧹 Cleaning up...")
        
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
        except Exception as e:
            print(f"⚠️ Error closing browser: {e}")
        
        self.stop_tor_service()
        
        # Clean up temp files
        try:
            import glob
            temp_files = glob.glob(f"/tmp/torrc_{os.getpid()}")
            temp_files.extend(glob.glob(f"/tmp/tor_data_{os.getpid()}/*"))
            
            for temp_file in temp_files:
                try:
                    if os.path.isfile(temp_file):
                        os.remove(temp_file)
                    elif os.path.isdir(temp_file):
                        import shutil
                        shutil.rmtree(temp_file)
                except:
                    pass
        except:
            pass
        
        print(f"✅ Cleanup completed")

def main():
    """Main function"""
    print(f"🇳🇱 ROBUST NETHERLANDS-ONLY TOR BROWSER")
    print(f"=" * 45)
    
    browser = RobustNLTorBrowser()
    
    try:
        # Run session
        success = browser.run_robust_session(duration_minutes=10)
        
        if success:
            print(f"\n🎉 Session completed successfully!")
        else:
            print(f"\n❌ Session failed!")
            
    except KeyboardInterrupt:
        print(f"\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        browser.cleanup()

if __name__ == "__main__":
    main()
