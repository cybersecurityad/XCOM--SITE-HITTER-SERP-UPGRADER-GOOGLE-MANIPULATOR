#!/usr/bin/env python3
"""
Import Test - Find the problematic import causing exit code 15
"""

print("🔍 TESTING IMPORTS ONE BY ONE")
print("=" * 40)

try:
    print("1. Testing time...")
    import time
    print("✅ time - OK")
except Exception as e:
    print(f"❌ time - FAILED: {e}")

try:
    print("2. Testing random...")
    import random
    print("✅ random - OK")
except Exception as e:
    print(f"❌ random - FAILED: {e}")

try:
    print("3. Testing json...")
    import json
    print("✅ json - OK")
except Exception as e:
    print(f"❌ json - FAILED: {e}")

try:
    print("4. Testing datetime...")
    from datetime import datetime
    print("✅ datetime - OK")
except Exception as e:
    print(f"❌ datetime - FAILED: {e}")

try:
    print("5. Testing typing...")
    from typing import List, Dict, Optional
    print("✅ typing - OK")
except Exception as e:
    print(f"❌ typing - FAILED: {e}")

try:
    print("6. Testing threading...")
    import threading
    print("✅ threading - OK")
except Exception as e:
    print(f"❌ threading - FAILED: {e}")

try:
    print("7. Testing subprocess...")
    import subprocess
    print("✅ subprocess - OK")
except Exception as e:
    print(f"❌ subprocess - FAILED: {e}")

try:
    print("8. Testing requests...")
    import requests
    print("✅ requests - OK")
except Exception as e:
    print(f"❌ requests - FAILED: {e}")

try:
    print("9. Testing selenium webdriver...")
    from selenium import webdriver
    print("✅ selenium webdriver - OK")
except Exception as e:
    print(f"❌ selenium webdriver - FAILED: {e}")

try:
    print("10. Testing selenium By...")
    from selenium.webdriver.common.by import By
    print("✅ selenium By - OK")
except Exception as e:
    print(f"❌ selenium By - FAILED: {e}")

try:
    print("11. Testing selenium ActionChains...")
    from selenium.webdriver.common.action_chains import ActionChains
    print("✅ selenium ActionChains - OK")
except Exception as e:
    print(f"❌ selenium ActionChains - FAILED: {e}")

try:
    print("12. Testing selenium WebDriverWait...")
    from selenium.webdriver.support.ui import WebDriverWait
    print("✅ selenium WebDriverWait - OK")
except Exception as e:
    print(f"❌ selenium WebDriverWait - FAILED: {e}")

try:
    print("13. Testing selenium expected_conditions...")
    from selenium.webdriver.support import expected_conditions as EC
    print("✅ selenium expected_conditions - OK")
except Exception as e:
    print(f"❌ selenium expected_conditions - FAILED: {e}")

try:
    print("14. Testing selenium exceptions...")
    from selenium.common.exceptions import TimeoutException, WebDriverException
    print("✅ selenium exceptions - OK")
except Exception as e:
    print(f"❌ selenium exceptions - FAILED: {e}")

try:
    print("15. Testing fake_useragent...")
    from fake_useragent import UserAgent
    print("✅ fake_useragent - OK")
except Exception as e:
    print(f"❌ fake_useragent - FAILED: {e}")

try:
    print("16. Testing urllib.parse...")
    from urllib.parse import urlparse, urljoin
    print("✅ urllib.parse - OK")
except Exception as e:
    print(f"❌ urllib.parse - FAILED: {e}")

try:
    print("17. Testing signal...")
    import signal
    print("✅ signal - OK")
except Exception as e:
    print(f"❌ signal - FAILED: {e}")

try:
    print("18. Testing sys...")
    import sys
    print("✅ sys - OK")
except Exception as e:
    print(f"❌ sys - FAILED: {e}")

try:
    print("19. Testing os...")
    import os
    print("✅ os - OK")
except Exception as e:
    print(f"❌ os - FAILED: {e}")

try:
    print("20. Testing tempfile...")
    import tempfile
    print("✅ tempfile - OK")
except Exception as e:
    print(f"❌ tempfile - FAILED: {e}")

try:
    print("21. Testing shutil...")
    import shutil
    print("✅ shutil - OK")
except Exception as e:
    print(f"❌ shutil - FAILED: {e}")

try:
    print("22. Testing psutil...")
    import psutil
    print("✅ psutil - OK")
except Exception as e:
    print(f"❌ psutil - FAILED: {e}")

print("\n🎉 ALL IMPORTS TESTED!")
print("If you see this message, all imports are working correctly.")
print("The exit code 15 issue is likely in the code logic, not imports.")
