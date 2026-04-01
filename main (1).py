'''

                            Online Python Compiler.
                Code, Compile, Run and Debug python program online.
Write your code in this editor and press "Run" button to execute it.

'''

#!/usr/bin/env python3
# ============================================================
# ShHEild - Women Safety App
# FILE: main.py  ← RUN THIS FILE TO START THE APP
#
# ██████████████████████████████████████████████
#  ██████  ██   ██ ██   ██ ███████ ██ ██      ██
#  ██      ██   ██ ██   ██ ██      ██ ██      ██
#  ███████ ███████ ███████ █████   ██ ██      ██
#       ██ ██   ██ ██   ██ ██      ██ ██      ██
#  ██████  ██   ██ ██   ██ ███████ ██ ███████ ██
# ██████████████████████████████████████████████
#          Your Invisible Guardian 💜
#
# HOW TO RUN:
#   1. Open terminal in the shheild/ folder
#   2. Type: python main.py
#   3. The app window will open!
#
# REQUIREMENTS:
#   - Python 3.8 or newer
#   - No extra libraries needed! (only built-in Python)
#
# FOLDER STRUCTURE:
#   shheild/
#   ├── main.py          ← Run this!
#   ├── ai_engine.py     ← AI that detects danger
#   ├── watch_sensor.py  ← Simulates smartwatch
#   ├── alert_system.py  ← Sends alerts, controls siren
#   ├── app_controller.py← Main coordinator
#   ├── dashboard.py     ← Beautiful UI
#   ├── data/            ← Contacts & backups saved here
#   ├── recordings/      ← Audio/video evidence saved here
#   └── logs/            ← Alert logs saved here
# ============================================================

import sys
import os

# Add current folder to Python path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from app_controller import AppController
from dashboard      import ShHEildDashboard


def main():
    """
    Main function - entry point of the app.
    
    1. Creates the AppController (brain)
    2. Creates the Dashboard (face/UI)
    3. Starts monitoring
    4. Shows the window
    """
    
    print("\n" + "═" * 55)
    print("  🛡️  ShHEild - Women Safety App")
    print("  💜  Your Invisible Guardian")
    print("═" * 55)
    print("  Starting up...\n")
    
    # Step 1: Create the app controller (brain of the app)
    controller = AppController()
    
    # Step 2: Create the beautiful dashboard UI
    dashboard = ShHEildDashboard(controller)
    
    # Step 3: Start monitoring (watch + AI run in background)
    controller.start()
    
    print("\n  ✅ ShHEild is running!")
    print("  💜 Go to 🎮 Simulate tab to test different scenarios")
    print("  🚨 Set scenario to DANGER to see the full alert flow")
    print("  💜 Press 'I'm Safe' button to cancel any alert")
    print("═" * 55 + "\n")
    
    # Step 4: Show the window (this blocks until window is closed)
    dashboard.run()
    
    print("\n  👋 ShHEild closed. Stay safe! 💜\n")


# ── THIS IS WHERE PYTHON STARTS RUNNING ──
# Only run main() if this file is run directly
# (not when it's imported by another file)
if __name__ == "__main__":
    main() 
# ============================================================
# ShHEild - Smartwatch Simulator
# FILE: watch_sensor.py
#
# In real app: This would connect to your smartwatch via
# Bluetooth or API (Apple Watch, Fitbit, Samsung Galaxy Watch)
#
# For learning/testing: This SIMULATES realistic heart rate
# data so you can test the app without a real watch.
#
# It can simulate 4 scenarios:
#   1. NORMAL   - Just sitting/resting
#   2. EXERCISE - Running, gym workout
#   3. STRESS   - Mildly stressful situation
#   4. DANGER   - Actual threatening situation
# ============================================================

import random      # For adding realistic "noise" to readings
import time        # For timing between readings
import threading   # For reading data in background


