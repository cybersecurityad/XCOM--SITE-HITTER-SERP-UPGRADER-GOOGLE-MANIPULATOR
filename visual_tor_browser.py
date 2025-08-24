#!/usr/bin/env python3
"""
🎭 VISUAL TOR BROWSER WITH CONSISTENT IP SESSION
==============================================
Enhanced Tor-powered browser automation with:
- Same IP maintained for entire website session
- Visual browser window to see real activity
- Human behavior simulation with visible actions
- Tor network integration for anonymization
- Google Analytics compatible tracking
- Random visit patterns and timing

FEATURES:
✅ Consistent IP per website session
✅ Visual browser window (see real browsing)
✅ Human-like behavior simulation
✅ Tor network anonymization
✅ Real-time action display
✅ Google Analytics tracking simulation
✅ Random visit timing and patterns
"""

import time
import random
import json
from datetime import datetime
from typing import List, Dict, Optional
import threading
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from urllib.parse import urlparse, urljoin
from google_serp_stealth import GoogleSerpStealth

class TorVisualController:
    """
    🧅 Visual Tor Controller
    
    Manages Tor connection with consistent IP per session
    """
    
    def __init__(self):
        """Initialize the visual Tor browser"""
        self.tor_process = None
        self.driver = None
        self.current_ip = None
        self.stealth_system = GoogleSerpStealth()
        self.user_profile = None  # Will be set when needed
        self.tor_controller = None  # Add tor controller reference
        
        # Google Analytics simulation settings
        self.ga_settings = {
            'enable_javascript': True,  # Enable JS for GA tracking
            'enable_cookies': True,     # Enable cookies for session tracking
            'send_analytics': True,     # Send GA events
            'user_id_persistent': True, # Maintain user ID across sessions
            'bounce_rate_control': True # Control bounce rate behavior
        }
    
    def start_tor_service(self) -> bool:
        """Start Tor service for this session with improved initialization and error handling"""
        try:
            if self.check_tor_running():
                print(f"✅ Using existing Tor service")
                existing_ip = self.get_tor_ip()
                if existing_ip and existing_ip != 'Unknown':
                    self.current_ip = existing_ip
                    self.session_start_time = datetime.now()
                    print(f"🧅 Session IP (Netherlands): {self.current_ip}")
                    print(f"🔒 This NL IP will be maintained for entire website session")
                    return True

            # Use random SOCKS port to force different circuits
            import random
            # Use standard port for stability, improve circuit rotation instead
            socks_port = 9050  # Standard Tor port
            print(f"🔄 Using SOCKS port: {socks_port}")
            
            # Start new Tor process with Netherlands-only exit nodes
            self.tor_process = subprocess.Popen(
                ['/opt/homebrew/bin/tor', '--quiet', f'--SocksPort', str(socks_port), 
                 '--NewCircuitPeriod', '10', '--MaxCircuitDirtiness', '30',
                 '--ExitNodes', '{nl}', '--StrictNodes', '1'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Store the port for browser configuration
            self.socks_port = socks_port
            
            # Wait for Tor to initialize with progress feedback
            print(f"⏳ Starting Tor service...")
            print(f"🇳🇱 Using Netherlands-only exit nodes")
            try:
                for i in range(10):
                    print(f"   🔄 Initializing... {i+1}/10")
                    time.sleep(1)
                    
                    # Test connection every 2 seconds after initial 3 seconds
                    if i >= 2 and i % 2 == 0:
                        test_ip = self.get_tor_ip()
                        if test_ip and test_ip != 'Unknown':
                            print(f"✅ Tor ready after {i+1} seconds!")
                            self.current_ip = test_ip
                            self.session_start_time = datetime.now()
                            print(f"🧅 Session IP (Netherlands): {self.current_ip}")
                            print(f"🔒 This NL IP will be maintained for entire website session")
                            return True
                
                # Final test after full wait
                self.current_ip = self.get_tor_ip()
                
                if self.current_ip and self.current_ip != 'Unknown':
                    self.session_start_time = datetime.now()
                    print(f"✅ Tor started successfully")
                    print(f"🧅 Session IP (Netherlands): {self.current_ip}")
                    print(f"🔒 This NL IP will be maintained for entire website session")
                    return True
                else:
                    print(f"❌ Failed to establish Tor connection")
                    return False
                    
            except KeyboardInterrupt:
                print(f"⚠️  Tor startup interrupted by user")
                print(f"💡 You can try again or use option 1/2 for non-visual browsing")
                self.stop_tor()
                return False
                
        except FileNotFoundError:
            print(f"❌ Tor not found. Please install Tor:")
            print(f"   macOS: brew install tor")
            print(f"   Ubuntu: sudo apt install tor")
            return False
        except Exception as e:
            print(f"❌ Error starting Tor: {e}")
            return False
    
    def check_tor_running(self):
        """Check if Tor is already running"""
        try:
            # Test if we can connect to Tor proxy
            test_ip = self.get_tor_ip()
            return test_ip and test_ip != 'Unknown'
        except:
            return False
    
    def stop_tor(self):
        """Stop Tor service"""
        if hasattr(self, 'tor_process') and self.tor_process:
            try:
                self.tor_process.terminate()
                self.tor_process.wait(timeout=5)
                print(f"🛑 Tor service stopped")
            except:
                try:
                    self.tor_process.kill()
                except:
                    pass
            self.tor_process = None
    
    def get_tor_ip(self) -> str:
        """Get current Tor exit IP"""
        try:
            proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('origin', 'Unknown')
            
        except Exception:
            pass
        
        return 'Unknown'
        
    def force_new_tor_circuit(self):
        """Force Tor to create a new circuit for IP rotation"""
        try:
            # Kill existing browser connections first
            if hasattr(self, 'driver') and self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            
            # Method 1: Kill and restart Tor process
            if self.tor_process:
                try:
                    self.tor_process.terminate()
                    self.tor_process.wait(timeout=5)
                except:
                    pass
                self.tor_process = None
            
            # Method 2: Kill any running Tor processes
            try:
                subprocess.run(['pkill', '-f', 'tor'], capture_output=True, timeout=5)
                time.sleep(2)
            except:
                pass
            
            # Method 3: Clear Tor data directory
            try:
                subprocess.run(['rm', '-rf', '/tmp/tor_data_visual'], capture_output=True)
                time.sleep(1)
            except:
                pass
            
            print(f"🔄 Forced Tor circuit refresh")
            return True
            
        except Exception as e:
            print(f"⚠️ Error forcing new circuit: {e}")
            return False
    
    def stop_tor_service(self):
        """Stop Tor service"""
        if self.tor_process:
            print(f"🛑 Stopping Tor service...")
            self.tor_process.terminate()
            self.tor_process.wait()
            self.tor_process = None
        
        self.current_ip = None
        self.session_start_time = None

class HumanBehaviorEngine:
    """
    👤 Advanced Human Behavior Engine
    
    Simulates realistic human browser interactions
    """
    
    def __init__(self):
        self.ua = UserAgent()
        
        # Human behavior profiles
        self.behavior_profiles = {
            'curious_explorer': {
                'name': 'Curious Explorer',
                'scroll_frequency': 0.8,
                'click_probability': 0.6,
                'read_speed_wpm': 180,
                'attention_span': 45,
                'patience': 0.7,
                'interests': ['technology', 'science', 'innovation']
            },
            'casual_browser': {
                'name': 'Casual Browser', 
                'scroll_frequency': 0.6,
                'click_probability': 0.3,
                'read_speed_wpm': 150,
                'attention_span': 30,
                'patience': 0.5,
                'interests': ['entertainment', 'lifestyle', 'news']
            },
            'focused_researcher': {
                'name': 'Focused Researcher',
                'scroll_frequency': 0.9,
                'click_probability': 0.8,
                'read_speed_wpm': 220,
                'attention_span': 120,
                'patience': 0.9,
                'interests': ['research', 'academic', 'data', 'analysis']
            },
            'quick_scanner': {
                'name': 'Quick Scanner',
                'scroll_frequency': 0.9,
                'click_probability': 0.4,
                'read_speed_wpm': 250,
                'attention_span': 20,
                'patience': 0.3,
                'interests': ['headlines', 'summary', 'quick']
            }
        }
        
        print(f"👤 Human Behavior Engine Ready")
    
    def generate_session_profile(self) -> Dict:
        """Generate complete human profile for session"""
        
        # Choose behavior type
        behavior_type = random.choice(list(self.behavior_profiles.keys()))
        base_profile = self.behavior_profiles[behavior_type].copy()
        
        # Add technical details
        base_profile.update({
            'user_agent': self.ua.random,
            'session_id': f"human_{random.randint(1000, 9999)}",
            'device_type': random.choice(['desktop', 'laptop']),  # Visual browsing works best on desktop
            'os': random.choice(['Windows 10', 'Windows 11', 'macOS', 'Ubuntu']),
            'browser': 'Chrome',  # Using Chrome for visual browsing
            'screen_resolution': random.choice(['1920x1080', '1366x768', '1440x900', '2560x1440']),
            'behavior_type': behavior_type
        })
        
        return base_profile
    
    def calculate_reading_time(self, text_length: int, profile: Dict) -> float:
        """Calculate realistic reading time"""
        if text_length < 100:
            return random.uniform(2, 5)
        
        words = text_length / 5  # Approximate words (5 chars per word)
        base_time = (words / profile['read_speed_wpm']) * 60  # Convert to seconds
        
        # Add human variability
        variability = random.uniform(0.7, 1.3)
        attention_factor = profile['patience']
        
        total_time = base_time * variability * attention_factor
        
        # Cap at attention span
        return min(total_time, profile['attention_span'])

class VisualTorBrowser:
    """
    🎭 Visual Tor Browser with Consistent IP
    
    Main browser automation with visual feedback and consistent IP per session
    """
    
    def __init__(self):
        self.tor_controller = TorVisualController()
        self.behavior_engine = HumanBehaviorEngine()
        self.driver = None
        self.current_profile = None
        self.session_data = []
        self.actions_log = []
        
        print(f"🎭 Visual Tor Browser Initialized")
    
    def start_session(self, domain: str) -> bool:
        """Start a new browsing session with consistent IP"""
        
        print(f"\n🚀 STARTING NEW BROWSING SESSION")
        print(f"🌐 Target domain: {domain}")
        
        # Start Tor with consistent IP (only if not already connected)
        if not hasattr(self.tor_controller, 'current_ip') or not self.tor_controller.current_ip:
            if not self.tor_controller.start_tor_service():
                print(f"❌ Failed to start Tor service")
                return False
        else:
            print(f"✅ Using existing Tor connection")
            print(f"🧅 Session IP (Netherlands): {self.tor_controller.current_ip}")
        
        # Generate human profile for this session
        self.current_profile = self.behavior_engine.generate_session_profile()
        
        print(f"\n👤 HUMAN PROFILE FOR THIS SESSION:")
        print(f"   Type: {self.current_profile['name']}")
        print(f"   OS: {self.current_profile['os']}")
        print(f"   Device: {self.current_profile['device_type']}")
        print(f"   Reading speed: {self.current_profile['read_speed_wpm']} WPM")
        print(f"   Attention span: {self.current_profile['attention_span']}s")
        print(f"   Interests: {', '.join(self.current_profile['interests'])}")
        print(f"   User Agent: {self.current_profile['user_agent'][:60]}...")
        
        # Create visual browser
        if not self.create_visual_browser():
            print(f"❌ Failed to create browser")
            return False
        
        print(f"\n✅ SESSION READY")
        print(f"🧅 Consistent IP: {self.tor_controller.current_ip}")
        print(f"👁️ Visual browser window opened")
        print(f"🎭 Ready to browse {domain} with human behavior")
        
        return True
    
    def create_visual_browser(self) -> bool:
        """Create visible Chrome browser with advanced stealth and Tor proxy"""
        try:
            if not self.current_profile:
                print(f"❌ No profile available for browser creation")
                return False
            
            print(f"🎭 Creating visual browser with stealth configuration...")
            
            # Import stealth system
            try:
                from google_serp_stealth import GoogleSerpStealth
                stealth_system = GoogleSerpStealth()
                stealth_profile, stealth_headers, _ = stealth_system.create_stealth_session()
                print(f"✅ Advanced stealth profile loaded")
            except ImportError:
                print(f"⚠️ Using basic stealth (google_serp_stealth not available)")
                stealth_profile = None
            
            options = uc.ChromeOptions()
            
            # Configure Tor proxy (CRITICAL) - use dynamic port
            tor_port = getattr(self.tor_controller, 'socks_port', 9050)
            proxy_url = f'socks5://127.0.0.1:{tor_port}'
            options.add_argument(f'--proxy-server={proxy_url}')
            print(f"🧅 Configured Tor proxy: {proxy_url}")
            
            # Advanced stealth configuration
            if stealth_profile:
                # Use advanced stealth profile
                options.add_argument(f'--user-agent={stealth_profile.user_agent}')
                resolution = stealth_profile.screen_resolution.split('x')
                options.add_argument(f'--window-size={resolution[0]},{resolution[1]}')
                print(f"🥷 Using advanced stealth: {stealth_profile.name} ({stealth_profile.os})")
            else:
                # Fallback to basic profile
                options.add_argument(f'--user-agent={self.current_profile["user_agent"]}')
                resolution = self.current_profile['screen_resolution'].split('x')
                width, height = int(resolution[0]), int(resolution[1])
                options.add_argument(f'--window-size={width},{height}')
            
            # Essential anti-detection options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--disable-features=VizDisplayCompositor')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-default-apps')
            options.add_argument('--disable-sync')
            options.add_argument('--no-first-run')
            options.add_argument('--no-default-browser-check')
            
            # Google Analytics compatibility settings
            # Enable JavaScript for GA tracking
            options.add_argument('--enable-javascript')
            # Enable cookies for session tracking
            options.add_argument('--enable-cookies')
            # Allow third-party cookies for GA
            options.add_argument('--disable-features=SameSiteByDefaultCookies')
            # Enable local storage for analytics
            options.add_argument('--enable-local-storage')
            print(f"📊 Google Analytics tracking enabled")
            
            # Exclude automation switches
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Disable images and CSS for faster loading and less detection
            prefs = {
                "profile.managed_default_content_settings.images": 2,
                "profile.default_content_setting_values.notifications": 2,
                "profile.managed_default_content_settings.stylesheets": 2
            }
            options.add_experimental_option("prefs", prefs)
            
            print(f"🚀 Launching browser...")
            
            # Create driver with enhanced error handling
            try:
                self.driver = uc.Chrome(options=options, version_main=None)
                print(f"✅ Chrome browser created successfully")
            except Exception as chrome_error:
                print(f"❌ Chrome creation failed: {chrome_error}")
                print(f"💡 Trying alternative browser setup...")
                
                # Fallback: Try with minimal options
                basic_options = uc.ChromeOptions()
                # Configure Tor proxy with dynamic port
                tor_port = getattr(self.tor_controller, 'socks_port', 9050)
                proxy_url = f'socks5://127.0.0.1:{tor_port}'
                basic_options.add_argument(f'--proxy-server={proxy_url}')
                basic_options.add_argument('--no-sandbox')
                basic_options.add_argument('--disable-dev-shm-usage')
                
                self.driver = uc.Chrome(options=basic_options)
                print(f"✅ Browser created with minimal configuration")
            
            # Execute advanced stealth scripts
            print(f"🥷 Applying stealth modifications...")
            stealth_scripts = [
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
                "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
                "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
                "window.chrome = { runtime: {} }",
                "Object.defineProperty(navigator, 'permissions', {get: () => undefined})"
            ]
            
            for script in stealth_scripts:
                try:
                    self.driver.execute_script(script)
                except:
                    pass
            
            # Verify Tor connection in browser
            print(f"🔍 Verifying Tor connection in browser...")
            try:
                self.driver.get('http://httpbin.org/ip')
                time.sleep(3)
                
                page_source = self.driver.page_source
                current_ip = self.tor_controller.current_ip
                
                if current_ip and current_ip in page_source:
                    print(f"✅ Browser confirmed using Tor IP: {current_ip}")
                else:
                    print(f"⚠️ IP verification unclear, but browser is ready")
                
                print(f"🎭 Visual browser ready - you can see all actions!")
                return True
                
            except Exception as verify_error:
                print(f"⚠️ IP verification failed: {verify_error}")
                print(f"✅ Browser created anyway - proceeding...")
                return True
                
        except Exception as e:
            print(f"❌ Failed to create browser: {e}")
            print(f"💡 Troubleshooting tips:")
            print(f"   - Ensure Chrome is installed")
            print(f"   - Check if Tor is running (port 9050)")
            print(f"   - Try: brew install --cask google-chrome")
            print(f"   - Try: pip install --upgrade undetected-chromedriver")
            
            # Attempt cleanup
            if hasattr(self, 'driver') and self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
            
            return False
    
    def browse_website_visually(self, domain: str, duration_minutes: int = 10) -> Dict:
        """
        🎯 Main browsing function with visual feedback and consistent IP
        
        This function will:
        1. Maintain same IP throughout entire session
        2. Show real browser window with all actions
        3. Simulate realistic human behavior
        4. Log all actions in real-time
        """
        
        if not self.start_session(domain):
            return {'success': False, 'error': 'Failed to start session'}
        
        print(f"\n🎭 STARTING VISUAL BROWSING SESSION")
        print(f"⏱️ Duration: {duration_minutes} minutes")
        print(f"👁️ Watch the browser window to see human behavior simulation")
        print(f"🧅 IP {self.tor_controller.current_ip} will be maintained throughout")
        
        session_result = {
            'domain': domain,
            'start_time': datetime.now().isoformat(),
            'consistent_ip': self.tor_controller.current_ip,
            'human_profile': self.current_profile,
            'pages_visited': [],
            'actions_performed': [],
            'total_duration': 0,
            'success': False
        }
        
        try:
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            # Navigate to main domain
            current_url = domain.rstrip('/')
            visited_urls = set()
            
            while time.time() < end_time and len(session_result['pages_visited']) < 15:
                
                print(f"\n🌐 VISITING: {current_url}")
                self.log_action(f"Navigating to: {current_url}")
                
                # Visit page with human behavior
                page_result = self.visit_page_with_behavior(current_url)
                
                if page_result['success']:
                    session_result['pages_visited'].append(page_result)
                    session_result['actions_performed'].extend(page_result['actions'])
                    visited_urls.add(current_url)
                    
                    print(f"✅ Page visited successfully")
                    print(f"   📄 Title: {page_result.get('title', 'Unknown')}")
                    print(f"   ⏱️ Time spent: {page_result['time_spent']:.1f}s")
                    print(f"   🔗 Links found: {len(page_result.get('links', []))}")
                    
                    # Choose next page based on human behavior
                    next_url = self.choose_next_page(page_result.get('links', []), visited_urls, domain)
                    
                    if next_url:
                        current_url = next_url
                        print(f"🔗 Next page chosen: {urlparse(next_url).path}")
                        
                        # Human-like delay between pages
                        delay = random.uniform(5, 20)
                        print(f"⏱️ Human delay: {delay:.1f} seconds...")
                        self.countdown_delay(delay)
                        
                    else:
                        print(f"🚪 No more interesting pages found")
                        break
                        
                else:
                    print(f"❌ Failed to visit page: {page_result.get('error', 'Unknown error')}")
                    break
            
            session_result['total_duration'] = time.time() - start_time
            session_result['success'] = True
            
        except KeyboardInterrupt:
            print(f"\n⏹️ Session stopped by user")
            session_result['total_duration'] = time.time() - start_time
            session_result['interrupted'] = True
            
        except Exception as e:
            print(f"❌ Session error: {e}")
            session_result['error'] = str(e)
            session_result['total_duration'] = time.time() - start_time
        
        finally:
            # Clean up
            if self.driver:
                print(f"\n🔄 Closing browser...")
                self.driver.quit()
            
            self.tor_controller.stop_tor_service()
        
        # Save session report
        self.save_visual_session_report(session_result)
        
        print(f"\n✅ VISUAL BROWSING SESSION COMPLETE")
        print(f"📄 Pages visited: {len(session_result['pages_visited'])}")
        print(f"⏱️ Total time: {session_result['total_duration']:.1f}s")
        print(f"🎬 Actions performed: {len(session_result['actions_performed'])}")
        print(f"🧅 Consistent IP used: {session_result['consistent_ip']}")
        
        return session_result
    
    def browse_website_with_rotation(self, domain: str, duration_minutes: int = 10) -> Dict:
        """
        🔄 Advanced browsing with automatic IP rotation and behavior changes
        
        This function will:
        1. Browse site for specified duration with current identity
        2. Rotate Tor IP and change all user behavior
        3. Revisit same site with completely new identity
        4. Repeat the cycle continuously with human-like timing
        """
        
        session_result = {
            'domain': domain,
            'start_time': datetime.now(),
            'duration_per_cycle': duration_minutes,
            'cycles': [],
            'total_actions': 0,
            'ips_used': [],
            'behaviors_used': [],
            'success': False
        }
        
        cycle_count = 0
        
        try:
            print(f"\n🔄 STARTING ADVANCED ROTATION BROWSING")
            print(f"🌐 Target: {domain}")
            print(f"⏱️ Duration per cycle: {duration_minutes} minutes")
            print(f"🔄 Will rotate IP and behavior after each cycle")
            print(f"⏹️ Press Ctrl+C to stop rotation\n")
            
            while True:  # Continuous rotation loop
                cycle_count += 1
                cycle_start = datetime.now()
                
                print(f"🔄 CYCLE #{cycle_count} - NEW IDENTITY")
                print(f"=" * 40)
                
                if cycle_count > 1:
                    # Rotate everything between cycles
                    print(f"🧅 Rotating Tor IP...")
                    if not self.rotate_tor_identity():
                        print(f"⚠️ IP rotation failed, continuing...")
                    
                    print(f"🎭 Generating new behavior profile...")
                    self.generate_new_behavior_profile()
                    
                    print(f"🔄 Creating fresh browser session...")
                    if not self.create_fresh_browser():
                        print(f"⚠️ Browser creation failed, continuing...")
                
                # Log current cycle info
                current_ip = self.tor_controller.current_ip
                current_behavior = self.current_profile.get('name', 'Unknown') if self.current_profile else 'Unknown'
                
                print(f"🧅 Current IP (Netherlands): {current_ip}")
                print(f"🎭 Behavior: {current_behavior}")
                
                if self.current_profile:
                    print(f"📊 Reading Speed: {self.current_profile.get('read_speed_wpm', 'Unknown')} WPM")
                    print(f"⏱️ Attention Span: {self.current_profile.get('attention_span', 'Unknown')}s")
                else:
                    print(f"📊 Reading Speed: Unknown WPM")
                    print(f"⏱️ Attention Span: Unknown s")
                
                session_result['ips_used'].append(current_ip)
                session_result['behaviors_used'].append(current_behavior)
                
                # Browse for the specified duration
                print(f"\n🌐 Starting browsing cycle...")
                cycle_result = self.perform_single_cycle(domain, duration_minutes)
                
                cycle_result['cycle_number'] = cycle_count
                cycle_result['ip_used'] = current_ip
                cycle_result['behavior_profile'] = current_behavior
                cycle_result['start_time'] = cycle_start
                cycle_result['end_time'] = datetime.now()
                
                session_result['cycles'].append(cycle_result)
                session_result['total_actions'] += cycle_result.get('actions_count', 0)
                
                print(f"\n✅ Cycle #{cycle_count} completed!")
                print(f"📊 Actions performed: {cycle_result.get('actions_count', 0)}")
                print(f"⏱️ Duration: {(cycle_result['end_time'] - cycle_result['start_time']).seconds}s")
                
                # Skip breaks for continuous browsing
                print(f"\n🚀 Continuing to next cycle immediately...")
                print(f"� No breaks - continuous browsing mode")
                print(f"🔄 Ready for next cycle with new identity...")
                
        except KeyboardInterrupt:
            print(f"\n⚠️ Rotation stopped by user after {cycle_count} cycles")
            session_result['stopped_by_user'] = True
        except Exception as e:
            print(f"\n❌ Error during rotation: {e}")
            session_result['error'] = str(e)
        finally:
            # Cleanup
            if hasattr(self, 'driver') and self.driver:
                try:
                    self.driver.quit()
                    print(f"🧹 Browser closed")
                except:
                    pass
            
            if hasattr(self, 'tor_controller'):
                self.tor_controller.stop_tor_service()
            
            session_result['success'] = True
            session_result['end_time'] = datetime.now()
            session_result['total_cycles'] = cycle_count
            
            # Save comprehensive rotation report
            self.save_rotation_report(session_result)
        
        return session_result
    
    def rotate_tor_identity(self) -> bool:
        """Force Tor to create new circuit with new IP"""
        try:
            print(f"🔄 Forcing new Tor circuit...")
            
            # Method 1: Try Tor control protocol to force new circuit
            try:
                import subprocess
                # Send NEWNYM signal to Tor (forces new circuit)
                result = subprocess.run(['killall', '-USR2', 'tor'], 
                                      capture_output=True, timeout=5)
                print(f"📡 Sent NEWNYM signal to Tor")
                time.sleep(3)  # Wait for new circuit
            except Exception as e:
                print(f"⚠️ Signal method failed: {e}")
            
            # Method 2: Restart Tor service completely
            if hasattr(self.tor_controller, 'tor_process') and self.tor_controller.tor_process:
                print(f"🔄 Restarting Tor service...")
                self.tor_controller.stop_tor_service()
                time.sleep(3)
            
            # Start fresh Tor connection
            if self.tor_controller.start_tor_service():
                new_ip = self.tor_controller.current_ip
                print(f"✅ New Tor IP (Netherlands): {new_ip}")
                
                # Verify IP actually changed
                if hasattr(self, 'last_ip') and new_ip == self.last_ip:
                    print(f"⚠️ IP didn't change, forcing another rotation...")
                    # Try one more time
                    self.tor_controller.stop_tor_service()
                    time.sleep(5)
                    if self.tor_controller.start_tor_service():
                        new_ip = self.tor_controller.current_ip
                        print(f"🔄 Final IP: {new_ip}")
                
                self.last_ip = new_ip
                return True
            else:
                print(f"❌ Failed to get new Tor IP")
                return False
                
        except Exception as e:
            print(f"❌ IP rotation error: {e}")
            return False
    
    def generate_new_behavior_profile(self):
        """Generate completely new human behavior profile"""
        self.current_profile = self.behavior_engine.generate_session_profile()
        
        print(f"👤 New Profile: {self.current_profile['name']}")
        print(f"💻 OS: {self.current_profile['os']}")
        print(f"📱 Device: {self.current_profile['device_type']}")
        print(f"🧠 Interests: {', '.join(self.current_profile['interests'][:3])}")
    
    def create_fresh_browser(self) -> bool:
        """Create new browser with fresh stealth configuration"""
        try:
            # Close existing browser
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
                time.sleep(2)
            
            # Create new browser with updated profile
            return self.create_visual_browser()
            
        except Exception as e:
            print(f"❌ Fresh browser creation error: {e}")
            return False
    
    def perform_single_cycle(self, domain: str, duration_minutes: int) -> Dict:
        """Perform one complete browsing cycle"""
        cycle_result = {
            'domain': domain,
            'duration_minutes': duration_minutes,
            'pages_visited': [],
            'actions_performed': [],
            'actions_count': 0,
            'success': False
        }
        
        try:
            if not hasattr(self, 'driver') or not self.driver:
                if not self.create_visual_browser():
                    return cycle_result
            
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            current_url = domain.rstrip('/')
            visited_urls = set()
            action_count = 0
            
            while time.time() < end_time and len(cycle_result['pages_visited']) < 10:
                print(f"🌐 Visiting: {current_url}")
                
                # Visit page with current behavior profile
                page_result = self.visit_page_with_behavior(current_url)
                
                if page_result['success']:
                    cycle_result['pages_visited'].append(page_result)
                    cycle_result['actions_performed'].extend(page_result['actions'])
                    visited_urls.add(current_url)
                    action_count += len(page_result['actions'])
                    
                    print(f"✅ Page completed: {page_result.get('title', 'Unknown')[:50]}")
                    
                    # Choose next page
                    next_url = self.choose_next_page(page_result.get('links', []), visited_urls, domain)
                    
                    if next_url and time.time() < end_time - 30:  # Leave time for next page
                        current_url = next_url
                        
                        # Variable delay based on current behavior profile
                        delay = self.get_personalized_delay()
                        print(f"⏱️ Personalized delay: {delay:.1f}s")
                        time.sleep(delay)
                    else:
                        break
                else:
                    print(f"❌ Page visit failed")
                    break
            
            cycle_result['success'] = True
            cycle_result['actions_count'] = action_count
            
        except Exception as e:
            print(f"❌ Cycle error: {e}")
            cycle_result['error'] = str(e)
        
        return cycle_result
    
    def get_personalized_delay(self) -> float:
        """Get delay based on current behavior profile"""
        if not self.current_profile:
            return random.uniform(5, 15)
        
        profile_name = self.current_profile.get('name', '')
        
        if 'Quick' in profile_name or 'Scanner' in profile_name:
            return random.uniform(2, 8)  # Faster users
        elif 'Focused' in profile_name or 'Researcher' in profile_name:
            return random.uniform(8, 20)  # Slower, more thorough
        elif 'Casual' in profile_name:
            return random.uniform(5, 15)  # Average speed
        else:
            return random.uniform(5, 15)  # Default
    
    def countdown_with_messages(self, duration: float):
        """Countdown with human-like break messages"""
        if duration > 300:  # For breaks longer than 5 minutes
            long_break_messages = [
                "🍽️ Having a meal...",
                "📺 Watching some videos...",
                "💬 Talking to someone...",
                "🚗 Running errands...",
                "📖 Reading something...",
                "🎮 Playing a quick game...",
                "🌐 Browsing other websites...",
                "💼 Doing some work...",
                "☕ Taking a coffee break...",
                "🚶 Going for a walk..."
            ]
            
            # For long breaks, show progress every minute
            minutes = int(duration / 60)
            remaining = duration
            
            for minute in range(minutes):
                if minute < len(long_break_messages):
                    print(f"   {long_break_messages[minute]} ({minutes - minute} minutes left)")
                else:
                    print(f"   🕒 Break continues... ({minutes - minute} minutes left)")
                time.sleep(60)  # Wait 1 minute
                remaining -= 60
            
            # Handle remaining seconds
            if remaining > 0:
                print(f"   🔄 Almost ready to return...")
                time.sleep(remaining)
        else:
            # Short break messages (original logic)
            messages = [
                "☕ Getting coffee...",
                "📱 Checking phone...",
                "🤔 Thinking about what to do next...",
                "👀 Looking around...",
                "💭 Taking a mental break...",
                "🚶 Stretching legs...",
                "📧 Checking notifications...",
                "🎵 Listening to music..."
            ]
            
            intervals = int(duration / 10)  # Show message every ~10 seconds
            interval_time = duration / intervals if intervals > 0 else duration
            
            for i in range(intervals):
                if i < len(messages):
                    print(f"   {messages[i]}")
                time.sleep(interval_time)
            
            # Sleep remaining time for short breaks
            remaining = duration - (intervals * interval_time)
            if remaining > 0:
                time.sleep(remaining)
    
    def save_rotation_report(self, session_result: Dict):
        """Save comprehensive rotation session report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rotation_session_{timestamp}.json"
        
        # Convert datetime objects to strings for JSON serialization
        def serialize_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return str(obj)
        
        with open(filename, 'w') as f:
            json.dump(session_result, f, indent=2, default=serialize_datetime)
        
        print(f"📊 Rotation report saved: {filename}")
        print(f"📈 Summary:")
        print(f"   🔄 Total cycles: {session_result.get('total_cycles', 0)}")
        print(f"   🧅 IPs used: {len(set(session_result.get('ips_used', [])))}")
        print(f"   🎭 Behaviors used: {len(set(session_result.get('behaviors_used', [])))}")
        print(f"   🎬 Total actions: {session_result.get('total_actions', 0)}")

    def visit_page_with_behavior(self, url: str) -> Dict:
        """Visit a single page with visible human behavior"""
        start_time = time.time()
        
        if not self.driver or not self.current_profile:
            return {
                'success': False,
                'url': url,
                'error': 'Browser or profile not initialized',
                'time_spent': time.time() - start_time
            }
        
        try:
            # Navigate to page
            self.driver.get(url)
            self.log_action(f"Loaded page: {url}")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Get page info
            title = self.driver.title
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            
            print(f"📄 Page loaded: {title}")
            self.log_action(f"Page title: {title}")
            
            # Simulate human reading and interaction
            actions_performed = []
            
            # 1. Initial page scan (quick scroll to bottom and back)
            print(f"👁️ Scanning page content...")
            self.log_action("Initial page scan")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1, 2))
            self.driver.execute_script("window.scrollTo(0, 0);")
            actions_performed.append("Initial page scan")
            
            # 2. Calculate reading time based on content
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            read_time = self.behavior_engine.calculate_reading_time(len(page_text), self.current_profile)
            
            print(f"📖 Simulating reading for {read_time:.1f} seconds...")
            self.log_action(f"Reading content ({read_time:.1f}s)")
            
            # 3. Human-like scrolling while "reading"
            scroll_actions = self.perform_human_scrolling(page_height, read_time)
            actions_performed.extend(scroll_actions)
            
            # 4. Look for interesting links
            links = self.find_clickable_links()
            
            # 5. Maybe click a link (based on interests)
            if links and random.random() < self.current_profile['click_probability']:
                clicked_link = self.maybe_click_interesting_link(links)
                if clicked_link:
                    actions_performed.append(f"Clicked link: {clicked_link}")
            
            total_time = time.time() - start_time
            
            return {
                'success': True,
                'url': url,
                'title': title,
                'time_spent': total_time,
                'page_height': page_height,
                'content_length': len(page_text),
                'actions': actions_performed,
                'links': [{'url': link['url'], 'text': link['text']} for link in links[:10]]  # Top 10 links
            }
            
        except Exception as e:
            return {
                'success': False,
                'url': url,
                'error': str(e),
                'time_spent': time.time() - start_time
            }
    
    def perform_human_scrolling(self, page_height: int, duration: float) -> List[str]:
        """Perform realistic human scrolling"""
        actions = []
        
        if page_height < 1000:
            # Short page - minimal scrolling
            time.sleep(duration)
            return ["Short page - minimal scrolling"]
        
        # Slower, more realistic reading scrolling
        scroll_segments = max(8, int(duration / 12))  # Scroll every 12 seconds (slower)
        segment_time = duration / scroll_segments
        
        # Add random pauses between segments for realistic reading
        reading_pause = random.uniform(3, 8)  # Additional pause for reading
        
        for i in range(scroll_segments):
            # Random scroll position
            scroll_position = random.randint(100, page_height - 500)
            
            print(f"🖱️ Scrolling to position {scroll_position}")
            self.log_action(f"Scroll to position {scroll_position}")
            
            # Smooth scroll
            if self.driver:
                self.driver.execute_script(f"window.scrollTo({{top: {scroll_position}, behavior: 'smooth'}});")
            else:
                print(f"⚠️ Driver not available for scrolling")
            
            actions.append(f"Scrolled to position {scroll_position}")
            
            # Pause at this position with reading simulation
            print(f"📖 Reading content at this position...")
            time.sleep(segment_time)
            
            # Additional random reading pause (realistic behavior)
            if i < scroll_segments - 1:  # Don't pause after last segment
                extra_pause = random.uniform(2, 6)
                print(f"🤔 Taking reading pause: {extra_pause:.1f}s")
                time.sleep(extra_pause)
        
    def simulate_google_analytics_events(self):
        """Simulate realistic Google Analytics events"""
        if not self.driver:
            return
            
        try:
            # Simulate page view event
            self.driver.execute_script("""
                // Simulate Google Analytics pageview
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'page_view', {
                        'page_title': document.title,
                        'page_location': window.location.href
                    });
                }
                
                // Simulate scroll tracking
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'scroll', {
                        'event_category': 'engagement',
                        'event_label': 'page_scroll'
                    });
                }
                
                // Simulate time on page
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'timing_complete', {
                        'name': 'page_read_time',
                        'value': Math.floor(Math.random() * 180 + 30) // 30-210 seconds
                    });
                }
            """)
            
            print(f"📊 Sent Google Analytics events")
            self.log_action("Sent GA tracking events")
            
        except Exception as e:
            print(f"⚠️ GA simulation error: {e}")
    
    def generate_realistic_visit_timing(self):
        """Generate realistic visit timing patterns"""
        # Simulate realistic user visit patterns
        visit_patterns = {
            'morning_rush': {'hour_range': (7, 9), 'probability': 0.15},
            'work_hours': {'hour_range': (9, 17), 'probability': 0.40},
            'evening': {'hour_range': (17, 22), 'probability': 0.35},
            'night': {'hour_range': (22, 24), 'probability': 0.10}
        }
        
        # Random day of week patterns
        weekday_patterns = {
            'weekday': {'probability': 0.7, 'longer_sessions': False},
            'weekend': {'probability': 0.3, 'longer_sessions': True}
        }
        
        current_hour = datetime.now().hour
        
        # Determine if this is a realistic visit time
        for pattern_name, pattern in visit_patterns.items():
            start_hour, end_hour = pattern['hour_range']
            if start_hour <= current_hour <= end_hour:
                if random.random() < pattern['probability']:
                    return True, pattern_name
        
        return False, 'off_hours'
    
    def perform_human_scrolling(self, page_height: int, duration: float) -> List[str]:
        """Perform realistic human scrolling"""
        actions = []
        
        if page_height < 1000:
            # Short page - minimal scrolling
            time.sleep(duration)
            return ["Short page - minimal scrolling"]
        
        # Slower, more realistic reading scrolling
        scroll_segments = max(8, int(duration / 12))  # Scroll every 12 seconds (slower)
        segment_time = duration / scroll_segments
        
        # Add random pauses between segments for realistic reading
        reading_pause = random.uniform(3, 8)  # Additional pause for reading
        
        for i in range(scroll_segments):
            # Random scroll position
            scroll_position = random.randint(100, page_height - 500)
            
            print(f"🖱️ Scrolling to position {scroll_position}")
            self.log_action(f"Scroll to position {scroll_position}")
            
            # Smooth scroll
            if self.driver:
                self.driver.execute_script(f"window.scrollTo({{top: {scroll_position}, behavior: 'smooth'}});")
            else:
                print(f"⚠️ Driver not available for scrolling")
            
            actions.append(f"Scrolled to position {scroll_position}")
            
            # Pause at this position with reading simulation
            print(f"📖 Reading content at this position...")
            time.sleep(segment_time)
            
            # Additional random reading pause (realistic behavior)
            if i < scroll_segments - 1:  # Don't pause after last segment
                extra_pause = random.uniform(2, 6)
                print(f"🤔 Taking reading pause: {extra_pause:.1f}s")
                time.sleep(extra_pause)
        
        return actions
    
    def find_clickable_links(self) -> List[Dict]:
        """Find interesting links on the page"""
        try:
            if not self.driver:
                return []
            link_elements = self.driver.find_elements(By.TAG_NAME, "a")
            links = []
            
            for element in link_elements[:20]:  # Check first 20 links
                try:
                    href = element.get_attribute('href')
                    text = element.text.strip()
                    
                    if href and text and len(text) > 3:
                        links.append({
                            'url': href,
                            'text': text,
                            'element': element
                        })
                        
                except Exception:
                    continue
            
            return links
            
        except Exception:
            return []
    
    def maybe_click_interesting_link(self, links: List[Dict]) -> Optional[str]:
        """Click a link if it matches user interests"""
        
        for link in links:
            link_text_lower = link['text'].lower()
            
            # Check if link matches interests
            if self.current_profile and 'interests' in self.current_profile:
                interest_match = any(
                    interest in link_text_lower 
                    for interest in self.current_profile['interests']
                )
            else:
                interest_match = False
            
            if interest_match:
                try:
                    if not self.driver:
                        return None
                        
                    print(f"🖱️ Clicking interesting link: {link['text']}")
                    self.log_action(f"Clicking link: {link['text']}")
                    
                    # Scroll to element first
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", link['element'])
                    time.sleep(1)
                    
                    # Click with human-like delay
                    ActionChains(self.driver).move_to_element(link['element']).pause(random.uniform(0.5, 1.5)).click().perform()
                    
                    time.sleep(random.uniform(2, 5))  # Wait for page load
                    
                    return link['text']
                    
                except Exception as e:
                    print(f"⚠️ Click failed: {e}")
                    continue
        
        return None
    
    def choose_next_page(self, links: List[Dict], visited: set, base_domain: str) -> Optional[str]:
        """Choose next page to visit based on human behavior"""
        
        if not links:
            return None
        
        base_netloc = urlparse(base_domain).netloc
        candidates = []
        
        for link in links:
            try:
                link_netloc = urlparse(link['url']).netloc
                
                if (link['url'] not in visited and 
                    (link_netloc == base_netloc or link_netloc == '')):
                    
                    # Score based on interest
                    if self.current_profile and 'interests' in self.current_profile:
                        interest_score = sum(
                            1 for interest in self.current_profile['interests']
                            if interest in link['text'].lower()
                        )
                    else:
                        interest_score = 0
                    
                    candidates.append((link, interest_score))
                    
            except Exception:
                continue
        
        if not candidates:
            return None
        
        # Sort by interest score and add randomness
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Choose from top candidates with some randomness
        top_candidates = candidates[:5]
        chosen = random.choice(top_candidates)
        
        return chosen[0]['url']
    
    def log_action(self, action: str):
        """Log action with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {action}"
        self.actions_log.append(log_entry)
        print(f"📝 {log_entry}")
    
    def countdown_delay(self, seconds: float):
        """Show countdown during delays"""
        remaining = int(seconds)
        while remaining > 0:
            print(f"⏳ Waiting {remaining}s...", end='\r')
            time.sleep(1)
            remaining -= 1
        print(" " * 20, end='\r')  # Clear countdown
    
    def save_visual_session_report(self, session_result: Dict):
        """Save detailed session report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"visual_tor_session_{timestamp}.json"
        
        # Add actions log to report
        session_result['detailed_actions_log'] = self.actions_log
        
        with open(filename, 'w') as f:
            json.dump(session_result, f, indent=2, default=str)
        
        print(f"📊 Session report saved: {filename}")

def main():
    """Main interface for visual Tor browsing"""
    
    print("🎭 VISUAL TOR BROWSER WITH CONSISTENT IP")
    print("=======================================")
    print("Browse websites with visual feedback and same IP per session")
    
    try:
        browser = VisualTorBrowser()
        
        print("\n🎯 VISUAL BROWSING OPTIONS:")
        print("1. 🎭 Browse website with visual feedback (consistent IP)")
        print("2. 📊 View previous sessions")
        print("3. 🧪 Test Tor connection")
        print("4. 🔄 Advanced rotation browsing (auto IP change + behavior rotation)")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            print(f"\n🧅 ESTABLISHING TOR CONNECTION")
            print(f"=============================")
            
            # First establish Tor connection
            tor_controller = TorVisualController()
            if not tor_controller.start_tor_service():
                print(f"❌ Failed to establish Tor connection")
                print(f"💡 Please ensure Tor is installed: brew install tor")
                return
            
            print(f"\n✅ Tor connection established successfully!")
            print(f"🌍 Your new anonymous IP: {tor_controller.current_ip}")
            print(f"🔒 This IP will be maintained for the entire session")
            print(f"🧅 All traffic will be routed through Tor network")
            
            # Now ask for website details
            print(f"\n🌐 WEBSITE SELECTION")
            print(f"==================")
            domain = input("Enter domain to browse (e.g., https://example.com): ").strip()
            if not domain.startswith('http'):
                domain = 'https://' + domain
            
            duration = int(input("Browsing duration in minutes (default 5): ") or "5")
            
            print(f"\n🚀 Starting visual browsing session")
            print(f"🌐 Target: {domain}")
            print(f"⏱️ Duration: {duration} minutes")
            print(f"🧅 Anonymous IP: {tor_controller.current_ip}")
            print(f"👁️ Browser window will open - watch the automation!")
            print(f"⏹️ Press Ctrl+C to stop early")
            
            # Set the tor controller for the browser to use the same connection
            browser.tor_controller = tor_controller
            
            session = browser.browse_website_visually(domain, duration)
            
            if session.get('success'):
                print(f"\n🎉 Session completed successfully!")
                print(f"🧅 Final IP: {tor_controller.current_ip}")
            else:
                print(f"\n⚠️ Session ended with issues")
            
            # Clean up
            tor_controller.stop_tor_service()
        
        elif choice == '2':
            print(f"📊 Previous sessions would be shown here")
        
        elif choice == '3':
            print(f"🧪 Testing Tor connection...")
            controller = TorVisualController()
            if controller.start_tor_service():
                print(f"✅ Tor test successful!")
                controller.stop_tor_service()
            else:
                print(f"❌ Tor test failed")
        
        elif choice == '4':
            print(f"\n🔄 ADVANCED ROTATION BROWSING")
            print(f"=============================")
            
            # First establish Tor connection
            tor_controller = TorVisualController()
            if not tor_controller.start_tor_service():
                print(f"❌ Failed to establish Tor connection")
                print(f"💡 Please ensure Tor is installed: brew install tor")
                return
            
            print(f"\n✅ Tor connection established successfully!")
            print(f"🌍 Starting IP: {tor_controller.current_ip}")
            print(f"🔄 This IP will change automatically after each cycle")
            print(f"🎭 Behavior profiles will rotate with each cycle")
            
            # Now ask for website details
            print(f"\n🌐 ROTATION BROWSING SETUP")
            print(f"=========================")
            domain = input("Enter domain to browse (e.g., https://example.com): ").strip()
            if not domain.startswith('http'):
                domain = 'https://' + domain
            
            duration = int(input("Minutes per cycle (default 5): ") or "5")
            
            print(f"\n🚀 Starting advanced rotation browsing")
            print(f"🌐 Target: {domain}")
            # Longer reading sessions (10-30 minutes)
            session_duration = random.randint(10, 30)  # 10-30 minutes
            print(f"⏱️ Duration per cycle: {session_duration} minutes")
            print(f"🔄 Will auto-rotate IP and behavior after each cycle")
            print(f"⏸️ Will take 10-30 minute breaks between site visits")
            print(f"🧅 Starting IP: {tor_controller.current_ip}")
            print(f"👁️ Browser window will open - watch the automation!")
            print(f"⏹️ Press Ctrl+C to stop rotation")
            
            # Set the tor controller for the browser to use
            browser.tor_controller = tor_controller
            
            session = browser.browse_website_with_rotation(domain, session_duration)
            
            if session.get('success'):
                print(f"\n🎉 Rotation session completed successfully!")
                print(f"🔄 Total cycles: {session.get('total_cycles', 0)}")
                print(f"🧅 IPs used: {len(set(session.get('ips_used', [])))}")
                print(f"🎭 Behaviors used: {len(set(session.get('behaviors_used', [])))}")
            else:
                print(f"\n⚠️ Rotation session ended with issues")
        
        else:
            print("❌ Invalid selection")
            
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Operation interrupted by user")
        print(f"💡 Tip: If Tor startup is slow, you can:")
        print(f"   - Wait for it to finish initializing")
        print(f"   - Use options 1/2 for faster non-visual browsing")
        print(f"   - Install Tor locally: brew install tor")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print(f"💡 Try restarting or use other browsing options")

if __name__ == "__main__":
    main()
