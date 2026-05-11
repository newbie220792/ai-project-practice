from app.services.scan_ip import load_ip, scan_ip
from flask import  jsonify
import psycopg2
import os
from psycopg2.extras import Json
import cv2
import datetime
from app.config import BLACKLIST_CAMERAS, IMAGE_SERVER_URL, OUTPUT_FOLDER
from app.config.config import WORKING_DIR
import app.logger as logger
from app.utils import _unix_to_iso_compact_tz
import time

import face_recognition

def post_data(data) -> jsonify:
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()

        alarmId= data.get("alarmId");
        dname= data.get("dname");
        msgType = data.get("msgType");
        thumbUrl = data.get("thumbUrl");
        time = data.get("time");
        did = data.get("did");
        msgType = data.get("msgType");

        if msgType == "mobileDetect":
            # time = _unix_to_iso_compact_tz(int(time), tz_offset_hours=7)  # Convert to ISO format with timezone offset  
            return jsonify({"status": "mobileDetect received, no image capture needed"}), 200

        if dname in BLACKLIST_CAMERAS:
            logger.warning(f"Camera {dname} is blacklisted. Skipping save.")
            return jsonify({"status": f"Camera '{dname}' is blacklisted. Skipping save."}), 200
        
        fileName = capture_image_from_camera(did)
        
        cur.execute(
            "INSERT INTO imou_camera_log (alarm_id, dname, msg_type, thumb_url, data, created_at, device_id, img, person_name) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                alarmId,
                dname,
                msgType,
                thumbUrl,
                Json(data),
                time,
                did,
                f"{IMAGE_SERVER_URL}/{fileName}",
                "Unknown"  # Placeholder for person_name, to be updated later after face recognition
            )
        )
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "saved"}), 200
    except Exception as e:
        logger.error(f"Error saving data: {str(e)} with data: {data}")  # Log the error message
        return jsonify({"error": str(e)}), 500

def capture_image_from_camera(camera_id) -> str:
    # Define IP mapping for different cameras
    camera_ip = load_ip()

    ip = camera_ip.get(camera_id).get("ip")  # nếu không có thì dùng luôn IP
    location = camera_ip.get(camera_id).get("location", "unknown")
    mac = camera_ip.get(camera_id).get("mac", "unknown")
    if not ip :
        raise ValueError(f"Camera ID '{camera_id}' is not recognized or does not have an associated IP address");
    
    username = os.getenv("CAMERA_USERNAME", "admin")
    password = os.getenv("CAMERA_PASSWORD", "password")

    if not username or not password:
        logger.error("Camera credentials are not set in environment variables")  # Log the error message
        raise ValueError("Camera credentials are not set in environment variables")
    
    url = f"rtsp://{username}:{password}@{ip}:554/cam/realmonitor?channel=1&subtype=0"
    logger.info(f"Connecting to camera at {ip} - {location}")  # Log the connection attempt
    
    current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    fileName = f"{location}_{current_time}_{camera_id}.jpg"
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    i = 0
    cap = None
    while i < 5:
        try:
            cap = cv2.VideoCapture(url)

            if not cap.isOpened():
                raise ConnectionError(f"Failed to connect to camera at {ip} - {location}")
            
            ret, frame = cap.read()

            if not ret or frame is None:
                logger.warning(f"Attempt {i+1}: Failed to read frame")
                i += 1
                time.sleep(1)
                continue

            rgb_frame = frame[:, :, ::-1]

            try:
                boxes = face_recognition.face_locations(rgb_frame)
            except Exception as e:
                logger.error(f"Face detection error: {e}")
                boxes = []

            no = len(boxes)
            if no > 0:
                cv2.imwrite(f"{WORKING_DIR}/capture_imou/{fileName}", frame)
                break
            elif i == 4:
                cv2.imwrite(f"{WORKING_DIR}/no_faces/{fileName}", frame)

        except Exception as e:
            if e is ConnectionError:
                logger.warning(f"Attempt {i+1}: Connection error - {e}. Retrying...")
                ip = scan_ip(camera_id)
                url = f"rtsp://{username}:{password}@{ip}:554/cam/realmonitor?channel=1&subtype=0"
            else:
                logger.error(f"Attempt {i+1}: Error - {e}")

        finally:
            if cap is not None:
                cap.release()
        i += 1
        time.sleep(1)
        
    return fileName
   
    