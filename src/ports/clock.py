# src/ports/clock.py
from abc import ABC, abstractmethod
from datetime import datetime


class Clock(ABC):
    """Interface pour l'accès au temps."""

    @abstractmethod
    def now(self) -> datetime:
        """Retourne la date et l'heure actuelles (UTC)."""
        pass
