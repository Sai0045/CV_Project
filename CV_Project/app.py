# =============================
# Ghost Guard AI (Updated + Debug Visible)
# =============================

import os

# 1) Reduce noisy logs (set BEFORE importing mediapipe)
os.environ["GLOG_minloglevel"] = "3"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Some builds of mediapipe use absl logging too:
try:
    from absl import logging as absl_logging
    absl_logging.set_verbosity(absl_logging.ERROR)
    absl_logging.set_stderrthreshold("error")
except Exception:
    pass

import cv2
import mediapipe as mp
import threading
import time
import tkinter as tk
import pystray
from pystray import MenuItem as item
from PIL import Image

# =============================
# Global State
# =============================
THREAT_DETECTED = False
SYSTEM_ENABLED = True
LAST_FACE_SEEN = time.time()

UNLOCK_DELAY = 1.0
SHOW_PREVIEW = True   # ✅ keep true so you SEE it running

# =============================
# MediaPipe Setup
# =============================
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(
    max_num_faces=5,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# =============================
# Exit helper
# =============================
def hard_exit(code=0):
    try:
        cv2.destroyAllWindows()
    except:
        pass
    os._exit(code)

# =============================
# Vision Thread
# =============================
def vision_loop():
    global THREAT_DETECTED, LAST_FACE_SEEN, SYSTEM_ENABLED

    print("✅ Vision thread started...")

    # Try multiple camera indexes
    cap = None
    for idx in [0, 1, 2]:
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"✅ Camera opened on index {idx}")
            break
        cap.release()
        cap = None

    if cap is None:
        print("❌ Camera not opening (0/1/2). Close Zoom/Teams/Camera app and run again.")
        return

    LAST_FACE_SEEN = time.time()
    THREAT_DETECTED = False

    while True:
        if not SYSTEM_ENABLED:
            time.sleep(0.2)
            continue

        ret, frame = cap.read()
        if not ret:
            print("⚠️ Frame not captured. Retrying...")
            time.sleep(0.1)
            continue

        if SHOW_PREVIEW:
            cv2.imshow("GhostGuard Camera (Press Q to Exit)", frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
                break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        now = time.time()

        if results.multi_face_landmarks:
            face_count = len(results.multi_face_landmarks)

            if face_count > 1:
                THREAT_DETECTED = True
                LAST_FACE_SEEN = now
            else:
                if now - LAST_FACE_SEEN > UNLOCK_DELAY:
                    THREAT_DETECTED = False
        else:
            if now - LAST_FACE_SEEN > UNLOCK_DELAY:
                THREAT_DETECTED = False

    cap.release()
    cv2.destroyAllWindows()
    hard_exit(0)

# =============================
# Overlay
# =============================
class Overlay:
    def __init__(self):
        print("✅ Overlay started...")
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")
        self.root.overrideredirect(True)

        # 🔥 show slight overlay for 1 second so you know it started
        self.root.attributes("-alpha", 0.15)
        self.root.after(1000, lambda: self.root.attributes("-alpha", 0.0))

        self.root.bind("<Escape>", self.exit_now)
        self.update_overlay()
        self.root.mainloop()

    def exit_now(self, event=None):
        hard_exit(0)

    def update_overlay(self):
        if THREAT_DETECTED and SYSTEM_ENABLED:
            self.root.attributes("-alpha", 1.0)
        else:
            self.root.attributes("-alpha", 0.0)
        self.root.after(30, self.update_overlay)

# =============================
# Tray
# =============================
def toggle(icon, item_):
    global SYSTEM_ENABLED
    SYSTEM_ENABLED = not SYSTEM_ENABLED
    print("🔁 SYSTEM_ENABLED =", SYSTEM_ENABLED)

def quit_app(icon, item_):
    hard_exit(0)

def tray_loop():
    print("✅ Tray started...")
    icon = pystray.Icon(
        "Ghost-Guard AI",
        Image.new("RGB", (64, 64), "black"),
        menu=pystray.Menu(
            item("Enable / Disable", toggle),
            item("Exit", quit_app)
        )
    )
    icon.run()

# =============================
# Main
# =============================
if __name__ == "__main__":
    print("✅ Ghost Guard AI starting... (Press ESC to exit overlay, Q to exit preview)")
    threading.Thread(target=vision_loop, daemon=True).start()
    threading.Thread(target=tray_loop, daemon=True).start()
    Overlay()
