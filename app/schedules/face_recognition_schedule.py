import os
from time import time

from app import logger
from app.config.config import WORKING_DIR
from app.services import face_recognition_from_image, load_known_faces

def face_recognition_schedule():
    # Schedule the face recognition task to run every 5 minutes
    img_dir = f"{WORKING_DIR}/capture_imou"

    image_files = sorted([
        f for f in os.listdir(img_dir)
        if f.endswith(".jpg") or f.endswith(".png")
    ])

    total_files = len(image_files)
    if total_files == 0:
        logger.info("No images to process.")
        return
    
    encodings, names = load_known_faces()
    for index, img_name in enumerate(image_files, start=1):
        remaining = total_files - index

        logger.info(
            f"Processing image: {img_name} "
            f"({index}/{total_files}) - Remaining: {remaining}"
        )
        
        start_time = time()
        person_name = face_recognition_from_image(img_name, encodings, names)
        # Update person_name to "Unknown" if it is None or empty
        # if not person_name:
        end_time = time()
            
        logger.info(f"Finished processing {img_name} in {end_time - start_time:.2f} seconds. Recognized: {person_name}")