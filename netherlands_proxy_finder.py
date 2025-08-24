#!/usr/bin/env python3
"""
Netherlands Proxy Finder and Tester
Searches for and tests publicly available proxies from the Netherlands
"""

import requests
import json
import time
import random
from typing import List, Dict
from advanced_rotation import AdvancedProxyRotator, RotationConfig


def fetch_free_proxies_netherlands() -> List[str]:
    """Fetch free proxies from the Netherlands using various sources"""
    
    print("🔍 Searching for Netherlands proxies...")
    netherlands_proxies = []
    
    # Source 1: ProxyScrape API
    try:
        print("📡 Checking ProxyScrape API...")
        url = "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=NL&format=textplain"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            proxies = response.text.strip().split('\n')
            for proxy in proxies:
                if proxy.strip() and ':' in proxy:
                    netherlands_proxies.append(f"http://{proxy.strip()}")
            print(f"   ✅ Found {len(proxies)} proxies from ProxyScrape")
        else:
            print(f"   ❌ ProxyScrape failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ ProxyScrape error: {e}")
    
    # Source 2: Proxy-List.download API
    try:
        print("📡 Checking Proxy-List.download API...")
        url = "https://www.proxy-list.download/api/v1/get?type=http&country=NL"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            proxies = response.text.strip().split('\n')
            for proxy in proxies:
                if proxy.strip() and ':' in proxy:
                    proxy_url = f"http://{proxy.strip()}"
                    if proxy_url not in netherlands_proxies:
                        netherlands_proxies.append(proxy_url)
            print(f"   ✅ Found additional proxies from Proxy-List.download")
        else:
            print(f"   ❌ Proxy-List.download failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Proxy-List.download error: {e}")
    
    # Source 3: Manual curated list of known Netherlands proxies
    manual_nl_proxies = [
        # Add known working Netherlands proxies here
        # These are example formats - replace with actual working proxies
        # "http://proxy.nl.example.com:8080",
        # "http://amsterdam.proxy.com:3128",
    ]
    
    netherlands_proxies.extend(manual_nl_proxies)
    
    # Remove duplicates
    netherlands_proxies = list(set(netherlands_proxies))
    
    print(f"🇳🇱 Total Netherlands proxies found: {len(netherlands_proxies)}")
    return netherlands_proxies


