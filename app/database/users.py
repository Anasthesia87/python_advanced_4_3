from collections.abc import Iterable

from select import select

from .engine import engine
from sqlmodel import Session



from app.models.User import UserData


def get_user(user_id: int) -> UserData | None:
    with Session(engine) as session:
        session.get(UserData, user_id)
        pass

def get_users() -> Iterable[UserData]:
    with Session(engine) as session:
        statement = select(UserData)
        return session.exec(statement).all()


