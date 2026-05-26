from netmiko import ConnectHandler

def run_audit(device):
    """Connects to a device, analyzes interface status, and flags compliance violations."""
    net_connect = None
    try:
        net_connect = ConnectHandler(**device)
        print("--> Scanning device interfaces for compliance rules...")
        
        # Pull the interface configuration status brief
        output = net_connect.send_command("show ip interface brief")
        lines = output.strip().split('\n')
        
        print("\n" + "-"*25 + " COMPLIANCE REPORT " + "-"*25)
        print(f"{'Interface':<20} {'Status':<10} {'Compliance Assessment'}")
        print("-"*69)
        
        non_compliant_count = 0
        
        # Skip the header line and parse the interface rows
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 2:
                interface = parts[0]
                status = parts[1] if "Ethernet" not in parts[1] else parts[4] # Simple parser logic
                
                # Check actual configuration context for a description
                desc_check = net_connect.send_command(f"show run interface {interface} | include description")
                
                # Compliance Rule 1: Active interfaces must have a description
                if "up" in line.lower() and not desc_check:
                    print(f"{interface:<20} {'[UP]':<10} ❌ VIOLATION: Missing description string!")
                    non_compliant_count += 1
                # Compliance Rule 2: Inactive interfaces should be shut down securely
                elif "down" in line.lower() and "administratively down" not in line.lower():
                    print(f"{interface:<20} {'[DOWN]':<10} ❌ VIOLATION: Interface open but inactive! Should be shutdown.")
                    non_compliant_count += 1
                else:
                    print(f"{interface:<20} {'[OK]':<10}  Compliant.")
                    
        print("-"*69)
        if non_compliant_count == 0:
            print("[+] AUDIT PASSED: Device is 100% compliant with corporate security baseline.")
        else:
            print(f"[!] AUDIT FAILED: Found {non_compliant_count} compliance vulnerabilities that require remediation.")
        print("-"*69 + "\n")
        
        return True

    except Exception as e:
        print(f"[!] Audit scan failed: {e}")
        return False
        
    finally:
        if net_connect:
            net_connect.disconnect()
