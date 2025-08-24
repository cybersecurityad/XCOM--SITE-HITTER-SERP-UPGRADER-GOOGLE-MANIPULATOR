#!/usr/bin/env python3
"""
Test the enhanced visual browser with stealth integration
"""
import sys
sys.path.append('.')

def test_enhanced_browser():
    """Test the browser creation with enhanced stealth"""
    print("🧪 Testing Enhanced Visual Browser")
    print("=================================")
    
    try:
        from visual_tor_browser import VisualTorBrowser, TorVisualController
        
        # Step 1: Establish Tor connection
        print("\n🧅 STEP 1: ESTABLISHING TOR CONNECTION")
        tor_controller = TorVisualController()
        if not tor_controller.start_tor_service():
            print("❌ Failed to establish Tor connection")
            return
        
        print(f"✅ Tor connection established")
        print(f"🧅 Anonymous IP: {tor_controller.current_ip}")
        
        # Step 2: Create browser with enhanced stealth
        print(f"\n🎭 STEP 2: CREATING ENHANCED BROWSER")
        browser = VisualTorBrowser()
        browser.tor_controller = tor_controller
        
        # Generate profile
        browser.current_profile = browser.behavior_engine.generate_session_profile()
        print(f"👤 Generated profile: {browser.current_profile['name']}")
        
        # Test browser creation
        print(f"\n🚀 STEP 3: TESTING BROWSER CREATION")
        success = browser.create_visual_browser()
        
        if success:
            print(f"✅ Browser creation test PASSED!")
            print(f"🎭 Visual browser ready with stealth features")
            
            # Quick test
            if browser.driver:
                print(f"🔍 Testing basic navigation...")
                try:
                    browser.driver.get("about:blank")
                    print(f"✅ Navigation test successful")
                except Exception as nav_error:
                    print(f"⚠️ Navigation test failed: {nav_error}")
                
                # Cleanup
                browser.driver.quit()
                print(f"🧹 Browser closed")
        else:
            print(f"❌ Browser creation test FAILED")
        
        # Cleanup Tor
        tor_controller.stop_tor_service()
        print(f"✅ Test completed")
        
    except KeyboardInterrupt:
        print(f"\n⚠️ Test interrupted by user")
    except ImportError as import_error:
        print(f"❌ Import error: {import_error}")
        print(f"💡 Ensure all dependencies are installed")
    except Exception as e:
        print(f"❌ Test error: {e}")
        print(f"💡 Check the error details above")

if __name__ == "__main__":
    test_enhanced_browser()
