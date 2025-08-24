#!/usr/bin/env python3
"""
Test the updated visual Tor browser with pre-connection
"""
import sys
sys.path.append('.')
from visual_tor_browser import VisualTorBrowser, TorVisualController

def test_new_flow():
    """Test the new flow: Tor connection first, then URL input"""
    print("🧪 Testing New Flow: Tor Connection → URL Input")
    print("===============================================")
    
    try:
        # Step 1: Establish Tor connection first
        print("\n🧅 STEP 1: ESTABLISHING TOR CONNECTION")
        print("=====================================")
        
        tor_controller = TorVisualController()
        if not tor_controller.start_tor_service():
            print("❌ Failed to establish Tor connection")
            return
        
        print(f"\n✅ Tor connection established successfully!")
        print(f"🌍 Your new anonymous IP: {tor_controller.current_ip}")
        print(f"🔒 This IP will be maintained for the entire session")
        
        # Step 2: Create browser with existing Tor connection
        print(f"\n🎭 STEP 2: INITIALIZING BROWSER")
        print(f"==============================")
        
        browser = VisualTorBrowser()
        browser.tor_controller = tor_controller  # Use existing connection
        
        print(f"✅ Browser initialized with existing Tor connection")
        print(f"🧅 Session IP: {tor_controller.current_ip}")
        
        # Step 3: Test session start (without actually opening browser)
        print(f"\n🚀 STEP 3: TESTING SESSION START")
        print(f"================================")
        
        # Mock the browser creation for testing
        browser.current_profile = browser.behavior_engine.generate_session_profile()
        
        print(f"✅ Session preparation successful!")
        print(f"👤 Generated human profile: {browser.current_profile['name']}")
        print(f"🧅 Ready to browse with IP: {tor_controller.current_ip}")
        
        # Cleanup
        tor_controller.stop_tor_service()
        print(f"\n🧹 Test completed successfully!")
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")

if __name__ == "__main__":
    test_new_flow()
