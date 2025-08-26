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

Advanced Dutch-only Tor Browser with IP rotation and User Agent rotation
for professional SEO enhancement and SERP manipulation activities.
Uses httpbin.org for testing IP and user agent changes.
"""

import random
import time
import json
import os
import sys
import subprocess
import tempfile
import glob
import shutil
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException

@dataclass
class DutchRotationConfig:
    """Configuration for Dutch-only rotating Tor browser with advanced human simulation"""
    # Tor settings
    tor_port: int = 9050
    control_port: int = 9051
    min_delay: float = 3.0
    max_delay: float = 8.0
    headless: bool = False
    save_screenshots: bool = True
    rotation_interval: int = 5  # Rotate IP every N requests
    max_retries: int = 3
    user_agent_rotation: bool = True
    verify_dutch_ip: bool = True
    
    # Dutch-specific settings
    use_dutch_exit_nodes_only: bool = True
    verify_geolocation: bool = True
    
    # Advanced human behavior simulation
    enable_human_simulation: bool = True
    simulate_mouse_movements: bool = True
    simulate_reading_behavior: bool = True
    simulate_scrolling: bool = True
    simulate_clicking: bool = True
    
    # Reading behavior
    min_reading_time: float = 3.0
    max_reading_time: float = 15.0
    reading_speed_wpm: int = 200  # Words per minute
    
    # Mouse and interaction
    mouse_movement_frequency: float = 0.7  # Probability of mouse movements
    click_probability: float = 0.3  # Probability of clicking interesting links
    scroll_frequency: float = 0.8  # How often to scroll
    
    # Behavioral profile
    behavior_profile: str = "balanced"  # balanced, curious, focused, scanner
    
    # Analytics simulation
    simulate_google_analytics: bool = True
    
    # Extended simulation settings
    page_stay_time_minutes: float = 5.0  # How long to stay on each page (10-60 minutes)
    simulation_repeat_count: int = 1  # How many times to repeat simulation (1 = once, 0 = infinite)


class HumanBehaviorEngine:
    """Advanced human behavior simulation engine for Dutch rotation browser"""
    
    def __init__(self, config: DutchRotationConfig):
        self.config = config
        self.behavior_profiles = {
            'balanced': {
                'name': 'Balanced User',
                'read_speed_wpm': 200,
                'attention_span': 180,
                'patience': 1.0,
                'scroll_frequency': 0.7,
                'click_probability': 0.4,
                'interests': ['general', 'news', 'information']
            },
            'curious': {
                'name': 'Curious Explorer',
                'read_speed_wpm': 220,
                'attention_span': 240,
                'patience': 1.2,
                'scroll_frequency': 0.8,
                'click_probability': 0.6,
                'interests': ['tech', 'science', 'innovation', 'research']
            },
            'focused': {
                'name': 'Focused Reader',
                'read_speed_wpm': 180,
                'attention_span': 300,
                'patience': 1.5,
                'scroll_frequency': 0.9,
                'click_probability': 0.8,
                'interests': ['detailed', 'academic', 'thorough', 'analysis']
            },
            'scanner': {
                'name': 'Quick Scanner',
                'read_speed_wpm': 300,
                'attention_span': 90,
                'patience': 0.6,
                'scroll_frequency': 0.9,
                'click_probability': 0.3,
                'interests': ['headlines', 'summary', 'quick', 'overview']
            }
        }
        
        self.current_profile = self.behavior_profiles.get(
            config.behavior_profile, 
            self.behavior_profiles['balanced']
        )
    
    def calculate_reading_time(self, text_length: int) -> float:
        """Calculate realistic reading time based on content and profile"""
        if text_length < 100:
            return random.uniform(2, 5)
        
        # Estimate words (average 5 characters per word)
        words = text_length / 5
        
        # Base reading time in seconds
        base_time = (words / self.current_profile['read_speed_wpm']) * 60
        
        # Add human variability and patience factor
        variability = random.uniform(0.7, 1.3)
        attention_factor = self.current_profile['patience']
        
        total_time = base_time * variability * attention_factor
        
        # Cap at attention span and config limits
        max_time = min(self.current_profile['attention_span'], self.config.max_reading_time)
        min_time = self.config.min_reading_time
        
        return max(min_time, min(total_time, max_time))
    
    def get_scroll_pattern(self) -> str:
        """Get scroll pattern based on profile"""
        if self.current_profile['read_speed_wpm'] > 250:
            return "scan"
        elif self.current_profile['patience'] > 1.2:
            return "detailed"
        else:
            return "natural"


class DutchRotationBrowser:
    """Advanced Dutch-only Tor browser with rotation capabilities and human simulation"""
    
    def __init__(self, config: Optional[DutchRotationConfig] = None):
        self.config = config or DutchRotationConfig()
        self.driver: Optional[webdriver.Chrome] = None
        self.tor_process: Optional[subprocess.Popen] = None
        self.tor_data_dir: Optional[str] = None
        
        # Initialize human behavior engine
        self.behavior_engine = HumanBehaviorEngine(self.config) if self.config.enable_human_simulation else None
        
        self.session_data = {
            'start_time': datetime.now().isoformat(),
            'requests': [],
            'ip_changes': [],
            'user_agents': [],
            'errors': []
        }
        self.request_count = 0
        self.current_ip: Optional[str] = None
        self.current_user_agent: Optional[str] = None
        
        # Dutch user agents
        self.dutch_user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
        ]
    
    def setup(self) -> bool:
        """Initialize the Dutch rotation browser with error recovery"""
        try:
            print("🇳🇱 Setting up Dutch-only Tor browser with rotation...")
            
            # Setup Tor first
            if not self._setup_homebrew_tor():
                print("❌ Failed to setup Tor")
                return False
            
            # Setup browser
            if not self._setup_browser():
                print("❌ Failed to setup browser")
                return False
            
            # Test basic browser functionality
            if not self._test_browser_health():
                print("❌ Browser health check failed")
                return False
            
            # Verify Dutch IP (optional - don't fail if this doesn't work)
            if self.config.verify_dutch_ip:
                if not self._verify_dutch_ip():
                    print("⚠️  Warning: IP verification failed, continuing anyway")
                    # Don't return False here - continue even if IP verification fails
            
            print("✅ Dutch rotation browser setup complete!")
            return True
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False
    
    def _test_browser_health(self) -> bool:
        """Test basic browser functionality"""
        try:
            if not self.driver:
                return False
            
            print("🏥 Testing browser health...")
            
            # Test basic navigation to a simple page
            self.driver.get("data:text/html,<html><body><h1>Test Page</h1></body></html>")
            time.sleep(1)
            
            # Check if we can interact with the page
            title_element = self.driver.find_element(By.TAG_NAME, "h1")
            if title_element.text == "Test Page":
                print("✅ Browser health check passed")
                return True
            else:
                print("❌ Browser health check failed: unexpected content")
                return False
                
        except Exception as e:
            print(f"❌ Browser health check failed: {e}")
            return False
    
    def _setup_homebrew_tor(self) -> bool:
        """Setup Homebrew Tor service with Dutch-only configuration"""
        try:
            print("🍺 Setting up Homebrew Tor service...")
            
            # Stop any existing Tor service
            subprocess.run(['brew', 'services', 'stop', 'tor'], 
                         capture_output=True, text=True)
            time.sleep(2)
            
            # Create custom torrc in user directory
            self.tor_data_dir = tempfile.mkdtemp(prefix="dutch_tor_homebrew_")
            
            torrc_content = f"""