class WatchSensor:
    """
    Simulates a smartwatch heart rate sensor.
    
    In production, you'd replace _read_from_watch() with
    actual Bluetooth code to connect to your wearable.
    """
    
    def __init__(self):
        # Current heart rate (beats per minute)
        self.heart_rate = 72
        
        # Which scenario are we simulating?
        # Options: "normal", "exercise", "stress", "danger"
        self.scenario = "normal"
        
        # Is the watch connected? (simulated)
        self.connected = True
        
        # Battery level (simulated, 0-100%)
        self.battery = 85
        
        # Callback function - called every time we get a new reading
        # (The main app will set this)
        self.on_new_reading = None
        
        # Is the sensor running?
        self._running = False
        
        # Background thread for continuous readings
        self._thread = None
        
        print("⌚ Watch sensor initialized!")
    
    
    def start(self):
        """Start reading heart rate data in the background."""
        self._running = True
        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()
        print("⌚ Watch sensor started - reading every 2 seconds")
    
    
    def stop(self):
        """Stop the sensor."""
        self._running = False
        print("⌚ Watch sensor stopped")
    
    
    def set_scenario(self, scenario):
        """
        Change what scenario is being simulated.
        
        Args:
            scenario (str): "normal", "exercise", "stress", or "danger"
        """
        valid = ["normal", "exercise", "stress", "danger"]
        if scenario in valid:
            self.scenario = scenario
            print(f"⌚ Scenario changed to: {scenario.upper()}")
        else:
            print(f"⚠️ Unknown scenario: {scenario}. Use: {valid}")
    
    
    def _read_loop(self):
        """
        Runs in background, continuously generating heart rate readings.
        Calls the callback function (on_new_reading) with each new value.
        """
        while self._running:
            # Get a new simulated heart rate reading
            hr = self._simulate_heart_rate()
            self.heart_rate = hr
            
            # If someone registered a callback, call it!
            if self.on_new_reading:
                self.on_new_reading(hr)
            
            # Wait 2 seconds before next reading
            # (Real smartwatches update every 1-5 seconds)
            time.sleep(2)
    
    
    def _simulate_heart_rate(self):
        """
        Generates a realistic-looking heart rate based on scenario.
        
        Adds small random "noise" to make it look like a real sensor
        (real heart rate readings always fluctuate a little).
        
        Returns:
            int: Simulated heart rate in BPM
        """
        # Small random variation (±3 BPM) to seem realistic
        noise = random.randint(-3, 3)
        
        if self.scenario == "normal":
            # Normal resting: 65-80 BPM
            target = 72
            # Slowly drift toward target
            self.heart_rate = self._drift_toward(self.heart_rate, target, speed=2)
        
        elif self.scenario == "exercise":
            # Exercise: 130-160 BPM, rises gradually
            target = random.randint(130, 160)
            # Gradual rise (exercise feels like slow climb)
            self.heart_rate = self._drift_toward(self.heart_rate, target, speed=3)
        
        elif self.scenario == "stress":
            # Stress/anxiety: 90-110 BPM, slightly elevated
            target = random.randint(90, 115)
            self.heart_rate = self._drift_toward(self.heart_rate, target, speed=4)
        
        elif self.scenario == "danger":
            # DANGER: Sudden adrenaline spike! 
            # Heart jumps to 140-180 BPM very quickly
            target = random.randint(145, 175)
            # Fast jump (adrenaline hits like a wave!)
            self.heart_rate = self._drift_toward(self.heart_rate, target, speed=25)
        
        # Add realistic noise and keep within human limits (40-220)
        result = int(self.heart_rate + noise)
        result = max(40, min(220, result))
        
        return result
    
    
    def _drift_toward(self, current, target, speed):
        """
        Smoothly moves current value toward target value.
        
        Speed controls how fast it moves:
        - speed=2  → very slow (resting/exercise)
        - speed=25 → very fast (danger/adrenaline!)
        
        Args:
            current (float): Current heart rate
            target  (float): Where we want to go
            speed   (float): How fast to move there
            
        Returns:
            float: New heart rate value, closer to target
        """
        diff = target - current
        
        if abs(diff) < speed:
            return target  # Close enough, just jump there
        elif diff > 0:
            return current + speed   # Move up
        else:
            return current - speed   # Move down
    
    
    def get_current_reading(self):
        """
        Get the latest heart rate reading right now.
        
        Returns:
            dict: Heart rate data with all sensor info
        """
        return {
            "heart_rate": self.heart_rate,
            "connected":  self.connected,
            "battery":    self.battery,
            "scenario":   self.scenario
        }


# ──────────────────────────────────────────────
# HOW TO CONNECT A REAL SMARTWATCH (for future!)
# ──────────────────────────────────────────────
# 
# For Apple Watch (uses HealthKit through iPhone):
#   pip install pyhealth
#
# For Fitbit:
#   pip install fitbit
#   # Uses Fitbit Web API with OAuth login
#
# For Samsung Galaxy Watch (Bluetooth):
#   pip install bleak
#   # Connect via BLE (Bluetooth Low Energy)
#
# For a real Bluetooth HR monitor:
#   import bleak
#   async def read_hr():
#       async with BleakClient(device_address) as client:
#           hr = await client.read_gatt_char(HR_CHARACTERISTIC_UUID)
#           return int(hr[1])  # HR is at index 1 in BLE HR data
# ──────────────────────────────────────────────
# ============================================================
# ShHEild - Alert & Safety System
# FILE: alert_system.py
#
# This handles everything that happens WHEN danger is detected:
#   ✅ Get current location (GPS)
#   ✅ Send SMS/WhatsApp to emergency contacts
#   ✅ Send alert to police
#   ✅ Start recording audio + video
#   ✅ Sound the siren
#   ✅ Upload everything to cloud storage
#
# For this demo, everything is SIMULATED with print messages.
# In production, you'd use real APIs (Twilio, Google Maps, etc.)
# ============================================================

import os
import json
import time
import threading
import random
from datetime import datetime


