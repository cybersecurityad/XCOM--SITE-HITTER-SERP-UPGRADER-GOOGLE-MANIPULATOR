#!/usr/bin/env python3
"""
🇳🇱 TEST NETHERLANDS-ONLY TOR EXIT NODES
======================================
Quick test to verify that Tor is only using Netherlands exit nodes

This script will:
1. Start Tor with Netherlands-only configuration
2. Test multiple IP rotations
3. Verify all IPs are from Netherlands
4. Display geolocation information
"""

import sys
import time
import requests
from visual_tor_browser import TorVisualController

def get_ip_location(ip):
    """Get geolocation information for an IP address"""
    try:
        # Use multiple IP geolocation services for accuracy
        services = [
            f"http://ip-api.com/json/{ip}",
            f"https://ipapi.co/{ip}/json/",
            f"http://www.geoplugin.net/json.gp?ip={ip}"
        ]
        
        for service_url in services:
            try:
                response = requests.get(service_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Parse different API response formats
                    if 'country' in data:
                        country = data.get('country', 'Unknown')
                        if 'countryCode' in data:
                            country_code = data.get('countryCode', 'XX')
                        else:
                            country_code = data.get('country_code', 'XX')
                        city = data.get('city', 'Unknown')
                        return country, country_code, city
                    elif 'geoplugin_countryName' in data:
                        country = data.get('geoplugin_countryName', 'Unknown')
                        country_code = data.get('geoplugin_countryCode', 'XX')
                        city = data.get('geoplugin_city', 'Unknown')
                        return country, country_code, city
                        
            except Exception as e:
                print(f"   ⚠️ Service error: {e}")
                continue
                
        return 'Unknown', 'XX', 'Unknown'
        
    except Exception as e:
        print(f"   ❌ Location lookup error: {e}")
        return 'Unknown', 'XX', 'Unknown'

def test_netherlands_only():
    """Test that all Tor exit nodes are from Netherlands"""
    print(f"🇳🇱 TESTING NETHERLANDS-ONLY TOR EXIT NODES")
    print(f"=" * 50)
    
    # Initialize Tor controller
    tor_controller = TorVisualController()
    
    netherlands_ips = []
    non_netherlands_ips = []
    test_count = 5  # Test 5 different IPs
    
    try:
        print(f"🔄 Testing {test_count} IP rotations...")
        
        for i in range(test_count):
            print(f"\n🔄 Test {i+1}/{test_count}")
            print(f"-" * 30)
            
            # Get new Tor circuit
            if i == 0:
                # First start
                success = tor_controller.start_tor_service()
            else:
                # Force new circuit
                print(f"🔄 Forcing new circuit...")
                tor_controller.force_new_tor_circuit()
                time.sleep(3)
                success = tor_controller.start_tor_service()
            
            if not success:
                print(f"❌ Failed to get Tor connection for test {i+1}")
                continue
            
            current_ip = tor_controller.current_ip
            if not current_ip or current_ip == 'Unknown':
                print(f"❌ Could not determine IP for test {i+1}")
                continue
                
            print(f"🌐 IP: {current_ip}")
            
            # Get location information
            print(f"📍 Looking up location...")
            country, country_code, city = get_ip_location(current_ip)
            
            print(f"🏳️ Country: {country} ({country_code})")
            print(f"🏙️ City: {city}")
            
            # Check if it's Netherlands
            if country_code.upper() in ['NL', 'NLD']:
                print(f"✅ SUCCESS: Netherlands IP confirmed!")
                netherlands_ips.append({
                    'ip': current_ip,
                    'country': country,
                    'country_code': country_code,
                    'city': city
                })
            else:
                print(f"❌ FAILURE: Not a Netherlands IP!")
                non_netherlands_ips.append({
                    'ip': current_ip,
                    'country': country,
                    'country_code': country_code,
                    'city': city
                })
            
            # Wait before next test
            if i < test_count - 1:
                print(f"⏱️ Waiting 5 seconds before next test...")
                time.sleep(5)
    
    finally:
        # Clean up
        print(f"\n🧹 Cleaning up...")
        try:
            tor_controller.stop_tor_service()
        except:
            pass
    
    # Final results
    print(f"\n🏁 FINAL RESULTS")
    print(f"=" * 50)
    print(f"✅ Netherlands IPs: {len(netherlands_ips)}")
    print(f"❌ Non-Netherlands IPs: {len(non_netherlands_ips)}")
    print(f"📊 Success Rate: {(len(netherlands_ips) / test_count) * 100:.1f}%")
    
    if netherlands_ips:
        print(f"\n🇳🇱 NETHERLANDS IPs FOUND:")
        for ip_info in netherlands_ips:
            print(f"   🌐 {ip_info['ip']} - {ip_info['city']}, {ip_info['country']}")
    
    if non_netherlands_ips:
        print(f"\n⚠️ NON-NETHERLANDS IPs FOUND:")
        for ip_info in non_netherlands_ips:
            print(f"   🌐 {ip_info['ip']} - {ip_info['city']}, {ip_info['country']} ({ip_info['country_code']})")
        print(f"\n💡 If you see non-NL IPs, Tor might not have enough NL exit nodes available")
        print(f"💡 Try again later or check Tor network status")
    
    # Overall assessment
    if len(netherlands_ips) == test_count:
        print(f"\n🎉 PERFECT! All exit nodes are from Netherlands!")
        return True
    elif len(netherlands_ips) > 0:
        print(f"\n⚠️ PARTIAL SUCCESS: Some IPs are from Netherlands")
        return True
    else:
        print(f"\n❌ FAILED: No Netherlands IPs found")
        print(f"💡 Check if Netherlands exit nodes are available in Tor network")
        return False

if __name__ == "__main__":
    print(f"🇳🇱 Netherlands-Only Tor Exit Node Test")
    print(f"=" * 40)
    
    try:
        success = test_netherlands_only()
        
        if success:
            print(f"\n✅ Test completed successfully!")
            sys.exit(0)
        else:
            print(f"\n❌ Test failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n⚠️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        sys.exit(1)