def test_proxy_geolocation(proxy_url: str) -> Dict:
    """Test if proxy is actually from Netherlands"""
    
    try:
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        
        # Test with IP geolocation service
        response = requests.get(
            'http://ip-api.com/json/',
            proxies=proxies,
            timeout=10,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'working': True,
                'ip': data.get('query', 'Unknown'),
                'country': data.get('country', 'Unknown'),
                'countryCode': data.get('countryCode', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'isp': data.get('isp', 'Unknown')
            }
    except Exception as e:
        pass
    
    return {'working': False, 'error': 'Connection failed'}


def test_netherlands_proxies():
    """Find and test Netherlands proxies"""
    
    print("🇳🇱 Netherlands Proxy Hunter")
    print("=" * 30)
    
    # Fetch proxies
    nl_proxies = fetch_free_proxies_netherlands()
    
    if not nl_proxies:
        print("❌ No Netherlands proxies found from public sources")
        print("\n💡 Alternative sources to try:")
        print("   • https://free-proxy-list.net/ (filter by Netherlands)")
        print("   • https://www.sslproxies.org/ (manual search)")
        print("   • https://spys.one/en/free-proxy-list/ (advanced filters)")
        print("   • Premium services like Bright Data or Oxylabs")
        return
    
    print(f"\n🧪 Testing {min(10, len(nl_proxies))} proxies...")
    
    working_nl_proxies = []
    
    # Test first 10 proxies to avoid taking too long
    test_proxies = nl_proxies[:10]
    
    for i, proxy in enumerate(test_proxies):
        print(f"\n🔍 Testing proxy {i+1}/{len(test_proxies)}: {proxy}")
        
        result = test_proxy_geolocation(proxy)
        
        if result['working']:
            country = result.get('country', 'Unknown')
            country_code = result.get('countryCode', 'Unknown')
            city = result.get('city', 'Unknown')
            ip = result.get('ip', 'Unknown')
            
            print(f"   ✅ Working! IP: {ip}")
            print(f"   🌍 Location: {city}, {country} ({country_code})")
            
            if country_code == 'NL':
                print("   🇳🇱 Confirmed Netherlands proxy!")
                working_nl_proxies.append(proxy)
            else:
                print(f"   ⚠️  Not Netherlands - actually {country}")
        else:
            print("   ❌ Not working")
    
    print(f"\n🎯 RESULTS:")
    print(f"   📊 Tested: {len(test_proxies)} proxies")
    print(f"   ✅ Working Netherlands proxies: {len(working_nl_proxies)}")
    
    if working_nl_proxies:
        print(f"\n🚀 Testing rotation with working Netherlands proxies...")
        test_rotation_with_nl_proxies(working_nl_proxies)
    else:
        print(f"\n😔 No working Netherlands proxies found in this batch")
        print(f"💡 Try running again later or use premium proxy services")


def test_rotation_with_nl_proxies(proxies: List[str]):
    """Test the rotation system with working Netherlands proxies"""
    
    print(f"\n🔄 Testing Rotation System")
    print("=" * 25)
    
    config = RotationConfig(
        rotation_strategy='random',
        rotation_interval=1,
        timeout=8
    )
    
    rotator = AdvancedProxyRotator(config)
    rotator.add_proxy_list(proxies)
    
    print(f"🔧 Added {len(proxies)} Netherlands proxies to rotator")
    
    for i in range(min(5, len(proxies))):
        try:
            session, proxy, user_agent = rotator.get_session_with_rotation()
            
            print(f"\n🌐 Request {i+1}:")
            print(f"   🔗 Proxy: {proxy.host}:{proxy.port}" if proxy else "   🔗 Proxy: None")
            print(f"   🎭 User-Agent: {user_agent[:50]}...")
            
            # Test the request
            response = session.get('http://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                ip_data = response.json()
                print(f"   📍 IP: {ip_data.get('origin', 'Unknown')}")
                
                # Get location info
                geo_response = session.get('http://ip-api.com/json/', timeout=10)
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    location = f"{geo_data.get('city', 'Unknown')}, {geo_data.get('country', 'Unknown')}"
                    print(f"   🌍 Location: {location}")
            else:
                print(f"   ❌ Request failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(2)


def save_working_proxies(proxies: List[str]):
    """Save working Netherlands proxies to a config file"""
    
    if not proxies:
        return
        
    config_content = f'''# Working Netherlands Proxies - Generated {time.strftime("%Y-%m-%d %H:%M:%S")}

NETHERLANDS_PROXIES = [
'''
    
    for proxy in proxies:
        config_content += f'    "{proxy}",\n'
    
    config_content += ''']

# Usage example:
# from proxy_config import NETHERLANDS_PROXIES
# from human_browser import HumanBehaviorSimulator, BrowsingConfig
# 
# config = BrowsingConfig(
#     use_advanced_rotation=True,
#     use_proxy=True,
#     proxy_list=NETHERLANDS_PROXIES
# )
# simulator = HumanBehaviorSimulator(config)
'''
    
    with open('netherlands_proxies.py', 'w') as f:
        f.write(config_content)
    
    print(f"💾 Saved {len(proxies)} working proxies to netherlands_proxies.py")


if __name__ == "__main__":
    print("🔍 Netherlands Proxy Hunter & Tester")
    print("=" * 40)
    print("⚠️  Note: Free proxies may be slow or unreliable")
    print("💡 For production use, consider premium proxy services")
    print("")
    
    test_netherlands_proxies()
