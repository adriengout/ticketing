"""
Tests unitaires pour le domaine (TD1).

Ces tests vérifient le comportement des entités du domaine.
Ils doivent passer sans aucune dépendance externe (pas de DB, pas d'API).

Écrivez vos tests ici après avoir implémenté les classes dans src/domain/.
Lancez-les avec : pytest tests/domain/
"""

from datetime import datetime

import pytest

from src.domain.comment import Comment
from src.domain.priority import Priority
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
    """Vérifie l'assignation d'un ticket (Version TD2b)."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")

    ticket.assign("agent1")

    assert ticket.assignee_id == "agent1"
    assert ticket.status == Status.OPEN


def test_ticket_resolve():
    """Vérifie la résolution d'un ticket (Nouveau test)."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    now = datetime.now()

    ticket.assign("agent1")
    ticket.start(agent_id="agent1", started_at=now)
    ticket.resolve()

    assert ticket.status == Status.RESOLVED


def test_ticket_close():
    """Vérifie la fermeture d'un ticket en suivant le cycle complet."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    now = datetime.now()

    ticket.assign("agent1")
    ticket.start(agent_id="agent1", started_at=now)
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
    now = datetime.now()

    ticket.assign("agent1")
    ticket.start(agent_id="agent1", started_at=now)
    ticket.resolve()
    ticket.close()

    with pytest.raises(
        ValueError, match="Impossible de faire cette transition de statut"
    ):
        ticket.assign("agent2")


def test_cannot_close_already_closed_ticket():
    """Règle : Un ticket déjà fermé ne peut pas être re-fermé."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    now = datetime.now()

    ticket.assign("agent1")
    ticket.start(agent_id="agent1", started_at=now)
    ticket.resolve()
    ticket.close()

    with pytest.raises(ValueError, match="Impossible de fermer le ticket"):
        ticket.close()


def test_workflow_transitions():
    """Règle : On ne peut pas sauter les étapes (ex: OPEN -> RESOLVED direct)."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")

    with pytest.raises(ValueError, match="Impossible de résoudre ce ticket"):
        ticket.resolve()

    with pytest.raises(ValueError, match="Impossible de fermer le ticket"):
        ticket.close()


# ==========================================================================
# 3. TESTS DES ENRICHISSEMENTS
# ==========================================================================


def test_default_priority_is_medium():
    ticket = Ticket(id="t1", title="Bug", description="desc", creator_id="u1")
    assert ticket.priority == Priority.MEDIUM


def test_change_priority():
    ticket = Ticket(id="t1", title="Bug", description="desc", creator_id="u1")
    ticket.set_priority(Priority.HIGH)
    assert ticket.priority == Priority.HIGH


def test_add_comment():
    ticket = Ticket(id="t1", title="Bug", description="desc", creator_id="u1")
    comment = Comment(id="c1", author_id="u1", content="J'ai besoin d'aide")

    ticket.add_comment(comment)

    assert len(ticket.comments) == 1
    assert ticket.comments[0].content == "J'ai besoin d'aide"


def test_cannot_comment_on_closed_ticket():
    """Règle métier : Pas de commentaire sur un ticket fermé."""
    ticket = Ticket(id="t1", title="Bug", description="desc", creator_id="u1")
    now = datetime.now()

    ticket.assign("agent1")
    ticket.start(agent_id="agent1", started_at=now)
    ticket.resolve()
    ticket.close()

    comment = Comment(id="c2", author_id="u1", content="Trop tard ?")

    with pytest.raises(ValueError, match="Impossible de commenter"):
        ticket.add_comment(comment)
