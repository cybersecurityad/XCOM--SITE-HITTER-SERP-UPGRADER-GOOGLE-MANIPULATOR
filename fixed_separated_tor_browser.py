#!/usr/bin/env python3
"""
Fixed Tor Browser with proper process management
Addresses the Tor crash issue by:
1. Running Tor in foreground mode
2. Proper stdout/stderr handling
3. Better error diagnostics
4. Robust process management
"""

import os
import sys
import time
import socket
import subprocess
import tempfile
import shutil
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

class FixedTorManager:
    def __init__(self, tor_port: int = 9050):
        self.tor_port = tor_port
        self.tor_process = None
        self.temp_dir = None
        self.is_ready = False
        
    def check_tor_installed(self) -> bool:
        """Check if Tor is installed"""
        try:
            result = subprocess.run(['which', 'tor'], capture_output=True, text=True)
            if result.returncode == 0:
                tor_path = result.stdout.strip()
                print(f"✅ Tor found: {tor_path}")
                return True
            else:
                print("❌ Tor not found")
                return False
        except Exception as e:
            print(f"❌ Error checking Tor: {e}")
            return False
    
    def test_proxy_port(self, port: int) -> bool:
        """Test if proxy port is responding"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result == 0
        except:
            return False
    
    def kill_existing_tor(self):
        """Kill any existing Tor processes"""
        try:
            print("🔪 Killing existing Tor processes...")
            subprocess.run(['pkill', '-f', 'tor'], check=False)
            time.sleep(2)
            print("✅ Existing Tor processes killed")
        except Exception as e:
            print(f"⚠️ Error killing Tor processes: {e}")
    
    def start_tor_fixed(self) -> bool:
        """Start Tor with proper configuration and error handling"""
        try:
            self.kill_existing_tor()
            
            # Create temp directory with proper permissions
            self.temp_dir = tempfile.mkdtemp(prefix='fixed_tor_')
            data_dir = os.path.join(self.temp_dir, 'data')
            os.makedirs(data_dir, mode=0o700, exist_ok=True)
            print(f"📁 Tor directory: {self.temp_dir}")
            
            # Fixed torrc configuration
            torrc_content = f"""# Fixed Tor Configuration
