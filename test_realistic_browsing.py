#!/usr/bin/env python3
"""
Test the realistic browsing with slower scrolling and longer sessions
"""

import os
import sys

# Test the updated visual Tor browser
if __name__ == "__main__":
    print("🧪 Testing Realistic Browsing Configuration")
    print("==========================================")
    
    # Activate environment and run the visual Tor browser
    os.system("""
        cd /Users/_akira/CSAD/websites-new-2025/seo-crawler && 
        source .venv/bin/activate && 
        echo "4
https://verenigdamsterdam.nl
" | python3 visual_tor_browser.py
    """)
