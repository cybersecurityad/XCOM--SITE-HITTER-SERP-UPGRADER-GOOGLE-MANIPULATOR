#!/usr/bin/env python3
#!/usr/bin/env python3
"""
XCOM.DEV -- ADVANCED WEB SITE HITTER -- SERP UPGRADER- GOOGLE MANIPULATOR
Professional SEO Enhancement & Web Automation Tool

Licensed to:
XCOM.DEV
PW OLDENBURGER
SINT OLOSSTEEG 4C
1012AK AMSTERDAM
NETHERLANDS
JEDI@XCOM.DEV
+31648319157

© 2025 XCOM.DEV. All rights reserved.

This software is proprietary and confidential. Unauthorized reproduction or 
distribution of this program, or any portion of it, may result in severe civil 
and criminal penalties, and will be prosecuted to the maximum extent possible 
under the law.

Main menu system for advanced SEO manipulation and web automation.
"""

import os
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
    control_port=9051,
    # Human simulation settings
    enable_human_simulation=True,
    simulate_mouse_movements=True,
    simulate_reading_behavior=True,
    simulate_scrolling=True,
    simulate_clicking=True,
    behavior_profile="balanced"
)


def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')


def show_banner():
    """Display the application banner"""
    clear_screen()
    print("--")
    print("🔐 ADVANCED TOR BROWSER AUTOMATION")
    print()
    print("$$\\   $$\\  $$$$$$\\   $$$$$$\\  $$\\      $$\\     $$$$$$$\\  $$$$$$$$\\ $$\\    $$\\")
    print("$$ |  $$ |$$  __$$\\ $$  __$$\\ $$$\\    $$$ |    $$  __$$\\ $$  _____|$$ |   $$ |")
    print("\\$$\\ $$  |$$ /  \\__|$$ /  $$ |$$$$\\  $$$$ |    $$ |  $$ |$$ |      $$ |   $$ |")
    print(" \\$$$$  / $$ |      $$ |  $$ |$$\\$$\\$$ $$ |    $$ |  $$ |$$$$$\\    \\$$\\  $$  /")
    print(" $$  $$<  $$ |      $$ |  $$ |$$ \\$$$  $$ |    $$ |  $$ |$$  __|    \\$$\\$$  /")
    print("$$  /\\$$\\ $$ |  $$\\ $$ |  $$ |$$ |\\$  /$$ |    $$ |  $$ |$$ |        \\$$$  /")
    print("$$ /  $$ |\\$$$$$$  | $$$$$$  |$$ | \\_/ $$ |$$\\ $$$$$$$  |$$$$$$$$\\    \\$  /")
    print("\\__|  \\__| \\______/  \\______/ \\__|     \\__|\\__|\\_______/ \\________|    \\_/")
    print()
    print("--")
    print()
    print("XCOM.DEV -- ADVANCED SITE HITTER --")
    print()
    print("--")
    print()
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
    stay_time = getattr(GLOBAL_CONFIG, 'page_stay_time_minutes', 5.0)
    repeat_count = getattr(GLOBAL_CONFIG, 'simulation_repeat_count', 1)
    repeat_text = "infinite" if repeat_count == 0 else str(repeat_count)
    print(f"⏰ Stay time: {stay_time} min, � Repeats: {repeat_text}")
    print("�💡 Use option 4 to change configuration\n")
    
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
            
            # Implement repeat functionality
            current_cycle = 0
            total_visits = 0
            
            while True:
                current_cycle += 1
                
                # Check if we should stop (finite repeats)
                if repeat_count > 0 and current_cycle > repeat_count:
                    print(f"\n🏁 Completed all {repeat_count} simulation cycles")
                    break
                
                if repeat_count == 0:
                    print(f"\n🔄 Starting infinite simulation cycle #{current_cycle}")
                    print("   💡 Press Ctrl+C to stop at any time")
                else:
                    print(f"\n🔄 Starting simulation cycle {current_cycle}/{repeat_count}")
                
                try:
                    # Visit the URL and stay for specified time
                    print(f"🌐 Visiting: {url}")
                    success = browser.visit_with_rotation(url)
                    
                    if success:
                        total_visits += 1
                        print(f"✅ Visit successful")
                        print(f"📊 Current IP: {browser.current_ip}")
                        ua_display = browser.current_user_agent[:50] if browser.current_user_agent else "Unknown"
                        print(f"🎭 Current UA: {ua_display}...")
                        
                        # Stay on page for specified time
                        stay_seconds = stay_time * 60
                        print(f"⏰ Staying on page for {stay_time} minutes ({stay_seconds:.0f} seconds)...")
                        
                        # Show progress every 30 seconds
                        elapsed = 0
                        while elapsed < stay_seconds:
                            wait_time = min(30, stay_seconds - elapsed)
                            time.sleep(wait_time)
                            elapsed += wait_time
                            remaining_mins = (stay_seconds - elapsed) / 60
                            if remaining_mins > 0:
                                print(f"   ⏳ {remaining_mins:.1f} minutes remaining...")
                        
                        print(f"✅ Completed {stay_time}-minute stay on page")
                        
                    else:
                        print(f"❌ Visit failed")
                        
                except KeyboardInterrupt:
                    print("\n\n⏹️  Simulation interrupted by user")
                    break
                    
                # Brief pause between cycles
                if repeat_count == 0 or current_cycle < repeat_count:
                    print("⏸️  Brief pause before next cycle...")
                    time.sleep(2)
            
            print(f"\n🎉 Simulation completed!")
            print(f"📈 Total successful visits: {total_visits}")
            print(f"🔄 Total cycles completed: {current_cycle - (1 if repeat_count > 0 and current_cycle > repeat_count else 0)}")
            print(f"� IP changes: {len(browser.session_data['ip_changes'])}")
        else:
            print("❌ Browser setup failed!")
    except KeyboardInterrupt:
        print("\n\n⏹️  Simulation interrupted by user")
    finally:
        browser.cleanup()
    
    input("\nPress Enter to continue...")


