#!/usr/bin/env python3
"""
Advanced Web Automation with Proxy & User Agent Rotation
Demonstrates comprehensive rotation strategies for cybersecurity testing
"""

import time
import random
from human_browser import HumanBehaviorSimulator, BrowsingConfig
from advanced_rotation import AdvancedProxyRotator, RotationConfig, UserAgentManager


def demo_basic_rotation():
    """Demonstrate basic user agent and proxy rotation"""
    print("🔄 Basic Rotation Demo")
    print("=" * 30)
    
    # Example proxy list (add your own proxies here)
    example_proxies = [
        # "http://proxy1.example.com:8080",
        # "http://proxy2.example.com:8080",
        # "socks5://proxy3.example.com:1080",
    ]
    
    config = BrowsingConfig(
        min_scroll_delay=1.0,
        max_scroll_delay=2.0,
        use_advanced_rotation=True,
        rotation_interval=2,  # Rotate every 2 requests
        rotation_strategy='random',
        use_realistic_user_agents=True,
        use_proxy=len(example_proxies) > 0,
        proxy_list=example_proxies if example_proxies else None
    )
    
    simulator = HumanBehaviorSimulator(config)
    
    try:
        test_urls = [
            "https://httpbin.org/headers",  # Shows headers including User-Agent
            "https://httpbin.org/ip",       # Shows IP address
            "https://httpbin.org/user-agent",  # Shows User-Agent
        ]
        
        for i, url in enumerate(test_urls):
            print(f"\n🌐 Request {i+1}: {url}")
            simulator.browse_page(url, ['read', 'scroll'])
            time.sleep(3)
            
    finally:
        simulator.close()


def demo_advanced_user_agent_rotation():
    """Demonstrate advanced user agent management"""
    print("\n🎭 Advanced User Agent Rotation Demo")
    print("=" * 40)
    
    ua_manager = UserAgentManager()
    
    print("🖥️ Desktop User Agents:")
    for i in range(5):
        ua = ua_manager.get_realistic_user_agent()
        print(f"  {i+1}. {ua}")
        
    print("\n📱 Mobile User Agents:")
    for i in range(3):
        ua = ua_manager.get_mobile_user_agent()
        print(f"  {i+1}. {ua}")


def demo_proxy_strategies():
    """Demonstrate different proxy rotation strategies"""
    print("\n🔄 Proxy Rotation Strategies Demo")
    print("=" * 35)
    
    # Example proxy configuration
    example_proxies = [
        # Add your proxy servers here
        # {"host": "proxy1.example.com", "port": 8080, "proxy_type": "http"},
        # {"host": "proxy2.example.com", "port": 8080, "proxy_type": "http"},
        # {"host": "proxy3.example.com", "port": 1080, "proxy_type": "socks5"},
    ]
    
    if not example_proxies:
        print("⚠️ No proxies configured. Add your proxy servers to test rotation strategies.")
        return
    
    strategies = ['round_robin', 'random', 'weighted']
    
    for strategy in strategies:
        print(f"\n📊 Testing {strategy} strategy:")
        
        config = RotationConfig(
            rotation_strategy=strategy,
            rotation_interval=1
        )
        
        rotator = AdvancedProxyRotator(config)
        rotator.add_proxy_servers(example_proxies)
        
        # Simulate requests
        for i in range(5):
            proxy = rotator.get_next_proxy()
            if proxy:
                print(f"  Request {i+1}: {proxy.host}:{proxy.port}")
            time.sleep(0.5)


