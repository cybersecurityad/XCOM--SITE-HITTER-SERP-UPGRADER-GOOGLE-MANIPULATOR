#!/usr/bin/env python3
"""
Advanced Tor Browser Menu System
==============================

Interactive menu interface for all Tor browser automation features.
Choose from different browsing modes and configurations.
"""

import os
import sys
from typing import Optional
from simple_advanced_tor_browser import SimpleAdvancedTorBrowser, SimpleTorConfig
from dutch_rotation_browser import DutchRotationBrowser, DutchRotationConfig
from visual_tor_browser import VisualTorBrowser


def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')


def main_menu():
    """Display main menu and handle user input"""
    while True:
        clear_screen()
        print("🚀 ADVANCED TOR BROWSER AUTOMATION SYSTEM")
        print("=" * 50)
        print("Features: Human simulation, stealth, proxy rotation, Dutch-only exit nodes")
        print("=" * 50)


def print_banner():
    """Print system banner"""
    print("🚀 ADVANCED TOR BROWSER AUTOMATION SYSTEM")
    print("=" * 50)
    print("Features: Human simulation, stealth, proxy rotation, Dutch-only exit nodes")
    print("=" * 50)


def print_main_menu():
    """Print the main menu options"""
    print("\n📋 MAIN MENU:")
    print("-" * 30)
    print("1. 🌐 Quick Website Test")
    print("2. 🎯 Custom URL with Full Simulation")
    print("3. 🔍 Multiple URL Batch Testing")
    print("4. ⚙️  Browser Configuration")
    print("5. 📊 Advanced Features Demo")
    print("6. 🧪 Tor Connection Test")
    print("7. 📖 Help & Documentation")
    print("8. 🚪 Exit")
    print("-" * 30)


def quick_test():
    """Quick website test with predefined URLs"""
    clear_screen()
    print("🌐 QUICK WEBSITE TEST")
    print("=" * 30)
    
    test_urls = [
        ("Tor IP Check", "https://httpbin.org/ip"),
        ("Tor Project Check", "https://check.torproject.org"),
        ("Headers Check", "https://httpbin.org/headers"),
        ("Example Site", "https://example.com")
    ]
    
    print("Available test sites:")
    for i, (name, url) in enumerate(test_urls, 1):
        print(f"{i}. {name} - {url}")
    
    try:
        choice = int(input("\nSelect a site (1-4): "))
        if 1 <= choice <= len(test_urls):
            name, url = test_urls[choice - 1]
            print(f"\n🎯 Testing: {name}")
            
            config = SimpleTorConfig(save_screenshots=True)
            browser = SimpleAdvancedTorBrowser(config)
            
            try:
                if browser.setup():
                    browser.comprehensive_page_visit(url)
                else:
                    print("❌ Browser setup failed!")
            finally:
                browser.cleanup()
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Please enter a valid number!")
    
    input("\nPress Enter to continue...")


def custom_url_test():
    """Custom URL with full simulation using Dutch rotation browser"""
    clear_screen()
    print("🎯 CUSTOM URL FULL SIMULATION")
    print("🇳🇱 Using Dutch rotation browser with IP rotation")
    print("=" * 45)
    
    url = input("Enter URL to test: ").strip()
    if not url:
        print("❌ No URL provided!")
        input("Press Enter to continue...")
        return
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"\n🚀 Starting Dutch rotation simulation for: {url}")
    
    # Configure Dutch rotation browser for full simulation
    config = DutchRotationConfig(
        rotation_interval=2,  # Rotate IP every 2 requests
        user_agent_rotation=True,
        verify_dutch_ip=True,
        save_screenshots=True,
        min_delay=3.0,
        max_delay=8.0
    )
    
    browser = DutchRotationBrowser(config)
    
    try:
        if browser.setup():
            print("✅ Dutch rotation browser setup successful!")
            print("🔄 Testing with automatic IP and user agent rotation...")
            
            # Visit the URL multiple times to trigger rotation
            for i in range(3):
                print(f"\n--- Visit {i+1}/3 ---")
                success = browser.visit_with_rotation(url)
                if success:
                    print(f"✅ Visit {i+1} completed successfully")
                    print(f"� Current IP: {browser.current_ip}")
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


