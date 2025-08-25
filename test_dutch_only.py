#!/usr/bin/env python3
"""
Test Dutch-only exit nodes feature
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_advanced_tor_browser import SimpleAdvancedTorBrowser, SimpleTorConfig

def test_dutch_exit_nodes():
    """Test Dutch-only exit nodes configuration"""
    print("🇳🇱 Testing Dutch-only exit nodes...")
    
    # Configure for Dutch-only exit nodes
    config = SimpleTorConfig(
        use_dutch_exit_nodes_only=True,
        save_screenshots=True,
        min_delay=2.0,
        max_delay=4.0
    )
    
    browser = SimpleAdvancedTorBrowser(config)
    
    try:
        print("🔄 Setting up browser with Dutch-only exit nodes...")
        if browser.setup():
            print("✅ Browser setup successful!")
            
            # Test IP geolocation
            print("\n🌐 Testing IP geolocation...")
            browser.comprehensive_page_visit("https://whatismyipaddress.com/")
            
            print("\n🇳🇱 Testing Dutch website...")
            browser.comprehensive_page_visit("https://www.nu.nl/")
            
            print("\n✅ Dutch-only exit nodes test completed!")
        else:
            print("❌ Browser setup failed!")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
    finally:
        print("🧹 Cleaning up...")
        browser.cleanup()

if __name__ == "__main__":
    test_dutch_exit_nodes()
