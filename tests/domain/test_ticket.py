"""
Tests unitaires pour le domaine (TD1).

Ces tests vérifient le comportement des entités du domaine.
Ils doivent passer sans aucune dépendance externe (pas de DB, pas d'API).

Écrivez vos tests ici après avoir implémenté les classes dans src/domain/.
Lancez-les avec : pytest tests/domain/
"""

from datetime import datetime

import pytest

from src.domain.status import Status
from src.domain.ticket import Ticket
from src.domain.user import User

# ==========================================================================
# 1. TESTS NOMINAUX (Le scénario idéal)
# ==========================================================================


def test_status_values_exist():
    """Vérifie que les 4 statuts existent."""
    assert Status.OPEN.value == "open"
    assert Status.IN_PROGRESS.value == "in_progress"
    assert Status.RESOLVED.value == "resolved"
    assert Status.CLOSED.value == "closed"


def test_user_creation():
    """Vérifie la création d'un utilisateur."""
    user = User(id="u1", username="alice", is_agent=False)
    assert user.id == "u1"
    assert user.username == "alice"


def test_ticket_creation():
    """Vérifie la création d'un ticket avec valeurs par défaut."""
    ticket = Ticket(
        id="t1",
        title="Bug connexion",
        description="Impossible de se connecter",
        creator_id="user1",
    )
    assert ticket.status == Status.OPEN
    assert ticket.assignee_id is None
    assert isinstance(ticket.created_at, datetime)


def test_ticket_assign():
    """Vérifie l'assignation d'un ticket."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")

    ticket.assign("agent1")

    assert ticket.assignee_id == "agent1"
    assert ticket.status == Status.IN_PROGRESS


def test_ticket_resolve():
    """Vérifie la résolution d'un ticket (Nouveau test)."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")

    ticket.assign("agent1")
    ticket.resolve()

    assert ticket.status == Status.RESOLVED


def test_ticket_close():
    """Vérifie la fermeture d'un ticket en suivant le cycle complet."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")

    ticket.assign("agent1")
    ticket.resolve()
    ticket.close()

    assert ticket.status == Status.CLOSED
    assert ticket.closed_at is not None


# ==========================================================================
# 2. TESTS DES RÈGLES MÉTIER (Invariants & Erreurs)
# ==========================================================================


def test_ticket_must_have_creator():
    """Règle : Un ticket doit avoir un créateur."""
    with pytest.raises(ValueError, match="créateur"):
        Ticket(id="t1", title="Titre", description="desc", creator_id="")


def test_ticket_title_cannot_be_empty():
    """Règle : Un ticket doit avoir un titre non vide."""
    with pytest.raises(ValueError, match="titre"):
        Ticket(id="t1", title="", description="desc", creator_id="u1")

    with pytest.raises(ValueError):
        Ticket(id="t2", title="   ", description="desc", creator_id="u1")


def test_cannot_assign_without_agent_id():
    """Règle : L'identifiant de l'agent est obligatoire pour assigner."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")

    with pytest.raises(ValueError, match="vide"):
        ticket.assign("")


def test_cannot_assign_closed_ticket():
    """Règle : Un ticket fermé ne peut plus être assigné."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")

    ticket.assign("agent1")
    ticket.resolve()
    ticket.close()

    with pytest.raises(ValueError, match="impossible"):
        ticket.assign("agent2")


def test_cannot_close_already_closed_ticket():
    """Règle : Un ticket déjà fermé ne peut pas être re-fermé."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")

    ticket.assign("agent1")
    ticket.resolve()
    ticket.close()

    with pytest.raises(ValueError, match="impossible"):
        ticket.close()


def test_workflow_transitions():
    """Règle : On ne peut pas sauter les étapes (ex: OPEN -> RESOLVED direct)."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")

    with pytest.raises(ValueError, match="Impossible de résoudre ce ticket"):
        ticket.resolve()

    with pytest.raises(ValueError, match="impossible de fermer le ticket"):
        ticket.close()
