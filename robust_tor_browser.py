#!/usr/bin/env python3
"""
🎭 ROBUST TOR-BROWSER INTEGRATION
================================
Advanced modular approach with proper timing, validation, and fallback mechanisms.
This addresses the Chrome exit code 15 issue by implementing:
1. Tor proxy validation before browser creation
2. Gradual browser startup with retries
3. Fallback to direct connection if Tor fails
4. Comprehensive error handling and debugging
"""

import time
import os
import sys
import signal
import subprocess
import tempfile
import shutil
import socket
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class RobustTorManager:
    """Enhanced Tor manager with validation and error recovery"""
    
    def __init__(self):
        self.tor_process = None
        self.temp_dir = None
        self.tor_port = 9050
        self.control_port = 9051
        self.is_running = False
        
    def validate_tor_proxy(self, timeout=10):
        """Validate that Tor SOCKS proxy is actually working"""
        try:
            print(f"🔍 Validating Tor proxy on port {self.tor_port}...")
            
            # Test socket connection to Tor SOCKS proxy
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex(('127.0.0.1', self.tor_port))
            sock.close()
            
            if result == 0:
                print(f"✅ Tor proxy responding on port {self.tor_port}")
                return True
            else:
                print(f"❌ Tor proxy not responding on port {self.tor_port}")
                return False
                
        except Exception as e:
            print(f"❌ Tor proxy validation failed: {e}")
            return False
    
    def test_tor_connection(self):
        """Test actual Tor connection by making a request"""
        try:
            print("🌐 Testing Tor connection with curl...")
            
            # Use curl with Tor proxy to test connection
            cmd = [
                'curl', 
                '--proxy', f'socks5://127.0.0.1:{self.tor_port}',
                '--connect-timeout', '10',
                '--max-time', '15',
                '--silent',
                '--head',
                'https://check.torproject.org/'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            
            if result.returncode == 0:
                print("✅ Tor connection test successful!")
                return True
            else:
                print(f"❌ Tor connection test failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Tor connection test timed out")
            return False
        except Exception as e:
            print(f"❌ Tor connection test error: {e}")
            return False
    
    def start_tor_with_validation(self):
        """Start Tor and validate it's working properly"""
        try:
            print("🧅 Starting Tor with comprehensive validation...")
            
            # Create temp directory
            self.temp_dir = tempfile.mkdtemp(prefix='robust_tor_')
            print(f"📁 Tor directory: {self.temp_dir}")
            
            # Create enhanced torrc
            torrc_content = f"""
# Enhanced Tor configuration for browser integration
SocksPort {self.tor_port}
ControlPort {self.control_port}
DataDirectory {self.temp_dir}/tor_data

# Netherlands-only exit nodes
ExitNodes {{nl}}
StrictNodes 1

# Performance and stability
CircuitBuildTimeout 30
LearnCircuitBuildTimeout 0
CircuitStreamTimeout 20
NewCircuitPeriod 60

# Reduce connection issues
ConnLimit 1000
MaxClientCircuitsPending 48
NumEntryGuards 8

# Logging for debugging
Log notice stdout
Log warn stdout
"""
            
            torrc_path = os.path.join(self.temp_dir, 'torrc')
            with open(torrc_path, 'w') as f:
                f.write(torrc_content)
            
            print(f"📝 Enhanced torrc created: {torrc_path}")
            
            # Start Tor process
            cmd = ['tor', '-f', torrc_path]
            print(f"🚀 Starting Tor: {' '.join(cmd)}")
            
            self.tor_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Wait for Tor to start with output monitoring
            print("⏳ Waiting for Tor initialization...")
            bootstrap_complete = False
            circuits_ready = False
            start_time = time.time()
            timeout = 60  # 60 second timeout
            
            while time.time() - start_time < timeout:
                if self.tor_process.poll() is not None:
                    print("❌ Tor process died unexpectedly")
                    return False
                
                # Read Tor output
                line = self.tor_process.stdout.readline()
                if line:
                    line = line.strip()
                    print(f"🧅 Tor: {line}")
                    
                    if "Bootstrapped 100%" in line:
                        bootstrap_complete = True
                        print("✅ Tor bootstrap complete!")
                    
                    if "Circuit established" in line or "Built circuit" in line:
                        circuits_ready = True
                        print("✅ Tor circuits established!")
                    
                    if bootstrap_complete and circuits_ready:
                        break
                
                time.sleep(0.5)
            
            # Validate Tor is working
            if not bootstrap_complete:
                print("❌ Tor bootstrap did not complete in time")
                return False
            
            # Give extra time for stability
            print("⏳ Allowing Tor to stabilize...")
            time.sleep(5)
            
            # Validate proxy
            if not self.validate_tor_proxy():
                print("❌ Tor proxy validation failed")
                return False
            
            # Test connection
            if not self.test_tor_connection():
                print("❌ Tor connection test failed")
                return False
            
            self.is_running = True
            print("✅ Tor started and validated successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Tor startup failed: {e}")
            return False
    
    def stop_tor(self):
        """Stop Tor process and clean up"""
        try:
            print("🛑 Stopping Tor...")
            
            if self.tor_process:
                self.tor_process.terminate()
                try:
                    self.tor_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.tor_process.kill()
                    self.tor_process.wait()
                print("✅ Tor process stopped")
            
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                print(f"🗑️ Cleaned up: {self.temp_dir}")
            
            self.is_running = False
            
        except Exception as e:
            print(f"⚠️ Tor cleanup error: {e}")

class RobustBrowserManager:
    """Enhanced browser manager with Tor integration and fallback"""
    
    def __init__(self):
        self.browser = None
        self.proxy_url = None
        self.ga_tracking_id = "G-0B4ZR31YFS"
    
    def create_browser_with_tor_validation(self, proxy_url: str, retries=3):
        """Create browser with Tor proxy and retry mechanism"""
        for attempt in range(retries):
            try:
                print(f"🌐 Creating browser (attempt {attempt + 1}/{retries})...")
                
                # Kill existing Chrome processes
                subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True, check=False)
                subprocess.run(['pkill', '-f', 'chromedriver'], capture_output=True, check=False)
                time.sleep(2)
                
                # Create Chrome options
                options = Options()
                
                # Tor proxy configuration
                print(f"🔗 Configuring proxy: {proxy_url}")
                options.add_argument(f'--proxy-server={proxy_url}')
                
                # Enhanced stability options
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--disable-extensions')
                options.add_argument('--disable-plugins')
                options.add_argument('--disable-images')  # Reduce load
                options.add_argument('--disable-javascript')  # Initial load without JS
                
                # Proxy-specific options
                options.add_argument('--proxy-bypass-list=<-loopback>')
                options.add_argument('--disable-web-security')
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--ignore-ssl-errors')
                
                # User agent
                options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
                
                # Create service with timeout
                service = Service()
                
                print("🚀 Starting Chrome with Tor proxy...")
                
                # Create browser with timeout
                browser = webdriver.Chrome(service=service, options=options)
                browser.set_page_load_timeout(30)
                browser.implicitly_wait(10)
                
                # Test basic functionality
                print("🧪 Testing browser functionality...")
                browser.get("data:text/html,<html><body><h1>Browser Test</h1></body></html>")
                time.sleep(2)
                
                if "Browser Test" in browser.page_source:
                    print("✅ Browser created and functional!")
                    self.browser = browser
                    self.proxy_url = proxy_url
                    return browser
                else:
                    print("❌ Browser functionality test failed")
                    browser.quit()
                    continue
                
            except Exception as e:
                print(f"❌ Browser creation attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    print(f"🔄 Retrying in 3 seconds...")
                    time.sleep(3)
                continue
        
        print("❌ All browser creation attempts failed")
        return None
    
    def create_browser_direct(self):
        """Create browser with direct connection (no proxy)"""
        try:
            print("🌐 Creating browser with direct connection...")
            
            # Kill existing processes
            subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True, check=False)
            time.sleep(1)
            
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            
            service = Service()
            browser = webdriver.Chrome(service=service, options=options)
            browser.set_page_load_timeout(15)
            
            self.browser = browser
            self.proxy_url = None
            print("✅ Direct browser created successfully!")
            return browser
            
        except Exception as e:
            print(f"❌ Direct browser creation failed: {e}")
            return None
    
    def test_website_access(self, url="https://verenigdamsterdam.nl"):
        """Test website access and GA injection"""
        try:
            if not self.browser:
                print("❌ No browser available")
                return False
            
            print(f"🌐 Testing website: {url}")
            self.browser.get(url)
            time.sleep(3)
            
            title = self.browser.title
            print(f"✅ Website loaded: {title[:50]}...")
            
            # Inject GA tracking
            ga_script = f"""
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{self.ga_tracking_id}');
            console.log('GA tracking injected');
            """
            
            self.browser.execute_script(ga_script)
            print("📊 GA tracking injected")
            
            return True
            
        except Exception as e:
            print(f"❌ Website test failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up browser resources"""
        try:
            if self.browser:
                self.browser.quit()
                print("✅ Browser closed")
        except:
            pass

class RobustTorBrowser:
    """Main class combining Tor and Browser with robust error handling"""
    
    def __init__(self):
        self.tor_manager = RobustTorManager()
        self.browser_manager = RobustBrowserManager()
        self.running = True
        
        # Signal handling
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🔄 Signal {signum} received. Gracefully shutting down...")
        self.running = False
        self.cleanup()
        sys.exit(0)
    
    def run_with_tor(self):
        """Run with Tor integration"""
        try:
            print("1️⃣ STARTING TOR WITH VALIDATION...")
            if not self.tor_manager.start_tor_with_validation():
                print("❌ Tor startup failed")
                return False
            
            print("\n2️⃣ CREATING BROWSER WITH TOR...")
            proxy_url = f"socks5://127.0.0.1:{self.tor_manager.tor_port}"
            browser = self.browser_manager.create_browser_with_tor_validation(proxy_url)
            
            if not browser:
                print("❌ Browser creation with Tor failed")
                return False
            
            print("\n3️⃣ TESTING WEBSITE ACCESS...")
            success = self.browser_manager.test_website_access()
            
            if success:
                print("\n🎉 TOR + BROWSER SUCCESS!")
                print("✅ Tor circuits established")
                print("✅ Browser created with proxy")
                print("✅ Website access functional")
                print("✅ GA tracking active")
                
                # Keep running for observation
                print("\n👀 Keeping browser open for testing...")
                input("Press Enter to close...")
                return True
            else:
                print("❌ Website access failed")
                return False
                
        except Exception as e:
            print(f"❌ Tor browser run failed: {e}")
            return False
    
    def run_direct(self):
        """Run with direct connection (fallback)"""
        try:
            print("🌐 RUNNING WITH DIRECT CONNECTION...")
            browser = self.browser_manager.create_browser_direct()
            
            if not browser:
                print("❌ Direct browser creation failed")
                return False
            
            success = self.browser_manager.test_website_access()
            
            if success:
                print("\n✅ DIRECT CONNECTION SUCCESS!")
                input("Press Enter to close...")
                return True
            else:
                print("❌ Direct connection test failed")
                return False
                
        except Exception as e:
            print(f"❌ Direct browser run failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up all resources"""
        print("\n🧹 CLEANING UP ALL MODULES...")
        self.browser_manager.cleanup()
        self.tor_manager.stop_tor()
        print("✅ All modules cleaned up!")

def main():
    """Main execution with robust error handling"""
    print("=" * 60)
    print("🎭 ROBUST TOR-BROWSER INTEGRATION")
    print("=" * 60)
    print("🎯 Advanced modular approach with validation")
    print("🛡️ Chrome exit code 15 prevention")
    print("🔄 Fallback mechanisms included")
    print("=" * 60)
    
    print("\nSelect mode:")
    print("1. Tor + Browser (with validation)")
    print("2. Direct connection (fallback)")
    print("3. Test both (comparison)")
    
    try:
        choice = input("Enter choice (1/2/3): ").strip()
        
        if choice == "1":
            print("\n🧅 STARTING TOR + BROWSER MODE...")
            browser = RobustTorBrowser()
            success = browser.run_with_tor()
            if not success:
                print("\n🔄 Tor mode failed, trying direct connection...")
                browser.run_direct()
        
        elif choice == "2":
            print("\n🌐 STARTING DIRECT CONNECTION MODE...")
            browser = RobustTorBrowser()
            browser.run_direct()
        
        elif choice == "3":
            print("\n🧪 TESTING BOTH MODES...")
            
            # Test direct first
            print("\n--- TESTING DIRECT CONNECTION ---")
            browser1 = RobustTorBrowser()
            direct_success = browser1.run_direct()
            browser1.cleanup()
            
            print("\n--- TESTING TOR CONNECTION ---")
            browser2 = RobustTorBrowser()
            tor_success = browser2.run_with_tor()
            browser2.cleanup()
            
            print("\n📊 COMPARISON RESULTS:")
            print(f"✅ Direct connection: {'SUCCESS' if direct_success else 'FAILED'}")
            print(f"🧅 Tor connection: {'SUCCESS' if tor_success else 'FAILED'}")
        
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n⏹️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
