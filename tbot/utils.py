from contextlib import contextmanager
from typing import Optional, List

from tbot import schemas
from tbot.db import Session
from tbot.models import User, House, Event


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:  # noqa E722
        session.rollback()
        raise
    finally:
        session.close()


def save_or_update_user(user: schemas.User) -> None:
    with session_scope() as session:
        if session.query(User).filter_by(id=user.id).first() is None:
            save_user(user)
        else:
            update_user(user)


def save_user(user: schemas.User) -> None:
    with session_scope() as session:
        obj = User.from_schemas(user)
        session.add(obj)


def update_user(user: schemas.User) -> None:
    with session_scope() as session:
        obj = session.query(User).filter_by(id=user.id).first()
        obj.update_from_schema(user)
        session.add(obj)


def get_user(user_id: int) -> Optional[schemas.User]:
    with session_scope() as session:
        user = session.query(User).filter_by(id=user_id).first()
        if user is None:
            return None
        return schemas.User.from_orm(user)


def list_relevant_users_for_event(event: Event = None) -> List[schemas.User]:
    target = schemas.EventTarget.ALL
    if event:
        target = event.target

    with session_scope() as session:
        users = []
        if target == schemas.EventTarget.ALL:
            users = session.query(User).all()

        elif target == schemas.EventTarget.AREA:
            for house in session.query(House).filter_by(
                    area=event.area):
                users.extend(house.users)  # TODO: use sql query

        elif target == schemas.EventTarget.HOUSE:
            for house in session.query(House).filter_by(
                    id=event.house_id):
                users.extend(house.users)  # TODO: use sql query

        return [schemas.User.from_orm(user) for user in users]


def list_house() -> List[schemas.House]:
    with session_scope() as session:
        return [schemas.House.from_orm(house)
                for house in session.query(House).all()]


def list_event() -> List[schemas.Event]:
    with session_scope() as session:
        return [schemas.Event.from_orm(event)
                for event in session.query(Event).all()]


def create_event(event: schemas.EventCreate) -> schemas.Event:
    with session_scope() as session:
        obj = Event(**event.dict())
        session.add(obj)
        session.flush()
        return schemas.Event.from_orm(obj)


def update_event(event: schemas.EventUpdate) -> schemas.Event:
    with session_scope() as session:
        obj = session.query(Event).filter_by(id=event.id).first()
        for key, value in event.dict().items():
            if value is not None:
                setattr(obj, key, value)
        return schemas.Event.from_orm(obj)


def delete_event(id: int):
    with session_scope() as session:
        obj = session.query(Event).filter_by(id=id).first()
        session.delete(obj)
