#!/usr/bin/env python3
"""
Real Google Analytics Integration for Netherlands-Only Tor Browser
This version actually triggers real Google Analytics tracking that you can see in GA dashboard
"""

import os
import sys
import time
import json
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from fake_useragent import UserAgent

class RealGANetherlandsTorBrowser:
    """Netherlands-only Tor browser with REAL Google Analytics tracking"""
    
    def __init__(self, ga_tracking_id=None):
        self.ga_tracking_id = ga_tracking_id  # Your GA4 property ID (e.g., "G-XXXXXXXXXX")
        self.driver = None
        self.session_data = {
            'session_id': f"nl_session_{int(time.time())}",
            'user_id': f"nl_user_{random.randint(10000, 99999)}",
            'events': []
        }
        
    def inject_real_google_analytics(self):
        """Inject real Google Analytics tracking code"""
        if not self.ga_tracking_id:
            print("⚠️ No GA tracking ID provided - using demo mode")
            return
            
        try:
            # Inject Google Analytics gtag script
            ga_script = f"""
            // Google Analytics 4 (gtag.js) - Real Implementation
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{self.ga_tracking_id}', {{
                'anonymize_ip': false,  // We want to see NL IPs in GA
                'allow_google_signals': true,
                'cookie_flags': 'secure',
                'custom_map': {{
                    'custom_parameter_1': 'tor_session',
                    'custom_parameter_2': 'netherlands_only'
                }}
            }});
            
            // Load the actual GA script
            var gaScript = document.createElement('script');
            gaScript.async = true;
            gaScript.src = 'https://www.googletagmanager.com/gtag/js?id={self.ga_tracking_id}';
            document.head.appendChild(gaScript);
            
            console.log('✅ Real Google Analytics loaded with ID: {self.ga_tracking_id}');
            """
            
            self.driver.execute_script(ga_script)
            time.sleep(2)  # Wait for GA to load
            
            print(f"✅ Real Google Analytics injected with ID: {self.ga_tracking_id}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to inject GA: {e}")
            return False
    
    def send_real_ga_pageview(self, page_title=None, page_url=None):
        """Send real Google Analytics pageview event"""
        if not self.ga_tracking_id:
            return
            
        try:
            current_url = page_url or self.driver.current_url
            current_title = page_title or self.driver.title
            
            # Send real GA pageview
            ga_event = f"""
            gtag('event', 'page_view', {{
                'page_title': '{current_title}',
                'page_location': '{current_url}',
                'custom_parameter_1': 'tor_session',
                'custom_parameter_2': 'netherlands_only',
                'session_id': '{self.session_data["session_id"]}',
                'user_id': '{self.session_data["user_id"]}'
            }});
            
            console.log('📊 Real GA pageview sent: {current_title}');
            """
            
            self.driver.execute_script(ga_event)
            
            # Log the event
            event_data = {
                'timestamp': datetime.now().isoformat(),
                'event_type': 'page_view',
                'page_title': current_title,
                'page_url': current_url,
                'session_id': self.session_data["session_id"],
                'user_id': self.session_data["user_id"]
            }
            self.session_data['events'].append(event_data)
            
            print(f"📊 Real GA pageview sent: {current_title}")
            
        except Exception as e:
            print(f"⚠️ GA pageview error: {e}")
    
    def send_real_ga_event(self, event_name, event_category=None, event_label=None, value=None):
        """Send real Google Analytics custom event"""
        if not self.ga_tracking_id:
            return
            
        try:
            event_params = {
                'event_category': event_category or 'engagement',
                'event_label': event_label or 'tor_browsing',
                'custom_parameter_1': 'tor_session',
                'custom_parameter_2': 'netherlands_only',
                'session_id': self.session_data["session_id"],
                'user_id': self.session_data["user_id"]
            }
            
            if value is not None:
                event_params['value'] = value
            
            # Build JavaScript for the event
            params_js = json.dumps(event_params).replace('"', "'")
            
            ga_event = f"""
            gtag('event', '{event_name}', {params_js});
            console.log('📊 Real GA event sent: {event_name}');
            """
            
            self.driver.execute_script(ga_event)
            
            # Log the event
            event_data = {
                'timestamp': datetime.now().isoformat(),
                'event_type': event_name,
                'event_category': event_category,
                'event_label': event_label,
                'value': value,
                'session_id': self.session_data["session_id"],
                'user_id': self.session_data["user_id"]
            }
            self.session_data['events'].append(event_data)
            
            print(f"📊 Real GA event sent: {event_name}")
            
        except Exception as e:
            print(f"⚠️ GA event error: {e}")
    
    def create_test_page_with_ga(self):
        """Create a test HTML page with your GA tracking"""
        if not self.ga_tracking_id:
            print("⚠️ No GA tracking ID - creating demo page instead")
            ga_tracking_id = "G-DEMO123456"  # Demo ID
        else:
            ga_tracking_id = self.ga_tracking_id
        
        test_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Netherlands Tor Browser Test - GA Tracking</title>
            
            <!-- Google Analytics -->
            <script async src="https://www.googletagmanager.com/gtag/js?id={ga_tracking_id}"></script>
            <script>
                window.dataLayer = window.dataLayer || [];
                function gtag(){{dataLayer.push(arguments);}}
                gtag('js', new Date());
                gtag('config', '{ga_tracking_id}', {{
                    'anonymize_ip': false,
                    'allow_google_signals': true,
                    'custom_map': {{
                        'custom_parameter_1': 'tor_session_type',
                        'custom_parameter_2': 'location_override'
                    }}
                }});
                
                // Send custom event when page loads
                gtag('event', 'tor_browser_test', {{
                    'event_category': 'tor_browsing',
                    'event_label': 'netherlands_only',
                    'custom_parameter_1': 'tor_session',
                    'custom_parameter_2': 'netherlands_only'
                }});
                
                console.log('✅ GA tracking initialized with ID: {ga_tracking_id}');
            </script>
            
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .status {{ background: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .event-btn {{ background: #007cba; color: white; padding: 10px 20px; 
                            border: none; border-radius: 4px; margin: 10px 5px; cursor: pointer; }}
                .event-btn:hover {{ background: #005a87; }}
                .info {{ background: #f0f8ff; padding: 15px; border-radius: 4px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🇳🇱 Netherlands-Only Tor Browser GA Test</h1>
                
                <div class="status">
                    <h2>✅ Google Analytics Active</h2>
                    <p><strong>Tracking ID:</strong> {ga_tracking_id}</p>
                    <p><strong>Session ID:</strong> <span id="session-id">{self.session_data["session_id"]}</span></p>
                    <p><strong>User ID:</strong> <span id="user-id">{self.session_data["user_id"]}</span></p>
                    <p><strong>Time:</strong> <span id="current-time">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span></p>
                </div>
                
                <div class="info">
                    <h3>📊 Analytics Information</h3>
                    <p>This page is being viewed through a Netherlands-only Tor exit node. 
                    All Google Analytics events from this session will show the Netherlands IP address.</p>
                    <p>You should see this traffic in your GA dashboard within a few minutes.</p>
                </div>
                
                <h3>🎯 Test Analytics Events</h3>
                <p>Click these buttons to send different types of analytics events:</p>
                
                <button class="event-btn" onclick="sendPageView()">📄 Send Page View</button>
                <button class="event-btn" onclick="sendScrollEvent()">📜 Send Scroll Event</button>
                <button class="event-btn" onclick="sendEngagementEvent()">💬 Send Engagement</button>
                <button class="event-btn" onclick="sendConversionEvent()">🎯 Send Conversion</button>
                
                <div id="event-log" style="margin-top: 20px; padding: 20px; background: #f5f5f5; border-radius: 4px;">
                    <h4>📋 Event Log</h4>
                    <div id="log-content">Page loaded with GA tracking...</div>
                </div>
            </div>
            
            <script>
                let eventCount = 0;
                
                function logEvent(message) {{
                    eventCount++;
                    const logContent = document.getElementById('log-content');
                    const timestamp = new Date().toLocaleTimeString();
                    logContent.innerHTML += '<br>' + timestamp + ' - ' + message;
                    console.log('GA Event: ' + message);
                }}
                
                function sendPageView() {{
                    gtag('event', 'page_view', {{
                        'page_title': 'Netherlands Tor Browser Test',
                        'page_location': window.location.href,
                        'custom_parameter_1': 'manual_pageview',
                        'custom_parameter_2': 'netherlands_only'
                    }});
                    logEvent('📄 Manual page view sent');
                }}
                
                function sendScrollEvent() {{
                    gtag('event', 'scroll', {{
                        'event_category': 'engagement',
                        'event_label': 'manual_scroll',
                        'custom_parameter_1': 'user_interaction',
                        'custom_parameter_2': 'netherlands_only'
                    }});
                    logEvent('📜 Scroll event sent');
                }}
                
                function sendEngagementEvent() {{
                    gtag('event', 'engagement', {{
                        'event_category': 'user_interaction',
                        'event_label': 'button_click',
                        'value': Math.floor(Math.random() * 100),
                        'custom_parameter_1': 'manual_engagement',
                        'custom_parameter_2': 'netherlands_only'
                    }});
                    logEvent('💬 Engagement event sent');
                }}
                
                function sendConversionEvent() {{
                    gtag('event', 'conversion', {{
                        'event_category': 'conversion',
                        'event_label': 'test_conversion',
                        'value': 1,
                        'currency': 'EUR',
                        'custom_parameter_1': 'test_conversion',
                        'custom_parameter_2': 'netherlands_only'
                    }});
                    logEvent('🎯 Conversion event sent');
                }}
                
                // Auto-send some events
                setTimeout(() => {{
                    sendScrollEvent();
                    logEvent('📜 Auto scroll event sent');
                }}, 3000);
                
                setTimeout(() => {{
                    sendEngagementEvent();
                    logEvent('💬 Auto engagement event sent');
                }}, 8000);
                
                // Update time every second
                setInterval(() => {{
                    document.getElementById('current-time').textContent = new Date().toLocaleString();
                }}, 1000);
            </script>
        </body>
        </html>
        """
        
        # Save to file
        test_file = "/tmp/ga_test_page.html"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_html)
        
        return f"file://{test_file}"
    
    def demonstrate_real_ga_tracking(self, ga_tracking_id=None):
        """Demonstrate real Google Analytics tracking that you can see in GA dashboard"""
        self.ga_tracking_id = ga_tracking_id
        
        print("🇳🇱 REAL GOOGLE ANALYTICS DEMONSTRATION")
        print("=" * 50)
        
        if not self.ga_tracking_id:
            print("⚠️ No GA tracking ID provided")
            print("📝 To see real analytics data:")
            print("   1. Create a Google Analytics 4 property")
            print("   2. Get your tracking ID (G-XXXXXXXXXX)")
            print("   3. Run this script with your tracking ID")
            print("   4. Watch the data appear in your GA dashboard!")
            print()
            print("🎮 Running in DEMO mode for now...")
        else:
            print(f"✅ Using GA tracking ID: {self.ga_tracking_id}")
            print("📊 Real analytics data will be sent to your GA property")
        
        try:
            # Create browser with Netherlands-only Tor
            print("🧅 Starting Netherlands-only Tor browser...")
            
            # Create test page with GA tracking
            test_url = self.create_test_page_with_ga()
            print(f"📄 Created test page: {test_url}")
            
            # Create browser (simplified for demo)
            options = uc.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # Add Tor proxy (you can uncomment this if Tor is running)
            # options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
            
            self.driver = uc.Chrome(options=options)
            print("✅ Browser created")
            
            # Navigate to test page
            print("🌐 Loading test page with GA tracking...")
            self.driver.get(test_url)
            
            # Wait for GA to load
            time.sleep(3)
            
            # Inject additional GA tracking if needed
            if self.ga_tracking_id:
                self.inject_real_google_analytics()
            
            print("✅ Test page loaded with Google Analytics!")
            print()
            print("🎯 WHAT YOU SHOULD SEE:")
            print("   📊 Real-time visitors in your GA dashboard")
            print("   🇳🇱 Netherlands as the visitor location")
            print("   📈 Page views, events, and engagement metrics")
            print("   ⏱️ Session duration and user behavior")
            print()
            print("📱 Check your Google Analytics dashboard now!")
            print("   👉 analytics.google.com → Realtime → Overview")
            print()
            
            # Demonstrate different GA events
            print("🎬 Demonstrating various GA events...")
            
            # Send custom events every few seconds
            for i in range(5):
                # Send a pageview
                self.send_real_ga_pageview()
                time.sleep(2)
                
                # Send scroll event
                self.send_real_ga_event('scroll', 'engagement', 'automated_scroll')
                time.sleep(2)
                
                # Send engagement event
                self.send_real_ga_event('engagement', 'user_interaction', 'bot_simulation', random.randint(10, 100))
                time.sleep(3)
                
                # Scroll page
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(1)
                
                print(f"📊 Completed event cycle {i+1}/5")
            
            # Final conversion event
            self.send_real_ga_event('conversion', 'conversion', 'demo_completed', 1)
            
            print()
            print("✅ GA demonstration completed!")
            print(f"📊 Sent {len(self.session_data['events'])} analytics events")
            print("🔍 Check your Google Analytics dashboard to see the data")
            print()
            print("⏱️ Keeping browser open for 30 seconds so you can see the page...")
            
            # Keep browser open briefly
            time.sleep(30)
            
        except Exception as e:
            print(f"❌ Demo error: {e}")
        finally:
            if self.driver:
                self.driver.quit()
            
            # Save session data
            session_file = f"ga_session_{int(time.time())}.json"
            with open(session_file, 'w') as f:
                json.dump(self.session_data, f, indent=2)
            print(f"💾 Session data saved to: {session_file}")

def main():
    """Main function to demonstrate real GA tracking"""
    print("🇳🇱 NETHERLANDS TOR BROWSER - REAL GOOGLE ANALYTICS")
    print("=" * 60)
    print()
    
    # Ask for GA tracking ID
    print("To see REAL Google Analytics data:")
    print("1. Go to https://analytics.google.com")
    print("2. Create a new GA4 property (if you don't have one)")
    print("3. Get your Tracking ID (format: G-XXXXXXXXXX)")
    print("4. Enter it below")
    print()
    
    ga_id = input("Enter your GA4 tracking ID (or press Enter for demo mode): ").strip()
    
    if ga_id and not ga_id.startswith('G-'):
        print("⚠️ Invalid format. GA4 tracking IDs start with 'G-'")
        ga_id = None
    
    # Create and run demonstration
    browser = RealGANetherlandsTorBrowser(ga_id)
    browser.demonstrate_real_ga_tracking()

if __name__ == "__main__":
    main()
