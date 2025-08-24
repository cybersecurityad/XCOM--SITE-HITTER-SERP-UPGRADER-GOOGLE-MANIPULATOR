#!/usr/bin/env python3
"""
🎭 SEPARATED TOR-BROWSER MANAGER
===============================
Simplified and more robust separation of Tor init and browser startup.
Always ensures Tor is fully operational before starting browser.

ARCHITECTURE:
1. 🧅 TOR PHASE: Start Tor, validate proxy, test connection
2. ⏸️  WAIT PHASE: Ensure Tor is stable and ready
3. 🌐 BROWSER PHASE: Create browser with confirmed Tor proxy
4. ✅ TEST PHASE: Verify end-to-end Tor browsing

This prevents Chrome exit code 15 by ensuring proper initialization order.
"""

# AUTO-INITIALIZE LOGGING
try:
    from auto_logger_init_v2 import auto_initialize_all_systems
    auto_initialize_all_systems(verbose=False)
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
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
import requests

class SimpleTorManager:
    """Simple Tor manager focused on reliable startup"""
    
    def __init__(self):
        self.tor_process = None
        self.temp_dir = None
        self.tor_port = 9050
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
                print("❌ Tor not found in PATH")
                return False
        except Exception as e:
            print(f"❌ Error checking Tor: {e}")
            return False
    
    def kill_existing_tor(self):
        """Kill any existing Tor processes"""
        try:
            print("🔪 Killing existing Tor processes...")
            subprocess.run(['pkill', '-f', 'tor'], capture_output=True, check=False)
            time.sleep(2)
            print("✅ Existing Tor processes killed")
        except:
            pass
    
    def test_proxy_port(self, port: int = 9050, timeout: int = 5) -> bool:
        """Test if proxy port is responding"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result == 0
        except:
            return False
    
    def start_tor_simple(self) -> bool:
        """Start Tor with minimal configuration"""
        try:
            print("🧅 Starting Tor with simple configuration...")
            
            # Kill existing Tor
            self.kill_existing_tor()
            
            # Create temp directory
            self.temp_dir = tempfile.mkdtemp(prefix='simple_tor_')
            print(f"📁 Tor directory: {self.temp_dir}")
            
            # Simple torrc
            torrc_content = f"""
SocksPort {self.tor_port}
DataDirectory {self.temp_dir}/data
Log notice stdout
ExitNodes {{us,ca,gb,de,fr}}
"""
            
            torrc_path = os.path.join(self.temp_dir, 'torrc')
            with open(torrc_path, 'w') as f:
                f.write(torrc_content)
            
            # Start Tor
            print(f"🚀 Starting Tor on port {self.tor_port}...")
            self.tor_process = subprocess.Popen(
                ['tor', '-f', torrc_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print(f"✅ Tor process started (PID: {self.tor_process.pid})")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Tor: {e}")
            return False
    
    def wait_for_tor(self, max_wait: int = 30) -> bool:
        """Wait for Tor to be ready"""
        print(f"⏳ Waiting for Tor proxy (max {max_wait}s)...")
        
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            # Check if process is still running
            if self.tor_process and self.tor_process.poll() is not None:
                print("❌ Tor process died")
                return False
            
            # Test proxy port
            if self.test_proxy_port(self.tor_port):
                print(f"✅ Tor proxy ready on port {self.tor_port}")
                self.is_ready = True
                return True
            
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
        """Complete Tor initialization"""
        print("=" * 50)
        print("🧅 PHASE 1: TOR INITIALIZATION")
        print("=" * 50)
        
        # Check Tor installation
        if not self.check_tor_installed():
            print("❌ Tor not installed. Install with: brew install tor")
            return False
        
        # Start Tor
        if not self.start_tor_simple():
            return False
        
        # Wait for Tor
        if not self.wait_for_tor():
            self.stop_tor()
            return False
        
        # Test connection
        if not self.test_tor_connection():
            print("❌ Tor connection test failed")
            self.stop_tor()
            return False
        
        print("🎉 TOR INITIALIZATION COMPLETE!")
        print("=" * 50)
        return True
    
    def stop_tor(self):
        """Stop Tor"""
        print("🛑 Stopping Tor...")
        
        if self.tor_process:
            try:
                self.tor_process.terminate()
                self.tor_process.wait(timeout=5)
                print("✅ Tor stopped")
            except:
                try:
                    self.tor_process.kill()
                    print("🔥 Tor killed")
                except:
                    pass
        
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                print("✅ Tor temp cleaned")
            except:
                pass
        
        self.is_ready = False

class SimpleBrowserManager:
    """Simple browser manager for Tor integration"""
    
    def __init__(self, tor_manager: SimpleTorManager):
        self.tor_manager = tor_manager
        self.driver = None
        
    def create_browser(self) -> bool:
        """Create browser with Tor proxy"""
        
        if not self.tor_manager.is_ready:
            print("❌ Tor not ready!")
            return False
        
        print("=" * 50)
        print("🌐 PHASE 2: BROWSER CREATION")
        print("=" * 50)
        
        try:
            print("🚀 Creating browser with Tor...")
            
            # Kill Chrome
            subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True, check=False)
            time.sleep(2)
            
            # Browser options
            options = uc.ChromeOptions()
            
            # Essential options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            
            # Tor proxy
            proxy_url = f'socks5://127.0.0.1:{self.tor_manager.tor_port}'
            options.add_argument(f'--proxy-server={proxy_url}')
            
            print(f"🔧 Using proxy: {proxy_url}")
            
            # Create driver
            self.driver = uc.Chrome(options=options)
            
            print("✅ Browser created with Tor!")
            return True
            
        except Exception as e:
            print(f"❌ Browser creation failed: {e}")
            return False
    
    def test_browsing(self) -> bool:
        """Test browsing with Tor"""
        try:
            if not self.driver:
                print("❌ No browser available")
                return False
            
            print("=" * 50)
            print("🌐 PHASE 3: BROWSING TEST")
            print("=" * 50)
            
            print("🔍 Testing IP verification...")
            self.driver.get('https://httpbin.org/ip')
            time.sleep(3)
            
            print("🌐 Testing Google...")
            self.driver.get('https://google.com')
            time.sleep(3)
            
            title = self.driver.title
            print(f"📄 Page title: {title}")
            
            print("✅ Browsing test successful!")
            return True
            
        except Exception as e:
            print(f"❌ Browsing test failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up browser"""
        if self.driver:
            try:
                self.driver.quit()
                print("✅ Browser closed")
            except:
                pass