def show_current_config():
    """Display current global configuration"""
    clear_screen()
    print("📋 CURRENT CONFIGURATION")
    print("=" * 40)
    
    # Basic settings
    print("🔧 BASIC SETTINGS:")
    print(f"🔄 Rotation interval: {GLOBAL_CONFIG.rotation_interval} requests")
    print(f"🎭 User agent rotation: {'✅ Enabled' if GLOBAL_CONFIG.user_agent_rotation else '❌ Disabled'}")
    print(f"🇳🇱 Verify Dutch IP: {'✅ Enabled' if GLOBAL_CONFIG.verify_dutch_ip else '❌ Disabled'}")
    print(f"📸 Screenshots: {'✅ Enabled' if GLOBAL_CONFIG.save_screenshots else '❌ Disabled'}")
    print(f"⏱️  Delay range: {GLOBAL_CONFIG.min_delay}s - {GLOBAL_CONFIG.max_delay}s")
    print(f"🖥️  Headless mode: {'✅ Enabled' if GLOBAL_CONFIG.headless else '❌ Disabled'}")
    print(f"🔍 Max retries: {GLOBAL_CONFIG.max_retries}")
    print(f"🗂️  Tor port: {GLOBAL_CONFIG.tor_port}")
    print(f"🎛️  Control port: {GLOBAL_CONFIG.control_port}")
    
    # Human simulation settings
    print(f"\n🎭 HUMAN SIMULATION:")
    print(f"🎪 Overall simulation: {'✅ Enabled' if GLOBAL_CONFIG.enable_human_simulation else '❌ Disabled'}")
    if hasattr(GLOBAL_CONFIG, 'behavior_profile'):
        print(f"🎯 Behavior profile: {GLOBAL_CONFIG.behavior_profile.capitalize()}")
    if hasattr(GLOBAL_CONFIG, 'simulate_mouse_movements'):
        print(f"🖱️  Mouse movements: {'✅ Enabled' if GLOBAL_CONFIG.simulate_mouse_movements else '❌ Disabled'}")
    if hasattr(GLOBAL_CONFIG, 'simulate_scrolling'):
        print(f"📜 Scrolling simulation: {'✅ Enabled' if GLOBAL_CONFIG.simulate_scrolling else '❌ Disabled'}")
    if hasattr(GLOBAL_CONFIG, 'simulate_clicking'):
        print(f"🔗 Link clicking: {'✅ Enabled' if GLOBAL_CONFIG.simulate_clicking else '❌ Disabled'}")
    if hasattr(GLOBAL_CONFIG, 'simulate_reading_behavior'):
        print(f"📖 Reading simulation: {'✅ Enabled' if GLOBAL_CONFIG.simulate_reading_behavior else '❌ Disabled'}")
    
    # Extended simulation settings
    print(f"\n⏰ EXTENDED SIMULATION:")
    if hasattr(GLOBAL_CONFIG, 'page_stay_time_minutes'):
        print(f"⏰ Page stay time: {GLOBAL_CONFIG.page_stay_time_minutes} minutes")
    if hasattr(GLOBAL_CONFIG, 'simulation_repeat_count'):
        repeat_text = "Infinite" if GLOBAL_CONFIG.simulation_repeat_count == 0 else str(GLOBAL_CONFIG.simulation_repeat_count)
        print(f"🔁 Simulation repeats: {repeat_text}")
    
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
    print("11. 🎪 Toggle human simulation")
    print("12. 🎯 Set behavior profile")
    print("13. 🖱️  Configure mouse simulation")
    print("14. 📜 Configure scrolling simulation")
    print("15. 🔗 Configure link clicking")
    print("16. ⏰ Set page stay time (10-60 minutes)")
    print("17. 🔁 Set simulation repeat count")
    print("18. 🔙 Back to main menu")
    
    try:
        choice = int(input("\nSelect option (1-18): "))
        
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
            GLOBAL_CONFIG.enable_human_simulation = not GLOBAL_CONFIG.enable_human_simulation
            status = "enabled" if GLOBAL_CONFIG.enable_human_simulation else "disabled"
            print(f"🎪 Human simulation {status}")
        elif choice == 12:
            profiles = ["balanced", "curious", "focused", "scanner"]
            print("\nAvailable behavior profiles:")
            for i, profile in enumerate(profiles, 1):
                current = " (current)" if profile == GLOBAL_CONFIG.behavior_profile else ""
                print(f"  {i}. {profile.capitalize()}{current}")
            try:
                profile_choice = int(input("Select profile (1-4): ")) - 1
                if 0 <= profile_choice < len(profiles):
                    GLOBAL_CONFIG.behavior_profile = profiles[profile_choice]
                    print(f"✅ Behavior profile set to {profiles[profile_choice]}")
                else:
                    print("❌ Invalid choice")
            except ValueError:
                print("❌ Invalid input")
        elif choice == 13:
            GLOBAL_CONFIG.simulate_mouse_movements = not GLOBAL_CONFIG.simulate_mouse_movements
            status = "enabled" if GLOBAL_CONFIG.simulate_mouse_movements else "disabled"
            print(f"🖱️  Mouse simulation {status}")
        elif choice == 14:
            GLOBAL_CONFIG.simulate_scrolling = not GLOBAL_CONFIG.simulate_scrolling
            status = "enabled" if GLOBAL_CONFIG.simulate_scrolling else "disabled"
            print(f"📜 Scrolling simulation {status}")
        elif choice == 15:
            GLOBAL_CONFIG.simulate_clicking = not GLOBAL_CONFIG.simulate_clicking
            status = "enabled" if GLOBAL_CONFIG.simulate_clicking else "disabled"
            print(f"🔗 Link clicking simulation {status}")
        elif choice == 16:
            try:
                stay_time = float(input("Enter page stay time in minutes (10-60): "))
                if 10.0 <= stay_time <= 60.0:
                    GLOBAL_CONFIG.page_stay_time_minutes = stay_time
                    print(f"✅ Page stay time set to {stay_time} minutes")
                else:
                    print("❌ Stay time must be between 10 and 60 minutes")
            except ValueError:
                print("❌ Invalid input")
        elif choice == 17:
            try:
                repeat_count = int(input("Enter simulation repeat count (1+ for limited, 0 for infinite): "))
                if repeat_count >= 0:
                    GLOBAL_CONFIG.simulation_repeat_count = repeat_count
                    if repeat_count == 0:
                        print("✅ Simulation repeat count set to INFINITE")
                    else:
                        print(f"✅ Simulation repeat count set to {repeat_count}")
                else:
                    print("❌ Repeat count must be 0 or positive")
            except ValueError:
                print("❌ Invalid input")
        elif choice == 18:
            return
        else:
            print("❌ Invalid choice!")
            
    except ValueError:
        print("❌ Invalid input!")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    if choice != 18 and choice != 10:
        input("\nPress Enter to continue...")
    
    # Recursively show the menu again unless returning
    if choice != 18:
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


