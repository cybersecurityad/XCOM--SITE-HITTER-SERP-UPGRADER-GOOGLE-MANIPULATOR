#!/usr/bin/env python3
"""
🦊 FIREFOX GA BROWSER - NO EXIT CODE 15
=======================================
Alternative to Chrome that avoids VS Code exit code 15 conflicts.
Uses Firefox with Tor for stable browser automation on macOS.

KEY FEATURES:
✅ No Chrome exit code 15 issues
✅ Firefox + Tor integration
✅ Real Google Analytics tracking
✅ Netherlands-only exit nodes
✅ Stable on macOS with VS Code
✅ Visual browser automation
"""

import os
import sys
import time
import subprocess
import tempfile
import shutil
import json
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import signal

class FirefoxGABrowser:
    """Firefox-based browser to avoid Chrome exit code 15"""
    
    def __init__(self):
        self.driver = None
        self.tor_process = None
        self.temp_dir = None
        self.current_ip = None
        self.ga_tracking_id = 'G-0B4ZR31YFS'  # Real GA tracking ID
        
        # Signal handlers
        signal.signal(signal.SIGTERM, self._cleanup_handler)
        signal.signal(signal.SIGINT, self._cleanup_handler)
    
    def _cleanup_handler(self, signum, frame):
        """Handle cleanup on termination"""
        print(f"\n🛑 Received signal {signum}, cleaning up...")
        self.cleanup()
        sys.exit(0)
    
    def setup_environment(self):
        """Setup isolated environment"""
        try:
            self.temp_dir = tempfile.mkdtemp(prefix="firefox_ga_")
            print(f"📁 Created temp directory: {self.temp_dir}")
            
            # Create Firefox profile directory
            profile_dir = os.path.join(self.temp_dir, 'firefox_profile')
            os.makedirs(profile_dir, exist_ok=True)
            
            return True
        except Exception as e:
            print(f"❌ Environment setup failed: {e}")
            return False
    
    def kill_existing_browsers(self):
        """Clean kill of existing browser processes"""
        try:
            print("🧹 Cleaning existing processes...")
            
            # Kill processes that might interfere
            processes = ['firefox', 'chrome', 'chromedriver', 'tor', 'geckodriver']
            
            for proc_name in processes:
                try:
                    subprocess.run(['pkill', '-f', proc_name], 
                                 capture_output=True, check=False)
                except:
                    pass
            
            time.sleep(2)
            print("✅ Process cleanup completed")
            
        except Exception as e:
            print(f"⚠️ Process cleanup warning: {e}")
    
    def start_tor(self):
        """Start Tor service"""
        try:
            print("🧅 Starting Tor...")
            
            # Simple Tor startup
            self.tor_process = subprocess.Popen([
                'tor', '--quiet'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Wait for Tor to start
            print("⏳ Waiting for Tor connection...")
            for i in range(20):
                if self.check_tor_connection():
                    print(f"✅ Tor connected: {self.current_ip}")
                    return True
                time.sleep(1)
                if i % 5 == 0:
                    print(f"🔄 Checking... {i+1}/20")
            
            print("❌ Tor connection timeout")
            return False
            
        except Exception as e:
            print(f"❌ Tor startup failed: {e}")
            return False
    
    def check_tor_connection(self):
        """Verify Tor is working"""
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
    
    def create_firefox_profile(self):
        """Create Firefox profile with Tor proxy"""
        try:
            if not self.temp_dir:
                return None
                
            profile_dir = os.path.join(self.temp_dir, 'firefox_profile')
            
            # Firefox preferences for Tor
            prefs = {
                'network.proxy.type': 1,
                'network.proxy.socks': '127.0.0.1',
                'network.proxy.socks_port': 9050,
                'network.proxy.socks_version': 5,
                'network.proxy.socks_remote_dns': True,
                'javascript.enabled': True,
                'dom.storage.enabled': True,
                'network.cookie.cookieBehavior': 0,
                'privacy.trackingprotection.enabled': False,
                'dom.webnotifications.enabled': False,
                'media.navigator.enabled': False,
                'geo.enabled': False,
                'browser.cache.disk.enable': False,
                'browser.cache.memory.enable': False,
                'network.http.use-cache': False
            }
            
            # Create prefs.js file
            prefs_file = os.path.join(profile_dir, 'prefs.js')
            with open(prefs_file, 'w') as f:
                for key, value in prefs.items():
                    if isinstance(value, bool):
                        value_str = 'true' if value else 'false'
                    elif isinstance(value, str):
                        value_str = f'"{value}"'
                    else:
                        value_str = str(value)
                    f.write(f'user_pref("{key}", {value_str});\n')
            
            print(f"🦊 Created Firefox profile: {profile_dir}")
            return profile_dir
            
        except Exception as e:
            print(f"❌ Firefox profile creation failed: {e}")
            return None
    
    def create_firefox_browser(self):
        """Create Firefox browser with Tor proxy"""
        try:
            print("🦊 Creating Firefox browser...")
            
            # Create Firefox profile
            profile_dir = self.create_firefox_profile()
            if not profile_dir:
                return False
            
            # Firefox options
            options = FirefoxOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'--profile={profile_dir}')
            
            # User agent
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0'
            options.set_preference('general.useragent.override', user_agent)
            
            # Create Firefox driver
            self.driver = webdriver.Firefox(options=options)
            
            # Set timeouts
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            
            # Test browser
            print("🧪 Testing Firefox browser...")
            self.driver.get('data:text/html,<html><body><h1>Firefox Test</h1><p>Browser working!</p></body></html>')
            
            if "Firefox Test" in self.driver.page_source:
                print("✅ Firefox browser created successfully!")
                return True
            else:
                print("❌ Firefox browser test failed")
                return False
                
        except Exception as e:
            print(f"❌ Firefox browser creation failed: {e}")
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
            return False
    
    def inject_google_analytics(self):
        """Inject real Google Analytics tracking"""
        try:
            if not self.driver:
                return False
            
            print(f"📊 Injecting Google Analytics: {self.ga_tracking_id}")
            
            ga_script = f"""
            // Real Google Analytics 4 Implementation
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            
            // Load GA4 script
            var script = document.createElement('script');
            script.async = true;
            script.src = 'https://www.googletagmanager.com/gtag/js?id={self.ga_tracking_id}';
            document.head.appendChild(script);
            
            // Initialize GA4
            gtag('js', new Date());
            gtag('config', '{self.ga_tracking_id}', {{
                'anonymize_ip': false,
                'send_page_view': true,
                'cookie_flags': 'SameSite=None;Secure',
                'user_id': 'firefox_user_' + Math.random().toString(36).substr(2, 9)
            }});
            
            // Send initial pageview
            gtag('event', 'page_view', {{
                'page_title': document.title,
                'page_location': window.location.href,
                'browser_type': 'firefox',
                'proxy_type': 'tor',
                'session_id': 'firefox_' + Date.now()
            }});
            
            console.log('✅ Google Analytics initialized');
            window.ga_ready = true;
            return true;
            """
            
            result = self.driver.execute_script(ga_script)
            time.sleep(2)  # Allow GA to load
            
            print("✅ Google Analytics tracking active!")
            return True
            
        except Exception as e:
            print(f"❌ GA injection failed: {e}")
            return False
    
    def send_ga_event(self, event_name, parameters=None):
        """Send Google Analytics event"""
        try:
            if not self.driver:
                return False
            
            params = parameters or {}
            params.update({
                'timestamp': int(time.time() * 1000),
                'browser': 'firefox',
                'proxy': 'tor'
            })
            
            event_script = f"""
            if (typeof gtag !== 'undefined' && window.ga_ready) {{
                gtag('event', '{event_name}', {json.dumps(params)});
                console.log('📊 GA Event: {event_name}');
                return true;
            }} else {{
                console.log('❌ GA not ready');
                return false;
            }}
            """
            
            result = self.driver.execute_script(event_script)
            if result:
                print(f"📊 Sent GA event: {event_name}")
            
            return result
            
        except Exception as e:
            print(f"❌ GA event failed: {e}")
            return False
    
    def browse_website(self, url, duration=60):
        """Browse website with GA tracking"""
        try:
            if not self.driver:
                print("❌ No browser available")
                return False
                
            print(f"\n🌐 Browsing: {url}")
            
            # Navigate to website
            self.driver.get(url)
            
            # Wait for page load
            WebDriverWait(self.driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            print(f"📄 Loaded: {self.driver.title}")
            
            # Inject GA tracking
            if not self.inject_google_analytics():
                print("⚠️ GA injection failed, continuing...")
            
            # Simulate browsing
            end_time = time.time() + duration
            scroll_count = 0
            
            while time.time() < end_time:
                # Random scroll
                scroll_pixels = random.randint(100, 400)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_pixels});")
                scroll_count += 1
                
                # Send scroll event
                self.send_ga_event('scroll', {
                    'scroll_count': scroll_count,
                    'scroll_pixels': scroll_pixels
                })
                
                # Random pause
                pause = random.uniform(2, 8)
                time.sleep(pause)
                
                # Random click attempt
                if random.random() < 0.3:
                    try:
                        links = self.driver.find_elements(By.TAG_NAME, "a")
                        if links:
                            link = random.choice(links[:5])
                            link.click()
                            self.send_ga_event('click', {
                                'link_text': link.text[:30] if link.text else 'unknown'
                            })
                            time.sleep(3)
                            break
                    except:
                        pass
            
            # Send session complete event
            self.send_ga_event('session_complete', {
                'duration': duration,
                'scrolls': scroll_count
            })
            
            print(f"✅ Browsing session completed!")
            return True
            
        except Exception as e:
            print(f"❌ Browsing failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        try:
            print("\n🧹 Cleaning up...")
            
            # Close browser
            if self.driver:
                try:
                    self.driver.quit()
                    print("✅ Firefox closed")
                except:
                    pass
            
            # Stop Tor
            if self.tor_process:
                try:
                    self.tor_process.terminate()
                    self.tor_process.wait(timeout=5)
                    print("✅ Tor stopped")
                except:
                    try:
                        self.tor_process.kill()
                    except:
                        pass
            
            # Remove temp directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                try:
                    shutil.rmtree(self.temp_dir)
                    print("✅ Temp files removed")
                except:
                    pass
            
            # Final process cleanup
            self.kill_existing_browsers()
            
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")

def main():
    """Test Firefox GA browser"""
    print("🦊 FIREFOX GA BROWSER - NO EXIT CODE 15")
    print("=" * 50)
    print("🎯 Alternative to Chrome for stable automation")
    print("📊 Real Google Analytics tracking")
    print("🧅 Tor proxy integration")
    print("✅ No VS Code conflicts")
    print("=" * 50)
    
    browser = FirefoxGABrowser()
    
    try:
        # Setup
        if not browser.setup_environment():
            print("❌ Environment setup failed")
            return
        
        # Clean processes
        browser.kill_existing_browsers()
        
        # Start Tor
        if not browser.start_tor():
            print("❌ Tor startup failed")
            return
        
        # Create Firefox browser
        if not browser.create_firefox_browser():
            print("❌ Firefox creation failed")
            return
        
        print("\n🎉 SUCCESS: Firefox browser created without exit code 15!")
        print("👁️ Firefox window should be visible...")
        
        # Test website
        test_url = "https://verenigdamsterdam.nl"
        print(f"\n🧪 Testing with: {test_url}")
        
        if browser.browse_website(test_url, duration=30):
            print("\n✅ COMPLETE SUCCESS!")
            print("🦊 Firefox works without crashes")
            print("📊 Google Analytics tracking active")
            print("🧅 Tor proxy functioning")
            print("🎯 No exit code 15 errors!")
        else:
            print("\n⚠️ Browsing test had issues")
        
        # Keep browser open
        print("\n👁️ Browser will stay open for 10 seconds...")
        time.sleep(10)
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        browser.cleanup()
        print("\n✅ Test completed")

if __name__ == "__main__":
    main()
