"""
Advanced Proxy and User Agent Rotation System
Supports multiple proxy types and comprehensive user agent rotation
"""

import random
import requests
import time
import json
import threading
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from fake_useragent import UserAgent
import itertools


@dataclass
class ProxyServer:
    """Individual proxy server configuration"""
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    proxy_type: str = 'http'  # http, https, socks4, socks5
    country: Optional[str] = None
    speed_ms: Optional[int] = None
    last_used: Optional[float] = None
    success_rate: float = 1.0
    consecutive_failures: int = 0
    
    @property
    def url(self) -> str:
        """Get proxy URL with authentication"""
        if self.username and self.password:
            return f"{self.proxy_type}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.proxy_type}://{self.host}:{self.port}"
    
    @property
    def is_healthy(self) -> bool:
        """Check if proxy is considered healthy"""
        return self.consecutive_failures < 3 and self.success_rate > 0.3


@dataclass
class RotationConfig:
    """Configuration for rotation strategies"""
    user_agent_rotation: bool = True
    proxy_rotation: bool = True
    rotation_interval: int = 5  # requests between rotations
    max_retries: int = 3
    timeout: int = 10
    verify_ssl: bool = False
    rotation_strategy: str = 'round_robin'  # round_robin, random, weighted, country_based
    

class UserAgentManager:
    """Advanced user agent management with device/browser simulation"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.custom_agents = []
        self.browser_stats = self._get_realistic_browser_stats()
        
    def _get_realistic_browser_stats(self) -> Dict[str, float]:
        """Realistic browser market share for more authentic rotation"""
        return {
            'chrome': 0.65,
            'firefox': 0.15,
            'safari': 0.12,
            'edge': 0.05,
            'opera': 0.03
        }
    
    def get_realistic_user_agent(self) -> str:
        """Get user agent based on realistic browser distribution"""
        browser = random.choices(
            list(self.browser_stats.keys()),
            weights=list(self.browser_stats.values())
        )[0]
        
        try:
            if browser == 'chrome':
                return self.ua.chrome
            elif browser == 'firefox':
                return self.ua.firefox
            elif browser == 'safari':
                return self.ua.safari
            elif browser == 'edge':
                return self.ua.edge
            else:
                return self.ua.random
        except:
            return self._get_fallback_user_agent()
    
    def _get_fallback_user_agent(self) -> str:
        """Fallback user agents if fake_useragent fails"""
        fallback_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
        ]
        return random.choice(fallback_agents)
    
    def add_custom_user_agent(self, user_agent: str):
        """Add custom user agent to rotation pool"""
        self.custom_agents.append(user_agent)
    
    def get_mobile_user_agent(self) -> str:
        """Get mobile-specific user agent"""
        mobile_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        ]
        return random.choice(mobile_agents)


class AdvancedProxyRotator:
    """Advanced proxy rotation with health monitoring and smart selection"""
    
    def __init__(self, config: RotationConfig):
        self.config = config
        self.proxies: List[ProxyServer] = []
        self.current_proxy_index = 0
        self.request_count = 0
        self.user_agent_manager = UserAgentManager()
        self.proxy_cycle = None
        self._lock = threading.Lock()
        
    def add_proxy_list(self, proxy_list: List[str], proxy_type: str = 'http'):
        """Add multiple proxies from list"""
        for proxy_url in proxy_list:
            self.add_proxy_from_url(proxy_url, proxy_type)
    
    def add_proxy_from_url(self, proxy_url: str, proxy_type: str = 'http'):
        """Parse and add proxy from URL string"""
        try:
            # Parse different proxy URL formats
            if '://' in proxy_url:
                parts = proxy_url.split('://', 1)[1]
            else:
                parts = proxy_url
                
            if '@' in parts:
                auth_part, host_part = parts.split('@', 1)
                username, password = auth_part.split(':', 1)
                host, port = host_part.split(':', 1)
            else:
                username = password = None
                host, port = parts.split(':', 1)
                
            proxy = ProxyServer(
                host=host,
                port=int(port),
                username=username,
                password=password,
                proxy_type=proxy_type
            )
            self.proxies.append(proxy)
            
        except Exception as e:
            print(f"Error parsing proxy {proxy_url}: {e}")
    
    def add_proxy_servers(self, servers: List[Dict]):
        """Add proxy servers from configuration dictionaries"""
        for server_config in servers:
            proxy = ProxyServer(**server_config)
            self.proxies.append(proxy)
    
    def validate_proxies(self) -> List[ProxyServer]:
        """Test all proxies and return working ones"""
        print(f"Validating {len(self.proxies)} proxies...")
        working_proxies = []
        
        for i, proxy in enumerate(self.proxies):
            print(f"Testing proxy {i+1}/{len(self.proxies)}: {proxy.host}:{proxy.port}")
            
            if self._test_proxy(proxy):
                working_proxies.append(proxy)
                print(f"✓ Proxy working: {proxy.host}:{proxy.port}")
            else:
                print(f"✗ Proxy failed: {proxy.host}:{proxy.port}")
                
        self.proxies = working_proxies
        self._initialize_cycle()
        return working_proxies
    
    def _test_proxy(self, proxy: ProxyServer) -> bool:
        """Test individual proxy with multiple test URLs"""
        test_urls = [
            'http://httpbin.org/ip',
            'http://icanhazip.com',
            'http://ident.me'
        ]
        
        proxies_dict = {
            'http': proxy.url,
            'https': proxy.url
        }
        
        for test_url in test_urls:
            try:
                start_time = time.time()
                response = requests.get(
                    test_url,
                    proxies=proxies_dict,
                    timeout=self.config.timeout,
                    verify=self.config.verify_ssl,
                    headers={'User-Agent': self.user_agent_manager.get_realistic_user_agent()}
                )
                
                if response.status_code == 200:
                    proxy.speed_ms = int((time.time() - start_time) * 1000)
                    return True
                    
            except Exception as e:
                continue
                
        proxy.consecutive_failures += 1
        return False
    
    def _initialize_cycle(self):
        """Initialize proxy cycling based on strategy"""
        if self.config.rotation_strategy == 'round_robin':
            self.proxy_cycle = itertools.cycle(range(len(self.proxies)))
        elif self.config.rotation_strategy == 'random':
            self.proxy_cycle = None  # Handle in get_next_proxy
        elif self.config.rotation_strategy == 'weighted':
            # Weight by success rate and inverse of speed
            weights = []
            for proxy in self.proxies:
                weight = proxy.success_rate
                if proxy.speed_ms:
                    weight *= (1000 / proxy.speed_ms)  # Faster = higher weight
                weights.append(weight)
            self.proxy_weights = weights
    
    def get_current_proxy(self) -> Optional[ProxyServer]:
        """Get current active proxy"""
        if not self.proxies:
            return None
        return self.proxies[self.current_proxy_index]
    
    def get_next_proxy(self) -> Optional[ProxyServer]:
        """Get next proxy based on rotation strategy"""
        if not self.proxies:
            return None
            
        with self._lock:
            if self.config.rotation_strategy == 'round_robin':
                self.current_proxy_index = next(self.proxy_cycle)
            elif self.config.rotation_strategy == 'random':
                self.current_proxy_index = random.randint(0, len(self.proxies) - 1)
            elif self.config.rotation_strategy == 'weighted':
                self.current_proxy_index = random.choices(
                    range(len(self.proxies)),
                    weights=self.proxy_weights
                )[0]
            
            proxy = self.proxies[self.current_proxy_index]
            proxy.last_used = time.time()
            return proxy
    
    def mark_proxy_success(self, proxy: ProxyServer):
        """Mark proxy as successful"""
        proxy.consecutive_failures = 0
        proxy.success_rate = min(1.0, proxy.success_rate + 0.1)
    
    def mark_proxy_failure(self, proxy: ProxyServer):
        """Mark proxy as failed"""
        proxy.consecutive_failures += 1
        proxy.success_rate = max(0.0, proxy.success_rate - 0.2)
    
    def should_rotate(self) -> bool:
        """Check if rotation should occur"""
        self.request_count += 1
        return self.request_count % self.config.rotation_interval == 0
    
    def get_proxy_dict(self, proxy: ProxyServer) -> Dict[str, str]:
        """Get proxy dictionary for requests"""
        return {
            'http': proxy.url,
            'https': proxy.url
        }
    
    def get_session_with_rotation(self) -> Tuple[requests.Session, ProxyServer, str]:
        """Get configured session with proxy and user agent"""
        session = requests.Session()
        
        # Get current or next proxy
        if self.should_rotate() or not self.get_current_proxy():
            proxy = self.get_next_proxy()
        else:
            proxy = self.get_current_proxy()
            
        if proxy:
            session.proxies.update(self.get_proxy_dict(proxy))
            
        # Set user agent
        user_agent = self.user_agent_manager.get_realistic_user_agent()
        session.headers.update({'User-Agent': user_agent})
        
        return session, proxy, user_agent


def load_proxy_sources() -> Dict[str, List[str]]:
    """Load proxies from various sources - implement your proxy sources here"""
    
    # Example proxy sources (replace with your actual proxy services)
    proxy_sources = {
        'free_proxies': [
            # Note: Free proxies are unreliable - use premium services for production
            # 'http://proxy1.example.com:8080',
            # 'http://proxy2.example.com:8080',
        ],
        'premium_service_1': [
            # Add your premium proxy service URLs here
            # 'http://username:password@premium1.proxy.com:8080',
        ],
        'residential_proxies': [
            # Add residential proxy service URLs here
            # 'http://user:pass@residential.proxy.com:8080',
        ]
    }
    
    return proxy_sources


def main():
    """Example usage of advanced proxy rotation"""
    print("🔄 Advanced Proxy & User Agent Rotation System")
    print("=" * 50)
    
    # Configuration
    config = RotationConfig(
        user_agent_rotation=True,
        proxy_rotation=True,
        rotation_interval=3,
        rotation_strategy='random',
        timeout=10
    )
    
    # Initialize rotator
    rotator = AdvancedProxyRotator(config)
    
    # Load proxy sources
    proxy_sources = load_proxy_sources()
    
    # Add proxies from different sources
    for source_name, proxy_list in proxy_sources.items():
        if proxy_list:  # Only add if not empty
            print(f"Adding {len(proxy_list)} proxies from {source_name}")
            rotator.add_proxy_list(proxy_list)
    
    if not rotator.proxies:
        print("⚠️ No proxies configured. Add your proxy servers to test rotation.")
        print("Example usage without proxies:")
        
        # Demonstrate user agent rotation without proxies
        for i in range(5):
            user_agent = rotator.user_agent_manager.get_realistic_user_agent()
            print(f"Request {i+1} User-Agent: {user_agent[:80]}...")
            time.sleep(1)
        return
    
    # Validate proxies
    working_proxies = rotator.validate_proxies()
    
    if not working_proxies:
        print("❌ No working proxies found.")
        return
    
    print(f"✅ {len(working_proxies)} working proxies found")
    
    # Test rotation
    for i in range(10):
        session, proxy, user_agent = rotator.get_session_with_rotation()
        
        print(f"\n🔄 Request {i+1}:")
        print(f"  Proxy: {proxy.host}:{proxy.port}" if proxy else "  Proxy: None")
        print(f"  User-Agent: {user_agent[:60]}...")
        
        try:
            # Test request
            response = session.get('http://httpbin.org/ip', timeout=config.timeout)
            if response.status_code == 200:
                ip_data = response.json()
                print(f"  ✅ IP: {ip_data.get('origin', 'Unknown')}")
                if proxy:
                    rotator.mark_proxy_success(proxy)
            else:
                print(f"  ❌ Request failed: {response.status_code}")
                if proxy:
                    rotator.mark_proxy_failure(proxy)
                    
        except Exception as e:
            print(f"  ❌ Request error: {e}")
            if proxy:
                rotator.mark_proxy_failure(proxy)
        
        time.sleep(2)


if __name__ == "__main__":
    main()
