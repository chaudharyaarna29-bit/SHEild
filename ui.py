"""
shield/ui.py
─────────────
Interactive Terminal Dashboard for SHEild.
Renders a live pulse dashboard and handles user input.
"""

import time
import threading
import os
import sys
from shield.monitor import ThreatLevel, CONFIRM_SECS, ALERT_MIN, DANGER_MIN
from shield.logger import Colors


# ─── ASCII art assets ─────────────────────────────────────────────────────────
HEART_SAFE   = "♥"
HEART_DANGER = "💔"
BAR_WIDTH    = 30


def _bpm_bar(bpm: int, threat: ThreatLevel) -> str:
    """Renders a text progress bar for BPM."""
    filled = min(BAR_WIDTH, int((bpm / 200) * BAR_WIDTH))
    empty  = BAR_WIDTH - filled
    if threat == ThreatLevel.DANGER:
        color = Colors.RED
    elif threat == ThreatLevel.ALERT:
        color = Colors.YELLOW
    else:
        color = Colors.GREEN
    bar = f"{color}{'█' * filled}{'░' * empty}{Colors.RESET}"
    return bar


def _threat_badge(threat: ThreatLevel) -> str:
    if threat == ThreatLevel.DANGER:
        return f"{Colors.RED}{Colors.BOLD}[ ● DANGER ]{Colors.RESET}"
    if threat == ThreatLevel.ALERT:
        return f"{Colors.YELLOW}{Colors.BOLD}[ ◉ ALERT  ]{Colors.RESET}"
    return f"{Colors.GREEN}[ ○ SAFE   ]{Colors.RESET}"


def _ecg_sparkline(history: list[int]) -> str:
    """Convert BPM history to a mini sparkline."""
    chars = " ▁▂▃▄▅▆▇█"
    lo, hi = 55, 185
    out = []
    for v in history[-30:]:
        idx = int((v - lo) / (hi - lo) * (len(chars) - 1))
        idx = max(0, min(len(chars) - 1, idx))
        out.append(chars[idx])
    return "".join(out)


def _countdown_bar(remaining: int, total: int = CONFIRM_SECS) -> str:
    filled = int((remaining / total) * 20)
    empty  = 20 - filled
    return (
        f"{Colors.RED}{'█' * filled}"
        f"{Colors.GREY}{'░' * empty}{Colors.RESET}"
        f" {Colors.RED}{Colors.BOLD}{remaining}s{Colors.RESET}"
    )


