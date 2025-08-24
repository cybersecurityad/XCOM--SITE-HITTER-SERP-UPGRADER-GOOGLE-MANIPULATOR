#!/usr/bin/env python3
"""
🎭 SEPARATED TOR + BROWSER STARTUP TEST
=====================================
Test browser startup separately from Tor to isolate exit code 15 issue.
This will help identify if the problem is:
1. First browser startup (Chrome initialization)
2. Tor integration specifically
3. Multiple browser instances
"""

import time
import os
import sys
import signal
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class SeparatedStartupTest:
    """Test browser and Tor startup separately"""
    
    def __init__(self):
        self.browser = None
        self.tor_process = None
        self.running = True
        self.ga_tracking_id = "G-0B4ZR31YFS"
        
        # Handle signals
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🔄 Signal {signum} received. Gracefully shutting down...")
        self.running = False
        self.cleanup()
        sys.exit(0)
    
    def kill_existing_processes(self):
        """Kill any existing Chrome and Tor processes"""
        print("🧹 Killing existing processes...")
        
        # Kill Chrome processes
        try:
            result = subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True, check=False)
            if result.returncode == 0:
                print("✅ Killed existing Chrome processes")
            else:
                print("ℹ️ No existing Chrome processes found")
        except:
            print("⚠️ Could not kill Chrome processes")
        
        # Kill chromedriver processes
        try:
            result = subprocess.run(['pkill', '-f', 'chromedriver'], capture_output=True, check=False)
            if result.returncode == 0:
                print("✅ Killed existing chromedriver processes")
            else:
                print("ℹ️ No existing chromedriver processes found")
        except:
            print("⚠️ Could not kill chromedriver processes")
        
        # Kill Tor processes
        try:
            result = subprocess.run(['pkill', '-f', 'tor'], capture_output=True, check=False)
            if result.returncode == 0:
                print("✅ Killed existing Tor processes")
            else:
                print("ℹ️ No existing Tor processes found")
        except:
            print("⚠️ Could not kill Tor processes")
        
        # Wait for processes to die
        time.sleep(3)
        print("✅ Process cleanup completed")
    
    def test_first_browser_startup(self):
        """Test the very first browser startup without any proxy"""
        try:
            print("\n1️⃣ TESTING FIRST BROWSER STARTUP")
            print("=" * 50)
            print("🎯 Testing browser creation without any proxy")
            print("🔍 This will identify if Chrome has startup issues")
            
            # Clean environment
            self.kill_existing_processes()
            
            print("🌐 Creating first browser instance...")
            
            options = Options()
            # Minimal options for first startup
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            
            service = Service()
            
            # Attempt browser creation
            browser = webdriver.Chrome(service=service, options=options)
            browser.set_page_load_timeout(15)
            browser.implicitly_wait(5)
            
            print("✅ First browser created successfully!")
            
            # Test basic functionality
            print("🧪 Testing basic browser functionality...")
            browser.get("data:text/html,<html><body><h1>First Browser Test</h1></body></html>")
            time.sleep(2)
            
            if "First Browser Test" in browser.page_source:
                print("✅ First browser functionality confirmed!")
                
                # Test website access
                print("🌐 Testing website access...")
                browser.get("https://verenigdamsterdam.nl")
                time.sleep(3)
                print(f"✅ Website loaded: {browser.title[:50]}...")
                
                browser.quit()
                print("✅ First browser closed successfully!")
                
                return True
            else:
                print("❌ First browser functionality test failed")
                browser.quit()
                return False
                
        except Exception as e:
            print(f"❌ First browser startup failed: {e}")
            try:
                if browser:
                    browser.quit()
            except:
                pass
            return False
    
    def test_second_browser_startup(self):
        """Test second browser startup (after first one worked)"""
        try:
            print("\n2️⃣ TESTING SECOND BROWSER STARTUP")
            print("=" * 50)
            print("🎯 Testing if second browser creation also works")
            
            # Small delay between browsers
            time.sleep(2)
            
            print("🌐 Creating second browser instance...")
            
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            
            service = Service()
            browser = webdriver.Chrome(service=service, options=options)
            browser.set_page_load_timeout(15)
            
            print("✅ Second browser created successfully!")
            
            # Test functionality
            browser.get("data:text/html,<html><body><h1>Second Browser Test</h1></body></html>")
            time.sleep(2)
            
            if "Second Browser Test" in browser.page_source:
                print("✅ Second browser functionality confirmed!")
                browser.quit()
                print("✅ Second browser closed successfully!")
                return True
            else:
                print("❌ Second browser functionality failed")
                browser.quit()
                return False
                
        except Exception as e:
            print(f"❌ Second browser startup failed: {e}")
            return False
    
    def test_tor_startup_only(self):
        """Test Tor startup separately from browser"""
        try:
            print("\n3️⃣ TESTING TOR STARTUP ONLY")
            print("=" * 50)
            print("🎯 Testing Tor initialization without browser")
            
            import tempfile
            import shutil
            
            # Create temp directory for Tor
            temp_dir = tempfile.mkdtemp(prefix='tor_test_')
            print(f"📁 Tor temp directory: {temp_dir}")
            
            # Create simple torrc
            torrc_content = f"""
SocksPort 9050
DataDirectory {temp_dir}/tor_data
ExitNodes {{nl}}
StrictNodes 1
Log notice stdout
"""
            
            torrc_path = os.path.join(temp_dir, 'torrc')
            with open(torrc_path, 'w') as f:
                f.write(torrc_content)
            
            print("🧅 Starting Tor process...")
            
            # Start Tor
            cmd = ['tor', '-f', torrc_path]
            self.tor_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            # Wait for Tor bootstrap
            print("⏳ Waiting for Tor bootstrap...")
            start_time = time.time()
            bootstrap_complete = False
            
            while time.time() - start_time < 30:  # 30 second timeout
                if self.tor_process.poll() is not None:
                    print("❌ Tor process died")
                    return False
                
                if self.tor_process.stdout:
                    line = self.tor_process.stdout.readline()
                    if line and "Bootstrapped 100%" in line:
                        bootstrap_complete = True
                        print("✅ Tor bootstrap complete!")
                        break
                
                time.sleep(0.5)
            
            if bootstrap_complete:
                print("✅ Tor started successfully (no browser)")
                
                # Stop Tor
                self.tor_process.terminate()
                self.tor_process.wait()
                print("✅ Tor stopped successfully")
                
                # Cleanup
                shutil.rmtree(temp_dir)
                print("🗑️ Tor cleanup completed")
                
                return True
            else:
                print("❌ Tor bootstrap did not complete")
                return False
                
        except Exception as e:
            print(f"❌ Tor startup failed: {e}")
            return False
    
    def test_browser_after_tor(self):
        """Test browser creation after Tor has been running"""
        try:
            print("\n4️⃣ TESTING BROWSER AFTER TOR")
            print("=" * 50)
            print("🎯 Starting Tor first, then creating browser")
            
            # This simulates the current failing scenario
            print("🧅 Starting Tor first...")
            
            # Simulate Tor startup (simplified)
            if not self.test_tor_startup_only():
                print("❌ Tor startup failed, skipping browser test")
                return False
            
            print("🌐 Now creating browser after Tor...")
            
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            
            service = Service()
            browser = webdriver.Chrome(service=service, options=options)
            
            print("✅ Browser created after Tor!")
            browser.quit()
            print("✅ Browser closed after Tor!")
            
            return True
            
        except Exception as e:
            print(f"❌ Browser after Tor failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.browser:
                self.browser.quit()
            if self.tor_process:
                self.tor_process.terminate()
                self.tor_process.wait()
            self.kill_existing_processes()
        except:
            pass

def main():
    """Run separated startup tests"""
    print("=" * 60)
    print("🧪 SEPARATED TOR + BROWSER STARTUP TESTS")
    print("=" * 60)
    print("🎯 Isolating Chrome exit code 15 issue")
    print("🔍 Testing each component separately")
    print("=" * 60)
    
    tester = SeparatedStartupTest()
    
    results = {}
    
    try:
        # Test 1: First browser startup
        results['first_browser'] = tester.test_first_browser_startup()
        
        # Test 2: Second browser startup  
        results['second_browser'] = tester.test_second_browser_startup()
        
        # Test 3: Tor startup only
        results['tor_only'] = tester.test_tor_startup_only()
        
        # Test 4: Browser after Tor
        results['browser_after_tor'] = tester.test_browser_after_tor()
        
        # Summary
        print("\n📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"1️⃣ First Browser:      {'✅ PASS' if results['first_browser'] else '❌ FAIL'}")
        print(f"2️⃣ Second Browser:     {'✅ PASS' if results['second_browser'] else '❌ FAIL'}")
        print(f"3️⃣ Tor Only:           {'✅ PASS' if results['tor_only'] else '❌ FAIL'}")
        print(f"4️⃣ Browser After Tor:  {'✅ PASS' if results['browser_after_tor'] else '❌ FAIL'}")
        
        # Analysis
        print("\n🔍 ANALYSIS:")
        if not results['first_browser']:
            print("❌ ISSUE: First browser startup fails")
            print("💡 CAUSE: Chrome initialization problem")
        elif not results['second_browser']:
            print("❌ ISSUE: Second browser startup fails")  
            print("💡 CAUSE: Process cleanup or resource conflict")
        elif not results['tor_only']:
            print("❌ ISSUE: Tor startup fails")
            print("💡 CAUSE: Tor configuration problem")
        elif not results['browser_after_tor']:
            print("❌ ISSUE: Browser fails after Tor runs")
            print("💡 CAUSE: Tor affects browser environment")
        else:
            print("✅ ALL TESTS PASS: Issue is with proxy configuration")
        
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
    finally:
        tester.cleanup()

if __name__ == "__main__":
    main()
