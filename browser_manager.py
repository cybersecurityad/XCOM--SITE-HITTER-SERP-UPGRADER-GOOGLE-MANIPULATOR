#!/usr/bin/env python3
"""
🌐 BROWSER MANAGER MODULE
========================
Separate browser management module that can work with or without Tor.
This isolates browser creation from Tor integration for better debugging.
"""

# AUTO-INITIALIZE LOGGING ON IMPORT
from auto_logger_init import auto_initialize
auto_initialize()

import time
import subprocess
import signal
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from typing import Optional

class BrowserManager:
    """Independent browser management - works with or without Tor"""
    
    def __init__(self, ga_tracking_id: str = "G-0B4ZR31YFS"):
        self.browser = None
        self.ga_tracking_id = ga_tracking_id
        self.running = True
        
        # Handle signals gracefully
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n🔄 Signal {signum} received. Gracefully shutting down...")
        self.running = False
        self.cleanup()
        sys.exit(0)
    
    def create_browser(self, proxy_url: Optional[str] = None) -> Optional[webdriver.Chrome]:
        """Create browser with optional proxy configuration"""
        try:
            print("🌐 Creating browser...")
            if proxy_url:
                print(f"🔗 Using proxy: {proxy_url}")
            else:
                print("🔗 Direct connection (no proxy)")
            
            # Kill any existing Chrome processes first
            subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True, check=False)
            time.sleep(2)
            
            options = Options()
            
            # Proxy configuration (if provided)
            if proxy_url:
                options.add_argument(f'--proxy-server={proxy_url}')
            
            # Stable Chrome options - prevent exit code 15
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            
            # Enable JavaScript and cookies for GA
            options.add_argument('--enable-javascript')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--disable-web-security')
            
            # User agent
            options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
            
            # Create service with proper timeout handling
            service = Service()
            
            # Create browser
            browser = webdriver.Chrome(service=service, options=options)
            browser.set_page_load_timeout(15)
            browser.implicitly_wait(5)
            
            self.browser = browser
            print("✅ Browser created successfully!")
            return browser
            
        except Exception as e:
            print(f"❌ Failed to create browser: {e}")
            return None
    
    def inject_ga_tracking(self) -> bool:
        """Inject Google Analytics tracking"""
        try:
            if not self.browser:
                print("❌ No browser available for GA injection")
                return False
            
            print(f"📊 Injecting GA tracking (ID: {self.ga_tracking_id})...")
            
            ga_script = f"""
            // Google Analytics 4 (GA4) - Real tracking
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{self.ga_tracking_id}', {{
                'send_page_view': true,
                'anonymize_ip': false,
                'cookie_flags': 'SameSite=None;Secure'
            }});
            
            // Load GA4 script
            var script = document.createElement('script');
            script.async = true;
            script.src = 'https://www.googletagmanager.com/gtag/js?id={self.ga_tracking_id}';
            document.head.appendChild(script);
            
            console.log('GA4 tracking initialized with ID: {self.ga_tracking_id}');
            """
            
            self.browser.execute_script(ga_script)
            time.sleep(2)
            print("✅ GA tracking injected successfully!")
            return True
            
        except Exception as e:
            print(f"❌ GA injection failed: {e}")
            return False
    
    def send_ga_event(self, event_name: str, parameters: Optional[dict] = None) -> bool:
        """Send Google Analytics event"""
        try:
            if not self.browser:
                return False
            
            if parameters is None:
                parameters = {}
            
            # Convert parameters to JavaScript object
            params_js = str(parameters).replace("'", '"')
            
            event_script = f"""
            if (typeof gtag !== 'undefined') {{
                gtag('event', '{event_name}', {params_js});
                console.log('GA event sent: {event_name}', {params_js});
            }} else {{
                console.warn('GA not loaded yet, event queued: {event_name}');
            }}
            """
            
            self.browser.execute_script(event_script)
            print(f"📊 Sent GA event: {event_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send GA event {event_name}: {e}")
            return False
    
    def navigate_to_website(self, url: str) -> bool:
        """Navigate to website and inject GA"""
        try:
            if not self.browser:
                print("❌ No browser available")
                return False
            
            print(f"🌐 Navigating to: {url}")
            self.browser.get(url)
            time.sleep(3)
            
            print(f"✅ Website loaded: {self.browser.title[:50]}...")
            
            # Inject GA tracking
            if self.inject_ga_tracking():
                # Send initial pageview
                self.send_ga_event('page_view', {
                    'page_title': self.browser.title,
                    'page_location': url,
                    'session_engaged': 1
                })
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Navigation failed: {e}")
            return False
    
    def simulate_human_activity(self, duration: int = 30):
        """Simulate human activity on the page"""
        try:
            if not self.browser:
                return
            
            print(f"👤 Simulating human activity for {duration} seconds...")
            
            end_time = time.time() + duration
            while time.time() < end_time and self.running:
                # Scroll randomly
                scroll_y = f"window.scrollTo(0, {200 + (time.time() % 100) * 10});"
                self.browser.execute_script(scroll_y)
                
                # Send scroll event to GA
                self.send_ga_event('scroll', {
                    'scroll_depth': f"{int((time.time() % 100))}%"
                })
                
                time.sleep(2)
                
                # Send engagement event occasionally
                if int(time.time()) % 10 == 0:
                    self.send_ga_event('user_engagement', {
                        'engagement_time_msec': 10000
                    })
                
                remaining = int(end_time - time.time())
                if remaining % 5 == 0 and remaining > 0:
                    print(f"⏳ {remaining} seconds remaining...")
            
            print("✅ Human activity simulation completed!")
            
        except Exception as e:
            print(f"❌ Activity simulation error: {e}")
    
    def cleanup(self):
        """Clean up browser resources"""
        try:
            print("\n🧹 Cleaning up browser...")
            
            if self.browser:
                try:
                    self.browser.quit()
                    print("✅ Browser closed")
                except Exception as e:
                    print(f"⚠️ Browser close warning: {e}")
            
            # Kill any remaining Chrome processes
            subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True, check=False)
            subprocess.run(['pkill', '-f', 'chromedriver'], capture_output=True, check=False)
            
        except Exception as e:
            print(f"⚠️ Browser cleanup error: {e}")

def test_browser_module():
    """Test browser module without Tor"""
    print("=" * 60)
    print("🧪 BROWSER MODULE TEST (NO TOR)")
    print("=" * 60)
    
    browser_manager = BrowserManager()
    
    try:
        # Test browser creation without proxy
        print("\n1️⃣ Testing browser creation (no proxy)...")
        browser = browser_manager.create_browser()
        if browser:
            print("✅ Browser creation: PASSED")
            
            # Test website navigation
            print("\n2️⃣ Testing website navigation...")
            if browser_manager.navigate_to_website("https://verenigdamsterdam.nl"):
                print("✅ Website navigation: PASSED")
                
                # Test human activity simulation
                print("\n3️⃣ Testing human activity simulation...")
                browser_manager.simulate_human_activity(15)
                print("✅ Activity simulation: PASSED")
            else:
                print("❌ Website navigation: FAILED")
        else:
            print("❌ Browser creation: FAILED")
        
        print("\n🎉 BROWSER MODULE TEST COMPLETED!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
    finally:
        browser_manager.cleanup()

if __name__ == "__main__":
    test_browser_module()
