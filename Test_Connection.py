import sys
import traceback
from netmiko import ConnectHandler

# Complete Cisco Sandbox Connection Parameters
cisco_router = {
    'device_type': 'cisco_ios',
    'host': '10.10.20.48',        # Private Sandbox IP Address
    'username': 'developer',      # Sandbox Username
    'password': 'C1sco12345',     # Sandbox Password
    'port': 22,                   # Standard SSH Port
    'global_delay_factor': 2,     # Gives the cloud router extra time to respond
    'fast_cli': False,            # Avoids aggressive optimizations that break slow links
}

def test_connection():
    net_connect = None
    try:
        print("Attempting to establish automated SSH connection via Netmiko...")
        
        # 1. Open the automated SSH tunnel through your active Cisco VPN
        net_connect = ConnectHandler(**cisco_router)
        print("Successfully authenticated and established SSH session!")
        
        # 2. Automatically find and verify the active device prompt
        print("Checking device engine status...")
        prompt = net_connect.find_prompt()
        print(f"Device Prompt Identified: {prompt}")
        
        # 3. Execute the network validation command
        print("Sending command: 'show ip interface brief'...")
        output = net_connect.send_command("show ip interface brief")
        
        print("\n" + "="*20 + " COMMAND OUTPUT " + "="*20)
        print(output)
        print("="*56 + "\n")
            
    except Exception as e:
        print(f"\n[!] Automation Engine Failure: {e}")
        print("\n--- Detailed Error Traceback ---")
        traceback.print_exc()
        print("---------------------------------")
        
    finally:
        # 4. Always safely close the SSH socket channel when finished
        if net_connect:
            net_connect.disconnect()
            print("SSH Session safely disconnected.")

if __name__ == "__main__":
    test_connection()