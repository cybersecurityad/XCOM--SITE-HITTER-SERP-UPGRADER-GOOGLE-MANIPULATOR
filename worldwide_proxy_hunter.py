#!/usr/bin/env python3
"""
Worldwide Free Proxy Hunter
Search for free proxies from multiple countries for IP rotation
"""

import requests
import json
import time
import random
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch_proxies_by_country(country_code: str = None) -> List[Dict]:
    """Fetch free proxies from multiple sources worldwide"""
    
    print(f"🌍 Searching for proxies{' from ' + country_code if country_code else ' worldwide'}...")
    all_proxies = []
    
    # Multiple free proxy sources
    sources = [
        {
            'name': 'ProxyScrape HTTP',
            'url': f'https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=5000&format=textplain{f"&country={country_code}" if country_code else ""}',
            'type': 'http'
        },
        {
            'name': 'ProxyScrape SOCKS4',
            'url': f'https://api.proxyscrape.com/v2/?request=get&protocol=socks4&timeout=5000&format=textplain{f"&country={country_code}" if country_code else ""}',
            'type': 'socks4'
        },
        {
            'name': 'ProxyScrape SOCKS5', 
            'url': f'https://api.proxyscrape.com/v2/?request=get&protocol=socks5&timeout=5000&format=textplain{f"&country={country_code}" if country_code else ""}',
            'type': 'socks5'
        },
        {
            'name': 'Proxy-List.download',
            'url': f'https://www.proxy-list.download/api/v1/get?type=http{f"&country={country_code}" if country_code else ""}',
            'type': 'http'
        },
        {
            'name': 'GeoNode',
            'url': 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc',
            'type': 'json'
        }
    ]
    
    for source in sources:
        try:
            print(f"📡 Checking {source['name']}...")
            response = requests.get(source['url'], timeout=15)
            
            if response.status_code == 200 and response.text.strip():
                if source['type'] == 'json':
                    # Handle JSON response (GeoNode)
                    try:
                        data = response.json()
                        if 'data' in data:
                            for proxy in data['data']:
                                proxy_info = {
                                    'ip': proxy.get('ip'),
                                    'port': proxy.get('port'),
                                    'country': proxy.get('country'),
                                    'protocol': proxy.get('protocols', ['http'])[0],
                                    'url': f"http://{proxy.get('ip')}:{proxy.get('port')}",
                                    'source': source['name']
                                }
                                all_proxies.append(proxy_info)
                    except:
                        pass
                else:
                    # Handle text response
                    proxies = response.text.strip().split('\n')
                    for proxy in proxies:
                        proxy = proxy.strip()
                        if proxy and ':' in proxy and len(proxy.split(':')) == 2:
                            ip, port = proxy.split(':')
                            proxy_info = {
                                'ip': ip,
                                'port': int(port),
                                'country': country_code or 'Unknown',
                                'protocol': source['type'],
                                'url': f"{source['type']}://{proxy}",
                                'source': source['name']
                            }
                            all_proxies.append(proxy_info)
                
                print(f"   ✅ Found {len([p for p in all_proxies if p['source'] == source['name']])} proxies")
            else:
                print(f"   ❌ No data returned")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Remove duplicates
    unique_proxies = []
    seen = set()
    for proxy in all_proxies:
        proxy_key = f"{proxy['ip']}:{proxy['port']}"
        if proxy_key not in seen:
            seen.add(proxy_key)
            unique_proxies.append(proxy)
    
    print(f"🎯 Total unique proxies: {len(unique_proxies)}")
    return unique_proxies


