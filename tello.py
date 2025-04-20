from djitellopy import Tello
import face_recognition
import cv2
import numpy as np
import os

# ✅ Ensure Bhavesh's face encoding exists
face_database_path = r"F:\Project - D\face_recognition_system\face_database\Bhavesh.npy"
if not os.path.exists(face_database_path):
    print("❌ Error: Bhavesh's face encoding file not found! Please run face capture first.")
    exit()

# ✅ Load Bhavesh's face encoding
bhavesh_face_encoding = np.load(face_database_path, allow_pickle=True)
known_face_encodings = [bhavesh_face_encoding]
known_face_names = ["Bhavesh"]

# ✅ Initialize Tello drone
tello = Tello()
tello.connect()
print(f"🔋 Battery: {tello.get_battery()}%")

# ✅ Start Tello video stream
tello.streamon()

# 🎥 **Step 1: Display Live Feed & Detect Face**
print("\n🎥 **Tello Live Stream Started!**")
print("🔍 Looking for Bhavesh's face...")

face_detected = False

while not face_detected:
    frame = tello.get_frame_read().frame
    if frame is None or frame.size == 0:
        print("⚠️ Warning: No frame received from Tello!")
        continue

    frame = cv2.resize(frame, (720, 480))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ✅ Face Recognition (Before Takeoff)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)

        if True in matches:
            face_detected = True
            print("✅ Bhavesh detected! Taking off...")
            tello.takeoff()
            break  # Exit the loop to start tracking

    # ✅ Show live video feed
    cv2.imshow("Tello Live Stream (Face Recognition)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        tello.streamoff()
        cv2.destroyAllWindows()
        exit()

# 🎯 **Step 2: Face Tracking & Hovering**
print("🔄 Locking onto Bhavesh's face and hovering...")

frame_center_x, frame_center_y = 360, 240
dead_zone = 20  # Smaller dead zone for smoother hovering
speed = 10  # Reduce speed for smooth movements

while True:
    frame = tello.get_frame_read().frame
    if frame is None or frame.size == 0:
        print("⚠️ Warning: No frame received from Tello!")
        continue

    frame = cv2.resize(frame, (720, 480))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect and recognize faces
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    recognized = False

    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)

        if True in matches:
            recognized = True
            # Calculate face position relative to frame center
            face_x = (left + right) // 2
            face_y = (top + bottom) // 2
            face_size = right - left

            move_x = frame_center_x - face_x
            move_y = frame_center_y - face_y
            move_z = 150 - face_size  

            # Apply dead zone: Only move if outside the dead zone
            move_x = 0 if abs(move_x) <= dead_zone else int(np.clip(move_x * 0.1, -speed, speed))
            move_y = 0 if abs(move_y) <= dead_zone else int(np.clip(move_y * 0.1, -speed, speed))
            move_z = 0 if abs(move_z) <= 20 else int(np.clip(move_z * 0.1, -speed, speed))

            # Move drone smoothly
            tello.send_rc_control(-move_x, 0, -move_y, 0)

            # ✅ Draw tracking box
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, "Bhavesh", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # ✅ If face lost, hover in place
    if not recognized:
        tello.send_rc_control(0, 0, 0, 0)

    # ✅ Show tracking video
    cv2.imshow("Tello Face Tracking", frame)

    # **Press 'q' to land the drone**
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 Stopping movement and landing...")
        tello.land()
        break

# **Cleanup**
tello.streamoff()
cv2.destroyAllWindows()