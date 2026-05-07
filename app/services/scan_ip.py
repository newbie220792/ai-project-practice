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


def load_ip() -> dict:
    return json.load(open("ip_mapping.json", "r"))