"""
Proxy rotation and IP management for web automation
"""

import random
import requests
import time
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ProxyConfig:
    """Configuration for proxy rotation"""
    proxy_list: List[str]
    rotation_interval: int = 5  # Change proxy every N requests
    timeout: int = 10
    verify_ssl: bool = False


class ProxyRotator:
    """Handles proxy rotation and validation"""
    
    def __init__(self, config: ProxyConfig):
        self.config = config
        self.current_proxy_index = 0
        self.request_count = 0
        self.working_proxies = []
        self._validate_proxies()
    
    def _validate_proxies(self):
        """Test proxies to ensure they're working"""
        print("Validating proxies...")
        for proxy in self.config.proxy_list:
            if self._test_proxy(proxy):
                self.working_proxies.append(proxy)
                print(f"✓ Proxy working: {proxy}")
            else:
                print(f"✗ Proxy failed: {proxy}")
    
    def _test_proxy(self, proxy: str) -> bool:
        """Test if a proxy is working"""
        try:
            proxies = {
                'http': proxy,
                'https': proxy
            }
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxies,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            return response.status_code == 200
        except:
            return False
    
    def get_current_proxy(self) -> Optional[str]:
        """Get the current proxy"""
        if not self.working_proxies:
            return None
        return self.working_proxies[self.current_proxy_index]
    
    def rotate_proxy(self):
        """Rotate to the next proxy"""
        if self.working_proxies:
            self.current_proxy_index = (self.current_proxy_index + 1) % len(self.working_proxies)
            print(f"Rotated to proxy: {self.get_current_proxy()}")
    
    def should_rotate(self) -> bool:
        """Check if it's time to rotate proxy"""
        self.request_count += 1
        return self.request_count % self.config.rotation_interval == 0


# Example free proxy list (for testing only - use premium services for production)
FREE_PROXY_LIST = [
    # Note: Free proxies are unreliable and may not work
    # Consider using premium proxy services for production use
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    # Add your proxy servers here
]


def get_random_user_agent() -> str:
    """Get a random user agent string"""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0"
    ]
    return random.choice(user_agents)
