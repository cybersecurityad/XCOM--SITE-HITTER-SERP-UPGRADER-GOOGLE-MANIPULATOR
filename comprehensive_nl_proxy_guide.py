#!/usr/bin/env python3
"""
Comprehensive Netherlands Proxy Sources
Multiple methods to obtain Netherlands proxies for testing
"""

import requests
import json
import time
from typing import List, Dict


def try_multiple_free_sources() -> List[str]:
    """Try multiple free proxy sources for Netherlands"""
    
    print("🔍 Trying Multiple Free Proxy Sources...")
    all_proxies = []
    
    sources = [
        {
            'name': 'ProxyScrape HTTP',
            'url': 'https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=5000&country=NL&format=textplain',
            'format': 'text'
        },
        {
            'name': 'ProxyScrape SOCKS4',
            'url': 'https://api.proxyscrape.com/v2/?request=get&protocol=socks4&timeout=5000&country=NL&format=textplain',
            'format': 'text'
        },
        {
            'name': 'ProxyScrape SOCKS5',
            'url': 'https://api.proxyscrape.com/v2/?request=get&protocol=socks5&timeout=5000&country=NL&format=textplain',
            'format': 'text'
        },
        {
            'name': 'FreeProxyList',
            'url': 'https://www.proxy-list.download/api/v1/get?type=http&country=NL',
            'format': 'text'
        }
    ]
    
    for source in sources:
        try:
            print(f"📡 Checking {source['name']}...")
            response = requests.get(source['url'], timeout=15)
            
            if response.status_code == 200 and response.text.strip():
                proxies = response.text.strip().split('\n')
                valid_proxies = []
                
                for proxy in proxies:
                    proxy = proxy.strip()
                    if proxy and ':' in proxy and len(proxy.split(':')) == 2:
                        # Add protocol prefix based on source
                        if 'socks4' in source['name'].lower():
                            proxy_url = f"socks4://{proxy}"
                        elif 'socks5' in source['name'].lower():
                            proxy_url = f"socks5://{proxy}"
                        else:
                            proxy_url = f"http://{proxy}"
                        
                        if proxy_url not in all_proxies:
                            valid_proxies.append(proxy_url)
                            all_proxies.append(proxy_url)
                
                print(f"   ✅ Found {len(valid_proxies)} unique proxies")
            else:
                print(f"   ❌ No data returned")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🎯 Total unique Netherlands proxies: {len(all_proxies)}")
    return all_proxies


