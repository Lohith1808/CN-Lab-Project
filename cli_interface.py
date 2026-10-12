"""
cli_interface.py
Terminal Interface & ASCII Display Module
"""

from core_engine import (
    calculate_subnet_details, 
    calculate_vlsm, 
    mask_to_cidr
)

def print_banner():
    print("=" * 70)
    print("        COMPUTER NETWORKS LAB (A405512) - SUBNET CALCULATOR TOOL")
    print("=" * 70)

def display_subnet_table(data: dict):
    print("\n" + "-" * 70)
    print(f"{'PARAMETER':<25} | {'VALUE':<42}")
    print("-" * 70)
    print(f"{'IP Address':<25} | {data['ip_address']} ({data['cidr_prefix']})")
    print(f"{'IP Binary':<25} | {data['ip_binary']}")
    print(f"{'Subnet Mask':<25} | {data['subnet_mask']}")
    print(f"{'Subnet Mask Binary':<25} | {data['mask_binary']}")
    print(f"{'Wildcard Mask':<25} | {data['wildcard_mask']}")
    print(f"{'Network Address (ID)':<25} | {data['network_id']}")
    print(f"{'Broadcast Address':<25} | {data['broadcast_id']}")
    print(f"{'Usable Host Range':<25} | {data['first_usable']} - {data['last_usable']}")
    print(f"{'Total Hosts':<25} | {data['total_hosts']}")
    print(f"{'Usable Hosts':<25} | {data['usable_hosts']}")
    print(f"{'Classful Category':<25} | {data['ip_class']}")
    print(f"{'Address Scope':<25} | {data['ip_scope']}")
    print("-" * 70 + "\n")

def run_flsm_interactive():
    print("\n--- Standard Subnet Calculation (FLSM / CIDR) ---")
    raw_input = input("Enter IP with CIDR or Mask (e.g., 192.168.10.25/27 or 10.0.0.1 255.255.0.0): ").strip()
    
    try:
        if "/" in raw_input:
            ip_part, cidr_part = raw_input.split("/")
            cidr = int(cidr_part)
        elif " " in raw_input:
            ip_part, mask_part = raw_input.split()
            cidr = mask_to_cidr(mask_part)
        else:
            ip_part = raw_input
            cidr = 24
            print("Prefix not specified. Defaulting to /24.")
            
        result = calculate_subnet_details(ip_part, cidr)
        display_subnet_table(result)
    except Exception as e:
        print(f"\n[Error]: {e}")

def run_vlsm_interactive():
    print("\n--- Variable Length Subnet Masking (VLSM) ---")
    base_net = input("Enter Base Network (e.g., 192.168.1.0/24): ").strip()
    
    try:
        if "/" not in base_net:
            raise ValueError("Base network must include prefix notation (e.g., /24).")
        ip_part, cidr_part = base_net.split("/")
        base_cidr = int(cidr_part)
        
        num_subnets = int(input("Enter number of subnets needed: ").strip())
        requirements = []
        for i in range(num_subnets):
            name = input(f"  Name for Subnet {i+1} (e.g., Sales): ").strip() or f"Subnet_{i+1}"
            hosts = int(input(f"  Required usable hosts for {name}: ").strip())
            requirements.append((name, hosts))
            
        allocations = calculate_vlsm(ip_part, base_cidr, requirements)
        
        print("\n" + "=" * 80)
        print(f"{'Name':<12} | {'Needed':<6} | {'Allocated':<9} | {'Network ID':<15} | {'CIDR':<5} | {'Broadcast ID':<15}")
        print("=" * 80)
        for sub in allocations:
            print(f"{sub['subnet_name']:<12} | {sub['requested_hosts']:<6} | {sub['usable_hosts']:<9} | "
                  f"{sub['network_id']:<15} | {sub['cidr_prefix']:<5} | {sub['broadcast_id']:<15}")
        print("=" * 80)
        print("\nAllocation complete with no IP overlaps.")
    except Exception as e:
        print(f"\n[Error]: {e}")

def run_app():
    while True:
        print_banner()
        print("1. Standard Subnet Calculation (CIDR / FLSM)")
        print("2. Variable Length Subnet Masking (VLSM Design)")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()
        
        if choice == "1":
            run_flsm_interactive()
        elif choice == "2":
            run_vlsm_interactive()
        elif choice == "3":
            print("\nExiting Subnet Calculator Tool.")
            break
        else:
            print("\nInvalid choice. Please select 1, 2, or 3.")
        
        input("Press Enter to continue...")