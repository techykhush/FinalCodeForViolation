import cv2
import os
from datetime import datetime
import pyttsx3
import playsound
import threading
import json

# === Configurations ===
CONFIDENCE_THRESHOLD = 0.6
ALERT_LABEL_PREFIX = "no_"
ALERT_SOUND_PATH = "alert.mp3"
SAVE_DIR = "violations"

os.makedirs(SAVE_DIR, exist_ok=True)

# === Text-to-Speech Setup ===
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 150)

def play_alert_sound():
    playsound.playsound(ALERT_SOUND_PATH)

def speak_alert(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def save_snapshot(frame, location):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{SAVE_DIR}/violation_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    metadata = {
        "timestamp": timestamp,
        "location": location,
        "file": filename
    }
    with open(f"{filename}.json", "w") as f:
        json.dump(metadata, f, indent=2)

def trigger_alert(label, confidence, frame, location):
    save_snapshot(frame, location)
    print(f"[ALERT] Violation: {label} | Confidence: {confidence:.2f}")
    threading.Thread(target=play_alert_sound).start()
    alert_text = f"Warning! {label.replace('_', ' ')} detected."
    threading.Thread(target=speak_alert, args=(alert_text,)).start()
    # Optional: send_api_alert(label, confidence, location)

def check_manual_input(label, confidence, frame, location="Zone 1"):
    if label.startswith(ALERT_LABEL_PREFIX) and confidence >= CONFIDENCE_THRESHOLD:
        trigger_alert(label, confidence, frame, location)
    else:
        print(f"[INFO] No violation or below threshold (Label: {label}, Confidence: {confidence})")

# === MAIN: Provide Manual Input Here ===
# 🔧 Replace this with your actual test image
frame = cv2.imread("test_image.jpg")  # Ensure this image exists

# 🔽 === USER INPUT (Simulating Model Output) === 🔽
label_input = input("Enter label (e.g., no_helmet): ")
confidence_input = float(input("Enter confidence score (e.g., 0.85): "))

check_manual_input(label_input.strip(), confidence_input, frame)
