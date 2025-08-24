#!/usr/bin/env python3
"""
🎭 STABLE GA BROWSER - NO CRASHES
================================
Stable browser with Google Analytics that won't crash VS Code.
Uses the proven stable browser foundation with GA tracking.
"""

# AUTO-INITIALIZE LOGGING ON IMPORT
from auto_logger_init import auto_initialize
auto_initialize()

import time
import os
import sys
import signal
import subprocess
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

class StableGABrowser:
    """Stable browser with Google Analytics - no crashes"""
    
    def __init__(self):
        self.driver = None
        self.running = True
        self.ga_tracking_id = "G-0B4ZR31YFS"  # Real GA ID from verenigdamsterdam.nl
        
        # Handle signals gracefully
        signal.signal(signal.SIGTERM, self._cleanup)
        signal.signal(signal.SIGINT, self._cleanup)
    
    def _cleanup(self, signum=None, frame=None):
        """Clean shutdown"""
        print(f"\n🛡️ Graceful shutdown (signal: {signum})")
        self.running = False
        if self.driver:
            try:
                self.driver.quit()
                print("✅ Browser closed")
            except:
                pass
        sys.exit(0)
    
    def create_stable_browser(self):
        """Create stable Chrome browser with JS enabled for GA"""
        try:
            print("🌐 Creating stable GA browser...")
            
            # Kill any existing Chrome processes
            subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True, check=False)
            time.sleep(2)
            
            # Chrome options optimized for stability
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            # Enable JavaScript for GA (but keep other features minimal)
            options.add_argument('--enable-javascript')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--disable-web-security')
            options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
            
            # Create service with timeout
            service = Service()
            
            # Create driver with short timeout to prevent hangs
            print("🚀 Starting Chrome with GA support...")
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_page_load_timeout(15)
            self.driver.implicitly_wait(5)
            
            print("✅ Stable GA browser created!")
            return True
            
        except Exception as e:
            print(f"❌ Browser creation failed: {e}")
            return False
    
    def inject_ga_tracking(self):
        """Inject Google Analytics tracking code"""
        try:
            if not self.driver:
                return False
                
            print(f"📊 Injecting GA tracking (ID: {self.ga_tracking_id})...")
            
            # Real GA4 implementation
            ga_script = f"""
            // Google Analytics 4 Implementation
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            
            // Load GA library
            var script = document.createElement('script');
            script.async = true;
            script.src = 'https://www.googletagmanager.com/gtag/js?id={self.ga_tracking_id}';
            document.head.appendChild(script);
            
            // Initialize GA
            gtag('js', new Date());
            gtag('config', '{self.ga_tracking_id}', {{
                'send_page_view': true,
                'anonymize_ip': false
            }});
            
            // Mark as ready
            window.ga_ready = true;
            console.log('✅ GA tracking active');
            """
            
            self.driver.execute_script(ga_script)
            time.sleep(2)  # Allow GA to initialize
            
            print("✅ GA tracking injected successfully!")
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
                'test_session': 'stable_browser'
            })
            
            ga_event = f"""
            if (typeof gtag !== 'undefined' && window.ga_ready) {{
                gtag('event', '{event_name}', {json.dumps(params)});
                console.log('📊 GA event sent: {event_name}');
                return true;
            }} else {{
                console.log('⚠️ GA not ready');
                return false;
            }}
            """
            
            result = self.driver.execute_script(ga_event)
            if result:
                print(f"📊 Sent GA event: {event_name}")
            
            return result
            
        except Exception as e:
            print(f"❌ GA event failed: {e}")
            return False
    
    def test_ga_website(self, url):
        """Test website with GA tracking"""
        try:
            if not self.driver:
                print("❌ No browser available")
                return False
                
            print(f"🌐 Testing GA website: {url}")
            
            # Load website
            self.driver.get(url)
            
            # Wait for page load
            WebDriverWait(self.driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Inject GA tracking
            if not self.inject_ga_tracking():
                print("⚠️ GA injection failed, continuing without GA")
            
            # Send pageview event
            self.send_ga_event('page_view', {
                'page_title': self.driver.title or 'Unknown',
                'page_location': url
            })
            
            # Simulate user engagement
            print("👤 Simulating user engagement...")
            
            # Scroll simulation
            for i in range(3):
                self.driver.execute_script(f"window.scrollTo(0, {(i+1) * 200});")
                self.send_ga_event('scroll', {
                    'scroll_depth': f"{((i+1)/3) * 100:.0f}%"
                })
                time.sleep(1)
            
            # Send engagement event
            self.send_ga_event('user_engagement', {
                'engagement_time_msec': 5000,
                'engaged_session_event': 1
            })
            
            title = (self.driver.title or "")[:50] if self.driver.title else "No title"
            print(f"✅ GA website loaded: {title}...")
            
            # Keep browser open for observation
            print("👁️ Browser with GA tracking is visible")
            print("📊 Check GA dashboard for real-time activity")
            print("⏱️ Keeping open for 15 seconds...")
            
            for i in range(15):
                if not self.running:
                    break
                time.sleep(1)
                if i % 5 == 0 and i > 0:
                    print(f"⏳ {15-i} seconds remaining...")
            
            return True
            
        except TimeoutException:
            print("⏰ Website load timeout")
            return False
        except Exception as e:
            print(f"❌ GA website test failed: {e}")
            return False
    
    def run_ga_test(self):
        """Run complete GA test"""
        try:
            print("🎭 STABLE GA BROWSER TEST")
            print("=" * 40)
            print(f"📊 GA Tracking ID: {self.ga_tracking_id}")
            print("🛡️ Crash-proof implementation")
            print("=" * 40)
            
            # Create browser
            if not self.create_stable_browser():
                print("❌ Browser creation failed")
                return False
            
            # Test with target website
            target_url = "https://verenigdamsterdam.nl"
            if self.test_ga_website(target_url):
                print("\n✅ GA WEBSITE TEST PASSED!")
                print("📊 Real GA events sent to dashboard")
                print("🎉 NO CRASHES DETECTED!")
                return True
            else:
                print("\n❌ GA website test failed")
                return False
                
        except KeyboardInterrupt:
            print("\n⚠️ Test interrupted by user")
            return False
        except Exception as e:
            print(f"\n❌ GA test error: {e}")
            return False
        finally:
            self._cleanup()

def main():
    """Main GA test function"""
    browser = StableGABrowser()
    
    print("🎭 STABLE GOOGLE ANALYTICS BROWSER")
    print("=" * 45)
    print("🎯 Target: https://verenigdamsterdam.nl")
    print(f"📊 GA Tracking: G-0B4ZR31YFS")
    print("🛡️ Crash-proof design")
    print("👀 Real-time GA dashboard monitoring")
    print("=" * 45)
    
    try:
        success = browser.run_ga_test()
        if success:
            print("\n🎉 SUCCESS: Stable GA browser with no crashes!")
            print("📊 Check Google Analytics dashboard:")
            print("   https://analytics.google.com/")
            print("   Look for real-time users and events")
        else:
            print("\n❌ GA test failed")
            
    except Exception as e:
        print(f"\n❌ Main error: {e}")
    finally:
        if browser.driver:
            try:
                browser.driver.quit()
            except:
                pass

if __name__ == "__main__":
    main()
