#!/usr/bin/env python3
"""
Cybersecurity Web Automation Tool
Human-like browsing behavior simulator for security testing
"""

import time
import random
import asyncio
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
import undetected_chromedriver as uc
import requests
import json
from advanced_rotation import AdvancedProxyRotator, RotationConfig, UserAgentManager


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
    # Advanced rotation features
    use_advanced_rotation: bool = False
    rotation_interval: int = 5
    rotation_strategy: str = 'random'  # round_robin, random, weighted
    use_realistic_user_agents: bool = True
    use_mobile_agents: bool = False


class HumanBehaviorSimulator:
    """Simulates human-like web browsing behavior"""
    
    def __init__(self, config: BrowsingConfig = None):
        self.config = config or BrowsingConfig()
        self.driver = None
        self.user_agent = UserAgent()
        
        # Initialize advanced rotation if enabled
        if self.config.use_advanced_rotation:
            rotation_config = RotationConfig(
                user_agent_rotation=self.config.use_realistic_user_agents,
                proxy_rotation=self.config.use_proxy,
                rotation_interval=self.config.rotation_interval,
                rotation_strategy=self.config.rotation_strategy
            )
            self.proxy_rotator = AdvancedProxyRotator(rotation_config)
            self.user_agent_manager = UserAgentManager()
            
            # Add proxies if provided
            if self.config.proxy_list:
                self.proxy_rotator.add_proxy_list(self.config.proxy_list)
                self.proxy_rotator.validate_proxies()
        else:
            self.proxy_rotator = None
            self.user_agent_manager = None
        
    def setup_driver(self, headless: bool = False) -> webdriver.Chrome:
        """Setup Chrome driver with human-like configurations"""
        options = uc.ChromeOptions()
        
        if headless:
            options.add_argument('--headless')
            
        # Human-like browser settings
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins-discovery')
        # Use add_argument instead of add_experimental_option for better compatibility
        options.add_argument('--disable-automation')
        options.add_argument('--disable-infobars')
        
        # Get user agent - use advanced rotation if available
        if self.user_agent_manager:
            if self.config.use_mobile_agents:
                user_agent = self.user_agent_manager.get_mobile_user_agent()
            else:
                user_agent = self.user_agent_manager.get_realistic_user_agent()
        else:
            user_agent = self.user_agent.random
            
        options.add_argument(f'--user-agent={user_agent}')
        
        # Get proxy - use advanced rotation if available
        current_proxy = None
        if self.proxy_rotator and self.proxy_rotator.proxies:
            if self.proxy_rotator.should_rotate():
                current_proxy = self.proxy_rotator.get_next_proxy()
            else:
                current_proxy = self.proxy_rotator.get_current_proxy()
                
            if current_proxy:
                options.add_argument(f'--proxy-server={current_proxy.url}')
                print(f"🔄 Using proxy: {current_proxy.host}:{current_proxy.port}")
        elif self.config.use_proxy and self.config.proxy_list:
            # Fallback to simple proxy rotation
            proxy = random.choice(self.config.proxy_list)
            options.add_argument(f'--proxy-server={proxy}')
            
        print(f"🎭 Using User-Agent: {user_agent[:60]}...")
            
        self.driver = uc.Chrome(options=options)
        
        # Execute script to hide webdriver property (more compatible approach)
        try:
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.driver.execute_script("window.chrome = { runtime: {} }")
        except Exception as e:
            print(f"Warning: Could not execute stealth scripts: {e}")
        
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
            
            # Get window size to avoid out-of-bounds movements
            window_size = self.driver.get_window_size()
            max_x = min(window_size['width'] - 100, 800)
            max_y = min(window_size['height'] - 100, 600)
            
            # Random movements within safe bounds
            for _ in range(random.randint(1, 2)):
                x = random.randint(50, max_x)
                y = random.randint(50, max_y)
                actions.move_by_offset(x - 400, y - 300)  # Relative movement
                actions.pause(random.uniform(0.1, 0.5))
                
            actions.perform()
        except Exception as e:
            print(f"Mouse movement skipped: {e}")
    
    def browse_page(self, url: str, actions: List[str] = None):
        """
        Browse a page with human-like behavior
        
        Args:
            url: URL to visit
            actions: List of actions to perform ['scroll', 'click_random', 'read']
        """
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
        """Click a random clickable element on the page"""
        try:
            # Find clickable elements
            clickable_elements = self.driver.find_elements(
                By.CSS_SELECTOR, 
                "a, button, input[type='submit'], input[type='button']"
            )
            
            if clickable_elements:
                # Filter out hidden elements
                visible_elements = [
                    elem for elem in clickable_elements 
                    if elem.is_displayed() and elem.is_enabled()
                ]
                
                if visible_elements:
                    element = random.choice(visible_elements)
                    self.human_click(element)
                    
        except Exception as e:
            print(f"Error clicking random element: {e}")
    
    def close(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()


def main():
    """Example usage of the human behavior simulator"""
    config = BrowsingConfig(
        min_scroll_delay=1.0,
        max_scroll_delay=2.5,
        use_proxy=False  # Set to True and provide proxy list for proxy rotation
    )
    
    simulator = HumanBehaviorSimulator(config)
    
    try:
        # Example websites for testing (use only for legitimate security testing)
        test_urls = [
            "https://example.com",
            "https://httpbin.org",
            "https://quotes.toscrape.com"
        ]
        
        for url in test_urls:
            actions = ['read', 'scroll', 'mouse_movement', 'scroll', 'read']
            simulator.browse_page(url, actions)
            
            # Random delay between pages
            time.sleep(random.uniform(3, 8))
            
    finally:
        simulator.close()


if __name__ == "__main__":
    main()
