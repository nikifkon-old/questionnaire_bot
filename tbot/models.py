from typing import Generic, TypeVar, Type

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import relationship

from tbot import schemas
from tbot.db import Base


SchemaType = TypeVar("SchemaType")


class SchemasMixin(Generic[SchemaType]):
    @classmethod
    def from_schema(cls, schema: Type[SchemaType]):
        kwargs = schema.dict()
        for name, property_ in inspect(cls).relationships.items():
            if name in schema.__fields__:
                child_schema = getattr(schema, name)
                if child_schema is not None:
                    instance = property_.mapper.class_.from_schema(
                        child_schema)
                    kwargs[name] = instance
                else:
                    kwargs[name] = None
        return cls(**kwargs)

    def update_from_schema(self, schema: Type[SchemaType]):
        kwargs = schema.dict()
        for name, property_ in inspect(self.__class__).relationships.items():
            if name in schema.__fields__:
                child_schema = getattr(schema, name)
                if child_schema is not None:
                    getattr(self, name).update_from_schema(child_schema)
                    kwargs.pop(name)
                else:
                    kwargs[name] = None
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)


class Area(Base, SchemasMixin[schemas.Area]):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    houses = relationship("House", back_populates="area")
    events = relationship("Event", back_populates="area")

    def __str__(self):
        return self.name


class House(Base, SchemasMixin[schemas.House]):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    street = Column(String)
    area_id = Column(Integer, ForeignKey("areas.id"))
    area = relationship("Area", back_populates="houses")
    users = relationship("User", back_populates="house")
    events = relationship("Event")

    def __repr__(self):
        return "<House id=%s, number=%s, street='%s', area='%s'>" % (self.id,
                                                                     self.number,
                                                                     self.street,
                                                                     self.area)

    def __str__(self):
        return f"{self.street} st. {self.number}"


class User(Base, SchemasMixin[schemas.User]):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    house_id = Column(Integer, ForeignKey("houses.id"))
    house = relationship("House", back_populates="users")
    flat = Column(Integer)

    def __repr__(self):
        return "<User id=%s name='%s', phone='%s', house=%s, flat=%s>"\
            % (self.id, self.name, self.phone, repr(self.house), self.flat)

    def __str__(self):
        return self.name or self.id


class Event(Base, SchemasMixin[schemas.Event]):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    type = Column(String)
    description = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    house_id = Column(Integer, ForeignKey("houses.id"))
    house = relationship("House", back_populates="events")
    area_id = Column(Integer, ForeignKey("areas.id"))
    area = relationship("Area", back_populates="events")
    target = Column(String)
    messages = relationship("Message", back_populates="event")

    @property
    def post(self):
        return f"""
{self.title} - {self.type}
{self.start} - {self.end}
{self.description}
{self.target}
"""

    def __repr__(self):
        return "<Event id=%s, title=%s, description=%s, start=%s, end=%s, house_id=%s, area=%s, target=%s"\
            % (self.id, self.title, self.description, self.start, self.end,
               self.house_id, self.area, self.target)

    def __str__(self):
        return f"{self.title} - {self.type}"


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    event = relationship("Event", back_populates="messages")

    def __repr__(self):
        return "<Message id=%s, chat_id=%s, event_id=%s>"\
            % (self.id, self.chat_id, self.event_id)

    def __str__(self):
        return f"{self.chat_id} - {self.event}"


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    login = Column(String(80), unique=True)
    email = Column(String(120))
    password = Column(String(94))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __str__(self):
        return self.username
