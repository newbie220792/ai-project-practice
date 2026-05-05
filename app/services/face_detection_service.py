import cv2

from app.config.config import WORKING_DIR
import face_recognition
import os

def face_detection_from_image(filename, frame):
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces in the test image using the default HOG-based model
    test_bounding_boxes = face_recognition.face_locations(rgb_frame)
    
    no = len(test_bounding_boxes)
    if no == 0:
        cv2.imwrite(f"{WORKING_DIR}/no_faces/{filename}", frame)
    else: 
        cv2.imwrite(f"{WORKING_DIR}/capture_imou/{filename}", frame)
    
    for (top, right, bottom, left) in test_bounding_boxes:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
    
    return test_bounding_boxes  


    