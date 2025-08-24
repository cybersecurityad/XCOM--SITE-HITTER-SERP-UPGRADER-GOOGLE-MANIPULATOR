#!/usr/bin/env python3
"""
🔍 DETAILED BROWSER STARTUP LOGGING SYSTEM
==========================================
Comprehensive logging to track exactly where and why browsers are exiting.
This will capture every step of the browser creation process with timestamps.
"""

import time
import os
import sys
import signal
import subprocess
import logging
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class DetailedLogger:
    """Comprehensive logging system for browser startup debugging"""
    
    def __init__(self, log_file="browser_startup_debug.log"):
        self.log_file = log_file
        self.setup_logging()
        self.step_counter = 0
        
    def setup_logging(self):
        """Setup detailed logging configuration"""
        # Create formatter with timestamp and detailed info
        formatter = logging.Formatter(
            '%(asctime)s.%(msecs)03d | %(levelname)8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        # File handler
        file_handler = logging.FileHandler(self.log_file, mode='w')
        file_handler.setFormatter(formatter)
        
        # Setup logger
        self.logger = logging.getLogger('BrowserDebug')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        self.logger.info("=" * 80)
        self.logger.info("🔍 DETAILED BROWSER STARTUP LOGGING INITIALIZED")
        self.logger.info("=" * 80)
    
    def step(self, message):
        """Log a step with counter"""
        self.step_counter += 1
        self.logger.info(f"STEP {self.step_counter:02d}: {message}")
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(f"DEBUG: {message}")
    
    def error(self, message, exception=None):
        """Log error with optional exception details"""
        self.logger.error(f"ERROR: {message}")
        if exception:
            self.logger.error(f"EXCEPTION: {str(exception)}")
            self.logger.error(f"TRACEBACK:\n{traceback.format_exc()}")
    
    def success(self, message):
        """Log success message"""
        self.logger.info(f"✅ SUCCESS: {message}")
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(f"⚠️  WARNING: {message}")

class DetailedBrowserTester:
    """Browser tester with comprehensive logging"""
    
    def __init__(self):
        self.logger = DetailedLogger()
        self.browsers = []
        self.running = True
        
        # Setup signal handling
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.logger.step("Detailed browser tester initialized")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.warning(f"Signal {signum} received - graceful shutdown")
        self.running = False
        self.cleanup_all()
        sys.exit(0)
    
    def check_existing_chrome_processes(self):
        """Check for existing Chrome processes"""
        try:
            self.logger.step("Checking for existing Chrome processes")
            result = subprocess.run(['pgrep', '-f', 'Chrome'], capture_output=True, text=True)
            
            if result.returncode == 0:
                pids = result.stdout.strip().split('\n')
                self.logger.warning(f"Found {len(pids)} existing Chrome processes: {pids}")
                return pids
            else:
                self.logger.success("No existing Chrome processes found")
                return []
                
        except Exception as e:
            self.logger.error("Failed to check Chrome processes", e)
            return []
    
    def kill_existing_chrome(self):
        """Kill existing Chrome processes"""
        try:
            self.logger.step("Killing existing Chrome processes")
            
            # Kill Chrome
            result1 = subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True)
            self.logger.debug(f"pkill Chrome result: {result1.returncode}")
            
            # Kill chromedriver
            result2 = subprocess.run(['pkill', '-f', 'chromedriver'], capture_output=True)
            self.logger.debug(f"pkill chromedriver result: {result2.returncode}")
            
            # Wait for processes to die
            time.sleep(2)
            
            # Verify cleanup
            remaining = self.check_existing_chrome_processes()
            if remaining:
                self.logger.warning(f"Still found {len(remaining)} Chrome processes after cleanup")
            else:
                self.logger.success("All Chrome processes cleaned up")
                
        except Exception as e:
            self.logger.error("Failed to kill Chrome processes", e)
    
    def create_browser_with_logging(self, test_name, attempt=1):
        """Create browser with detailed step-by-step logging"""
        try:
            self.logger.step(f"=== CREATING BROWSER: {test_name} (Attempt {attempt}) ===")
            
            # Pre-creation checks
            self.logger.step("Pre-creation environment check")
            self.check_existing_chrome_processes()
            
            # Create Chrome options
            self.logger.step(f"Creating Chrome options for: {test_name}")
            options = Options()
            
            # Add options one by one with logging
            option_list = [
                '--no-sandbox',
                '--disable-dev-shm-usage', 
                '--disable-gpu',
                '--disable-extensions',
                '--disable-plugins',
                '--enable-javascript'
            ]
            
            for opt in option_list:
                options.add_argument(opt)
                self.logger.debug(f"Added Chrome option: {opt}")
            
            # User agent
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            options.add_argument(f'--user-agent={user_agent}')
            self.logger.debug(f"Added user agent: {user_agent[:50]}...")
            
            # Create Chrome service
            self.logger.step("Creating Chrome service")
            service = Service()
            self.logger.debug(f"Chrome service created: {service}")
            
            # Create WebDriver
            self.logger.step("Creating WebDriver instance")
            start_time = time.time()
            
            browser = webdriver.Chrome(service=service, options=options)
            
            creation_time = time.time() - start_time
            self.logger.success(f"WebDriver created in {creation_time:.2f} seconds")
            
            # Configure timeouts
            self.logger.step("Configuring browser timeouts")
            browser.set_page_load_timeout(15)
            browser.implicitly_wait(5)
            self.logger.debug("Timeouts configured: page_load=15s, implicit=5s")
            
            # Test basic functionality
            self.logger.step("Testing basic browser functionality")
            test_html = "data:text/html,<html><body><h1>Test Page</h1><p>Browser startup test</p></body></html>"
            browser.get(test_html)
            
            # Verify page loaded
            if "Test Page" in browser.page_source:
                self.logger.success(f"Browser {test_name} fully functional!")
                return browser
            else:
                self.logger.error(f"Browser {test_name} failed functionality test")
                browser.quit()
                return None
                
        except Exception as e:
            self.logger.error(f"Browser creation failed for {test_name}", e)
            return None
    
    def test_multiple_browser_startup(self):
        """Test multiple browser startup sequence with detailed logging"""
        self.logger.step("=== TESTING MULTIPLE BROWSER STARTUP ===")
        
        # Clean start
        self.kill_existing_chrome()
        
        success_count = 0
        
        for i in range(3):
            browser_name = f"Browser_{i+1}"
            self.logger.step(f"--- Creating {browser_name} ({i+1}/3) ---")
            
            # Wait between browsers
            if i > 0:
                wait_time = 3
                self.logger.step(f"Waiting {wait_time} seconds before next browser")
                time.sleep(wait_time)
            
            browser = self.create_browser_with_logging(browser_name)
            
            if browser:
                self.browsers.append(browser)
                success_count += 1
                self.logger.success(f"{browser_name} created successfully ({success_count}/3)")
                
                # Test the browser quickly
                try:
                    title = browser.title
                    self.logger.debug(f"{browser_name} title: {title}")
                except Exception as e:
                    self.logger.warning(f"{browser_name} title check failed: {e}")
                    
            else:
                self.logger.error(f"{browser_name} creation FAILED - stopping test")
                break
        
        self.logger.step(f"Multiple browser test completed: {success_count}/3 successful")
        
        # Keep browsers open for observation
        if self.browsers:
            self.logger.step(f"Keeping {len(self.browsers)} browsers open for observation")
            self.logger.step("Press Ctrl+C to close all browsers and exit")
            
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.logger.warning("Interrupted by user")
        
        return success_count == 3
    
    def cleanup_all(self):
        """Clean up all browsers"""
        self.logger.step("=== CLEANING UP ALL BROWSERS ===")
        
        for i, browser in enumerate(self.browsers):
            try:
                self.logger.step(f"Cleaning up Browser_{i+1}")
                browser.quit()
                self.logger.success(f"Browser_{i+1} closed successfully")
            except Exception as e:
                self.logger.error(f"Failed to close Browser_{i+1}", e)
        
        self.browsers.clear()
        
        # Final process cleanup
        self.kill_existing_chrome()
        
        self.logger.success("All cleanup completed")

def main():
    """Main execution with detailed logging"""
    print("🔍 DETAILED BROWSER STARTUP LOGGING")
    print("=" * 50)
    print("This will create a detailed log of every browser startup step")
    print("Log file: browser_startup_debug.log")
    print("=" * 50)
    
    tester = DetailedBrowserTester()
    tester.test_multiple_browser_startup()

if __name__ == "__main__":
    main()
