# src/adapters/db/ticket_repository_inmemory.py
from typing import Optional, dict, list

from src.domain.ticket import Ticket
from src.ports.ticket_repository import TicketRepository


class InMemoryTicketRepository(TicketRepository):
    def __init__(self):
        self._tickets: dict[str, Ticket] = {}

    def get(self, ticket_id: str) -> Optional[Ticket]:
        return self._tickets.get(ticket_id)

    def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        return self.get(ticket_id)

    def save(self, ticket: Ticket) -> None:
        self._tickets[ticket.id] = ticket

    def list_all(self) -> list[Ticket]:
        return list(self._tickets.values())
