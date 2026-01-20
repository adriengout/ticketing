from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from src.domain.comment import Comment
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
        if not user_id:
            raise ValueError("L'identifiant de l'agent ne peut pas être vide")
        if not self.verif_status(Status.IN_PROGRESS):
            raise ValueError("Impossible de faire cette transition de statut")

        self.assignee_id = user_id
        self.updated_at = _now_utc()

    def resolve(self):
        if not self.verif_status(Status.RESOLVED):
            raise ValueError("Impossible de résoudre ce ticket")
        self.status = Status.RESOLVED
        self.updated_at = _now_utc()

    def close(self):
        if not self.verif_status(Status.CLOSED):
            raise ValueError("Impossible de fermer le ticket")

        self.status = Status.CLOSED
        self.closed_at = _now_utc()
        self.updated_at = _now_utc()

    def set_priority(self, priority: Priority):
        """Change la priorité du ticket."""
        if self.status == Status.CLOSED:
            raise ValueError("Impossible de changer la priorité d'un ticket fermé")

        self.priority = priority
        self.updated_at = _now_utc()

    def add_comment(self, comment: Comment):
        """Ajoute un commentaire au ticket."""
        if self.status == Status.CLOSED:
            raise ValueError("Impossible de commenter un ticket fermé")

        self.comments.append(comment)
        self.updated_at = _now_utc()
