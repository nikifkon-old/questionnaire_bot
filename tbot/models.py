from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from tbot import schemas
from tbot.db import Base


class House(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    street = Column(String)
    area = Column(String)
    users = relationship("User", back_populates="house")

    @classmethod
    def from_schemas(cls, schema: schemas.House):
        kwargs = schema.dict()
        return cls(**kwargs)

    def update_from_schema(self, schema: schemas.House):
        for key, value in schema.dict().items():
            setattr(self, key, value)

    def __eq__(self, obj):
        return (self.id == obj.id
                and self.street == obj.street
                and self.number == obj.number
                and self.area == obj.area)

    def __repr__(self):
        return "<House number=%s, street='%s', area='%s'>" % (self.number,
                                                              self.street,
                                                              self.area)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    house_id = Column(Integer, ForeignKey("houses.id"))
    house = relationship("House", back_populates="users")
    flat = Column(Integer)

    @classmethod
    def from_schemas(cls, schema: schemas.User):
        kwargs = schema.dict()
        house_kwargs = kwargs.pop("house", None)
        house = House(**house_kwargs)
        return cls(house=house, **kwargs)

    def update_from_schema(self, schema: schemas.User):
        for key, value in schema.dict().items():
            if key == "house":
                if value["id"] is not None:
                    self.house.update_from_schema(schemas.House(**value))
                else:
                    self.hosue = None
                    self.house_id = None
                continue
            setattr(self, key, value)

    def __eq__(self, obj):
        return (self.id == obj.id
                and self.name == obj.name
                and self.phone == obj.phone
                and self.house == obj.house
                and self.flat == obj.flat)

    def __repr__(self):
        return "<User id=%s name='%s', phone='%s', house=%s, flat=%s>"\
            % (self.id, self.name, self.phone, repr(self.house), self.flat)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    type = Column(String)
    description = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    house_id = Column(Integer, ForeignKey("houses.id"))
    area = Column(String)
    target = Column(String)
    messages = relationship("Message", back_populates="event")

    @classmethod
    def from_schemas(cls, schema: schemas.Event):
        kwargs = schema.dict()
        return cls(**kwargs)

    def __eq__(self, obj):
        return (self.id == obj.id
                and self.title == obj.title
                and self.type == obj.type
                and self.description == obj.description
                and self.start == obj.start
                and self.end == obj.end
                and self.house_id == obj.house_id
                and self.area == obj.area
                and self.target == obj.target)

    def __repr__(self):
        return "<Event id=%s, title=%s, description=%s, start=%s, end=%s, house_id=%s, area=%s, target=%s"\
            % (self.id, self.title, self.description, self.start, self.end,
               self.house_id, self.area, self.target)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    event = relationship("Event", back_populates="messages")

    def __eq__(self, obj):
        return (self.id == obj.id
                and self.chat_id == obj.chat_id
                and self.event_id == obj.event_id)

    def __repr__(self):
        return "<Message id=%s, chat_id=%s, event_id=%s>"\
            % (self.id, self.chat_id, self.event_id)
