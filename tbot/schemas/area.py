from typing import Optional

from pydantic import BaseModel


class BaseArea(BaseModel):
    name: Optional[str] = None

    def __eq__(self, obj):
        return self.name == obj.name

    def __repr__(self):
        return "<Area name=%s>" % (self.number,)

    def __str__(self):
        return self.name


class BaseInDBArea(BaseArea):
    id: Optional[int] = None

    class Config:
        orm_mode = True

    def to_base(self):
        return BaseArea(**self.dict())

    def __eq__(self, obj):
        return super().__eq__(obj) and self.id == obj.id

    def __repr__(self):
        return "<Area id=%s, name=%s>" % (self.id, self.name,)


# return via api
class Area(BaseInDBArea):
    pass
