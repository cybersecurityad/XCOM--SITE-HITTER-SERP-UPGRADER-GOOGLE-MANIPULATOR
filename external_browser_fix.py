#!/usr/bin/env python3
"""
� EXTERNAL BROWSER FIX - No Exit Code 15
==========================================
Uses regular Selenium WebDriver instead of undetected_chromedriver
to avoid the startup hanging issue that causes VS Code to kill the process.
"""

import os
import sys
import time
import subprocess
import signal
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

def create_external_script():
    """Create a browser automation script that runs externally"""
    
    external_script = '''#!/usr/bin/env python3
"""
External browser automation - runs outside VS Code
"""

import time
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

def start_tor():
    print("🧅 Starting Tor...")
    try:
        subprocess.run(['pkill', '-f', 'tor'], capture_output=True)
        time.sleep(2)
    except:
        pass
    
    tor_process = subprocess.Popen(['tor'], 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL)
    
    # Wait for Tor
    for i in range(30):
        time.sleep(1)
        try:
            proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
            if r.status_code == 200:
                ip = r.json().get('origin', 'Unknown')
                print(f"✅ Tor ready: {ip}")
                return tor_process, ip
        except:
            if i % 5 == 0:
                print(f"⏳ Waiting for Tor... {i}/30")
    
    print("❌ Tor timeout")
    return None, None

def run_browser_automation():
    print("🌐 EXTERNAL BROWSER AUTOMATION")
    print("=" * 40)
    print("🎯 Running OUTSIDE VS Code to avoid crashes")
    print("=" * 40)
    
    try:
        # Start Tor
        tor_process, ip = start_tor()
        if not tor_process:
            print("❌ Tor failed")
            return False
        
        print(f"✅ Connected via Tor: {ip}")
        
        # Configure Firefox
        options = FirefoxOptions()
        options.set_preference('network.proxy.type', 1)
        options.set_preference('network.proxy.socks', '127.0.0.1')
        options.set_preference('network.proxy.socks_port', 9050)
        options.set_preference('network.proxy.socks_remote_dns', True)
        options.set_preference('permissions.default.image', 2)
        
        # Remove headless to see the browser
        # options.add_argument('--headless')
        
        print("🌐 Starting Firefox...")
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(30)
        
        # Test with the real target site
        target_url = "https://verenigdamsterdam.nl"
        print(f"🎯 Loading: {target_url}")
        
        driver.get(target_url)
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        print(f"✅ Page loaded: {driver.title}")
        print("👁️ Browser window should be visible with the website")
        print("⏱️ Browser will stay open for 30 seconds...")
        
        # Keep browser open
        time.sleep(30)
        
        # Cleanup
        driver.quit()
        tor_process.terminate()
        
        print("✅ External automation completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ External automation failed: {e}")
        return False

if __name__ == "__main__":
    success = run_browser_automation()
    sys.exit(0 if success else 1)
'''
    
    # Write the external script
    script_path = '/tmp/external_browser_automation.py'
    with open(script_path, 'w') as f:
        f.write(external_script)
    
    os.chmod(script_path, 0o755)
    return script_path

def run_external_automation():
    """Run browser automation in external process"""
    print("🚀 LAUNCHING EXTERNAL BROWSER AUTOMATION")
    print("=" * 50)
    print("🎯 Goal: Avoid VS Code exit code 15 crashes")
    print("💡 Strategy: Run completely outside VS Code process")
    print("=" * 50)
    
    try:
        # Create external script
        script_path = create_external_script()
        print(f"📝 Created external script: {script_path}")
        
        # Activate virtual environment and run
        venv_python = '/Users/_akira/CSAD/websites-new-2025/seo-crawler/.venv/bin/python3'
        
        print("🚀 Launching external process...")
        print("👁️ This will open a Firefox window with the website")
        print("⚠️ Do NOT close this terminal while browser is running")
        
        # Run in external process completely isolated from VS Code
        result = subprocess.run([
            venv_python, script_path
        ], cwd='/Users/_akira/CSAD/websites-new-2025/seo-crawler')
        
        if result.returncode == 0:
            print("🎉 EXTERNAL AUTOMATION SUCCESS!")
            print("✅ No VS Code crashes detected")
            print("✅ Browser automation completed")
        else:
            print(f"❌ External automation failed with code: {result.returncode}")
        
        # Clean up
        os.remove(script_path)
        
    except KeyboardInterrupt:
        print("\n⚠️ External automation interrupted")
    except Exception as e:
        print(f"❌ External automation error: {e}")

def main():
    """Main function"""
    print("🔧 VS CODE EXIT CODE 15 SOLUTION")
    print("=" * 40)
    print("🎯 Running browser automation externally")
    print("💡 This avoids VS Code process conflicts")
    print("=" * 40)
    
    # Check if we have the required tools
    print("🔍 Checking requirements...")
    
    # Check if we're in the right directory
    if not os.path.exists('.venv'):
        print("❌ Virtual environment not found")
        print("💡 Please run this from the project directory")
        return
    
    print("✅ Virtual environment found")
    
    # Check if Tor is available
    try:
        subprocess.run(['which', 'tor'], check=True, capture_output=True)
        print("✅ Tor available")
    except subprocess.CalledProcessError:
        print("❌ Tor not found - please install: brew install tor")
        return
    
    # Check if Firefox is available
    if os.path.exists('/Applications/Firefox.app'):
        print("✅ Firefox available")
    else:
        print("❌ Firefox not found - please install Firefox")
        return
    
    print("\n🚀 All requirements met - starting external automation...")
    
    # Run external automation
    run_external_automation()

if __name__ == "__main__":
    main()
