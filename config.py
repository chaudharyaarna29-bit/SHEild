"""
shield/config.py
─────────────────
Central configuration for SHEild.
Replace placeholder values with your real API credentials.
"""

# ─── Smartwatch API ───────────────────────────────────────────────────────────
WATCH_API_URL   = "https://api.yourwatch.com/v1/health/heart_rate"
WATCH_API_TOKEN = "YOUR_WATCH_API_TOKEN"

# ─── Twilio (SMS / Calls) ─────────────────────────────────────────────────────
TWILIO_ACCOUNT_SID = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN  = "your_twilio_auth_token"
TWILIO_FROM_PHONE  = "+1XXXXXXXXXX"

# ─── Firebase (Push Notifications) ───────────────────────────────────────────
FIREBASE_SERVER_KEY = "YOUR_FIREBASE_SERVER_KEY"
FIREBASE_DEVICE_TOKEN = "USER_DEVICE_FCM_TOKEN"

# ─── Police API (if available in your region) ─────────────────────────────────
POLICE_API_URL = "https://police-api.gov.in/v1/emergency"
POLICE_API_KEY = "YOUR_POLICE_API_KEY"

# ─── IP Geolocation (fallback if no GPS) ─────────────────────────────────────
IPGEO_API_URL = "https://ipapi.co/json/"

# ─── Pulse Detection Thresholds ───────────────────────────────────────────────
BPM_ALERT_THRESHOLD  = 110   # share location
BPM_DANGER_THRESHOLD = 130   # start SOS countdown
SOS_CONFIRM_SECONDS  = 15    # countdown before auto-SOS

# ─── User Profile ─────────────────────────────────────────────────────────────
USER_NAME  = "User"
USER_PHONE = "+91 XXXXX XXXXX"
