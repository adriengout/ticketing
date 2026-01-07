"""
Entité Ticket (ticket de support).

TODO (TD01) : Compléter cette classe avec les attributs et méthodes nécessaires.
C'est l'entité centrale du domaine métier.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from domain.status import Status


def _now_utc() -> datetime:
    """Retourne l'heure actuelle en UTC."""
    return datetime.now(timezone.utc)


@dataclass
class Ticket:
    """
    Entité principale du domaine : un ticket de support.

    TODO: Compléter cette classe avec :
    1. Les attributs obligatoires (id, title, description, status...)
    2. Les attributs optionnels (assignee, dates...)
    3. Les méthodes métier (assign, close...)

    Pensez aux règles métier (invariants) :
    - Un ticket doit avoir un titre non vide
    - Un ticket fermé ne peut plus être modifié
    - etc.

    Attributs:
        id: Identifiant unique du ticket
        title: Titre court décrivant le problème
        description: Description détaillée
        # TODO: Ajouter les autres attributs
    """

    id: str
    title: str
    description: str
    creator_id: str

    status: Status = Status.OPEN
    created_at: datetime = _now_utc()
    updated_at: datetime = _now_utc()

    assignee_id: Optional[str] = None
    closed_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("Le titre du ticket ne peut pas être vide")

        if not self.creator_id:
            raise ValueError("Un ticket doit avoir un créateur")

    def verif_status(self, asked_status: Status) -> bool:
        transitions_autorisee = {
            Status.OPEN: {Status.IN_PROGRESS},
            Status.IN_PROGRESS: {Status.RESOLVED},
            Status.RESOLVED: {Status.CLOSED, Status.IN_PROGRESS},
            Status.CLOSED: set(),
        }
        return asked_status in transitions_autorisee[self.status]

    def assign(self, user_id: str):
        """Assigne le ticket à un agent."""
        if not user_id:
            raise ValueError("L'identifiant de l'agent ne peut pas être vide")
        if not self.verif_status(Status.IN_PROGRESS):
            raise ValueError("impossible de faire cette transition de statut")
        self.assignee_id = user_id
        self.status = Status.IN_PROGRESS

    #
    def close(self):
        """Ferme le ticket."""
        if not self.verif_status(Status.CLOSED):
            raise ValueError("impossible de fermer le ticket")
        self.status = Status.CLOSED