class AlertSystem:
    """
    Handles all safety alerts and emergency responses.
    
    Think of this as the action arm of ShHEild -
    the AI Engine detects danger, this system ACTS on it.
    """
    
    def __init__(self, contacts_file="data/contacts.json"):
        # Path where contacts are saved
        self.contacts_file = contacts_file
        
        # Load emergency contacts from file
        self.contacts = self._load_contacts()
        
        # Is the siren currently on?
        self.siren_active = False
        
        # Is recording currently on?
        self.recording_active = False
        
        # Current simulated location
        self.location = {
            "lat":     28.6139,    # Default: New Delhi
            "lng":     77.2090,
            "address": "Bulandshahr, Uttar Pradesh, India"
        }
        
        # Log file for all alerts
        self.log_file = "logs/alerts.log"
        os.makedirs("logs", exist_ok=True)
        
        print("🔔 Alert system ready!")
    
    
    # ════════════════════════════════════════
    #   LOCATION
    # ════════════════════════════════════════
    
    def get_location(self):
        """
        Gets the current GPS location.
        
        In production: Use device GPS or IP geolocation API.
        Right now: Returns simulated location with small random drift.
        
        Returns:
            dict: Location with lat, lng, and readable address
        """
        # Simulate small GPS movement (like walking)
        self.location["lat"] += random.uniform(-0.0001, 0.0001)
        self.location["lng"] += random.uniform(-0.0001, 0.0001)
        
        # Google Maps link anyone can click to see exactly where you are
        maps_link = (
            f"https://maps.google.com/?q="
            f"{self.location['lat']},{self.location['lng']}"
        )
        
        return {
            "lat":      round(self.location["lat"], 6),
            "lng":      round(self.location["lng"], 6),
            "address":  self.location["address"],
            "maps_url": maps_link
        }
    
    
    # ════════════════════════════════════════
    #   SIREN
    # ════════════════════════════════════════
    
    def start_siren(self):
        """
        Activates the loud siren sound.
        
        In production: Use pygame or playsound to play a loud alarm.
        Right now: Prints a simulation message.
        """
        if not self.siren_active:
            self.siren_active = True
            print("🚨 SIREN ACTIVATED - LOUD ALARM SOUNDING!")
            
            # Log this event
            self._log("SIREN_START", "Loud siren activated")
            
            # In real app, you'd do:
            # import pygame
            # pygame.mixer.init()
            # pygame.mixer.music.load("assets/siren.mp3")
            # pygame.mixer.music.play(-1)  # -1 means loop forever
    
    
    def stop_siren(self):
        """Stop the siren."""
        if self.siren_active:
            self.siren_active = False
            print("🔇 Siren stopped")
            self._log("SIREN_STOP", "Siren deactivated")
            
            # In real app:
            # pygame.mixer.music.stop()
    
    
    # ════════════════════════════════════════
    #   EMERGENCY CONTACTS
    # ════════════════════════════════════════
    
    def send_alert_to_contacts(self, heart_rate, danger_score):
        """
        Sends emergency SMS/WhatsApp to all saved contacts.
        
        In production: Use Twilio API to send real SMS.
        Right now: Simulates sending and shows what message would be sent.
        
        Args:
            heart_rate   (int): Current heart rate
            danger_score (float): AI danger score (0-100)
        """
        location = self.get_location()
        timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
        
        # Compose the alert message
        message = (
            f"🚨 SHHEILD EMERGENCY ALERT 🚨\n\n"
            f"⚠️ {self._get_contact_name()} may be in DANGER!\n\n"
            f"📍 Location: {location['address']}\n"
            f"🗺️ Live Map: {location['maps_url']}\n\n"
            f"💓 Heart Rate: {heart_rate} BPM\n"
            f"⚡ Danger Level: {danger_score:.0f}/100\n\n"
            f"🕐 Time: {timestamp}\n\n"
            f"Please check on her immediately or call 112!\n"
            f"— ShHEild Safety App"
        )
        
        print("\n" + "═" * 50)
        print("📱 SENDING EMERGENCY ALERTS TO CONTACTS...")
        print("═" * 50)
        
        if not self.contacts:
            print("⚠️ No contacts saved! Please add emergency contacts.")
            return
        
        for contact in self.contacts:
            print(f"\n📤 Sending to: {contact['name']} ({contact['phone']})")
            # Simulate small delay (real SMS takes a moment)
            time.sleep(0.3)
            print(f"   ✅ Alert sent successfully!")
            print(f"   Message preview:\n   {message[:100]}...")
        
        print("\n" + "═" * 50)
        self._log("ALERT_SENT", f"Alerts sent to {len(self.contacts)} contacts")
        
        # ── HOW TO USE REAL TWILIO SMS IN PRODUCTION ──
        # pip install twilio
        #
        # from twilio.rest import Client
        # client = Client(TWILIO_SID, TWILIO_TOKEN)
        # for contact in self.contacts:
        #     client.messages.create(
        #         body=message,
        #         from_="+1234567890",   # Your Twilio number
        #         to=contact["phone"]
        #     )
    
    
    def send_sos_to_police(self, heart_rate):
        """
        Sends SOS alert to emergency services (Police - 112).
        
        This is only called AFTER the user DOESN'T press "I'm Safe"
        within the confirmation window.
        
        In production: Integrate with local emergency dispatch API
        or auto-dial 112 with location details.
        """
        location = self.get_location()
        timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
        
        sos_message = (
            f"🆘 SOS EMERGENCY - ShHEild Women Safety App\n\n"
            f"Woman in distress! Immediate assistance needed.\n\n"
            f"📍 Location: {location['address']}\n"
            f"🗺️ Coordinates: {location['lat']}, {location['lng']}\n"
            f"🗺️ Map: {location['maps_url']}\n\n"
            f"💓 Abnormal Heart Rate: {heart_rate} BPM\n"
            f"🕐 Alert Time: {timestamp}\n\n"
            f"AI Danger Detection Score: HIGH\n"
            f"Please dispatch assistance immediately."
        )
        
        print("\n🆘 SENDING SOS TO EMERGENCY SERVICES (112)...")
        print(f"📍 Location shared: {location['maps_url']}")
        print("✅ SOS transmitted to local police station!")
        
        self._log("SOS_POLICE", f"SOS sent to police. Location: {location['address']}")
    
    
    # ════════════════════════════════════════
    #   RECORDING
    # ════════════════════════════════════════
    
    def start_recording(self):
        """
        Starts recording audio and video as evidence.
        
        In production:
        - Audio: Use pyaudio or sounddevice library
        - Video: Use OpenCV (cv2) to record from camera
        
        Files are saved with timestamp so you always know when it happened.
        """
        if not self.recording_active:
            self.recording_active = True
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create filenames for this recording session
            audio_file = f"recordings/audio_{timestamp}.wav"
            video_file = f"recordings/video_{timestamp}.mp4"
            
            os.makedirs("recordings", exist_ok=True)
            
            print(f"\n🎙️ RECORDING STARTED!")
            print(f"   Audio → {audio_file}")
            print(f"   Video → {video_file}")
            print(f"   (Recording silently in background as evidence)")
            
            self._log("RECORDING_START", f"Recording to {audio_file}, {video_file}")
            
            # ── REAL RECORDING CODE (for production) ──
            # Audio with pyaudio:
            # import pyaudio, wave
            # pa = pyaudio.PyAudio()
            # stream = pa.open(format=pyaudio.paInt16, channels=1,
            #                  rate=44100, input=True, frames_per_buffer=1024)
            #
            # Video with OpenCV:
            # import cv2
            # cap = cv2.VideoCapture(0)  # 0 = front camera
            # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            # out = cv2.VideoWriter(video_file, fourcc, 20.0, (640,480))
    
    
    def stop_recording(self):
        """Stop all recordings."""
        if self.recording_active:
            self.recording_active = False
            print("⏹️ Recording stopped and saved to recordings/")
            self._log("RECORDING_STOP", "Recording stopped")
    
    
    # ════════════════════════════════════════
    #   CLOUD STORAGE
    # ════════════════════════════════════════
    
    def upload_to_cloud(self, data):
        """
        Uploads evidence and alert data to cloud storage.
        
        In production: Use Firebase, AWS S3, or Google Drive API.
        Right now: Saves to local JSON file (simulated cloud).
        
        Args:
            data (dict): Data to upload
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cloud_file = f"data/cloud_backup_{timestamp}.json"
        
        os.makedirs("data", exist_ok=True)
        
        # Add metadata
        data["upload_time"] = datetime.now().isoformat()
        data["app_version"] = "ShHEild v1.0"
        
        # Save to file (simulating cloud upload)
        with open(cloud_file, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"☁️ Data backed up to cloud: {cloud_file}")
        
        # ── REAL FIREBASE UPLOAD (for production) ──
        # pip install firebase-admin
        #
        # import firebase_admin
        # from firebase_admin import credentials, firestore
        # cred = credentials.Certificate("serviceAccountKey.json")
        # firebase_admin.initialize_app(cred)
        # db = firestore.client()
        # db.collection("incidents").add(data)
    
    
    # ════════════════════════════════════════
    #   CONTACTS MANAGEMENT
    # ════════════════════════════════════════
    
    def save_contact(self, name, phone, relation):
        """
        Save a new emergency contact.
        
        Args:
            name     (str): Contact's name (e.g., "Mom")
            phone    (str): Phone number with country code
            relation (str): Relationship (e.g., "Mother", "Friend")
        """
        contact = {
            "name":     name,
            "phone":    phone,
            "relation": relation,
            "added":    datetime.now().isoformat()
        }
        
        self.contacts.append(contact)
        self._save_contacts()
        print(f"✅ Contact saved: {name} ({phone})")
    
    
    def remove_contact(self, index):
        """Remove a contact by its list index."""
        if 0 <= index < len(self.contacts):
            removed = self.contacts.pop(index)
            self._save_contacts()
            print(f"🗑️ Removed contact: {removed['name']}")
    
    
    def _load_contacts(self):
        """Load contacts from file. Returns empty list if no file."""
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.contacts_file):
            try:
                with open(self.contacts_file, "r") as f:
                    return json.load(f)
            except:
                pass
        # Default sample contacts for first run
        return [
            {"name": "Mom", "phone": "+91-9876543210", "relation": "Mother"},
            {"name": "Dad", "phone": "+91-9876543211", "relation": "Father"}
        ]
    
    
    def _save_contacts(self):
        """Save contacts list to file."""
        os.makedirs("data", exist_ok=True)
        with open(self.contacts_file, "w") as f:
            json.dump(self.contacts, f, indent=2)
    
    
    def _get_contact_name(self):
        """Get user's name (could be stored in settings)."""
        return "The ShHEild User"
    
    
    def _log(self, event_type, message):
        """Write a log entry to the log file."""
        timestamp = datetime.now().isoformat()
        entry = f"[{timestamp}] {event_type}: {message}\n"
        
        with open(self.log_file, "a") as f:
            f.write(entry)
            # ============================================================
