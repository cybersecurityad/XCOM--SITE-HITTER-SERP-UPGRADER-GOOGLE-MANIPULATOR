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
    headless=False,
    min_delay=2.0,
    max_delay=5.0,
    rotation_interval=3,
    save_screenshots=True,
    verify_dutch_ip=False,
    user_agent_rotation=True,
    enable_human_simulation=True,
    simulate_mouse_movements=True,
    simulate_scrolling=True,
    simulate_clicking=True,
    page_stay_time_minutes=5.0,
    simulation_repeat_count=1
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
    print("🔍 Will search for keywords and click ONLY exact matching URL results")
    print("🎯 Only clicks if exact URL or URL/* extensions found")
    print("🦆 DuckDuckGo is Tor-friendly and privacy-focused!")
    print()
    
    # Get search keywords first
    search_terms = input("Enter search keywords/terms: ").strip()
    if not search_terms:
        print("❌ No search terms provided!")
        input("\nPress Enter to continue...")
        return
    
    # Get target URL to click on
    target_url = input("Enter target URL to click on: ").strip()
    if not target_url:
        print("❌ No target URL provided!")
        input("\nPress Enter to continue...")
        return
    
    # Add protocol if not present
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url
    
    # Extract domain from target URL for matching
    target_domain = target_url.replace('https://', '').replace('http://', '').split('/')[0]
    
    print(f"🔍 Search terms: {search_terms}")
    print(f"🎯 Target URL: {target_url}")
    print(f"🌐 Looking for domain: {target_domain}")
    print("🦆 Using DuckDuckGo search...")
    
    browser = DutchRotationBrowser(GLOBAL_CONFIG)
    
    try:
        if browser.setup():
            print("✅ Browser setup successful!")
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
                    
                    # Type the search terms with human-like typing
                    print(f"⌨️  Typing search terms: {search_terms}")
                    for char in search_terms:
                        search_box.send_keys(char)
                        time.sleep(random.uniform(0.05, 0.15))
                    
                    time.sleep(random.uniform(1, 2))
                    
                    # Press Enter to search
                    print("🔍 Submitting search...")
                    search_box.send_keys(Keys.RETURN)
                    
                    # Wait for search results
                    time.sleep(random.uniform(3, 5))
                    
                    # Look for search results and try to click the matching one
                    try:
                        # Try to find DuckDuckGo search result links
                        search_results = browser.driver.find_elements(By.CSS_SELECTOR, "h2 a, .result__title a, [data-testid='result-title-a']")
                        
                        if search_results:
                            print(f"🔍 Found {len(search_results)} search results")
                            
                            # Look for a result that matches our exact target URL
                            clicked_result = False
                            for i, result in enumerate(search_results):
                                try:
                                    result_url = result.get_attribute('href')
                                    if result_url:
                                        # Clean up URLs for comparison
                                        clean_result = result_url.replace('https://', '').replace('http://', '').rstrip('/')
                                        clean_target = target_url.replace('https://', '').replace('http://', '').rstrip('/')
                                        
                                        # Check if it's an exact match or URL with extension
                                        is_exact_match = clean_result == clean_target
                                        is_extension_match = clean_result.startswith(clean_target + '/')
                                        
                                        if is_exact_match or is_extension_match:
                                            print(f"🎯 Found exact matching result #{i+1}: {result_url}")
                                            print(f"   Target: {target_url}")
                                            print(f"   Match type: {'Exact' if is_exact_match else 'Extension'}")
                                            
                                            # Click the result directly without scrolling
                                            result.click()
                                            clicked_result = True
                                            break
                                        else:
                                            print(f"   ❌ Result #{i+1}: {result_url} (doesn't match {target_url})")
                                except Exception as e:
                                    continue
                            
                            if not clicked_result:
                                print(f"❌ No result found matching exact URL '{target_url}' or its extensions!")
                                print("🚫 Skipping click - only exact matches allowed")
                                return
                            
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


