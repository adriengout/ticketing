# tests/adapters/fixed_clock.py
from datetime import datetime

from src.ports.clock import Clock


class FixedClock(Clock):
    def __init__(self, fixed_now: datetime):
        self.fixed_now = fixed_now

    def now(self) -> datetime:
        return self.fixed_now