# Dutch-only exit nodes configuration
DataDirectory {self.tor_data_dir}
SocksPort {self.config.tor_port}
ControlPort {self.config.control_port}

# Force Dutch exit nodes only
ExitNodes {{nl}}
StrictNodes 1

# Additional security settings
ExcludeNodes {{??}}
ExcludeExitNodes {{??}}

# Performance settings
CircuitBuildTimeout 30
LearnCircuitBuildTimeout 0
MaxCircuitDirtiness 300

# Logging
Log notice stdout
"""
            
            # Write custom torrc
            torrc_path = os.path.join(self.tor_data_dir, "torrc")
            with open(torrc_path, 'w') as f:
                f.write(torrc_content)
            
            print(f"🔧 Created Dutch-only torrc: {torrc_path}")
            
            # Start Tor with custom config using subprocess
            cmd = ['/opt/homebrew/bin/tor', '-f', torrc_path]
            self.tor_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            print("✅ Started Tor with Dutch-only configuration!")
            
            # Wait for Tor to bootstrap
            print("⏳ Waiting for Tor to bootstrap...")
            time.sleep(8)
            
            # Check if Tor is still running
            if self.tor_process.poll() is not None:
                stdout, stderr = self.tor_process.communicate()
                print(f"❌ Tor failed: {stderr}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup Homebrew Tor: {e}")
            return False
    
    def _start_dutch_tor(self) -> bool:
        """Start Tor with Dutch-only exit nodes"""
        try:
            # Create temporary directory for Tor data
            self.tor_data_dir = tempfile.mkdtemp(prefix="dutch_tor_")
            
            # Create custom torrc for Dutch-only exits
            torrc_content = f"""
