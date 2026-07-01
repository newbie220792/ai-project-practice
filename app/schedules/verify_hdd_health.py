import os
from app import logger

from gradio_client import file

from app.services.send_email_service import send_email

def verify_hdd_health() -> bool:
    # Implementation for verifying HDD health
    # sudo smartctl -a -d sat /dev/sda1 | grep "Reallocated_Sector_Ct"
    #  5 Reallocated_Sector_Ct   0x0033   098   098   036    Pre-fail  Always       -       44

    output = os.popen(f"sudo smartctl -a -d sat /dev/sda | grep \"Reallocated_Sector_Ct\"").read()
    lines = output.splitlines()
    new_sector = 0
    old_sector = 0
    if lines and len(lines) > 0:
        parts = lines[0].split()
        if len(parts) > 0:
            new_sector = int(parts[-1])
    
    with open("reallocated_sector.txt", "r") as f:
        old_sector = int(f.read().strip())
    
    logger.info(
            f"Reallocated sector count: Old: {old_sector}, New: {new_sector}")
    
    if(new_sector > old_sector):
        logger.warning(
            f"Warning: Reallocated sector count has increased! "
            f"Old: {old_sector}, New: {new_sector}")
        
        with open("reallocated_sector.txt", "w") as f:
            f.write(str(new_sector))

        send_email(
            subject="HDD Health Alert: Reallocated Sector Count Increased",
            body=(
                f"The reallocated sector count of your HDD has increased, "
                f"which may indicate potential issues with the drive.\n\n"
                f"Old Sector Count: {old_sector}\n"
                f"New Sector Count: {new_sector}\n\n"
                f"Please check the HDD health and consider backing up your data."
            ),
            to="bavudoan@gmail.com")
        return False
    return True