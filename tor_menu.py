#!/usr/bin/env python3
"""
Advanced Tor Browser Menu System
Interactive menu interface for all Tor browser automation features
Uses global configuration for unified Dutch rotation browser functionality
"""

import os
import time
from dutch_rotation_browser import DutchRotationBrowser, DutchRotationConfig

# Global configuration - used by all browser operations
GLOBAL_CONFIG = DutchRotationConfig(
    rotation_interval=3,
    user_agent_rotation=True,
    verify_dutch_ip=True,
    save_screenshots=True,
    min_delay=2.0,
    max_delay=6.0,
    headless=False,
    max_retries=3,
    tor_port=9050,
    control_port=9051
)


def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')


def show_banner():
    """Display the application banner"""
    clear_screen()
    print("🔐 ADVANCED TOR BROWSER AUTOMATION")
    print("🇳🇱 Dutch-Only Exit Nodes with IP Rotation")
    print("=" * 45)
    print("🎯 All operations use unified Dutch rotation browser")
    print("⚙️  Configure settings in option 4")
    print()


def custom_url_test():
    """Custom URL with full simulation using global Dutch rotation configuration"""
    clear_screen()
    print("🎯 CUSTOM URL FULL SIMULATION")
    print("🇳🇱 Using Dutch rotation browser with current global configuration")
    print("=" * 55)
    
    # Show current config briefly
    print(f"📋 Current config: {GLOBAL_CONFIG.rotation_interval} req rotation, "
          f"{GLOBAL_CONFIG.min_delay}-{GLOBAL_CONFIG.max_delay}s delay")
    print("💡 Use option 4 to change configuration\n")
    
    url = input("Enter URL to test: ").strip()
    if not url:
        print("❌ No URL provided!")
        input("Press Enter to continue...")
        return
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"\n🚀 Starting Dutch rotation simulation for: {url}")
    
    # Use global configuration
    browser = DutchRotationBrowser(GLOBAL_CONFIG)
    
    try:
        if browser.setup():
            print("✅ Dutch rotation browser setup successful!")
            print("🔄 Testing with current global configuration...")
            
            # Visit the URL multiple times to trigger rotation
            visits = min(5, GLOBAL_CONFIG.rotation_interval + 2)  # Ensure rotation happens
            for i in range(visits):
                print(f"\n--- Visit {i+1}/{visits} ---")
                success = browser.visit_with_rotation(url)
                if success:
                    print(f"✅ Visit {i+1} completed successfully")
                    print(f"📊 Current IP: {browser.current_ip}")
                    ua_display = browser.current_user_agent[:50] if browser.current_user_agent else "Unknown"
                    print(f"🎭 Current UA: {ua_display}...")
                else:
                    print(f"❌ Visit {i+1} failed")
            
            print(f"\n🎉 Full simulation completed!")
            print(f"📈 Total requests made: {browser.request_count}")
            print(f"🔄 IP changes: {len(browser.session_data['ip_changes'])}")
        else:
            print("❌ Browser setup failed!")
    finally:
        browser.cleanup()
    
    input("\nPress Enter to continue...")


def show_current_config():
    """Display current global configuration"""
    clear_screen()
    print("📋 CURRENT CONFIGURATION")
    print("=" * 30)
    print(f"🔄 Rotation interval: {GLOBAL_CONFIG.rotation_interval} requests")
    print(f"🎭 User agent rotation: {'✅ Enabled' if GLOBAL_CONFIG.user_agent_rotation else '❌ Disabled'}")
    print(f"🇳🇱 Verify Dutch IP: {'✅ Enabled' if GLOBAL_CONFIG.verify_dutch_ip else '❌ Disabled'}")
    print(f"📸 Screenshots: {'✅ Enabled' if GLOBAL_CONFIG.save_screenshots else '❌ Disabled'}")
    print(f"⏱️  Delay range: {GLOBAL_CONFIG.min_delay}s - {GLOBAL_CONFIG.max_delay}s")
    print(f"🖥️  Headless mode: {'✅ Enabled' if GLOBAL_CONFIG.headless else '❌ Disabled'}")
    print(f"🔍 Max retries: {GLOBAL_CONFIG.max_retries}")
    print(f"🗂️  Tor port: {GLOBAL_CONFIG.tor_port}")
    print(f"🎛️  Control port: {GLOBAL_CONFIG.control_port}")
    input("\nPress Enter to continue...")


