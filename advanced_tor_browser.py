#!/usr/bin/env python3
"""
Advanced Tor Browser - Full-Featured Implementation with Homebrew Tor
==================================================================

Complete browser automation with all advanced features:
- Stable Homebrew Tor integration (no exit code 15 errors)
- Advanced human behavior simulation  
- Comprehensive logging and monitoring
- Proxy rotation and stealth capabilities
- Security testing features
- Full workspace integration
"""

import time
import random
import subprocess
import socket
import signal
import sys
import json
import os
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from contextlib import closing
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import requests
import logging
from auto_logger_init_v2 import initialize_all_loggers


@dataclass
class AdvancedTorConfig:
    """Advanced configuration for comprehensive Tor browser automation"""
    # Tor settings
    tor_port: int = 9050
    auto_start_tor: bool = True
    verify_tor_ip: bool = True
    request_new_identity_interval: int = 10  # requests before new identity
    
    # Browser settings
    page_load_timeout: int = 45
    implicit_wait: int = 15
    window_size: tuple = (1920, 1080)
    headless: bool = False
    
    # Human behavior simulation
    min_delay: float = 1.0
    max_delay: float = 4.0
    min_reading_time: float = 3.0
    max_reading_time: float = 10.0
    simulate_mouse_movements: bool = True
    random_scroll_patterns: bool = True
    
    # Advanced features
    save_screenshots: bool = False
    save_page_source: bool = False
    extract_forms: bool = True
    extract_links: bool = True
    
    # User agent rotation
    rotate_user_agents: bool = True
    use_mobile_agents: bool = False
    
    # Proxy settings (for non-Tor scenarios)
    external_proxy_list: List[str] = field(default_factory=list)
    proxy_rotation_enabled: bool = False
    
    # Logging and monitoring
    enable_comprehensive_logging: bool = True
    log_level: str = "INFO"
    session_log_file: str = "advanced_tor_session.log"
    
    # Security testing features
    check_tor_detection: bool = True
    analyze_security_headers: bool = True
    detect_waf: bool = True


