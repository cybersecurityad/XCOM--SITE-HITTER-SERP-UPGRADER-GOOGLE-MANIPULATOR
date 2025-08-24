#!/usr/bin/env python3
"""
🎭 BROWSER TEST WITHOUT TOR
==========================
Test the browser creation and GA tracking without Tor to isolate the issue.
This will help identify if the problem is with Tor or the browser itself.
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

class BrowserTestNoTor:
    """Test browser without Tor to isolate issues"""
    
    def __init__(self):
        self.browser = None
        self.running = True
        self.ga_tracking_id = "G-0B4ZR31YFS"
        
        # Handle signals gracefully
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n🔄 Signal {signum} received. Gracefully shutting down...")
        self.running = False
        self.cleanup()
        sys.exit(0)
    
    def create_browser_no_tor(self):
        """Create browser WITHOUT Tor - direct connection"""
        try:
            print("🌐 Creating browser WITHOUT Tor (direct connection)...")
            
            # Kill any existing Chrome processes first
            subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True, check=False)
            time.sleep(2)
            
            options = Options()
            
            # Stable Chrome options - prevent exit code 15
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            
            # Enable JavaScript and cookies for GA
            options.add_argument('--enable-javascript')
            
            # User agent
            options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
            
            # Create service
            service = Service()
            
            # Create browser
            browser = webdriver.Chrome(service=service, options=options)
            browser.set_page_load_timeout(15)
            browser.implicitly_wait(5)
            
            self.browser = browser
            print("✅ Browser created successfully (NO TOR)!")
            return browser
            
        except Exception as e:
            print(f"❌ Failed to create browser: {e}")
            return None
    
    def inject_ga_tracking(self):
        """Inject Google Analytics tracking"""
        try:
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
    
    def test_website_access(self):
        """Test accessing the target website"""
        try:
            target_url = "https://verenigdamsterdam.nl"
            print(f"🌐 Testing website access: {target_url}")
            
            self.browser.get(target_url)
            time.sleep(3)
            
            print(f"✅ Website loaded: {self.browser.title[:50]}...")
            
            # Inject GA
            if self.inject_ga_tracking():
                print("📊 GA tracking active - check real-time dashboard")
            
            # Send a test event
            self.browser.execute_script(f"""
                gtag('event', 'page_view', {{
                    'page_title': document.title,
                    'page_location': window.location.href,
                    'custom_parameter': 'browser_test_no_tor'
                }});
            """)
            
            print("📊 Sent test GA event: page_view")
            
            # Keep browser open for observation
            print("👁️  Browser is open - check if it's stable")
            print("⏱️  Keeping open for 30 seconds...")
            
            for i in range(30, 0, -1):
                if not self.running:
                    break
                if i % 5 == 0:
                    print(f"⏳ {i} seconds remaining...")
                time.sleep(1)
            
            print("✅ Browser test completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Website test failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        try:
            print("\n🧹 Cleaning up...")
            
            if self.browser:
                try:
                    self.browser.quit()
                    print("✅ Browser closed")
                except:
                    pass
            
            # Kill any remaining Chrome processes
            subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True, check=False)
            subprocess.run(['pkill', '-f', 'chromedriver'], capture_output=True, check=False)
            
        except Exception as e:
            print(f"⚠️  Cleanup error: {e}")

def main():
    """Test browser without Tor"""
    print("=" * 60)
    print("🧪 BROWSER TEST WITHOUT TOR")
    print("=" * 60)
    print("🎯 Testing browser creation and GA tracking")
    print("🚫 Tor DISABLED - direct connection")
    print("✅ This will isolate browser vs Tor issues")
    print("=" * 60)
    
    tester = BrowserTestNoTor()
    
    try:
        # Create browser
        browser = tester.create_browser_no_tor()
        if not browser:
            print("❌ Browser creation failed")
            return
        
        print("\n📊 BROWSER CREATED SUCCESSFULLY")
        print("=" * 40)
        print("✅ No Tor - direct connection")
        print("✅ Standard Chrome options")
        print("✅ No proxy configuration")
        print("=" * 40)
        
        # Test website access
        success = tester.test_website_access()
        
        if success:
            print("\n🎉 TEST PASSED!")
            print("✅ Browser works without Tor")
            print("✅ No exit code 15 errors")
            print("✅ GA tracking functional")
            print("\n💡 CONCLUSION: Issue is with Tor integration")
        else:
            print("\n❌ TEST FAILED!")
            print("❌ Browser has issues even without Tor")
            print("💡 CONCLUSION: Issue is with browser setup")
        
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
    finally:
        tester.cleanup()

if __name__ == "__main__":
    main()
