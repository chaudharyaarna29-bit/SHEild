"""
shield/location.py
───────────────────
GPS Location Service
Fetches current coordinates via IP-geolocation API.
In production, integrates with phone GPS or smartwatch GPS.
"""

import time
import random


# ─── Sample location (used when real API unavailable) ─────────────────────────
_FALLBACK_LOCATION = {
    "latitude":  12.9352,
    "longitude": 77.6245,
    "address":   "Koramangala 4th Block, Bengaluru, Karnataka 560034",
    "city":      "Bengaluru",
    "state":     "Karnataka",
    "country":   "India",
    "maps_url":  "https://maps.google.com/?q=12.9352,77.6245",
}


class LocationService:
    """
    Provides current GPS coordinates.

    Production integration:
    ─────────────────────────────────────────────────────────────────
    Option A — Phone GPS (via Flask/FastAPI server on device):
        GET http://localhost:5000/location
        → {"lat": 12.93, "lng": 77.62, "accuracy": 10}

    Option B — IP Geolocation fallback:
        GET https://ipapi.co/json/
        Headers: {}
        → {"latitude": ..., "longitude": ..., "city": ..., ...}

    Option C — Smartwatch GPS:
        GET https://api.garmin.com/wellness-api/rest/activities
        (or Apple HealthKit / Fitbit Location API)
    ─────────────────────────────────────────────────────────────────
    """

    def __init__(self, logger):
        self.logger    = logger
        self._cached   = None
        self._last_fetch: float = 0.0
        self._cache_ttl = 30  # seconds

    def get_current(self) -> dict:
        """
        Returns current location dict.
        Uses cache if fresh, else re-fetches.
        """
        now = time.time()
        if self._cached and (now - self._last_fetch) < self._cache_ttl:
            return self._cached

        location = self._fetch_from_api()
        self._cached    = location
        self._last_fetch = now
        return location

    def get_maps_link(self) -> str:
        loc = self.get_current()
        lat = loc.get("latitude",  _FALLBACK_LOCATION["latitude"])
        lng = loc.get("longitude", _FALLBACK_LOCATION["longitude"])
        return f"https://maps.google.com/?q={lat},{lng}"

    def get_formatted(self) -> str:
        loc = self.get_current()
        return (
            f"{loc.get('address', 'Unknown address')}\n"
            f"  Lat: {loc.get('latitude')}  Lng: {loc.get('longitude')}\n"
            f"  📌 {loc.get('maps_url', self.get_maps_link())}"
        )

    # ── Internal ──────────────────────────────────────────────────────────────
    def _fetch_from_api(self) -> dict:
        """
        Replace this block with a real API call, e.g.:

            import requests
            try:
                r = requests.get("https://ipapi.co/json/", timeout=5)
                r.raise_for_status()
                data = r.json()
                return {
                    "latitude":  data["latitude"],
                    "longitude": data["longitude"],
                    "address":   f"{data['city']}, {data['region']}",
                    "city":      data["city"],
                    "maps_url":  f"https://maps.google.com/?q={data['latitude']},{data['longitude']}",
                }
            except Exception:
                pass   # fall through to fallback

        For now we simulate a small GPS drift to mimic real movement.
        """
        loc = dict(_FALLBACK_LOCATION)
        # Simulate tiny movement (±0.0005 degrees ≈ ±55 metres)
        loc["latitude"]  = round(loc["latitude"]  + random.uniform(-0.0005, 0.0005), 6)
        loc["longitude"] = round(loc["longitude"] + random.uniform(-0.0005, 0.0005), 6)
        loc["maps_url"]  = (
            f"https://maps.google.com/?q={loc['latitude']},{loc['longitude']}"
        )
        return loc