# ShHEild - Main App Controller
# FILE: app_controller.py
#
# This is the MAIN BRAIN that connects everything together.
# Think of it as the manager:
#   - It talks to the watch sensor
#   - Sends readings to the AI engine
#   - If AI says danger → tells alert system to act
#   - Updates the dashboard (UI)
#
# This runs as a background service while the UI shows on screen.
# ============================================================

import time
import threading
from datetime import datetime

# Import our other modules
from watch_sensor  import WatchSensor
from ai_engine     import AIEngine
from alert_system  import AlertSystem


# ── HOW LONG TO WAIT (in seconds) before each stage ──
# When danger is detected:
#   1. Siren starts immediately
#   2. Wait 15 seconds → if user doesn't press "I'm Safe" → alert contacts
#   3. Wait 30 more seconds → if still no response → call police
SIREN_DELAY    = 0      # Siren starts right away
CONTACT_DELAY  = 15     # Seconds to wait before alerting contacts
POLICE_DELAY   = 30     # Seconds after contacts before alerting police


class AppController:
    """
    Central coordinator for the entire ShHEild app.
    
    It runs continuously in the background, monitoring the watch,
    feeding data to AI, and triggering alerts when needed.
    """
    
    def __init__(self):
        # Create all the component objects
        self.sensor  = WatchSensor()   # Reads heart rate
        self.ai      = AIEngine()      # Analyzes heart rate
        self.alerts  = AlertSystem()   # Sends alerts/recordings
        
        # ── STATE VARIABLES ──
        self.is_running       = False    # Is app running?
        self.danger_confirmed = False    # Has AI confirmed real danger?
        self.user_is_safe     = False    # Did user press "I'm Safe"?
        self.alert_timer      = None     # Timer for delayed alerts
        
        # Current status shown on dashboard
        self.status = {
            "heart_rate":   72,
            "context":      "SAFE",
            "danger_score": 0,
            "message":      "All systems ready 💜",
            "timestamp":    datetime.now().strftime("%H:%M:%S"),
            "siren":        False,
            "recording":    False,
            "contacts":     self.alerts.contacts,
            "watch_battery": 85,
            "scenario":     "normal"     # For demo controls
        }
        
        # Callback to update the UI (set by main.py)
        self.on_status_update = None
        
        # Wire up the sensor to AI analysis
        self.sensor.on_new_reading = self._on_heart_rate_reading
        
        print("🛡️ ShHEild App Controller initialized!")
    
    
    def start(self):
        """Start the app - begin monitoring."""
        self.is_running = True
        self.sensor.start()
        print("🛡️ ShHEild is now ACTIVE and monitoring!")
    
    
    def stop(self):
        """Stop the app."""
        self.is_running = False
        self.sensor.stop()
        print("🛡️ ShHEild stopped.")
    
    
    def press_im_safe(self):
        """
        Called when user presses the big "I'm Safe" button.
        
        This cancels all pending alerts, stops siren and recording,
        and resets everything back to normal monitoring.
        """
        print("\n💜 'I'M SAFE' pressed by user - cancelling all alerts!")
        
        self.user_is_safe     = True
        self.danger_confirmed = False
        
        # Cancel any pending alert timers
        if self.alert_timer:
            self.alert_timer.cancel()
            self.alert_timer = None
        
        # Stop siren and recording
        self.alerts.stop_siren()
        self.alerts.stop_recording()
        
        # Reset AI engine
        self.ai.reset_alert()
        
        # Update status
        self._update_status({
            "context":      "SAFE",
            "danger_score": 0,
            "message":      "✅ User confirmed safe - monitoring resumed",
            "siren":        False,
            "recording":    False
        })
        
        # Reset the flag so next danger detection works
        time.sleep(2)
        self.user_is_safe = False
    
    
    def set_scenario(self, scenario):
        """
        Change the simulation scenario (for demo/testing).
        
        Args:
            scenario (str): "normal", "exercise", "stress", or "danger"
        """
        self.sensor.set_scenario(scenario)
        self.status["scenario"] = scenario
        
        # If switching back to normal/exercise, reset any danger state
        if scenario in ["normal", "exercise"]:
            self.ai.reset_alert()
            self.danger_confirmed = False
    
    
    def add_contact(self, name, phone, relation):
        """Add an emergency contact."""
        self.alerts.save_contact(name, phone, relation)
        # Update status so UI refreshes
        self.status["contacts"] = self.alerts.contacts
        if self.on_status_update:
            self.on_status_update(self.status.copy())
    
    
    def remove_contact(self, index):
        """Remove an emergency contact."""
        self.alerts.remove_contact(index)
        self.status["contacts"] = self.alerts.contacts
        if self.on_status_update:
            self.on_status_update(self.status.copy())
    
    
    # ══════════════════════════════════════════════
    #   PRIVATE METHODS (internal logic)
    # ══════════════════════════════════════════════
    
    def _on_heart_rate_reading(self, heart_rate):
        """
        Called automatically every time watch sends a new reading.
        
        This is the core loop:
        1. Get reading from watch
        2. Feed to AI
        3. Check AI result
        4. Act accordingly
        """
        # Feed reading to AI engine
        result = self.ai.add_reading(heart_rate)
        
        # Update the status dictionary (UI reads from this)
        self._update_status({
            "heart_rate":    heart_rate,
            "context":       result["context"],
            "danger_score":  result["danger_score"],
            "message":       result["message"],
            "timestamp":     result["timestamp"],
            "watch_battery": self.sensor.battery
        })
        
        # ── RESPOND TO DANGER ──
        if result["context"] == "DANGER" and not self.danger_confirmed:
            if not self.user_is_safe:
                self._handle_danger_detected(heart_rate, result["danger_score"])
    
    
    def _handle_danger_detected(self, heart_rate, danger_score):
        """
        The danger response sequence.
        
        Step 1 (immediate):     Start siren + recording
        Step 2 (15s later):     Alert emergency contacts
        Step 3 (45s later):     Alert police if still no "I'm Safe"
        """
        self.danger_confirmed = True
        
        print("\n🚨 " + "═" * 45)
        print("🚨  DANGER DETECTED BY AI ENGINE!")
        print(f"🚨  Heart Rate: {heart_rate} BPM")
        print(f"🚨  Danger Score: {danger_score:.0f}/100")
        print("🚨 " + "═" * 45)
        print("🚨  User has 15 seconds to press 'I'm Safe'")
        print("🚨  Otherwise emergency contacts will be alerted!")
        print("🚨 " + "═" * 45 + "\n")
        
        # ── STEP 1: Immediate response ──
        self.alerts.start_siren()
        self.alerts.start_recording()
        
        self._update_status({
            "context":   "DANGER",
            "message":   "🚨 DANGER! Press I'm Safe if you're okay!",
            "siren":     True,
            "recording": True
        })
        
        # ── STEP 2: Alert contacts after CONTACT_DELAY seconds ──
        # (unless user presses I'm Safe first)
        def alert_contacts():
            if not self.user_is_safe and self.danger_confirmed:
                print(f"\n⏰ {CONTACT_DELAY}s passed - no safe signal - alerting contacts!")
                self.alerts.send_alert_to_contacts(heart_rate, danger_score)
                
                # Also upload to cloud
                self.alerts.upload_to_cloud({
                    "event":        "DANGER_DETECTED",
                    "heart_rate":   heart_rate,
                    "danger_score": danger_score,
                    "location":     self.alerts.get_location()
                })
                
                # ── STEP 3: Alert police after another POLICE_DELAY seconds ──
                def alert_police():
                    if not self.user_is_safe and self.danger_confirmed:
                        print(f"\n⏰ {POLICE_DELAY}s passed - no response - calling police!")
                        self.alerts.send_sos_to_police(heart_rate)
                
                police_timer = threading.Timer(POLICE_DELAY, alert_police)
                police_timer.daemon = True
                police_timer.start()
        
        # Schedule the contact alert
        self.alert_timer = threading.Timer(CONTACT_DELAY, alert_contacts)
        self.alert_timer.daemon = True
        self.alert_timer.start()
    
    
    def _update_status(self, updates):
        """
        Update the status dictionary and notify UI.
        
        Args:
            updates (dict): Key-value pairs to update
        """
        self.status.update(updates)
        
        # If UI has registered a callback, call it with new status
        if self.on_status_update:
            self.on_status_update(self.status.copy())
            # ============================================================
