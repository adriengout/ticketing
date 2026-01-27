from datetime import datetime, timedelta, timezone

import pytest

from src.adapters.db.ticket_repository_inmemory import InMemoryTicketRepository
from src.application.usecases.reopen_ticket import ReopenTicketUseCase
from src.domain.exceptions import InvalidTicketStateError
from src.domain.status import Status
from src.domain.ticket import Ticket
from tests.adapters.fixed_clock import FixedClock


class TestReopenTicket:
    def setup_method(self):
        self.repo = InMemoryTicketRepository()
        self.base_time = datetime(2026, 1, 20, 12, 0, 0, tzinfo=timezone.utc)
        self.clock = FixedClock(self.base_time)
        self.use_case = ReopenTicketUseCase(self.repo, self.clock)

    def test_reopen_success_within_7_days(self):
        """Doit rouvrir un ticket fermé il y a 6 jours."""
        # Arrange
        ticket = Ticket("t1", "Bug", "Desc", "u1")
        ticket.status = Status.CLOSED
        ticket.closed_at = self.base_time - timedelta(days=6)
        self.repo.save(ticket)

        # Act
        updated_ticket = self.use_case.execute("t1")

        # Assert
        assert updated_ticket.status == Status.IN_PROGRESS
        assert updated_ticket.updated_at == self.base_time

    def test_reopen_fails_after_7_days(self):
        """Doit échouer si le ticket est fermé depuis 7 jours et 1 seconde."""
        # Arrange
        ticket = Ticket("t1", "Bug", "Desc", "u1")
        ticket.status = Status.CLOSED
        # On simule une fermeture il y a 7 jours + 1 sec
        ticket.closed_at = self.base_time - timedelta(days=7, seconds=1)
        self.repo.save(ticket)

        # Act & Assert
        with pytest.raises(InvalidTicketStateError):
            self.use_case.execute("t1")

    def test_reopen_exactly_at_limit(self):
        """Doit accepter la réouverture pile à 7 jours."""
        ticket = Ticket("t1", "Bug", "Desc", "u1")
        ticket.status = Status.CLOSED
        ticket.closed_at = self.base_time - timedelta(days=7)
        self.repo.save(ticket)

        updated_ticket = self.use_case.execute("t1")
        assert updated_ticket.status == Status.IN_PROGRESS
