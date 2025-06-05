from http import HTTPStatus

from fastapi import APIRouter

from app.database.engine import check_availability
# from app.database import users_list
from app.models.AppStatus import AppStatus
# from tests.test_smoke import users

router = APIRouter()


@router.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    # return AppStatus(users=bool(users_list))
    return AppStatus(database=check_availability())