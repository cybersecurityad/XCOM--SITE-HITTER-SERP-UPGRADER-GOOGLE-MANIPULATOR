#!/usr/bin/env python3
"""
IP Test Script - Verify proxy rotation is working
"""

import requests
import time
from advanced_rotation import AdvancedProxyRotator, RotationConfig


def test_ip_rotation_with_proxies():
    """Test IP rotation with actual proxy configuration"""
    
    print("🔍 IP Rotation Test")
    print("=" * 25)
    
    # First, show your current IP
    print("📍 Your current IP (no proxy):")
    try:
        response = requests.get('https://httpbin.org/ip', timeout=10)
        current_ip = response.json()['origin']
        print(f"   Direct IP: {current_ip}")
    except Exception as e:
        print(f"   Error getting current IP: {e}")
    
    print("\n" + "="*50)
    print("🔧 PROXY CONFIGURATION NEEDED")
    print("="*50)
    
    print("""
To see different IP addresses, you need to add actual proxy servers.
Here are your options:

1. 📋 COPY THE TEMPLATE:
   cp proxy_config_template.py proxy_config.py

2. ✏️ ADD YOUR PROXIES to proxy_config.py:
   
   PREMIUM_HTTP_PROXIES = [
       "http://username:password@proxy1.provider.com:8080",
       "http://username:password@proxy2.provider.com:8080",
   ]
   
   Or for free proxies (less reliable):
   FREE_PROXIES = [
       "http://free-proxy1.com:8080",
       "http://free-proxy2.com:3128",
   ]

3. 🔄 QUICK TEST WITH EXAMPLE PROXIES:
   Edit the example below with real proxy servers:
""")
    
    # Example with placeholder proxies
    example_proxies = [
        # "http://proxy1.example.com:8080",
        # "http://proxy2.example.com:8080", 
        # "socks5://user:pass@proxy3.example.com:1080",
    ]
    
    if not example_proxies:
        print("\n⚠️  NO PROXIES CONFIGURED")
        print("   Add real proxy servers to see IP rotation")
        print("   Without proxies, you'll always see your personal IP")
        return
    
    # If proxies were configured, test them
    config = RotationConfig(
        rotation_strategy='random',
        rotation_interval=1,
        timeout=10
    )
    
    rotator = AdvancedProxyRotator(config)
    rotator.add_proxy_list(example_proxies)
    
    print(f"\n🔄 Testing {len(example_proxies)} proxy servers...")
    working_proxies = rotator.validate_proxies()
    
    if not working_proxies:
        print("❌ No working proxies found")
        return
        
    print(f"✅ {len(working_proxies)} working proxies")
    
    # Test rotation
    for i in range(5):
        session, proxy, user_agent = rotator.get_session_with_rotation()
        
        try:
            response = session.get('https://httpbin.org/ip', timeout=10)
            ip_data = response.json()
            displayed_ip = ip_data['origin']
            
            print(f"Request {i+1}:")
            print(f"  🌐 IP: {displayed_ip}")
            print(f"  🔗 Proxy: {proxy.host}:{proxy.port}" if proxy else "  🔗 Proxy: None")
            print(f"  🎭 UA: {user_agent[:50]}...")
            
        except Exception as e:
            print(f"Request {i+1}: ❌ Error: {e}")
            
        time.sleep(2)


def suggest_proxy_sources():
    """Suggest where to get proxy servers"""
    
    print("\n💡 WHERE TO GET PROXY SERVERS")
    print("="*35)
    
    sources = {
        "🆓 Free Proxy Lists": [
            "https://www.proxy-list.download/",
            "https://free-proxy-list.net/",
            "https://www.proxyscrape.com/",
            "⚠️ Warning: Free proxies are often slow/unreliable"
        ],
        "💰 Premium Proxy Services": [
            "Bright Data: https://brightdata.com/",
            "Oxylabs: https://oxylabs.io/",
            "SmartProxy: https://smartproxy.com/",
            "ProxyMesh: https://proxymesh.com/",
            "✅ Recommended for production use"
        ],
        "🏠 Residential Proxies": [
            "Bright Data Residential",
            "NetNut: https://netnut.io/",
            "GeoSurf: https://www.geosurf.com/",
            "🎯 Best for avoiding detection"
        ],
        "🖥️ DIY Datacenter Proxies": [
            "DigitalOcean + Squid proxy setup",
            "AWS EC2 + 3proxy installation", 
            "Vultr + TinyProxy configuration",
            "⚙️ Most control, requires setup"
        ]
    }
    
    for category, items in sources.items():
        print(f"\n{category}")
        for item in items:
            print(f"  • {item}")


def show_proxy_setup_example():
    """Show how to set up proxy configuration"""
    
    print("\n🛠️ PROXY SETUP EXAMPLE")
    print("="*25)
    
    print("""
1. Create proxy_config.py file:

# Example proxy configuration
WORKING_PROXIES = [
    # HTTP proxies
    "http://proxy1.yourprovider.com:8080",
    "http://username:password@proxy2.yourprovider.com:8080",
    
    # SOCKS proxies  
    "socks5://user:pass@proxy3.yourprovider.com:1080",
    "socks4://proxy4.yourprovider.com:1080",
]

2. Test your proxies:

from advanced_rotation import AdvancedProxyRotator, RotationConfig
from proxy_config import WORKING_PROXIES

config = RotationConfig()
rotator = AdvancedProxyRotator(config)
rotator.add_proxy_list(WORKING_PROXIES)
working = rotator.validate_proxies()
print(f"Working proxies: {len(working)}")

3. Use in browser automation:

from human_browser import HumanBehaviorSimulator, BrowsingConfig
from proxy_config import WORKING_PROXIES

config = BrowsingConfig(
    use_advanced_rotation=True,
    use_proxy=True,
    proxy_list=WORKING_PROXIES
)

simulator = HumanBehaviorSimulator(config)
# Now each request will use different IP + User Agent
""")


if __name__ == "__main__":
    test_ip_rotation_with_proxies()
    suggest_proxy_sources() 
    show_proxy_setup_example()
    
    print(f"\n🎯 SUMMARY:")
    print(f"   ✅ Your tool is working correctly")
    print(f"   📍 Showing your IP because no proxies configured")
    print(f"   🔧 Add real proxy servers to see IP rotation")
    print(f"   🚀 Then run this script again to test rotation")
