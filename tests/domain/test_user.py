import pytest

from src.domain.user import User


def test_create_user_nominal():
    user = User(id="u1", username="alice", is_agent=True)
    assert user.username == "alice"
    assert user.is_agent is True
    assert user.is_admin is False  # Valeur par défaut


def test_create_user_empty_username():
    with pytest.raises(ValueError, match="Username cannot be empty"):
        User(id="u1", username="", is_agent=False)
