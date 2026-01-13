from dataclasses import dataclass
from datetime import datetime, timezone


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Comment:
    id: str
    author_id: str
    content: str

    created_at: datetime = _now_utc()

    def __post_init__(self):
        if not self.content or not self.content.strip():
            raise ValueError("Le commentaire ne peut pas être vide")
        if not self.author_id:
            raise ValueError("Un commentaire doit avoir un auteur")
