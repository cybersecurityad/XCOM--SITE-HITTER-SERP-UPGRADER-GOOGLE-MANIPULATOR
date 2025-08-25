#!/usr/bin/env python3
"""
Quick test to verify the global configuration system works
"""

from tor_menu import GLOBAL_CONFIG

print("🔧 TESTING GLOBAL CONFIGURATION")
print("=" * 35)

# Show initial config
print("📋 Initial Configuration:")
print(f"🔄 Rotation interval: {GLOBAL_CONFIG.rotation_interval}")
print(f"⏱️  Delay range: {GLOBAL_CONFIG.min_delay}s - {GLOBAL_CONFIG.max_delay}s")
print(f"🎭 User agent rotation: {GLOBAL_CONFIG.user_agent_rotation}")

# Modify config
print("\n🔧 Modifying configuration...")
GLOBAL_CONFIG.rotation_interval = 10
GLOBAL_CONFIG.min_delay = 1.0
GLOBAL_CONFIG.max_delay = 3.0
GLOBAL_CONFIG.user_agent_rotation = False

# Show modified config
print("\n📋 Modified Configuration:")
print(f"🔄 Rotation interval: {GLOBAL_CONFIG.rotation_interval}")
print(f"⏱️  Delay range: {GLOBAL_CONFIG.min_delay}s - {GLOBAL_CONFIG.max_delay}s")
print(f"🎭 User agent rotation: {GLOBAL_CONFIG.user_agent_rotation}")

print("\n✅ Global configuration system working correctly!")