class AdvancedTorBrowser:
    """Complete advanced Tor browser with all features"""
    
    def __init__(self, config: Optional[AdvancedTorConfig] = None):
        self.config = config or AdvancedTorConfig()
        self.driver: Optional[uc.Chrome] = None
        self.tor_running = False
        self.session_data = {
            'start_time': time.time(),
            'requests_made': 0,
            'errors_encountered': 0,
            'tor_ip': None,
            'identity_changes': 0,
            'pages_visited': [],
            'screenshots_taken': 0
        }
        
        # User agents for rotation
        self.desktop_user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        
        self.mobile_user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 13; Mobile; rv:68.0) Gecko/68.0 Firefox/110.0',
            'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        ]
        
        # Minimal logging setup - disable comprehensive logging
        self.setup_logging()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def setup_logging(self):
        """Setup comprehensive logging system"""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(getattr(logging, self.config.log_level))
        
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
            
            # File handler
            file_handler = logging.FileHandler(self.config.session_log_file)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.warning(f"Signal {signum} received - shutting down...")
        self.cleanup()
        sys.exit(0)
    
    # ===== TOR MANAGEMENT =====
    
    def check_homebrew_tor(self) -> bool:
        """Check if Homebrew Tor service is running"""
        try:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                sock.settimeout(5)
                result = sock.connect_ex(('127.0.0.1', self.config.tor_port))
                if result == 0:
                    self.tor_running = True
                    self.logger.info("✅ Homebrew Tor service detected and accessible")
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
                self.logger.info("✅ Homebrew Tor service started successfully")
                time.sleep(5)  # Give Tor time to start
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
    
    def request_new_tor_identity(self) -> bool:
        """Request new Tor identity for enhanced privacy"""
        try:
            # Method 1: Try Tor control protocol
            try:
                import stem.control
                with stem.control.Controller.from_port(port=9051) as controller:
                    controller.authenticate()
                    controller.signal(stem.Signal.NEWNYM)
                    self.logger.info("✅ New Tor identity requested via control protocol")
                    self.session_data['identity_changes'] += 1
                    time.sleep(5)  # Wait for new circuit
                    return True
            except ImportError:
                self.logger.debug("stem library not available")
            except Exception as e:
                self.logger.debug(f"Tor control failed: {e}")
            
            # Method 2: Restart Tor service (fallback)
            self.logger.info("🔄 Requesting new Tor identity via service restart...")
            result = subprocess.run(['brew', 'services', 'restart', 'tor'], 
                                  capture_output=True, timeout=30)
            if result.returncode == 0:
                time.sleep(5)
                if self.check_homebrew_tor():
                    self.session_data['identity_changes'] += 1
                    self.logger.info("✅ New Tor identity obtained via service restart")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get new Tor identity: {e}")
            return False
    
    # ===== BROWSER MANAGEMENT =====
    
    def get_user_agent(self) -> str:
        """Get user agent based on configuration"""
        try:
            if self.config.use_mobile_agents:
                return random.choice(self.mobile_user_agents)
            else:
                return random.choice(self.desktop_user_agents)
        except Exception:
            # Fallback
            return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    def create_browser(self) -> bool:
        """Create advanced Chrome browser with Tor proxy"""
        if not self.tor_running:
            self.logger.error("❌ Tor service not running")
            return False
        
        try:
            self.logger.info("🔄 Creating advanced Chrome browser with Tor proxy...")
            
            # Chrome options (using exact working config from main_tor_browser.py)
            options = Options()
            
            # Tor proxy
            options.add_argument(f'--proxy-server=socks5://127.0.0.1:{self.config.tor_port}')
            
            # Basic stability options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            # User agent
            user_agent = self.get_user_agent()
            options.add_argument(f'--user-agent={user_agent}')
            self.logger.info(f"🔧 User agent: {user_agent}")
            
            # Window settings
            if self.config.headless:
                options.add_argument('--headless')
            options.add_argument(f'--window-size={self.config.window_size[0]},{self.config.window_size[1]}')
            
            # Create driver (no problematic experimental options)
            self.driver = uc.Chrome(options=options)
            
            # Configure timeouts
            self.driver.set_page_load_timeout(self.config.page_load_timeout)
            self.driver.implicitly_wait(self.config.implicit_wait)
            
            # Anti-detection scripts
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("✅ Advanced Chrome browser created successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error creating browser: {e}")
            return False
    
    def setup(self) -> bool:
        """Complete setup process with all features"""
        self.logger.info("🚀 Setting up advanced Tor browser automation...")
        
        # Step 1: Tor setup
        if self.config.auto_start_tor:
            if not self.start_homebrew_tor():
                self.logger.error("❌ Failed to start Tor service")
                return False
        else:
            if not self.check_homebrew_tor():
                self.logger.error("❌ Tor service not running")
                return False
        
        # Step 2: Verify Tor connectivity
        if self.config.verify_tor_ip:
            tor_ip = self.get_tor_ip()
            if not tor_ip:
                self.logger.error("❌ Could not verify Tor connectivity")
                return False
        
        # Step 3: Create browser
        if not self.create_browser():
            self.logger.error("❌ Failed to create browser")
            return False
        
        # Step 4: Tor detection test
        if self.config.check_tor_detection:
            if not self.verify_tor_detection():
                self.logger.warning("⚠️  Tor detection verification failed")
        
        self.logger.info("✅ Advanced Tor browser setup completed successfully!")
        return True
    
    # ===== ADVANCED NAVIGATION =====
    
    def navigate_with_behavior(self, url: str) -> bool:
        """Navigate with comprehensive human behavior simulation"""
        if not self.driver:
            self.logger.error("❌ Browser not initialized")
            return False
        
        try:
            self.logger.info(f"🌐 Navigating to: {url}")
            
            # Pre-navigation delay (thinking time)
            pre_delay = random.uniform(0.5, 2.0)
            time.sleep(pre_delay)
            
            # Navigate
            self.driver.get(url)
            self.session_data['requests_made'] += 1
            
            # Record page visit
            page_info = {
                'url': url,
                'timestamp': time.time(),
                'user_agent': self.get_user_agent()
            }
            self.session_data['pages_visited'].append(page_info)
            
            # Wait for page load
            try:
                WebDriverWait(self.driver, self.config.page_load_timeout).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
            except TimeoutException:
                self.logger.warning(f"⚠️  Page load timeout for {url}")
            
            # Post-navigation human behavior
            self.simulate_human_reading()
            
            if self.config.simulate_mouse_movements:
                self.simulate_mouse_movements()
            
            # Check if we need new Tor identity
            if (self.session_data['requests_made'] % self.config.request_new_identity_interval == 0 and 
                self.session_data['requests_made'] > 0):
                self.logger.info("🔄 Requesting new Tor identity for enhanced privacy...")
                self.request_new_tor_identity()
                time.sleep(3)  # Brief pause after identity change
            
            self.logger.info(f"✅ Successfully navigated to: {self.driver.title}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error navigating to {url}: {e}")
            self.session_data['errors_encountered'] += 1
            return False
    
    def simulate_human_reading(self):
        """Simulate realistic reading behavior"""
        reading_time = random.uniform(self.config.min_reading_time, self.config.max_reading_time)
        self.logger.info(f"📖 Simulating reading for {reading_time:.1f}s")
        time.sleep(reading_time)
    
    def simulate_mouse_movements(self):
        """Simulate realistic mouse movements"""
        if not self.driver:
            return
            
        try:
            actions = ActionChains(self.driver)
            
            # Random mouse movements
            for _ in range(random.randint(3, 7)):
                x_offset = random.randint(-200, 200)
                y_offset = random.randint(-100, 100)
                actions.move_by_offset(x_offset, y_offset)
                actions.pause(random.uniform(0.1, 0.5))
            
            actions.perform()
            
        except Exception as e:
            self.logger.debug(f"Mouse movement simulation failed: {e}")
    
    def advanced_scroll_behavior(self, pattern: str = "natural") -> bool:
        """Advanced scrolling with different patterns"""
        if not self.driver:
            return False
        
        try:
            if pattern == "natural":
                # Natural reading scroll
                for _ in range(random.randint(4, 8)):
                    scroll_amount = random.randint(150, 350)
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    time.sleep(random.uniform(0.8, 2.5))
                    
            elif pattern == "scan":
                # Quick scanning pattern
                total_height = self.driver.execute_script("return document.body.scrollHeight")
                positions = [total_height // 4, total_height // 2, total_height * 3 // 4, total_height]
                
                for position in positions:
                    self.driver.execute_script(f"window.scrollTo(0, {position});")
                    time.sleep(random.uniform(0.5, 1.5))
                    
            elif pattern == "detailed":
                # Detailed reading with back-scrolling
                for _ in range(random.randint(6, 10)):
                    # Forward scroll
                    self.driver.execute_script("window.scrollBy(0, 100);")
                    time.sleep(random.uniform(1.0, 2.5))
                    
                    # Occasional back-scroll
                    if random.random() < 0.3:
                        self.driver.execute_script("window.scrollBy(0, -30);")
                        time.sleep(random.uniform(0.5, 1.0))
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error during scrolling: {e}")
            return False
    
    # ===== SECURITY ANALYSIS =====
    
    def verify_tor_detection(self) -> bool:
        """Verify that Tor is properly detected"""
        if not self.driver:
            self.logger.error("❌ Browser not initialized")
            return False
            
        try:
            self.logger.info("🔍 Verifying Tor detection...")
            self.driver.get("https://check.torproject.org")
            time.sleep(5)
            
            page_source = self.driver.page_source.lower()
            if 'congratulations' in page_source and 'tor' in page_source:
                self.logger.info("✅ Tor properly detected by check.torproject.org")
                return True
            else:
                self.logger.warning("⚠️  Tor not detected properly")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error verifying Tor detection: {e}")
            return False
    
    def analyze_security_headers(self, url: str) -> Dict[str, Any]:
        """Analyze security headers of a webpage"""
        if not self.driver:
            return {}
        
        try:
            # Get headers via JavaScript (limited to what's available)
            headers_script = """
            var req = new XMLHttpRequest();
            req.open('HEAD', arguments[0], false);
            req.send(null);
            return req.getAllResponseHeaders();
            """
            
            try:
                headers_raw = self.driver.execute_script(headers_script, url)
                headers = {}
                for line in headers_raw.split('\\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        headers[key.strip().lower()] = value.strip()
            except:
                headers = {}
            
            # Analyze security headers
            security_analysis = {
                'url': url,
                'has_hsts': 'strict-transport-security' in headers,
                'has_csp': 'content-security-policy' in headers,
                'has_xframe': 'x-frame-options' in headers,
                'has_xss_protection': 'x-xss-protection' in headers,
                'has_content_type_options': 'x-content-type-options' in headers,
                'headers_found': list(headers.keys())
            }
            
            self.logger.info(f"🔒 Security headers analysis: {security_analysis}")
            return security_analysis
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing security headers: {e}")
            return {}
    
    def extract_page_data(self, url: str) -> Dict[str, Any]:
        """Extract comprehensive data from current page"""
        if not self.driver:
            return {}
        
        try:
            data = {
                'url': url,
                'title': self.driver.title,
                'current_url': self.driver.current_url,
                'page_source_length': len(self.driver.page_source),
                'timestamp': time.time()
            }
            
            # Extract forms
            if self.config.extract_forms:
                forms = []
                form_elements = self.driver.find_elements(By.TAG_NAME, "form")
                for form in form_elements:
                    form_data = {
                        'action': form.get_attribute('action'),
                        'method': form.get_attribute('method'),
                        'inputs': []
                    }
                    
                    inputs = form.find_elements(By.TAG_NAME, "input")
                    for inp in inputs:
                        form_data['inputs'].append({
                            'type': inp.get_attribute('type'),
                            'name': inp.get_attribute('name'),
                            'id': inp.get_attribute('id')
                        })
                    
                    forms.append(form_data)
                
                data['forms'] = forms
            
            # Extract links
            if self.config.extract_links:
                links = []
                link_elements = self.driver.find_elements(By.TAG_NAME, "a")
                for link in link_elements[:20]:  # Limit to first 20 links
                    href = link.get_attribute('href')
                    if href:
                        links.append({
                            'href': href,
                            'text': link.text[:50],  # Limit text length
                            'is_external': not href.startswith(self.driver.current_url.split('/')[0:3][0]) if href.startswith('http') else False
                        })
                
                data['links'] = links
            
            # Basic counts
            data['stats'] = {
                'links_count': len(self.driver.find_elements(By.TAG_NAME, "a")),
                'images_count': len(self.driver.find_elements(By.TAG_NAME, "img")),
                'forms_count': len(self.driver.find_elements(By.TAG_NAME, "form")),
                'scripts_count': len(self.driver.find_elements(By.TAG_NAME, "script")),
                'iframes_count': len(self.driver.find_elements(By.TAG_NAME, "iframe"))
            }
            
            return data
            
        except Exception as e:
            self.logger.error(f"❌ Error extracting page data: {e}")
            return {}
    
    def save_screenshot(self, url: str):
        """Save screenshot with metadata"""
        if not self.config.save_screenshots or not self.driver:
            return
            
        try:
            timestamp = int(time.time())
            safe_url = url.replace('://', '_').replace('/', '_').replace('?', '_')[:50]
            filename = f"screenshot_{safe_url}_{timestamp}.png"
            
            self.driver.save_screenshot(filename)
            self.session_data['screenshots_taken'] += 1
            self.logger.info(f"📸 Screenshot saved: {filename}")
            
        except Exception as e:
            self.logger.warning(f"⚠️  Could not save screenshot: {e}")
    
    def save_page_source(self, url: str):
        """Save page source with metadata"""
        if not self.config.save_page_source or not self.driver:
            return
            
        try:
            timestamp = int(time.time())
            safe_url = url.replace('://', '_').replace('/', '_').replace('?', '_')[:50]
            filename = f"page_source_{safe_url}_{timestamp}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            
            self.logger.info(f"💾 Page source saved: {filename}")
            
        except Exception as e:
            self.logger.warning(f"⚠️  Could not save page source: {e}")
    
    # ===== COMPREHENSIVE AUTOMATION =====
    
    def comprehensive_page_analysis(self, url: str, actions: Optional[List[str]] = None) -> Dict[str, Any]:
        """Perform comprehensive page analysis with all features"""
        if actions is None:
            actions = ['navigate', 'analyze', 'scroll', 'extract', 'security']
        
        results = {
            'url': url,
            'success': False,
            'timestamp': time.time(),
            'actions_performed': []
        }
        
        try:
            # Navigate
            if 'navigate' in actions:
                if self.navigate_with_behavior(url):
                    results['actions_performed'].append('navigate')
                else:
                    return results
            
            # Page analysis
            if 'analyze' in actions:
                page_data = self.extract_page_data(url)
                results['page_data'] = page_data
                results['actions_performed'].append('analyze')
            
            # Scrolling behavior
            if 'scroll' in actions and self.config.random_scroll_patterns:
                scroll_pattern = random.choice(['natural', 'scan', 'detailed'])
                self.advanced_scroll_behavior(scroll_pattern)
                results['actions_performed'].append(f'scroll_{scroll_pattern}')
            
            # Data extraction
            if 'extract' in actions:
                extracted_data = self.extract_page_data(url)
                results['extracted_data'] = extracted_data
                results['actions_performed'].append('extract')
            
            # Security analysis
            if 'security' in actions and self.config.analyze_security_headers:
                security_data = self.analyze_security_headers(url)
                results['security_analysis'] = security_data
                results['actions_performed'].append('security')
            
            # Save artifacts
            self.save_screenshot(url)
            self.save_page_source(url)
            
            results['success'] = True
            self.logger.info(f"✅ Comprehensive analysis completed for: {url}")
            
        except Exception as e:
            self.logger.error(f"❌ Error during comprehensive analysis of {url}: {e}")
            results['error'] = str(e)
        
        return results
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get comprehensive session summary"""
        duration = time.time() - self.session_data['start_time']
        
        return {
            'session_duration_seconds': duration,
            'session_duration_human': f"{duration/60:.1f} minutes",
            'requests_made': self.session_data['requests_made'],
            'errors_encountered': self.session_data['errors_encountered'],
            'success_rate': (self.session_data['requests_made'] - self.session_data['errors_encountered']) / max(1, self.session_data['requests_made']),
            'tor_ip': self.session_data['tor_ip'],
            'identity_changes': self.session_data['identity_changes'],
            'pages_visited_count': len(self.session_data['pages_visited']),
            'screenshots_taken': self.session_data['screenshots_taken'],
            'average_request_time': duration / max(1, self.session_data['requests_made']),
            'pages_visited': self.session_data['pages_visited']
        }
    
    def save_session_data(self):
        """Save session data to JSON file"""
        try:
            summary = self.get_session_summary()
            timestamp = int(time.time())
            filename = f"advanced_tor_session_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            
            self.logger.info(f"💾 Session data saved: {filename}")
            
        except Exception as e:
            self.logger.warning(f"⚠️  Could not save session data: {e}")
    
    def cleanup(self):
        """Comprehensive cleanup with session summary"""
        self.logger.info("🔄 Starting comprehensive cleanup...")
        
        # Save session data
        self.save_session_data()
        
        # Print session summary
        summary = self.get_session_summary()
        self.logger.info("📊 SESSION SUMMARY:")
        for key, value in summary.items():
            if key != 'pages_visited':  # Skip detailed page list in log
                self.logger.info(f"   {key}: {value}")
        
        # Close browser
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("✅ Browser closed successfully")
            except Exception as e:
                self.logger.warning(f"⚠️  Error closing browser: {e}")
        
        self.logger.info("ℹ️  Homebrew Tor service left running (managed externally)")
        self.logger.info("✅ Comprehensive cleanup completed")


# ===== CONVENIENCE FUNCTIONS =====

def create_advanced_tor_browser(config: Optional[AdvancedTorConfig] = None) -> AdvancedTorBrowser:
    """Create advanced Tor browser with sensible defaults"""
    if config is None:
        config = AdvancedTorConfig(
            auto_start_tor=True,
            verify_tor_ip=True,
            enable_comprehensive_logging=True,
            simulate_mouse_movements=True,
            random_scroll_patterns=True
        )
    
    return AdvancedTorBrowser(config)


def main():
    """Demonstration of advanced Tor browser capabilities"""
    print("🚀 ADVANCED TOR BROWSER - COMPREHENSIVE IMPLEMENTATION")
    print("=" * 70)
    
    # Create advanced configuration
    config = AdvancedTorConfig(
        auto_start_tor=True,
        verify_tor_ip=True,
        check_tor_detection=True,
        save_screenshots=True,
        save_page_source=True,
        analyze_security_headers=True,
        enable_comprehensive_logging=True,
        simulate_mouse_movements=True,
        random_scroll_patterns=True,
        request_new_identity_interval=5
    )
    
    # Create browser
    browser = AdvancedTorBrowser(config)
    
    try:
        # Setup
        if not browser.setup():
            print("❌ Setup failed!")
            return
        
        # Test URLs for comprehensive analysis
        test_urls = [
            "https://httpbin.org/ip",
            "https://httpbin.org/headers",
            "https://check.torproject.org",
            "https://httpbin.org/forms/post"
        ]
        
        # Perform comprehensive analysis on each URL
        for i, url in enumerate(test_urls):
            print(f"\n🔍 Comprehensive analysis {i+1}/{len(test_urls)}: {url}")
            
            # Perform analysis with all features
            results = browser.comprehensive_page_analysis(
                url, 
                ['navigate', 'analyze', 'scroll', 'extract', 'security']
            )
            
            if results['success']:
                print(f"✅ Analysis completed: {', '.join(results['actions_performed'])}")
            else:
                print(f"❌ Analysis failed: {results.get('error', 'Unknown error')}")
            
            # Human-like delay between pages
            if i < len(test_urls) - 1:
                delay = random.uniform(3, 8)
                print(f"⏰ Waiting {delay:.1f}s before next page...")
                time.sleep(delay)
        
        print("\n✅ All comprehensive tests completed!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        browser.cleanup()


if __name__ == "__main__":
    main()
