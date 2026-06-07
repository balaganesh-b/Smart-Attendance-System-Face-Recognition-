import os
import cv2
import numpy as np
import face_recognition
from attendance_utils import mark_attendance

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
KNOWN_FACES_DIR = os.path.join(DATA_DIR, "known_faces")


def load_known_faces():
    """Load known face encodings and their names from KNOWN_FACES_DIR."""
    known_encodings = []
    known_names = []

    if not os.path.exists(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR, exist_ok=True)
        print(f"[INFO] Created directory: {KNOWN_FACES_DIR}")
        print("[INFO] Please add images of known people into this folder and re-run.")
        return known_encodings, known_names

    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if len(encodings) == 0:
                print(f"[WARNING] No face found in {filename}. Skipping.")
                continue
            encoding = encodings[0]
            name = os.path.splitext(filename)[0]
            known_encodings.append(encoding)
            known_names.append(name)
            print(f"[INFO] Loaded encoding for {name} from {filename}")

    if not known_encodings:
        print("[WARNING] No valid faces found in known_faces directory.")
    return known_encodings, known_names


def main():
    known_encodings, known_names = load_known_faces()

    if len(known_encodings) == 0:
        print("[ERROR] No known faces available. Exiting.")
        return

    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("[ERROR] Could not open webcam.")
        return

    print("[INFO] Press 'q' to quit.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("[ERROR] Failed to read frame from webcam.")
            break

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces and encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)

            name = "Unknown"

            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]
                    mark_attendance(name)

            # Scale back up face locations since we detected on the smaller image
            top, right, bottom, left = face_location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Label with name
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

        cv2.imshow("Smart Attendance - Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
