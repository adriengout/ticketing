from datetime import datetime, timezone

from src.ports.clock import Clock


class SystemClock(Clock):
    def now(self) -> datetime:
        # On utilise UTC par bonne pratique
        return datetime.now(timezone.utc)
