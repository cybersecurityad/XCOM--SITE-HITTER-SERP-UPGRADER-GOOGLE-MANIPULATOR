#!/usr/bin/env python3
"""
🧅 TOR MANAGER MODULE
====================
Separate Tor integration module to isolate proxy issues from browser creation.
This allows independent testing and debugging of Tor vs browser components.
"""

# AUTO-INITIALIZE LOGGING ON IMPORT
from auto_logger_init import auto_initialize
auto_initialize()

import os
import time
import subprocess
import tempfile
import shutil
import socket
from typing import Optional, Tuple

class TorManager:
    """Independent Tor management - separate from browser"""
    
    def __init__(self, tor_port: int = 9050, control_port: int = 9051):
        self.tor_port = tor_port
        self.control_port = control_port
        self.tor_process = None
        self.temp_dir = None
        self.is_running = False
        
    def create_tor_config(self) -> Optional[str]:
        """Create Tor configuration for Netherlands-only exit nodes"""
        try:
            # Create temporary directory for Tor data
            self.temp_dir = tempfile.mkdtemp(prefix="tor_")
            
            tor_config = f"""
# Tor Configuration for Netherlands-only exit nodes
DataDirectory {self.temp_dir}
SocksPort {self.tor_port}
ControlPort {self.control_port}

# Netherlands-only exit nodes
ExitNodes {{nl}}
StrictNodes 1

# Additional security
CookieAuthentication 1
HashedControlPassword 16:E600ADC1B52C80BB6022A0E999A7734934A90B6E5A842C2B7ABCF2211D

# Logging
Log notice stdout
Log info file {self.temp_dir}/tor.log

# Circuit preferences
NewCircuitPeriod 30
MaxCircuitDirtiness 600
CircuitBuildTimeout 20
"""
            
            config_path = os.path.join(self.temp_dir, "torrc")
            with open(config_path, 'w') as f:
                f.write(tor_config)
            
            print(f"📝 Tor config created: {config_path}")
            return config_path
            
        except Exception as e:
            print(f"❌ Failed to create Tor config: {e}")
            return None
    
    def start_tor(self) -> bool:
        """Start Tor process with Netherlands-only configuration"""
        try:
            print("🧅 Starting Tor with Netherlands-only exit nodes...")
            
            # Kill any existing Tor processes
            subprocess.run(['pkill', '-f', 'tor'], capture_output=True, check=False)
            time.sleep(2)
            
            # Create config
            config_path = self.create_tor_config()
            if not config_path:
                return False
            
            # Start Tor process
            tor_cmd = [
                'tor',
                '-f', config_path,
                '--quiet'
            ]
            
            print(f"🚀 Starting Tor: {' '.join(tor_cmd)}")
            self.tor_process = subprocess.Popen(
                tor_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for Tor to start
            print("⏳ Waiting for Tor to initialize...")
            if not self.wait_for_tor_startup():
                print("❌ Tor startup failed")
                return False
            
            self.is_running = True
            print("✅ Tor started successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Tor: {e}")
            return False
    
    def wait_for_tor_startup(self, timeout: int = 30) -> bool:
        """Wait for Tor to be ready with circuit establishment"""
        try:
            print("🔄 Waiting for Tor circuits to establish...")
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Check if Tor process is still running
                if self.tor_process and self.tor_process.poll() is not None:
                    print("❌ Tor process died during startup")
                    return False
                
                # Test SOCKS proxy connection
                if self.test_tor_proxy():
                    print("✅ Tor circuits established successfully!")
                    return True
                
                print("⏳ Still waiting for circuits...")
                time.sleep(2)
            
            print("❌ Timeout waiting for Tor circuits")
            return False
            
        except Exception as e:
            print(f"❌ Error waiting for Tor: {e}")
            return False
    
    def test_tor_proxy(self) -> bool:
        """Test if Tor SOCKS proxy is responding"""
        try:
            # Test SOCKS proxy connection
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(('127.0.0.1', self.tor_port))
            sock.close()
            
            return result == 0
            
        except Exception:
            return False
    
    def get_proxy_settings(self) -> Optional[str]:
        """Get proxy settings for browser if Tor is running"""
        if self.is_running and self.test_tor_proxy():
            return f"socks5://127.0.0.1:{self.tor_port}"
        return None
    
    def rotate_identity(self) -> bool:
        """Rotate Tor identity (new IP)"""
        try:
            if not self.is_running:
                print("❌ Tor not running, cannot rotate identity")
                return False
            
            print("🔄 Rotating Tor identity (new IP)...")
            
            # Send NEWNYM signal to Tor control port
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('127.0.0.1', self.control_port))
            sock.send(b'AUTHENTICATE\r\n')
            sock.recv(1024)
            sock.send(b'SIGNAL NEWNYM\r\n')
            response = sock.recv(1024)
            sock.close()
            
            if b'250 OK' in response:
                print("✅ Tor identity rotated successfully!")
                time.sleep(5)  # Wait for new circuit
                return True
            else:
                print(f"❌ Identity rotation failed: {response}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to rotate Tor identity: {e}")
            return False
    
    def get_current_ip(self) -> Optional[str]:
        """Get current external IP through Tor"""
        try:
            if not self.is_running:
                return None
            
            import urllib.request
            import urllib.error
            
            # Use Tor proxy to get IP
            proxy_handler = urllib.request.ProxyHandler({
                'http': f'socks5://127.0.0.1:{self.tor_port}',
                'https': f'socks5://127.0.0.1:{self.tor_port}'
            })
            opener = urllib.request.build_opener(proxy_handler)
            
            response = opener.open('https://httpbin.org/ip', timeout=10)
            import json
            data = json.loads(response.read().decode())
            return data.get('origin')
            
        except Exception as e:
            print(f"❌ Failed to get IP: {e}")
            return None
    
    def stop_tor(self):
        """Stop Tor process and cleanup"""
        try:
            print("🛑 Stopping Tor...")
            
            if self.tor_process:
                self.tor_process.terminate()
                time.sleep(2)
                if self.tor_process.poll() is None:
                    self.tor_process.kill()
                print("✅ Tor process stopped")
            
            # Cleanup temp directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                print(f"🗑️ Cleaned up: {self.temp_dir}")
            
            self.is_running = False
            
        except Exception as e:
            print(f"⚠️ Tor cleanup error: {e}")
    
    def get_status(self) -> dict:
        """Get Tor status information"""
        return {
            'running': self.is_running,
            'tor_port': self.tor_port,
            'control_port': self.control_port,
            'proxy_ready': self.test_tor_proxy() if self.is_running else False,
            'proxy_url': self.get_proxy_settings(),
            'temp_dir': self.temp_dir
        }

