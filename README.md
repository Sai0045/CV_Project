# 👻 Ghost Guard AI

### Real-Time Face Monitoring & Privacy Protection System

---

## 📌 Overview

Ghost Guard AI is a real-time computer vision-based security system that monitors the number of faces in front of a screen using a webcam.

If more than one face is detected, the system automatically triggers a full-screen black overlay to protect sensitive information, ensuring user privacy.

The application runs continuously in the background with a system tray interface and live camera preview.

---

## 🚀 Key Features

* 🎥 Real-time face detection using webcam
* 👥 Detects multiple faces simultaneously
* 🔒 Privacy protection via full-screen overlay
* ⚡ Automatic threat detection and response
* 🖥️ Live camera preview window
* 🧵 Multi-threaded execution (vision + tray + UI)
* 🖱️ System tray controls (Enable/Disable & Exit)

---

## 🏗️ System Workflow

```
Webcam Input
     ↓
Face Detection (MediaPipe Face Mesh)
     ↓
Face Count Analysis
     ↓
If Multiple Faces Detected → Trigger Threat
     ↓
Fullscreen Black Overlay Activated
```

---

## 📂 Project Structure

```
GhostGuard_AI/
│
├── main.py   # Complete application (vision + overlay + tray system)
└── README.md
```

---

## 🛠️ Technologies Used

* **Python** 🐍
* **OpenCV (cv2)** – Camera handling and image processing
* **MediaPipe** – Face detection (Face Mesh)
* **Tkinter** – Fullscreen overlay UI
* **PyStray** – System tray integration
* **Pillow (PIL)** – Tray icon handling
* **Threading** – Parallel execution

---

## ⚙️ Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/Sai0045/CV_Project.git
cd CV_Project
```

### Step 2: Install Dependencies

```bash
pip install opencv-python mediapipe pystray pillow
```

---

## ▶️ How to Run

```bash
python main.py
```

---

## 🎮 Controls

* Press **Q** → Exit camera preview
* Press **ESC** → Exit overlay
* Use **System Tray Menu**:

  * Enable / Disable system
  * Exit application

---

## ⚠️ How It Works

* The system continuously reads frames from the webcam
* Detects faces using MediaPipe Face Mesh
* If more than one face is detected →
  👉 `THREAT_DETECTED = True`
* A full-screen black overlay appears to block the screen

---

## 🎯 Use Cases

* Privacy protection in public environments
* Prevent shoulder surfing
* Secure workspaces
* Exam monitoring systems
* Confidential data protection

---

## 📈 Future Enhancements

* Face recognition (authorized vs unauthorized users)
* Alert notification system
* Screenshot logging on threat detection
* Mobile/remote monitoring integration
* GUI dashboard

---

## 👨‍💻 Author

**Sairaj Abhale**
AI & ML Student | Computer Vision Enthusiast

---

## 📜 License

This project is open-source and available for educational use.
