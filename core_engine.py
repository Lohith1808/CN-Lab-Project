"""
core_engine.py
Network Layer Bitwise Calculation Engine
Course: Computer Networks (A405310 / A405512)
"""

import math

def ip_to_int(ip_str: str) -> int:
    """Convert dotted-decimal IPv4 string to 32-bit integer."""
    octets = [int(o) for o in ip_str.strip().split(".")]
    if len(octets) != 4 or any(o < 0 or o > 255 for o in octets):
        raise ValueError("Invalid IPv4 address format.")
    return (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]

def int_to_ip(ip_int: int) -> str:
    """Convert 32-bit integer to dotted-decimal IPv4 string."""
    return f"{(ip_int >> 24) & 0xFF}.{(ip_int >> 16) & 0xFF}.{(ip_int >> 8) & 0xFF}.{ip_int & 0xFF}"

def int_to_bin_str(ip_int: int) -> str:
    """Convert 32-bit integer to 4-octet dotted binary representation."""
    binary = f"{ip_int:032b}"
    return f"{binary[0:8]}.{binary[8:16]}.{binary[16:24]}.{binary[24:32]}"

def cidr_to_mask_int(cidr: int) -> int:
    """Generate 32-bit mask integer from CIDR prefix length (0-32)."""
    if cidr < 0 or cidr > 32:
        raise ValueError("CIDR prefix must be between 0 and 32.")
    if cidr == 0:
        return 0
    return (0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF

def mask_to_cidr(mask_str: str) -> int:
    """Derive CIDR prefix length from dotted-decimal subnet mask."""
    mask_int = ip_to_int(mask_str)
    bin_str = f"{mask_int:032b}"
    if "01" in bin_str:
        raise ValueError("Invalid subnet mask: contiguous 1s required.")
    return bin_str.count("1")

def determine_ip_class(first_octet: int) -> str:
    """Identify traditional classful addressing scheme."""
    if 1 <= first_octet <= 126:
        return "Class A"
    elif first_octet == 127:
        return "Class A (Loopback Address)"
    elif 128 <= first_octet <= 191:
        return "Class B"
    elif 192 <= first_octet <= 223:
        return "Class C"
    elif 224 <= first_octet <= 239:
        return "Class D (Multicast)"
    elif 240 <= first_octet <= 255:
        return "Class E (Experimental)"
    return "Unknown"

def determine_ip_scope(ip_int: int) -> str:
    """Identify Private (RFC 1918) vs Public addressing scope."""
    o1 = (ip_int >> 24) & 0xFF
    o2 = (ip_int >> 16) & 0xFF
    if o1 == 10:
        return "Private (10.0.0.0/8)"
    if o1 == 172 and 16 <= o2 <= 31:
        return "Private (172.16.0.0/12)"
    if o1 == 192 and o2 == 168:
        return "Private (192.168.0.0/16)"
    if o1 == 127:
        return "Loopback"
    if o1 >= 224:
        return "Reserved"
    return "Public"

def calculate_subnet_details(ip_str: str, cidr: int) -> dict:
    """Perform bitwise ANDing and compute full subnet boundaries."""
    ip_num = ip_to_int(ip_str)
    mask_num = cidr_to_mask_int(cidr)
    wildcard_num = (~mask_num) & 0xFFFFFFFF
    
    network_num = ip_num & mask_num
    broadcast_num = network_num | wildcard_num
    
    total_hosts = 2 ** (32 - cidr)
    
    if cidr == 32:
        usable_hosts = 1
        first_usable = network_num
        last_usable = network_num
    elif cidr == 31:
        usable_hosts = 2
        first_usable = network_num
        last_usable = broadcast_num
    else:
        usable_hosts = total_hosts - 2
        first_usable = network_num + 1
        last_usable = broadcast_num - 1
        
    first_octet = (ip_num >> 24) & 0xFF

    return {
        "ip_address": int_to_ip(ip_num),
        "ip_binary": int_to_bin_str(ip_num),
        "cidr_prefix": f"/{cidr}",
        "subnet_mask": int_to_ip(mask_num),
        "mask_binary": int_to_bin_str(mask_num),
        "wildcard_mask": int_to_ip(wildcard_num),
        "network_id": int_to_ip(network_num),
        "broadcast_id": int_to_ip(broadcast_num),
        "first_usable": int_to_ip(first_usable),
        "last_usable": int_to_ip(last_usable),
        "total_hosts": total_hosts,
        "usable_hosts": usable_hosts,
        "ip_class": determine_ip_class(first_octet),
        "ip_scope": determine_ip_scope(ip_num)
    }

def calculate_vlsm(base_ip: str, base_cidr: int, requirements: list) -> list:
    """
    Compute Variable Length Subnet Masking (VLSM).
    requirements format: [('Dept A', 50), ('Dept B', 20), ...]
    """
    sorted_reqs = sorted(requirements, key=lambda x: x[1], reverse=True)
    current_network = ip_to_int(base_ip) & cidr_to_mask_int(base_cidr)
    
    allocations = []
    for name, req_hosts in sorted_reqs:
        # formula: 2^h - 2 >= req_hosts => 2^h >= req_hosts + 2
        host_bits = math.ceil(math.log2(req_hosts + 2)) if req_hosts > 0 else 2
        if host_bits < 2:
            host_bits = 2
        subnet_cidr = 32 - host_bits
        
        if subnet_cidr < base_cidr:
            raise ValueError(f"Requirement for '{name}' exceeds base network address space.")
            
        details = calculate_subnet_details(int_to_ip(current_network), subnet_cidr)
        details["subnet_name"] = name
        details["requested_hosts"] = req_hosts
        allocations.append(details)
        
        # Advance network pointer by block size (total hosts)
        current_network += details["total_hosts"]
        
    return allocations