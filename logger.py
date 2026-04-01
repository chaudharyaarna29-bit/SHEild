"""
shield/logger.py
────────────────
Colour-coded, timestamped logger for SHEild.
"""

import datetime


class Colors:
    RESET   = "\033[0m"
    RED     = "\033[91m"
    YELLOW  = "\033[93m"
    GREEN   = "\033[92m"
    CYAN    = "\033[96m"
    MAGENTA = "\033[95m"
    WHITE   = "\033[97m"
    GREY    = "\033[90m"
    BOLD    = "\033[1m"


class ShieldLogger:
    """Thread-safe colour logger."""

    def __init__(self):
        self._log_history: list[dict] = []

    def _timestamp(self) -> str:
        return datetime.datetime.now().strftime("%H:%M:%S")

    def _record(self, level: str, message: str):
        self._log_history.append({
            "time":    self._timestamp(),
            "level":   level,
            "message": message,
        })
        # Keep only last 100 entries
        if len(self._log_history) > 100:
            self._log_history.pop(0)

    def info(self, message: str):
        self._record("INFO", message)
        print(f"{Colors.GREY}[{self._timestamp()}]{Colors.RESET} "
              f"{Colors.CYAN}[INFO]{Colors.RESET}  {message}")

    def success(self, message: str):
        self._record("OK", message)
        print(f"{Colors.GREY}[{self._timestamp()}]{Colors.RESET} "
              f"{Colors.GREEN}[ OK ]{Colors.RESET}  {message}")

    def warn(self, message: str):
        self._record("WARN", message)
        print(f"{Colors.GREY}[{self._timestamp()}]{Colors.RESET} "
              f"{Colors.YELLOW}[WARN]{Colors.RESET}  {Colors.YELLOW}{message}{Colors.RESET}")

    def danger(self, message: str):
        self._record("SOS", message)
        print(f"{Colors.GREY}[{self._timestamp()}]{Colors.RESET} "
              f"{Colors.RED}{Colors.BOLD}[SOS!]{Colors.RESET}  "
              f"{Colors.RED}{Colors.BOLD}{message}{Colors.RESET}")

    def section(self, title: str):
        """Print a visual section divider."""
        width = 54
        bar = "─" * width
        print(f"\n{Colors.MAGENTA}{bar}\033[0m")
        print(f"{Colors.MAGENTA}  {title}\033[0m")
        print(f"{Colors.MAGENTA}{bar}\033[0m")

    def get_history(self) -> list[dict]:
        return list(self._log_history)
