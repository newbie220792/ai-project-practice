import json
import os

def scan_ip(camera_id)-> str:
    ip_mapping = load_ip()
    return ip_mapping.get(camera_id, {}).get("ip")

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

def load_ip():
    return json.load(open("etc/ip_mapping.json", "r"))