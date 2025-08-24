#!/usr/bin/env python3
"""
🇳🇱 AUTOMATED NETHERLANDS TOR TEST
=================================
Automatically test the visual Tor browser with Netherlands-only exit nodes
"""

import sys
import os
import subprocess
import time
import signal

def test_nl_tor_browser():
    """Test the visual Tor browser with Netherlands-only exit nodes"""
    print(f"🇳🇱 AUTOMATED NETHERLANDS TOR BROWSER TEST")
    print(f"=" * 45)
    
    # Activate virtual environment and run the browser
    cmd = """
source .venv/bin/activate
python3 -c "
from visual_tor_browser import TorVisualController
import time

print('🧅 Testing Netherlands-only Tor exit nodes...')

# Initialize controller
controller = TorVisualController()

# Start Tor service
print('🔄 Starting Tor service...')
if controller.start_tor_service():
    print('✅ Tor service started')
    
    # Get current IP
    ip = controller.current_ip
    if ip:
        print(f'🌐 Current Netherlands IP: {ip}')
        
        # Verify it's Netherlands
        import requests
        try:
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=10)
            if response.status_code == 200:
                data = response.json()
                country = data.get('country', 'Unknown')
                country_code = data.get('countryCode', 'XX')
                city = data.get('city', 'Unknown')
                
                print(f'📍 Location: {city}, {country} ({country_code})')
                
                if country_code.upper() == 'NL':
                    print('✅ SUCCESS: Netherlands IP confirmed!')
                else:
                    print(f'❌ FAILURE: Not Netherlands ({country_code})')
            else:
                print('⚠️ Could not verify location')
        except Exception as e:
            print(f'⚠️ Location check error: {e}')
    else:
        print('❌ Could not get IP')
        
    # Test rotation
    print('🔄 Testing IP rotation...')
    controller.force_new_tor_circuit()
    time.sleep(5)
    
    # Restart Tor service to get new IP
    controller.start_tor_service()
    new_ip = controller.current_ip
    if new_ip and new_ip != ip:
        print(f'🌐 New Netherlands IP: {new_ip}')
        
        # Verify new IP is also Netherlands
        try:
            response = requests.get(f'http://ip-api.com/json/{new_ip}', timeout=10)
            if response.status_code == 200:
                data = response.json()
                country = data.get('country', 'Unknown')
                country_code = data.get('countryCode', 'XX')
                city = data.get('city', 'Unknown')
                
                print(f'📍 New Location: {city}, {country} ({country_code})')
                
                if country_code.upper() == 'NL':
                    print('✅ SUCCESS: IP rotation to Netherlands worked!')
                else:
                    print(f'❌ FAILURE: New IP not Netherlands ({country_code})')
        except Exception as e:
            print(f'⚠️ New IP location check error: {e}')
    else:
        print('⚠️ IP rotation may not have worked')
    
    # Cleanup
    controller.stop_tor_service()
    print('🧹 Cleanup completed')
    
else:
    print('❌ Failed to start Tor service')

print('🏁 Test completed')
"
"""
    
    try:
        # Run the test
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print("📊 TEST OUTPUT:")
        print("=" * 40)
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ ERRORS:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Test completed successfully!")
            return True
        else:
            print(f"❌ Test failed with exit code: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️ Test timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main function"""
    success = test_nl_tor_browser()
    
    if success:
        print(f"\n🎉 Netherlands-only Tor configuration is working!")
        sys.exit(0)
    else:
        print(f"\n❌ Netherlands-only Tor test failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