def batch_testing():
    """Multiple URL batch testing"""
    clear_screen()
    print("🔍 BATCH URL TESTING")
    print("=" * 25)
    
    print("Enter URLs (one per line, empty line to finish):")
    urls = []
    while True:
        url = input(f"URL {len(urls) + 1}: ").strip()
        if not url:
            break
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        urls.append(url)
    
    if not urls:
        print("❌ No URLs provided!")
        input("Press Enter to continue...")
        return
    
    print(f"\n🚀 Testing {len(urls)} URLs...")
    
    config = SimpleTorConfig(save_screenshots=True)
    browser = SimpleAdvancedTorBrowser(config)
    
    try:
        if browser.setup():
            results = []
            for i, url in enumerate(urls, 1):
                print(f"\n🌐 Testing {i}/{len(urls)}: {url}")
                result = browser.comprehensive_page_visit(url)
                results.append((url, result))
                
                # Delay between requests
                if i < len(urls):
                    import time, random
                    delay = random.uniform(3, 8)
                    print(f"⏰ Waiting {delay:.1f}s before next URL...")
                    time.sleep(delay)
            
            # Summary
            print(f"\n📊 BATCH RESULTS:")
            print("-" * 40)
            successful = sum(1 for _, r in results if r['success'])
            print(f"✅ Successful: {successful}/{len(urls)}")
            print(f"❌ Failed: {len(urls) - successful}/{len(urls)}")
            
            for url, result in results:
                status = "✅" if result['success'] else "❌"
                print(f"{status} {url}")
        else:
            print("❌ Browser setup failed!")
    finally:
        browser.cleanup()
    
    input("\nPress Enter to continue...")


def browser_config():
    """Browser configuration menu"""
    clear_screen()
    print("⚙️  BROWSER CONFIGURATION")
    print("=" * 30)
    
    print("Configuration options:")
    print("1. 🏃 Fast mode (minimal delays)")
    print("2. 🚶 Normal mode (balanced)")
    print("3. 🐌 Slow mode (maximum stealth)")
    print("4. 🖥️  Headless mode")
    print("5. 🇳🇱 Dutch rotation browser (IP + UA rotation)")
    print("6. 🇳🇱 Dutch-only exit nodes (simple)")
    print("7. 🌍 Global exit nodes (default)")
    print("8. � Visual GA4 browser (human simulation)")
    print("9. �🖱️  Mouse simulation settings")
    print("10. 📸 Screenshot settings")
    print("11. 🔙 Back to main menu")
    
    try:
        choice = int(input("\nSelect option (1-11): "))
        
        browser = None
        
        if choice == 1:
            print("🏃 Fast mode selected")
            config = SimpleTorConfig(min_delay=0.5, max_delay=1.5)
            browser = SimpleAdvancedTorBrowser(config)
        elif choice == 2:
            print("🚶 Normal mode selected")
            config = SimpleTorConfig(min_delay=2.0, max_delay=5.0)
            browser = SimpleAdvancedTorBrowser(config)
        elif choice == 3:
            print("🐌 Slow mode selected")
            config = SimpleTorConfig(min_delay=5.0, max_delay=12.0)
            browser = SimpleAdvancedTorBrowser(config)
        elif choice == 4:
            print("🖥️  Headless mode")
            config = SimpleTorConfig(headless=True)
            browser = SimpleAdvancedTorBrowser(config)
        elif choice == 5:
            print("🇳🇱 Dutch rotation browser - Advanced IP & User Agent rotation")
            config = DutchRotationConfig(
                rotation_interval=3,
                user_agent_rotation=True,
                verify_dutch_ip=True,
                save_screenshots=True
            )
            browser = DutchRotationBrowser(config)
        elif choice == 6:
            print("🇳🇱 Dutch-only exit nodes (simple)")
            config = SimpleTorConfig(
                use_dutch_exit_nodes_only=True,
                save_screenshots=True
            )
            browser = SimpleAdvancedTorBrowser(config)
        elif choice == 7:
            print("🌍 Global exit nodes mode")
            config = SimpleTorConfig(
                use_dutch_exit_nodes_only=False,
                save_screenshots=True
            )
            browser = SimpleAdvancedTorBrowser(config)
        elif choice == 8:
            print("📊 Visual GA4 browser - Google Analytics compatible with human simulation")
            browser = VisualTorBrowser()
        elif choice == 11:
            return
        else:
            print("⚙️  Feature configuration coming soon...")
            input("Press Enter to continue...")
            return
        
        # Test with selected config
        if choice in [1, 2, 3, 4, 6, 7]:
            url = input("Enter test URL: ").strip()
            if url:
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                try:
                    if browser and browser.setup():
                        browser.comprehensive_page_visit(url)
                finally:
                    if browser:
                        browser.cleanup()
        elif choice == 5:
            # Dutch rotation browser
            print("🧪 Testing Dutch rotation browser with httpbin...")
            if browser and isinstance(browser, DutchRotationBrowser):
                try:
                    if browser.setup():
                        # Test httpbin features with rotation
                        browser.test_httpbin_features()
                finally:
                    browser.cleanup()
            else:
                print("❌ Browser type mismatch!")
                input("Press Enter to continue...")
                return
        elif choice == 8:
            # Visual GA4 browser
            print("📊 Testing Visual GA4 browser...")
            if browser and isinstance(browser, VisualTorBrowser):
                url = input("Enter URL to visit with GA4 tracking: ").strip()
                if url:
                    if not url.startswith(('http://', 'https://')):
                        url = 'https://' + url
                    try:
                        # Extract domain from URL for the browse method
                        from urllib.parse import urlparse
                        domain = urlparse(url).netloc
                        print(f"🚀 Starting visual browsing session for {domain}...")
                        result = browser.browse_website_visually(domain, duration_minutes=2)
                        print(f"✅ Session completed: {result}")
                    except Exception as e:
                        print(f"❌ Error: {e}")
            else:
                print("❌ Browser type mismatch!")
                input("Press Enter to continue...")
                return
        
    except ValueError:
        print("❌ Please enter a valid number!")
    
    input("Press Enter to continue...")


