from flask import json
import requests

from app import logger
from app.config import DEEP_FACE_SERVER_URL
from app.config.config import WORKING_DIR

def face_recognition_using_deep_face(img_name) -> str:
    
    img = open(f"{WORKING_DIR}/capture_imou/{img_name}", "rb")
    if img is None:
        img = open(f"{WORKING_DIR}/no_faces/{img_name}", "rb")
    if img is None:
        return {"error": "Image not found"}
    response = requests.post(
        f"{DEEP_FACE_SERVER_URL}/recognize",
        files={"image": img},
    )
    json_response = response.json()
    logger.info(f"DeepFace response for {img_name}: {json_response}")
    if json_response is None or json_response == "" or "name" not in json_response or json_response.get("name") is None or json_response.get('error'):
        return "Unknown"
    return json_response.get("name")