def test_proxy_with_location(proxy_info: Dict) -> Dict:
    """Test proxy and get its real location"""
    
    try:
        if proxy_info['protocol'] in ['socks4', 'socks5']:
            # Skip SOCKS for now (needs special handling)
            return {'working': False, 'reason': 'SOCKS not supported in basic test'}
        
        proxies = {
            'http': proxy_info['url'],
            'https': proxy_info['url']
        }
        
        # Test basic connectivity
        response = requests.get(
            'http://httpbin.org/ip',
            proxies=proxies,
            timeout=8,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        
        if response.status_code == 200:
            ip_data = response.json()
            current_ip = ip_data.get('origin', '').split(',')[0]  # Sometimes returns multiple IPs
            
            # Get geolocation
            geo_response = requests.get(
                f'http://ip-api.com/json/{current_ip}',
                timeout=5
            )
            
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                return {
                    'working': True,
                    'ip': current_ip,
                    'country': geo_data.get('country', 'Unknown'),
                    'country_code': geo_data.get('countryCode', 'Unknown'),
                    'city': geo_data.get('city', 'Unknown'),
                    'isp': geo_data.get('isp', 'Unknown'),
                    'proxy_info': proxy_info
                }
            else:
                return {
                    'working': True,
                    'ip': current_ip,
                    'country': 'Unknown',
                    'proxy_info': proxy_info
                }
        
    except Exception as e:
        return {'working': False, 'reason': str(e), 'proxy_info': proxy_info}
    
    return {'working': False, 'reason': 'Connection failed', 'proxy_info': proxy_info}


def test_proxies_parallel(proxies: List[Dict], max_workers: int = 10) -> List[Dict]:
    """Test multiple proxies in parallel"""
    
    print(f"🧪 Testing {len(proxies)} proxies (max {max_workers} concurrent)...")
    working_proxies = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all proxy tests
        future_to_proxy = {
            executor.submit(test_proxy_with_location, proxy): proxy 
            for proxy in proxies
        }
        
        completed = 0
        for future in as_completed(future_to_proxy):
            completed += 1
            result = future.result()
            
            if result['working']:
                working_proxies.append(result)
                country = result.get('country', 'Unknown')
                city = result.get('city', 'Unknown') 
                ip = result.get('ip', 'Unknown')
                print(f"   ✅ {completed}/{len(proxies)} - {ip} ({city}, {country})")
            else:
                reason = result.get('reason', 'Failed')[:30]
                print(f"   ❌ {completed}/{len(proxies)} - {reason}")
    
    return working_proxies


def search_worldwide_proxies():
    """Search for free proxies from multiple countries"""
    
    print("🌍 WORLDWIDE FREE PROXY SEARCH")
    print("=" * 35)
    
    # Countries to search (ISO 2-letter codes)
    target_countries = [
        ('US', 'United States'),
        ('GB', 'United Kingdom'), 
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('NL', 'Netherlands'),
        ('CA', 'Canada'),
        ('AU', 'Australia'),
        ('JP', 'Japan'),
        ('SG', 'Singapore'),
        ('BR', 'Brazil')
    ]
    
    all_working_proxies = []
    
    # Search each country
    for country_code, country_name in target_countries:
        print(f"\n🔍 Searching {country_name} ({country_code})...")
        proxies = fetch_proxies_by_country(country_code)
        
        if proxies:
            # Test first 5 proxies from each country to save time
            test_proxies = proxies[:5]
            working = test_proxies_parallel(test_proxies, max_workers=3)
            all_working_proxies.extend(working)
            
            if working:
                print(f"   🎯 Found {len(working)} working {country_name} proxies")
            else:
                print(f"   😔 No working {country_name} proxies")
        else:
            print(f"   ❌ No {country_name} proxies found")
    
    # Also search without country filter (global)
    print(f"\n🌐 Searching global proxy lists...")
    global_proxies = fetch_proxies_by_country()
    if global_proxies:
        # Test first 10 global proxies
        test_proxies = global_proxies[:10]
        working = test_proxies_parallel(test_proxies, max_workers=5)
        all_working_proxies.extend(working)
        print(f"   🎯 Found {len(working)} additional working proxies")
    
    return all_working_proxies


def create_rotation_config(working_proxies: List[Dict]):
    """Create configuration file with working proxies"""
    
    if not working_proxies:
        print("❌ No working proxies to save")
        return
    
    # Group by country
    by_country = {}
    for proxy in working_proxies:
        country = proxy.get('country', 'Unknown')
        if country not in by_country:
            by_country[country] = []
        by_country[country].append(proxy)
    
    config_content = f'''# Free Worldwide Proxies - Generated {time.strftime("%Y-%m-%d %H:%M:%S")}
# Found {len(working_proxies)} working proxies from {len(by_country)} countries

'''
    
    # Create country-specific lists
    for country, proxies in by_country.items():
        safe_country = country.replace(' ', '_').replace('-', '_').upper()
        config_content += f'{safe_country}_PROXIES = [\n'
        for proxy in proxies:
            proxy_info = proxy['proxy_info']
            city = proxy.get('city', 'Unknown')
            isp = proxy.get('isp', 'Unknown')[:30]
            config_content += f'    "{proxy_info["url"]}",  # {city}, {country} - {isp}\n'
        config_content += ']\n\n'
    
    # Create combined list
    config_content += 'ALL_WORKING_PROXIES = [\n'
    for proxy in working_proxies:
        proxy_info = proxy['proxy_info']
        country = proxy.get('country', 'Unknown')
        city = proxy.get('city', 'Unknown')
        config_content += f'    "{proxy_info["url"]}",  # {city}, {country}\n'
    config_content += ']\n\n'
    
    # Add usage example
    config_content += '''# Usage Example:
from human_browser import HumanBehaviorSimulator, BrowsingConfig

# Use all proxies for maximum rotation
config = BrowsingConfig(
    use_advanced_rotation=True,
    rotation_interval=2,  # Change every 2 requests
    rotation_strategy='random',
    use_realistic_user_agents=True,
    use_proxy=True,
    proxy_list=ALL_WORKING_PROXIES
)

simulator = HumanBehaviorSimulator(config)
# Now you have rotating IPs from multiple countries!
'''
    
    filename = 'worldwide_working_proxies.py'
    with open(filename, 'w') as f:
        f.write(config_content)
    
    print(f"💾 Saved {len(working_proxies)} working proxies to {filename}")
    
    # Show summary
    print(f"\n📊 PROXY SUMMARY:")
    for country, proxies in by_country.items():
        print(f"   🌍 {country}: {len(proxies)} proxies")


def main():
    """Main function"""
    
    print("🚀 Free Worldwide Proxy Hunter")
    print("=" * 32)
    print("⚠️  Note: Free proxies are often unreliable")
    print("💡 This finds working ones for testing rotation")
    print("")
    
    # Search worldwide
    working_proxies = search_worldwide_proxies()
    
    print(f"\n🎯 FINAL RESULTS:")
    print(f"   ✅ Working proxies found: {len(working_proxies)}")
    
    if working_proxies:
        # Create config file
        create_rotation_config(working_proxies)
        
        print(f"\n🚀 NEXT STEPS:")
        print(f"   1. Check worldwide_working_proxies.py")
        print(f"   2. Import: from worldwide_working_proxies import ALL_WORKING_PROXIES")
        print(f"   3. Use in your browser automation for IP rotation")
        print(f"   4. Each request will use different country's IP!")
        
        # Show sample
        print(f"\n🌍 SAMPLE WORKING PROXIES:")
        for i, proxy in enumerate(working_proxies[:5]):
            country = proxy.get('country', 'Unknown')
            city = proxy.get('city', 'Unknown')
            ip = proxy.get('ip', 'Unknown')
            print(f"   {i+1}. {ip} - {city}, {country}")
    else:
        print(f"\n😔 No working proxies found this time")
        print(f"   💡 Try running again later")
        print(f"   💰 Consider premium services for reliable rotation")


if __name__ == "__main__":
    main()
