#!/usr/bin/env python3
"""
🎭 MODULAR GA TOR BROWSER
========================
Combined manager using separate Tor and Browser modules.
This approach isolates issues and allows independent testing.
"""

# AUTO-INITIALIZE LOGGING ON IMPORT
from auto_logger_init import auto_initialize
auto_initialize()

import time
import random
from datetime import datetime
from typing import Optional

from tor_manager import TorManager
from browser_manager import BrowserManager

class ModularGATorBrowser:
    """Modular browser with separate Tor and Browser components"""
    
    def __init__(self, ga_tracking_id: str = "G-0B4ZR31YFS"):
        self.tor_manager = TorManager()
        self.browser_manager = BrowserManager(ga_tracking_id)
        self.session_start = None
        
    def start_with_tor(self) -> bool:
        """Start with Tor proxy"""
        try:
            print("🎭 STARTING MODULAR GA TOR BROWSER")
            print("=" * 50)
            
            # Step 1: Start Tor independently
            print("\n1️⃣ STARTING TOR MODULE...")
            if not self.tor_manager.start_tor():
                print("❌ Tor module failed")
                return False
            
            print("✅ Tor module ready!")
            
            # Step 2: Get proxy settings
            proxy_url = self.tor_manager.get_proxy_settings()
            if not proxy_url:
                print("❌ Tor proxy not available")
                return False
            
            print(f"🔗 Proxy ready: {proxy_url}")
            
            # Step 3: Create browser with Tor proxy
            print("\n2️⃣ STARTING BROWSER MODULE...")
            browser = self.browser_manager.create_browser(proxy_url)
            if not browser:
                print("❌ Browser module failed")
                return False
            
            print("✅ Browser module ready!")
            
            # Step 4: Test IP
            print("\n3️⃣ TESTING TOR CONNECTION...")
            current_ip = self.tor_manager.get_current_ip()
            if current_ip:
                print(f"🌍 Current IP: {current_ip}")
            else:
                print("⚠️ Could not verify IP")
            
            print("\n🎉 MODULAR SETUP COMPLETE!")
            return True
            
        except Exception as e:
            print(f"❌ Modular startup failed: {e}")
            return False
    
    def start_without_tor(self) -> bool:
        """Start without Tor proxy (direct connection)"""
        try:
            print("🌐 STARTING BROWSER WITHOUT TOR")
            print("=" * 40)
            
            # Create browser without proxy
            browser = self.browser_manager.create_browser()
            if browser:
                print("✅ Direct browser connection ready!")
                return True
            else:
                print("❌ Browser creation failed")
                return False
                
        except Exception as e:
            print(f"❌ Direct browser startup failed: {e}")
            return False
    
    def browse_website_with_ga(self, url: str, duration: int = 60) -> bool:
        """Browse website with GA tracking"""
        try:
            print(f"\n🎯 BROWSING SESSION: {url}")
            print("=" * 50)
            self.session_start = datetime.now()
            
            # Navigate to website
            if not self.browser_manager.navigate_to_website(url):
                print("❌ Website navigation failed")
                return False
            
            print("📊 GA tracking active - check real-time dashboard!")
            
            # Simulate human activity
            print(f"\n👤 SIMULATING HUMAN ACTIVITY ({duration}s)...")
            self.browser_manager.simulate_human_activity(duration)
            
            # Send session completion event
            session_duration = (datetime.now() - self.session_start).total_seconds()
            self.browser_manager.send_ga_event('session_complete', {
                'session_duration': int(session_duration),
                'pages_viewed': 1,
                'bounce': 0
            })
            
            print(f"✅ Session completed! Duration: {session_duration:.1f}s")
            return True
            
        except Exception as e:
            print(f"❌ Browsing session failed: {e}")
            return False
    
    def rotate_tor_identity(self) -> bool:
        """Rotate Tor identity if using Tor"""
        if self.tor_manager.is_running:
            return self.tor_manager.rotate_identity()
        else:
            print("ℹ️ Not using Tor, no identity to rotate")
            return True
    
    def get_status(self) -> dict:
        """Get status of all components"""
        return {
            'tor': self.tor_manager.get_status(),
            'browser': {
                'active': self.browser_manager.browser is not None,
                'ga_tracking_id': self.browser_manager.ga_tracking_id
            },
            'session_start': self.session_start.isoformat() if self.session_start else None
        }
    
    def cleanup(self):
        """Clean up all components"""
        print("\n🧹 CLEANING UP ALL MODULES...")
        self.browser_manager.cleanup()
        self.tor_manager.stop_tor()
        print("✅ All modules cleaned up!")

def test_modular_approach():
    """Test the modular approach"""
    print("=" * 60)
    print("🧪 MODULAR APPROACH TEST")
    print("=" * 60)
    
    browser = ModularGATorBrowser()
    
    try:
        # Test 1: Without Tor
        print("\n🧪 TEST 1: BROWSER WITHOUT TOR")
        print("-" * 40)
        if browser.start_without_tor():
            browser.browse_website_with_ga("https://verenigdamsterdam.nl", 15)
            print("✅ Test 1 PASSED: Browser works without Tor")
        else:
            print("❌ Test 1 FAILED: Browser issues")
            return
        
        # Clean up before next test
        browser.cleanup()
        time.sleep(5)
        
        # Test 2: With Tor
        print("\n🧪 TEST 2: BROWSER WITH TOR")
        print("-" * 40)
        if browser.start_with_tor():
            browser.browse_website_with_ga("https://verenigdamsterdam.nl", 15)
            print("✅ Test 2 PASSED: Browser works with Tor")
        else:
            print("❌ Test 2 FAILED: Tor integration issues")
        
        # Show status
        print("\n📊 FINAL STATUS:")
        status = browser.get_status()
        print(f"Tor running: {status['tor']['running']}")
        print(f"Browser active: {status['browser']['active']}")
        
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
    finally:
        browser.cleanup()

def main():
    """Main execution with modular approach"""
    print("=" * 60)
    print("🎭 MODULAR GA TOR BROWSER")
    print("=" * 60)
    print("🎯 Target: https://verenigdamsterdam.nl")
    print("📊 GA Tracking ID: G-0B4ZR31YFS")
    print("🧅 Modular Tor + Browser architecture")
    print("=" * 60)
    
    browser = ModularGATorBrowser()
    
    try:
        # Ask user for mode
        print("\nSelect mode:")
        print("1. With Tor (may have exit code 15 issue)")
        print("2. Without Tor (direct connection)")
        print("3. Test both (comparison)")
        
        mode = input("Enter choice (1/2/3): ").strip()
        
        if mode == "1":
            if browser.start_with_tor():
                browser.browse_website_with_ga("https://verenigdamsterdam.nl", 60)
            
        elif mode == "2":
            if browser.start_without_tor():
                browser.browse_website_with_ga("https://verenigdamsterdam.nl", 60)
        
        elif mode == "3":
            test_modular_approach()
        
        else:
            print("Invalid choice, running without Tor...")
            if browser.start_without_tor():
                browser.browse_website_with_ga("https://verenigdamsterdam.nl", 60)
        
        input("\n👀 Press Enter to close...")
        
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        browser.cleanup()

if __name__ == "__main__":
    main()