# ShHEild - Beautiful Dashboard UI
# FILE: dashboard.py
#
# This creates the app's visual interface using Tkinter
# (Python's built-in GUI library - no extra install needed!)
#
# The UI has 4 sections (like tabs):
#   💜 Dashboard    - Heart rate display + status
#   👤 Contacts     - Add/remove emergency contacts
#   🎮 Simulate     - Test different scenarios
#   ⚙️  Settings    - App preferences
#
# Color palette: Soft lavender / light purple theme
#   Background:  #F5EEFF  (very light lavender)
#   Cards:       #FFFFFF  (white)
#   Purple:      #9D5CF6  (main purple)
#   Light Purple:#D8B4FE  (soft purple)
#   Pale Purple: #E6C3FF  (palest purple)
#   Dark Text:   #2D1B69  (deep purple for text)
#   Accent:      #7C3AED  (deeper accent)
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import time
import math
from datetime import datetime


# ── COLORS (Lavender / Light Purple Theme) ──
BG          = "#F5EEFF"    # Main background (lightest lavender)
CARD        = "#FFFFFF"    # Card background
CARD2       = "#FAF5FF"    # Slightly tinted card
PURPLE      = "#9D5CF6"    # Main purple
PURPLE_DARK = "#7C3AED"    # Deeper purple
PURPLE_LITE = "#D8B4FE"    # Soft purple
PURPLE_PALE = "#E6C3FF"    # Palest purple
PURPLE_MID  = "#C084FC"    # Mid purple
TEXT_DARK   = "#2D1B69"    # Deep purple for main text
TEXT_MED    = "#6B21A8"    # Medium purple for labels
TEXT_LIGHT  = "#A78BFA"    # Light purple for hints
GREEN       = "#22C55E"    # Safe green
YELLOW      = "#F59E0B"    # Warning amber
RED         = "#EF4444"    # Danger red
WHITE       = "#FFFFFF"


