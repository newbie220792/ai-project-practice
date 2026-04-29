import shutil

import cv2

import face_recognition
from sklearn import svm
import os
import logger

def face_recognition_from_image(image, encodings=[], names=[]):
    # encodings = []
    # names = []
    
    working_dir = os.getenv("WORK_DIR", "/home/rasp/Desktop/imou")

    # Training directory
    # known_faces_dir = os.listdir(f"{working_dir}/known_faces/")
    # Loop through each person in the training directory
    # for person in known_faces_dir:
    #     pix = os.listdir(f"{working_dir}/known_faces/{person}")

    #     # Loop through each training image for the current person
    #     for person_img in pix:
    #         # Get the face encodings for the face in each image file
    #         face = face_recognition.load_image_file(f"{working_dir}/known_faces/{person}/{person_img}")
    #         face_bounding_boxes = face_recognition.face_locations(face)

    #         #If training image contains exactly one face
    #         if len(face_bounding_boxes) == 1:
    #             face_enc = face_recognition.face_encodings(face)[0]
    #             # Add face encoding for current image with corresponding label (name) to the training data
    #             encodings.append(face_enc)
    #             names.append(person)
    #         else:
    #             logger.warning(f"{person}/{person_img} was skipped and can't be used for training")

    # logger.info("Added encodings for the following people: " + str(set(names)))

    # Create and train the SVC classifier
    clf = svm.SVC(gamma='scale')
    clf.fit(encodings,names)

    if image is None or image == "" or not image.lower().endswith(('.jpg', '.jpeg', '.png')):
        logger.warning(f"Skipping non-image file: {image}")
        return
    else:
        test_image = face_recognition.load_image_file(f"{working_dir}/capture_imou/{image}")
        # Find all the faces in the test image using the default HOG-based model
        test_bounding_boxes = face_recognition.face_locations(test_image)

        no = len(test_bounding_boxes)
        if no == 0:
            logger.info(f"No faces found in the image: {working_dir}/capture_imou/{image}")
            # Optionally, you can choose to remove the image if no faces are found
            # os.remove(f"{working_dir}/capture_imou/{image}")
            _move_file_to_output_folder(image)
        else: 
            # Predict all the faces in the test image using the trained classifier
            logger.info(f"Found: {no} faces in the {working_dir}/capture_imou/{image}.")

            for i in range(no):
                test_image_enc = face_recognition.face_encodings(test_image)[i]
                name = clf.predict([test_image_enc])
                if name != "Unknown" and name is not None and name != "" and len(name) > 0:
                    logger.info(f"Recognized face: {name}")
                    return name[0]
                else:
                    for (top, right, bottom, left), face_encoding in zip(test_bounding_boxes, test_image_enc):
                        matches = face_recognition.compare_faces(encodings, face_encoding)

                        if True in matches:
                            first_match_index = matches.index(True)
                            name = names[first_match_index]
                            return name
                        logger.info(f"Unrecognized face: {name}")

            for (top, right, bottom, left) in test_bounding_boxes:
                cv2.rectangle(test_image, (left, top), (right, bottom), (0, 255, 0), 2)
    
    return "Unknown"


def load_known_faces():
    encodings = []
    names = []
    working_dir = os.getenv("WORK_DIR", "/home/rasp/Desktop/imou")

    # Training directory
    known_faces_dir = os.listdir(f"{working_dir}/known_faces/")
    # Loop through each person in the training directory
    for person in known_faces_dir:
        pix = os.listdir(f"{working_dir}/known_faces/{person}")

        # Loop through each training image for the current person
        for person_img in pix:
            # Get the face encodings for the face in each image file
            face = face_recognition.load_image_file(f"{working_dir}/known_faces/{person}/{person_img}")
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
    working_dir = os.getenv("WORK_DIR", "/home/rasp/Desktop/imou")
    source_path = f"{working_dir}/capture_imou/{fileName}"
    OUTPUT_FOLDER =f"{working_dir}/no_faces"
    destination_path = f"{OUTPUT_FOLDER}/{fileName}"

    try:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        shutil.move(source_path, destination_path)
        logger.info(f"Moved file from {source_path} to {destination_path}")
    
    except FileNotFoundError:
        logger.error(f"File not found: {source_path}")

    except Exception as e:
        logger.error(f"Move failed: {e}")