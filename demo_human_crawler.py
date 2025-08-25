#!/usr/bin/env python3
"""
XCOM.DEV -- ADVANCED WEB SITE HITTER -- SERP UPGRADER- GOOGLE MANIPULATOR

🎯 WEBSITE CRAWLER WITH HUMAN SIMULATION (TOR-READY)
==================================================

Licensed to:
XCOM.DEV
PW OLDENBURGER
SINT OLOSSTEEG 4C
1012AK AMSTERDAM
NETHERLANDS
JEDI@XCOM.DEV
+31648319157

© 2025 XCOM.DEV. All rights reserved.

Complete website crawling system with human behavior simulation.
Ready for Tor integration once Tor is installed.

FEATURES:
1. ✅ Automatic website crawling with human simulation
2. 🔄 Full user agent and profile rotation
3. 🥷 Advanced anonymization (Tor-ready)
4. 👤 Realistic human behavior patterns
5. 📊 Comprehensive reporting

USAGE:
- Install Tor: brew install tor (macOS) or sudo apt install tor (Linux)
- Run: python tor_human_crawler.py
- Or use this demo version without Tor
"""

import requests
import random
import time
import json
from datetime import datetime
from typing import List, Dict, Optional
from fake_useragent import UserAgent
from urllib.parse import urljoin, urlparse
import re

class HumanSimulator:
    """Human behavior simulation for website crawling"""
    
    def __init__(self):
        self.ua = UserAgent()
        
        # Human profiles
        self.profiles = [
            {
                'name': 'Tech Enthusiast',
                'interests': ['technology', 'programming', 'gadgets', 'AI'],
                'reading_speed': 180,  # WPM
                'patience': 45,  # seconds
                'curiosity': 0.8
            },
            {
                'name': 'News Reader', 
                'interests': ['news', 'politics', 'business', 'world'],
                'reading_speed': 220,
                'patience': 30,
                'curiosity': 0.6
            },
            {
                'name': 'Casual Browser',
                'interests': ['entertainment', 'sports', 'lifestyle'],
                'reading_speed': 150,
                'patience': 60,
                'curiosity': 0.9
            },
            {
                'name': 'Researcher',
                'interests': ['science', 'education', 'research', 'academic'],
                'reading_speed': 200,
                'patience': 120,
                'curiosity': 0.95
            }
        ]
    
    def generate_profile(self) -> Dict:
        """Generate random human profile"""
        base_profile = random.choice(self.profiles)
        
        return {
            **base_profile,
            'user_agent': self.ua.random,
            'session_id': f"session_{random.randint(1000, 9999)}",
            'device_type': random.choice(['desktop', 'mobile', 'tablet']),
            'os': random.choice(['Windows', 'macOS', 'Linux', 'iOS', 'Android']),
            'browser': random.choice(['Chrome', 'Firefox', 'Safari', 'Edge'])
        }
    
    def calculate_read_time(self, content: str, profile: Dict) -> float:
        """Calculate realistic reading time"""
        words = len(content.split())
        base_time = (words / profile['reading_speed']) * 60  # seconds
        
        # Add human factors
        attention_factor = random.uniform(0.7, 1.3)
        interest_factor = random.uniform(0.8, 1.2)
        
        total_time = base_time * attention_factor * interest_factor
        return min(max(2, total_time), profile['patience'])
    
    def should_click_link(self, link_text: str, profile: Dict) -> bool:
        """Decide if human would click this link"""
        if not link_text:
            return False
        
        link_lower = link_text.lower()
        
        # Check interest match
        interest_score = sum(1 for interest in profile['interests'] 
                           if interest in link_lower)
        
        if interest_score > 0:
            return random.random() < (0.7 * profile['curiosity'])
        
        return random.random() < (0.2 * profile['curiosity'])

