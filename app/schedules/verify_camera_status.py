import os

from flask import json

from app import logger
from app.services import scan_all_ip, scan_ip, load_ip
from app.services.send_email_service import send_email

def verify_camera_status():
    ip_list = load_ip()
    camera_id = scan_all_ip()

    for camera in ip_list.items():
        camera_info = camera[1]
        mac = camera_info['mac']
        location = camera_info['location']
        ip = camera_info['ip']
        new_ip = camera_id.get(mac)
        if new_ip:
            if new_ip == camera_info['ip']:
                logger.info(f"Camera {mac} is online with IP {new_ip}.")
            else:
                logger.warning(f"Camera {mac} has changed IP from {ip} to {new_ip}.")
                # Update the IP in the database or configuration here
                camera_info["ip"] = new_ip
        else:
            logger.error(f"Camera {location} is offline or not detected.")
            # send email or alert here
            send_email(
                subject=f"Camera {location} is offline",
                body=f"The camera with MAC address {location} is currently offline or not detected. Please check the device."
            )
    logger.info("Camera status verification completed and updated IP list.")
    
    with open("etc/ip_mapping.json", "w") as f:
        json.dump(ip_list, f, indent=4)
    return
