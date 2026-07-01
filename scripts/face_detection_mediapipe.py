import cv2
import mediapipe as mp

def detect_faces(image_path, output_path=None):
    mp_face = mp.solutions.face_detection
    detector = mp_face.FaceDetection()

    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = detector.process(rgb)

    if results.detections:
        for det in results.detections:
            bbox = det.location_data.relative_bounding_box
            h, w, _ = image.shape

            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            w_box = int(bbox.width * w)
            h_box = int(bbox.height * h)

            cv2.rectangle(image, (x,y), (x+w_box, y+h_box), (0,255,0), 2)

    if output_path:
        cv2.imwrite(output_path, image)


if __name__ == "__main__":
    image_path = 'C:\\DATA\\Source_Codes\\ai-project-practice\\images\\living_room_20260428_113709_06F2EBDPSF0A55F.jpg'  # Example image path
    output_path = 'C:\\DATA\\Source_Codes\\ai-project-practice\\faces\\detected_faces_mediapipe.jpg'  # Example output path
    detect_faces(image_path,output_path)