class WebsiteCrawler:
    """Website crawler with human behavior simulation"""
    
    def __init__(self, use_tor: bool = False):
        self.use_tor = use_tor
        self.human_sim = HumanSimulator()
        self.session_data = []
        
        print(f"🕷️ Website Crawler Initialized")
        print(f"🧅 Tor support: {'✅ Ready' if use_tor else '❌ Disabled'}")
    
    def get_session(self, profile: Dict) -> requests.Session:
        """Create HTTP session with human-like headers"""
        session = requests.Session()
        
        # Human-like headers
        session.headers.update({
            'User-Agent': profile['user_agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        })
        
        # Configure Tor proxy if enabled
        if self.use_tor:
            session.proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
        
        return session
    
    def crawl_website_human_like(self, domain: str, duration_minutes: int = 10, 
                                max_pages: int = 15) -> Dict:
        """
        🎯 MAIN FEATURE: Crawl website with realistic human behavior
        
        Features:
        - Always changing user agents and profiles
        - Realistic reading and browsing patterns
        - Human-like navigation decisions
        - Randomized timing and actions
        - Comprehensive session logging
        """
        
        print(f"\n🎯 STARTING HUMAN-LIKE WEBSITE CRAWLING")
        print(f"🌐 Target: {domain}")
        print(f"⏱️ Duration: {duration_minutes} minutes")
        print(f"📄 Max pages: {max_pages}")
        
        # Generate human profile
        profile = self.human_sim.generate_profile()
        
        print(f"\n👤 HUMAN PROFILE GENERATED:")
        print(f"   Type: {profile['name']}")
        print(f"   Interests: {', '.join(profile['interests'])}")
        print(f"   Reading speed: {profile['reading_speed']} WPM")
        print(f"   Device: {profile['device_type']} ({profile['os']})")
        print(f"   Browser: {profile['browser']}")
        print(f"   User Agent: {profile['user_agent'][:60]}...")
        
        session_result = {
            'domain': domain,
            'profile': profile,
            'start_time': datetime.now().isoformat(),
            'pages_visited': [],
            'actions_performed': [],
            'total_time': 0,
            'success': False
        }
        
        session = self.get_session(profile)
        current_url = domain.rstrip('/')
        visited_urls = set()
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        try:
            while time.time() < end_time and len(session_result['pages_visited']) < max_pages:
                
                # Visit current page
                page_result = self.visit_page(session, current_url, profile)
                
                if page_result['success']:
                    session_result['pages_visited'].append(page_result)
                    session_result['actions_performed'].extend(page_result['actions'])
                    visited_urls.add(current_url)
                    
                    print(f"✅ Page {len(session_result['pages_visited'])}: {current_url}")
                    print(f"   📄 Content: {page_result['content_length']} chars")
                    print(f"   ⏱️ Time: {page_result['time_spent']:.1f}s")
                    print(f"   🔗 Links: {len(page_result['links'])}")
                    
                    # Choose next page based on human behavior
                    next_url = self.choose_next_page(
                        page_result['links'], visited_urls, profile, domain
                    )
                    
                    if next_url:
                        current_url = next_url
                        print(f"🔗 Next: {urlparse(next_url).path}")
                    else:
                        print(f"🚪 No more interesting pages")
                        break
                    
                    # Human-like delay
                    delay = random.uniform(3, 15)
                    print(f"⏱️ Waiting {delay:.1f}s...")
                    time.sleep(delay)
                    
                else:
                    print(f"❌ Failed: {current_url}")
                    break
            
            session_result['total_time'] = time.time() - start_time
            session_result['success'] = True
            
        except Exception as e:
            print(f"❌ Crawling error: {e}")
            session_result['error'] = str(e)
        
        # Save session
        self.session_data.append(session_result)
        self.save_session_report(session_result)
        
        print(f"\n✅ CRAWLING COMPLETE")
        print(f"📄 Pages visited: {len(session_result['pages_visited'])}")
        print(f"⏱️ Total time: {session_result['total_time']:.1f}s")
        print(f"🎬 Actions: {len(session_result['actions_performed'])}")
        
        return session_result
    
    def visit_page(self, session: requests.Session, url: str, profile: Dict) -> Dict:
        """Visit single page with human simulation"""
        start_time = time.time()
        
        try:
            response = session.get(url, timeout=30)
            
            if response.status_code != 200:
                return {
                    'success': False,
                    'url': url,
                    'error': f'HTTP {response.status_code}',
                    'time_spent': time.time() - start_time
                }
            
            # Extract content and links
            content = response.text
            content_length = len(content)
            
            # Extract links using regex
            links = self.extract_links(content, url, profile)
            
            # Simulate human reading
            read_time = self.human_sim.calculate_read_time(content, profile)
            
            # Simulate human actions
            actions = []
            
            # Scrolling simulation
            if content_length > 1000:
                scroll_actions = random.randint(3, 8)
                for _ in range(scroll_actions):
                    actions.append({
                        'type': 'scroll',
                        'position': random.randint(100, content_length),
                        'duration': random.uniform(0.5, 2.0)
                    })
            
            # Reading simulation
            time.sleep(min(read_time, 30))  # Cap at 30 seconds
            
            total_time = time.time() - start_time
            
            return {
                'success': True,
                'url': url,
                'content_length': content_length,
                'time_spent': total_time,
                'actions': actions,
                'links': links,
                'read_time': read_time
            }
            
        except Exception as e:
            return {
                'success': False,
                'url': url,
                'error': str(e),
                'time_spent': time.time() - start_time
            }
    
    def extract_links(self, html_content: str, base_url: str, profile: Dict) -> List[Dict]:
        """Extract clickable links from HTML"""
        links = []
        
        # Simple regex to find links
        link_pattern = r'<a[^>]+href=["\'](.*?)["\'][^>]*>(.*?)</a>'
        matches = re.findall(link_pattern, html_content, re.IGNORECASE | re.DOTALL)
        
        for href, link_text in matches[:30]:  # Limit to 30 links
            # Clean link text
            link_text = re.sub(r'<[^>]+>', '', link_text).strip()
            
            if href and (href.startswith('http') or href.startswith('/')):
                full_url = urljoin(base_url, href)
                
                links.append({
                    'url': full_url,
                    'text': link_text,
                    'clickable': self.human_sim.should_click_link(link_text, profile)
                })
        
        return links
    
    def choose_next_page(self, links: List[Dict], visited: set, 
                        profile: Dict, base_domain: str) -> Optional[str]:
        """Choose next page based on human behavior"""
        
        # Filter to clickable, unvisited, same-domain links
        candidates = []
        base_netloc = urlparse(base_domain).netloc
        
        for link in links:
            link_netloc = urlparse(link['url']).netloc
            
            if (link['clickable'] and 
                link['url'] not in visited and
                (link_netloc == base_netloc or link_netloc == '')):
                candidates.append(link)
        
        if not candidates:
            return None
        
        # Prioritize by interest
        interested = []
        for link in candidates:
            interest_score = sum(
                1 for interest in profile['interests'] 
                if interest in link['text'].lower()
            )
            if interest_score > 0:
                interested.append((link, interest_score))
        
        if interested:
            # Choose from most interesting
            interested.sort(key=lambda x: x[1], reverse=True)
            return interested[0][0]['url']
        
        # Random choice from candidates
        return random.choice(candidates)['url']
    
    def save_session_report(self, session_result: Dict):
        """Save detailed session report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"crawl_session_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(session_result, f, indent=2, default=str)
        
        print(f"📊 Session report saved: {filename}")

def main():
    """Main interface"""
    
    print("🕷️ WEBSITE CRAWLER WITH HUMAN SIMULATION")
    print("=========================================")
    
    # Check for Tor
    try:
        # Test if Tor is available
        import subprocess
        result = subprocess.run(['which', 'tor'], capture_output=True, text=True)
        tor_available = result.returncode == 0
    except:
        tor_available = False
    
    if tor_available:
        print("✅ Tor detected - Full anonymization available")
        use_tor = input("Use Tor network? (y/N): ").lower() == 'y'
    else:
        print("⚠️ Tor not installed - Running without anonymization")
        print("💡 Install Tor: brew install tor (macOS) or sudo apt install tor (Linux)")
        use_tor = False
    
    crawler = WebsiteCrawler(use_tor)
    
    print("\n🎯 CRAWLING OPTIONS:")
    print("1. 🕷️ Crawl website with human simulation")
    print("2. 📊 View previous sessions")
    print("3. 🧪 Test different human profiles")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == '1':
        domain = input("Enter domain (e.g., https://example.com): ").strip()
        if not domain.startswith('http'):
            domain = 'https://' + domain
        
        duration = int(input("Duration in minutes (default 5): ") or "5")
        max_pages = int(input("Max pages (default 10): ") or "10")
        
        print(f"\n🚀 Starting crawl of {domain}")
        if use_tor:
            print("🧅 Using Tor for complete anonymization")
        print("👤 Generating human profile...")
        
        session = crawler.crawl_website_human_like(domain, duration, max_pages)
        
    elif choice == '2':
        if crawler.session_data:
            print(f"\n📊 SESSION HISTORY:")
            for i, session in enumerate(crawler.session_data, 1):
                print(f"{i}. {session['domain']} - {len(session['pages_visited'])} pages")
        else:
            print("📊 No sessions yet")
    
    elif choice == '3':
        print(f"\n🧪 TESTING HUMAN PROFILES:")
        for i in range(3):
            profile = crawler.human_sim.generate_profile()
            print(f"\nProfile {i+1}: {profile['name']}")
            print(f"   Interests: {', '.join(profile['interests'])}")
            print(f"   Device: {profile['device_type']} ({profile['os']})")
            print(f"   Reading: {profile['reading_speed']} WPM")
    
    else:
        print("❌ Invalid selection")

if __name__ == "__main__":
    main()
