from src.domain.exceptions import TicketNotFoundError
from src.ports.clock import Clock
from src.ports.ticket_repository import TicketRepository


class ReopenTicketUseCase:
    def __init__(self, ticket_repo: TicketRepository, clock: Clock):
        self.ticket_repo = ticket_repo
        self.clock = clock

    def execute(self, ticket_id: str):
        ticket = self.ticket_repo.get_by_id(ticket_id)
        if not ticket:
            raise TicketNotFoundError()

        # On récupère l'heure via le port Clock
        now = self.clock.now()

        # On délègue la logique au domaine
        ticket.reopen(now)

        self.ticket_repo.save(ticket)
        return ticket
