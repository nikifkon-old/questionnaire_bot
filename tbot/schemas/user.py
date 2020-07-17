from typing import Optional

from pydantic import BaseModel

from .house import (BaseHouse, BaseInDBHouse, House)


class BaseUser(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    house: Optional[BaseHouse] = None
    flat: Optional[int] = None

    def __eq__(self, obj):
        return (self.name == obj.name and self.phone == obj.phone and self.house == obj.house and self.flat == obj.flat)

    def __repr__(self):
        return "<User name='%s', phone='%s', house=%s, flat=%s>"\
            % (self.name, self.phone, repr(self.house), self.flat)

    def __str__(self):
        return "Name: %s\nphone: %s\nhouse: %s\nflat: %s"\
            % (self.name, self.phone, str(self.house), self.flat)


class BaseInDBUser(BaseUser):
    id: Optional[int] = None
    house: Optional[BaseInDBHouse] = None

    class Config:
        orm_mode = True

    def to_base(self):
        return BaseUser(**self.dict())

    def __repr__(self):
        return "<User id=%s name='%s', phone='%s', house=%s, flat=%s>"\
            % (self.id, self.name, self.phone, repr(self.house), self.flat)

    def __eq__(self, obj):
        return super().__eq__(obj) and self.id == obj.id


# return via api
class User(BaseInDBUser):
    house: Optional[House] = None
