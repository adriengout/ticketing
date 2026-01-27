# tests/application/test_sqlite_integration.py
from src.application.usecases.assign_ticket import AssignTicketUseCase
from src.application.usecases.create_ticket import CreateTicketUseCase
from src.domain.status import Status


def test_create_ticket_with_sqlite(sqlite_ticket_repo):
    """Vérifie que le Use Case CreateTicket fonctionne avec l'adaptateur SQLite."""
    # Arrange
    use_case = CreateTicketUseCase(ticket_repo=sqlite_ticket_repo)

    # Act
    ticket = use_case.execute(
        title="Bug SQLite",
        description="Vérification de la persistance réelle",
        creator_id="user-456",
    )

    # Assert
    assert ticket.id is not None
    # On vérifie la persistance réelle en allant chercher dans la DB
    retrieved = sqlite_ticket_repo.get_by_id(ticket.id)
    assert retrieved is not None
    assert retrieved.title == "Bug SQLite"
    assert retrieved.status == Status.OPEN


def test_assign_ticket_with_sqlite(sqlite_ticket_repo):
    """Vérifie que l'assignation persiste bien en base SQLite."""
    # Arrange
    create_uc = CreateTicketUseCase(sqlite_ticket_repo)
    assign_uc = AssignTicketUseCase(sqlite_ticket_repo)

    ticket = create_uc.execute("Titre", "Desc", "u1")
    agent_id = "agent-007"

    # Act
    assign_uc.execute(ticket.id, agent_id)

    # Assert
    saved_ticket = sqlite_ticket_repo.get_by_id(ticket.id)
    assert saved_ticket.assignee_id == agent_id
