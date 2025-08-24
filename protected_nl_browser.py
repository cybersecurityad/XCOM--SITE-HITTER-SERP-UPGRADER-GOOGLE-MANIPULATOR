#!/usr/bin/env python3
"""
Netherlands-only Visual Browser with Anti-Termination
Specifically designed to handle signal 15 (SIGTERM) termination
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
import requests
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class AntiTerminationNLBrowser:
    """Netherlands-only browser with anti-termination protection"""
    
    def __init__(self):
        self.tor_process = None
        self.driver = None
        self.socks_port = 9050
        self.session_active = False
        self.restart_count = 0
        self.last_ip = None
        
        # Setup signal handlers to prevent termination
        self.setup_signal_protection()
    
    def setup_signal_protection(self):
        """Setup comprehensive signal protection"""
        def signal_handler(signum, frame):
            logger.info(f"🛡️ Signal {signum} intercepted, protecting browser...")
            
            if signum == signal.SIGTERM:  # Signal 15
                logger.info("🛡️ SIGTERM (15) blocked - browser protection active")
                return  # Block the signal
            elif signum == signal.SIGINT:  # Ctrl+C
                logger.info("🛑 SIGINT received - graceful shutdown")
                self.graceful_shutdown()
                sys.exit(0)
            else:
                logger.info(f"🛡️ Signal {signum} handled")
        
        # Block SIGTERM (signal 15) to prevent termination
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        
        # Ignore other potentially harmful signals
        try:
            signal.signal(signal.SIGPIPE, signal.SIG_IGN)
            signal.signal(signal.SIGHUP, signal.SIG_IGN)
        except:
            pass  # Some signals may not be available on all systems
        
        logger.info("🛡️ Signal protection activated")
    
    def start_tor_with_nl_only(self):
        """Start Tor with Netherlands-only exit nodes"""
        try:
            logger.info("🧅 Starting Netherlands-only Tor...")
            
            # Kill any existing Tor
            self.stop_tor()
            
            # Create torrc for Netherlands only
            torrc_content = f"""
