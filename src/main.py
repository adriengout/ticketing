"""
Racine de composition (Composition Root).

Ce fichier est le point d'entrée de l'application. C'est ici que :
- Les adaptateurs concrets sont instanciés
- Les dépendances sont injectées dans les cas d'usage
- L'application FastAPI est configurée avec ses routes

La règle d'or : seul ce fichier connaît les implémentations concrètes.
Les cas d'usage ne voient que les interfaces (ports).
"""

from fastapi import FastAPI

from src.adapters.api.ticket_router import router as ticket_api
from src.adapters.api.user_routeur import router as user_api
from src.adapters.db.ticket_repository_sqlite import SQLiteTicketRepository
from src.adapters.db.user_repository_inmemory import InMemoryUserRepository
from src.application.usecases.create_ticket import CreateTicketUseCase
from src.application.usecases.create_user import CreateUserUseCase
from src.application.usecases.list_tickets import ListTicketsUseCase
from src.application.usecases.list_user import ListUsersUseCase

# 1. Initialisation de l'app
app = FastAPI(title="Ticketing Starter")

# 2. Initialisation des Adaptateurs (Repositories)
ticket_repository = SQLiteTicketRepository("ticketing.db")
user_repository = InMemoryUserRepository()


# 3. Factories pour les cas d'usage (utilisées par les routeurs)
def get_create_ticket_usecase() -> CreateTicketUseCase:
    return CreateTicketUseCase(ticket_repository)


def get_list_tickets_usecase() -> ListTicketsUseCase:
    return ListTicketsUseCase(ticket_repository)


def get_create_user_usecase() -> CreateUserUseCase:
    return CreateUserUseCase(user_repository)


def get_list_users_usecase():
    return ListUsersUseCase(user_repository)


# On utilise directement les variables importées car ce sont déjà les objets router
app.include_router(ticket_api)
app.include_router(user_api)


# TODO: Ajouter d'autres factories de cas d'usage au fur et à mesure
# def get_assign_ticket_usecase() -> AssignTicketUseCase:
#     return AssignTicketUseCase(ticket_repository)

# --- Routes ---
app.include_router(ticket_api)


@app.get("/")
def root():
    """Route racine pour vérifier que l'API fonctionne."""
    return {"status": "ok"}
