import requests

from app.config import DEEP_FACE_SERVER_URL
from app.config.config import WORKING_DIR

def face_recognition_using_deep_face(img_name) -> dict:
    
    img = open(f"{WORKING_DIR}/capture_imou/{img_name}", "rb")
    if img is None:
        img = open(f"{WORKING_DIR}/no_faces/{img_name}", "rb")
    if img is None:
        return {"error": "Image not found"}
    response = requests.post(
        f"{DEEP_FACE_SERVER_URL}/recognize",
        files={"image": img},
    )
    return response.json()