import cv2
import os
import time
from datetime import datetime
import pyttsx3
import playsound
import threading
import json

# === Configurable Parameters ===
CONFIDENCE_THRESHOLD = 0.6  # Set your threshold for triggering alerts
ALERT_LABEL_PREFIX = "no_"  # Violation label prefix (e.g., no_helmet, no_vest)
ALERT_SOUND_PATH = "alarm.mp3"  # Replace with your alert sound file
SAVE_DIR = "violations"  # Directory to store violation snapshots

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

    # 📝 You can edit metadata as per your project need
    metadata = {
        "timestamp": timestamp,
        "location": location,
        "file": filename
    }
    with open(f"{filename}.json", "w") as f:
        json.dump(metadata, f, indent=2)

def trigger_alert(label, confidence, frame, location):
    save_snapshot(frame, location)

    # 🚨 You can connect this print with your web frontend (via Flask, socket, etc.)
    print(f"[ALERT] Violation: {label} | Confidence: {confidence:.2f}")

    # 🔊 Make sure alert.mp3 exists or replace with your own path
    threading.Thread(target=play_alert_sound).start()

    # 🗣️ You can customize spoken alert message format if needed
    alert_text = f"Warning! {label.replace('_', ' ')} detected."
    threading.Thread(target=speak_alert, args=(alert_text,)).start()

    # 📤 OPTIONAL: Uncomment and implement if using WhatsApp/Email/Twilio APIs
    # send_api_alert(label, confidence, location)

def check_violations(detections, frame, location="Zone 1"):
    """
    detections = list of dictionaries:
    Example: [{'label': 'no_helmet', 'confidence': 0.78}, ...]
    """
    for det in detections:
        label = det['label']
        confidence = det['confidence']
        if label.startswith(ALERT_LABEL_PREFIX) and confidence >= CONFIDENCE_THRESHOLD:
            trigger_alert(label, confidence, frame, location)
