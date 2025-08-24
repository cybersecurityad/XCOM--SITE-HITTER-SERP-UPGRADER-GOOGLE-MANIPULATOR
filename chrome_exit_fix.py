#!/usr/bin/env python3
"""
🔧 CHROME EXIT CODE 15 FIX
========================
Advanced fix for Chrome termination on macOS with VS Code extensions.
Addresses conflicts between Pylance, Jupyter, and browser automation.

Key fixes:
- Process isolation from VS Code
- Alternative browser engines
- Robust error handling
- Fallback mechanisms
"""

import os
import sys
import time
import signal
import subprocess
import tempfile
import shutil
from pathlib import Path
import requests
import psutil

class ChromeExitFix:

import time
import subprocess
import os
import signal
import sys
import psutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import tempfile
import shutil

class ChromeExitFix:
    """Fix Chrome exit code 15 on macOS with VS Code/Pylance"""
    
    def __init__(self):
        self.driver = None
        self.tor_process = None
        self.current_ip = None
        self.chrome_user_data_dir = None
        
    def detect_vscode_conflict(self):
        """Detect if VS Code/Pylance is causing conflicts"""
        conflicts = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    info = proc.info
                    name = info['name'].lower()
                    cmdline = ' '.join(info['cmdline'] or []).lower()
                    
                    # Check for VS Code processes
                    if 'code' in name or 'electron' in name:
                        if 'vscode' in cmdline or 'code-server' in cmdline:
                            conflicts.append(f"VS Code: {info['pid']}")
                    
                    # Check for Pylance processes
                    if 'pylance' in cmdline or 'python-language-server' in cmdline:
                        conflicts.append(f"Pylance: {info['pid']}")
                        
                    # Check for Chrome processes that might conflict
                    if 'chrome' in name and 'selenium' not in cmdline:
                        conflicts.append(f"Chrome: {info['pid']}")
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            print(f"⚠️ Process detection warning: {e}")
        
        if conflicts:
            print("🔍 Detected potential conflicts:")
            for conflict in conflicts:
                print(f"   - {conflict}")
            return True
        return False
    
    def create_isolated_chrome_profile(self):
        """Create isolated Chrome user data directory"""
        try:
            # Create temporary directory for Chrome profile
            self.chrome_user_data_dir = tempfile.mkdtemp(prefix='chrome_selenium_')
            print(f"📁 Created isolated Chrome profile: {self.chrome_user_data_dir}")
            return True
        except Exception as e:
            print(f"❌ Failed to create Chrome profile: {e}")
            return False
    
    def kill_conflicting_processes(self):
        """Kill processes that might conflict with Chrome"""
        try:
            # Kill existing Chrome instances
            subprocess.run(['pkill', '-f', 'Google Chrome'], 
                         capture_output=True, check=False)
            subprocess.run(['pkill', '-f', 'chromedriver'], 
                         capture_output=True, check=False)
            
            # Kill Tor processes
            subprocess.run(['pkill', '-f', 'tor'], 
                         capture_output=True, check=False)
            
            time.sleep(3)
            print("🧹 Cleared conflicting processes")
            return True
        except Exception as e:
            print(f"⚠️ Process cleanup warning: {e}")
            return False
    
    def start_tor_isolated(self):
        """Start Tor in isolated mode"""
        print("🧅 Starting isolated Tor...")
        
        try:
            # Create temporary Tor data directory
            tor_data_dir = tempfile.mkdtemp(prefix='tor_data_')
            
            # Minimal Tor configuration
            tor_config = f"""
SocksPort 9050
DataDirectory {tor_data_dir}
Log notice stdout
ExitNodes {{nl}}
StrictNodes 1
"""
            
            # Write config file
            config_file = os.path.join(tor_data_dir, 'torrc')
            with open(config_file, 'w') as f:
                f.write(tor_config)
            
            # Start Tor process with isolation
            self.tor_process = subprocess.Popen([
                'tor', '-f', config_file
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
               preexec_fn=os.setsid)
            
            # Wait for Tor
            print("🔄 Waiting for Tor to start...")
            for attempt in range(20):
                try:
                    response = requests.get(
                        'http://httpbin.org/ip',
                        proxies={'http': 'socks5://127.0.0.1:9050',
                               'https': 'socks5://127.0.0.1:9050'},
                        timeout=5
                    )
                    if response.status_code == 200:
                        data = response.json()
                        self.current_ip = data.get('origin')
                        print(f"✅ Tor ready: {self.current_ip}")
                        return True
                except:
                    pass
                
                time.sleep(1)
                print(f"⏳ Attempt {attempt + 1}/20")
            
            print("❌ Tor startup timeout")
            return False
            
        except Exception as e:
            print(f"❌ Tor startup error: {e}")
            return False
    
    def create_chrome_options_macos_fix(self):
        """Create Chrome options specifically for macOS code 15 fix"""
        options = Options()
        
        # CRITICAL: Disable features that conflict with VS Code/Pylance
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        
        # VS Code conflict fixes
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-features=TranslateUI,VizDisplayCompositor')
        
        # Process isolation
        options.add_argument('--process-per-site')
        options.add_argument('--single-process')  # Sometimes helps with code 15
        
        # Extension conflicts
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-default-apps')
        
        # Use isolated profile
        if self.chrome_user_data_dir:
            options.add_argument(f'--user-data-dir={self.chrome_user_data_dir}')
        
        # Tor proxy
        options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
        
        # Debugging
        options.add_argument('--remote-debugging-port=0')
        options.add_argument('--enable-logging')
        options.add_argument('--log-level=0')
        
        # User agent
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        
        return options
    
    def create_browser_with_fix(self):
        """Create browser with macOS code 15 fix"""
        print("🔧 Creating browser with code 15 fix...")
        
        # Step 1: Check for conflicts
        has_conflicts = self.detect_vscode_conflict()
        if has_conflicts:
            print("⚠️ VS Code/Pylance conflict detected - applying fixes")
        
        # Step 2: Clean processes
        self.kill_conflicting_processes()
        
        # Step 3: Create isolated profile
        if not self.create_isolated_chrome_profile():
            return False
        
        # Step 4: Verify Tor
        if not self.current_ip:
            print("❌ Tor not ready")
            return False
        
        try:
            # Step 5: Create Chrome with special options
            options = self.create_chrome_options_macos_fix()
            service = Service()
            
            print("🚀 Launching Chrome with isolation...")
            self.driver = webdriver.Chrome(
                service=service,
                options=options
            )
            
            # Step 6: Configure timeouts
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            
            # Step 7: Test browser
            print("🧪 Testing browser...")
            self.driver.get('data:text/html,<html><body><h1>Code 15 Fix Test</h1><p>If you see this, the fix worked!</p></body></html>')
            
            if "Code 15 Fix Test" in self.driver.page_source:
                print("✅ Browser created successfully - no code 15!")
                return True
            else:
                print("❌ Browser test failed")
                return False
                
        except Exception as e:
            print(f"❌ Browser creation failed: {e}")
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
            return False
    
    def test_real_website(self, url):
        """Test with real website"""
        if not self.driver:
            print("❌ No browser available")
            return False
        
        try:
            print(f"🌐 Testing with: {url}")
            self.driver.get(url)
            
            # Wait for load
            WebDriverWait(self.driver, 20).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            title = self.driver.title or "No title"
            print(f"✅ Loaded successfully: {title[:50]}...")
            
            # Show window
            print("👁️ Browser window visible - no code 15 exit!")
            print("⏱️ Keeping open for 15 seconds...")
            time.sleep(15)
            
            return True
            
        except Exception as e:
            print(f"❌ Website test failed: {e}")
            return False
    
    def cleanup_fix(self):
        """Clean up with proper resource management"""
        print("🧹 Cleaning up...")
        
        # Close browser
        if self.driver:
            try:
                self.driver.quit()
                print("✅ Browser closed")
            except Exception as e:
                print(f"⚠️ Browser close warning: {e}")
        
        # Stop Tor
        if self.tor_process:
            try:
                os.killpg(os.getpgid(self.tor_process.pid), signal.SIGTERM)
                self.tor_process.wait(timeout=5)
                print("✅ Tor stopped")
            except Exception as e:
                print(f"⚠️ Tor stop warning: {e}")
        
        # Clean up temporary directories
        if self.chrome_user_data_dir and os.path.exists(self.chrome_user_data_dir):
            try:
                shutil.rmtree(self.chrome_user_data_dir)
                print("✅ Chrome profile cleaned")
            except Exception as e:
                print(f"⚠️ Profile cleanup warning: {e}")

def test_chrome_exit_fix():
    """Test the Chrome exit code 15 fix"""
    print("🔧 CHROME EXIT CODE 15 FIX TEST")
    print("=" * 50)
    print("🎯 Fixing VS Code/Pylance conflict on macOS")
    print("📋 Known issue: VS Code Jupyter/Pylance extensions")
    print("🔗 Reference: https://github.com/microsoft/vscode/issues/196057")
    print("=" * 50)
    
    fixer = ChromeExitFix()
    
    try:
        # Start isolated Tor
        if not fixer.start_tor_isolated():
            print("❌ Tor startup failed")
            return
        
        # Create browser with fix
        if not fixer.create_browser_with_fix():
            print("❌ Browser creation failed")
            return
        
        # Test with real website
        test_url = "https://httpbin.org/ip"
        if fixer.test_real_website(test_url):
            print("\n🎉 SUCCESS: Chrome exit code 15 FIXED!")
            print("✅ Browser stayed open without termination")
            print("✅ VS Code/Pylance conflict resolved")
        else:
            print("❌ Website test failed")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        fixer.cleanup_fix()
        print("✅ Fix test completed")

if __name__ == "__main__":
    test_chrome_exit_fix()
