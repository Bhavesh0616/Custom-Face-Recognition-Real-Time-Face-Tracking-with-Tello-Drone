import cv2
import face_recognition
import numpy as np
import os
import time

# Ensure the database directory exists
if not os.path.exists("face_database"):
    os.makedirs("face_database")

# Get user name
person_name = input("Enter your name: ").strip()

# Initialize camera
cap = cv2.VideoCapture(0)

# Face encoding storage
face_encodings_list = []
samples_collected = 0
MAX_SAMPLES = 10  # Collect 10 good samples for accuracy

while samples_collected < MAX_SAMPLES:
    ret, frame = cap.read()
    if not ret:
        continue  # Skip if no frame captured

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)

    if len(face_locations) == 1:  # Ensure only one face is in the frame
        top, right, bottom, left = face_locations[0]
        face_encoding = face_recognition.face_encodings(rgb_frame, [face_locations[0]])[0]

        # Store encoding if it's valid
        face_encodings_list.append(face_encoding)
        samples_collected += 1
        print(f"✅ Sample {samples_collected}/{MAX_SAMPLES} collected")

        # Draw box & show progress
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, f"Capturing Face {samples_collected}/{MAX_SAMPLES}", 
                    (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Face Detection", frame)

    # Press 'q' to manually exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Compute the average encoding for more accuracy
if len(face_encodings_list) > 0:
    avg_face_encoding = np.mean(face_encodings_list, axis=0)
    np.save(f"face_database/{person_name}.npy", avg_face_encoding)
    print(f"🎯 Face data for {person_name} successfully saved with high accuracy!")

print("✅ Face detection process completed and automatically stopped!")
