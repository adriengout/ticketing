# src/adapters/db/ticket_repository_sqlite.py
from typing import Optional

from src.adapters.db.database import close_connection, get_connection
from src.adapters.db.mappers import row_to_ticket, ticket_to_row
from src.domain.ticket import Ticket
from src.ports.ticket_repository import TicketRepository


class SQLiteTicketRepository(TicketRepository):
    def __init__(self, db_path: str = "ticketing.db"):
        self.db_path = db_path

    def save(self, ticket: Ticket) -> Ticket:
        """Sauvegarde ou met à jour un ticket dans la base SQLite."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        # Conversion de l'entité en dictionnaire via le mapper fourni
        row = ticket_to_row(ticket)

        cursor.execute(
            """
            INSERT OR REPLACE INTO tickets 
            (id, title, description, creator_id, status, priority, 
             assignee_id, project_id, created_at, updated_at, started_at, closed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                row["id"],
                row["title"],
                row["description"],
                row["creator_id"],
                row["status"],
                row["priority"],
                row["assignee_id"],
                row["project_id"],
                row["created_at"],
                row["updated_at"],
                row["started_at"],
                row["closed_at"],
            ),
        )

        conn.commit()
        close_connection(conn)
        return ticket

    def get(self, ticket_id: str) -> Optional[Ticket]:
        """
        Récupère un ticket par son ID.
        Cette méthode est requise par l'interface TicketRepository.
        """
        return self.get_by_id(ticket_id)

    def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """Récupère un ticket par son ID via une requête SQL."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
        row = cursor.fetchone()
        close_connection(conn)

        if row is None:
            return None

        # Conversion de la ligne SQLite vers l'entité Domaine via le mapper
        return row_to_ticket(dict(row))

    def list_all(self) -> list[Ticket]:
        """Récupère tous les tickets de la base."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tickets")
        rows = cursor.fetchall()
        close_connection(conn)

        return [row_to_ticket(dict(row)) for row in rows]
