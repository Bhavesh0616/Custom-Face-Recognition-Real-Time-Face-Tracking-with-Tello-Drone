# Custom-Face-Recognition-Real-Time-Face-Tracking-with-Tello-Drone

This project enables **custom face recognition** and **real-time face tracking** using a **DJI Tello drone**, powered by `face_recognition`, `OpenCV`, and `djitellopy`. It combines computer vision with aerial robotics to create an intelligent drone that can recognize a specific person and follow them smoothly in real-time.

---

## 📸 Project Highlights

✅ Collect and store face encodings of any individual  
✅ Recognize known faces through webcam or drone camera  
✅ Automatically take off when a known face is detected  
✅ Real-time tracking and dynamic hovering based on facial position  
✅ Press `q` anytime to stop or land the drone safely

---

## 🗂️ Folder Structure

├── detect.py # Capture & encode face samples from webcam
├── recognize.py # Recognize known faces using webcam
├── tello.py # Drone logic: recognition + tracking + flight 
└── face_database/ 
    └── Bhavesh.npy # Saved numpy face encoding (auto-generated)


---

## 🧠 How It Works

### `detect.py` - Face Capture & Encoding
- Prompts user to enter their name
- Collects 10 clear face samples from webcam
- Computes and averages encodings using `face_recognition`
- Saves encoding to `face_database/<name>.npy`

### `recognize.py` - Webcam Face Recognition
- Loads all encodings from `face_database/`
- Matches detected faces in real-time from webcam
- Displays name labels for known faces or "Unknown" otherwise

### `tello.py` - Drone-Based Recognition & Tracking
- Loads a specific person’s face encoding
- Connects and streams live video from DJI Tello
- Waits for a successful face match
- Takes off, then actively tracks the face using RC control
- Adjusts drone position based on facial location and size
- Lands on command (`q` key)

---

## 🚀 Getting Started

### 🔧 Requirements
Install all dependencies:
```bash
pip install opencv-python face_recognition numpy djitellopy
```

Make sure:

You have a DJI Tello connected via Wi-Fi

You’ve created at least one face encoding using detect.py


▶️ How to Run
1. Collect Face Encoding
```bash
python detect.py
```
2. Test with Webcam
```bash
recognize.py
```
3. Start Drone Tracking
```bash
tello.py
```
The drone will:

Detect your face
Automatically take off
Follow and hover based on your face position

🎯 Face Tracking Mechanics
Calculates position difference between face and frame center

Applies a dead zone to avoid jitter

Adjusts X (left/right), Y (up/down), and Z (forward/backward) axes

Smooth control via send_rc_control()

📌 Notes
Tracking is tuned for stability using dead_zone and speed parameters.

Make sure you're the only visible face during detection for best results.

Always test in a safe environment (indoor preferred) to avoid collisions.

👨‍💻 Developer Notes
Developed using face_recognition

Drone controlled via djitellopy

Tested on Windows with Tello EDU

🛡️ License
MIT License - Feel free to modify, use, or contribute!

📽️ Demo
![Gesture Control Demo](./test.gif)
