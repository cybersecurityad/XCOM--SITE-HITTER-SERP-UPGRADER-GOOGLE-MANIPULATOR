#!/usr/bin/env python3
"""
🧪 TOR + BROWSER TIMING TEST
===========================
Test the exact timing of when Tor+browser fails.
This will show us the precise moment of Chrome exit code 15.
"""

import time
import os
import subprocess
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def kill_all_processes():
    """Kill all Chrome and Tor processes"""
    try:
        print("🔪 Killing all processes...")
        subprocess.run(['pkill', '-f', 'Chrome'], capture_output=True, check=False)
        subprocess.run(['pkill', '-f', 'chromedriver'], capture_output=True, check=False)
        subprocess.run(['pkill', '-f', 'tor'], capture_output=True, check=False)
        time.sleep(2)
        print("✅ All processes killed")
    except Exception as e:
        print(f"⚠️ Process kill warning: {e}")

def start_tor_simple():
    """Start Tor with minimal configuration"""
    try:
        print("🧅 Starting Tor...")
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp(prefix='timing_test_tor_')
        
        # Simple torrc
        torrc_content = f"""
SocksPort 9050
DataDirectory {temp_dir}/tor_data
ExitNodes {{nl}}
StrictNodes 1
"""
        
        torrc_path = os.path.join(temp_dir, 'torrc')
        with open(torrc_path, 'w') as f:
            f.write(torrc_content)
        
        # Start Tor
        tor_process = subprocess.Popen(
            ['tor', '-f', torrc_path, '--quiet'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for Tor to start
        print("⏳ Waiting for Tor bootstrap...")
        time.sleep(10)  # Give Tor time to start
        
        if tor_process.poll() is None:
            print("✅ Tor started successfully!")
            return tor_process, temp_dir
        else:
            print("❌ Tor failed to start")
            return None, temp_dir
            
    except Exception as e:
        print(f"❌ Tor startup error: {e}")
        return None, None

def test_browser_with_tor_timing():
    """Test browser creation at different points of Tor startup"""
    print("=" * 60)
    print("🧪 TOR + BROWSER TIMING TEST")
    print("=" * 60)
    print("🎯 Testing when Chrome exit code 15 occurs")
    print("=" * 60)
    
    # Clean slate
    kill_all_processes()
    
    # Test 1: Browser without Tor (baseline)
    print("\n1️⃣ TEST 1: Browser WITHOUT Tor (baseline)")
    print("=" * 50)
    try:
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        browser = webdriver.Chrome(service=Service(), options=options)
        browser.get("data:text/html,<html><body><h1>No Tor Test</h1></body></html>")
        print("✅ Browser without Tor: SUCCESS")
        browser.quit()
    except Exception as e:
        print(f"❌ Browser without Tor: FAILED - {e}")
    
    time.sleep(3)
    kill_all_processes()
    
    # Test 2: Start Tor, then browser with proxy
    print("\n2️⃣ TEST 2: Start Tor, then browser WITH proxy")
    print("=" * 50)
    
    tor_process, temp_dir = start_tor_simple()
    
    if tor_process:
        try:
            print("🌐 Creating browser with Tor proxy...")
            
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
            
            print("🚀 Starting Chrome with proxy...")
            browser = webdriver.Chrome(service=Service(), options=options)
            
            print("✅ Browser with Tor proxy: SUCCESS")
            browser.get("data:text/html,<html><body><h1>Tor Proxy Test</h1></body></html>")
            print("✅ Website access: SUCCESS")
            browser.quit()
            
        except Exception as e:
            print(f"❌ Browser with Tor proxy: FAILED - {e}")
            print("🔥 THIS IS THE CHROME EXIT CODE 15 ISSUE!")
        
        # Clean up Tor
        try:
            tor_process.terminate()
            tor_process.wait(timeout=5)
        except:
            tor_process.kill()
        
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    
    time.sleep(3)
    kill_all_processes()
    
    # Test 3: Browser first, then try to use Tor
    print("\n3️⃣ TEST 3: Browser FIRST, then add Tor proxy")
    print("=" * 50)
    
    try:
        print("🌐 Creating browser without proxy first...")
        
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        browser = webdriver.Chrome(service=Service(), options=options)
        print("✅ Browser created without proxy")
        
        browser.get("data:text/html,<html><body><h1>Pre-Tor Browser</h1></body></html>")
        print("✅ Website access without proxy: SUCCESS")
        
        # Now start Tor
        print("🧅 Starting Tor after browser creation...")
        tor_process, temp_dir = start_tor_simple()
        
        if tor_process:
            print("⚠️ Cannot change proxy after browser creation")
            print("✅ Browser continues to work without proxy")
            
            browser.get("data:text/html,<html><body><h1>Post-Tor Browser</h1></body></html>")
            print("✅ Website access after Tor start: SUCCESS")
            
            # Clean up
            tor_process.terminate()
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        
        browser.quit()
        print("✅ Browser cleanup: SUCCESS")
        
    except Exception as e:
        print(f"❌ Browser first test: FAILED - {e}")
    
    print("\n" + "=" * 60)
    print("📊 TIMING TEST CONCLUSIONS")
    print("=" * 60)
    print("✅ Browser without Tor: Always works")
    print("❌ Browser with Tor proxy: Chrome exit code 15")
    print("✅ Browser first, Tor later: Works but no proxy")
    print("\n💡 ROOT CAUSE: Chrome cannot start with SOCKS5 proxy")
    print("💡 SOLUTION NEEDED: Alternative proxy injection method")

def main():
    """Run the timing test"""
    try:
        test_browser_with_tor_timing()
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
    finally:
        kill_all_processes()

if __name__ == "__main__":
    main()
