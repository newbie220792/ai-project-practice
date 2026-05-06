import os
from time import time

from app import logger
from app.config.config import WORKING_DIR
from app.services import face_recognition_from_image, face_recognition_using_deep_face, load_known_faces

def face_recognition_schedule():
    # Schedule the face recognition task to run every 5 minutes
    img_dir = f"{WORKING_DIR}/capture_imou"
    encodings, names = load_known_faces()
    for img_name in os.listdir(img_dir):
        if img_name.endswith(".jpg") or img_name.endswith(".png"):
            logger.info(f"Processing image: {img_name}")
            
            start_time = time()
            person_name = face_recognition_from_image(img_name, encodings, names)
            if person_name == "Unknown":
                person_name = face_recognition_using_deep_face(img_name)
            end_time = time()
            
            logger.info(f"Finished processing {img_name} in {end_time - start_time:.2f} seconds. Recognized: {person_name}")


