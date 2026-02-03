"""Use case : Lister tous les tickets."""

from src.domain.ticket import Ticket
from src.ports.ticket_repository import TicketRepository


class ListTicketsUseCase:
    def __init__(self, ticket_repository: TicketRepository):
        self.ticket_repository = ticket_repository

    def execute(self) -> list[Ticket]:
        return self.ticket_repository.list_all()
