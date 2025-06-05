from http import HTTPStatus

from fastapi import HTTPException, APIRouter

from app.database import users_list
from app.models.User import UserData


router = APIRouter(prefix="/api/users")


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> UserData:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    if user_id > len(users_list):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users_list[user_id - 1]


@router.get("/", status_code=HTTPStatus.OK)
def get_users() -> list[UserData]:
    return users_list