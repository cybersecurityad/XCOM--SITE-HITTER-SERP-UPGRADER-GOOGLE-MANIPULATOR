#!/usr/bin/env python3
"""
Debug script to test browser creation and basic functionality
"""

import time
import tempfile
import subprocess
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

def test_tor_setup():
    """Test basic Tor setup"""
    print("🔧 Testing Tor setup...")
    
    try:
        # Create temp directory
        tor_data_dir = tempfile.mkdtemp(prefix="debug_tor_")
        print(f"📁 Tor data dir: {tor_data_dir}")
        
        # Create simple torrc
        torrc_content = f"""
DataDirectory {tor_data_dir}
SocksPort 9050
ControlPort 9051
ExitNodes {{nl}}
StrictNodes 1
Log notice stdout
"""
        
        torrc_path = f"{tor_data_dir}/torrc"
        with open(torrc_path, 'w') as f:
            f.write(torrc_content)
        
        print("✅ Torrc created")
        
        # Start Tor
        cmd = ['/opt/homebrew/bin/tor', '-f', torrc_path]
        tor_process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        print("⏳ Waiting for Tor...")
        time.sleep(5)
        
        if tor_process.poll() is None:
            print("✅ Tor is running")
            return tor_process, tor_data_dir
        else:
            stdout, stderr = tor_process.communicate()
            print(f"❌ Tor failed: {stderr}")
            return None, None
            
    except Exception as e:
        print(f"❌ Tor setup failed: {e}")
        return None, None

def test_simple_browser():
    """Test basic browser without Tor"""
    print("🌐 Testing simple browser...")
    
    try:
        options = uc.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = uc.Chrome(options=options)
        print("✅ Browser created")
        
        # Test navigation
        driver.get("data:text/html,<html><body><h1>Test</h1></body></html>")
        print("✅ Basic navigation works")
        
        # Test element finding
        h1 = driver.find_element(By.TAG_NAME, "h1")
        print(f"✅ Found element: {h1.text}")
        
        driver.quit()
        print("✅ Browser closed cleanly")
        return True
        
    except Exception as e:
        print(f"❌ Simple browser test failed: {e}")
        return False

def test_tor_browser():
    """Test browser with Tor proxy"""
    print("🔐 Testing browser with Tor proxy...")
    
    tor_process, tor_data_dir = test_tor_setup()
    if not tor_process:
        return False
    
    try:
        options = uc.ChromeOptions()
        options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-web-security')
        options.add_argument('--ignore-certificate-errors')
        
        driver = uc.Chrome(options=options)
        print("✅ Tor browser created")
        
        # Test simple data URL first
        driver.get("data:text/html,<html><body><h1>Tor Test</h1></body></html>")
        print("✅ Data URL navigation works")
        
        # Test external navigation (this is where it might fail)
        print("🔍 Testing external navigation...")
        driver.get("http://httpbin.org/ip")
        time.sleep(5)
        
        body = driver.find_element(By.TAG_NAME, "body").text
        print(f"✅ IP response: {body[:100]}...")
        
        driver.quit()
        print("✅ Tor browser test successful")
        
        # Cleanup
        tor_process.terminate()
        tor_process.wait()
        
        return True
        
    except Exception as e:
        print(f"❌ Tor browser test failed: {e}")
        
        # Cleanup
        try:
            driver.quit()
        except:
            pass
        
        tor_process.terminate()
        tor_process.wait()
        
        return False

def main():
    print("🔬 Browser Debug Tests")
    print("=" * 30)
    
    # Test 1: Simple browser
    if test_simple_browser():
        print("\n✅ Simple browser test PASSED")
    else:
        print("\n❌ Simple browser test FAILED")
        return
    
    # Test 2: Tor browser
    if test_tor_browser():
        print("\n✅ Tor browser test PASSED")
    else:
        print("\n❌ Tor browser test FAILED")
        return
    
    print("\n🎉 All tests passed!")

if __name__ == "__main__":
    main()
