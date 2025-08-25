#!/usr/bin/env python3
"""
Simple test for Dutch-only Tor with httpbin
"""

import requests
import json

def test_dutch_tor():
    """Test Dutch Tor connection"""
    print("🇳🇱 Testing Dutch Tor connection...")
    
    # Configure requests to use Tor proxy
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    
    try:
        # Test IP
        print("🌐 Getting IP from httpbin...")
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=30)
        ip_data = response.json()
        current_ip = ip_data['origin']
        print(f"📍 Current IP: {current_ip}")
        
        # Test geolocation
        print("🗺️  Checking geolocation...")
        geo_response = requests.get(f'http://ip-api.com/json/{current_ip}', timeout=30)
        geo_data = geo_response.json()
        
        country = geo_data.get('country', 'Unknown')
        country_code = geo_data.get('countryCode', 'Unknown')
        city = geo_data.get('city', 'Unknown')
        
        print(f"🏙️  Location: {city}, {country} ({country_code})")
        
        if country_code.lower() == 'nl':
            print("✅ SUCCESS: Using Dutch IP!")
            return True
        else:
            print(f"⚠️  WARNING: IP is from {country}, not Netherlands")
            return False
            
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

if __name__ == "__main__":
    test_dutch_tor()
