#!/usr/bin/env python3
"""
🛡️ SIMPLIFIED DEFENSIVE WEB SIMULATOR
=====================================
Create defensive traffic simulation to test website protections
while completely hiding your real IP address.

PURPOSE:
- Simulate various attack patterns against websites
- Test website defenses (rate limiting, bot detection, etc.)
- Your real IP remains completely hidden
- Helps improve website security

USAGE:
1. Add proxy servers to protect your IP
2. Choose attack simulation pattern
3. Run test against target website
4. Analyze defense effectiveness
"""

import requests
import random
import time
from datetime import datetime
import threading
from fake_useragent import UserAgent
import json
from typing import List, Dict, Optional

class DefensiveWebSimulator:
    """
    🛡️ Defensive Web Traffic Simulator
    
    Simulates malicious traffic patterns to test website defenses.
    Your real IP is protected through proxy rotation.
    """
    
    def __init__(self, target_url: str, proxy_list: Optional[List[str]] = None):
        self.target_url = target_url.rstrip('/')
        self.proxy_list = proxy_list or []
        self.ua = UserAgent()
        self.results = []
        
        print(f"🎯 Target: {self.target_url}")
        print(f"🔒 IP Protection: {'✅ Active' if self.proxy_list else '❌ WARNING: Your real IP will be exposed!'}")
        print(f"🔄 Available proxies: {len(self.proxy_list)}")
    
    def get_stealth_headers(self) -> Dict[str, str]:
        """Generate realistic headers to avoid detection"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Pragma': 'no-cache'
        }
    
    def get_random_proxy(self) -> Dict[str, str]:
        """Get random proxy configuration"""
        if not self.proxy_list:
            return {}
        
        proxy_url = random.choice(self.proxy_list)
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    
    def make_stealth_request(self, endpoint: str = '') -> Dict:
        """Make a single stealth request"""
        url = f"{self.target_url}{endpoint}"
        headers = self.get_stealth_headers()
        proxies = self.get_random_proxy()
        
        try:
            start_time = time.time()
            
            response = requests.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=10,
                allow_redirects=True,
                verify=True
            )
            
            response_time = time.time() - start_time
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'status_code': response.status_code,
                'response_time': response_time,
                'content_length': len(response.content),
                'proxy_used': proxies.get('http', 'Direct'),
                'user_agent': headers['User-Agent'][:50] + '...',
                'headers_received': dict(response.headers),
                'success': True
            }
            
            # Check for defense indicators
            content_lower = response.text.lower()
            defense_indicators = []
            
            if response.status_code == 429:
                defense_indicators.append('Rate Limited')
            elif response.status_code == 403:
                defense_indicators.append('Access Forbidden')
            elif response.status_code == 503:
                defense_indicators.append('Service Unavailable')
            
            if 'captcha' in content_lower:
                defense_indicators.append('CAPTCHA Required')
            if 'bot' in content_lower and 'detected' in content_lower:
                defense_indicators.append('Bot Detection')
            if 'cloudflare' in content_lower:
                defense_indicators.append('Cloudflare Protection')
            if 'access denied' in content_lower:
                defense_indicators.append('Access Denied')
            
            result['defense_indicators'] = defense_indicators
            
            return result
            
        except requests.exceptions.Timeout:
            return {
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'error': 'Request Timeout',
                'proxy_used': proxies.get('http', 'Direct'),
                'success': False
            }
        except requests.exceptions.ConnectionError as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'error': f'Connection Error: {str(e)[:100]}',
                'proxy_used': proxies.get('http', 'Direct'),
                'success': False
            }
        except Exception as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'error': f'Unknown Error: {str(e)[:100]}',
                'proxy_used': proxies.get('http', 'Direct'),
                'success': False
            }
    
    def simulate_bot_crawler(self, duration_minutes: int = 5):
        """
        🤖 Simulate aggressive bot crawling
        Tests: Rate limiting, bot detection
        """
        print(f"\n🤖 STARTING BOT CRAWLER SIMULATION")
        print(f"⏱️ Duration: {duration_minutes} minutes")
        print(f"🚀 Pattern: Fast automated requests")
        
        end_time = time.time() + (duration_minutes * 60)
        request_count = 0
        
        # Common crawler endpoints
        endpoints = ['/', '/robots.txt', '/sitemap.xml', '/search', '/api', '/admin', '/wp-admin']
        
        while time.time() < end_time:
            endpoint = random.choice(endpoints)
            result = self.make_stealth_request(endpoint)
            self.results.append(result)
            request_count += 1
            
            if request_count % 10 == 0:
                print(f"📊 Requests sent: {request_count}")
                if result.get('defense_indicators'):
                    print(f"🛡️ Defense detected: {', '.join(result['defense_indicators'])}")
            
            # Bot-like timing: very fast requests
            time.sleep(random.uniform(0.1, 0.5))
        
        print(f"✅ Bot crawler simulation complete: {request_count} requests")
    
    def simulate_ddos_attack(self, duration_minutes: int = 3):
        """
        💥 Simulate DDoS attack pattern
        Tests: DDoS protection, traffic filtering
        """
        print(f"\n💥 STARTING DDOS SIMULATION")
        print(f"⏱️ Duration: {duration_minutes} minutes")
        print(f"🚀 Pattern: High-volume concurrent requests")
        
        end_time = time.time() + (duration_minutes * 60)
        threads = []
        
        def ddos_worker():
            while time.time() < end_time:
                result = self.make_stealth_request('/')
                self.results.append(result)
                time.sleep(random.uniform(0.01, 0.1))  # Very fast requests
        
        # Launch multiple concurrent threads
        for i in range(5):  # 5 concurrent attackers
            thread = threading.Thread(target=ddos_worker)
            threads.append(thread)
            thread.start()
            print(f"🔴 Attacker {i+1} launched")
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        print(f"✅ DDoS simulation complete")
    
    def simulate_human_like_browsing(self, duration_minutes: int = 10):
        """
        👤 Simulate normal human browsing (control test)
        Tests: Baseline behavior for comparison
        """
        print(f"\n👤 STARTING HUMAN-LIKE BROWSING")
        print(f"⏱️ Duration: {duration_minutes} minutes")
        print(f"🚀 Pattern: Normal human behavior")
        
        end_time = time.time() + (duration_minutes * 60)
        request_count = 0
        
        while time.time() < end_time:
            result = self.make_stealth_request('/')
            self.results.append(result)
            request_count += 1
            
            if request_count % 5 == 0:
                print(f"📊 Page visits: {request_count}")
            
            # Human-like timing: slower, variable delays
            time.sleep(random.uniform(3, 10))
        
        print(f"✅ Human browsing simulation complete: {request_count} visits")
    
    def simulate_recon_attack(self, duration_minutes: int = 8):
        """
        🔍 Simulate reconnaissance attack
        Tests: Security through obscurity, directory traversal protection
        """
        print(f"\n🔍 STARTING RECONNAISSANCE SIMULATION")
        print(f"⏱️ Duration: {duration_minutes} minutes")
        print(f"🚀 Pattern: Probing for vulnerabilities")
        
        end_time = time.time() + (duration_minutes * 60)
        request_count = 0
        
        # Common recon endpoints
        recon_endpoints = [
            '/.env', '/.git', '/config', '/backup', '/admin', '/phpmyadmin',
            '/wp-config.php', '/database.sql', '/api/v1', '/swagger',
            '/graphql', '/../../../etc/passwd', '/app/config', '/debug'
        ]
        
        while time.time() < end_time:
            endpoint = random.choice(recon_endpoints)
            result = self.make_stealth_request(endpoint)
            self.results.append(result)
            request_count += 1
            
            if request_count % 5 == 0:
                print(f"📊 Probes sent: {request_count}")
                if result.get('status_code') == 200:
                    print(f"⚠️ Potential vulnerability found: {endpoint}")
            
            # Recon timing: methodical but not too fast
            time.sleep(random.uniform(1, 3))
        
        print(f"✅ Reconnaissance simulation complete: {request_count} probes")
    
    def analyze_results(self):
        """Analyze simulation results"""
        if not self.results:
            print("❌ No results to analyze")
            return
        
        print(f"\n📊 SIMULATION ANALYSIS")
        print(f"{'='*50}")
        
        total_requests = len(self.results)
        successful_requests = len([r for r in self.results if r.get('success', False)])
        failed_requests = total_requests - successful_requests
        
        # Status code analysis
        status_codes = {}
        defense_indicators = []
        
        for result in self.results:
            if 'status_code' in result:
                code = result['status_code']
                status_codes[code] = status_codes.get(code, 0) + 1
            
            if 'defense_indicators' in result:
                defense_indicators.extend(result['defense_indicators'])
        
        print(f"📈 Total Requests: {total_requests}")
        print(f"✅ Successful: {successful_requests}")
        print(f"❌ Failed: {failed_requests}")
        
        print(f"\n📊 STATUS CODES:")
        for code, count in sorted(status_codes.items()):
            percentage = (count / total_requests) * 100
            print(f"   {code}: {count} ({percentage:.1f}%)")
        
        if defense_indicators:
            unique_defenses = list(set(defense_indicators))
            print(f"\n🛡️ DEFENSES DETECTED:")
            for defense in unique_defenses:
                count = defense_indicators.count(defense)
                print(f"   {defense}: {count} times")
        
        # Security assessment
        blocked_percentage = ((status_codes.get(403, 0) + status_codes.get(429, 0) + 
                              status_codes.get(503, 0)) / total_requests) * 100
        
        print(f"\n🔒 SECURITY ASSESSMENT:")
        if blocked_percentage > 50:
            print("   ✅ STRONG: Website effectively blocks attack patterns")
        elif blocked_percentage > 20:
            print("   ⚠️ MODERATE: Some protection, but room for improvement")
        elif len(unique_defenses) > 0:
            print("   ⚠️ WEAK: Defense mechanisms present but not effective")
        else:
            print("   ❌ POOR: No significant defense mechanisms detected")
        
        print(f"   Block rate: {blocked_percentage:.1f}%")
        
        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"defensive_test_report_{timestamp}.json"
        
        report = {
            'target_url': self.target_url,
            'test_timestamp': datetime.now().isoformat(),
            'summary': {
                'total_requests': total_requests,
                'successful_requests': successful_requests,
                'failed_requests': failed_requests,
                'status_codes': status_codes,
                'defense_indicators': unique_defenses,
                'block_percentage': blocked_percentage
            },
            'detailed_results': self.results
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n📄 Detailed report saved: {filename}")

def main():
    """Run defensive web simulation"""
    
    print("🛡️ DEFENSIVE WEB SIMULATION FRAMEWORK")
    print("====================================")
    print("Test website defenses while protecting your IP")
    
    # Get target
    target = input("\nEnter target URL (e.g., https://example.com): ").strip()
    if not target:
        target = "https://httpbin.org"
        print(f"Using test target: {target}")
    
    # Proxy configuration (CRITICAL for IP protection)
    PROXY_LIST = [
        # Add your proxies here to hide your real IP
        # "http://username:password@proxy1.com:8080",
        # "http://username:password@proxy2.com:3128",
        # "socks5://username:password@proxy3.com:1080",
    ]
    
    if not PROXY_LIST:
        print("\n⚠️ CRITICAL WARNING: NO PROXIES CONFIGURED!")
        print("Your real IP address will be exposed to the target website!")
        print("This could be traced back to you!")
        print("\nTo protect your IP:")
        print("1. Get proxies from providers like ProxyMesh, Smartproxy, etc.")
        print("2. Add them to PROXY_LIST in the script")
        print("3. Or use a VPN before running this tool")
        
        response = input("\nContinue WITHOUT IP protection? (y/N): ")
        if response.lower() != 'y':
            print("Exiting. Configure proxies first for safe testing.")
            return
    
    # Create simulator
    simulator = DefensiveWebSimulator(target, PROXY_LIST)
    
    # Show simulation options
    print("\n🚨 AVAILABLE ATTACK SIMULATIONS:")
    print("1. 🤖 Bot Crawler (tests rate limiting)")
    print("2. 💥 DDoS Attack (tests traffic protection)")
    print("3. 👤 Human Browsing (baseline test)")
    print("4. 🔍 Reconnaissance (tests security)")
    print("5. 🎯 Full Test Suite (all simulations)")
    
    choice = input("\nSelect simulation (1-5): ").strip()
    
    print(f"\n🚨 STARTING DEFENSIVE SIMULATION")
    print(f"🔒 Your IP protection: {'✅ Active' if PROXY_LIST else '❌ EXPOSED'}")
    print("📊 Monitor output for defense detection...")
    
    try:
        if choice == '1':
            simulator.simulate_bot_crawler()
        elif choice == '2':
            simulator.simulate_ddos_attack()
        elif choice == '3':
            simulator.simulate_human_like_browsing()
        elif choice == '4':
            simulator.simulate_recon_attack()
        elif choice == '5':
            print("🎯 Running full test suite...")
            simulator.simulate_human_like_browsing(3)  # Baseline
            time.sleep(2)
            simulator.simulate_bot_crawler(3)
            time.sleep(2)
            simulator.simulate_recon_attack(3)
            time.sleep(2)
            simulator.simulate_ddos_attack(2)
        else:
            print("❌ Invalid selection")
            return
        
        # Analyze results
        simulator.analyze_results()
        
        print(f"\n✅ SIMULATION COMPLETE")
        print("📊 Check the generated JSON report for detailed analysis")
        print("🛡️ Use results to improve website security")
        
    except KeyboardInterrupt:
        print(f"\n⏹️ Simulation stopped by user")
        simulator.analyze_results()

if __name__ == "__main__":
    main()
