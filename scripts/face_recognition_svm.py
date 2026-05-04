import cv2

import face_recognition
from sklearn import svm
import os

# Training the SVC classifier

def face_recognition_svm():
# The training data would be all the face encodings from all the known images and the labels are their names
    encodings = []
    names = []
    
    working_dir = os.getenv("WORK_DIR")

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
                print(person + "/" + person_img + " was skipped and can't be used for training")

    print("Added encodings for the following people: " + str(set(names)))

    # Create and train the SVC classifier
    clf = svm.SVC(gamma='scale')
    clf.fit(encodings,names)

    # Load the test image with unknown faces into a numpy array
    test_image_dir = os.listdir(f"{working_dir}/capture_imou/")
    for image in test_image_dir:
        if image is None or image == "" or not image.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Skipping non-image file: {image}")
            continue

        test_image = face_recognition.load_image_file(f"{working_dir}/capture_imou/{image}")
        # Find all the faces in the test image using the default HOG-based model
        test_bounding_boxes = face_recognition.face_locations(test_image)

        no = len(test_bounding_boxes)
        if no == 0:
            print(f"No faces found in the image: {working_dir}/capture_imou/{image}")

            os.remove(f"{working_dir}/capture_imou/{image}")
            print(f"Removed image: {working_dir}/capture_imou/{image}")
            continue
        
        # Predict all the faces in the test image using the trained classifier
        print(f"Found: {no} faces in the {working_dir}/capture_imou/{image}.")

        for i in range(no):
            test_image_enc = face_recognition.face_encodings(test_image)[i]
            name = clf.predict([test_image_enc])
            if name != "Unknown" and name is not None and name != "" and len(name) > 0:
                print(*name)
            else:
                for (top, right, bottom, left), face_encoding in zip(test_bounding_boxes, test_image_enc):
                    matches = face_recognition.compare_faces(encodings, face_encoding)
                    name = "Unknown"

                    if True in matches:
                        first_match_index = matches.index(True)
                        name = names[first_match_index]

                    print(name)

    # face_locations = face_recognition.face_locations(test_image)
    # for (top, right, bottom, left) in face_locations:
    #     cv2.rectangle(test_image, (left, top), (right, bottom), (0, 255, 0), 2)

if __name__ == "__main__":
    face_recognition_svm()