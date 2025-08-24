#!/usr/bin/env python3
"""
Simple test script for the cybersecurity web automation tool
"""

import time
import random
from human_browser import HumanBehaviorSimulator, BrowsingConfig


def simple_test():
    """Simple test of the automation tool"""
    print("🚀 Starting Cybersecurity Web Automation Tool Test")
    print("=" * 50)
    
    # Create a simple configuration
    config = BrowsingConfig(
        min_scroll_delay=1.0,
        max_scroll_delay=2.0,
        min_click_delay=1.0,
        max_click_delay=2.0,
        use_proxy=False
    )
    
    # Initialize the simulator
    simulator = HumanBehaviorSimulator(config)
    
    try:
        # Test with a safe public site
        test_url = "https://httpbin.org/get"
        print(f"🌐 Testing with: {test_url}")
        
        # Simple actions without risky clicking
        safe_actions = ['read', 'scroll', 'scroll', 'read']
        
        print("🤖 Simulating human browsing behavior...")
        simulator.browse_page(test_url, safe_actions)
        
        print("✅ Test completed successfully!")
        print("🔍 Check the browser window to see the human-like behavior")
        
        # Keep browser open for a moment to observe
        time.sleep(5)
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
    finally:
        print("🔒 Closing browser...")
        simulator.close()
        print("✨ Test session completed")


if __name__ == "__main__":
    simple_test()
