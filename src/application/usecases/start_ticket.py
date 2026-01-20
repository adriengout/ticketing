from src.domain.exceptions import TicketNotFoundError
from src.domain.ticket import Ticket
from src.ports.clock import Clock
from src.ports.ticket_repository import TicketRepository


class StartTicketUseCase:
    def __init__(self, repository: TicketRepository, clock: Clock):
        self.repository = repository
        self.clock = clock

    def execute(self, ticket_id: str, agent_id: str) -> Ticket:
        ticket = self.repository.get(ticket_id)

        if ticket is None:
            raise TicketNotFoundError(f"Ticket {ticket_id} introuvable")

        now = self.clock.now()

        ticket.start(agent_id=agent_id, started_at=now)

        self.repository.save(ticket)

        return ticket
