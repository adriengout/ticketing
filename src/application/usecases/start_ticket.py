from src.domain.exceptions import TicketNotFoundError
from src.domain.ticket import Ticket
from src.ports.clock import Clock
from src.ports.ticket_repository import TicketRepository


class StartTicketUseCase:
    def __init__(self, ticket_repo: TicketRepository, clock: Clock):
        self.ticket_repo = ticket_repo
        self.clock = clock

    def execute(self, ticket_id: str, agent_id: str) -> Ticket:
        ticket = self.ticket_repo.get_by_id(ticket_id)

        if not ticket:
            raise TicketNotFoundError(f"Ticket {ticket_id} not found")

        current_time = self.clock.now()
        ticket.start(agent_id, current_time)

        self.ticket_repo.save(ticket)

        return ticket
