#!/usr/bin/env python3
"""
🛡️ WEBSITE DEFENSE TESTING FRAMEWORK
====================================
Test your website's defenses against various attack patterns
while keeping your real IP completely hidden.

DEFENSE TESTS:
- Rate limiting bypass attempts
- Bot detection circumvention 
- DDoS simulation resistance
- Geographic blocking validation
- Session hijacking protection
- Form spam protection
- Click fraud detection
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional
import random
import threading
from concurrent.futures import ThreadPoolExecutor

@dataclass
class DefenseTest:
    """Configuration for a specific defense test"""
    name: str
    description: str
    test_type: str
    target_endpoints: List[str]
    request_rate: int  # requests per second
    duration_seconds: int
    expected_defense: str
    success_indicators: List[str]
    proxy_rotation: bool
    user_agent_rotation: bool

class WebsiteDefenseTester:
    """
    🛡️ Comprehensive Website Defense Testing
    
    Tests various security mechanisms while protecting your identity:
    - Your real IP is never exposed to the target
    - All traffic appears to come from different sources
    - Realistic attack patterns simulate real threats
    """
    
    def __init__(self, target_domain: str, proxy_list: Optional[List[str]] = None):
        self.target_domain = target_domain.rstrip('/')
        self.proxy_list = proxy_list or []
        self.test_results = []
        self.session_count = 0
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
        ]
        
        # Predefined defense tests
        self.defense_tests = {
            'rate_limiting': DefenseTest(
                name='Rate Limiting Test',
                description='Test if the website blocks excessive requests from same IP',
                test_type='rate_limit',
                target_endpoints=['/'],
                request_rate=50,  # 50 requests per second
                duration_seconds=60,
                expected_defense='429 Too Many Requests or IP blocking',
                success_indicators=['429', '403', 'blocked', 'rate limit'],
                proxy_rotation=True,
                user_agent_rotation=True
            ),
            'bot_detection': DefenseTest(
                name='Bot Detection Test',
                description='Test if website detects and blocks automated traffic',
                test_type='bot_detection',
                target_endpoints=['/', '/search', '/api'],
                request_rate=10,
                duration_seconds=120,
                expected_defense='Captcha, bot detection, or access denial',
                success_indicators=['captcha', 'bot', 'blocked', 'access denied'],
                proxy_rotation=True,
                user_agent_rotation=True
            ),
            'ddos_simulation': DefenseTest(
                name='DDoS Protection Test',
                description='Test DDoS mitigation capabilities',
                test_type='ddos',
                target_endpoints=['/'],
                request_rate=100,  # 100 requests per second
                duration_seconds=300,  # 5 minutes
                expected_defense='Traffic filtering or service degradation',
                success_indicators=['503', '429', 'cloudflare', 'ddos protection'],
                proxy_rotation=True,
                user_agent_rotation=True
            ),
            'geographic_blocking': DefenseTest(
                name='Geographic Blocking Test',
                description='Test if website blocks specific geographic regions',
                test_type='geo_block',
                target_endpoints=['/'],
                request_rate=5,
                duration_seconds=60,
                expected_defense='Geographic access restrictions',
                success_indicators=['geographic', 'region blocked', '451', 'location'],
                proxy_rotation=True,
                user_agent_rotation=False
            ),
            'form_spam_protection': DefenseTest(
                name='Form Spam Protection Test',
                description='Test protection against automated form submissions',
                test_type='form_spam',
                target_endpoints=['/contact', '/register', '/login'],
                request_rate=20,
                duration_seconds=180,
                expected_defense='Captcha, form validation, or submission blocking',
                success_indicators=['captcha', 'spam', 'blocked', 'validation'],
                proxy_rotation=True,
                user_agent_rotation=True
            )
        }
    
    def get_random_proxy(self) -> Optional[str]:
        """Get a random proxy from the list"""
        return random.choice(self.proxy_list) if self.proxy_list else None
    
    def get_random_user_agent(self) -> str:
        """Get a random user agent"""
        return random.choice(self.user_agents)
    
    async def make_request(self, session: aiohttp.ClientSession, endpoint: str, 
                          proxy: Optional[str] = None, user_agent: Optional[str] = None) -> Dict:
        """Make a single HTTP request with stealth features"""
        headers = {
            'User-Agent': user_agent or self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        url = f"{self.target_domain}{endpoint}"
        
        try:
            # Configure proxy if available
            connector = None
            if proxy:
                connector = aiohttp.TCPConnector()
                # Note: aiohttp proxy syntax differs from requests
                proxy_url = proxy
            
            async with session.get(url, headers=headers, 
                                 proxy=proxy_url if proxy else None,
                                 timeout=aiohttp.ClientTimeout(total=10)) as response:
                
                content = await response.text()
                
                return {
                    'timestamp': datetime.now().isoformat(),
                    'url': url,
                    'status_code': response.status,
                    'headers': dict(response.headers),
                    'content_length': len(content),
                    'proxy_used': proxy,
                    'user_agent': headers['User-Agent'],
                    'response_time': time.time(),
                    'content_sample': content[:200]  # First 200 chars
                }
                
        except Exception as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'error': str(e),
                'proxy_used': proxy,
                'user_agent': headers['User-Agent']
            }
    
    async def run_defense_test(self, test_name: str) -> Dict:
        """Run a specific defense test"""
        if test_name not in self.defense_tests:
            return {'error': f'Unknown test: {test_name}'}
        
        test = self.defense_tests[test_name]
        print(f"\n🚨 STARTING DEFENSE TEST: {test.name}")
        print(f"📋 Description: {test.description}")
        print(f"⏱️ Duration: {test.duration_seconds} seconds")
        print(f"🎯 Request rate: {test.request_rate}/second")
        print(f"🔒 Proxy rotation: {'✅' if test.proxy_rotation else '❌'}")
        print(f"🔄 User agent rotation: {'✅' if test.user_agent_rotation else '❌'}")
        
        results = []
        start_time = time.time()
        request_interval = 1.0 / test.request_rate
        
        # Create aiohttp session
        async with aiohttp.ClientSession() as session:
            while time.time() - start_time < test.duration_seconds:
                tasks = []
                
                # Create batch of requests
                for endpoint in test.target_endpoints:
                    proxy = self.get_random_proxy() if test.proxy_rotation else None
                    user_agent = self.get_random_user_agent() if test.user_agent_rotation else None
                    
                    task = self.make_request(session, endpoint, proxy, user_agent)
                    tasks.append(task)
                
                # Execute requests
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                results.extend([r for r in batch_results if not isinstance(r, Exception)])
                
                # Wait before next batch
                await asyncio.sleep(request_interval)
                
                # Progress update
                elapsed = time.time() - start_time
                if int(elapsed) % 10 == 0:  # Every 10 seconds
                    print(f"⏳ Progress: {elapsed:.0f}/{test.duration_seconds}s - Requests sent: {len(results)}")
        
        # Analyze results
        analysis = self.analyze_test_results(test, results)
        
        print(f"\n✅ TEST COMPLETED: {test.name}")
        print(f"📊 Total requests: {len(results)}")
        print(f"🛡️ Defense effectiveness: {analysis['defense_effectiveness']}")
        
        return {
            'test_config': test.__dict__,
            'raw_results': results,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }
    
    def analyze_test_results(self, test: DefenseTest, results: List[Dict]) -> Dict:
        """Analyze test results to determine defense effectiveness"""
        total_requests = len(results)
        successful_requests = len([r for r in results if r.get('status_code', 0) == 200])
        blocked_requests = len([r for r in results if r.get('status_code', 0) in [403, 429, 503]])
        error_requests = len([r for r in results if 'error' in r])
        
        # Look for defense indicators
        defense_indicators = []
        for result in results:
            content = result.get('content_sample', '').lower()
            for indicator in test.success_indicators:
                if indicator.lower() in content:
                    defense_indicators.append(indicator)
        
        # Calculate defense effectiveness
        block_rate = (blocked_requests + error_requests) / total_requests if total_requests > 0 else 0
        
        if block_rate > 0.7:
            effectiveness = "Strong - Website successfully blocked most attacks"
        elif block_rate > 0.3:
            effectiveness = "Moderate - Some blocking detected"
        elif len(defense_indicators) > 0:
            effectiveness = "Weak - Defense mechanisms detected but not effective"
        else:
            effectiveness = "None - No defense mechanisms detected"
        
        return {
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'blocked_requests': blocked_requests,
            'error_requests': error_requests,
            'block_rate': block_rate,
            'defense_indicators': list(set(defense_indicators)),
            'defense_effectiveness': effectiveness,
            'recommendations': self.generate_recommendations(test, block_rate, defense_indicators)
        }
    
    def generate_recommendations(self, test: DefenseTest, block_rate: float, 
                               indicators: List[str]) -> List[str]:
        """Generate security recommendations based on test results"""
        recommendations = []
        
        if test.test_type == 'rate_limit' and block_rate < 0.5:
            recommendations.append("⚠️ Implement rate limiting (e.g., nginx rate limiting, Cloudflare)")
            recommendations.append("⚠️ Consider IP-based throttling for excessive requests")
        
        if test.test_type == 'bot_detection' and block_rate < 0.3:
            recommendations.append("⚠️ Implement bot detection (e.g., Cloudflare Bot Management)")
            recommendations.append("⚠️ Add CAPTCHA for suspicious traffic patterns")
        
        if test.test_type == 'ddos' and block_rate < 0.8:
            recommendations.append("⚠️ Implement DDoS protection (e.g., Cloudflare, AWS Shield)")
            recommendations.append("⚠️ Configure traffic filtering and rate limiting")
        
        if test.test_type == 'geo_block' and 'geographic' not in indicators:
            recommendations.append("ℹ️ Consider geographic blocking if needed for compliance")
        
        if test.test_type == 'form_spam' and block_rate < 0.4:
            recommendations.append("⚠️ Add CAPTCHA to forms")
            recommendations.append("⚠️ Implement form submission rate limiting")
            recommendations.append("⚠️ Add CSRF protection")
        
        if not recommendations:
            recommendations.append("✅ Website shows good defense against this attack type")
        
        return recommendations
    
    def run_comprehensive_test(self, test_names: Optional[List[str]] = None) -> Dict:
        """Run multiple defense tests"""
        if test_names is None:
            test_names = list(self.defense_tests.keys())
        
        print(f"🛡️ STARTING COMPREHENSIVE DEFENSE TEST")
        print(f"🎯 Target: {self.target_domain}")
        print(f"🔒 IP Protection: {'✅ Active' if self.proxy_list else '❌ No proxies configured'}")
        print(f"📋 Tests to run: {', '.join(test_names)}")
        
        all_results = {}
        
        for test_name in test_names:
            print(f"\n{'='*60}")
            try:
                result = asyncio.run(self.run_defense_test(test_name))
                all_results[test_name] = result
                
                # Brief pause between tests
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ Test {test_name} failed: {e}")
                all_results[test_name] = {'error': str(e)}
        
        # Generate final report
        self.generate_comprehensive_report(all_results)
        
        return all_results
    
    def generate_comprehensive_report(self, results: Dict):
        """Generate a comprehensive security report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"website_defense_report_{timestamp}.json"
        
        report = {
            'target_domain': self.target_domain,
            'test_timestamp': datetime.now().isoformat(),
            'proxy_protection': len(self.proxy_list) > 0,
            'proxy_count': len(self.proxy_list),
            'test_results': results,
            'overall_security_score': self.calculate_security_score(results),
            'critical_recommendations': self.get_critical_recommendations(results)
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n📊 COMPREHENSIVE REPORT GENERATED: {filename}")
        print(f"🔒 Overall Security Score: {report['overall_security_score']}/100")
        
        if report['critical_recommendations']:
            print("\n🚨 CRITICAL RECOMMENDATIONS:")
            for rec in report['critical_recommendations']:
                print(f"   {rec}")
    
    def calculate_security_score(self, results: Dict) -> int:
        """Calculate overall security score (0-100)"""
        if not results:
            return 0
        
        total_score = 0
        test_count = 0
        
        for test_name, result in results.items():
            if 'analysis' in result:
                block_rate = result['analysis'].get('block_rate', 0)
                defense_indicators = result['analysis'].get('defense_indicators', [])
                
                # Score based on block rate and defense indicators
                test_score = (block_rate * 80) + (min(len(defense_indicators), 2) * 10)
                total_score += min(test_score, 100)
                test_count += 1
        
        return int(total_score / test_count) if test_count > 0 else 0
    
    def get_critical_recommendations(self, results: Dict) -> List[str]:
        """Extract critical security recommendations"""
        critical_recs = []
        
        for test_name, result in results.items():
            if 'analysis' in result:
                recommendations = result['analysis'].get('recommendations', [])
                critical_recs.extend([rec for rec in recommendations if '⚠️' in rec])
        
        return list(set(critical_recs))

def main():
    """Example usage for website defense testing"""
    
    print("🛡️ WEBSITE DEFENSE TESTING FRAMEWORK")
    print("====================================")
    
    # Get target domain
    target = input("Enter target domain (e.g., https://example.com): ").strip()
    if not target:
        target = "https://httpbin.org"  # Default test target
        print(f"Using default target: {target}")
    
    # Configure proxies for IP protection
    PROXY_LIST = [
        # Add your proxies here for IP protection
        # "http://user:pass@proxy1.com:8080",
        # "http://user:pass@proxy2.com:8080",
    ]
    
    if not PROXY_LIST:
        print("\n⚠️ WARNING: No proxies configured!")
        print("Your real IP will be exposed to the target website.")
        print("Add proxies to PROXY_LIST for IP protection.")
        
        response = input("Continue without IP protection? (y/N): ")
        if response.lower() != 'y':
            print("Exiting. Configure proxies for anonymous testing.")
            return
    
    # Create tester
    tester = WebsiteDefenseTester(target, PROXY_LIST)
    
    # Show available tests
    print("\n🧪 AVAILABLE DEFENSE TESTS:")
    for i, (test_key, test) in enumerate(tester.defense_tests.items(), 1):
        print(f"{i}. {test.name} - {test.description}")
    
    print(f"{len(tester.defense_tests) + 1}. Run all tests")
    
    # Get user selection
    choice = input(f"\nSelect test (1-{len(tester.defense_tests) + 1}): ").strip()
    
    try:
        choice_num = int(choice)
        test_keys = list(tester.defense_tests.keys())
        
        if choice_num == len(tester.defense_tests) + 1:
            # Run all tests
            print("\n🚨 Running comprehensive defense test...")
            tester.run_comprehensive_test()
        elif 1 <= choice_num <= len(tester.defense_tests):
            # Run specific test
            test_name = test_keys[choice_num - 1]
            print(f"\n🚨 Running {test_name} test...")
            result = asyncio.run(tester.run_defense_test(test_name))
        else:
            print("❌ Invalid selection")
            
    except ValueError:
        print("❌ Invalid input")

if __name__ == "__main__":
    main()
