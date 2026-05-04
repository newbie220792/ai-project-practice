import sys
from turtle import home
import cv2
import face_recognition
import os
import app.logger as logger
import datetime

WORKING_DIR = os.getenv("WORK_DIR")
current_date = datetime.datetime.now().strftime('%Y%m%d')
log_dir = os.path.join(WORKING_DIR, "logs")

os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"{current_date}_image.log")

logger.set_file_logger(log_file)

def detect_faces(image_path, output_path=None):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Unable to open image: {image_path}")
    
    # image = cv2.resize(image, (640, 480))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # if output_path:
    #     if len(faces) == 0:
    #         raise RuntimeError("No faces detected to crop")
    #     x, y, w, h = faces[0]
        
    #     # face cropping
    #     image = image[y:y+h, x:x+w] 
    #     cv2.imwrite(output_path, image)

    _face_recognition(image)

    cv2.imwrite(output_path, image)
        
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def _face_recognition(face):
    known_encodings = []
    known_names = []

    working_dir = os.getenv("WORK_DIR")

    # load known faces
    for file in os.listdir(f"{working_dir}/known_faces/"):
        if file is None or file == "" or not file.lower().endswith(('.jpg', '.jpeg', '.png')):
            logger.warning(f"Skipping non-image file: {file}")
            continue
        img = face_recognition.load_image_file(f"{working_dir}/known_faces/{file}")
        enc = face_recognition.face_encodings(img)

        if len(enc) == 0:
            logger.warning(f"No face found in {file}, skipping.")
            continue
        known_encodings.append(enc)
        known_names.append(file.split(".")[0])
    
    if len(known_encodings) == 0:
        logger.warning("No known faces loaded, skipping recognition.")
        return
    
    face_locations = face_recognition.face_locations(face)
    face_encodings = face_recognition.face_encodings(face, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]

        # cv2.rectangle(face, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(face, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

if __name__ == "__main__":
    image_path = os.path.join(WORKING_DIR, "images", "living_room_20260428_145439_06F2EBDPSF0A55F.jpg")  # Example image path
    output_path = os.path.join(WORKING_DIR, "face_detected", "detected_faces.jpg")  # Example output path
    detect_faces(image_path, output_path)