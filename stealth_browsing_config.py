
# Maximum stealth configuration
from human_browser import HumanBehaviorSimulator, BrowsingConfig

# Option A: Proxy-based stealth
STEALTH_PROXIES = [
    # Add your proxy servers here
    # "http://user:pass@proxy1.com:8080",
    # "http://user:pass@proxy2.com:8080",
]

stealth_config = BrowsingConfig(
    # Advanced rotation
    use_advanced_rotation=True,
    rotation_interval=1,  # Change IP every request
    rotation_strategy='random',
    
    # Realistic behavior
    use_realistic_user_agents=True,
    min_scroll_delay=2.0,
    max_scroll_delay=5.0,
    
    # Proxy settings
    use_proxy=True,
    proxy_list=STEALTH_PROXIES,
    
    # Extended delays for stealth
    page_load_timeout=30
)

# Option B: Tor-based stealth (requires Tor running)
def create_tor_browser():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    options = Options()
    options.add_argument('--proxy-server=socks5://127.0.0.1:9050')  # Tor proxy
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    return webdriver.Chrome(options=options)

# Option C: VPN + Proxy combination
vpn_proxy_config = BrowsingConfig(
    use_advanced_rotation=True,
    use_proxy=True,
    proxy_list=STEALTH_PROXIES,  # Even with VPN, add proxy layer
    rotation_interval=3,
    use_realistic_user_agents=True
)