def google_search_visit():
    """Visit a URL through DuckDuckGo search - more realistic browsing pattern"""
    clear_screen()
    print("🌐 VISIT URL THROUGH DUCKDUCKGO SEARCH")
    print("=" * 50)
    print("🇳🇱 Using Dutch rotation browser with current global configuration")
    print("🔍 Will search on DuckDuckGo and click the result")
    print("🦆 DuckDuckGo is Tor-friendly and privacy-focused!")
    print()
    
    url = input("Enter URL to find via DuckDuckGo search: ").strip()
    if not url:
        print("❌ No URL provided!")
        input("\nPress Enter to continue...")
        return
    
    # Add protocol if not present
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Extract domain for search query
    domain = url.replace('https://', '').replace('http://', '').split('/')[0]
    
    print(f"🎯 Target URL: {url}")
    print(f"🔍 Searching for: {domain}")
    print("🦆 Using DuckDuckGo search...")
    
    browser = DutchRotationBrowser(GLOBAL_CONFIG)
    
    try:
        if browser.setup():
            print("✅ Dutch rotation browser setup successful!")
            print(f"📊 Current IP: {browser.current_ip}")
            print()
            
            # Visit DuckDuckGo first
            print("🦆 Visiting DuckDuckGo...")
            if browser.visit_with_rotation("https://duckduckgo.com"):
                time.sleep(random.uniform(2, 4))
                
                try:
                    # Wait for the page to load and find the search box
                    time.sleep(random.uniform(2, 4))
                    
                    # Try multiple selectors for DuckDuckGo search box
                    search_box = None
                    selectors = ["input[name='q']", "input#search_form_input_homepage", "input#searchbox_input", "[name='q']"]
                    
                    for selector in selectors:
                        try:
                            search_box = browser.driver.find_element(By.CSS_SELECTOR, selector)
                            if search_box.is_displayed() and search_box.is_enabled():
                                break
                        except:
                            continue
                    
                    if not search_box:
                        print("❌ Could not find DuckDuckGo search box")
                        return
                    
                    # Click on the search box to focus it
                    search_box.click()
                    time.sleep(random.uniform(0.5, 1.0))
                    
                    # Clear any existing text and type the search query
                    search_box.clear()
                    time.sleep(random.uniform(0.5, 1.0))
                    
                    # Type the domain with human-like typing
                    search_query = f"site:{domain}"
                    print(f"⌨️  Typing search query: {search_query}")
                    for char in search_query:
                        search_box.send_keys(char)
                        time.sleep(random.uniform(0.05, 0.15))
                    
                    time.sleep(random.uniform(1, 2))
                    
                    # Press Enter to search
                    print("🔍 Submitting search...")
                    search_box.send_keys(Keys.RETURN)
                    
                    # Wait for search results
                    time.sleep(random.uniform(3, 5))
                    
                    # Look for search results and try to click the first relevant one
                    try:
                        # Try to find DuckDuckGo search result links
                        search_results = browser.driver.find_elements(By.CSS_SELECTOR, "h2 a, .result__title a, [data-testid='result-title-a']")
                        
                        if search_results:
                            # Click on the first search result
                            print("🎯 Clicking on first search result...")
                            first_result = search_results[0]
                            
                            # Scroll the element into view
                            browser.driver.execute_script("arguments[0].scrollIntoView(true);", first_result)
                            time.sleep(random.uniform(1, 2))
                            
                            # Click the result
                            first_result.click()
                            
                            # Wait for page to load
                            time.sleep(random.uniform(3, 6))
                            
                            print("✅ Successfully navigated through DuckDuckGo search!")
                            current_url = browser.driver.current_url
                            print(f"📍 Current URL: {current_url}")
                            
                            # Perform human simulation on the target page
                            if browser.config.enable_human_simulation:
                                print("🎭 Performing human simulation...")
                                browser.simulate_mouse_movements()
                                browser.simulate_scrolling_behavior(current_url)
                                browser.find_and_click_interesting_links(current_url)
                            
                            # Stay on page for configured time
                            stay_time = browser.config.page_stay_time_minutes
                            print(f"⏰ Staying on page for {stay_time} minutes...")
                            
                            # Break stay time into smaller chunks for more realistic behavior
                            total_seconds = stay_time * 60
                            chunk_size = 30  # 30 second chunks
                            chunks = int(total_seconds / chunk_size)
                            
                            for i in range(chunks):
                                time.sleep(chunk_size)
                                if i % 4 == 0:  # Every 2 minutes, show progress
                                    remaining_time = (chunks - i - 1) * chunk_size / 60
                                    print(f"⏳ Time remaining: {remaining_time:.1f} minutes")
                                    
                                    # Random small interactions
                                    if random.random() < 0.3:  # 30% chance
                                        if browser.driver:
                                            browser.driver.execute_script("window.scrollBy(0, Math.random() * 200 - 100);")
                            
                            print("✅ Page visit through DuckDuckGo search completed!")
                            
                        else:
                            print("❌ No search results found!")
                            
                    except Exception as e:
                        print(f"❌ Error interacting with search results: {e}")
                        
                except Exception as e:
                    print(f"❌ Error during DuckDuckGo search: {e}")
                    
            else:
                print("❌ Failed to visit DuckDuckGo")
                
        else:
            print("❌ Browser setup failed!")
            
    except Exception as e:
        print(f"❌ Error during DuckDuckGo search visit: {e}")
        
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
        print("4. 🦆 Visit URL through DuckDuckGo Search")
        print("5. ⚙️  Browser Configuration")
        print("6. 📋 Show Current Configuration")
        print("7. 🚪 Exit")
        print()
        
        try:
            choice = input("Select option (1-7): ").strip()
            
            if choice == '1':
                custom_url_test()
            elif choice == '2':
                batch_testing()
            elif choice == '3':
                httpbin_testing()
            elif choice == '4':
                google_search_visit()
            elif choice == '5':
                browser_config()
            elif choice == '6':
                show_current_config()
            elif choice == '7':
                clear_screen()
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please select 1-7.")
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
