from typing import Optional

from src.domain.user import User
from src.ports.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users: dict[str, User] = {}

    def save(self, user: User) -> User:
        self._users[user.id] = user
        return user

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def find_by_username(self, username: str) -> Optional[User]:
        return next((u for u in self._users.values() if u.username == username), None)

    def list_all(self) -> list[User]:
        return list(self._users.values())
