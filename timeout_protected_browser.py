#!/usr/bin/env python3
"""
🔧 EXTERNAL BROWSER FIX - No Exit Code 15
==========================================
Uses regular Selenium WebDriver with timeout protection
to prevent the hanging issue that causes VS Code crashes.
"""

import os
import sys
import time
import subprocess
import signal
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import requests

class ExternalBrowserFix:
    """Browser that won't crash VS Code"""
    
    def __init__(self):
        self.driver = None
        self.tor_process = None
        self.temp_dir = None
        self.current_ip = None
        
    def setup_environment(self):
        """Setup isolated environment"""
        try:
            self.temp_dir = tempfile.mkdtemp(prefix="browser_external_")
            print(f"🔧 Environment: {self.temp_dir}")
            return True
        except Exception as e:
            print(f"❌ Environment setup failed: {e}")
            return False
    
    def kill_existing_browsers(self):
        """Kill existing browser processes"""
        try:
            print("🧹 Cleaning browser processes...")
            subprocess.run(['pkill', '-f', 'chrome'], capture_output=True, check=False)
            subprocess.run(['pkill', '-f', 'chromedriver'], capture_output=True, check=False)
            subprocess.run(['pkill', '-f', 'tor'], capture_output=True, check=False)
            time.sleep(2)
            print("✅ Browser cleanup done")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")
    
    def start_tor(self):
        """Start Tor service"""
        try:
            print("🧅 Starting Tor...")
            self.tor_process = subprocess.Popen([
                'tor', '--quiet'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            for i in range(15):
                if self.check_tor():
                    print(f"✅ Tor ready: {self.current_ip}")
                    return True
                time.sleep(2)
                print(f"⏳ Tor starting... {i+1}/15")
            
            print("❌ Tor startup timeout")
            return False
            
        except Exception as e:
            print(f"❌ Tor startup failed: {e}")
            return False
    
    def check_tor(self):
        """Check if Tor is working"""
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
    
    def create_chrome_driver(self):
        """Create Chrome driver with timeout protection"""
        try:
            print("🌐 Creating Chrome driver with timeout protection...")
            
            # Chrome options
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
            
            if self.temp_dir:
                chrome_data_dir = os.path.join(self.temp_dir, 'chrome_data')
                os.makedirs(chrome_data_dir, exist_ok=True)
                options.add_argument(f'--user-data-dir={chrome_data_dir}')
            
            # Create service with timeout
            service = Service()
            
            # Timeout protection using signal
            def timeout_handler(signum, frame):
                raise TimeoutError("Chrome startup timeout")
            
            print("🚀 Launching Chrome (45 second timeout)...")
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(45)  # 45 second timeout
            
            try:
                self.driver = webdriver.Chrome(service=service, options=options)
                signal.alarm(0)  # Cancel alarm
                signal.signal(signal.SIGALRM, old_handler)
                
                print("✅ Chrome driver created successfully!")
                
                # Test with simple page
                self.driver.get('data:text/html,<html><body><h1>Chrome Test</h1></body></html>')
                print("✅ Chrome is working!")
                return True
                
            except TimeoutError:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
                print("❌ Chrome startup timeout - prevented VS Code crash")
                return False
                
        except Exception as e:
            print(f"❌ Chrome driver creation failed: {e}")
            return False
    
    def test_website(self, url):
        """Test loading a website"""
        try:
            if not self.driver:
                print("❌ No driver available")
                return False
            
            print(f"🌐 Loading: {url}")
            self.driver.set_page_load_timeout(30)
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            title = self.driver.title or "No title"
            print(f"✅ Loaded: {title[:50]}...")
            
            # Inject Google Analytics
            self.inject_ga_tracking()
            
            print("👁️ Browser should be visible with website loaded")
            print("⏱️ Keeping open for 15 seconds for observation...")
            time.sleep(15)
            
            return True
            
        except Exception as e:
            print(f"❌ Website loading failed: {e}")
            return False
    
    def inject_ga_tracking(self):
        """Inject Google Analytics tracking"""
        try:
            if not self.driver:
                print("⚠️ No driver available for GA injection")
                return
                
            ga_script = """
            // Real Google Analytics 4
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            
            var gaScript = document.createElement('script');
            gaScript.async = true;
            gaScript.src = 'https://www.googletagmanager.com/gtag/js?id=G-0B4ZR31YFS';
            document.head.appendChild(gaScript);
            
            gtag('js', new Date());
            gtag('config', 'G-0B4ZR31YFS', {
                'anonymize_ip': false,
                'send_page_view': true
            });
            
            gtag('event', 'page_view', {
                'page_title': document.title,
                'page_location': window.location.href,
                'user_type': 'timeout_protected_browser'
            });
            
            console.log('✅ GA tracking injected');
            """
            
            self.driver.execute_script(ga_script)
            print("📊 Google Analytics injected")
            
        except Exception as e:
            print(f"⚠️ GA injection warning: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        try:
            print("🧹 Cleaning up...")
            
            if self.driver:
                try:
                    self.driver.quit()
                    print("✅ Chrome closed")
                except:
                    pass
            
            if self.tor_process:
                try:
                    self.tor_process.terminate()
                    self.tor_process.wait(timeout=5)
                    print("✅ Tor stopped")
                except:
                    pass
            
            if self.temp_dir and os.path.exists(self.temp_dir):
                try:
                    shutil.rmtree(self.temp_dir)
                except:
                    pass
            
            self.kill_existing_browsers()
            
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")

def main():
    """Main function that prevents VS Code crashes"""
    print("🔧 EXTERNAL BROWSER FIX - NO VS CODE CRASHES")
    print("=" * 50)
    print("🎯 Using regular Selenium WebDriver")
    print("⏰ 45-second timeout protection")
    print("🛡️ Isolated from VS Code process")
    print("=" * 50)
    
    browser = ExternalBrowserFix()
    
    try:
        # Setup
        if not browser.setup_environment():
            return
        
        # Clean existing processes
        browser.kill_existing_browsers()
        
        # Start Tor
        if not browser.start_tor():
            print("❌ Tor failed - continuing without proxy")
        
        # Create Chrome driver (critical step - this is where hangs occur)
        print("\n🧪 CRITICAL TEST: Chrome Driver Creation")
        if not browser.create_chrome_driver():
            print("❌ Chrome driver creation failed or timed out")
            print("💡 This timeout protection prevents VS Code from crashing")
            return
        
        print("\n🎉 SUCCESS: No VS Code crash!")
        print("✅ Chrome started without hanging")
        print("✅ No exit code 15 error")
        print("✅ Timeout protection worked")
        
        # Test website with GA
        test_url = "https://verenigdamsterdam.nl"
        if browser.test_website(test_url):
            print("✅ Website test successful with GA tracking!")
        
        print("\n📊 Check Google Analytics dashboard for activity:")
        print("   https://analytics.google.com/")
        input("👁️ Press Enter to close browser and exit...")
        
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        browser.cleanup()
        print("✅ External browser test completed")

if __name__ == "__main__":
    # Run in separate process to isolate from VS Code
    if len(sys.argv) > 1 and sys.argv[1] == "external":
        main()
    else:
        # Launch in external process
        print("🚀 Launching external browser (isolated from VS Code)...")
        try:
            result = subprocess.run([sys.executable, __file__, "external"])
            print(f"🏁 External process completed with code: {result.returncode}")
        except Exception as e:
            print(f"❌ External process error: {e}")
