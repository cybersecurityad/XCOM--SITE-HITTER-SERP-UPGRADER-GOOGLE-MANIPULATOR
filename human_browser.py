#!/usr/bin/env python3
"""
Advanced Cybersecurity Web Automation Tool with Homebrew Tor Integration
======================================================================

Comprehensive human-like browsing behavior simulator for security testing
using stable Homebrew Tor service with advanced features:
- Zero exit code 15 errors (Homebrew Tor approach)  
- Advanced proxy rotation
- Human-like behavior simulation
- Comprehensive logging integration
- Stealth browsing capabilities
"""

import time
import random
import asyncio
import subprocess
import socket
import signal
import sys
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from contextlib import closing
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
import logging


@dataclass
class AdvancedBrowsingConfig:
    """Advanced configuration for human-like browsing behavior with Homebrew Tor support"""
    # Basic timing settings
    min_scroll_delay: float = 1.0
    max_scroll_delay: float = 3.0
    min_click_delay: float = 0.5
    max_click_delay: float = 2.0
    scroll_pause_time: float = 2.0
    page_load_timeout: int = 30
    implicit_wait: int = 10
    
    # Tor configuration (Homebrew approach)
    use_tor: bool = True
    tor_port: int = 9050
    auto_start_tor: bool = True
    verify_tor_ip: bool = True
    
    # Proxy settings (for non-Tor scenarios)
    use_external_proxy: bool = False
    proxy_list: Optional[List[str]] = field(default_factory=list)
    proxy_rotation_interval: int = 5
    
    # User agent and stealth settings
    use_realistic_user_agents: bool = True
    use_mobile_agents: bool = False
    rotate_user_agents: bool = True
    
    # Advanced behavior simulation
    simulate_reading_time: bool = True
    min_reading_time: float = 2.0
    max_reading_time: float = 8.0
    simulate_mouse_movements: bool = True
    random_scroll_patterns: bool = True
    
    # Error handling and retry settings
    max_retries: int = 3
    retry_delay: float = 2.0
    auto_recover: bool = True
    
    # Logging and monitoring
    enable_logging: bool = True
    log_level: str = "INFO"
    save_screenshots: bool = False
    
    # Browser options
    headless: bool = False
    window_size: tuple = (1920, 1080)
    disable_images: bool = False
    disable_javascript: bool = False


class AdvancedHumanBehaviorSimulator:
    """Advanced human behavior simulation with full Homebrew Tor integration"""
    
    def __init__(self, config: Optional[AdvancedBrowsingConfig] = None):
        self.config = config or AdvancedBrowsingConfig()
        self.driver = None
        self.user_agent = UserAgent()
        self.current_proxy = None
        self.request_count = 0
        self.tor_running = False
        self.session_data = {
            'start_time': time.time(),
            'requests_made': 0,
            'errors_encountered': 0,
            'tor_ip': None
        }
        
        # Setup logging if enabled
        if self.config.enable_logging:
            self.setup_logging()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info("🚀 Advanced Human Behavior Simulator initialized")
    
    def setup_logging(self):
        """Setup logging system"""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(getattr(logging, self.config.log_level))
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.warning(f"Signal {signum} received - shutting down...")
        self.cleanup()
        sys.exit(0)
    
    # ===== HOMEBREW TOR INTEGRATION =====
    
    def check_homebrew_tor(self) -> bool:
        """Check if Homebrew Tor service is running"""
        try:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                sock.settimeout(5)
                result = sock.connect_ex(('127.0.0.1', self.config.tor_port))
                if result == 0:
                    self.tor_running = True
                    self.logger.info("✅ Homebrew Tor service detected")
                    return True
                return False
        except Exception as e:
            self.logger.error(f"❌ Error checking Tor service: {e}")
            return False
    
    def start_homebrew_tor(self) -> bool:
        """Start Homebrew Tor service if needed"""
        if self.check_homebrew_tor():
            return True
            
        self.logger.info("🔄 Starting Homebrew Tor service...")
        try:
            result = subprocess.run(['brew', 'services', 'start', 'tor'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                self.logger.info("✅ Homebrew Tor service started")
                time.sleep(3)  # Give Tor time to start
                return self.check_homebrew_tor()
            else:
                self.logger.error(f"❌ Failed to start Tor: {result.stderr}")
                return False
        except Exception as e:
            self.logger.error(f"❌ Error starting Tor: {e}")
            return False
    
    def get_tor_ip(self) -> Optional[str]:
        """Get current Tor IP address and verify connectivity"""
        if not self.tor_running:
            return None
            
        proxies = {
            'http': f'socks5://127.0.0.1:{self.config.tor_port}',
            'https': f'socks5://127.0.0.1:{self.config.tor_port}'
        }
        
        try:
            response = requests.get('https://httpbin.org/ip', 
                                  proxies=proxies, timeout=15)
            tor_ip = response.json()['origin']
            self.session_data['tor_ip'] = tor_ip
            self.logger.info(f"✅ Tor IP verified: {tor_ip}")
            return tor_ip
        except Exception as e:
            self.logger.error(f"❌ Error getting Tor IP: {e}")
            return None
    
    def new_tor_identity(self) -> bool:
        """Request new Tor identity (circuit refresh)"""
        try:
            # Method 1: Use Tor control protocol (if available)
            import stem.control
            with stem.control.Controller.from_port(port=9051) as controller:
                controller.authenticate()
                controller.signal(stem.Signal.NEWNYM)
                self.logger.info("✅ New Tor identity requested")
                time.sleep(5)  # Wait for new circuit
                return True
        except ImportError:
            self.logger.warning("⚠️  stem library not available for Tor control")
        except Exception as e:
            self.logger.warning(f"⚠️  Tor control failed: {e}")
        
        # Method 2: Restart Tor service (fallback)
        try:
            subprocess.run(['brew', 'services', 'restart', 'tor'], 
                         capture_output=True, timeout=30)
            time.sleep(5)
            if self.check_homebrew_tor():
                self.logger.info("✅ Tor service restarted for new identity")
                return True
        except Exception as e:
            self.logger.error(f"❌ Failed to restart Tor: {e}")
        
        return False
    
    # ===== BROWSER MANAGEMENT =====
    
    def get_user_agent(self) -> str:
        """Get appropriate user agent based on configuration"""
        if not hasattr(self, 'logger'):
            self.setup_logging()
            
        try:
            if self.config.use_mobile_agents:
                # Mobile user agents
                mobile_agents = [
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
                    'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0',
                    'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
                ]
                return random.choice(mobile_agents)
            elif self.config.use_realistic_user_agents:
                # Desktop user agents
                desktop_agents = [
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ]
                return random.choice(desktop_agents)
            else:
                return self.user_agent.random
        except Exception:
            # Fallback user agent
            return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    def get_proxy_settings(self) -> Optional[str]:
        """Get proxy settings based on configuration"""
        # Priority 1: Tor proxy (if enabled and running)
        if self.config.use_tor and self.tor_running:
            return f'socks5://127.0.0.1:{self.config.tor_port}'
        
        # Priority 2: External proxy rotation
        if self.config.use_external_proxy and self.config.proxy_list:
            # Simple round-robin proxy selection
            proxy_index = self.request_count % len(self.config.proxy_list)
            return self.config.proxy_list[proxy_index]
        
        return None
        
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
