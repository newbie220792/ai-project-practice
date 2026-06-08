import os
from app import logger

from gradio_client import file

from app.services.send_email_service import send_email

def verify_hdd_health() -> bool:
    # Implementation for verifying HDD health
    # sudo smartctl -a -d sat /dev/sda1 | grep "Reallocated_Sector_Ct"
    #  5 Reallocated_Sector_Ct   0x0033   098   098   036    Pre-fail  Always       -       44

    output = os.popen(f"smartctl -a -d sat /dev/sda1 | grep \"Reallocated_Sector_Ct\"").read()
    lines = output.splitlines()
    new_sector = 0
    old_sector = 0
    if lines and len(lines) > 0:
        parts = lines[0].split()
        if len(parts) > 0:
            new_sector = int(parts[-1])
    
    with open("reallocated_sector.txt", "r") as f:
        old_sector = file.load(f)
        if(new_sector > old_sector):
            logger.warning("Warning: Reallocated sector count has increased!")
            file.save(new_sector, f)
            send_email(
                subject="HDD Health Alert: Reallocated Sector Count Increased",
                body="The reallocated sector count of your HDD has increased, which may indicate potential issues with the drive. Please check the HDD health and consider backing up your data.",
                to="user@example.com"
            )
            return False
        
    # return old_sector != 0 and new_sector != 0 and new_sector > old_sector
    return True