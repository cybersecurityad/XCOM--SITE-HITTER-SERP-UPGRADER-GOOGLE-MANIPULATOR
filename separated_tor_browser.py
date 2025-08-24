#!/usr/bin/env python3
"""
🎭 SEPARATED TOR-BROWSER ARCHITECTURE
====================================
ALWAYS separate Tor initialization from browser startup.
This ensures Tor is fully operational before any browser activity.

SEPARATION PRINCIPLE:
1. 🧅 START TOR FIRST (complete initialization & validation)
2. ⏸️  WAIT & VERIFY (proxy ready, IP changed)  
3. 🌐 THEN START BROWSER (with confirmed Tor proxy)
4. 🚀 EXECUTE BROWSING (with stable Tor connection)

This prevents Chrome exit code 15 and ensures reliable Tor integration.
"""

# AUTO-INITIALIZE LOGGING
try:
    from auto_logger_init_v2 import auto_initialize_all_systems
    auto_initialize_all_systems(verbose=True)
except ImportError:
    print("⚠️ Auto-logging not available, continuing...")

import time
import os
import sys
import signal
import subprocess
import tempfile
import shutil
import socket
import json
from datetime import datetime
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import requests

class SeparatedTorManager:
    """Dedicated Tor manager - runs FIRST and INDEPENDENTLY"""
    
    def __init__(self):
        self.tor_process = None
        self.temp_dir = None
        self.tor_port = 9050
        self.control_port = 9051
        self.is_fully_ready = False
        self.original_ip = None
        self.tor_ip = None
        
        print("🧅 Separated Tor Manager initialized")
        
    def get_current_ip(self) -> Optional[str]:
        """Get current public IP address"""
        try:
            response = requests.get('https://httpbin.org/ip', timeout=10)
            return response.json()['origin']
        except:
            try:
                response = requests.get('https://api.ipify.org', timeout=10)
                return response.text.strip()
            except:
                return None
    
    def validate_tor_proxy(self, timeout=15) -> bool:
        """Validate Tor SOCKS proxy is accepting connections"""
        try:
            print(f"🔍 Validating Tor proxy on port {self.tor_port}...")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex(('127.0.0.1', self.tor_port))
            sock.close()
            
            if result == 0:
                print(f"✅ Tor proxy responding on port {self.tor_port}")
                return True
            else:
                print(f"❌ Tor proxy not responding (error: {result})")
                return False
                
        except Exception as e:
            print(f"❌ Tor proxy validation failed: {e}")
            return False
    
    def test_tor_connectivity(self) -> bool:
        """Test actual Tor network connectivity"""
        try:
            print("🌐 Testing Tor network connectivity...")
            
            # Configure requests to use Tor proxy
            proxies = {
                'http': f'socks5://127.0.0.1:{self.tor_port}',
                'https': f'socks5://127.0.0.1:{self.tor_port}'
            }
            
            # Test Tor connectivity
            response = requests.get(
                'https://check.torproject.org/',
                proxies=proxies,
                timeout=20,
                headers={'User-Agent': 'Mozilla/5.0 (compatible; Tor test)'}
            )
            
            if response.status_code == 200:
                print("✅ Tor network connectivity confirmed!")
                return True
            else:
                print(f"❌ Tor connectivity failed (status: {response.status_code})")
                return False
                
        except Exception as e:
            print(f"❌ Tor connectivity test error: {e}")
            return False
    
    def get_tor_ip(self) -> Optional[str]:
        """Get IP address through Tor proxy"""
        try:
            print("🔍 Getting IP through Tor...")
            
            proxies = {
                'http': f'socks5://127.0.0.1:{self.tor_port}',
                'https': f'socks5://127.0.0.1:{self.tor_port}'
            }
            
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxies,
                timeout=15
            )
            
            tor_ip = response.json()['origin']
            print(f"🧅 Tor IP: {tor_ip}")
            return tor_ip
            
        except Exception as e:
            print(f"❌ Failed to get Tor IP: {e}")
            return None
    
    def start_tor_process(self) -> bool:
        """Start Tor process with proper configuration"""
        try:
            print("🚀 Starting Tor process...")
            
            # Create temp directory for Tor
            self.temp_dir = tempfile.mkdtemp(prefix='separated_tor_')
            print(f"📁 Tor directory: {self.temp_dir}")
            
            # Create torrc configuration
            torrc_content = f"""
SocksPort {self.tor_port}
ControlPort {self.control_port}
DataDirectory {self.temp_dir}/data
Log notice stdout
ExitNodes {{us,ca,gb,de,fr,nl,se,ch}}
StrictNodes 1
NewCircuitPeriod 60
MaxCircuitDirtiness 600
CircuitBuildTimeout 30
LearnCircuitBuildTimeout 0
"""
            
            torrc_path = os.path.join(self.temp_dir, 'torrc')
            with open(torrc_path, 'w') as f:
                f.write(torrc_content)
            
            # Start Tor process
            tor_cmd = ['tor', '-f', torrc_path]
            print(f"🔧 Tor command: {' '.join(tor_cmd)}")
            
            self.tor_process = subprocess.Popen(
                tor_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print(f"✅ Tor process started (PID: {self.tor_process.pid})")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Tor process: {e}")
            return False
    
    def wait_for_tor_ready(self, max_wait=60) -> bool:
        """Wait for Tor to be fully ready for connections"""
        print(f"⏳ Waiting for Tor to be ready (max {max_wait}s)...")
        
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            # Check if process is still running
            if self.tor_process and self.tor_process.poll() is not None:
                print("❌ Tor process terminated unexpectedly")
                return False
            
            # Test proxy availability
            if self.validate_tor_proxy(timeout=5):
                # Test network connectivity
                if self.test_tor_connectivity():
                    print(f"✅ Tor is ready! (took {time.time() - start_time:.1f}s)")
                    return True
            
            print("⏳ Tor not ready yet, waiting...")
            time.sleep(5)
        
        print(f"❌ Tor failed to become ready within {max_wait}s")
        return False
    
    def full_tor_initialization(self) -> bool:
        """Complete Tor initialization process - MUST be called FIRST"""
        print("=" * 60)
        print("🧅 PHASE 1: SEPARATED TOR INITIALIZATION")
        print("=" * 60)
        
        # Get original IP
        self.original_ip = self.get_current_ip()
        if self.original_ip:
            print(f"🌐 Original IP: {self.original_ip}")
        
        # Start Tor process
        if not self.start_tor_process():
            return False
        
        # Wait for Tor to be ready
        if not self.wait_for_tor_ready():
            self.stop_tor()
            return False
        
        # Get Tor IP and verify it's different
        self.tor_ip = self.get_tor_ip()
        if not self.tor_ip:
            print("❌ Could not get Tor IP")
            self.stop_tor()
            return False
        
        # Verify IP changed
        if self.original_ip and self.tor_ip == self.original_ip:
            print("❌ IP did not change - Tor not working properly")
            self.stop_tor()
            return False
        
        print(f"✅ IP successfully changed: {self.original_ip} → {self.tor_ip}")
        
        self.is_fully_ready = True
        print("🎉 TOR INITIALIZATION COMPLETE!")
        print("=" * 60)
        return True
    
    def stop_tor(self):
        """Stop Tor process and cleanup"""
        print("🛑 Stopping Tor process...")
        
        if self.tor_process:
            try:
                self.tor_process.terminate()
                self.tor_process.wait(timeout=10)
                print("✅ Tor process terminated")
            except:
                try:
                    self.tor_process.kill()
                    print("🔥 Tor process killed")
                except:
                    pass
        
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                print("✅ Tor temp directory cleaned")
            except:
                pass
        
        self.is_fully_ready = False

class SeparatedBrowserManager:
    """Browser manager - runs AFTER Tor is ready"""
    
    def __init__(self, tor_manager: SeparatedTorManager):
        self.tor_manager = tor_manager
        self.driver = None
        self.ga_tracking_id = 'G-0B4ZR31YFS'
        
        print("🌐 Separated Browser Manager initialized")
    
    def create_browser_with_tor(self) -> bool:
        """Create browser with confirmed Tor proxy - ONLY after Tor is ready"""
        
        if not self.tor_manager.is_fully_ready:
            print("❌ Cannot create browser - Tor is not ready!")
            return False
        
        print("=" * 60)
        print("🌐 PHASE 2: BROWSER CREATION WITH TOR")
        print("=" * 60)
        
        try:
            print("🚀 Creating browser with confirmed Tor proxy...")
            
            # Kill any existing Chrome processes
            subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True, check=False)
            time.sleep(2)
            
            # Configure Chrome options with Tor proxy
            options = uc.ChromeOptions()
            
            # Essential Chrome options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            
            # Tor proxy configuration
            proxy_url = f'socks5://127.0.0.1:{self.tor_manager.tor_port}'
            options.add_argument(f'--proxy-server={proxy_url}')
            options.add_argument('--proxy-bypass-list=<-loopback>')
            
            print(f"🔧 Using Tor proxy: {proxy_url}")
            
            # Anti-detection settings
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # User agent
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            options.add_argument(f'--user-agent={user_agent}')
            
            # Create driver
            print("🚀 Launching Chrome with Tor proxy...")
            self.driver = uc.Chrome(options=options)
            
            # Apply stealth scripts
            print("🥷 Applying stealth modifications...")
            stealth_scripts = [
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
                "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
                "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
                "window.chrome = { runtime: {} }"
            ]
            
            for script in stealth_scripts:
                try:
                    self.driver.execute_script(script)
                except:
                    pass
            
            print("✅ Browser created successfully with Tor proxy!")
            return True
            
        except Exception as e:
            print(f"❌ Browser creation failed: {e}")
            return False
    
    def verify_tor_in_browser(self) -> bool:
        """Verify browser is actually using Tor network"""
        try:
            if not self.driver:
                print("❌ No browser available for verification")
                return False
                
            print("🔍 Verifying Tor connection in browser...")
            
            self.driver.get('https://httpbin.org/ip')
            time.sleep(3)
            
            page_source = self.driver.page_source
            
            if self.tor_manager.tor_ip and self.tor_manager.tor_ip in page_source:
                print(f"✅ Browser confirmed using Tor IP: {self.tor_manager.tor_ip}")
                return True
            else:
                print("❌ Browser not using Tor IP!")
                return False
                
        except Exception as e:
            print(f"❌ Tor verification failed: {e}")
            return False
    
    def test_website_with_ga(self, url: str = "https://google.com") -> bool:
        """Test website access with Google Analytics tracking"""
        try:
            if not self.driver:
                print("❌ No browser available for testing")
                return False
                
            print(f"🌐 Testing website access: {url}")
            
            # Navigate to website
            self.driver.get(url)
            time.sleep(5)
            
            # Inject Google Analytics
            ga_script = f"""
            (function(i,s,o,g,r,a,m){{i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){{
            (i[r].q=i[r].q||[]).push(arguments)}},i[r].l=1*new Date();a=s.createElement(o),
            m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
            }})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
            
            ga('create', '{self.ga_tracking_id}', 'auto');
            ga('send', 'pageview');
            
            console.log('Google Analytics loaded and pageview sent');
            """
            
            self.driver.execute_script(ga_script)
            print("📊 Google Analytics injected and pageview sent")
            
            # Check page title
            title = self.driver.title
            print(f"📄 Page title: {title}")
            
            print(f"✅ Website access successful!")
            return True
            
        except Exception as e:
            print(f"❌ Website test failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up browser resources"""
        if self.driver:
            try:
                self.driver.quit()
                print("✅ Browser closed")
            except:
                pass

class SeparatedTorBrowser:
    """Main class implementing separated Tor-Browser architecture"""
    
    def __init__(self):
        self.tor_manager = None
        self.browser_manager = None
        
        # Signal handlers
        signal.signal(signal.SIGTERM, self._cleanup_handler)
        signal.signal(signal.SIGINT, self._cleanup_handler)
    
    def _cleanup_handler(self, signum, frame):
        """Handle cleanup on termination"""
        print(f"\n🛑 Received signal {signum}, cleaning up...")
        self.cleanup()
        sys.exit(0)
    
    def run_separated_tor_browser(self) -> bool:
        """Run the complete separated Tor-Browser process"""
        print("🎯 SEPARATED TOR-BROWSER ARCHITECTURE")
        print("=" * 60)
        print("✅ Always separate Tor init from browser startup")
        print("✅ Tor runs first, browser runs second")
        print("✅ Full validation between phases")
        print("=" * 60)
        
        try:
            # PHASE 1: Initialize Tor FIRST
            print("\\n🧅 PHASE 1: TOR INITIALIZATION...")
            self.tor_manager = SeparatedTorManager()
            
            if not self.tor_manager.full_tor_initialization():
                print("❌ Tor initialization failed!")
                return False
            
            # PHASE 2: Create browser AFTER Tor is ready
            print("\\n🌐 PHASE 2: BROWSER CREATION...")
            self.browser_manager = SeparatedBrowserManager(self.tor_manager)
            
            if not self.browser_manager.create_browser_with_tor():
                print("❌ Browser creation failed!")
                return False
            
            # PHASE 3: Verify Tor integration
            print("\\n🔍 PHASE 3: TOR VERIFICATION...")
            if not self.browser_manager.verify_tor_in_browser():
                print("❌ Tor verification failed!")
                return False
            
            # PHASE 4: Test website with GA
            print("\\n🌐 PHASE 4: WEBSITE TESTING...")
            if not self.browser_manager.test_website_with_ga():
                print("❌ Website test failed!")
                return False
            
            print("\\n🎉 ALL PHASES SUCCESSFUL!")
            print("=" * 60)
            print("✅ Tor initialization: SUCCESS")
            print("✅ Browser creation: SUCCESS") 
            print("✅ Tor verification: SUCCESS")
            print("✅ Website testing: SUCCESS")
            print("=" * 60)
            
            input("\\nPress Enter to continue browsing or Ctrl+C to exit...")
            return True
            
        except Exception as e:
            print(f"❌ Separated Tor-Browser run failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up all resources"""
        print("\\n🧹 CLEANING UP ALL RESOURCES...")
        
        if self.browser_manager:
            self.browser_manager.cleanup()
        
        if self.tor_manager:
            self.tor_manager.stop_tor()
        
        print("✅ All resources cleaned up!")

def main():
    """Main execution with separated architecture"""
    print("🎭 SEPARATED TOR-BROWSER ARCHITECTURE")
    print("=" * 60)
    print("🎯 Always runs Tor initialization FIRST")
    print("🎯 Then creates browser with confirmed Tor proxy")
    print("🎯 Prevents Chrome exit code 15 issues")
    print("=" * 60)
    
    browser = SeparatedTorBrowser()
    
    try:
        success = browser.run_separated_tor_browser()
        
        if success:
            print("\\n🎉 SEPARATED TOR-BROWSER RUN SUCCESSFUL!")
        else:
            print("\\n❌ SEPARATED TOR-BROWSER RUN FAILED!")
            
    except KeyboardInterrupt:
        print("\\n⏹️ Interrupted by user")
    except Exception as e:
        print(f"\\n❌ Error: {e}")
    finally:
        browser.cleanup()

if __name__ == "__main__":
    main()
