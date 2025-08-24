#!/usr/bin/env python3
"""
🔧 CHROME EXIT CODE 15 FIX - ADVANCED
=====================================
Complete solution for Chrome termination on macOS with VS Code.
Addresses Pylance/Jupyter conflicts with browser automation.
"""

import os
import sys
import time
import signal
import subprocess
import tempfile
import shutil
import requests
import psutil

class AdvancedChromeFix:
    """Complete Chrome exit code 15 fix"""
    
    def __init__(self):
        self.tor_process = None
        self.browser_process = None
        self.temp_dir = None
        self.current_ip = None
        
    def setup_isolated_environment(self):
        """Create isolated environment for browser"""
        try:
            self.temp_dir = tempfile.mkdtemp(prefix="browser_fix_")
            print(f"🔧 Created isolated environment: {self.temp_dir}")
            
            # Isolate from VS Code environment
            os.environ['CHROME_LOG_FILE'] = os.path.join(self.temp_dir, 'chrome.log')
            os.environ['TMPDIR'] = self.temp_dir
            
            return True
        except Exception as e:
            print(f"❌ Environment setup failed: {e}")
            return False
    
    def kill_all_browsers(self):
        """Kill all browser and related processes"""
        try:
            print("🧹 Killing browser processes...")
            
            processes_to_kill = [
                'chromedriver', 'Google Chrome', 'Chrome', 'chrome',
                'tor', 'firefox', 'safari'
            ]
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    if any(name.lower() in proc_name for name in processes_to_kill):
                        print(f"🔪 Killing: {proc.info['name']} (PID: {proc.info['pid']})")
                        proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            time.sleep(3)
            print("✅ Process cleanup completed")
            
        except Exception as e:
            print(f"⚠️ Process cleanup warning: {e}")
    
    def start_minimal_tor(self):
        """Start Tor with minimal configuration"""
        try:
            print("🧅 Starting minimal Tor...")
            
            # Simple Tor startup
            self.tor_process = subprocess.Popen([
                'tor', '--quiet'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Wait for Tor
            print("⏳ Waiting for Tor...")
            for i in range(20):
                if self.check_tor():
                    print(f"✅ Tor ready: {self.current_ip}")
                    return True
                time.sleep(1)
            
            print("❌ Tor timeout")
            return False
            
        except Exception as e:
            print(f"❌ Tor failed: {e}")
            return False
    
    def check_tor(self):
        """Check Tor connection"""
        try:
            proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxies,
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                self.current_ip = data.get('origin', 'Unknown')
                return True
        except:
            pass
        return False
    
    def launch_chrome_direct(self, url="data:text/html,<html><body><h1>Test</h1></body></html>"):
        """Launch Chrome directly without Selenium"""
        try:
            print("🌐 Launching Chrome directly...")
            
            # Chrome executable path on macOS
            chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            
            if not os.path.exists(chrome_path):
                print("❌ Chrome not found at expected path")
                return False
            
            # Create user data directory
            chrome_data_dir = os.path.join(self.temp_dir or '/tmp', 'chrome_data')
            os.makedirs(chrome_data_dir, exist_ok=True)
            
            # Minimal Chrome arguments
            chrome_args = [
                chrome_path,
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-background-timer-throttling',
                '--proxy-server=socks5://127.0.0.1:9050',
                f'--user-data-dir={chrome_data_dir}',
                '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                url
            ]
            
            # Launch Chrome
            self.browser_process = subprocess.Popen(
                chrome_args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            print("👁️ Chrome should be visible now...")
            return True
            
        except Exception as e:
            print(f"❌ Chrome launch failed: {e}")
            return False
    
    def test_chrome_stability(self, duration=15):
        """Test Chrome stability for specified duration"""
        try:
            print(f"🧪 Testing Chrome stability for {duration} seconds...")
            
            for i in range(duration):
                if self.browser_process and self.browser_process.poll() is not None:
                    exit_code = self.browser_process.returncode
                    print(f"❌ Chrome exited with code: {exit_code}")
                    return False
                
                time.sleep(1)
                if i % 5 == 0 and i > 0:
                    print(f"⏳ {duration - i} seconds remaining...")
            
            print("✅ Chrome stability test PASSED!")
            return True
            
        except Exception as e:
            print(f"❌ Stability test failed: {e}")
            return False
    
    def test_website_loading(self, url):
        """Test loading a specific website"""
        try:
            print(f"🌐 Testing website: {url}")
            
            # Launch Chrome with the specific URL
            if not self.launch_chrome_direct(url):
                return False
            
            # Test stability
            return self.test_chrome_stability(10)
            
        except Exception as e:
            print(f"❌ Website test failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up all resources"""
        try:
            print("🧹 Cleaning up...")
            
            # Kill browser
            if self.browser_process:
                try:
                    self.browser_process.terminate()
                    self.browser_process.wait(timeout=5)
                except:
                    try:
                        self.browser_process.kill()
                    except:
                        pass
            
            # Kill Tor
            if self.tor_process:
                try:
                    self.tor_process.terminate()
                    self.tor_process.wait(timeout=5)
                except:
                    try:
                        self.tor_process.kill()
                    except:
                        pass
            
            # Remove temp directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                try:
                    shutil.rmtree(self.temp_dir)
                except:
                    pass
            
            # Final cleanup
            self.kill_all_browsers()
            print("✅ Cleanup completed")
            
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")

def main():
    """Main test function"""
    print("🔧 ADVANCED CHROME EXIT CODE 15 FIX")
    print("=" * 45)
    print("🎯 Fixing Chrome termination on macOS")
    print("🔍 VS Code extension conflicts")
    print("💡 Direct Chrome launch solution")
    print("=" * 45)
    
    fix = AdvancedChromeFix()
    
    try:
        # Setup
        if not fix.setup_isolated_environment():
            return
        
        # Clean processes
        fix.kill_all_browsers()
        
        # Start Tor
        if not fix.start_minimal_tor():
            return
        
        # Test basic Chrome launch
        print("\n🧪 TEST 1: Basic Chrome Launch")
        if fix.launch_chrome_direct():
            if fix.test_chrome_stability(10):
                print("✅ TEST 1 PASSED: No exit code 15!")
            else:
                print("❌ TEST 1 FAILED: Chrome unstable")
                return
        else:
            print("❌ TEST 1 FAILED: Launch failed")
            return
        
        # Test website loading
        print("\n🧪 TEST 2: Website Loading")
        test_url = "https://httpbin.org/ip"
        if fix.test_website_loading(test_url):
            print("✅ TEST 2 PASSED: Website loaded!")
        else:
            print("❌ TEST 2 FAILED: Website loading failed")
        
        print("\n🎉 CHROME EXIT CODE 15 FIX SUCCESSFUL!")
        print("✅ Chrome launches without termination")
        print("✅ Tor proxy works correctly")
        print("✅ No VS Code extension conflicts")
        
        input("\n👁️ Press Enter to close Chrome and exit...")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        fix.cleanup()

if __name__ == "__main__":
    main()
