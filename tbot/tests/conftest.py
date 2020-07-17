from datetime import datetime

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from tbot import schemas
from tbot.models import User, Event, House
from tbot.db import Base


@pytest.fixture
def engine():
    engine = create_engine("sqlite:///:memory:")
    return engine


@pytest.fixture
def session_class(engine):
    return sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def session(engine, session_class):
    from tbot.models import Event, House, User  # noqa import all models for auto create test database
    Base.metadata.create_all(engine)
    session = session_class()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def create_house_schema():
    data = {
        "street": "Ленинская",
        "number": 100,
        "area": {
            "name": "Ленинский"
        }
    }
    return schemas.House(**data)


@pytest.fixture
def create_house(session, create_house_schema):
    house = House.from_schema(create_house_schema)
    session.add(house)
    return house


@pytest.fixture
def create_event_schema(create_house_schema):
    data = {
        "title": "Горячая вода будет отключена",
        "type": schemas.EventType.SCHEDUELD_WORK,
        "start": datetime(2020, 6, 30, 12),
        "end": datetime(2020, 6, 30, 15),
        "description": "В связи с заменой труб, водоснобжение в доме номер. 100 на улице Ленинкая будет недоступно 30.06 в период с 12:00 до 15:00.\nПриносим свои извенения за предостваленные неудабства.",  # noqa
        "house": create_house_schema,
        "area": None,
        "target": schemas.EventTarget.HOUSE
    }
    return schemas.EventCreate(**data)


@pytest.fixture
def create_event(session, create_event_schema):
    event = Event.from_schema(create_event_schema)
    session.add(event)
    return event


@pytest.fixture
def user_data():
    return {
        "name": "test_name",
        "phone": "+123",
        "flat": 99,
        "house": {
            "street": "test_street",
            "area": {
                "name": "test_area"
            },
            "number": 123
        }
    }


@pytest.fixture
def create_user_schema(user_data):
    return schemas.User(**user_data)


@pytest.fixture
def create_user(session, create_user_schema):
    user = User.from_schema(create_user_schema)
    session.add(user)
    session.commit()
    return user