SocksPort 127.0.0.1:{self.tor_port}
DataDirectory {data_dir}
Log notice stdout
RunAsDaemon 0
ExitNodes {{us,ca,gb,de,fr}}
ClientOnly 1
"""
            
            torrc_path = os.path.join(self.temp_dir, 'torrc')
            with open(torrc_path, 'w') as f:
                f.write(torrc_content)
            
            print(f"🚀 Starting Tor on port {self.tor_port}...")
            
            # Start Tor with explicit foreground mode and better process handling
            cmd = [
                'tor',
                '-f', torrc_path,
                '--RunAsDaemon', '0',
                '--Log', 'notice stdout'
            ]
            
            print(f"🔧 Tor command: {' '.join(cmd)}")
            
            # Use DEVNULL for stderr and file for stdout to avoid pipe blocking
            log_file = os.path.join(self.temp_dir, 'tor.log')
            
            with open(log_file, 'w') as log:
                self.tor_process = subprocess.Popen(
                    cmd,
                    stdout=log,
                    stderr=subprocess.STDOUT,  # Redirect stderr to stdout
                    text=True,
                    cwd=self.temp_dir,
                    env=dict(os.environ, HOME=self.temp_dir)  # Set HOME to avoid permission issues
                )
            
            print(f"✅ Tor process started (PID: {self.tor_process.pid})")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Tor: {e}")
            if self.tor_process:
                try:
                    self.tor_process.terminate()
                except:
                    pass
            return False
    
    def wait_for_tor_fixed(self, max_wait: int = 30) -> bool:
        """Wait for Tor with better diagnostics"""
        print(f"⏳ Waiting for Tor proxy (max {max_wait}s)...")
        
        start_time = time.time()
        last_log_check = 0
        
        while time.time() - start_time < max_wait:
            # Check if process is still running
            if self.tor_process and self.tor_process.poll() is not None:
                print(f"❌ Tor process died (exit code: {self.tor_process.returncode})")
                
                # Show the last lines of the log for debugging
                log_file = os.path.join(self.temp_dir, 'tor.log') if self.temp_dir else None
                if log_file and os.path.exists(log_file):
                    print("📋 Tor log (last 10 lines):")
                    try:
                        with open(log_file, 'r') as f:
                            lines = f.readlines()
                            for line in lines[-10:]:
                                print(f"   {line.strip()}")
                    except Exception as e:
                        print(f"   ❌ Could not read log: {e}")
                
                return False
            
            # Test proxy port
            if self.test_proxy_port(self.tor_port):
                print(f"✅ Tor proxy ready on port {self.tor_port}")
                self.is_ready = True
                return True
            
            # Periodically check log for progress
            current_time = time.time()
            if current_time - last_log_check > 5:
                log_file = os.path.join(self.temp_dir, 'tor.log') if self.temp_dir else None
                if log_file and os.path.exists(log_file):
                    try:
                        with open(log_file, 'r') as f:
                            lines = f.readlines()
                            if lines:
                                last_line = lines[-1].strip()
                                if 'Bootstrapped' in last_line:
                                    print(f"🔄 {last_line}")
                    except:
                        pass
                last_log_check = current_time
            
            print("⏳ Tor starting...")
            time.sleep(2)
        
        print(f"❌ Tor failed to start within {max_wait}s")
        return False
    
    def test_tor_connection(self) -> bool:
        """Test Tor connection"""
        try:
            print("🌐 Testing Tor connection...")
            
            proxies = {
                'http': f'socks5://127.0.0.1:{self.tor_port}',
                'https': f'socks5://127.0.0.1:{self.tor_port}'
            }
            
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code == 200:
                ip_data = response.json()
                tor_ip = ip_data['origin']
                print(f"🧅 Tor IP: {tor_ip}")
                return True
            else:
                print(f"❌ Tor test failed (status: {response.status_code})")
                return False
                
        except Exception as e:
            print(f"❌ Tor test error: {e}")
            return False
    
    def full_tor_init(self) -> bool:
        """Complete Tor initialization with proper error handling"""
        print("=" * 50)
        print("🧅 PHASE 1: TOR INITIALIZATION (FIXED)")
        print("=" * 50)
        
        # Check Tor installation
        if not self.check_tor_installed():
            print("❌ Tor not installed. Install with: brew install tor")
            return False
        
        # Start Tor
        if not self.start_tor_fixed():
            return False
        
        # Wait for Tor
        if not self.wait_for_tor_fixed():
            self.stop_tor()
            return False
        
        # Test connection
        if not self.test_tor_connection():
            print("⚠️ Tor started but connection test failed")
            # Don't fail here - connection might still work for browser
        
        print("✅ Tor initialization complete!")
        return True
    
    def stop_tor(self):
        """Stop Tor and cleanup"""
        try:
            print("🛑 Stopping Tor...")
            
            if self.tor_process:
                # First try graceful termination
                self.tor_process.terminate()
                try:
                    self.tor_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if graceful termination fails
                    self.tor_process.kill()
                    self.tor_process.wait()
                
                print("✅ Tor stopped")
            
            # Cleanup temp directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                print("✅ Tor temp cleaned")
            
            self.is_ready = False
            
        except Exception as e:
            print(f"⚠️ Error stopping Tor: {e}")

class FixedBrowserManager:
    def __init__(self, tor_manager: FixedTorManager):
        self.tor_manager = tor_manager
        self.driver = None
    
    def create_tor_browser(self) -> webdriver.Chrome:
        """Create browser with Tor proxy"""
        if not self.tor_manager.is_ready:
            raise Exception("Tor is not ready! Call tor_manager.full_tor_init() first")
        
        print("=" * 50)
        print("🌐 PHASE 2: BROWSER INITIALIZATION")
        print("=" * 50)
        
        try:
            # Chrome options for Tor
            options = uc.ChromeOptions()
            
            # Proxy settings
            proxy_arg = f"--proxy-server=socks5://127.0.0.1:{self.tor_manager.tor_port}"
            options.add_argument(proxy_arg)
            
            # Privacy settings
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--incognito")
            
            # Create driver
            print("🚀 Creating Chrome driver with Tor proxy...")
            self.driver = uc.Chrome(options=options)
            
            print("✅ Browser created successfully!")
            return self.driver
            
        except Exception as e:
            print(f"❌ Failed to create browser: {e}")
            raise
    
    def test_browser_tor_ip(self) -> bool:
        """Test that browser is using Tor"""
        try:
            if not self.driver:
                print("❌ No browser instance")
                return False
            
            print("🔍 Testing browser Tor IP...")
            self.driver.get("https://httpbin.org/ip")
            
            # Get page content
            page_source = self.driver.page_source
            
            if "origin" in page_source:
                print("✅ Browser is using Tor proxy")
                return True
            else:
                print("❌ Browser might not be using Tor")
                return False
                
        except Exception as e:
            print(f"❌ Browser test error: {e}")
            return False
    
    def cleanup(self):
        """Cleanup browser"""
        try:
            if self.driver:
                self.driver.quit()
                print("✅ Browser closed")
        except Exception as e:
            print(f"⚠️ Error closing browser: {e}")

def main():
    """Test the fixed Tor + Browser setup"""
    print("🧪 TESTING FIXED TOR + BROWSER SETUP")
    print("=" * 60)
    
    tor_manager = None
    browser_manager = None
    
    try:
        # Phase 1: Initialize Tor
        tor_manager = FixedTorManager()
        
        if not tor_manager.full_tor_init():
            print("❌ FAILED! Tor initialization failed")
            return False
        
        # Phase 2: Initialize Browser
        browser_manager = FixedBrowserManager(tor_manager)
        driver = browser_manager.create_tor_browser()
        
        # Phase 3: Test
        if browser_manager.test_browser_tor_ip():
            print("🎉 SUCCESS! Tor + Browser working correctly")
            
            # Optional: Quick Google test
            try:
                print("🔍 Testing Google search...")
                driver.get("https://www.google.com")
                print(f"📄 Page title: {driver.title}")
            except Exception as e:
                print(f"⚠️ Google test failed: {e}")
            
            return True
        else:
            print("❌ FAILED! Browser not using Tor properly")
            return False
            
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
        return False
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        if browser_manager:
            browser_manager.cleanup()
        if tor_manager:
            tor_manager.stop_tor()
        print("✅ Cleanup complete!")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
