from datetime import datetime, timezone

import pytest

from src.application.usecases.start_ticket import StartTicketUseCase
from src.domain.exceptions import (
    InvalidTicketStateError,
    TicketNotAssignedError,
    TicketNotFoundError,
)
from src.domain.status import Status
from src.domain.ticket import Ticket
from src.ports.ticket_repository import TicketRepository
from tests.adapters.fixed_clock import FixedClock


class MemoryTicketRepository(TicketRepository):
    def __init__(self):
        self.tickets = {}

    def get(self, ticket_id: str):
        return self.tickets.get(ticket_id)

    def get_by_id(self, ticket_id: str):
        return self.get(ticket_id)

    def save(self, ticket: Ticket):
        self.tickets[ticket.id] = ticket

    def list_all(self):
        return list(self.tickets.values())


# --- Tests ---


def test_start_ticket_success():
    """Scénario nominal : Tout se passe bien, l'heure est fixée."""
    # 1. Setup
    repo = MemoryTicketRepository()
    fixed_time = datetime(2026, 1, 16, 14, 30, 0, tzinfo=timezone.utc)
    clock = FixedClock(fixed_time)
    use_case = StartTicketUseCase(repo, clock)

    # Création d'un ticket OPEN et déjà assigné (pré-requis métier)
    ticket = Ticket(id="t1", title="Bug", description="Desc", creator_id="user1")
    ticket.assign("agent_007")  # status reste OPEN
    repo.save(ticket)

    # 2. Execution
    result_ticket = use_case.execute(ticket_id="t1", agent_id="agent_007")

    # 3. Assertions
    assert result_ticket.status == Status.IN_PROGRESS
    assert result_ticket.started_at == fixed_time  # Déterminisme vérifié !
    assert result_ticket.updated_at == fixed_time
    # Vérifier que c'est bien sauvegardé
    assert repo.get("t1").status == Status.IN_PROGRESS


def test_start_ticket_not_found():
    """Erreur si le ticket n'existe pas."""
    repo = MemoryTicketRepository()
    clock = FixedClock(datetime.now())
    use_case = StartTicketUseCase(repo, clock)

    with pytest.raises(TicketNotFoundError):
        use_case.execute("fake_id", "agent_007")


def test_start_ticket_invalid_status():
    """Erreur si le ticket n'est pas OPEN (ex: déjà CLOSED)."""
    repo = MemoryTicketRepository()
    fixed_time = datetime(2026, 1, 16, 14, 30, 0, tzinfo=timezone.utc)
    clock = FixedClock(fixed_time)
    use_case = StartTicketUseCase(repo, clock)

    # Setup du ticket
    ticket = Ticket(id="t1", title="Bug", description="Desc", creator_id="user1")
    ticket.assign("agent_007")

    # ÉTAPES OBLIGATOIRES pour arriver à CLOSED :
    ticket.start("agent_007", fixed_time)
    ticket.resolve()
    ticket.close()
    repo.save(ticket)

    with pytest.raises(InvalidTicketStateError):
        use_case.execute("t1", "agent_007")


def test_start_ticket_not_assigned():
    """Optionnel : Erreur si le ticket n'est pas assigné."""
    repo = MemoryTicketRepository()
    clock = FixedClock(datetime.now())
    use_case = StartTicketUseCase(repo, clock)

    ticket = Ticket(id="t1", title="Bug", description="Desc", creator_id="user1")
    # Pas d'assignation
    repo.save(ticket)

    with pytest.raises(TicketNotAssignedError):
        use_case.execute("t1", "agent_007")
