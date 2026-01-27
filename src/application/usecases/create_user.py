import uuid

from src.domain.user import User
from src.ports.user_repository import UserRepository


class CreateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(
        self, username: str, is_agent: bool = False, is_admin: bool = False
    ) -> User:
        if self.user_repo.find_by_username(username):
            raise ValueError(f"Username '{username}' already exists")

        user = User(
            id=str(uuid.uuid4()),
            username=username,
            is_agent=is_agent,
            is_admin=is_admin,
        )
        self.user_repo.save(user)
        return user
