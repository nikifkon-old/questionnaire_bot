from datetime import datetime

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from tbot.models import Event, House
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
def create_house(session):
    data = {
        "street": "Ленинская",
        "number": 100,
        "area": "Ленинский"
    }
    house = House(**data)
    session.add(house)
    return house


@pytest.fixture
def create_event(session, create_house):
    data = {
        "title": "Горячая вода будет отключена",
        "type": "Scheduled works",
        "start": datetime(2020, 6, 30, 12),
        "end": datetime(2020, 6, 30, 15),
        "description": "В связи с заменой труб, водоснобжение в доме номер. 100 на улице Ленинкая будет недоступно 30.06 в период с 12:00 до 15:00.\nПриносим свои извенения за предостваленные неудабства.",  # noqa
        "house_id": create_house.id,
        "area": None,
        "target": "house"
    }
    event = Event(**data)
    session.add(event)
    return event


@pytest.fixture
def user_data(create_house):
    return {
        "name": "Иван",
        "phone": "+12345678901",
        "house_id": create_house.id,
        "flat": 99
    }