# ─── Dashboard Renderer ───────────────────────────────────────────────────────
class ShieldUI:

    def __init__(self, monitor, alert, location, logger):
        self.monitor  = monitor
        self.alert    = alert
        self.location = location
        self.logger   = logger
        self._running = True

    # ── Main loop ─────────────────────────────────────────────────────────────
    def run(self):
        self._print_welcome()
        time.sleep(1)

        # Render dashboard in a background thread
        dash_thread = threading.Thread(target=self._dashboard_loop, daemon=True)
        dash_thread.start()

        # Input loop on main thread
        self._input_loop()

    def _dashboard_loop(self):
        while self._running:
            self._render_dashboard()
            time.sleep(1)

    def _render_dashboard(self):
        os.system("clear" if os.name != "nt" else "cls")

        bpm    = self.monitor.current_bpm
        threat = self.monitor.threat_level
        hist   = self.monitor.bpm_history
        loc    = self.location.get_current()

        # ── Header ──
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("  ╔═══════════════════════════════════════════════════╗")
        print("  ║          🛡️  SHEild — Safety Dashboard            ║")
        print("  ╚═══════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}")

        # ── Pulse ──
        heart = HEART_DANGER if threat == ThreatLevel.DANGER else HEART_SAFE
        print(f"  {heart}  PULSE   {Colors.BOLD}{bpm:>3} BPM{Colors.RESET}  "
              f"{_bpm_bar(bpm, threat)}  {_threat_badge(threat)}")
        print()

        # ── ECG sparkline ──
        ecg_color = (Colors.RED if threat == ThreatLevel.DANGER
                     else Colors.YELLOW if threat == ThreatLevel.ALERT
                     else Colors.GREEN)
        print(f"  ECG ▶  {ecg_color}{_ecg_sparkline(hist)}{Colors.RESET}")
        print()

        # ── Thresholds ──
        print(f"  {Colors.GREY}Thresholds ─  "
              f"{Colors.YELLOW}Alert ≥ {ALERT_MIN} BPM{Colors.RESET}  │  "
              f"{Colors.RED}Danger ≥ {DANGER_MIN} BPM{Colors.RESET}")
        print()

        # ── Location ──
        print(f"  📍 {Colors.CYAN}{loc.get('address', 'Locating...')}{Colors.RESET}")
        print(f"     {Colors.GREY}{loc.get('maps_url', '')}{Colors.RESET}")
        print()

        # ── SOS / Confirming state ──
        if self.alert.sos_active:
            print(f"  {Colors.RED}{Colors.BOLD}{'─'*51}{Colors.RESET}")
            print(f"  {Colors.RED}{Colors.BOLD}  🔴 SOS ACTIVE — HELP IS ON THE WAY{Colors.RESET}")
            print(f"  {Colors.RED}{Colors.BOLD}{'─'*51}{Colors.RESET}")
            print(f"  {Colors.RED}  Police & contacts have been notified.{Colors.RESET}")
            print(f"  {Colors.GREY}  Press [C] to cancel if you are safe.{Colors.RESET}")
            print()
        elif self.monitor.is_confirming:
            remaining = self.monitor.get_confirm_remaining()
            print(f"  {Colors.YELLOW}{Colors.BOLD}{'─'*51}{Colors.RESET}")
            print(f"  {Colors.YELLOW}{Colors.BOLD}  ⚠️  DANGER DETECTED — SOS COUNTDOWN{Colors.RESET}")
            print(f"  {Colors.YELLOW}{Colors.BOLD}{'─'*51}{Colors.RESET}")
            print(f"  Auto-SOS in: {_countdown_bar(remaining)}")
            print(f"  {Colors.GREY}  [S] Confirm SOS now  │  [C] I'm safe, cancel{Colors.RESET}")
            print()
        elif threat == ThreatLevel.ALERT:
            print(f"  {Colors.YELLOW}  ⚠️  Elevated pulse. Location shared with contacts.{Colors.RESET}")
            print()

        # ── Menu ──
        print(f"  {Colors.GREY}{'─'*51}{Colors.RESET}")
        print(f"  {Colors.WHITE}Commands:{Colors.RESET}")
        print(f"  {Colors.GREEN}[S]{Colors.RESET} Manual SOS     "
              f"{Colors.CYAN}[P]{Colors.RESET} Simulate panic    "
              f"{Colors.YELLOW}[C]{Colors.RESET} Cancel / I'm safe")
        print(f"  {Colors.GREY}[L]{Colors.RESET} View log        "
              f"{Colors.GREY}[Q]{Colors.RESET} Quit")
        print(f"  {Colors.GREY}{'─'*51}{Colors.RESET}")
        print(f"  {Colors.GREY}Input: {Colors.RESET}", end="", flush=True)

    # ── Input handler ─────────────────────────────────────────────────────────
    def _input_loop(self):
        while self._running:
            try:
                raw = input("").strip().upper()
            except EOFError:
                time.sleep(0.1)
                continue

            if raw == "S":
                self.monitor.trigger_manual_sos()

            elif raw == "P":
                self.monitor.simulate_panic()

            elif raw == "C":
                if self.alert.sos_active or self.monitor.is_confirming:
                    self.monitor.cancel_sos()
                else:
                    self.logger.info("Nothing to cancel. System is monitoring normally.")

            elif raw == "L":
                self._show_log()
                input(f"\n  {Colors.GREY}Press Enter to return to dashboard...{Colors.RESET}")

            elif raw == "Q":
                self._running = False
                self.monitor.stop()
                print(f"\n{Colors.MAGENTA}  SHEild shutting down. Stay safe. 💜{Colors.RESET}\n")
                sys.exit(0)

    # ── Log viewer ────────────────────────────────────────────────────────────
    def _show_log(self):
        os.system("clear" if os.name != "nt" else "cls")
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}  📋  SHEild Event Log{Colors.RESET}\n")
        history = self.logger.get_history()
        if not history:
            print(f"  {Colors.GREY}No events recorded yet.{Colors.RESET}")
            return
        for entry in reversed(history[-20:]):
            level = entry["level"]
            color = (Colors.RED    if level == "SOS"  else
                     Colors.YELLOW if level == "WARN" else
                     Colors.GREEN  if level == "OK"   else
                     Colors.GREY)
            print(f"  {Colors.GREY}{entry['time']}{Colors.RESET}  "
                  f"{color}[{level:4}]{Colors.RESET}  {entry['message']}")

    # ── Welcome screen ────────────────────────────────────────────────────────
    def _print_welcome(self):
        os.system("clear" if os.name != "nt" else "cls")
        print(f"""
{Colors.MAGENTA}{Colors.BOLD}
  ╔══════════════════════════════════════════════════════╗
  ║                                                      ║
  ║    🛡️   SHEild — Women's Autonomous Safety App       ║
  ║                                                      ║
  ║    ● Smartwatch pulse monitoring  ACTIVE             ║
  ║    ● GPS location service         ACTIVE             ║
  ║    ● Emergency contacts           3 loaded           ║
  ║    ● Police station               Configured         ║
  ║                                                      ║
  ╚══════════════════════════════════════════════════════╝
{Colors.RESET}
  {Colors.GREY}Initialising systems...{Colors.RESET}
        """)