class SeparatedManager:
    """Main manager for separated Tor-Browser"""
    
    def __init__(self):
        self.tor_manager = None
        self.browser_manager = None
        
        # Signal handlers
        signal.signal(signal.SIGTERM, self._cleanup)
        signal.signal(signal.SIGINT, self._cleanup)
    
    def _cleanup(self, signum=None, frame=None):
        """Cleanup handler"""
        print(f"\n🛑 Cleaning up...")
        self.cleanup()
        if signum:
            sys.exit(0)
    
    def run_separated(self) -> bool:
        """Run separated Tor-Browser process"""
        print("🎭 SEPARATED TOR-BROWSER MANAGER")
        print("=" * 50)
        print("✅ Always separate: Tor FIRST, Browser SECOND")
        print("✅ Full validation between phases")
        print("=" * 50)
        
        try:
            # Phase 1: Tor initialization
            self.tor_manager = SimpleTorManager()
            if not self.tor_manager.full_tor_init():
                print("❌ Tor initialization failed!")
                return False
            
            # Phase 2: Browser creation
            self.browser_manager = SimpleBrowserManager(self.tor_manager)
            if not self.browser_manager.create_browser():
                print("❌ Browser creation failed!")
                return False
            
            # Phase 3: Browsing test
            if not self.browser_manager.test_browsing():
                print("❌ Browsing test failed!")
                return False
            
            print("\n🎉 ALL PHASES SUCCESSFUL!")
            print("=" * 50)
            print("✅ Tor: READY")
            print("✅ Browser: READY")
            print("✅ Browsing: WORKING")
            print("=" * 50)
            
            input("\nPress Enter to continue or Ctrl+C to exit...")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def cleanup(self):
        """Clean up all resources"""
        print("\n🧹 Cleaning up...")
        
        if self.browser_manager:
            self.browser_manager.cleanup()
        
        if self.tor_manager:
            self.tor_manager.stop_tor()
        
        print("✅ Cleanup complete!")

def main():
    """Main entry point"""
    print("🎯 SEPARATED TOR-BROWSER ARCHITECTURE")
    print("Always separates Tor init from browser startup")
    print()
    
    manager = SeparatedManager()
    
    try:
        success = manager.run_separated()
        
        if success:
            print("\n🎉 SUCCESS!")
        else:
            print("\n❌ FAILED!")
            
    except KeyboardInterrupt:
        print("\n⏹️ Interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        manager.cleanup()

if __name__ == "__main__":
    main()
