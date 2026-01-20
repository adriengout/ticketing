# src/ports/ticket_repository.py
from abc import ABC, abstractmethod
from typing import Optional

from src.domain.ticket import Ticket


class TicketRepository(ABC):
    @abstractmethod
    def get(self, ticket_id: str) -> Optional[Ticket]:
        pass

    @abstractmethod
    def save(self, ticket: Ticket) -> None:
        pass

    @abstractmethod
    def list_all(self) -> list[Ticket]:
        pass

    @abstractmethod
    def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        pass
