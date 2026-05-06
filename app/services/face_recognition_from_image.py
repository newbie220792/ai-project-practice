from fileinput import filename
import shutil
from tkinter.font import names
import cv2

from app.config import WORKING_DIR

import face_recognition
from sklearn import svm
import os
import app.logger as logger

def face_recognition_from_image(filename, encodings:list[str]=[], names:list[str]=[]) -> str:
    # Create and train the SVC classifier
    clf = svm.SVC(gamma='scale')
    clf.fit(encodings,names)
    person_name = "Unknown"

    if filename is None or filename == "" or not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        logger.warning(f"Skipping non-image file: {filename}")
        return person_name
    else:
        # Find all the faces in the test image using the CNN model instead of the HOG-based model
        image_test = face_recognition.load_image_file(f"{WORKING_DIR}/capture_imou/{filename}")
        test_bounding_boxes = face_recognition.face_locations(image_test)

        no = len(test_bounding_boxes)
        
        if no != 0:
            # Predict all the faces in the test image using the trained classifier
            logger.info(f"Found: {no} faces in the {WORKING_DIR}/capture_imou/{filename}.")

            for i in range(no):
                test_image_enc = face_recognition.face_encodings(image_test)[i]

                for (top, right, bottom, left), face_encoding in zip(test_bounding_boxes, test_image_enc):
                    matches = face_recognition.compare_faces(encodings, face_encoding)

                    logger.info(f"Drawing in the {filename}")
                    cv2.rectangle(image_test, (left, top), (right, bottom), (0, 255, 0), 2)
                    
                    if True in matches:
                        first_match_index = matches.index(True)
                        person_name = names[first_match_index]
                        logger.info(f"Recognized face: {person_name}")
                        cv2.putText(image_test, person_name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                        break

                # Try SVM to recognize
                if person_name == "Unknown":
                     # Predict the name of the person in the test image using the SVM classifier
                    name = clf.predict([test_image_enc])
                    if name != "Unknown" and name is not None and name != "" and len(name) > 0:
                        logger.info(f"Recognized face: {name}")
                        person_name = name[0]
                        continue
                cv2.imwrite(f"{WORKING_DIR}/capture_imou/{filename}", image_test)
                logger.warning(f"Unrecognized face: {person_name} using direct comparison.")
                i += 1
        else: 
            logger.warning(f"No faces found in the image: {filename}")
            os.remove(f"{WORKING_DIR}/capture_imou/{filename}")
    return person_name

def load_known_faces():
    encodings = []
    names = []

    # Training directory
    known_faces_dir = os.listdir(f"{WORKING_DIR}/known_faces/")
    # Loop through each person in the training directory
    for person in known_faces_dir:
        pix = os.listdir(f"{WORKING_DIR}/known_faces/{person}")

        # Loop through each training image for the current person
        for person_img in pix:
            # Get the face encodings for the face in each image file
            face = face_recognition.load_image_file(f"{WORKING_DIR}/known_faces/{person}/{person_img}")
            face_bounding_boxes = face_recognition.face_locations(face)

            #If training image contains exactly one face
            if len(face_bounding_boxes) == 1:
                face_enc = face_recognition.face_encodings(face)[0]
                # Add face encoding for current image with corresponding label (name) to the training data
                encodings.append(face_enc)
                names.append(person)
            else:
                logger.warning(f"{person}/{person_img} was skipped and can't be used for training")

    logger.info("Added encodings for the following people: " + str(set(names)))
    return encodings, names

def _move_file_to_output_folder(fileName):
    source_path = f"{WORKING_DIR}/capture_imou/{fileName}"
    OUTPUT_FOLDER =f"{WORKING_DIR}/no_faces"
    destination_path = f"{OUTPUT_FOLDER}/{fileName}"

    try:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        shutil.move(source_path, destination_path)
        logger.info(f"Moved file from {source_path} to {destination_path}")
    
    except FileNotFoundError:
        logger.error(f"File not found: {source_path}")

    except Exception as e:
        logger.error(f"Move failed: {e}")