def suggest_proxy_sources():
    """Suggest different types of proxy sources and implementation ideas"""
    print("\n💡 Proxy Source Suggestions & Implementation Ideas")
    print("=" * 55)
    
    suggestions = {
        "Free Proxy Sources": {
            "description": "Not recommended for production use",
            "sources": [
                "ProxyList.geonode.com API",
                "Free-proxy-list.net scraping",
                "ProxyScrape.com API",
                "GitHub proxy lists"
            ],
            "pros": ["Free", "Easy to get started"],
            "cons": ["Unreliable", "Slow", "Often blocked", "Security risks"]
        },
        
        "Premium Proxy Services": {
            "description": "Recommended for professional use",
            "sources": [
                "Bright Data (formerly Luminati)",
                "Oxylabs",
                "SmartProxy",
                "ProxyMesh",
                "Storm Proxies"
            ],
            "pros": ["Reliable", "Fast", "Geographic targeting", "Support"],
            "cons": ["Expensive", "Usage limits"]
        },
        
        "Residential Proxies": {
            "description": "Most authentic for avoiding detection",
            "sources": [
                "Bright Data Residential",
                "Oxylabs Residential",
                "NetNut",
                "GeoSurf",
                "Soax"
            ],
            "pros": ["Real user IPs", "Hard to detect", "High success rate"],
            "cons": ["Most expensive", "Slower", "Ethical considerations"]
        },
        
        "Datacenter Proxies": {
            "description": "Good balance of speed and cost",
            "sources": [
                "DigitalOcean + Proxy software",
                "AWS + Squid proxy",
                "Vultr + 3proxy",
                "Linode + TinyProxy"
            ],
            "pros": ["Fast", "Controllable", "Cost-effective at scale"],
            "cons": ["Easier to detect", "Setup required"]
        }
    }
    
    for category, info in suggestions.items():
        print(f"\n🏷️ {category}")
        print(f"   📝 {info['description']}")
        print(f"   🔗 Sources: {', '.join(info['sources'])}")
        print(f"   ✅ Pros: {', '.join(info['pros'])}")
        print(f"   ❌ Cons: {', '.join(info['cons'])}")


def implementation_ideas():
    """Suggest advanced implementation ideas"""
    print("\n🚀 Advanced Implementation Ideas")
    print("=" * 35)
    
    ideas = [
        {
            "title": "IP Geolocation Rotation",
            "description": "Rotate proxies based on target website's geography",
            "implementation": [
                "Use MaxMind GeoIP database",
                "Group proxies by country/region",
                "Rotate within same geography for consistency"
            ]
        },
        {
            "title": "Browser Fingerprint Rotation",
            "description": "Change browser characteristics beyond just User-Agent",
            "implementation": [
                "Rotate screen resolution",
                "Change timezone settings",
                "Modify language preferences",
                "Alter canvas fingerprints"
            ]
        },
        {
            "title": "Timing Pattern Randomization",
            "description": "Make request timing appear more human",
            "implementation": [
                "Analyze real user behavior patterns",
                "Implement burst/pause cycles",
                "Add randomized idle periods",
                "Simulate day/night usage patterns"
            ]
        },
        {
            "title": "Session Management",
            "description": "Maintain consistent sessions across requests",
            "implementation": [
                "Cookie persistence per proxy/UA combo",
                "Session state tracking",
                "Login state management",
                "Form data persistence"
            ]
        },
        {
            "title": "Health Monitoring & Auto-Recovery",
            "description": "Intelligent proxy health management",
            "implementation": [
                "Real-time proxy speed testing",
                "Automatic proxy replacement",
                "Ban detection algorithms",
                "Proxy pool auto-scaling"
            ]
        }
    ]
    
    for i, idea in enumerate(ideas, 1):
        print(f"\n💡 {i}. {idea['title']}")
        print(f"   📄 {idea['description']}")
        for step in idea['implementation']:
            print(f"   • {step}")


def main():
    """Run all demonstrations and suggestions"""
    print("🎯 Cybersecurity Web Automation: Advanced Rotation System")
    print("=" * 60)
    
    # Run demonstrations
    demo_advanced_user_agent_rotation()
    demo_basic_rotation()
    demo_proxy_strategies()
    
    # Show suggestions
    suggest_proxy_sources()
    implementation_ideas()
    
    print(f"\n✅ Demo completed! Check the files:")
    print(f"   • human_browser.py - Enhanced with rotation support")
    print(f"   • advanced_rotation.py - Advanced rotation system")
    print(f"   • This file - Comprehensive examples")
    
    print(f"\n⚠️ Remember:")
    print(f"   • Only use on authorized systems")
    print(f"   • Respect rate limits and robots.txt")
    print(f"   • Use premium proxies for production")
    print(f"   • Monitor for detection and adapt accordingly")


if __name__ == "__main__":
    main()