SocksPort {self.socks_port}
ControlPort {self.socks_port + 1}
ExitNodes {{nl}}
StrictNodes 1
DataDirectory /tmp/tor_nl_{os.getpid()}
Log notice stdout
"""
            
            torrc_path = f"/tmp/torrc_nl_{os.getpid()}"
            with open(torrc_path, 'w') as f:
                f.write(torrc_content)
            
            # Start Tor process with its own process group
            self.tor_process = subprocess.Popen([
                '/opt/homebrew/bin/tor', '-f', torrc_path
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
               preexec_fn=os.setsid, text=True)
            
            # Wait for Tor to be ready
            for i in range(30):
                if self.is_tor_ready():
                    logger.info(f"✅ Tor ready after {i+1} seconds")
                    return True
                time.sleep(1)
            
            logger.error("❌ Tor failed to start")
            return False
            
        except Exception as e:
            logger.error(f"❌ Tor start error: {e}")
            return False
    
    def is_tor_ready(self):
        """Check if Tor is ready"""
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                return sock.connect_ex(('127.0.0.1', self.socks_port)) == 0
        except:
            return False
    
    def get_nl_ip(self):
        """Get current Netherlands IP"""
        try:
            proxies = {
                'http': f'socks5://127.0.0.1:{self.socks_port}',
                'https': f'socks5://127.0.0.1:{self.socks_port}'
            }
            
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxies,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                ip = data.get('origin', '').split(',')[0].strip()
                
                # Verify it's Netherlands
                geo_response = requests.get(
                    f'http://ip-api.com/json/{ip}',
                    timeout=10
                )
                
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    country_code = geo_data.get('countryCode', '').upper()
                    
                    if country_code == 'NL':
                        city = geo_data.get('city', 'Unknown')
                        logger.info(f"🇳🇱 Netherlands IP: {ip} ({city})")
                        self.last_ip = ip
                        return ip
                    else:
                        country = geo_data.get('country', 'Unknown')
                        logger.warning(f"⚠️ Non-NL IP: {ip} ({country})")
                        return None
                        
        except Exception as e:
            logger.warning(f"⚠️ IP check failed: {e}")
            return None
    
    def create_protected_browser(self):
        """Create browser with maximum protection against termination"""
        try:
            logger.info("🎭 Creating protected browser...")
            
            # Ultra-robust Chrome options
            options = uc.ChromeOptions()
            
            # Core stability and anti-termination
            stability_args = [
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-software-rasterizer',
                '--single-process',  # Keep everything in one process
                '--no-zygote',       # Disable zygote process
                '--disable-hang-monitor',
                '--disable-prompt-on-repost',
                '--disable-background-timer-throttling',
                '--disable-renderer-backgrounding',
                '--disable-backgrounding-occluded-windows',
                '--disable-features=TranslateUI,VizDisplayCompositor',
                '--disable-crash-reporter',
                '--no-crash-upload',
                '--disable-breakpad',
                '--disable-logging',
                '--silent',
                '--log-level=3',
                '--disable-default-apps',
                '--disable-sync',
                '--disable-background-networking',
                '--memory-pressure-off',
                '--disable-background-mode',
                '--disable-plugins-discovery',
                '--disable-preconnect',
                '--disable-domain-reliability',
                '--disable-component-update',
                '--disable-ipc-flooding-protection',
            ]
            
            for arg in stability_args:
                options.add_argument(arg)
            
            # Tor proxy
            options.add_argument(f'--proxy-server=socks5://127.0.0.1:{self.socks_port}')
            options.add_argument('--proxy-bypass-list=<-loopback>')
            
            # Random user agent
            ua = UserAgent()
            options.add_argument(f'--user-agent={ua.random}')
            
            # Additional protection
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            # Create driver with multiple fallback strategies
            strategies = [
                lambda: uc.Chrome(options=options, version_main=None),
                lambda: uc.Chrome(options=options),
                lambda: self.create_standard_chrome(options),
                lambda: self.create_minimal_chrome()
            ]
            
            for i, strategy in enumerate(strategies):
                try:
                    logger.info(f"🚀 Browser creation strategy {i+1}...")
                    
                    self.driver = strategy()
                    
                    # Configure timeouts
                    self.driver.set_page_load_timeout(30)
                    self.driver.implicitly_wait(10)
                    
                    # Test basic functionality
                    self.driver.get('data:text/html,<h1>Protected Browser Test</h1>')
                    
                    logger.info(f"✅ Browser created with strategy {i+1}")
                    return True
                    
                except Exception as e:
                    logger.warning(f"⚠️ Strategy {i+1} failed: {e}")
                    if hasattr(self, 'driver') and self.driver:
                        try:
                            self.driver.quit()
                        except:
                            pass
                        self.driver = None
                    
                    if i < len(strategies) - 1:
                        time.sleep(2)
            
            logger.error("❌ All browser creation strategies failed")
            return False
            
        except Exception as e:
            logger.error(f"❌ Browser creation error: {e}")
            return False
    
    def create_standard_chrome(self, uc_options):
        """Fallback to standard Chrome"""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        
        # Convert options
        options = Options()
        for arg in uc_options.arguments:
            options.add_argument(arg)
        
        return webdriver.Chrome(options=options)
    
    def create_minimal_chrome(self):
        """Minimal Chrome configuration as last resort"""
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'--proxy-server=socks5://127.0.0.1:{self.socks_port}')
        
        return uc.Chrome(options=options)
    
    def test_browser_with_nl_ip(self):
        """Test browser with Netherlands IP"""
        try:
            if not self.driver:
                logger.error("❌ No browser available")
                return False
            
            logger.info("🔍 Testing browser with Netherlands IP...")
            
            # Navigate to IP check
            self.driver.get('https://httpbin.org/ip')
            
            # Wait for content
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            
            # Get page content
            content = self.driver.find_element(By.TAG_NAME, 'body').text
            logger.info(f"📄 Browser content: {content}")
            
            # Extract IP from JSON
            try:
                import json
                data = json.loads(content)
                browser_ip = data.get('origin', '').split(',')[0].strip()
                
                if browser_ip:
                    logger.info(f"🌐 Browser IP: {browser_ip}")
                    
                    # Check if it matches our Tor IP
                    if browser_ip == self.last_ip:
                        logger.info("✅ Browser using correct Netherlands Tor IP!")
                        return True
                    else:
                        logger.warning(f"⚠️ IP mismatch - Tor: {self.last_ip}, Browser: {browser_ip}")
                        return False
                else:
                    logger.error("❌ Could not extract IP from browser")
                    return False
                    
            except Exception as e:
                logger.error(f"❌ Could not parse browser response: {e}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Browser test failed: {e}")
            return False
    
    def run_protected_session(self, duration_minutes=5):
        """Run protected browsing session"""
        logger.info("🇳🇱 STARTING PROTECTED NETHERLANDS BROWSER SESSION")
        logger.info("=" * 60)
        
        self.session_active = True
        
        try:
            # Start Tor
            if not self.start_tor_with_nl_only():
                return False
            
            # Get Netherlands IP
            if not self.get_nl_ip():
                logger.error("❌ Could not get Netherlands IP")
                return False
            
            # Create protected browser
            if not self.create_protected_browser():
                return False
            
            # Test browser
            if not self.test_browser_with_nl_ip():
                logger.warning("⚠️ Browser test failed, but continuing...")
            
            # Main session loop
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            logger.info(f"🚀 Session started - running for {duration_minutes} minutes")
            
            cycle = 1
            while self.session_active and time.time() < end_time:
                try:
                    logger.info(f"🔄 Cycle {cycle}")
                    
                    # Check if browser is still alive
                    if not self.is_browser_alive():
                        logger.warning("⚠️ Browser died, attempting restart...")
                        if not self.restart_browser():
                            logger.error("❌ Could not restart browser")
                            break
                    
                    # Simple browsing activity
                    self.perform_browsing_activity()
                    
                    cycle += 1
                    time.sleep(30)  # Wait between cycles
                    
                except KeyboardInterrupt:
                    logger.info("⚠️ Session interrupted by user")
                    break
                except Exception as e:
                    logger.error(f"❌ Session error: {e}")
                    time.sleep(10)
            
            elapsed = time.time() - start_time
            logger.info(f"✅ Session completed - {cycle-1} cycles in {elapsed/60:.1f} minutes")
            return True
            
        except Exception as e:
            logger.error(f"❌ Session failed: {e}")
            return False
        finally:
            self.session_active = False
    
    def is_browser_alive(self):
        """Check if browser is still responsive"""
        try:
            if not self.driver:
                return False
            
            # Try to get current URL - will fail if browser is dead
            current_url = self.driver.current_url
            return True
            
        except Exception as e:
            error_msg = str(e).lower()
            if 'target window already closed' in error_msg:
                logger.warning("⚠️ Browser window closed")
            elif 'chrome not reachable' in error_msg:
                logger.warning("⚠️ Chrome not reachable")
            elif 'session deleted' in error_msg:
                logger.warning("⚠️ Browser session deleted")
            else:
                logger.warning(f"⚠️ Browser check failed: {e}")
            return False
    
    def restart_browser(self):
        """Restart browser after crash"""
        self.restart_count += 1
        logger.info(f"🔄 Restarting browser (attempt {self.restart_count})")
        
        if self.restart_count > 3:
            logger.error("❌ Too many restarts")
            return False
        
        # Clean up old browser
        try:
            if self.driver:
                self.driver.quit()
        except:
            pass
        self.driver = None
        
        time.sleep(3)
        
        # Create new browser
        return self.create_protected_browser()
    
    def perform_browsing_activity(self):
        """Perform simple browsing activity"""
        try:
            if not self.driver:
                logger.warning("⚠️ No driver available for browsing")
                return
                
            urls = [
                'https://httpbin.org/ip',
                'https://httpbin.org/user-agent',
                'https://httpbin.org/headers'
            ]
            
            import random
            url = random.choice(urls)
            
            logger.info(f"🌐 Visiting: {url}")
            self.driver.get(url)
            
            # Wait and scroll
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, 200);")
            time.sleep(1)
            
            logger.info("✅ Browsing activity completed")
            
        except Exception as e:
            logger.warning(f"⚠️ Browsing activity failed: {e}")
    
    def stop_tor(self):
        """Stop Tor service"""
        try:
            if self.tor_process:
                logger.info("🛑 Stopping Tor...")
                os.killpg(os.getpgid(self.tor_process.pid), signal.SIGTERM)
                self.tor_process.wait(timeout=5)
                self.tor_process = None
        except Exception as e:
            logger.warning(f"⚠️ Tor stop error: {e}")
    
    def graceful_shutdown(self):
        """Graceful shutdown of all components"""
        logger.info("🧹 Graceful shutdown...")
        
        self.session_active = False
        
        try:
            if self.driver:
                self.driver.quit()
        except:
            pass
        
        self.stop_tor()
        
        # Cleanup temp files
        try:
            import glob
            for file in glob.glob(f"/tmp/torrc_nl_{os.getpid()}"):
                os.remove(file)
            for dir in glob.glob(f"/tmp/tor_nl_{os.getpid()}"):
                import shutil
                shutil.rmtree(dir, ignore_errors=True)
        except:
            pass
        
        logger.info("✅ Shutdown completed")

def main():
    """Main function"""
    browser = AntiTerminationNLBrowser()
    
    try:
        success = browser.run_protected_session(duration_minutes=3)
        logger.info(f"🏁 Session result: {'SUCCESS' if success else 'FAILED'}")
        
    except KeyboardInterrupt:
        logger.info("⚠️ Interrupted by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
    finally:
        browser.graceful_shutdown()

if __name__ == "__main__":
    main()