class ShHEildDashboard:
    """
    The main UI window for ShHEild.
    
    Built with Tkinter - Python's built-in GUI toolkit.
    No extra installation needed, works on any computer!
    """
    
    def __init__(self, controller):
        """
        Initialize the dashboard.
        
        Args:
            controller: AppController object (the brain of the app)
        """
        self.controller = controller
        
        # Latest status data from the controller
        self.status = {}
        
        # Animation variables
        self.pulse_angle   = 0      # For the animated heart ring
        self.pulse_growing = True   # Direction of pulse animation
        self.hr_history    = []     # For the mini heart rate graph
        
        # ── CREATE THE MAIN WINDOW ──
        self.root = tk.Tk()
        self.root.title("ShHEild 💜 Women Safety App")
        self.root.geometry("480x780")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        
        # Try to make the window look nice on different systems
        try:
            self.root.tk.call('tk', 'scaling', 1.2)
        except:
            pass
        
        # ── BUILD ALL UI SECTIONS ──
        self._build_header()
        self._build_tabs()
        self._build_dashboard_tab()
        self._build_contacts_tab()
        self._build_simulate_tab()
        self._build_settings_tab()
        
        # Show dashboard tab first
        self._show_tab("dashboard")
        
        # Register callback so controller sends us status updates
        self.controller.on_status_update = self._on_status_update
        
        # Start animation loop
        self._animate()
    
    
    # ════════════════════════════════════════
    #   BUILD HEADER
    # ════════════════════════════════════════
    
    def _build_header(self):
        """Creates the top purple header bar with logo."""
        
        header = tk.Frame(self.root, bg=PURPLE_DARK, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Shield emoji + app name
        tk.Label(
            header,
            text="🛡️  ShHEild",
            font=("Georgia", 22, "bold"),
            bg=PURPLE_DARK, fg=WHITE
        ).pack(side="left", padx=20, pady=15)
        
        # Tagline on the right
        tk.Label(
            header,
            text="Your Invisible Guardian",
            font=("Georgia", 9, "italic"),
            bg=PURPLE_DARK, fg=PURPLE_LITE
        ).pack(side="right", padx=20)
    
    
    # ════════════════════════════════════════
    #   BUILD TABS (navigation buttons)
    # ════════════════════════════════════════
    
    def _build_tabs(self):
        """Creates the 4 navigation buttons (like phone app tabs)."""
        
        self.tab_frame = tk.Frame(self.root, bg=PURPLE_PALE, height=50)
        self.tab_frame.pack(fill="x")
        self.tab_frame.pack_propagate(False)
        
        # Tab definitions: (display text, tab name)
        tabs = [
            ("💜 Home",    "dashboard"),
            ("👤 Contacts", "contacts"),
            ("🎮 Simulate", "simulate"),
            ("⚙️ Settings", "settings"),
        ]
        
        self.tab_buttons = {}
        
        for text, name in tabs:
            btn = tk.Button(
                self.tab_frame,
                text=text,
                font=("Georgia", 9),
                bg=PURPLE_PALE, fg=TEXT_MED,
                activebackground=PURPLE,
                activeforeground=WHITE,
                relief="flat", cursor="hand2",
                command=lambda n=name: self._show_tab(n)
            )
            btn.pack(side="left", expand=True, fill="both")
            self.tab_buttons[name] = btn
        
        # Content area where tab contents go
        self.content = tk.Frame(self.root, bg=BG)
        self.content.pack(fill="both", expand=True)
        
        # Dictionary to hold each tab's frame
        self.tabs = {}
    
    
    def _show_tab(self, name):
        """Show a specific tab, hide all others."""
        
        # Update button colors
        for tab_name, btn in self.tab_buttons.items():
            if tab_name == name:
                btn.config(bg=PURPLE, fg=WHITE, font=("Georgia", 9, "bold"))
            else:
                btn.config(bg=PURPLE_PALE, fg=TEXT_MED, font=("Georgia", 9))
        
        # Hide all tab frames, show the selected one
        for tab_name, frame in self.tabs.items():
            if tab_name == name:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()
    
    
    # ════════════════════════════════════════
    #   DASHBOARD TAB
    # ════════════════════════════════════════
    
    def _build_dashboard_tab(self):
        """Builds the main dashboard screen."""
        
        frame = tk.Frame(self.content, bg=BG)
        self.tabs["dashboard"] = frame
        
        # Scrollable content
        canvas = tk.Canvas(frame, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG)
        
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ── HEART RATE CARD ──
        hr_card = self._make_card(scroll_frame, padding=20)
        
        # Status label at top of card
        self.status_label = tk.Label(
            hr_card,
            text="💜  MONITORING ACTIVE",
            font=("Georgia", 10, "bold"),
            bg=CARD, fg=TEXT_LIGHT
        )
        self.status_label.pack(pady=(0, 10))
        
        # Canvas for the animated heart rate ring
        self.hr_canvas = tk.Canvas(
            hr_card,
            width=200, height=200,
            bg=CARD, highlightthickness=0
        )
        self.hr_canvas.pack()
        
        # Big heart rate number in center of ring
        self.hr_number = tk.Label(
            hr_card,
            text="72",
            font=("Georgia", 52, "bold"),
            bg=CARD, fg=PURPLE
        )
        self.hr_number.pack()
        
        # "BPM" label below the number
        tk.Label(
            hr_card,
            text="beats per minute",
            font=("Georgia", 10),
            bg=CARD, fg=TEXT_LIGHT
        ).pack(pady=(0, 5))
        
        # Status message (e.g., "All good 💜")
        self.context_label = tk.Label(
            hr_card,
            text="All good 💜",
            font=("Georgia", 11, "italic"),
            bg=CARD, fg=TEXT_MED
        )
        self.context_label.pack(pady=(5, 0))
        
        # Danger score bar
        self.danger_frame = tk.Frame(hr_card, bg=CARD)
        self.danger_frame.pack(fill="x", pady=(15, 5), padx=10)
        
        tk.Label(
            self.danger_frame, text="Danger Score:",
            font=("Georgia", 9), bg=CARD, fg=TEXT_LIGHT
        ).pack(side="left")
        
        self.danger_bar_frame = tk.Frame(self.danger_frame, bg=PURPLE_PALE, height=8)
        self.danger_bar_frame.pack(side="left", fill="x", expand=True, padx=10)
        
        self.danger_bar = tk.Frame(self.danger_bar_frame, bg=PURPLE_LITE, height=8)
        self.danger_bar.place(x=0, y=0, relheight=1, relwidth=0.0)
        
        self.danger_score_label = tk.Label(
            self.danger_frame, text="0",
            font=("Georgia", 9, "bold"), bg=CARD, fg=PURPLE
        )
        self.danger_score_label.pack(side="right")
        
        # Mini graph for heart rate history
        self.graph_canvas = tk.Canvas(
            hr_card,
            width=380, height=60,
            bg="#F8F0FF", highlightthickness=1,
            highlightbackground=PURPLE_PALE
        )
        self.graph_canvas.pack(pady=(10, 5), padx=10)
        
        tk.Label(
            hr_card, text="Heart rate history (last 20 readings)",
            font=("Georgia", 8), bg=CARD, fg=TEXT_LIGHT
        ).pack()
        
        # ── I'M SAFE BUTTON ──
        safe_card = self._make_card(scroll_frame, padding=20)
        
        tk.Label(
            safe_card,
            text="Press if you are safe & want to cancel alert",
            font=("Georgia", 9, "italic"),
            bg=CARD, fg=TEXT_LIGHT
        ).pack(pady=(0, 10))
        
        self.safe_btn = tk.Button(
            safe_card,
            text="💜  I'm Safe",
            font=("Georgia", 18, "bold"),
            bg=PURPLE, fg=WHITE,
            activebackground=PURPLE_DARK,
            activeforeground=WHITE,
            relief="flat", cursor="hand2",
            pady=15, padx=40,
            command=self._on_safe_pressed
        )
        self.safe_btn.pack(pady=(0, 5))
        
        # Add rounded look with a border frame
        tk.Label(
            safe_card,
            text="Tap this immediately if you're okay",
            font=("Georgia", 8),
            bg=CARD, fg=TEXT_LIGHT
        ).pack()
        
        # ── WATCH STATUS CARD ──
        watch_card = self._make_card(scroll_frame, padding=15)
        
        tk.Label(
            watch_card,
            text="⌚  Smartwatch Connection",
            font=("Georgia", 10, "bold"),
            bg=CARD, fg=TEXT_DARK
        ).pack(anchor="w", pady=(0, 8))
        
        info_row = tk.Frame(watch_card, bg=CARD)
        info_row.pack(fill="x")
        
        # Connected status
        self.watch_status_lbl = tk.Label(
            info_row,
            text="● Connected",
            font=("Georgia", 10),
            bg=CARD, fg=GREEN
        )
        self.watch_status_lbl.pack(side="left")
        
        # Battery level
        self.battery_lbl = tk.Label(
            info_row,
            text="🔋 85%",
            font=("Georgia", 10),
            bg=CARD, fg=TEXT_MED
        )
        self.battery_lbl.pack(side="right")
        
        # Timestamp of last reading
        self.time_lbl = tk.Label(
            watch_card,
            text="Last reading: just now",
            font=("Georgia", 8),
            bg=CARD, fg=TEXT_LIGHT
        )
        self.time_lbl.pack(anchor="w", pady=(5, 0))
    
    
    # ════════════════════════════════════════
    #   CONTACTS TAB
    # ════════════════════════════════════════
    
    def _build_contacts_tab(self):
        """Builds the emergency contacts management screen."""
        
        frame = tk.Frame(self.content, bg=BG)
        self.tabs["contacts"] = frame
        
        # Title
        title_card = self._make_card(frame, padding=15)
        tk.Label(
            title_card,
            text="👤  Emergency Contacts",
            font=("Georgia", 14, "bold"),
            bg=CARD, fg=TEXT_DARK
        ).pack(anchor="w")
        tk.Label(
            title_card,
            text="These people will be notified when danger is detected",
            font=("Georgia", 9, "italic"),
            bg=CARD, fg=TEXT_LIGHT
        ).pack(anchor="w")
        
        # Add contact button
        add_card = self._make_card(frame, padding=15)
        
        tk.Label(
            add_card,
            text="Add New Contact",
            font=("Georgia", 11, "bold"),
            bg=CARD, fg=TEXT_MED
        ).pack(anchor="w", pady=(0, 10))
        
        # Input fields
        fields_frame = tk.Frame(add_card, bg=CARD)
        fields_frame.pack(fill="x")
        
        # Name field
        tk.Label(fields_frame, text="Name:", font=("Georgia", 9),
                 bg=CARD, fg=TEXT_LIGHT).grid(row=0, column=0, sticky="w", pady=3)
        self.contact_name_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.contact_name_var,
                 font=("Georgia", 10), width=20,
                 bg=BG, fg=TEXT_DARK, relief="flat",
                 highlightthickness=1, highlightcolor=PURPLE,
                 highlightbackground=PURPLE_LITE
                 ).grid(row=0, column=1, padx=5, pady=3)
        
        # Phone field
        tk.Label(fields_frame, text="Phone:", font=("Georgia", 9),
                 bg=CARD, fg=TEXT_LIGHT).grid(row=1, column=0, sticky="w", pady=3)
        self.contact_phone_var = tk.StringVar(value="+91-")
        tk.Entry(fields_frame, textvariable=self.contact_phone_var,
                 font=("Georgia", 10), width=20,
                 bg=BG, fg=TEXT_DARK, relief="flat",
                 highlightthickness=1, highlightcolor=PURPLE,
                 highlightbackground=PURPLE_LITE
                 ).grid(row=1, column=1, padx=5, pady=3)
        
        # Relation field
        tk.Label(fields_frame, text="Relation:", font=("Georgia", 9),
                 bg=CARD, fg=TEXT_LIGHT).grid(row=2, column=0, sticky="w", pady=3)
        self.contact_relation_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.contact_relation_var,
                 font=("Georgia", 10), width=20,
                 bg=BG, fg=TEXT_DARK, relief="flat",
                 highlightthickness=1, highlightcolor=PURPLE,
                 highlightbackground=PURPLE_LITE
                 ).grid(row=2, column=1, padx=5, pady=3)
        
        # Add button
        tk.Button(
            add_card,
            text="+ Add Contact",
            font=("Georgia", 10, "bold"),
            bg=PURPLE, fg=WHITE,
            activebackground=PURPLE_DARK,
            relief="flat", cursor="hand2",
            pady=8, padx=20,
            command=self._add_contact
        ).pack(pady=(12, 0))
        
        # Contacts list
        list_card = self._make_card(frame, padding=15)
        tk.Label(
            list_card,
            text="Saved Contacts",
            font=("Georgia", 11, "bold"),
            bg=CARD, fg=TEXT_MED
        ).pack(anchor="w", pady=(0, 8))
        
        # This frame will hold contact items
        self.contacts_list_frame = tk.Frame(list_card, bg=CARD)
        self.contacts_list_frame.pack(fill="x")
        
        # Initial render
        self._refresh_contacts_list()
    
    
    def _refresh_contacts_list(self):
        """Re-draws the contacts list."""
        # Clear existing items
        for w in self.contacts_list_frame.winfo_children():
            w.destroy()
        
        contacts = self.controller.alerts.contacts
        
        if not contacts:
            tk.Label(
                self.contacts_list_frame,
                text="No contacts saved yet.\nAdd your first emergency contact above!",
                font=("Georgia", 9, "italic"),
                bg=CARD, fg=TEXT_LIGHT,
                justify="center"
            ).pack(pady=20)
            return
        
        for i, contact in enumerate(contacts):
            row = tk.Frame(self.contacts_list_frame, bg=PURPLE_PALE, pady=2)
            row.pack(fill="x", pady=2)
            
            # Contact info
            info = tk.Frame(row, bg=PURPLE_PALE)
            info.pack(side="left", fill="x", expand=True, padx=10, pady=8)
            
            tk.Label(
                info,
                text=f"👤 {contact['name']}  •  {contact['relation']}",
                font=("Georgia", 10, "bold"),
                bg=PURPLE_PALE, fg=TEXT_DARK
            ).pack(anchor="w")
            
            tk.Label(
                info,
                text=contact['phone'],
                font=("Georgia", 9),
                bg=PURPLE_PALE, fg=TEXT_MED
            ).pack(anchor="w")
            
            # Remove button
            tk.Button(
                row,
                text="✕",
                font=("Georgia", 10),
                bg=PURPLE_PALE, fg=RED,
                activebackground=RED, activeforeground=WHITE,
                relief="flat", cursor="hand2", padx=8,
                command=lambda idx=i: self._remove_contact(idx)
            ).pack(side="right", padx=8)
    
    
    # ════════════════════════════════════════
    #   SIMULATE TAB (for testing/demo)
    # ════════════════════════════════════════
    
    def _build_simulate_tab(self):
        """
        Builds the simulation control panel.
        
        This lets you test different scenarios without a real watch.
        In production you'd remove or hide this tab.
        """
        frame = tk.Frame(self.content, bg=BG)
        self.tabs["simulate"] = frame
        
        title_card = self._make_card(frame, padding=15)
        tk.Label(
            title_card,
            text="🎮  Simulation Controls",
            font=("Georgia", 14, "bold"),
            bg=CARD, fg=TEXT_DARK
        ).pack(anchor="w")
        tk.Label(
            title_card,
            text="Test ShHEild with different scenarios\n(for demo - not in real app)",
            font=("Georgia", 9, "italic"),
            bg=CARD, fg=TEXT_LIGHT
        ).pack(anchor="w")
        
        scenarios_card = self._make_card(frame, padding=20)
        
        tk.Label(
            scenarios_card,
            text="Choose a scenario to simulate:",
            font=("Georgia", 10, "bold"),
            bg=CARD, fg=TEXT_MED
        ).pack(pady=(0, 15))
        
        # Scenario buttons
        scenarios = [
            ("😴  Normal / Resting",  "normal",   PURPLE_PALE, TEXT_DARK,
             "Heart rate: 65-80 BPM\nSimulates sitting, reading, relaxing"),
             
            ("🏃  Exercise / Workout", "exercise", "#E8F5E9", "#2E7D32",
             "Heart rate: 130-160 BPM (gradual rise)\nShHEild should NOT alert - this is exercise!"),
            
            ("😰  Stress / Anxiety",   "stress",   "#FFF8E1", "#E65100",
             "Heart rate: 90-115 BPM\nMild stress, monitoring closely"),
            
            ("🚨  DANGER Scenario",    "danger",   "#FFEBEE", "#C62828",
             "Heart rate: 145-175 BPM (sudden spike!)\nAI should detect danger & trigger alerts"),
        ]
        
        for label, name, bg_col, fg_col, description in scenarios:
            btn_frame = tk.Frame(scenarios_card, bg=bg_col, pady=0)
            btn_frame.pack(fill="x", pady=5)
            
     