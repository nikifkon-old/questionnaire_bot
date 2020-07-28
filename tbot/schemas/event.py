from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator

from .area import Area, BaseArea, BaseInDBArea
from .house import BaseHouse, BaseInDBHouse, House


class EventType(str, Enum):
    EMERGENCY = "Emergency"
    SCHEDUELD_WORK = "Scheduled work"
    UNSCHEDUELD_WORK = "Unscheduled work"
    ADS = "Ads"


class EventTarget(str, Enum):
    ALL = "all"
    AREA = "area"
    HOUSE = "house"


class BaseEvent(BaseModel):
    title: Optional[str] = None
    type: Optional[EventType] = None
    description: Optional[str] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    target: Optional[EventTarget] = None
    house: Optional[BaseHouse] = None
    area: Optional[BaseArea] = None

    @validator("house")
    def house_required_if_target_for_house(cls, v, values, **kwargs):
        if v is None and values["target"] == EventTarget.HOUSE:
            raise ValueError("House field is required if you specify this target")
        return v

    @validator("area")
    def area_required_if_target_for_area(cls, v, values, **kwargs):
        if v is None and values["target"] == EventTarget.AREA:
            raise ValueError("Arae field is required if you specify this target")
        return v

    def __eq__(self, obj):
        return (self.title == obj.title and self.type == obj.type and self.description == obj.description and self.start == obj.start and self.end == obj.end and self.house == obj.house and self.area == obj.area and self.target == obj.target)

    def __repr__(self):
        return "<Event title=%s, description=%s, start=%s, end=%s, house=%s, area=%s, target=%s"\
            % (self.title, self.description, self.start, self.end,
               self.house, self.area, self.target)

    def __str__(self):
        return f"""
{self.title} - {self.type}
{self.start} - {self.end}
{self.description}
{self.target}
"""


class EventCreate(BaseEvent):
    title: str
    type: EventType
    description: str
    start: datetime
    target: EventTarget


class EventUpdate(BaseEvent):
    id: int


class BaseInDBEvent(BaseEvent):
    id: Optional[int] = None
    area: Optional[BaseInDBArea] = None
    house: Optional[BaseInDBHouse] = None

    class Config:
        orm_mode = True

    def to_base(self):
        return BaseEvent(**self.dict())

    def __eq__(self, obj):
        return super().__eq__(obj) and self.id == obj.id

    def __repr__(self):
        return "<Event id=%s, title=%s, description=%s, start=%s, end=%s, house=%s, area=%s, target=%s"\
            % (self.id, self.title, self.description, self.start, self.end,
               self.house, self.area, self.target)


class Event(BaseInDBEvent):
    area: Optional[Area] = None
    house: Optional[House] = None
