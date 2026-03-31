"""
Adaptateur API REST pour les tickets.

Ce module définit les routes HTTP pour manipuler les tickets.
C'est un adaptateur "primaire" (ou "driving") : il reçoit les requêtes
de l'extérieur et appelle les cas d'usage de l'application.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/tickets", tags=["tickets"])


class TicketIn(BaseModel):
    """
    Schéma d'entrée pour la création d'un ticket.

    Attributes:
        title: Titre du ticket
        description: Description détaillée du problème
    """

    title: str
    description: str
    creator_id: str


class TicketOut(BaseModel):
    """
    Schéma de sortie pour un ticket.

    Attributes:
        id: Identifiant unique du ticket
        title: Titre du ticket
        description: Description du problème
        status: Statut actuel (open, in_progress, resolved, closed)
    """

    id: str
    title: str
    description: str
    status: str


# Import de la factory du cas d'usage depuis la racine de composition
# Ceci évite les imports circulaires et garde l'injection de dépendances propre
def get_create_ticket_usecase():
    """
    Factory pour obtenir le cas d'usage CreateTicket.

    Cette fonction sera surchargée par la vraie factory dans main.py
    via app.dependency_overrides ou un pattern d'import direct.
    """
    from src.main import get_create_ticket_usecase as factory

    return factory()


@router.post("/", status_code=201, response_model=TicketOut)
async def create_ticket(
    ticket_data: TicketIn,
    # TODO: Ajouter creator_id depuis le contexte d'authentification
):
    """
    Crée un nouveau ticket.

    Args:
        payload: Les données du ticket à créer

    Returns:
        Le ticket créé avec son identifiant et son statut
    """
    # Exemple de câblage (les étudiants complèteront ceci) :
    # usecase = get_create_ticket_usecase()
    # ticket = usecase.execute(
    #     payload.title, payload.description, creator_id="anonymous"
    # )
    # return TicketOut(
    #     id=ticket.id, title=ticket.title,
    #     description=ticket.description, status=ticket.status.value
    # )

    from src.main import get_create_ticket_usecase

    usecase = get_create_ticket_usecase()

    # 2. Appeler le use case
    ticket = usecase.execute(
        title=ticket_data.title,
        description=ticket_data.description,
        creator_id=ticket_data.creator_id,
    )

    # 3. Convertir l'entité domaine en schéma API
    return TicketOut(
        id=ticket.id,
        title=ticket.title,
        description=ticket.description,
        status=ticket.status.value,  # Enum → string
    )


@router.get("/", response_model=list[TicketOut])
async def list_tickets():
    from src.main import get_list_tickets_usecase

    usecase = get_list_tickets_usecase()
    tickets = usecase.execute()

    return [
        TicketOut(
            id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            status=ticket.status.value,
        )
        for ticket in tickets
    ]


class AssignmentIn(BaseModel):
    agent_id: str


class StartTicketIn(BaseModel):
    agent_id: str


# --- Nouvelles Routes PATCH ---
@router.patch("/{ticket_id}/assign", response_model=TicketOut)
async def assign_ticket(ticket_id: str, assignment: AssignmentIn):
    from src.domain.exceptions import TicketNotFoundError
    from src.main import get_assign_ticket_usecase

    try:
        usecase = get_assign_ticket_usecase()
        ticket = usecase.execute(ticket_id=ticket_id, agent_id=assignment.agent_id)

        return TicketOut(
            id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            status=ticket.status.value,
        )
    except TicketNotFoundError:
        raise HTTPException(status_code=404, detail="Ticket not found") from None
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.patch("/{ticket_id}/start", response_model=TicketOut)
async def start_ticket(ticket_id: str, data: StartTicketIn):
    # 1. Assure-toi d'importer toutes les exceptions nécessaires
    from src.domain.exceptions import (
        TicketNotAssignedError,
        TicketNotFoundError,
        WrongAgentError,
    )
    from src.main import get_start_ticket_usecase

    try:
        usecase = get_start_ticket_usecase()
        ticket = usecase.execute(ticket_id=ticket_id, agent_id=data.agent_id)

        return TicketOut(
            id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            status=ticket.status.value,
        )
    except TicketNotFoundError:
        raise HTTPException(status_code=404, detail="Ticket not found") from None

    except (TicketNotAssignedError, WrongAgentError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