# Dutch-only exit nodes configuration
DataDirectory {self.tor_data_dir}
SocksPort {self.config.tor_port}
ControlPort {self.config.control_port}

# Force Dutch exit nodes only
ExitNodes {{nl}}
StrictNodes 1

# Additional security
ExcludeNodes {{??}}
ExcludeExitNodes {{??}}

# Performance settings
CircuitBuildTimeout 30
LearnCircuitBuildTimeout 0
MaxCircuitDirtiness 300

# Logging
Log notice stdout
"""
            
            torrc_path = os.path.join(self.tor_data_dir, "torrc")
            with open(torrc_path, 'w') as f:
                f.write(torrc_content)
            
            print(f"🔧 Starting Dutch-only Tor with config: {torrc_path}")
            
            # Start Tor process
            cmd = ['tor', '-f', torrc_path]
            self.tor_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Wait for Tor to bootstrap
            print("⏳ Waiting for Tor to bootstrap...")
            time.sleep(10)
            
            if self.tor_process.poll() is not None:
                stdout, stderr = self.tor_process.communicate()
                print(f"❌ Tor failed to start: {stderr}")
                return False
            
            print("✅ Dutch-only Tor started successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Dutch Tor: {e}")
            return False
    
    def _setup_browser(self) -> bool:
        """Setup Chrome with Tor proxy and random user agent using standard Selenium"""
        try:
            # Select random user agent
            if self.config.user_agent_rotation:
                self.current_user_agent = random.choice(self.dutch_user_agents)
            else:
                self.current_user_agent = self.dutch_user_agents[0]
            
            print(f"🎭 Using user agent: {self.current_user_agent[:50]}...")
            
            # Chrome options for maximum stability with standard Selenium
            options = Options()
            
            # Tor proxy settings
            options.add_argument(f'--proxy-server=socks5://127.0.0.1:{self.config.tor_port}')
            
            # Stability and stealth options
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-images')
            options.add_argument('--disable-javascript-harmony-shipping')
            options.add_argument('--disable-background-timer-throttling')
            options.add_argument('--disable-renderer-backgrounding')
            options.add_argument('--disable-backgrounding-occluded-windows')
            options.add_argument('--disable-client-side-phishing-detection')
            options.add_argument('--disable-sync')
            options.add_argument('--metrics-recording-only')
            options.add_argument('--no-first-run')
            options.add_argument('--safebrowsing-disable-auto-update')
            options.add_argument('--disable-default-apps')
            options.add_argument('--disable-background-networking')
            options.add_argument('--disable-web-security')
            options.add_argument('--ignore-certificate-errors')
            
            # Anti-detection options for standard Selenium
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # User agent
            options.add_argument(f'--user-agent={self.current_user_agent}')
            
            # Window management
            if not self.config.headless:
                options.add_argument('--start-maximized')
                options.add_argument('--disable-infobars')
            else:
                options.add_argument('--headless=new')
                options.add_argument('--window-size=1920,1080')
            
            # Create driver with standard Selenium
            try:
                self.driver = webdriver.Chrome(options=options)
                print("✅ Chrome driver created successfully")
                
                # Hide webdriver property
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                # Configure timeouts
                self.driver.implicitly_wait(10)
                self.driver.set_page_load_timeout(30)
                
                # Test basic functionality
                user_agent_result = self.driver.execute_script("return navigator.userAgent;")
                print(f"✅ Browser script execution test passed: {user_agent_result[:50]}...")
                
            except Exception as e:
                print(f"❌ Chrome driver creation failed: {e}")
                return False
            
            print("✅ Browser setup complete!")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
    
    def _verify_dutch_ip(self) -> bool:
        """Verify that we're using a Dutch IP"""
        try:
            if not self.driver:
                print("❌ No browser driver available")
                return False
                
            print("🇳🇱 Verifying Dutch IP address...")
            
            # Check if browser is still alive
            try:
                self.driver.current_url
            except Exception as e:
                print(f"❌ Browser window closed during verification: {e}")
                return False
            
            # Get IP info from httpbin with retry logic
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    print(f"🔄 IP verification attempt {attempt + 1}/{max_attempts}")
                    self.driver.get("http://httpbin.org/ip")
                    
                    # Wait for page to load
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    
                    # Extract IP
                    body_text = self.driver.find_element(By.TAG_NAME, "body").text
                    ip_data = json.loads(body_text)
                    self.current_ip = ip_data.get('origin', 'Unknown')
                    
                    print(f"🌐 Current IP: {self.current_ip}")
                    break
                    
                except Exception as e:
                    print(f"⚠️ IP verification attempt {attempt + 1} failed: {e}")
                    if attempt < max_attempts - 1:
                        time.sleep(2)
                    else:
                        print("❌ All IP verification attempts failed")
                        return False
            
            # Check geolocation with retry logic
            for attempt in range(max_attempts):
                try:
                    print(f"🔄 Geolocation check attempt {attempt + 1}/{max_attempts}")
                    self.driver.get("http://ip-api.com/json/")
                    
                    # Wait for page to load
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    
                    geo_text = self.driver.find_element(By.TAG_NAME, "body").text
                    geo_data = json.loads(geo_text)
                    
                    country = geo_data.get('country', 'Unknown')
                    country_code = geo_data.get('countryCode', 'Unknown')
                    city = geo_data.get('city', 'Unknown')
                    
                    print(f"🗺️  Location: {city}, {country} ({country_code})")
                    break
                    
                except Exception as e:
                    print(f"⚠️ Geolocation check attempt {attempt + 1} failed: {e}")
                    if attempt < max_attempts - 1:
                        time.sleep(2)
                    else:
                        print("⚠️ Geolocation check failed, continuing anyway")
                        break
            
            # Record IP change
            self.session_data['ip_changes'].append({
                'timestamp': datetime.now().isoformat(),
                'ip': self.current_ip,
                'country': country,
                'country_code': country_code,
                'city': city
            })
            
            is_dutch = country_code.lower() == 'nl'
            if is_dutch:
                print("✅ Confirmed: Using Dutch IP address!")
            else:
                print(f"⚠️  Warning: IP appears to be from {country}, not Netherlands")
            
            return is_dutch
            
        except Exception as e:
            print(f"❌ IP verification failed: {e}")
            return False
    
    def rotate_identity(self) -> bool:
        """Rotate Tor identity and user agent"""
        try:
            print("🔄 Rotating identity...")
            
            # Close current browser
            if self.driver:
                self.driver.quit()
                time.sleep(2)
            
            # Stop current Tor and restart with new circuit
            if self.tor_process:
                self.tor_process.terminate()
                self.tor_process.wait()
                time.sleep(3)
            
            # Start new Tor session
            if not self._setup_homebrew_tor():
                return False
            
            time.sleep(5)
            
            # Setup new browser with new user agent
            if not self._setup_browser():
                return False
            
            # Verify new IP
            if self.config.verify_dutch_ip:
                self._verify_dutch_ip()
            
            print("✅ Identity rotation complete!")
            return True
            
        except Exception as e:
            print(f"❌ Identity rotation failed: {e}")
            return False
    
    def simulate_human_reading(self, content_length: int) -> float:
        """Simulate realistic human reading behavior"""
        if not self.behavior_engine or not self.config.simulate_reading_behavior:
            return 0
        
        reading_time = self.behavior_engine.calculate_reading_time(content_length)
        print(f"📖 Simulating reading for {reading_time:.1f} seconds...")
        time.sleep(reading_time)
        return reading_time
    
    def simulate_mouse_movements(self):
        """Simulate realistic mouse movements with safe bounds"""
        if (not self.behavior_engine or 
            not self.config.simulate_mouse_movements or 
            not self.driver or
            random.random() > self.config.mouse_movement_frequency):
            return
        
        try:
            # Get window size to calculate safe bounds
            window_size = self.driver.get_window_size()
            window_width = window_size['width']
            window_height = window_size['height']
            
            # Calculate safe movement area (leave margins)
            safe_margin = 50
            max_x = window_width - safe_margin
            max_y = window_height - safe_margin
            min_x = safe_margin
            min_y = safe_margin
            
            actions = ActionChains(self.driver)
            
            # 3-7 random mouse movements within safe bounds
            num_movements = random.randint(3, 7)
            print(f"🖱️ Simulating {num_movements} mouse movements...")
            
            # Start from center
            center_x = window_width // 2
            center_y = window_height // 2
            current_x = center_x
            current_y = center_y
            
            for i in range(num_movements):
                # Calculate safe offset that won't go out of bounds
                max_x_offset = min(50, max_x - current_x, current_x - min_x)
                max_y_offset = min(50, max_y - current_y, current_y - min_y)
                
                if max_x_offset > 0 and max_y_offset > 0:
                    x_offset = random.randint(-max_x_offset, max_x_offset)
                    y_offset = random.randint(-max_y_offset, max_y_offset)
                    
                    # Update current position
                    current_x += x_offset
                    current_y += y_offset
                    
                    # Ensure we stay within bounds
                    current_x = max(min_x, min(current_x, max_x))
                    current_y = max(min_y, min(current_y, max_y))
                    
                    actions.move_by_offset(x_offset, y_offset)
                    actions.pause(random.uniform(0.1, 0.5))
            
            actions.perform()
            
        except Exception as e:
            print(f"⚠️ Mouse movement simulation failed: {e}")
    
    def simulate_scrolling_behavior(self, url: str):
        """Simulate realistic scrolling behavior"""
        if (not self.behavior_engine or 
            not self.config.simulate_scrolling or 
            not self.driver or
            random.random() > self.config.scroll_frequency):
            return
        
        try:
            # Get page height
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            if page_height < 1000:
                print("📄 Short page - minimal scrolling")
                time.sleep(random.uniform(1, 3))
                return
            
            # Get scroll pattern from behavior engine
            pattern = self.behavior_engine.get_scroll_pattern()
            print(f"📜 Simulating {pattern} scrolling behavior...")
            
            if pattern == "natural":
                # Natural reading scroll
                segments = random.randint(4, 8)
                for i in range(segments):
                    scroll_amount = random.randint(150, 350)
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    time.sleep(random.uniform(0.8, 2.5))
                    
            elif pattern == "scan":
                # Quick scanning pattern
                positions = [page_height // 4, page_height // 2, page_height * 3 // 4, page_height]
                for position in positions:
                    self.driver.execute_script(f"window.scrollTo({{top: {position}, behavior: 'smooth'}});")
                    time.sleep(random.uniform(0.5, 1.5))
                    
            elif pattern == "detailed":
                # Detailed reading with occasional back-scrolling
                for i in range(random.randint(6, 10)):
                    # Forward scroll
                    self.driver.execute_script("window.scrollBy(0, 100);")
                    time.sleep(random.uniform(1.0, 2.5))
                    
                    # Occasional back-scroll (realistic reading regression)
                    if random.random() < 0.3:
                        self.driver.execute_script("window.scrollBy(0, -30);")
                        time.sleep(random.uniform(0.5, 1.0))
            
        except Exception as e:
            print(f"⚠️ Scrolling simulation failed: {e}")
    
    def find_and_click_interesting_links(self, url: str):
        """Find and potentially click interesting links based on behavior profile"""
        if (not self.behavior_engine or 
            not self.config.simulate_clicking or 
            not self.driver or
            random.random() > self.config.click_probability):
            return
        
        try:
            # Find links
            link_elements = self.driver.find_elements(By.TAG_NAME, "a")
            clickable_links = []
            
            for element in link_elements[:15]:  # Check first 15 links
                try:
                    href = element.get_attribute('href')
                    text = element.text.strip()
                    
                    if href and text and len(text) > 3:
                        clickable_links.append({
                            'element': element,
                            'text': text,
                            'href': href
                        })
                except:
                    continue
            
            if not clickable_links:
                return
            
            # Find links matching interests
            interests = self.behavior_engine.current_profile['interests']
            interesting_links = []
            
            for link in clickable_links:
                text_lower = link['text'].lower()
                if any(interest in text_lower for interest in interests):
                    interesting_links.append(link)
            
            # Click an interesting link
            if interesting_links:
                selected_link = random.choice(interesting_links)
                try:
                    print(f"🖱️ Clicking interesting link: {selected_link['text'][:50]}...")
                    
                    # Scroll to element first
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", selected_link['element'])
                    time.sleep(random.uniform(0.5, 1.5))
                    
                    # Click with human-like timing
                    ActionChains(self.driver).move_to_element(selected_link['element']).pause(
                        random.uniform(0.5, 1.5)
                    ).click().perform()
                    
                    time.sleep(random.uniform(2, 4))  # Wait for page load
                    print(f"✅ Successfully clicked link")
                    
                except Exception as e:
                    print(f"⚠️ Link clicking failed: {e}")
            
        except Exception as e:
            print(f"⚠️ Link analysis failed: {e}")
    
    def simulate_google_analytics_events(self):
        """Simulate Google Analytics events for realistic tracking"""
        if not self.config.simulate_google_analytics or not self.driver:
            return
        
        try:
            # Simulate GA4 events
            self.driver.execute_script("""
                // Simulate Google Analytics pageview
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'page_view', {
                        'page_title': document.title,
                        'page_location': window.location.href
                    });
                    
                    gtag('event', 'scroll', {
                        'event_category': 'engagement',
                        'event_label': 'page_scroll'
                    });
                    
                    gtag('event', 'timing_complete', {
                        'name': 'page_read_time',
                        'value': Math.floor(Math.random() * 180 + 30)
                    });
                }
            """)
            print(f"📊 Simulated Google Analytics events")
            
        except Exception as e:
            print(f"⚠️ GA simulation failed: {e}")

    def visit_with_rotation(self, url: str) -> bool:
        """Visit URL with automatic rotation and browser recovery"""
        try:
            # Check if rotation is needed
            if (self.request_count > 0 and 
                self.request_count % self.config.rotation_interval == 0):
                print(f"🔄 Auto-rotating after {self.request_count} requests...")
                if not self.rotate_identity():
                    print("⚠️  Rotation failed, attempting browser recovery...")
                    if not self._recover_browser():
                        print("❌ Browser recovery failed")
                        return False
            
            # Attempt to visit URL with retries
            for attempt in range(self.config.max_retries):
                if attempt > 0:
                    print(f"🔄 Retry attempt {attempt + 1}/{self.config.max_retries}")
                    
                    # Try to recover browser if previous attempt failed
                    if not self._check_browser_alive():
                        print("🏥 Browser appears dead, attempting recovery...")
                        if not self._recover_browser():
                            print("❌ Browser recovery failed")
                            continue
                
                if self._visit_url(url):
                    self.request_count += 1
                    return True
                
                # If visit failed, wait before retry
                if attempt < self.config.max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    print(f"⏳ Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
            
            print(f"❌ All {self.config.max_retries} attempts failed for {url}")
            return False
            
        except Exception as e:
            print(f"❌ Visit with rotation failed: {e}")
            return False
    
    def _visit_url(self, url: str) -> bool:
        """Visit a single URL with comprehensive human behavior simulation"""
        try:
            if not self.driver:
                print("❌ No browser driver available")
                return False
            
            # Check if browser window is still alive
            try:
                current_url = self.driver.current_url
            except Exception as e:
                print(f"❌ Browser window closed: {e}")
                return False
                
            start_time = time.time()
            print(f"🌐 Visiting: {url}")
            
            # Pre-navigation delay (human hesitation)
            pre_delay = random.uniform(0.5, 2.0)
            time.sleep(pre_delay)
            
            # Navigate with error handling
            try:
                self.driver.get(url)
                
                # Wait for page load with explicit wait
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
            except TimeoutException:
                print(f"⏰ Timeout waiting for {url} to load")
                return False
            except Exception as e:
                print(f"❌ Navigation failed: {e}")
                return False
            
            # Additional wait for dynamic content
            time.sleep(random.uniform(1, 3))
            
            # Human behavior simulation
            if self.behavior_engine and self.config.enable_human_simulation:
                print(f"🎭 Simulating human behavior (Profile: {self.behavior_engine.current_profile['name']})...")
                
                # 1. Get page content for reading time calculation
                try:
                    page_text = self.driver.find_element(By.TAG_NAME, "body").text
                    content_length = len(page_text)
                except:
                    content_length = 1000  # Default assumption
                
                # 2. Simulate initial page scan (quick scroll)
                if self.config.simulate_scrolling:
                    print(f"👁️ Initial page scan...")
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(random.uniform(1, 2))
                    self.driver.execute_script("window.scrollTo(0, 0);")
                
                # 3. Simulate human reading
                reading_time = self.simulate_human_reading(content_length)
                
                # 4. Simulate scrolling behavior during "reading"
                self.simulate_scrolling_behavior(url)
                
                # 5. Simulate mouse movements
                self.simulate_mouse_movements()
                
                # 6. Maybe click interesting links
                self.find_and_click_interesting_links(url)
                
                # 7. Simulate Google Analytics events
                self.simulate_google_analytics_events()
            
            else:
                # Standard delay without simulation
                delay = random.uniform(self.config.min_delay, self.config.max_delay)
                time.sleep(delay)
            
            # Take screenshot if enabled
            if self.config.save_screenshots:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"dutch_rotation_{timestamp}.png"
                self.driver.save_screenshot(screenshot_path)
                print(f"📸 Screenshot saved: {screenshot_path}")
            
            # Record request with simulation data
            self.request_count += 1
            user_agent_display = self.current_user_agent[:100] if self.current_user_agent else "Unknown"
            
            request_data = {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'duration': time.time() - start_time,
                'ip': self.current_ip,
                'user_agent': user_agent_display,
                'request_number': self.request_count
            }
            
            # Add simulation data if enabled
            if self.behavior_engine and self.config.enable_human_simulation:
                request_data['simulation'] = {
                    'profile': self.behavior_engine.current_profile['name'],
                    'reading_time': reading_time if 'reading_time' in locals() else 0,
                    'content_length': content_length if 'content_length' in locals() else 0,
                    'human_behaviors': {
                        'scrolling': self.config.simulate_scrolling,
                        'mouse_movements': self.config.simulate_mouse_movements,
                        'link_clicking': self.config.simulate_clicking,
                        'ga_events': self.config.simulate_google_analytics
                    }
                }
            
            self.session_data['requests'].append(request_data)
            
            print(f"✅ Successfully visited {url} (Request #{self.request_count})")
            if self.behavior_engine:
                print(f"🎭 Human simulation complete with {self.behavior_engine.current_profile['name']} profile")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to visit {url}: {e}")
            self.session_data['errors'].append({
                'url': url,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return False
    
    def test_httpbin_features(self):
        """Test various httpbin endpoints to verify rotation"""
        print("🧪 Testing httpbin features with rotation...")
        
        test_urls = [
            "http://httpbin.org/ip",
            "http://httpbin.org/user-agent",
            "http://httpbin.org/headers",
            "http://httpbin.org/get",
            "http://httpbin.org/anything",
            "http://httpbin.org/status/200",
            "http://httpbin.org/delay/2",
            "http://httpbin.org/cache/60"
        ]
        
        for i, url in enumerate(test_urls):
            print(f"\n--- Test {i+1}/{len(test_urls)} ---")
            self.visit_with_rotation(url)
            
            # Show current status
            print(f"📊 Current IP: {self.current_ip}")
            ua_display = self.current_user_agent[:50] if self.current_user_agent else "Unknown"
            print(f"🎭 Current UA: {ua_display}...")
            print(f"📈 Total requests: {self.request_count}")
    
    def save_session_data(self):
        """Save session data to JSON file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dutch_rotation_session_{timestamp}.json"
            
            self.session_data['end_time'] = datetime.now().isoformat()
            self.session_data['total_requests'] = self.request_count
            self.session_data['total_ip_changes'] = len(self.session_data['ip_changes'])
            
            with open(filename, 'w') as f:
                json.dump(self.session_data, f, indent=2)
            
            print(f"💾 Session data saved: {filename}")
            
        except Exception as e:
            print(f"❌ Failed to save session data: {e}")
    
    def _check_browser_alive(self) -> bool:
        """Check if the browser is still responsive"""
        try:
            if not self.driver:
                return False
            
            # Try to get current URL
            current_url = self.driver.current_url
            
            # Try to execute a simple script
            result = self.driver.execute_script("return document.readyState;")
            
            return True
            
        except Exception:
            return False
    
    def _recover_browser(self) -> bool:
        """Attempt to recover a dead browser"""
        try:
            print("🔧 Attempting browser recovery...")
            
            # Close existing browser if possible
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
            
            # Wait a moment
            time.sleep(3)
            
            # Recreate browser
            if self._setup_browser():
                print("✅ Browser recovery successful")
                return True
            else:
                print("❌ Browser recovery failed")
                return False
                
        except Exception as e:
            print(f"❌ Browser recovery error: {e}")
            return False

    def cleanup(self):
        """Clean up resources"""
        try:
            print("🧹 Cleaning up Dutch rotation browser...")
            
            # Save session data
            self.save_session_data()
            
            # Close browser
            if self.driver:
                self.driver.quit()
                time.sleep(2)
            
            # Stop Tor process
            if self.tor_process:
                self.tor_process.terminate()
                self.tor_process.wait()
                print("🛑 Stopped Tor process")
            
            # Clean up Tor data directory
            if self.tor_data_dir and os.path.exists(self.tor_data_dir):
                shutil.rmtree(self.tor_data_dir)
                print("🧹 Cleaned up Tor data directory")
            
            print("✅ Cleanup complete!")
            
        except Exception as e:
            print(f"❌ Cleanup error: {e}")

def main():
    """Main demo function"""
    print("🇳🇱 Dutch Rotation Browser Demo")
    print("=" * 40)
    
    # Configure for rotation testing
    config = DutchRotationConfig(
        rotation_interval=3,  # Rotate every 3 requests
        user_agent_rotation=True,
        verify_dutch_ip=True,
        save_screenshots=True
    )
    
    browser = DutchRotationBrowser(config)
    
    try:
        if browser.setup():
            # Test httpbin features with rotation
            browser.test_httpbin_features()
            
            # Additional custom tests
            print("\n🎯 Testing custom URLs...")
            custom_urls = [
                "https://www.nu.nl/",
                "http://httpbin.org/json",
                "https://www.nos.nl/"
            ]
            
            for url in custom_urls:
                browser.visit_with_rotation(url)
        
    except KeyboardInterrupt:
        print("\n⏸️  Test interrupted by user")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    finally:
        browser.cleanup()

if __name__ == "__main__":
    main()
