from dotenv import load_dotenv
import os

load_dotenv()

BLACKLIST_CAMERAS = set([cam.strip() for cam in os.getenv("BLACKLIST_CAMERAS").split(",")])  # Danh sách đen để lưu trữ các IP đã bị chặn
WORKING_DIR = os.getenv("WORK_DIR")
OUTPUT_FOLDER = os.path.join(WORKING_DIR, "capture_imou")
IMAGE_SERVER_URL = os.getenv("IMAGE_SERVER_URL", "http://localhost/img")
DEEP_FACE_SERVER_URL = os.getenv("DEEP_FACE_SERVER_URL", "http://localhost:5000")
ENABLE_SCHEDULE = os.getenv("ENABLE_SCHEDULE", "false")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
CAMERA_USERNAME = os.getenv("CAMERA_USERNAME")
CAMERA_PASSWORD = os.getenv("CAMERA_PASSWORD")