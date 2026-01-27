import pytest

from src.adapters.db.database import init_database
from src.adapters.db.ticket_repository_sqlite import SQLiteTicketRepository


@pytest.fixture
def sqlite_ticket_repo(tmp_path):
    """Fixture qui crée une base SQLite temporaire pour chaque test."""
    # Création d'un chemin temporaire pour la DB (évite de polluer ton projet)
    db_path = tmp_path / "test_ticketing.db"

    # Initialisation du schéma (CREATE TABLE)
    init_database(str(db_path))

    # Retourne le repository configuré sur cette DB
    return SQLiteTicketRepository(str(db_path))


@pytest.fixture
def sqlite_user_repo(tmp_path):
    from src.adapters.db.database import init_database
    from src.adapters.db.user_repository_sqlite import SQLiteUserRepository

    db_path = tmp_path / "test_users.db"
    init_database(str(db_path))
    return SQLiteUserRepository(str(db_path))
