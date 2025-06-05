from collections.abc import Iterable
from http import HTTPStatus

from fastapi import HTTPException, APIRouter

# from app.database import users_list
from app.database import users
from app.models.User import UserData


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
def get_users() -> Iterable[UserData]:
    return users.get_users()