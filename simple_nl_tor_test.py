#!/usr/bin/env python3
"""
🇳🇱 SIMPLE NETHERLANDS TOR TEST
==============================
Quick test to verify Netherlands-only Tor exit nodes
"""

import os
import time
import subprocess
import requests
import signal
import sys

class SimpleNLTorTest:
    def __init__(self):
        self.tor_process = None
        self.socks_port = 9050
        
    def start_tor_nl_only(self):
        """Start Tor with Netherlands-only configuration"""
        try:
            # Stop any existing Tor
            self.stop_tor()
            
            print(f"🧅 Starting Tor with Netherlands-only exit nodes...")
            
            # Create torrc for Netherlands only
            torrc_content = f"""
SocksPort {self.socks_port}
ExitNodes {{nl}}
StrictNodes 1
DataDirectory /tmp/tor_nl_test
Log notice stdout
"""
            
            # Write torrc
            torrc_path = "/tmp/torrc_nl_test"
            with open(torrc_path, 'w') as f:
                f.write(torrc_content)
            
            # Start Tor
            cmd = ['/opt/homebrew/bin/tor', '-f', torrc_path]
            self.tor_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for Tor to be ready
            print(f"⏳ Waiting for Tor to start...")
            for i in range(20):
                time.sleep(1)
                if self.is_tor_ready():
                    print(f"✅ Tor ready after {i+1} seconds!")
                    return True
                print(f"   🔄 {i+1}/20...")
            
            print(f"❌ Tor failed to start")
            return False
            
        except Exception as e:
            print(f"❌ Error starting Tor: {e}")
            return False
    
    def is_tor_ready(self):
        """Check if Tor SOCKS proxy is ready"""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', self.socks_port))
            sock.close()
            return result == 0
        except:
            return False
    
    def get_tor_ip(self):
        """Get current Tor IP"""
        try:
            proxies = {
                'http': f'socks5://127.0.0.1:{self.socks_port}',
                'https': f'socks5://127.0.0.1:{self.socks_port}'
            }
            
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxies,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('origin', 'Unknown')
            return None
            
        except Exception as e:
            print(f"⚠️ IP fetch error: {e}")
            return None
    
    def check_ip_location(self, ip):
        """Check if IP is from Netherlands"""
        try:
            print(f"📍 Checking location for IP: {ip}")
            
            # Try multiple geolocation services
            services = [
                f"http://ip-api.com/json/{ip}",
                f"https://ipapi.co/{ip}/json/"
            ]
            
            for service in services:
                try:
                    response = requests.get(service, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Parse response
                        if 'country' in data:
                            country = data.get('country', 'Unknown')
                            country_code = data.get('countryCode', data.get('country_code', 'XX'))
                            city = data.get('city', 'Unknown')
                        else:
                            continue
                        
                        print(f"🏳️ Country: {country} ({country_code})")
                        print(f"🏙️ City: {city}")
                        
                        # Check if Netherlands
                        if country_code.upper() in ['NL', 'NLD']:
                            print(f"✅ SUCCESS: Netherlands IP confirmed!")
                            return True
                        else:
                            print(f"❌ FAILURE: Not Netherlands ({country_code})")
                            return False
                            
                except Exception as e:
                    print(f"⚠️ Service error: {e}")
                    continue
            
            print(f"⚠️ Could not verify location")
            return False
            
        except Exception as e:
            print(f"❌ Location check error: {e}")
            return False
    
    def test_multiple_circuits(self, count=3):
        """Test multiple Tor circuits"""
        print(f"🔄 Testing {count} different Tor circuits...")
        
        nl_count = 0
        total_count = 0
        
        for i in range(count):
            print(f"\n🔄 Test {i+1}/{count}")
            print(f"-" * 25)
            
            if i > 0:
                # Get new circuit
                print(f"🔄 Getting new circuit...")
                self.new_circuit()
                time.sleep(5)
            
            # Get IP
            ip = self.get_tor_ip()
            if not ip:
                print(f"❌ Could not get IP")
                continue
            
            print(f"🌐 Current IP: {ip}")
            total_count += 1
            
            # Check location
            if self.check_ip_location(ip):
                nl_count += 1
            
            # Wait between tests
            if i < count - 1:
                print(f"⏱️ Waiting 3 seconds...")
                time.sleep(3)
        
        # Results
        print(f"\n📊 RESULTS")
        print(f"=" * 30)
        print(f"✅ Netherlands IPs: {nl_count}/{total_count}")
        print(f"📈 Success rate: {(nl_count/total_count)*100:.1f}%" if total_count > 0 else "No data")
        
        return nl_count > 0
    
    def new_circuit(self):
        """Force new Tor circuit"""
        try:
            # Send NEWNYM signal to Tor
            if self.tor_process:
                os.system("echo 'NEWNYM' | nc 127.0.0.1 9051 2>/dev/null")
        except:
            pass
    
    def stop_tor(self):
        """Stop Tor process"""
        try:
            if self.tor_process:
                print(f"🛑 Stopping Tor...")
                self.tor_process.terminate()
                self.tor_process.wait(timeout=5)
                self.tor_process = None
        except:
            try:
                if self.tor_process:
                    self.tor_process.kill()
                    self.tor_process = None
            except:
                pass
        
        # Clean up any remaining tor processes
        os.system("pkill -f 'tor -f'")
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_tor()
        
        # Clean temp files
        try:
            os.remove("/tmp/torrc_nl_test")
        except:
            pass
        
        try:
            import shutil
            shutil.rmtree("/tmp/tor_nl_test")
        except:
            pass

def main():
    print(f"🇳🇱 SIMPLE NETHERLANDS TOR TEST")
    print(f"=" * 35)
    
    test = SimpleNLTorTest()
    
    def signal_handler(signum, frame):
        print(f"\n🛑 Interrupted, cleaning up...")
        test.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Start Tor
        if not test.start_tor_nl_only():
            print(f"❌ Failed to start Tor")
            return False
        
        # Test multiple circuits
        success = test.test_multiple_circuits(3)
        
        if success:
            print(f"\n🎉 Netherlands-only configuration working!")
        else:
            print(f"\n❌ No Netherlands IPs found")
        
        return success
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False
    finally:
        test.cleanup()

if __name__ == "__main__":
    main()
