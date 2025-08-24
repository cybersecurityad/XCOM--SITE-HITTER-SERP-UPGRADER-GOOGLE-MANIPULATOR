# Proxy Configuration Template
# Copy this to proxy_config.py and add your actual proxy servers

# Free proxy lists (unreliable - for testing only)
FREE_PROXIES = [
    # "http://proxy1.example.com:8080",
    # "http://proxy2.example.com:8080",
    # Add free proxies here (not recommended for production)
]

# Premium HTTP/HTTPS proxies
PREMIUM_HTTP_PROXIES = [
    # "http://username:password@premium1.proxy.com:8080",
    # "http://username:password@premium2.proxy.com:8080",
    # Add your premium HTTP proxies here
]

# SOCKS proxies
SOCKS_PROXIES = [
    # "socks5://username:password@socks1.proxy.com:1080",
    # "socks4://username:password@socks2.proxy.com:1080",
    # Add your SOCKS proxies here
]

# Residential proxies (most authentic)
RESIDENTIAL_PROXIES = [
    # "http://user:pass@residential1.proxy.com:8080",
    # "http://user:pass@residential2.proxy.com:8080",
    # Add your residential proxies here
]

# Datacenter proxies with geographic targeting
DATACENTER_PROXIES = {
    "US": [
        # "http://user:pass@us1.datacenter.com:8080",
        # "http://user:pass@us2.datacenter.com:8080",
    ],
    "EU": [
        # "http://user:pass@eu1.datacenter.com:8080",
        # "http://user:pass@eu2.datacenter.com:8080",
    ],
    "ASIA": [
        # "http://user:pass@asia1.datacenter.com:8080",
        # "http://user:pass@asia2.datacenter.com:8080",
    ]
}

# Proxy rotation configuration
ROTATION_CONFIG = {
    "strategy": "random",  # round_robin, random, weighted, country_based
    "interval": 5,         # requests between rotations
    "timeout": 10,         # seconds
    "max_retries": 3,
    "verify_ssl": False,
    "health_check_interval": 300,  # seconds between health checks
}

# User agent configuration
USER_AGENT_CONFIG = {
    "use_realistic_distribution": True,
    "include_mobile": False,
    "custom_agents": [
        # Add custom user agents here
        # "Mozilla/5.0 (Custom) ...",
    ],
    "browser_weights": {
        "chrome": 0.65,
        "firefox": 0.15,
        "safari": 0.12,
        "edge": 0.05,
        "opera": 0.03
    }
}

# Anti-detection features
ANTI_DETECTION_CONFIG = {
    "randomize_viewport": True,
    "randomize_timezone": True,
    "disable_images": False,
    "disable_javascript": False,
    "randomize_language": True,
    "supported_languages": ["en-US", "en-GB", "es-ES", "fr-FR", "de-DE"],
    "canvas_randomization": True,
    "webgl_randomization": True,
}

# Rate limiting and human behavior simulation
BEHAVIOR_CONFIG = {
    "min_request_delay": 2.0,
    "max_request_delay": 8.0,
    "burst_mode": {
        "enabled": True,
        "burst_size": 5,
        "burst_delay": 30.0,
    },
    "human_patterns": {
        "morning_hours": (9, 12),
        "afternoon_hours": (14, 17),
        "reduced_activity_hours": (22, 6),
        "weekend_factor": 0.7,
    }
}
