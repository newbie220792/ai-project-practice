from dotenv import load_dotenv
import os

load_dotenv()

BLACKLIST_CAMERAS = set(['Nhà 2', 'Nhà 1'])  # Danh sách đen để lưu trữ các IP đã bị chặn
WORKING_DIR = os.getenv("WORK_DIR")
OUTPUT_FOLDER = os.path.join(WORKING_DIR, "capture_imou")
IMAGE_SERVER_URL = os.getenv("IMAGE_SERVER_URL", "http://localhost/img")
