import json
import os

def scan_ip(mac)-> str:
    output = os.popen(f"sudo arp-scan --localnet | grep -v 'Starting' | grep -v 'Ending'").read()
    lines = output.splitlines()
    for line in lines:
        if mac in line:
            ip = line.split()[0]
            return ip
    raise ValueError(f"IP address for MAC {mac} not found")

def scan_all_ip()-> dict:
    output = os.popen(f"sudo arp-scan --localnet | grep -v 'Starting' | grep -v 'Ending'").read()
    lines = output.splitlines()
    ip_dict = {}
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            mac = parts[1]
            ip = parts[0]
            ip_dict[mac] = ip
    return ip_dict

def load_ip() -> dict:
    return json.load(open("ip_mapping.json", "r"))