def test_tor_module():
    """Test the Tor module independently"""
    print("=" * 60)
    print("🧪 TOR MODULE TEST")
    print("=" * 60)
    
    tor_manager = TorManager()
    
    try:
        # Test Tor startup
        print("\n1️⃣ Testing Tor startup...")
        if tor_manager.start_tor():
            print("✅ Tor startup: PASSED")
            
            # Test proxy
            print("\n2️⃣ Testing proxy connection...")
            proxy = tor_manager.get_proxy_settings()
            if proxy:
                print(f"✅ Proxy ready: {proxy}")
            else:
                print("❌ Proxy not ready")
            
            # Test IP
            print("\n3️⃣ Testing IP retrieval...")
            ip = tor_manager.get_current_ip()
            if ip:
                print(f"✅ Current IP: {ip}")
            else:
                print("❌ IP retrieval failed")
            
            # Test rotation
            print("\n4️⃣ Testing identity rotation...")
            if tor_manager.rotate_identity():
                new_ip = tor_manager.get_current_ip()
                print(f"✅ New IP after rotation: {new_ip}")
            
            # Status
            print("\n📊 Tor Status:")
            status = tor_manager.get_status()
            for key, value in status.items():
                print(f"   {key}: {value}")
            
        else:
            print("❌ Tor startup: FAILED")
        
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
    finally:
        tor_manager.stop_tor()

if __name__ == "__main__":
    test_tor_module()