def website_search_and_click():
    """Visit a website and search for keywords to find and click specific links"""
    clear_screen()
    print("🔍 WEBSITE SEARCH & CLICK")
    print("=" * 50)
    print("🇳🇱 Using Dutch rotation browser with current global configuration")
    print("🌐 Will visit website and search for keywords to find specific links")
    print("🎯 Finds and clicks on matching article/page links")
    print()
    
    # Get target website
    target_website = input("Enter website URL to visit: ").strip()
    if not target_website:
        print("❌ No website URL provided!")
        input("\nPress Enter to continue...")
        return
    
    # Add protocol if not present
    if not target_website.startswith(('http://', 'https://')):
        target_website = 'https://' + target_website
    
    # Get search keywords
    search_keywords = input("Enter keywords to search for on the page: ").strip()
    if not search_keywords:
        print("❌ No search keywords provided!")
        input("\nPress Enter to continue...")
        return
    
    # Get target URL to look for if keywords don't match
    target_url = input("Enter target URL to click (if keywords don't match): ").strip()
    if target_url and not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url
    
    print(f"🌐 Target website: {target_website}")
    print(f"🔍 Search keywords: {search_keywords}")
    if target_url:
        print(f"🎯 Fallback target URL: {target_url}")
    print("🎯 Will search page content for matching links...")
    
    browser = DutchRotationBrowser(GLOBAL_CONFIG)
    
    try:
        if browser.setup():
            print("✅ Browser setup successful!")
            print()
            
            # Visit target website
            print(f"🌐 Visiting {target_website}...")
            if browser.visit_with_rotation(target_website):
                time.sleep(random.uniform(3, 5))
                
                try:
                    # Search for links containing the keywords
                    print(f"🔍 Searching for links containing: {search_keywords}")
                    
                    # Try to find all links on the page
                    all_links = browser.driver.find_elements(By.TAG_NAME, "a")
                    matching_links = []
                    url_matching_links = []
                    
                    # Filter links that contain the search keywords or URL
                    keywords_lower = search_keywords.lower()
                    for link in all_links:
                        try:
                            link_text = link.text.strip()
                            link_href = link.get_attribute('href')
                            
                            if link_text and link_href:
                                # Priority 1: Check if keywords are in the link text
                                if keywords_lower in link_text.lower():
                                    matching_links.append({
                                        'element': link,
                                        'text': link_text,
                                        'href': link_href,
                                        'match_type': 'keyword'
                                    })
                                # Priority 2: Check if target URL matches (if provided)
                                elif target_url and (target_url in link_href or link_href.startswith(target_url)):
                                    url_matching_links.append({
                                        'element': link,
                                        'text': link_text,
                                        'href': link_href,
                                        'match_type': 'url'
                                    })
                        except:
                            continue
                    
                    # Use keyword matches first, then URL matches as fallback
                    if matching_links:
                        selected_links = matching_links
                        print(f"🎯 Found {len(matching_links)} keyword matching links:")
                    elif url_matching_links:
                        selected_links = url_matching_links
                        print(f"🔗 No keyword matches found, using {len(url_matching_links)} URL matching links:")
                    else:
                        selected_links = []
                    
                    if selected_links:
                        print("-" * 60)
                        
                        # Display all matching links
                        for i, link_info in enumerate(selected_links, 1):
                            match_type = "🔍 Keyword" if link_info['match_type'] == 'keyword' else "🔗 URL"
                            print(f"{i}. [{match_type}] {link_info['text']}")
                            print(f"   URL: {link_info['href']}")
                            print()
                        
                        # Automatically click the first matching link
                        selected_link = selected_links[0]
                        match_type_desc = "keyword match" if selected_link['match_type'] == 'keyword' else "URL match"
                        print(f"🎯 Automatically clicking first {match_type_desc}: {selected_link['text']}")
                        print(f"📍 Target URL: {selected_link['href']}")
                        
                        try:
                            # Multiple click strategies for better reliability
                            link_element = selected_link['element']
                            link_url = selected_link['href']
                            
                            print("🎯 Attempting to click link using multiple strategies...")
                            
                            # Strategy 1: Scroll and wait, then normal click
                            try:
                                browser.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", link_element)
                                time.sleep(random.uniform(2, 3))
                                link_element.click()
                                print("✅ Successfully clicked using normal click")
                            except Exception as e1:
                                print(f"⚠️ Normal click failed: {str(e1)[:100]}...")
                                
                                # Strategy 2: JavaScript click
                                try:
                                    browser.driver.execute_script("arguments[0].click();", link_element)
                                    print("✅ Successfully clicked using JavaScript click")
                                except Exception as e2:
                                    print(f"⚠️ JavaScript click failed: {str(e2)[:100]}...")
                                    
                                    # Strategy 3: Navigate directly to URL
                                    try:
                                        print(f"🔗 Navigating directly to: {link_url}")
                                        browser.driver.get(link_url)
                                        print("✅ Successfully navigated directly to URL")
                                    except Exception as e3:
                                        print(f"❌ All click strategies failed: {str(e3)[:100]}...")
                                        raise e3
                            
                            # Wait for page to load
                            time.sleep(random.uniform(3, 6))
                            
                            print("✅ Successfully clicked on the selected link!")
                            current_url = browser.driver.current_url
                            print(f"📍 Current URL: {current_url}")
                            
                            # Perform human simulation on the target page
                            if browser.config.enable_human_simulation:
                                print("🎭 Performing human simulation on target page...")
                                browser.simulate_mouse_movements()
                                browser.simulate_scrolling_behavior(current_url)
                                browser.find_and_click_interesting_links(current_url)
                            
                            # Stay on page for configured time
                            stay_time = browser.config.page_stay_time_minutes
                            print(f"⏰ Staying on page for {stay_time} minutes...")
                            
                            # Break stay time into smaller chunks
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
                            
                            print("✅ Website search and click completed!")
                            
                        except Exception as e:
                            print(f"❌ Error clicking link: {e}")
                            
                    else:
                        if target_url:
                            print(f"❌ No links found containing keywords '{search_keywords}' or matching URL '{target_url}'")
                        else:
                            print(f"❌ No links found containing keywords: {search_keywords}")
                        print("💡 Try different keywords, provide a target URL, or check if the content loaded properly")
                        
                except Exception as e:
                    print(f"❌ Error searching for links: {e}")
                    
            else:
                print("❌ Failed to visit target website")
                
        else:
            print("❌ Browser setup failed!")
            
    except Exception as e:
        print(f"❌ Error during website search and click: {e}")
        
    finally:
        browser.cleanup()
    
    input("\nPress Enter to continue...")


