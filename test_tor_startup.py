#!/usr/bin/env python3
"""
Quick test for the improved Tor startup
"""
import sys
sys.path.append('.')
from visual_tor_browser import TorVisualController

def test_tor_startup():
    """Test the improved Tor startup with feedback"""
    print("🧪 Testing Tor Startup Improvements")
    print("==================================")
    
    controller = TorVisualController()
    
    print("\n🚀 Starting Tor with improved feedback...")
    print("⏹️ Press Ctrl+C to test interrupt handling")
    
    try:
        success = controller.start_tor_service()
        
        if success:
            print(f"\n✅ Tor startup test PASSED!")
            print(f"🧅 Current IP: {controller.current_ip}")
            controller.stop_tor_service()
        else:
            print(f"\n❌ Tor startup test FAILED")
            
    except KeyboardInterrupt:
        print(f"\n⚠️  Test interrupted - this is expected behavior!")
        print(f"✅ KeyboardInterrupt handling works correctly")
        controller.stop_tor_service()

if __name__ == "__main__":
    test_tor_startup()
