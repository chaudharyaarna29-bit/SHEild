"""
shield/alert.py
────────────────
Alert System
Handles contact notification, SOS activation, and police alert.

Production integrations:
  SMS  → Twilio / AWS SNS
  Call → Twilio Voice API
  Push → Firebase Cloud Messaging
"""

import time
import threading
from dataclasses import dataclass


# ─── Emergency Contacts ───────────────────────────────────────────────────────
@dataclass
class Contact:
    name:     str
    phone:    str
    relation: str


EMERGENCY_CONTACTS: list[Contact] = [
    Contact("Priya (Sister)",  "+91 98765 43210", "sister"),
    Contact("Mom",             "+91 91234 56789", "mother"),
    Contact("Rahul (Friend)",  "+91 87654 32109", "friend"),
]


# ─── Police Station ───────────────────────────────────────────────────────────
@dataclass
class PoliceStation:
    name:    str
    number:  str
    email:   str


NEAREST_POLICE = PoliceStation(
    name   = "Koramangala Police Station",
    number = "100 / +91 80 2553 1253",
    email  = "koramangala.ps@ksp.gov.in",
)


# ─── Alert System ─────────────────────────────────────────────────────────────
class AlertSystem:

    def __init__(self, logger, location_service):
        self.logger    = logger
        self.location  = location_service
        self.sos_active: bool = False
        self._notified_contacts: list[str] = []
        self._lock = threading.Lock()

    # ── Step 1: Share location with contacts ──────────────────────────────────
    def send_location_to_contacts(self):
        """
        Sends live GPS location to all emergency contacts.
        Production: replace _send_sms() with Twilio or SNS call.
        """
        loc = self.location.get_current()
        maps_link = loc.get("maps_url", self.location.get_maps_link())
        address   = loc.get("address", "Unknown")

        self.logger.section("📍 LIVE LOCATION SHARED")

        for contact in EMERGENCY_CONTACTS:
            if contact.name in self._notified_contacts:
                continue  # already sent this session

            message = (
                f"🚨 SHEild ALERT 🛡️\n"
                f"[Name] may need help.\n"
                f"📍 Location: {address}\n"
                f"🗺️  Map: {maps_link}\n"
                f"This is an automated safety alert from SHEild App."
            )

            self._send_sms(contact, message)
            with self._lock:
                self._notified_contacts.append(contact.name)

            self.logger.success(
                f"📲 Location SMS sent → {contact.name} ({contact.phone})"
            )
            time.sleep(0.5)  # stagger messages

    # ── Step 2: Activate SOS ──────────────────────────────────────────────────
    def activate_sos(self, trigger_reason: str = ""):
        with self._lock:
            if self.sos_active:
                return
            self.sos_active = True

        loc     = self.location.get_current()
        address = loc.get("address", "Unknown location")
        maps    = loc.get("maps_url", self.location.get_maps_link())

        self.logger.section("🔴 SOS ACTIVATED")
        self.logger.danger(f"Trigger: {trigger_reason}")
        self.logger.danger(f"Location: {address}")
        self.logger.danger(f"Map link: {maps}")

        # Notify all contacts with full SOS message
        for contact in EMERGENCY_CONTACTS:
            sos_msg = (
                f"🔴 SOS EMERGENCY — SHEild App 🛡️\n"
                f"IMMEDIATE HELP NEEDED!\n"
                f"📍 {address}\n"
                f"🗺️  {maps}\n"
                f"Trigger: {trigger_reason}\n"
                f"Please call or respond immediately!"
            )
            self._send_sms(contact, sos_msg)
            self.logger.danger(
                f"🆘 SOS SMS sent → {contact.name} ({contact.phone})"
            )
            time.sleep(0.3)

        # Alert police station
        self._alert_police(address, maps, trigger_reason)

    # ── Step 3: Police notification ───────────────────────────────────────────
    def _alert_police(self, address: str, maps: str, reason: str):
        police_msg = (
            f"EMERGENCY ALERT — SHEild Women's Safety App\n"
            f"A woman may be in danger.\n"
            f"📍 Location: {address}\n"
            f"🗺️  Map: {maps}\n"
            f"Trigger: {reason}\n"
            f"Please dispatch assistance immediately.\n"
            f"Contact via app or respond to this message."
        )

        self.logger.section("🚔 POLICE NOTIFIED")
        self.logger.danger(
            f"Alert sent to: {NEAREST_POLICE.name}"
        )
        self.logger.danger(
            f"Police number: {NEAREST_POLICE.number}"
        )
        self.logger.danger(
            f"Email: {NEAREST_POLICE.email}"
        )
        self.logger.danger(
            f"Location shared: {address}"
        )

        # ── Production police alert (replace below) ──
        # import requests
        # requests.post(
        #     "https://police-api.gov.in/v1/emergency",
        #     json={
        #         "location": address,
        #         "coordinates": {"lat": lat, "lng": lng},
        #         "message": police_msg,
        #         "app": "SHEild",
        #     },
        #     headers={"Authorization": f"Bearer {POLICE_API_KEY}"},
        # )

        # Simulated: log confirmation
        self.logger.success(
            "✅ Police alert delivered. Reference ID: SHE-"
            + str(int(time.time()))[-6:]
        )

    # ── Deactivate SOS ────────────────────────────────────────────────────────
    def deactivate_sos(self):
        with self._lock:
            self.sos_active = False
            self._notified_contacts.clear()
        self.logger.success("SOS deactivated. All systems reset.")

    # ── SMS stub ──────────────────────────────────────────────────────────────
    @staticmethod
    def _send_sms(contact: Contact, message: str):
        """
        Stub — replace with Twilio in production:

            from twilio.rest import Client
            client = Client(TWILIO_SID, TWILIO_AUTH)
            client.messages.create(
                body  = message,
                from_ = TWILIO_PHONE,
                to    = contact.phone,
            )
        """
        # Simulated delivery (prints first line of message only)
        _ = message  # suppress unused warning
        pass         # delivery confirmed via logger above
