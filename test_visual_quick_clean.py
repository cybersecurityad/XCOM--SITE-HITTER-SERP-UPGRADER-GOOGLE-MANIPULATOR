#!/usr/bin/env python3
"""
Quick visual browser test using Firefox with Tor (avoids Chrome exit code 15)
"""
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

def start_tor():
    """Start Tor service and return process and IP"""
    print("🧅 Starting Tor service...")
    try:
        subprocess.run(['pkill', '-f', 'tor'], capture_output=True)
        time.sleep(2)
    except Exception:
        pass
    
    tor_process = subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for i in range(20):
        time.sleep(1)
        try:
            import requests
            proxies = {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
            r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=3)
            if r.status_code == 200:
                ip = r.json().get('origin', 'Unknown')
                print(f"✅ Tor ready: {ip}")
                return tor_process, ip
        except Exception:
            pass
    
    print("❌ Tor startup timeout")
    return None, None

def quick_visual_test_firefox():
    """Test Firefox with Tor - no Chrome exit code 15 issues"""
    print("🧪 Quick Visual Browsing Test (Firefox)")
    print("======================================")
    
    tor_process = None
    driver = None
    
    try:
        # Start Tor
        tor_process, ip = start_tor()
        if not tor_process:
            print("❌ Tor connection failed")
            return
        print(f"✅ Connected with IP: {ip}")

        # Firefox options with Tor proxy
        options = FirefoxOptions()
        options.set_preference('network.proxy.type', 1)
        options.set_preference('network.proxy.socks', '127.0.0.1')
        options.set_preference('network.proxy.socks_port', 9050)
        options.set_preference('network.proxy.socks_remote_dns', True)
        options.set_preference('permissions.default.image', 2)  # Disable images for speed
        # Comment out the next line to see the browser window:
        # options.add_argument('--headless')

        print("🌐 Launching Firefox browser...")
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(30)

        # Test with a simple page
        test_domain = "https://httpbin.org/ip"
        print(f"🌐 Testing with: {test_domain}")
        driver.get(test_domain)
        
        # Wait for page to load
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        print(f"✅ Page loaded: {driver.title}")
        print(f"👁️ Browser window should be visible")
        print(f"⏱️ Waiting 10 seconds to view the page...")
        time.sleep(10)

        print(f"✅ Test completed successfully!")

    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"❌ Test error: {e}")
    finally:
        # Clean up
        if driver:
            try:
                driver.quit()
                print("🔥 Firefox closed")
            except:
                pass
        
        if tor_process:
            try:
                tor_process.terminate()
                print("🔥 Tor stopped")
            except:
                pass

if __name__ == "__main__":
    quick_visual_test_firefox()
