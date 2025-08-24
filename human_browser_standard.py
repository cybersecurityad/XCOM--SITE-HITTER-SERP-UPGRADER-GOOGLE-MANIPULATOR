#!/usr/bin/env python3
"""
Alternative Human Browser using standard Selenium WebDriver
Compatible with Python 3.13+
"""

import time
import random
import os
from typing import List, Optional
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent


@dataclass
class BrowsingConfig:
    """Configuration for human-like browsing behavior"""
    min_scroll_delay: float = 1.0
    max_scroll_delay: float = 3.0
    min_click_delay: float = 0.5
    max_click_delay: float = 2.0
    scroll_pause_time: float = 2.0
    page_load_timeout: int = 30
    use_proxy: bool = False
    proxy_list: Optional[List[str]] = None


class StandardHumanBrowser:
    """Human-like browsing using standard Selenium WebDriver"""
    
    def __init__(self, config: BrowsingConfig = None):
        self.config = config or BrowsingConfig()
        self.driver = None
        self.user_agent = UserAgent()
        
    def setup_driver(self, headless: bool = False) -> webdriver.Chrome:
        """Setup Chrome driver with stealth configurations"""
        options = Options()
        
        if headless:
            options.add_argument('--headless')
            
        # Stealth settings
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Random user agent
        user_agent = self.user_agent.random
        options.add_argument(f'--user-agent={user_agent}')
        
        # Additional stealth options
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins-discovery')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        
        # Proxy configuration
        if self.config.use_proxy and self.config.proxy_list:
            proxy = random.choice(self.config.proxy_list)
            options.add_argument(f'--proxy-server={proxy}')
            
        # Try to find Chrome executable
        chrome_paths = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS
            '/usr/bin/google-chrome',  # Linux
            '/usr/bin/chromium-browser',  # Linux alternative
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',  # Windows
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                options.binary_location = path
                break
                
        self.driver = webdriver.Chrome(options=options)
        
        # Execute script to hide webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return self.driver
    
    def human_scroll(self, element=None):
        """Simulate human-like scrolling behavior"""
        if not self.driver:
            raise ValueError("Driver not initialized")
            
        # Random scroll amount and direction
        scroll_amount = random.randint(100, 500)
        direction = random.choice(['down', 'up'])
        
        if direction == 'down':
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        else:
            self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")
            
        # Random pause
        delay = random.uniform(self.config.min_scroll_delay, self.config.max_scroll_delay)
        time.sleep(delay)
    
    def human_click(self, element):
        """Simulate human-like clicking with mouse movement"""
        if not self.driver:
            raise ValueError("Driver not initialized")
            
        try:
            # Move to element with human-like curve
            actions = ActionChains(self.driver)
            
            # Add some randomness to the click position
            x_offset = random.randint(-5, 5)
            y_offset = random.randint(-5, 5)
            
            actions.move_to_element_with_offset(element, x_offset, y_offset)
            actions.pause(random.uniform(0.1, 0.3))
            actions.click()
            actions.perform()
            
            # Random delay after click
            delay = random.uniform(self.config.min_click_delay, self.config.max_click_delay)
            time.sleep(delay)
        except Exception as e:
            print(f"Error clicking element: {e}")
    
    def simulate_reading(self, min_time: float = 2.0, max_time: float = 10.0):
        """Simulate human reading time on a page"""
        reading_time = random.uniform(min_time, max_time)
        time.sleep(reading_time)
    
    def random_mouse_movement(self):
        """Add random mouse movements to appear more human"""
        if not self.driver:
            return
            
        try:
            actions = ActionChains(self.driver)
            
            # Random movements
            for _ in range(random.randint(1, 3)):
                x = random.randint(50, 400)
                y = random.randint(50, 300)
                actions.move_by_offset(x, y)
                actions.pause(random.uniform(0.1, 0.5))
                
            actions.perform()
        except Exception as e:
            print(f"Error with mouse movement: {e}")
    
    def browse_page(self, url: str, actions: List[str] = None):
        """Browse a page with human-like behavior"""
        if not self.driver:
            self.setup_driver()
            
        actions = actions or ['scroll', 'read', 'scroll']
        
        try:
            print(f"Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page load
            WebDriverWait(self.driver, self.config.page_load_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Perform human-like actions
            for action in actions:
                if action == 'scroll':
                    self.human_scroll()
                elif action == 'read':
                    self.simulate_reading()
                elif action == 'click_random':
                    self._click_random_link()
                elif action == 'mouse_movement':
                    self.random_mouse_movement()
                    
        except Exception as e:
            print(f"Error browsing page: {e}")
    
    def _click_random_link(self):
        """Click a random safe element on the page"""
        try:
            # Find safe clickable elements (avoid forms and dangerous buttons)
            safe_selectors = [
                "a[href^='#']",  # Internal links
                "a[href^='/']",  # Relative links
                "button[type='button']",  # Safe buttons
            ]
            
            for selector in safe_selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                visible_elements = [
                    elem for elem in elements 
                    if elem.is_displayed() and elem.is_enabled()
                ]
                
                if visible_elements:
                    element = random.choice(visible_elements)
                    self.human_click(element)
                    return
                    
        except Exception as e:
            print(f"Error clicking random element: {e}")
    
    def close(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()


def main():
    """Example usage"""
    config = BrowsingConfig(
        min_scroll_delay=1.0,
        max_scroll_delay=2.5,
        use_proxy=False
    )
    
    browser = StandardHumanBrowser(config)
    
    try:
        test_urls = [
            "https://httpbin.org/get",
            "https://quotes.toscrape.com"
        ]
        
        for url in test_urls:
            actions = ['read', 'scroll', 'mouse_movement', 'scroll', 'read']
            browser.browse_page(url, actions)
            time.sleep(random.uniform(3, 8))
            
    finally:
        browser.close()


if __name__ == "__main__":
    main()
