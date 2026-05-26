import json
import sys
from modules.backup import run_backup
from modules.audit import run_audit

def load_inventory(filename="devices.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"[!] Inventory file {filename} missing.")
        sys.exit(1)

def main():
    devices = load_inventory()
    
    print("="*40)
    print("   NETWORK AUTOMATION & AUDIT TOOLKIT   ")
    print("="*40)
    print(f"Loaded {len(devices)} device(s) from inventory.")
    print("1. Run Automated Network Backups")
    print("2. Run Security Compliance Audit Scan")
    print("3. Exit")
    print("="*40)
    
    choice = input("Select an option (1-3): ")
    
    if choice == "1" or choice == "2":
        for device in devices:
            device_copy = device.copy()
            name = device_copy.pop("device_name", device_copy["host"])
            
            # Inject timing flags
            device_copy['global_delay_factor'] = 2
            device_copy['fast_cli'] = False
            
            if choice == "1":
                print(f"\n=== Backing up {name} ({device_copy['host']}) ===")
                run_backup(device_copy)
            elif choice == "2":
                print(f"\n=== Commencing Compliance Audit for {name} ===")
                run_audit(device_copy)
                
    elif choice == "3":
        print("Exiting toolkit.")
        sys.exit(0)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
