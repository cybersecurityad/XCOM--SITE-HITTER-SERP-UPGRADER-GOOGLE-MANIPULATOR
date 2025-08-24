#!/usr/bin/env python3
"""
Quick Tor Browser Launcher - Simple one-command execution
======================================================

Launch Tor browser for quick testing without interactive prompts.
"""

import sys
from main_tor_browser import MainTorBrowser, TorBrowserConfig


def quick_test():
    """Quick connectivity test"""
    print("🚀 QUICK TOR BROWSER TEST")
    print("=" * 40)
    
    config = TorBrowserConfig(auto_start_tor=True)
    browser = MainTorBrowser(config)
    
    try:
        # Setup and test
        if browser.setup():
            print("✅ Setup successful!")
            
            # Quick test
            test_urls = [
                "https://httpbin.org/ip",
                "https://check.torproject.org"
            ]
            
            for url in test_urls:
                if browser.navigate(url):
                    info = browser.get_page_info()
                    print(f"✅ {url} - {info.get('page_source_length', 0)} chars")
                else:
                    print(f"❌ Failed: {url}")
            
            print("🎉 Quick test completed!")
            return True
        else:
            print("❌ Setup failed!")
            return False
            
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        browser.cleanup()


if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)
