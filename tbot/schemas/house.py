from typing import Optional, Tuple, Union

from pydantic import BaseModel

from .area import Area, BaseArea, BaseInDBArea


class BaseHouse(BaseModel):
    number: Optional[int] = None
    street: Optional[str] = None
    area: Optional[BaseArea] = None

    @classmethod
    def from_string(cls, string: str) -> Tuple[Union[dict], bool]:
        """ Create House object from string formatted like '{number: int}_{street: str}_{area: str}'

        :param string: The string formatted {number:int}_{street:str}_{area:str}
        """
        splited = string.split('_')
        if len(splited) < 3:
            return {
                "error_msg": "Payload must formatted like <i>{number:int}_{street:str}_{area:str}</i>. But your payload has less then 2 `_`"
            }, False
        else:
            if (splited[0].isalnum() and splited[1].isalpha() and splited[2].isalpha()):
                return cls(number=int(splited[0]), street=splited[1],
                           area=splited[2]), True
            else:
                return {
                    "error_msg": "Payload must formatted like <i>{number:int}_{street:str}_{area:str}</i>. But your payload does not match typing or some field is not specified"
                }, False

    def __eq__(self, obj):
        return (self.street == obj.street and self.number == obj.number and self.area == obj.area)

    def __repr__(self):
        return "<House number=%s, street='%s', area='%s'>"\
            % (self.number, self.street, self.area)

    def __str__(self):
        return "st. %s, %s, %s area" % (self.street, self.number, self.area)


class BaseInDBHouse(BaseHouse):
    id: Optional[int] = None
    area: Optional[BaseInDBArea] = None

    class Config:
        orm_mode = True

    def to_base(self):
        return BaseHouse(**self.dict())

    def __eq__(self, obj):
        return super().__eq__(obj) and self.id == obj.id

    def __repr__(self):
        return "<House id=%s, number=%s, street='%s', area='%s'>"\
            % (self.id, self.number, self.street, self.area)


# return via api
class House(BaseInDBHouse):
    area: Optional[Area] = None
