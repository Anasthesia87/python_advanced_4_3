
from typing import Iterable, Type
from fastapi import HTTPException
from .engine import engine
from app.models.User import UserData
from sqlmodel import Session, select



def get_user(user_id: int) -> UserData | None:
    with Session(engine) as session:
        return session.get(UserData, user_id)


def get_users(session: Session):
    stmt = select(UserData)
    result = session.exec(stmt)
    return result.all()


def create_user(user: UserData) -> UserData:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def update_user_put(user_id: int, user: UserData) -> Type[UserData]:
    with Session as session:
        db_user = session.get(UserData, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def update_user_patch(user_id: int, user: UserData) -> Type[UserData]:
    with Session as session:
        db_user = session.get(UserData, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(UserData, user_id)
        session.delete(user)
        session.commit()