def advanced_demo():
    """Advanced features demonstration"""
    clear_screen()
    print("📊 ADVANCED FEATURES DEMO")
    print("=" * 30)
    
    print("Available demos:")
    print("1. 🎭 User Agent Rotation Demo")
    print("2. 🖱️  Mouse Movement Simulation")
    print("3. 📜 Scrolling Patterns Demo")
    print("4. 🔍 Content Analysis Demo")
    print("5. 🔄 Tor Identity Change Demo")
    print("6. 🔙 Back to main menu")
    
    try:
        choice = int(input("\nSelect demo (1-6): "))
        
        if choice == 6:
            return
        elif choice == 1:
            print("🎭 User Agent Rotation Demo")
            config = SimpleTorConfig(rotate_user_agents=True)
            browser = SimpleAdvancedTorBrowser(config)
            
            try:
                if browser.setup():
                    # Show different user agents
                    for i in range(3):
                        ua = browser.get_user_agent()
                        print(f"User Agent {i+1}: {ua[:60]}...")
                        browser.navigate_with_behavior("https://httpbin.org/headers")
                        import time
                        time.sleep(2)
            finally:
                browser.cleanup()
        else:
            print("🚧 Demo coming soon...")
            
    except ValueError:
        print("❌ Please enter a valid number!")
    
    input("Press Enter to continue...")


def tor_test():
    """Tor connection test"""
    clear_screen()
    print("🧪 TOR CONNECTION TEST")
    print("=" * 25)
    
    print("Testing Tor connectivity...")
    
    config = SimpleTorConfig()
    browser = SimpleAdvancedTorBrowser(config)
    
    try:
        print("🔄 Checking Homebrew Tor service...")
        if browser.check_homebrew_tor():
            print("✅ Tor service is running")
            
            print("🔄 Verifying Tor IP...")
            tor_ip = browser.get_tor_ip()
            if tor_ip:
                print(f"✅ Tor IP confirmed: {tor_ip}")
                print("🔄 Testing Tor detection...")
                
                if browser.create_browser():
                    browser.navigate_with_behavior("https://check.torproject.org")
                    print("✅ Tor detection test completed")
                else:
                    print("❌ Browser creation failed")
            else:
                print("❌ Could not verify Tor IP")
        else:
            print("❌ Tor service not running")
            print("💡 Try: brew services start tor")
    finally:
        browser.cleanup()
    
    input("\nPress Enter to continue...")


def show_help():
    """Show help and documentation"""
    clear_screen()
    print("📖 HELP & DOCUMENTATION")
    print("=" * 30)
    
    print("""
🚀 ADVANCED TOR BROWSER SYSTEM

This system provides anonymous web browsing with human-like behavior
simulation using Tor network and advanced browser automation.

📋 MAIN FEATURES:
• 🔒 Tor anonymization (Homebrew integration)
• 🤖 Human behavior simulation
• 🎯 Advanced page analysis
• 📸 Screenshot capture
• 🖱️  Mouse movement simulation
• 📜 Natural scrolling patterns
• 🔄 User agent rotation

🛠️  REQUIREMENTS:
• Homebrew Tor service: brew install tor
• Python virtual environment activated
• Chrome browser installed

🚀 QUICK START:
1. Start Tor: brew services start tor
2. Run menu: python3 tor_menu.py
3. Choose option 1 for quick test

🔧 CONFIGURATION:
• Fast mode: Minimal delays (0.5-1.5s)
• Normal mode: Balanced timing (2-5s)
• Slow mode: Maximum stealth (5-12s)

📁 KEY FILES:
• simple_advanced_tor_browser.py - Main implementation
• main_tor_browser.py - Core Tor browser
• test_verenigdamsterdam.py - Example usage

🆘 TROUBLESHOOTING:
• Exit code 15: Use Homebrew Tor service
• Chrome issues: Check Chrome version
• Tor connectivity: Verify port 9050

For more help, check the README.md file.
    """)
    
    input("\nPress Enter to continue...")


def main():
    """Main menu loop"""
    while True:
        clear_screen()
        print_banner()
        print_main_menu()
        
        try:
            choice = input("\nSelect option (1-8): ").strip()
            
            if choice == '1':
                quick_test()
            elif choice == '2':
                custom_url_test()
            elif choice == '3':
                batch_testing()
            elif choice == '4':
                browser_config()
            elif choice == '5':
                advanced_demo()
            elif choice == '6':
                tor_test()
            elif choice == '7':
                show_help()
            elif choice == '8':
                clear_screen()
                print("👋 Thanks for using Advanced Tor Browser System!")
                print("🔒 Stay anonymous, stay safe!")
                sys.exit(0)
            else:
                print("❌ Invalid choice! Please select 1-8.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            clear_screen()
            print("\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
