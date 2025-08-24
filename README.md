# Cybersecurity Web Automation Tool

A sophisticated Python-based web automation tool designed for cybersecurity professionals to simulate human-like browsing behavior with advanced IP rotation and user agent management for security testing and research purposes.

## 🚀 Advanced Features

- **Human-like Browsing**: Simulates natural browsing patterns with random scrolling, clicking, and reading behaviors
- **Advanced Proxy Rotation**: Intelligent proxy management with health monitoring and multiple rotation strategies
- **Realistic User Agent Rotation**: Smart user agent distribution based on real browser market share
- **Stealth Mode**: Uses undetected Chrome driver with advanced anti-detection techniques
- **Geographic IP Targeting**: Support for country-based proxy rotation
- **Session Management**: Maintains consistent sessions across requests
- **Health Monitoring**: Real-time proxy performance tracking and auto-recovery

## 📁 Project Structure

```
├── human_browser.py              # Main automation engine
├── human_browser_standard.py     # Alternative standard implementation
├── advanced_rotation.py          # Advanced proxy & user agent rotation
├── proxy_manager.py             # Basic proxy management
├── rotation_demo.py             # Comprehensive demonstration
├── example_usage.py             # Usage examples
├── test_simple.py              # Simple test script
├── proxy_config_template.py    # Configuration template
├── requirements.txt            # Dependencies
└── .env.example               # Environment variables
```

## 🎯 Quick Start

### Basic Usage with Advanced Rotation

```python
from human_browser import HumanBehaviorSimulator, BrowsingConfig

# Configure advanced rotation
config = BrowsingConfig(
    min_scroll_delay=1.0,
    max_scroll_delay=3.0,
    use_advanced_rotation=True,
    rotation_interval=5,
    rotation_strategy='random',
    use_realistic_user_agents=True,
    use_proxy=True,
    proxy_list=["http://proxy1:8080", "http://proxy2:8080"]
)

# Initialize and use
simulator = HumanBehaviorSimulator(config)
simulator.browse_page("https://example.com", ["read", "scroll", "click_random"])
simulator.close()
```

### Advanced Proxy Management

```python
from advanced_rotation import AdvancedProxyRotator, RotationConfig, UserAgentManager

# Setup advanced rotation
rotation_config = RotationConfig(
    rotation_strategy='weighted',  # or 'round_robin', 'random'
    rotation_interval=3,
    timeout=10
)

rotator = AdvancedProxyRotator(rotation_config)
rotator.add_proxy_list([
    "http://proxy1:8080",
    "socks5://user:pass@proxy2:1080"
])

# Validate and use
working_proxies = rotator.validate_proxies()
session, proxy, user_agent = rotator.get_session_with_rotation()
```

### Quick Test

```bash
# Simple test
python test_simple.py

# Advanced rotation demo
python rotation_demo.py

# Full feature demo
python example_usage.py
```

## ⚙️ Configuration Options

### Advanced BrowsingConfig
- `use_advanced_rotation`: Enable sophisticated rotation system
- `rotation_interval`: Requests between rotations (default: 5)
- `rotation_strategy`: 'round_robin', 'random', 'weighted' (default: 'random')
- `use_realistic_user_agents`: Use market-share based user agents
- `use_mobile_agents`: Include mobile user agents in rotation
- `min_scroll_delay`/`max_scroll_delay`: Timing between scrolls
- `use_proxy`: Enable proxy rotation
- `proxy_list`: List of proxy servers to rotate through

### Proxy Types Supported
- **HTTP/HTTPS proxies**: `http://proxy:8080`
- **SOCKS4/5 proxies**: `socks5://user:pass@proxy:1080`
- **Authenticated proxies**: `http://user:pass@proxy:8080`

### Rotation Strategies
- **Round Robin**: Sequential rotation through proxy list
- **Random**: Random selection from available proxies
- **Weighted**: Performance-based proxy selection
- **Geographic**: Country/region-based rotation (planned)

## 💡 Advanced Implementation Ideas

### 1. **IP Geolocation Rotation**
```python
# Group proxies by country for consistent geographic targeting
datacenter_proxies = {
    "US": ["http://us1.proxy.com:8080", "http://us2.proxy.com:8080"],
    "EU": ["http://eu1.proxy.com:8080", "http://eu2.proxy.com:8080"],
    "ASIA": ["http://asia1.proxy.com:8080"]
}
```

### 2. **Browser Fingerprint Randomization**
- Rotate screen resolution and viewport size
- Change timezone and language settings
- Modify canvas and WebGL fingerprints
- Randomize installed fonts and plugins

### 3. **Intelligent Timing Patterns**
- Simulate realistic day/night usage patterns
- Implement burst/pause cycles
- Add weekend/weekday behavior differences
- Human-like idle periods between sessions

### 4. **Session Persistence**
- Maintain cookies per proxy/user-agent combination
- Track login states across rotations
- Preserve form data and shopping carts
- Handle multi-step authentication flows

### 5. **Health Monitoring & Auto-Recovery**
- Real-time proxy speed and success rate tracking
- Automatic bad proxy detection and replacement
- Ban detection algorithms with auto-switching
- Proxy pool auto-scaling based on demand

## 🔧 Proxy Source Recommendations

### Free Sources (Testing Only)
- ProxyList.geonode.com API
- Free-proxy-list.net scraping  
- ProxyScrape.com API
- ⚠️ **Not recommended for production**

### Premium Services (Recommended)
- **Bright Data** - Industry leader, expensive but reliable
- **Oxylabs** - Good balance of features and price
- **SmartProxy** - Affordable residential proxies
- **ProxyMesh** - Simple HTTP proxies
- **Storm Proxies** - Budget-friendly option

### Self-Hosted Options
- **DigitalOcean + Squid** - DIY datacenter proxies
- **AWS + 3proxy** - Scalable cloud-based solution
- **Vultr + TinyProxy** - Lightweight proxy setup

## Ethical Usage

This tool is designed for legitimate cybersecurity testing and research purposes only:

- ✅ Security testing of your own applications
- ✅ Authorized penetration testing
- ✅ Research and educational purposes
- ✅ Bug bounty programs with proper authorization

- ❌ Unauthorized access to systems
- ❌ Malicious activities
- ❌ Violating terms of service
- ❌ Any illegal activities

## Legal Disclaimer

Users are responsible for ensuring their use of this tool complies with all applicable laws and regulations. Only use this tool on systems you own or have explicit permission to test.

## Dependencies

- `selenium`: Web browser automation
- `undetected-chromedriver`: Stealth Chrome driver
- `fake-useragent`: Random user agent generation
- `requests`: HTTP library for proxy testing
- `beautifulsoup4`: HTML parsing (optional)

## Contributing

Contributions are welcome! Please ensure all contributions maintain the ethical focus of this project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
