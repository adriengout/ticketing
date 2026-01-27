from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

from src.domain.comment import Comment
from src.domain.exceptions import (
    InvalidTicketStateError,
    TicketNotAssignedError,
    WrongAgentError,
)
from src.domain.priority import Priority
from src.domain.status import Status


def _now_utc() -> datetime:
    """Retourne l'heure actuelle en UTC."""
    return datetime.now(timezone.utc)


@dataclass
class Ticket:
    id: str
    title: str
    description: str
    creator_id: str

    status: Status = Status.OPEN
    priority: Priority = Priority.MEDIUM

    comments: list[Comment] = field(default_factory=list)

    created_at: datetime = field(default_factory=_now_utc)
    updated_at: datetime = field(default_factory=_now_utc)

    assignee_id: Optional[str] = None
    closed_at: Optional[datetime] = None
    started_at: Optional[datetime] = None

    # Constante métier pour la réouverture
    REOPEN_DEADLINE_DAYS: int = 7

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("Le titre du ticket ne peut pas être vide")
        if not self.creator_id:
            raise ValueError("Un ticket doit avoir un créateur")

    def verif_status(self, asked_status: Status) -> bool:
        """Définit les transitions d'états autorisées."""
        transitions_autorisee = {
            Status.OPEN: {Status.IN_PROGRESS},
            Status.IN_PROGRESS: {Status.RESOLVED},
            Status.RESOLVED: {Status.CLOSED, Status.IN_PROGRESS},
            Status.CLOSED: {Status.IN_PROGRESS},  # Autorise la réouverture
        }
        return asked_status in transitions_autorisee.get(self.status, set())

    def assign(self, user_id: str):
        """Assigne un agent au ticket."""
        if not user_id:
            raise ValueError("L'identifiant de l'agent ne peut pas être vide")

        # Règle : impossible d'assigner si le ticket est CLOSED
        if self.status == Status.CLOSED:
            raise ValueError("Impossible de faire cette transition de statut")

        self.assignee_id = user_id
        self.updated_at = _now_utc()

    def start(self, agent_id: str, started_at: datetime):
        """Démarre le traitement du ticket."""
        if self.assignee_id is None:
            raise TicketNotAssignedError(
                "Le ticket doit être assigné avant de démarrer"
            )
        if self.assignee_id != agent_id:
            raise WrongAgentError("Seul l'agent assigné peut démarrer le ticket")
        if self.status != Status.OPEN:
            raise InvalidTicketStateError(
                f"Le ticket doit être OPEN (actuel: {self.status.value})"
            )

        self.status = Status.IN_PROGRESS
        self.started_at = started_at
        self.updated_at = started_at

    def resolve(self):
        """Passe le ticket en résolu."""
        if not self.verif_status(Status.RESOLVED):
            raise ValueError("Impossible de résoudre ce ticket")
        self.status = Status.RESOLVED
        self.updated_at = _now_utc()

    def close(self):
        """Ferme définitivement le ticket."""
        if not self.verif_status(Status.CLOSED):
            raise ValueError("Impossible de fermer le ticket")
        self.status = Status.CLOSED
        self.closed_at = _now_utc()
        self.updated_at = _now_utc()

    def set_priority(self, priority: Priority):
        """Change la priorité du ticket (interdit si fermé)."""
        if self.status == Status.CLOSED:
            raise ValueError("Impossible de changer la priorité d'un ticket fermé")
        self.priority = priority
        self.updated_at = _now_utc()

    def add_comment(self, comment: Comment):
        """Ajoute un commentaire (interdit si fermé)."""
        if self.status == Status.CLOSED:
            raise ValueError("Impossible de commenter un ticket fermé")
        self.comments.append(comment)
        self.updated_at = _now_utc()

    def can_be_reopened(self, current_time: datetime) -> bool:
        """Vérifie la règle des 7 jours pour la réouverture."""
        if self.status != Status.CLOSED or self.closed_at is None:
            return False
        return (current_time - self.closed_at) <= timedelta(
            days=self.REOPEN_DEADLINE_DAYS
        )

    def reopen(self, current_time: datetime):
        """Réouvre un ticket fermé dans le délai imparti."""
        if not self.can_be_reopened(current_time):
            raise InvalidTicketStateError(
                "Impossible de rouvrir le ticket : délai dépassé ou état invalide"
            )

        self.status = Status.IN_PROGRESS
        self.closed_at = None
        self.updated_at = current_time
