#!/usr/bin/env python3
"""
Test verenigdamsterdam.nl with Full Human Simulation
==================================================

Advanced Tor browser test with comprehensive human behavior simulation.
"""

from simple_advanced_tor_browser import SimpleAdvancedTorBrowser, SimpleTorConfig
import time
import random


def test_verenigdamsterdam():
    """Test verenigdamsterdam.nl with full simulation"""
    print("🚀 TESTING VERENIGDAMSTERDAM.NL WITH FULL SIMULATION")
    print("=" * 60)
    
    # Enhanced configuration for full simulation
    config = SimpleTorConfig(
        auto_start_tor=True,
        verify_tor_ip=True,
        save_screenshots=True,
        simulate_mouse_movements=True,
        extract_data=True,
        min_delay=3.0,  # Longer reading times
        max_delay=8.0,
        page_load_timeout=45,
        implicit_wait=15
    )
    
    # Create browser
    browser = SimpleAdvancedTorBrowser(config)
    
    try:
        # Setup
        if not browser.setup():
            print("❌ Setup failed!")
            return
        
        # Target URL
        url = "https://verenigdamsterdam.nl"
        
        print(f"\n🎯 TARGET: {url}")
        print("🧠 FULL HUMAN SIMULATION MODE")
        print("-" * 40)
        
        # Pre-visit thinking time
        thinking_time = random.uniform(2, 5)
        print(f"🤔 Thinking before visit: {thinking_time:.1f}s")
        time.sleep(thinking_time)
        
        # Comprehensive visit with detailed simulation
        results = browser.comprehensive_page_visit(url)
        
        if results['success']:
            print(f"\n✅ VISIT SUCCESSFUL!")
            print(f"📊 Page Data: {results.get('page_data', {})}")
            
            # Additional human-like interactions
            print("\n🖱️  PERFORMING ADDITIONAL INTERACTIONS...")
            
            # Extended scrolling with pauses
            print("📜 Extended scrolling simulation...")
            for scroll_session in range(3):
                print(f"   Scroll session {scroll_session + 1}/3")
                browser.scroll_page()
                
                # Pause as if reading content
                read_time = random.uniform(5, 12)
                print(f"   📖 Reading content: {read_time:.1f}s")
                time.sleep(read_time)
            
            # Simulate looking for specific content
            print("🔍 Simulating content exploration...")
            try:
                if browser.driver:
                    # Look for navigation links
                    nav_links = browser.driver.find_elements("css selector", "nav a, header a, .menu a")
                    if nav_links:
                        print(f"   Found {len(nav_links)} navigation links")
                        
                        # Hover over some links (human behavior)
                        from selenium.webdriver.common.action_chains import ActionChains
                        actions = ActionChains(browser.driver)
                        
                        for i in range(min(3, len(nav_links))):
                            try:
                                link = nav_links[i]
                                actions.move_to_element(link).perform()
                                hover_time = random.uniform(0.5, 2.0)
                                print(f"   🎯 Hovering over link {i+1}: {hover_time:.1f}s")
                                time.sleep(hover_time)
                            except:
                                pass
                    
                    # Look for main content areas
                    content_areas = browser.driver.find_elements("css selector", "main, article, .content, #content")
                    if content_areas:
                        print(f"   Found {len(content_areas)} main content areas")
                    
                    # Check for images
                    images = browser.driver.find_elements("tag name", "img")
                    if images:
                        print(f"   Found {len(images)} images on page")
                        
                        # Simulate viewing some images
                        for i in range(min(2, len(images))):
                            try:
                                img = images[i]
                                browser.driver.execute_script("arguments[0].scrollIntoView();", img)
                                view_time = random.uniform(1, 3)
                                print(f"   🖼️  Viewing image {i+1}: {view_time:.1f}s")
                                time.sleep(view_time)
                            except:
                                pass
                
            except Exception as e:
                print(f"   ⚠️  Content exploration error: {e}")
            
            # Final screenshot
            timestamp = int(time.time())
            browser.save_screenshot(f"verenigdamsterdam_final_{timestamp}.png")
            
            # Simulate decision-making pause
            decision_time = random.uniform(3, 8)
            print(f"🤔 Decision-making pause: {decision_time:.1f}s")
            time.sleep(decision_time)
            
        else:
            print(f"❌ VISIT FAILED: {results.get('error', 'Unknown error')}")
        
        print("\n✅ FULL SIMULATION COMPLETED!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        browser.cleanup()


if __name__ == "__main__":
    test_verenigdamsterdam()
