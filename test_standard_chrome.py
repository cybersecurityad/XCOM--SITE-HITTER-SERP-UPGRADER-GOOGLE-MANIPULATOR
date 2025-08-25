#!/usr/bin/env python3
"""
Alternative browser test using standard selenium chromedriver
"""

import time
import subprocess
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_standard_chrome():
    """Test with standard selenium chromedriver"""
    print("🔬 Testing standard Chrome...")
    
    try:
        options = Options()
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Try to create driver
        driver = webdriver.Chrome(options=options)
        print("✅ Standard Chrome driver created")
        
        # Execute script to hide webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Test basic navigation
        driver.get("data:text/html,<html><body><h1>Standard Chrome Test</h1></body></html>")
        print("✅ Navigation successful")
        
        # Test element finding
        wait = WebDriverWait(driver, 10)
        h1 = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        print(f"✅ Found element: {h1.text}")
        
        # Keep browser open for a moment
        time.sleep(2)
        
        driver.quit()
        print("✅ Standard Chrome test successful")
        return True
        
    except Exception as e:
        print(f"❌ Standard Chrome test failed: {e}")
        try:
            driver.quit()
        except:
            pass
        return False

def test_standard_chrome_with_tor():
    """Test standard Chrome with Tor proxy"""
    print("🔐 Testing standard Chrome with Tor...")
    
    # Start Tor first
    tor_data_dir = tempfile.mkdtemp(prefix="standard_tor_")
    torrc_content = f"""
DataDirectory {tor_data_dir}
SocksPort 9050
ControlPort 9051
ExitNodes {{nl}}
StrictNodes 1
"""
    
    torrc_path = f"{tor_data_dir}/torrc"
    with open(torrc_path, 'w') as f:
        f.write(torrc_content)
    
    try:
        # Start Tor
        tor_process = subprocess.Popen([
            '/opt/homebrew/bin/tor', '-f', torrc_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⏳ Waiting for Tor...")
        time.sleep(6)
        
        if tor_process.poll() is not None:
            print("❌ Tor failed to start")
            return False
        
        # Create Chrome with proxy
        options = Options()
        options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-web-security')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=options)
        print("✅ Standard Chrome with Tor created")
        
        # Hide webdriver
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Test local page first
        driver.get("data:text/html,<html><body><h1>Tor Chrome Test</h1></body></html>")
        print("✅ Local navigation works")
        
        # Test external site
        print("🌐 Testing external navigation...")
        driver.set_page_load_timeout(30)
        driver.get("http://httpbin.org/ip")
        
        # Wait for content
        wait = WebDriverWait(driver, 15)
        body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        print(f"✅ IP response: {body.text[:100]}...")
        
        driver.quit()
        tor_process.terminate()
        tor_process.wait()
        
        print("✅ Standard Chrome with Tor test successful")
        return True
        
    except Exception as e:
        print(f"❌ Standard Chrome with Tor failed: {e}")
        try:
            driver.quit()
        except:
            pass
        try:
            tor_process.terminate()
            tor_process.wait()
        except:
            pass
        return False

def main():
    print("🔬 Alternative Browser Tests")
    print("=" * 35)
    
    # Test standard Chrome
    if test_standard_chrome():
        print("\n✅ Standard Chrome PASSED")
        
        # Test with Tor
        if test_standard_chrome_with_tor():
            print("\n✅ Standard Chrome + Tor PASSED")
            print("\n🎉 Alternative approach works!")
        else:
            print("\n❌ Standard Chrome + Tor FAILED")
    else:
        print("\n❌ Standard Chrome FAILED")

if __name__ == "__main__":
    main()