def test_proxy_quick(proxy_url: str) -> bool:
    """Quick test if proxy responds"""
    try:
        if proxy_url.startswith('socks'):
            # For SOCKS proxies, we'd need special handling
            return False
        
        proxies = {'http': proxy_url, 'https': proxy_url}
        response = requests.get(
            'http://httpbin.org/ip',
            proxies=proxies,
            timeout=5,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        return response.status_code == 200
    except:
        return False


def suggest_premium_netherlands_providers():
    """Suggest reliable premium Netherlands proxy providers"""
    
    print("\n💰 PREMIUM NETHERLANDS PROXY PROVIDERS")
    print("=" * 45)
    
    providers = [
        {
            'name': 'Bright Data (Luminati)',
            'netherlands': True,
            'types': ['Residential', 'Datacenter', 'Mobile'],
            'pricing': '$500+/month',
            'pros': ['Most reliable', 'Largest pool', 'Real Netherlands IPs'],
            'cons': ['Expensive', 'Complex setup'],
            'url': 'https://brightdata.com/'
        },
        {
            'name': 'Oxylabs',
            'netherlands': True,
            'types': ['Residential', 'Datacenter'],
            'pricing': '$300+/month',
            'pros': ['Good Netherlands coverage', 'Professional support'],
            'cons': ['Expensive', 'Enterprise focused'],
            'url': 'https://oxylabs.io/'
        },
        {
            'name': 'SmartProxy',
            'netherlands': True,
            'types': ['Residential'],
            'pricing': '$75+/month',
            'pros': ['Affordable', 'Good performance', 'Netherlands IPs'],
            'cons': ['Limited datacenter options'],
            'url': 'https://smartproxy.com/'
        },
        {
            'name': 'NetNut',
            'netherlands': True,
            'types': ['Residential', 'Static Residential'],
            'pricing': '$300+/month',
            'pros': ['High-speed', 'Netherlands coverage'],
            'cons': ['Expensive'],
            'url': 'https://netnut.io/'
        },
        {
            'name': 'ProxyMesh',
            'netherlands': False,
            'types': ['Datacenter'],
            'pricing': '$10+/month',
            'pros': ['Cheap', 'Simple'],
            'cons': ['No Netherlands specific', 'Limited locations'],
            'url': 'https://proxymesh.com/'
        }
    ]
    
    for provider in providers:
        print(f"\n🏢 {provider['name']}")
        print(f"   🇳🇱 Netherlands IPs: {'✅ Yes' if provider['netherlands'] else '❌ No'}")
        print(f"   🔗 Types: {', '.join(provider['types'])}")
        print(f"   💰 Pricing: {provider['pricing']}")
        print(f"   ✅ Pros: {', '.join(provider['pros'])}")
        print(f"   ❌ Cons: {', '.join(provider['cons'])}")
        print(f"   🌐 URL: {provider['url']}")


def suggest_diy_netherlands_setup():
    """Suggest DIY Netherlands proxy setup"""
    
    print("\n🛠️ DIY NETHERLANDS PROXY SETUP")
    print("=" * 35)
    
    print("""
💡 Create Your Own Netherlands Proxy Server:

1. 🇳🇱 RENT NETHERLANDS VPS:
   • DigitalOcean Amsterdam: $6/month
   • Vultr Amsterdam: $6/month  
   • Linode Amsterdam: $5/month
   • Hetzner Germany (close): $4/month

2. 🔧 INSTALL PROXY SOFTWARE:
   
   # Option A: Squid Proxy
   sudo apt update
   sudo apt install squid
   sudo nano /etc/squid/squid.conf
   # Add: http_access allow all
   # Add: http_port 3128
   sudo systemctl restart squid
   
   # Option B: 3proxy
   wget https://github.com/z3APA3A/3proxy/archive/0.9.3.tar.gz
   tar -xzf 0.9.3.tar.gz
   cd 3proxy-0.9.3
   make -f Makefile.Linux
   sudo make -f Makefile.Linux install

3. 🔐 SECURE YOUR PROXY:
   • Set up authentication
   • Configure firewall
   • Use non-standard ports
   • Monitor usage

4. 💰 COST BREAKDOWN:
   • Netherlands VPS: $5-6/month
   • Setup time: 1-2 hours
   • Maintenance: Minimal
   • Total: ~$60/year for dedicated Netherlands IP

5. 🎯 USAGE:
   proxy_url = "http://your-username:password@your-nl-server.com:3128"
""")


def create_test_with_working_examples():
    """Create test script with example working setup"""
    
    print("\n📝 CREATING TEST SCRIPT WITH EXAMPLES")
    print("=" * 40)
    
    test_script = '''#!/usr/bin/env python3
"""
Netherlands Proxy Test - Add your real proxies here
"""

from human_browser import HumanBehaviorSimulator, BrowsingConfig
import requests

# 🔧 ADD YOUR REAL NETHERLANDS PROXIES HERE:
NETHERLANDS_PROXIES = [
    # Example formats (replace with real proxies):
    # "http://username:password@nl-proxy1.provider.com:8080",
    # "http://username:password@nl-proxy2.provider.com:8080", 
    # "socks5://user:pass@amsterdam-proxy.com:1080",
    
    # 🆓 Free proxies (often don't work):
    # "http://94.100.18.111:3128",  # Amsterdam (may not work)
    # "http://188.166.30.17:8888",  # Netherlands (may not work)
]

def test_netherlands_rotation():
    """Test Netherlands proxy rotation"""
    
    if not NETHERLANDS_PROXIES:
        print("⚠️  No proxies configured!")
        print("   Add real Netherlands proxies to NETHERLANDS_PROXIES list")
        print("   Check the suggestions for premium providers or DIY setup")
        return
    
    config = BrowsingConfig(
        use_advanced_rotation=True,
        rotation_interval=2,
        rotation_strategy='random',
        use_realistic_user_agents=True,
        use_proxy=True,
        proxy_list=NETHERLANDS_PROXIES
    )
    
    simulator = HumanBehaviorSimulator(config)
    
    try:
        test_urls = [
            "https://httpbin.org/ip",
            "https://httpbin.org/headers",
            "http://ip-api.com/json/"
        ]
        
        for i, url in enumerate(test_urls):
            print(f"\\n🌐 Request {i+1}: {url}")
            simulator.browse_page(url, ['read'])
            
            # Check the current IP
            try:
                response = requests.get('http://ip-api.com/json/', timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    print(f"   📍 Current IP: {data.get('query', 'Unknown')}")
                    print(f"   🌍 Location: {data.get('city', 'Unknown')}, {data.get('country', 'Unknown')}")
            except:
                pass
                
    finally:
        simulator.close()

if __name__ == "__main__":
    test_netherlands_rotation()
'''
    
    with open('test_netherlands_proxies.py', 'w') as f:
        f.write(test_script)
    
    print("✅ Created test_netherlands_proxies.py")
    print("   Edit the NETHERLANDS_PROXIES list with real proxy servers")


def main():
    """Main function to run all tests and suggestions"""
    
    print("🇳🇱 Netherlands Proxy Comprehensive Guide")
    print("=" * 45)
    
    # Try free sources first
    free_proxies = try_multiple_free_sources()
    
    if free_proxies:
        print(f"\n🧪 Quick testing {min(5, len(free_proxies))} proxies...")
        working = 0
        
        for i, proxy in enumerate(free_proxies[:5]):
            print(f"   Testing {i+1}: {proxy[:30]}...")
            if test_proxy_quick(proxy):
                print(f"   ✅ Working!")
                working += 1
            else:
                print(f"   ❌ Failed")
        
        print(f"\n📊 Results: {working}/{min(5, len(free_proxies))} working")
        
        if working == 0:
            print("😔 No free proxies working (this is normal)")
    
    # Show premium options
    suggest_premium_netherlands_providers()
    
    # Show DIY setup
    suggest_diy_netherlands_setup()
    
    # Create test script
    create_test_with_working_examples()
    
    print(f"\n🎯 NEXT STEPS:")
    print(f"   1. 🆓 Free proxies rarely work reliably")
    print(f"   2. 💰 Consider premium service for $75+/month")
    print(f"   3. 🛠️ DIY VPS setup for $6/month")
    print(f"   4. ✏️ Edit test_netherlands_proxies.py with real proxies")
    print(f"   5. 🚀 Run: python test_netherlands_proxies.py")


if __name__ == "__main__":
    main()
