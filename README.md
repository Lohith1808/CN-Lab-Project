# Subnet Mask Calculator & Network Design Tool

**Course:** B.Tech CSE V Semester  
**Subject:** Computer Networks Laboratory (`A405512`)  
**Theory Code:** `A405310` (Unit III: Network Layer - Internetworking & Subnets)  
**Course Outcome:** CO3 (Classify routing protocols and analyze how to assign IP addresses)

---

## 1. Description
A modular Python tool that demonstrates bitwise mathematical logic used in the Network Layer of the TCP/IP stack. It performs standard CIDR/FLSM subnet breakdown and Variable Length Subnet Masking (VLSM) without high-level wrapper libraries.

## 2. Core Bitwise Formulas Implemented
- **Subnet Mask from CIDR:**  
  `Mask = (0xFFFFFFFF << (32 - CIDR)) & 0xFFFFFFFF`
- **Network ID:**  
  `Network_ID = IP_Address & Subnet_Mask`
- **Wildcard Mask:**  
  `Wildcard_Mask = ~Subnet_Mask & 0xFFFFFFFF`
- **Broadcast Address:**  
  `Broadcast_Address = Network_ID | Wildcard_Mask`
- **Host Calculation:**  
  `Total Hosts = 2^(32 - CIDR)`  
  `Usable Hosts = 2^(32 - CIDR) - 2` (for prefixes <= 30)

---

## 3. How to Run
Navigate to the directory and run:

```bash
python main.py