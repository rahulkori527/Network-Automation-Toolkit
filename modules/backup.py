import os
from datetime import datetime
from netmiko import ConnectHandler

def run_backup(device):
    """Connects to a device, pulls the running-config, and saves it to a file."""
    net_connect = None
    try:
        # Create a backups directory if it doesn't exist
        if not os.path.exists("backups"):
            os.makedirs("backups")

        # Connect using the parameters passed from main.py
        net_connect = ConnectHandler(**device)
        print("--> Pulling running configuration...")
        
        config_data = net_connect.send_command("show running-config")
        
        # Generate a clean filename with a timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f"backups/{device['host']}_{timestamp}.cfg"
        
        with open(filename, "w") as backup_file:
            backup_file.write(config_data)
            
        print(f"[+] Backup successfully saved to {filename}")
        return True

    except Exception as e:
        print(f"[!] Backup failed: {e}")
        return False
        
    finally:
        if net_connect:
            net_connect.disconnect()