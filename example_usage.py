"""
Example script demonstrating ethical security testing
"""

import os
import sys
import time
import random
import logging
from human_browser import HumanBehaviorSimulator, BrowsingConfig
from proxy_manager import ProxyRotator, ProxyConfig, get_random_user_agent

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
    Example of ethical security testing workflow
    
    IMPORTANT: Only use on systems you own or have explicit permission to test!
    """
    
    # Test URLs (replace with your authorized targets)
    test_urls = [
        "https://httpbin.org/get",  # Public testing API
        "https://quotes.toscrape.com",  # Public scraping practice site
        # Add your authorized test targets here
    ]
    
    # Configuration for human-like behavior
    config = BrowsingConfig(
        min_scroll_delay=2.0,
        max_scroll_delay=4.0,
        min_click_delay=1.0,
        max_click_delay=3.0,
        use_proxy=False  # Set to True if you have proxy servers
    )
    
    simulator = HumanBehaviorSimulator(config)
    
    try:
        logger.info("Starting ethical security testing session")
        
        for i, url in enumerate(test_urls):
            logger.info(f"Testing target {i+1}/{len(test_urls)}: {url}")
            
            # Define realistic browsing actions
            actions = [
                'read',           # Simulate reading content
                'scroll',         # Scroll down the page
                'mouse_movement', # Random mouse movements
                'scroll',         # More scrolling
                'read',           # More reading time
                'click_random'    # Click on random elements (be careful!)
            ]
            
            # Browse the page with human-like behavior
            simulator.browse_page(url, actions)
            
            # Random delay between targets
            delay = random.uniform(10, 30)  # 10-30 second delay
            time.sleep(delay)
            logger.info(f"Waiting {delay:.1f} seconds before next target")
            
    except KeyboardInterrupt:
        logger.info("Testing interrupted by user")
    except Exception as e:
        logger.error(f"Error during testing: {e}")
    finally:
        simulator.close()
        logger.info("Security testing session completed")


def proxy_rotation_example():
    """
    Example of using proxy rotation for enhanced anonymity
    """
    
    # Example proxy configuration (replace with your proxies)
    proxy_list = [
        # "http://proxy1.example.com:8080",
        # "http://proxy2.example.com:8080",
        # Add your proxy servers here
    ]
    
    if not proxy_list:
        logger.warning("No proxies configured. Skipping proxy rotation example.")
        return
    
    proxy_config = ProxyConfig(
        proxy_list=proxy_list,
        rotation_interval=3,  # Rotate every 3 requests
        timeout=10
    )
    
    rotator = ProxyRotator(proxy_config)
    
    # Use with browser automation
    browser_config = BrowsingConfig(
        use_proxy=True,
        proxy_list=rotator.working_proxies
    )
    
    simulator = HumanBehaviorSimulator(browser_config)
    
    try:
        # Test with proxy rotation
        test_url = "https://httpbin.org/ip"  # Shows your IP address
        
        for i in range(5):
            logger.info(f"Request {i+1} using proxy: {rotator.get_current_proxy()}")
            simulator.browse_page(test_url, ['read'])
            
            if rotator.should_rotate():
                rotator.rotate_proxy()
                
    finally:
        simulator.close()


if __name__ == "__main__":
    print("Cybersecurity Web Automation Tool")
    print("=" * 40)
    print("IMPORTANT: Only use on authorized targets!")
    print("=" * 40)
    
    choice = input("Choose test type:\n1. Basic ethical testing\n2. Proxy rotation example\n> ")
    
    if choice == "1":
        ethical_security_test()
    elif choice == "2":
        proxy_rotation_example()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)
