import requests

from app.config import DEEP_FACE_SERVER_URL

def face_recognition_using_deep_face(self, img) -> dict:
    # self.logger.info("Sending image to DeepFace server for recognition...")
    response = requests.post(
        f"{DEEP_FACE_SERVER_URL}/recognize",
        files={"image": img},
    )
    return response.json()