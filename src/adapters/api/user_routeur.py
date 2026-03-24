from typing import list

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["users"])


class UserIn(BaseModel):
    username: str
    is_agent: bool = False
    is_admin: bool = False


class UserOut(BaseModel):
    id: str
    username: str
    is_agent: bool
    is_admin: bool


@router.post("/", status_code=201, response_model=UserOut)
async def create_user(payload: UserIn):
    from src.main import get_create_user_usecase

    usecase = get_create_user_usecase()

    user = usecase.execute(
        username=payload.username, is_agent=payload.is_agent, is_admin=payload.is_admin
    )

    return UserOut(
        id=user.id,
        username=user.username,
        is_agent=user.is_agent,
        is_admin=user.is_admin,
    )


@router.get("/", response_model=list[UserOut])
async def list_users():
    from src.main import get_list_users_usecase

    usecase = get_list_users_usecase()
    users = usecase.execute()

    return [
        UserOut(id=u.id, username=u.username, is_agent=u.is_agent, is_admin=u.is_admin)
        for u in users
    ]
