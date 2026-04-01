# 🛡️ SHEild — Women's Autonomous Safety App
### Python Edition | Pulse-Based Threat Detection

---

## Overview

SHEild is an autonomous women's safety application written in Python.  
It continuously reads pulse data from a wrist smartwatch API, detects danger autonomously, and takes a 3-stage protective response — all without the user having to do anything.

---

## 🔁 Autonomous Response Flow

```
Smartwatch API  ──►  Pulse Monitor  ──►  Threat Classifier
                                               │
                      ┌────────────────────────┼────────────────────────┐
                      │                        │                        │
                   SAFE (< 110)           ALERT (110–129)         DANGER (≥ 130)
                   Continue watch         ┌─────────┐             ┌─────────────┐
                                          │ Send    │             │ 15-second   │
                                          │ live GPS│             │ SOS confirm │
                                          │ to all  │             │ countdown   │
                                          │contacts │             │             │
                                          └─────────┘             │ No response?│
                                                                  │ AUTO-SOS ✓  │
                                                                  └─────────────┘
                                                                         │
                                                            ┌────────────▼────────────┐
                                                            │   SOS ACTIVATED         │
                                                            │  • SMS all contacts     │
                                                            │  • GPS link shared      │
                                                            │  • Police station alert │
                                                            └─────────────────────────┘
```

---

## 📂 Project Structure

```
SHEild/
├── main.py              ← Entry point
├── requirements.txt
└── shield/
    ├── __init__.py
    ├── config.py        ← API keys & thresholds
    ├── monitor.py       ← Smartwatch pulse polling & threat detection
    ├── location.py      ← GPS / IP geolocation service
    ├── alert.py         ← Contact SMS, SOS, police notification
    ├── logger.py        ← Colour-coded terminal logger
    └── ui.py            ← Live terminal dashboard
```

---

## ⚙️ Setup & Run

```bash
# 1. Clone / unzip the project
cd SHEild

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your credentials to shield/config.py

# 4. Run the app
python main.py
```

---

## 🖥️ Terminal Dashboard Commands

| Key | Action                        |
|-----|-------------------------------|
| `S` | Trigger manual SOS            |
| `P` | Simulate panic/stress event   |
| `C` | Cancel SOS / confirm I'm safe |
| `L` | View event log                |
| `Q` | Quit the application          |

---

## 🔌 API Integrations

### Smartwatch Pulse (`shield/monitor.py`)
Replace `SmartWatchAPI.fetch_bpm()` with a real HTTP call:
```python
import requests
r = requests.get(WATCH_API_URL, headers={"Authorization": f"Bearer {WATCH_API_TOKEN}"})
return r.json()["bpm"]
```
Supports: **Fitbit API**, **Garmin Connect**, **Apple HealthKit**, **Samsung Health**, **Wear OS**.

### SMS Alerts (`shield/alert.py`)
Replace `_send_sms()` with Twilio:
```python
from twilio.rest import Client
Client(TWILIO_SID, TWILIO_AUTH).messages.create(
    body=message, from_=TWILIO_FROM_PHONE, to=contact.phone
)
```

### GPS Location (`shield/location.py`)
Replace `_fetch_from_api()` with:
```python
import requests
r = requests.get("https://ipapi.co/json/")
data = r.json()
return {"latitude": data["latitude"], "longitude": data["longitude"], ...}
```
Or use phone GPS via a local Flask server running on the device.

### Police Alert (`shield/alert.py → _alert_police()`)
```python
requests.post(POLICE_API_URL, json={
    "location": address, "coordinates": {...}, "app": "SHEild"
}, headers={"Authorization": f"Bearer {POLICE_API_KEY}"})
```

---

## 🎯 Thresholds (configurable in `shield/config.py`)

| Level  | BPM     | Action                                      |
|--------|---------|---------------------------------------------|
| Safe   | < 110   | Normal monitoring                           |
| Alert  | 110–129 | Share live GPS with all contacts            |
| Danger | ≥ 130   | 15s countdown → auto-SOS if no response     |
| SOS    | Active  | SMS contacts + alert police + stream GPS    |

---

## 💜 Built with care for safety.
