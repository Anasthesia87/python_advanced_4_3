from collections.abc import Iterable

from select import select

from .engine import engine
from sqlmodel import Session

from ..models import User


def get_user(user_id: int) -> User | None:
    with Session(engine) as session:
        session.get(User, user_id)
        pass

def get_users() -> Iterable[User]:
    with Session(engine) as session:
        statement = select(User)
        return session.exec(statement).all()
