#!/usr/bin/env python3
"""
Interactive test for the updated visual Tor browser
"""
import sys
sys.path.append('.')

def simulate_option_1():
    """Simulate running option 1 with the new flow"""
    print("🎭 VISUAL TOR BROWSER WITH CONSISTENT IP")
    print("=======================================")
    print("Browse websites with visual feedback and same IP per session")
    
    try:
        from visual_tor_browser import VisualTorBrowser, TorVisualController
        
        browser = VisualTorBrowser()
        
        print("\n🎯 VISUAL BROWSING OPTIONS:")
        print("1. 🎭 Browse website with visual feedback (consistent IP)")
        print("2. 📊 View previous sessions")
        print("3. 🧪 Test Tor connection")
        
        print("\nSelected option: 1")
        
        # The new flow
        print(f"\n🧅 ESTABLISHING TOR CONNECTION")
        print(f"=============================")
        
        # First establish Tor connection
        tor_controller = TorVisualController()
        if not tor_controller.start_tor_service():
            print(f"❌ Failed to establish Tor connection")
            print(f"💡 Please ensure Tor is installed: brew install tor")
            return
        
        print(f"\n✅ Tor connection established successfully!")
        print(f"🌍 Your new anonymous IP: {tor_controller.current_ip}")
        print(f"🔒 This IP will be maintained for the entire session")
        print(f"🧅 All traffic will be routed through Tor network")
        
        # Now ask for website details
        print(f"\n🌐 WEBSITE SELECTION")
        print(f"==================")
        domain = "https://httpbin.org/ip"  # Test site to show IP
        print(f"Using test domain: {domain}")
        
        duration = 1  # Short test
        print(f"Duration: {duration} minutes")
        
        print(f"\n🚀 Starting visual browsing session")
        print(f"🌐 Target: {domain}")
        print(f"⏱️ Duration: {duration} minutes")
        print(f"🧅 Anonymous IP: {tor_controller.current_ip}")
        print(f"👁️ Browser window would open - watch the automation!")
        print(f"⏹️ Press Ctrl+C to stop early")
        
        # Set the tor controller for the browser to use the same connection
        browser.tor_controller = tor_controller
        
        print(f"\n🎉 New flow test completed successfully!")
        print(f"🧅 Final IP: {tor_controller.current_ip}")
        
        # Clean up
        tor_controller.stop_tor_service()
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Operation interrupted by user")
        print(f"💡 Tip: If Tor startup is slow, you can:")
        print(f"   - Wait for it to finish initializing")
        print(f"   - Use options 1/2 for faster non-visual browsing")
        print(f"   - Install Tor locally: brew install tor")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print(f"💡 Try restarting or use other browsing options")

if __name__ == "__main__":
    simulate_option_1()
