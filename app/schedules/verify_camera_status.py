from flask import json

from app import logger
from app.services import scan_all_ip, scan_ip, load_ip
from app.services.send_email_service import send_email

def verify_camera_status():
    ip_list = load_ip()
    logger.info("Starting camera status verification..." + str(ip_list))
    camera_id = scan_all_ip()

    for camera in ip_list:
        new_ip = camera_id.get(camera["mac"])
        if new_ip:
            if new_ip == camera["ip"]:
                logger.info(f"Camera {camera['mac']} is online with IP {new_ip}.")
            else:
                logger.warning(f"Camera {camera['mac']} has changed IP from {camera['ip']} to {new_ip}.")
                # Update the IP in the database or configuration here
                camera["ip"] = new_ip
        else:
            logger.error(f"Camera {camera['mac']} is offline or not detected.")
            # send email or alert here
            send_email(
                subject=f"Camera {camera['location']} is offline",
                body=f"The camera with MAC address {camera['location']} is currently offline or not detected. Please check the device."
            )
    logger.info("Camera status verification completed and updated ip list: " + str(ip_list))
    
    with open("ip_mapping.json", "w") as f:
        json.dump(ip_list, f, indent=4)
    return
