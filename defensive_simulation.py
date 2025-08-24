#!/usr/bin/env python3
"""
🛡️ DEFENSIVE WEB TRAFFIC SIMULATOR
===================================
Simulates various attack patterns and malicious traffic to test website defenses.
Protects your real IP using multiple anonymization layers.

DEFENSIVE USE CASES:
- Test rate limiting effectiveness
- Validate bot detection systems
- Assess DDoS mitigation capabilities
- Verify geographic blocking
- Test security monitoring alerts

ANONYMIZATION LAYERS:
- Rotating proxy chains
- User agent randomization
- Behavioral pattern variation
- Traffic timing obfuscation
"""

import random
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import requests
from dataclasses import dataclass
from typing import List, Dict, Optional, Union
import json
import logging
from datetime import datetime, timedelta

@dataclass
class AttackPattern:
    """Defines different attack simulation patterns"""
    name: str
    requests_per_minute: int
    concurrent_browsers: int
    page_dwell_time: tuple  # (min, max) seconds
    scroll_behavior: str  # 'aggressive', 'normal', 'none'
    click_probability: float  # 0.0 to 1.0
    form_interaction: bool
    repeat_visits: int
    geographic_spread: bool

class DefensiveSimulator:
    """
    🛡️ Defensive Traffic Simulator
    
    Simulates various malicious traffic patterns to test website defenses
    while protecting your real IP through multiple anonymization layers.
    """
    
    def __init__(self, target_url: str, proxy_list: Optional[List[str]] = None):
        self.target_url = target_url
        self.proxy_list = proxy_list or []
        self.ua = UserAgent()
        self.active_browsers = []
        self.session_logs = []
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('defensive_simulation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Predefined attack patterns
        self.attack_patterns = {
            'bot_crawler': AttackPattern(
                name='Bot Crawler Simulation',
                requests_per_minute=60,
                concurrent_browsers=3,
                page_dwell_time=(0.5, 2.0),
                scroll_behavior='none',
                click_probability=0.1,
                form_interaction=False,
                repeat_visits=5,
                geographic_spread=True
            ),
            'ddos_simulation': AttackPattern(
                name='DDoS Traffic Simulation',
                requests_per_minute=300,
                concurrent_browsers=10,
                page_dwell_time=(0.1, 0.5),
                scroll_behavior='none',
                click_probability=0.0,
                form_interaction=False,
                repeat_visits=20,
                geographic_spread=True
            ),
            'scraper_bot': AttackPattern(
                name='Data Scraper Simulation',
                requests_per_minute=120,
                concurrent_browsers=5,
                page_dwell_time=(1.0, 3.0),
                scroll_behavior='aggressive',
                click_probability=0.3,
                form_interaction=True,
                repeat_visits=10,
                geographic_spread=False
            ),
            'click_fraud': AttackPattern(
                name='Click Fraud Simulation',
                requests_per_minute=45,
                concurrent_browsers=2,
                page_dwell_time=(2.0, 8.0),
                scroll_behavior='normal',
                click_probability=0.8,
                form_interaction=True,
                repeat_visits=3,
                geographic_spread=True
            ),
            'reconnaissance': AttackPattern(
                name='Reconnaissance Simulation',
                requests_per_minute=20,
                concurrent_browsers=1,
                page_dwell_time=(5.0, 15.0),
                scroll_behavior='normal',
                click_probability=0.5,
                form_interaction=True,
                repeat_visits=1,
                geographic_spread=False
            )
        }
    
    def get_stealth_browser(self, proxy: Optional[str] = None) -> Optional[webdriver.Chrome]:
        """Create a stealth browser with anonymization features"""
        options = uc.ChromeOptions()
        
        # Anonymization options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Randomize window size
        width = random.randint(1024, 1920)
        height = random.randint(768, 1080)
        options.add_argument(f'--window-size={width},{height}')
        
        # Randomize user agent
        user_agent = self.ua.random
        options.add_argument(f'--user-agent={user_agent}')
        
        # Proxy configuration (CRITICAL for IP hiding)
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
            self.logger.info(f"🔒 Using proxy: {proxy}")
        
        # Additional stealth options
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')  # Faster loading
        options.add_argument('--disable-javascript')  # Avoid detection scripts
        
        try:
            driver = uc.Chrome(options=options)
            
            # Execute stealth scripts
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
            
            return driver
        except Exception as e:
            self.logger.error(f"❌ Failed to create stealth browser: {e}")
            return None
    
    def simulate_human_behavior(self, driver: webdriver.Chrome, pattern: AttackPattern):
        """Simulate human-like or bot-like behavior based on pattern"""
        try:
            # Navigate to target
            self.logger.info(f"🎯 Accessing target: {self.target_url}")
            driver.get(self.target_url)
            
            # Wait for page load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Simulate dwell time
            dwell_time = random.uniform(*pattern.page_dwell_time)
            self.logger.info(f"⏱️ Dwelling for {dwell_time:.1f} seconds")
            
            # Simulate scrolling behavior
            if pattern.scroll_behavior == 'aggressive':
                self.aggressive_scroll(driver)
            elif pattern.scroll_behavior == 'normal':
                self.normal_scroll(driver)
            
            # Random clicking
            if random.random() < pattern.click_probability:
                self.random_click(driver)
            
            # Form interaction
            if pattern.form_interaction:
                self.interact_with_forms(driver)
            
            # Final dwell
            time.sleep(dwell_time)
            
        except Exception as e:
            self.logger.error(f"❌ Behavior simulation error: {e}")
    
    def aggressive_scroll(self, driver: webdriver.Chrome):
        """Simulate aggressive bot-like scrolling"""
        for _ in range(random.randint(5, 15)):
            scroll_amount = random.randint(100, 500)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.1, 0.3))
    
    def normal_scroll(self, driver: webdriver.Chrome):
        """Simulate normal human scrolling"""
        for _ in range(random.randint(2, 6)):
            scroll_amount = random.randint(200, 800)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 2.0))
    
    def random_click(self, driver: webdriver.Chrome):
        """Simulate random clicking on elements"""
        try:
            clickable_elements = driver.find_elements(By.CSS_SELECTOR, 
                "a, button, input[type='submit'], input[type='button']")
            
            if clickable_elements:
                element = random.choice(clickable_elements)
                if element.is_displayed() and element.is_enabled():
                    self.logger.info("🖱️ Performing random click")
                    element.click()
                    time.sleep(random.uniform(1, 3))
        except Exception as e:
            self.logger.warning(f"⚠️ Click simulation failed: {e}")
    
    def interact_with_forms(self, driver: webdriver.Chrome):
        """Simulate form interactions"""
        try:
            forms = driver.find_elements(By.TAG_NAME, "form")
            if forms:
                form = random.choice(forms)
                inputs = form.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='email'], textarea")
                
                for input_field in inputs[:random.randint(1, 3)]:
                    if input_field.is_displayed() and input_field.is_enabled():
                        fake_data = self.generate_fake_data(input_field.get_attribute('type') or 'text')
                        input_field.clear()
                        input_field.send_keys(fake_data)
                        time.sleep(random.uniform(0.5, 1.5))
                        
                self.logger.info("📝 Simulated form interaction")
        except Exception as e:
            self.logger.warning(f"⚠️ Form interaction failed: {e}")
    
    def generate_fake_data(self, field_type: str) -> str:
        """Generate fake data for form fields"""
        fake_data = {
            'text': ['test', 'sample', 'demo', 'user123', 'example'],
            'email': ['test@example.com', 'demo@test.org', 'sample@fake.net'],
            'default': ['testing', 'simulation', 'defensive']
        }
        return random.choice(fake_data.get(field_type, fake_data['default']))
    
    def run_attack_simulation(self, pattern_name: str, duration_minutes: int = 10):
        """
        🚨 Run a specific attack pattern simulation
        
        Args:
            pattern_name: Name of attack pattern to simulate
            duration_minutes: How long to run the simulation
        """
        if pattern_name not in self.attack_patterns:
            self.logger.error(f"❌ Unknown attack pattern: {pattern_name}")
            return
        
        pattern = self.attack_patterns[pattern_name]
        end_time = datetime.now() + timedelta(minutes=duration_minutes)
        
        self.logger.info(f"🚨 STARTING DEFENSIVE SIMULATION: {pattern.name}")
        self.logger.info(f"⏰ Duration: {duration_minutes} minutes")
        self.logger.info(f"🎯 Target: {self.target_url}")
        self.logger.info(f"🔄 Requests per minute: {pattern.requests_per_minute}")
        self.logger.info(f"👥 Concurrent browsers: {pattern.concurrent_browsers}")
        
        # Calculate timing
        requests_per_second = pattern.requests_per_minute / 60
        delay_between_requests = 1 / requests_per_second if requests_per_second > 0 else 1
        
        # Start concurrent browser threads
        threads = []
        for i in range(pattern.concurrent_browsers):
            proxy = random.choice(self.proxy_list) if self.proxy_list else None
            thread = threading.Thread(
                target=self.browser_worker,
                args=(pattern, end_time, delay_between_requests, proxy, i)
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        self.logger.info(f"✅ SIMULATION COMPLETE: {pattern.name}")
        self.generate_simulation_report(pattern_name, duration_minutes)
    
    def browser_worker(self, pattern: AttackPattern, end_time: datetime, 
                      delay: float, proxy: str, worker_id: int):
        """Worker function for concurrent browser automation"""
        driver = None
        try:
            driver = self.get_stealth_browser(proxy)
            if not driver:
                self.logger.error(f"❌ Worker {worker_id}: Failed to create browser")
                return
            
            self.logger.info(f"🟢 Worker {worker_id}: Started with proxy {proxy}")
            
            request_count = 0
            while datetime.now() < end_time:
                try:
                    # Simulate the behavior
                    self.simulate_human_behavior(driver, pattern)
                    request_count += 1
                    
                    self.logger.info(f"Worker {worker_id}: Request #{request_count}")
                    
                    # Repeat visits if configured
                    for _ in range(pattern.repeat_visits - 1):
                        if datetime.now() >= end_time:
                            break
                        time.sleep(delay)
                        self.simulate_human_behavior(driver, pattern)
                        request_count += 1
                    
                    # Wait before next cycle
                    time.sleep(delay)
                    
                except Exception as e:
                    self.logger.error(f"❌ Worker {worker_id} error: {e}")
                    time.sleep(5)  # Brief pause on error
                    
        finally:
            if driver:
                driver.quit()
                self.logger.info(f"🔴 Worker {worker_id}: Stopped")
    
    def generate_simulation_report(self, pattern_name: str, duration: int):
        """Generate a report of the simulation"""
        report = {
            'simulation': pattern_name,
            'duration_minutes': duration,
            'target_url': self.target_url,
            'timestamp': datetime.now().isoformat(),
            'proxy_count': len(self.proxy_list),
            'pattern_details': self.attack_patterns[pattern_name].__dict__
        }
        
        with open(f'simulation_report_{pattern_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"📊 Simulation report saved")

def main():
    """Example usage of the defensive simulator"""
    
    # Configuration
    TARGET_URL = "https://example.com"  # Replace with your test target
    
    # Add your anonymization proxies here (CRITICAL for IP protection)
    PROXY_LIST = [
        # "http://user:pass@proxy1.com:8080",
        # "http://user:pass@proxy2.com:8080",
        # "socks5://user:pass@proxy3.com:1080",
    ]
    
    if not PROXY_LIST:
        print("⚠️ WARNING: No proxies configured!")
        print("Your real IP will be exposed to the target website.")
        print("Add proxies to PROXY_LIST for IP protection.")
        
        response = input("Continue without IP protection? (y/N): ")
        if response.lower() != 'y':
            print("Exiting. Configure proxies first.")
            return
    
    # Create simulator
    simulator = DefensiveSimulator(TARGET_URL, PROXY_LIST)
    
    print("\n🛡️ DEFENSIVE TRAFFIC SIMULATION PATTERNS:")
    print("1. bot_crawler - Simulate automated crawling")
    print("2. ddos_simulation - High-volume traffic test")
    print("3. scraper_bot - Data extraction simulation")
    print("4. click_fraud - Click fraud detection test")
    print("5. reconnaissance - Information gathering test")
    
    pattern = input("\nSelect pattern (1-5): ").strip()
    duration = int(input("Duration in minutes (default 5): ") or "5")
    
    pattern_map = {
        "1": "bot_crawler",
        "2": "ddos_simulation", 
        "3": "scraper_bot",
        "4": "click_fraud",
        "5": "reconnaissance"
    }
    
    if pattern in pattern_map:
        print(f"\n🚨 Starting {pattern_map[pattern]} simulation...")
        print("🔒 Your IP will be protected through proxy rotation")
        print("📊 Check the log files for detailed results")
        
        simulator.run_attack_simulation(pattern_map[pattern], duration)
    else:
        print("❌ Invalid selection")

if __name__ == "__main__":
    main()