def simple_tor_test():
    """Simple Tor connectivity test"""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    clear_screen()
    print("🧪 SIMPLE TOR CONNECTIVITY TEST")
    print("=" * 40)
    
    chrome_options = Options()
    chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    try:
        print("🔍 Testing basic Tor connection on port 9050...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://httpbin.org/ip")
        time.sleep(2)
        
        ip_info = driver.find_element(By.TAG_NAME, "body").text
        print(f"✅ Tor connection successful!")
        print(f"📍 IP info: {ip_info}")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Tor connectivity failed: {e}")
        print("\n💡 Try these fixes:")
        print("1. brew services restart tor")
        print("2. Check: brew services list | grep tor")
        print("3. View logs: tail /opt/homebrew/var/log/tor.log")
        return False
    
    input("\nPress Enter to continue...")


def reset_tor_connection():
    """Reset Tor connection and restart service safely"""
    clear_screen()
    print("🔄 RESET TOR CONNECTION")
    print("=" * 40)
    print("🔧 Safely resetting Tor service and clearing circuits...")
    
    import subprocess
    
    try:
        # Stop Tor service gracefully first
        print("🛑 Stopping Tor service gracefully...")
        result = subprocess.run(['brew', 'services', 'stop', 'tor'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Tor service stopped gracefully")
        else:
            print(f"⚠️ Tor stop result: {result.stderr}")
        
        time.sleep(3)  # Give it time to stop properly
        
        # Only kill specific tor processes (not all processes containing "tor")
        print("🧹 Cleaning up remaining Tor processes safely...")
        try:
            # More specific process killing - only actual tor daemon
            subprocess.run(['pkill', '-x', 'tor'], capture_output=True, timeout=5)
            subprocess.run(['pkill', '-f', '/opt/homebrew/bin/tor'], capture_output=True, timeout=5)
        except subprocess.TimeoutExpired:
            print("⚠️ Process cleanup timeout - continuing anyway")
        
        time.sleep(2)
        
        # Clear Tor data directory safely
        print("🧹 Clearing Tor data directory...")
        import os
        tor_data_dirs = [
            '/opt/homebrew/var/lib/tor',
            '/usr/local/var/lib/tor'
        ]
        
        for tor_dir in tor_data_dirs:
            if os.path.exists(tor_dir):
                try:
                    print(f"🧹 Clearing: {tor_dir}")
                    # Safer cleanup - only specific files
                    subprocess.run(['find', tor_dir, '-name', 'state', '-delete'], 
                                 capture_output=True, timeout=5)
                    subprocess.run(['find', tor_dir, '-name', 'cached-*', '-delete'], 
                                 capture_output=True, timeout=5)
                    subprocess.run(['find', tor_dir, '-name', 'lock', '-delete'], 
                                 capture_output=True, timeout=5)
                except (subprocess.TimeoutExpired, OSError):
                    print(f"⚠️ Could not clean {tor_dir} - continuing anyway")
        
        # Restart Tor service
        print("🚀 Starting fresh Tor service...")
        result = subprocess.run(['brew', 'services', 'start', 'tor'], 
                              capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            print("✅ Tor service started successfully")
        else:
            print(f"⚠️ Tor start result: {result.stderr}")
        
        # Wait for Tor to bootstrap
        print("⏳ Waiting for Tor to bootstrap (10 seconds)...")
        for i in range(10):
            time.sleep(1)
            if i % 3 == 0:
                print(f"   {10-i} seconds remaining...")
        
        print("🎉 Tor connection reset completed!")
        print("🔄 Fresh circuits and IP address should be available")
        print("💡 Use option 6 to test the new connection")
        
    except subprocess.TimeoutExpired:
        print("⚠️ Operation timed out - Tor reset may be incomplete")
        print("💡 Try running 'brew services restart tor' manually")
    except Exception as e:
        print(f"❌ Error during Tor reset: {e}")
        print("\n💡 Manual reset commands:")
        print("1. brew services restart tor")
        print("2. brew services stop tor && brew services start tor")
    
    input("\nPress Enter to continue...")


def main_menu():
    """Display the main menu and handle user selections"""
    while True:
        show_banner()
        
        print("Main Menu:")
        print("1. 🎯 Custom URL (Full Simulation)")
        print("2. 🦆 Search Keywords & Visit URL through DuckDuckGo")
        print("3. 🔍 Website Search & Click (Find keywords on page)")
        print("4. ⚙️  Browser Configuration")
        print("5. 📋 Show Current Configuration")
        print("6. 🧪 Simple Tor Test")
        print("7. � Reset Tor Connection")
        print("8. �🚪 Exit")
        print()
        
        try:
            choice = input("Select option (1-8): ").strip()
            
            if choice == '1':
                custom_url_test()
            elif choice == '2':
                google_search_visit()
            elif choice == '3':
                website_search_and_click()
            elif choice == '4':
                browser_config()
            elif choice == '5':
                show_current_config()
            elif choice == '6':
                simple_tor_test()
            elif choice == '7':
                reset_tor_connection()
            elif choice == '8':
                clear_screen()
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please select 1-8.")
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
