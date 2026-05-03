from email.mime import message
from flask import Flask, jsonify, request, Response
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import Json
import cv2
import base64
from cryptography.fernet import Fernet
import datetime
from face_recognition_svm_from_image import face_recognition_from_image, load_known_faces
import logger

app = Flask(__name__)

load_dotenv()

BLACKLIST_CAMERAS = set(['Nhà 2', 'Nhà 1'])  # Danh sách đen để lưu trữ các IP đã bị chặn
WORKING_DIR = os.getenv("WORK_DIR")
OUTPUT_FOLDER = os.path.join(WORKING_DIR, "capture_imou")
IMAGE_SERVER_URL = os.getenv("IMAGE_SERVER_URL", "http://localhost/img")
encodings, names = load_known_faces()

@app.route('/callback', methods=['POST','GET', 'PUT', 'DELETE','OPTIONS'])
def callback():
    data = request.json  # nhận JSON từ server gửi tới
    return  post_data(data)
    # xử lý logic ở đây

@app.route('/', methods=['GET'])
def get_data():
    logger.error("This is an error message from the main app")  # Example of logging an error message
    logger.warning("This is a warning message from the main app")  # Example of logging a warning
    logger.info("This is an info message from the main app")  # Example of logging an info message
    logger.critical("This is a critical message from the main app")  # Example of logging a critical message
    return jsonify({"data": "Hello, World!"})

def post_data(data):
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
            time = _unix_to_iso_compact_tz(int(time), tz_offset_hours=7)  # Convert to ISO format with timezone offset  


        if dname in BLACKLIST_CAMERAS:
            logger.warning(f"Camera {dname} is blacklisted. Skipping save.")
            return jsonify({"status": f"Camera '{dname}' is blacklisted. Skipping save."}), 200
        
        fileName, person_name = capture_image_from_camera(did)
        
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
                person_name
            )
        )
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "saved"}), 200
    except Exception as e:
        logger.error(f"Error saving data: {str(e)} with data: {data}")  # Log the error message
        return jsonify({"error": str(e)}), 500

def capture_image_from_camera(camera_id):
    # Define IP mapping for different cameras
    camera_ip = {
        "A4562BCPSFDFF1A": {"ip" :"192.168.1.225","location": "gate"}, #cổng
        "06F2EBDPSF0A55F": {"ip" :"192.168.1.221","location": "living_room"}, #phòng khách
        "C9804BJPSF67B3E": {"ip" :"192.168.1.102","location": "bedroom"}, #phòng ngủ
        "C9804BJPSF52581": {"ip" :"192.168.1.117","location": "kitchen"}, #phòng bếp
        "C9804BJPSF07E00": {"ip" :"192.168.1.143","location": "second_floor"}, #tầng 2
    }

    ip = camera_ip.get(camera_id).get("ip")  # nếu không có thì dùng luôn IP
    location = camera_ip.get(camera_id).get("location", "unknown")
    if not ip :
        raise ValueError(f"Camera ID '{camera_id}' is not recognized or does not have an associated IP address");
    
    username = os.getenv("CAMERA_USERNAME", "admin")
    password = os.getenv("CAMERA_PASSWORD", "password")

    if not username or not password:
        logger.error("Camera credentials are not set in environment variables")  # Log the error message
        raise ValueError("Camera credentials are not set in environment variables")
    
    url = f"rtsp://{username}:{password}@{ip}:554/cam/realmonitor?channel=1&subtype=0"
    logger.info(f"Connecting to camera at {ip} - {location}")  # Log the connection attempt
    
    cap = cv2.VideoCapture(url)
    ret, frame = cap.read()

    current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    fileName = f"{location}_{current_time}_{camera_id}.jpg"

    filepath = os.path.join(OUTPUT_FOLDER, fileName)

    if ret:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        cv2.imwrite(filepath, frame)
    else:
       logger.error(f"Failed to capture image from camera {camera_id} at {url}")  # Log the failure
       raise ValueError("Failed to capture image from camera")

    cap.release()
    person_name = face_recognition_from_image(fileName, encodings, names)

    return fileName, person_name

def _mask_string(value, visible_chars=4):    
    """Mask a string showing only the last N characters."""
    if not value or len(value) <= visible_chars:
        return "*" * len(value)
    return "*" * (len(value) - visible_chars) + value[-visible_chars:]

def decrypt(encryptedValue):
    salt = os.getenv("DECRYPT_SALT", "default_salt")
    decrypted_bytes = base64.b64decode(encryptedValue.encode())
    cipher = Fernet(base64.urlsafe_b64encode(salt.encode().ljust(32)[:32]))
    return cipher.decrypt(decrypted_bytes).decode()


def encrypt(plainValue):
    salt = os.getenv("DECRYPT_SALT", "default_salt")
    cipher = Fernet(base64.urlsafe_b64encode(salt.encode().ljust(32)[:32]))
    encrypted_bytes = cipher.encrypt(plainValue.encode())
    return base64.b64encode(encrypted_bytes).decode()

def _unix_to_iso_compact_tz(ts: int, tz_offset_hours: int = 0) -> str:
    tz = datetime.timezone(datetime.timedelta(hours=tz_offset_hours))
    return datetime.datetime.fromtimestamp(ts, tz).strftime('%Y%m%dT%H%M%S')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)