from typing import Iterable, Type
from http import HTTPStatus
from fastapi import HTTPException, APIRouter
from app.database import users
from app.models.User import UserData, UserDataCreateBody, UserDataUpdateBody



from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.engine import get_session, engine
from app.database.users import get_users

router = APIRouter(prefix="/api/users")


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> UserData:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    user = users.get_user(user_id)

    # if user is None:
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@router.get("/", status_code=HTTPStatus.OK)
def get_users(session: Session = Depends(get_session)):
    return users.get_users(session)  # <- session передается явно


@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(user: UserData) -> UserData:
    UserDataCreateBody.model_validate(user.model_dump())
    return users.create_user(user)


@router.patch("/{user_id}", response_model=None)
def update_user(user_id: int, user_data: UserData):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalide user")
    UserDataUpdateBody.model_validate(user_data.model_dump())
    return users.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Incorrect user")
    users.delete_user(user_id)
    return {"message": "User deleted"}
