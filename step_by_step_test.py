#!/usr/bin/env python3
"""
🔍 STEP-BY-STEP CRASH ISOLATION
==============================
Testing the main application step by step to find the exact crash point.
"""

import time
import random
import json
from datetime import datetime
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import signal
import sys
import os
import tempfile
import shutil
import psutil

class StepByStepTest:
    """Test each step of the main application"""
    
    def __init__(self):
        print("🔍 STEP-BY-STEP CRASH ISOLATION")
        print("=" * 40)
        self.temp_dir = None
        self.tor_process = None
        self.browser = None
        
    def step_1_setup_environment(self):
        """Step 1: Setup isolated environment"""
        try:
            print("📋 STEP 1: Setup Environment")
            print("-" * 30)
            
            self.temp_dir = tempfile.mkdtemp(prefix="step_test_")
            os.environ['CHROME_LOG_FILE'] = os.path.join(self.temp_dir, 'chrome.log')
            os.environ['TMPDIR'] = self.temp_dir
            
            print(f"✅ Environment setup: {self.temp_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Step 1 failed: {e}")
            return False
    
    def step_2_setup_signals(self):
        """Step 2: Setup signal handlers"""
        try:
            print("\n📋 STEP 2: Setup Signal Handlers")
            print("-" * 30)
            
            def dummy_handler(signum, frame):
                print(f"Signal {signum} received")
            
            signal.signal(signal.SIGTERM, dummy_handler)
            signal.signal(signal.SIGINT, dummy_handler)
            
            print("✅ Signal handlers setup")
            return True
            
        except Exception as e:
            print(f"❌ Step 2 failed: {e}")
            return False
    
    def step_3_kill_processes(self):
        """Step 3: Kill conflicting processes"""
        try:
            print("\n📋 STEP 3: Kill Conflicting Processes")
            print("-" * 30)
            
            processes_to_kill = ['chromedriver', 'Google Chrome', 'Chrome']
            killed_count = 0
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name']
                    if any(name in proc_name for name in processes_to_kill):
                        proc.kill()
                        killed_count += 1
                except:
                    pass
            
            time.sleep(2)
            print(f"✅ Killed {killed_count} conflicting processes")
            return True
            
        except Exception as e:
            print(f"❌ Step 3 failed: {e}")
            return False
    
    def step_4_start_tor(self):
        """Step 4: Start Tor process"""
        try:
            print("\n📋 STEP 4: Start Tor Process")
            print("-" * 30)
            
            # Kill existing Tor
            subprocess.run(['pkill', '-f', 'tor'], capture_output=True)
            time.sleep(2)
            
            # Start simple Tor
            self.tor_process = subprocess.Popen([
                'tor', '--quiet'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            print("⏳ Waiting for Tor...")
            
            # Test Tor connection (with timeout)
            for i in range(10):  # 20 second timeout
                try:
                    response = requests.get(
                        'http://httpbin.org/ip',
                        proxies={'http': 'socks5://127.0.0.1:9050',
                               'https': 'socks5://127.0.0.1:9050'},
                        timeout=3
                    )
                    if response.status_code == 200:
                        ip_data = response.json()
                        print(f"✅ Tor ready: {ip_data.get('origin', 'Unknown')}")
                        return True
                except:
                    pass
                
                time.sleep(2)
                print(f"⏳ Attempt {i+1}/10")
            
            print("❌ Tor startup timeout")
            return False
            
        except Exception as e:
            print(f"❌ Step 4 failed: {e}")
            return False
    
    def step_5_create_browser_options(self):
        """Step 5: Create browser options"""
        try:
            print("\n📋 STEP 5: Create Browser Options")
            print("-" * 30)
            
            options = Options()
            
            # Basic options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            
            # Tor proxy
            options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
            
            # User agent
            options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
            
            print("✅ Browser options created")
            return options
            
        except Exception as e:
            print(f"❌ Step 5 failed: {e}")
            return None
    
    def step_6_create_browser(self, options):
        """Step 6: Create browser instance"""
        try:
            print("\n📋 STEP 6: Create Browser Instance")
            print("-" * 30)
            
            service = Service()
            
            print("🚀 Creating Chrome WebDriver...")
            self.browser = webdriver.Chrome(service=service, options=options)
            self.browser.set_page_load_timeout(15)
            self.browser.implicitly_wait(5)
            
            print("✅ Browser created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Step 6 failed: {e}")
            return False
    
    def step_7_test_navigation(self):
        """Step 7: Test basic navigation"""
        try:
            if not self.browser:
                print("❌ No browser available")
                return False
                
            print("\n📋 STEP 7: Test Navigation")
            print("-" * 30)
            
            test_html = """
            <!DOCTYPE html>
            <html>
            <head><title>Step Test</title></head>
            <body><h1>Navigation Test Successful</h1></body>
            </html>
            """
            
            self.browser.get(f"data:text/html,{test_html}")
            title = self.browser.title or "No title"
            
            print(f"✅ Navigation successful: {title}")
            return True
            
        except Exception as e:
            print(f"❌ Step 7 failed: {e}")
            return False
    
    def step_8_test_real_website(self):
        """Step 8: Test real website"""
        try:
            if not self.browser:
                print("❌ No browser available")
                return False
                
            print("\n📋 STEP 8: Test Real Website")
            print("-" * 30)
            
            print("🌐 Loading httpbin.org...")
            self.browser.get("https://httpbin.org/ip")
            
            title = self.browser.title or "No title"
            print(f"✅ Real website loaded: {title}")
            
            # Keep open briefly
            print("👁️ Browser visible for 5 seconds...")
            time.sleep(5)
            
            return True
            
        except Exception as e:
            print(f"❌ Step 8 failed: {e}")
            return False
    
    def step_9_cleanup(self):
        """Step 9: Cleanup"""
        try:
            print("\n📋 STEP 9: Cleanup")
            print("-" * 30)
            
            if self.browser:
                self.browser.quit()
                print("✅ Browser closed")
            
            if self.tor_process:
                self.tor_process.terminate()
                self.tor_process.wait(timeout=5)
                print("✅ Tor stopped")
            
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                print("✅ Temp directory removed")
            
            return True
            
        except Exception as e:
            print(f"❌ Step 9 failed: {e}")
            return False
    
    def run_step_by_step_test(self):
        """Run complete step-by-step test"""
        
        steps = [
            ("Setup Environment", self.step_1_setup_environment),
            ("Setup Signals", self.step_2_setup_signals),
            ("Kill Processes", self.step_3_kill_processes),
            ("Start Tor", self.step_4_start_tor),
            ("Create Options", self.step_5_create_browser_options),
        ]
        
        options = None
        
        try:
            # Run initial steps
            for step_name, step_func in steps:
                result = step_func()
                if not result:
                    if step_name == "Create Options":
                        options = result  # None means failure
                        break
                    else:
                        print(f"\n🚨 CRASH POINT IDENTIFIED: {step_name}")
                        return False
                elif step_name == "Create Options":
                    options = result  # Options object
            
            if options is None:
                print("\n🚨 CRASH POINT: Browser options creation")
                return False
            
            # Continue with browser steps
            browser_steps = [
                ("Create Browser", lambda: self.step_6_create_browser(options)),
                ("Test Navigation", self.step_7_test_navigation),
                ("Test Real Website", self.step_8_test_real_website),
            ]
            
            for step_name, step_func in browser_steps:
                result = step_func()
                if not result:
                    print(f"\n🚨 CRASH POINT IDENTIFIED: {step_name}")
                    return False
            
            print("\n🎉 ALL STEPS COMPLETED SUCCESSFULLY!")
            print("✅ No crash points found in step-by-step test")
            return True
            
        except KeyboardInterrupt:
            print("\n⚠️ Test interrupted")
            return False
        except Exception as e:
            print(f"\n💥 UNEXPECTED CRASH: {e}")
            return False
        finally:
            self.step_9_cleanup()

def main():
    """Main test function"""
    tester = StepByStepTest()
    
    try:
        success = tester.run_step_by_step_test()
        
        if success:
            print("\n🔍 CONCLUSION:")
            print("   All steps work individually")
            print("   Issue might be in:")
            print("   1. Rapid step execution")
            print("   2. Resource management")
            print("   3. VS Code interaction")
        else:
            print("\n🔍 CONCLUSION:")
            print("   Crash point identified above")
            print("   Focus debugging on that step")
            
    except Exception as e:
        print(f"\n💥 Main test crashed: {e}")

if __name__ == "__main__":
    main()