def batch_testing():
    """Multiple URL batch testing using global Dutch rotation configuration"""
    clear_screen()
    print("🔍 BATCH URL TESTING")
    print("🇳🇱 Using Dutch rotation browser with current global configuration")
    print("=" * 50)
    
    print("Enter URLs (one per line, empty line to finish):")
    urls = []
    while True:
        url = input(f"URL {len(urls)+1}: ").strip()
        if not url:
            break
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        urls.append(url)
    
    if not urls:
        print("❌ No URLs provided!")
        input("Press Enter to continue...")
        return
    
    print(f"\n🚀 Testing {len(urls)} URLs with Dutch rotation...")
    
    # Use global configuration for batch testing
    browser = DutchRotationBrowser(GLOBAL_CONFIG)
    
    try:
        if browser.setup():
            results = []
            for i, url in enumerate(urls, 1):
                print(f"\n🌐 Testing {i}/{len(urls)}: {url}")
                success = browser.visit_with_rotation(url)
                results.append((url, success))
                
                # Show current IP for successful visits
                if success:
                    print(f"📊 Current IP: {browser.current_ip}")
            
            # Summary
            print(f"\n📊 BATCH RESULTS:")
            print("-" * 40)
            successful = sum(1 for _, success in results if success)
            print(f"✅ Successful: {successful}/{len(urls)}")
            print(f"❌ Failed: {len(urls) - successful}/{len(urls)}")
            print(f"🔄 IP changes: {len(browser.session_data['ip_changes'])}")
            
            for url, success in results:
                status = "✅" if success else "❌"
                print(f"{status} {url}")
        else:
            print("❌ Browser setup failed!")
    finally:
        browser.cleanup()
    
    input("\nPress Enter to continue...")


