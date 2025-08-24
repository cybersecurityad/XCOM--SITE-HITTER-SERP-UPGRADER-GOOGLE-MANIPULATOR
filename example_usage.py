"""
Main Homebrew Tor Browser Example - Clean & Simple Implementation
===============================================================

Example script demonstrating ethical security testing with the stable Homebrew Tor approach.
Uses the main_tor_browser module for reliable, exit-code-15-free operation.
"""

import os
import sys
import time
import random
import logging
from main_tor_browser import MainTorBrowser, TorBrowserConfig

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


"""
Main Homebrew Tor Browser Example - Clean & Simple Implementation
===============================================================

Example script demonstrating ethical security testing with the stable Homebrew Tor approach.
Uses the main_tor_browser module for reliable, exit-code-15-free operation.
"""

import os
import sys
import time
import random
import logging
from main_tor_browser import MainTorBrowser, TorBrowserConfig

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def ethical_security_test():
    """
    Example of ethical security testing workflow using main Tor browser
    
    IMPORTANT: Only use on systems you own or have explicit permission to test!
    """
    
    # Test URLs (replace with your authorized targets)
    test_urls = [
        "https://httpbin.org/ip",       # Check IP address through Tor
        "https://httpbin.org/headers",  # Check headers
        "https://httpbin.org/user-agent", # Check user agent
        "https://check.torproject.org", # Tor Project's official checker
    ]
    
    # Configure browser
    config = TorBrowserConfig(
        auto_start_tor=True,
        page_load_timeout=30,
        min_delay=2.0,
        max_delay=5.0
    )
    
    browser = MainTorBrowser(config)
    
    try:
        logger.info("🚀 Starting ethical security testing session")
        
        # Setup browser and Tor
        if not browser.setup():
            logger.error("❌ Browser setup failed")
            return False
        
        logger.info(f"✅ Testing {len(test_urls)} targets with Tor")
        
        for i, url in enumerate(test_urls):
            logger.info(f"🔍 Testing target {i+1}/{len(test_urls)}: {url}")
            
            # Navigate to URL
            if browser.navigate(url):
                # Get page information
                info = browser.get_page_info()
                logger.info(f"📄 Page: {info.get('title', 'No title')} ({info.get('page_source_length', 0)} chars)")
                
                # Simulate human behavior
                browser.scroll_page(random.randint(2, 4))
                
                # Random delay between targets
                if i < len(test_urls) - 1:
                    delay = random.uniform(3, 8)
                    logger.info(f"⏰ Waiting {delay:.1f} seconds...")
                    time.sleep(delay)
            else:
                logger.warning(f"⚠️  Failed to test: {url}")
        
        logger.info("✅ Security testing completed successfully")
        return True
        
    except KeyboardInterrupt:
        logger.info("⚠️  Testing interrupted by user")
        return False
    except Exception as e:
        logger.error(f"❌ Error during testing: {e}")
        return False
    finally:
        browser.cleanup()


def tor_connectivity_test():
    """Simple test to verify Tor connectivity"""
    logger.info("🔄 Running Tor connectivity test...")
    
    config = TorBrowserConfig(auto_start_tor=True)
    browser = MainTorBrowser(config)
    
    try:
        success = browser.setup() and browser.test_connectivity()
        if success:
            logger.info("🎉 Tor connectivity test passed!")
        else:
            logger.error("❌ Tor connectivity test failed!")
        return success
    except Exception as e:
        logger.error(f"❌ Connectivity test error: {e}")
        return False
    finally:
        browser.cleanup()


def interactive_tor_session():
    """Interactive session for manual testing"""
    logger.info("🔄 Starting interactive Tor session...")
    
    config = TorBrowserConfig(auto_start_tor=True)
    browser = MainTorBrowser(config)
    
    try:
        # Setup browser
        if not browser.setup():
            logger.error("❌ Cannot start interactive session")
            return False
        
        logger.info("✅ Interactive Tor session ready!")
        logger.info("🌐 Browser is running with Tor proxy")
        logger.info("💡 Navigate to websites for testing")
        logger.info("🔍 Try: https://check.torproject.org")
        logger.info("⚠️  Press Ctrl+C to exit")
        
        # Navigate to Tor checker page
        browser.navigate("https://check.torproject.org")
        
        # Keep session alive
        try:
            while True:
                time.sleep(10)
                # Check if browser is still alive
                try:
                    if browser.driver:
                        browser.driver.current_url
                except:
                    logger.warning("⚠️  Browser session ended")
                    break
        except KeyboardInterrupt:
            logger.info("⚠️  Interactive session ended by user")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Interactive session error: {e}")
        return False
    finally:
        browser.cleanup()


def custom_browsing_demo():
    """Demonstrate custom browsing patterns"""
    logger.info("🔄 Running custom browsing demo...")
    
    # Custom configuration
    config = TorBrowserConfig(
        auto_start_tor=True,
        min_delay=1.0,
        max_delay=3.0,
        page_load_timeout=45
    )
    
    browser = MainTorBrowser(config)
    
    try:
        if not browser.setup():
            logger.error("❌ Setup failed")
            return False
        
        # Demo URLs with different content types
        demo_urls = [
            "https://httpbin.org/json",
            "https://httpbin.org/html",
            "https://httpbin.org/xml"
        ]
        
        for url in demo_urls:
            logger.info(f"🔍 Demo browsing: {url}")
            
            if browser.navigate(url):
                # Different scrolling patterns
                browser.scroll_page(random.randint(1, 3))
                
                # Simulate reading time
                reading_time = random.uniform(2, 6)
                logger.info(f"📖 Simulating reading for {reading_time:.1f}s")
                time.sleep(reading_time)
        
        logger.info("✅ Custom browsing demo completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Demo error: {e}")
        return False
    finally:
        browser.cleanup()


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 MAIN TOR BROWSER - EXAMPLE USAGE")
    print("=" * 60)
    print("IMPORTANT: Only use on authorized targets!")
    print("=" * 60)
    
    print("\nAvailable options:")
    print("1. Ethical security testing (automated)")
    print("2. Tor connectivity test")
    print("3. Interactive Tor session (manual)")
    print("4. Custom browsing demo")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nChoose option (1-5): ").strip()
            
            if choice == "1":
                print("\n🔄 Starting ethical security testing...")
                success = ethical_security_test()
                if success:
                    print("✅ Testing completed successfully!")
                else:
                    print("❌ Testing failed!")
                    
            elif choice == "2":
                print("\n🔄 Running Tor connectivity test...")
                success = tor_connectivity_test()
                
            elif choice == "3":
                print("\n🔄 Starting interactive session...")
                success = interactive_tor_session()
                
            elif choice == "4":
                print("\n🔄 Running custom browsing demo...")
                success = custom_browsing_demo()
                
            elif choice == "5":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            break
