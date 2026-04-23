from email.mime import message
import time

from flask import Flask, jsonify, request, Response
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import Json
import cv2
import base64
from cryptography.fernet import Fernet
import logger

app = Flask(__name__)

load_dotenv()

BLACKLIST_CAMERAS = set(['Nhà 2', 'Nhà 1'])  # Danh sách đen để lưu trữ các IP đã bị chặn

@app.route('/callback', methods=['POST','GET', 'PUT', 'DELETE'])
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

        if dname in BLACKLIST_CAMERAS:
            logger.warning(f"Camera {dname} is blacklisted. Skipping save.")
            return jsonify({"status": f"Camera '{dname}' is blacklisted. Skipping save."}), 200
        
        capture_image_from_camera(did)
        cur.execute(
            "INSERT INTO imou_camera_log (alarm_id, dname, msg_type, thumb_url, data, created_at, device_id, img) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                alarmId,
                dname,
                msgType,
                thumbUrl,
                Json(data),
                time,
                did,
                "http://example.com/default_image.jpg"
            )
        )
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "saved"}), 200
    except Exception as e:
        print(str(e));
        logger.error(f"Error saving data: {str(e)}")  # Log the error message
        return jsonify({"error": str(e)}), 500

def capture_image_from_camera(camera_id):
    # Define IP mapping for different cameras
    camera_ip = {
        "A4562BCPSFDFF1A": "192.168.1.225", #cổng
        "06F2EBDPSF0A55F": "192.168.1.221", #phòng khách
        "C9804BJPSF67B3E": "192.168.1.102", #phòng ngủ
        "C9804BJPSF52581": "192.168.1.117", #phòng bếp
        "C9804BJPSF07E00": "192.168.1.143", #tầng 2
    }

    ip = camera_ip.get(camera_id)  # nếu không có thì dùng luôn IP
    if not ip :
        raise ValueError(f"Camera ID '{camera_id}' is not recognized or does not have an associated IP address");
    
    username = os.getenv("CAMERA_USERNAME", "admin")
    password = os.getenv("CAMERA_PASSWORD", "password")

    if not username or not password:
        raise ValueError("Camera credentials are not set in environment variables")
    
    url = f"rtsp://{username}:{password}@{ip}:554/cam/realmonitor?channel=1&subtype=0"
    logger.info(f"Connecting to camera at {url}")  # Log the connection attempt
    
    cap = cv2.VideoCapture(url)
    ret, frame = cap.read()

    timestamp = int(time.time())

    OUTPUT_FOLDER = "/home/rasp/Desktop/imou/capture_imou"
    filepath = os.path.join(OUTPUT_FOLDER, f"{camera_id}_{timestamp}.jpg")

    if ret:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        cv2.imwrite(filepath, frame)
    else:
       logger.error(f"Failed to capture image from camera {camera_id} at {url}")  # Log the failure
       raise ValueError("Failed to capture image from camera")

    cap.release()

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)