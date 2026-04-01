"""
shield/monitor.py
──────────────────
Smartwatch Pulse Monitor
Polls the wearable API (real or simulated) every second.
Detects elevated / danger BPM and escalates automatically.
"""

import time
import random
import threading
from dataclasses import dataclass, field
from enum import Enum


# ─── Thresholds ───────────────────────────────────────────────────────────────
SAFE_MAX   = 109   # bpm ─ below this is safe
ALERT_MIN  = 110   # bpm ─ elevated / location sharing
DANGER_MIN = 130   # bpm ─ critical / SOS countdown
CONFIRM_SECS = 15  # seconds before auto-SOS fires


class ThreatLevel(Enum):
    SAFE    = "SAFE"
    ALERT   = "ALERT"
    DANGER  = "DANGER"


@dataclass
class PulseReading:
    bpm: int
    threat: ThreatLevel
    timestamp: float = field(default_factory=time.time)


# ─── Simulated Smartwatch API ─────────────────────────────────────────────────
class SmartWatchAPI:
    """
    Simulates a wrist smartwatch BPM data API.
    In production, replace `fetch_bpm()` with a real HTTP/BLE call:

        GET https://api.yourwatch.com/v1/health/heart_rate
        Headers: { Authorization: Bearer <token> }
        Response: { "bpm": 72, "timestamp": "..." }
    """

    def __init__(self):
        self._base_bpm: float = 72.0
        self._spike_active: bool = False
        self._lock = threading.Lock()

    def trigger_spike(self):
        """Simulate a sudden stress / panic event."""
        with self._lock:
            self._spike_active = True

    def clear_spike(self):
        with self._lock:
            self._spike_active = False
            self._base_bpm = 72.0

    def fetch_bpm(self) -> int:
        """
        Returns a BPM reading.
        In production, swap with:
            response = requests.get(WATCH_API_URL, headers=AUTH_HEADER, timeout=3)
            return response.json()["bpm"]
        """
        with self._lock:
            if self._spike_active:
                # Simulate rapid escalation
                self._base_bpm = min(185.0, self._base_bpm + random.uniform(4, 10))
            else:
                # Normal resting variance
                delta = random.uniform(-1.5, 1.5)
                self._base_bpm = max(60.0, min(82.0, self._base_bpm + delta))
            return round(self._base_bpm)


# ─── Pulse Monitor ────────────────────────────────────────────────────────────
class PulseMonitor:
    """
    Continuously polls the smartwatch API.
    Escalates through SAFE → ALERT → DANGER autonomously.
    """

    def __init__(self, logger, alert_system):
        self.logger       = logger
        self.alert        = alert_system
        self.watch        = SmartWatchAPI()

        self.current_bpm   : int         = 72
        self.threat_level  : ThreatLevel = ThreatLevel.SAFE
        self.bpm_history   : list[int]   = [72] * 30
        self.running       : bool        = False

        self._prev_threat  : ThreatLevel = ThreatLevel.SAFE
        self._confirm_timer: threading.Timer | None = None
        self._confirming   : bool        = False
        self._confirm_start: float       = 0.0
        self._lock         = threading.Lock()

    # ── Public API ────────────────────────────────────────────────────────────
    def start(self):
        self.running = True
        while self.running:
            bpm = self.watch.fetch_bpm()
            self._process(bpm)
            time.sleep(1)

    def stop(self):
        self.running = False
        self._cancel_confirm_timer()

    def trigger_manual_sos(self):
        self.logger.danger("Manual SOS button pressed by user!")
        self._cancel_confirm_timer()
        self.alert.activate_sos("MANUAL TRIGGER")

    def cancel_sos(self):
        """Called when user confirms they are safe."""
        self._cancel_confirm_timer()
        with self._lock:
            self._confirming = False
        self.watch.clear_spike()
        self.alert.deactivate_sos()
        self.logger.success("SOS cancelled. User confirmed safe. Monitoring resumed.")

    def simulate_panic(self):
        """Demo helper — simulates a stress/panic spike."""
        self.watch.trigger_spike()
        self.logger.warn("⚡ Simulated panic event injected into pulse stream.")

    def get_confirm_remaining(self) -> int:
        """Seconds remaining on the auto-SOS countdown."""
        if not self._confirming:
            return 0
        elapsed = time.time() - self._confirm_start
        return max(0, CONFIRM_SECS - int(elapsed))

    @property
    def is_confirming(self) -> bool:
        return self._confirming

    # ── Internal ──────────────────────────────────────────────────────────────
    def _process(self, bpm: int):
        with self._lock:
            self.current_bpm = bpm
            self.bpm_history.append(bpm)
            if len(self.bpm_history) > 60:
                self.bpm_history.pop(0)

            new_threat = self._classify(bpm)
            self.threat_level = new_threat

        self._handle_transition(bpm, new_threat)
        self._prev_threat = new_threat

    def _classify(self, bpm: int) -> ThreatLevel:
        if bpm >= DANGER_MIN:
            return ThreatLevel.DANGER
        if bpm >= ALERT_MIN:
            return ThreatLevel.ALERT
        return ThreatLevel.SAFE

    def _handle_transition(self, bpm: int, threat: ThreatLevel):
        prev = self._prev_threat

        # ── SAFE → ALERT: send location ──
        if prev == ThreatLevel.SAFE and threat == ThreatLevel.ALERT:
            self.logger.warn(
                f"Elevated pulse detected: {bpm} BPM ≥ {ALERT_MIN}. "
                "Sending live location to contacts."
            )
            threading.Thread(
                target=self.alert.send_location_to_contacts,
                daemon=True
            ).start()

        # ── Any → DANGER: start confirm countdown ──
        if threat == ThreatLevel.DANGER and not self._confirming and \
                not self.alert.sos_active:
            self._start_confirm_countdown(bpm)

        # ── DANGER/ALERT → SAFE: reset ──
        if threat == ThreatLevel.SAFE and prev != ThreatLevel.SAFE:
            if not self.alert.sos_active:
                self._cancel_confirm_timer()
                with self._lock:
                    self._confirming = False
                self.logger.success(
                    f"Pulse normalised ({bpm} BPM). Monitoring resumed."
                )

    def _start_confirm_countdown(self, bpm: int):
        with self._lock:
            self._confirming  = True
            self._confirm_start = time.time()

        self.logger.danger(
            f"CRITICAL pulse: {bpm} BPM ≥ {DANGER_MIN}! "
            f"Auto-SOS in {CONFIRM_SECS}s unless cancelled."
        )
        # Also immediately share location
        threading.Thread(
            target=self.alert.send_location_to_contacts,
            daemon=True
        ).start()

        self._confirm_timer = threading.Timer(
            CONFIRM_SECS, self._auto_sos
        )
        self._confirm_timer.daemon = True
        self._confirm_timer.start()

    def _auto_sos(self):
        with self._lock:
            self._confirming = False
        self.logger.danger(
            "No response within confirmation window. AUTO-SOS ACTIVATED."
        )
        self.alert.activate_sos("AUTO — no user response")

    def _cancel_confirm_timer(self):
        if self._confirm_timer and self._confirm_timer.is_alive():
            self._confirm_timer.cancel()
