import os

response = os.system(f"sudo arp-scan --localnet | grep -v 'Starting' | grep -v 'Ending'")