def browser_config():
    """Browser configuration menu - modifies global config for all operations"""
    global GLOBAL_CONFIG
    clear_screen()
    print("⚙️  BROWSER CONFIGURATION")
    print("=" * 30)
    print("💡 All changes apply to the global configuration used everywhere\n")
    
    print("Configuration options:")
    print("1. 🏃 Fast mode (minimal delays)")
    print("2. 🚶 Normal mode (balanced)")
    print("3. 🐌 Slow mode (maximum stealth)")
    print("4. 🖥️  Toggle headless mode")
    print("5. 🔄 Set rotation interval")
    print("6. 🎭 Toggle user agent rotation")
    print("7. 📸 Toggle screenshots")
    print("8. 🇳🇱 Toggle Dutch IP verification")
    print("9. ⏱️  Set delay range")
    print("10. 📋 Show current configuration")
    print("11. 🔙 Back to main menu")
    
    try:
        choice = int(input("\nSelect option (1-11): "))
        
        if choice == 1:
            print("🏃 Fast mode selected")
            GLOBAL_CONFIG.min_delay = 0.5
            GLOBAL_CONFIG.max_delay = 1.5
            GLOBAL_CONFIG.rotation_interval = 1
            print("✅ Global config updated to fast mode")
        elif choice == 2:
            print("🚶 Normal mode selected")
            GLOBAL_CONFIG.min_delay = 2.0
            GLOBAL_CONFIG.max_delay = 5.0
            GLOBAL_CONFIG.rotation_interval = 3
            print("✅ Global config updated to normal mode")
        elif choice == 3:
            print("🐌 Slow mode selected")
            GLOBAL_CONFIG.min_delay = 5.0
            GLOBAL_CONFIG.max_delay = 12.0
            GLOBAL_CONFIG.rotation_interval = 5
            print("✅ Global config updated to slow mode")
        elif choice == 4:
            GLOBAL_CONFIG.headless = not GLOBAL_CONFIG.headless
            status = "enabled" if GLOBAL_CONFIG.headless else "disabled"
            print(f"🖥️  Headless mode {status}")
        elif choice == 5:
            try:
                interval = int(input("Enter rotation interval (requests): "))
                if interval > 0:
                    GLOBAL_CONFIG.rotation_interval = interval
                    print(f"✅ Rotation interval set to {interval} requests")
                else:
                    print("❌ Invalid interval")
            except ValueError:
                print("❌ Invalid input")
        elif choice == 6:
            GLOBAL_CONFIG.user_agent_rotation = not GLOBAL_CONFIG.user_agent_rotation
            status = "enabled" if GLOBAL_CONFIG.user_agent_rotation else "disabled"
            print(f"🎭 User agent rotation {status}")
        elif choice == 7:
            GLOBAL_CONFIG.save_screenshots = not GLOBAL_CONFIG.save_screenshots
            status = "enabled" if GLOBAL_CONFIG.save_screenshots else "disabled"
            print(f"📸 Screenshots {status}")
        elif choice == 8:
            GLOBAL_CONFIG.verify_dutch_ip = not GLOBAL_CONFIG.verify_dutch_ip
            status = "enabled" if GLOBAL_CONFIG.verify_dutch_ip else "disabled"
            print(f"🇳🇱 Dutch IP verification {status}")
        elif choice == 9:
            try:
                min_delay = float(input("Enter minimum delay (seconds): "))
                max_delay = float(input("Enter maximum delay (seconds): "))
                if min_delay >= 0 and max_delay > min_delay:
                    GLOBAL_CONFIG.min_delay = min_delay
                    GLOBAL_CONFIG.max_delay = max_delay
                    print(f"✅ Delay range set to {min_delay}s - {max_delay}s")
                else:
                    print("❌ Invalid delay range")
            except ValueError:
                print("❌ Invalid input")
        elif choice == 10:
            show_current_config()
            return
        elif choice == 11:
            return
        else:
            print("❌ Invalid choice!")
            
    except ValueError:
        print("❌ Invalid input!")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    if choice != 11 and choice != 10:
        input("\nPress Enter to continue...")
    
    # Recursively show the menu again unless returning
    if choice != 11:
        browser_config()


def httpbin_testing():
    """Test httpbin features with Dutch rotation browser"""
    clear_screen()
    print("🧪 HTTPBIN TESTING")
    print("🇳🇱 Using Dutch rotation browser with current global configuration")
    print("=" * 50)
    
    browser = DutchRotationBrowser(GLOBAL_CONFIG)
    
    try:
        if browser.setup():
            print("✅ Dutch rotation browser setup successful!")
            print("🔄 Testing httpbin features with current global configuration...")
            
            # Test httpbin features with rotation
            browser.test_httpbin_features()
        else:
            print("❌ Browser setup failed!")
    finally:
        browser.cleanup()
    
    input("\nPress Enter to continue...")


def main_menu():
    """Display the main menu and handle user selections"""
    while True:
        show_banner()
        
        print("Main Menu:")
        print("1. 🎯 Custom URL (Full Simulation)")
        print("2. 🔍 Batch URL Testing")
        print("3. 🧪 HTTPBin Testing")
        print("4. ⚙️  Browser Configuration")
        print("5. 📋 Show Current Configuration")
        print("6. 🚪 Exit")
        print()
        
        try:
            choice = input("Select option (1-6): ").strip()
            
            if choice == '1':
                custom_url_test()
            elif choice == '2':
                batch_testing()
            elif choice == '3':
                httpbin_testing()
            elif choice == '4':
                browser_config()
            elif choice == '5':
                show_current_config()
            elif choice == '6':
                clear_screen()
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please select 1-6.")
                time.sleep(1)
                
        except KeyboardInterrupt:
            clear_screen()
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main_menu()
