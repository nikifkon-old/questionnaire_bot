class House:
    def __init__(self, number: int = None, street: str = None,
                 area: str = None, id: int = None):
        self.id = id
        self.number = number
        self.street = street
        self.area = area

    @classmethod
    def from_string(cls, string: str):
        """ Create Hosue object from string format like '{number}_{street}_{area}'
        """
        splited = string.split('_')
        if len(splited) < 3:
            print("missed required parametrs")
        else:
            if (splited[0].isalnum()
                and splited[1].isalpha()
                    and splited[2].isalpha()):

                return cls(number=int(splited[0]), street=splited[1],
                           area=splited[2])
            else:
                print("wrong types")

    @classmethod
    def from_turple(cls, row: tuple):
        data = {
            "id": row[0],
            "street": row[1],
            "number": row[2],
            "area": row[3]
        }
        return cls(**data)

    def __eq__(self, obj):
        return (self.id == obj.id
                and self.street == obj.street
                and self.number == obj.number
                and self.area == obj.area)

    def __repr__(self):
        return "<House number=%s, street='%s', area='%s'>" % (self.number,
                                                              self.street,
                                                              self.area)

    def __str__(self):
        return "st. %s, %s, %s area" % (self.street, self.number, self.area)


class User:
    def __init__(self, id: int, name: str = None, phone: str = None,
                 house: House = None, flat: int = None):
        self.id = id
        self.name = name
        self.phone = phone
        self.house = house
        self.flat = flat

    @classmethod
    def from_turple(cls, row: tuple):
        data = {
            "id": row[0],
            "name": row[1],
            "phone": row[2],
            "house": House(id=row[3]),
            "flat": row[4]
        }
        return cls(**data)

    def __eq__(self, obj):
        return (self.id == obj.id
                and self.name == obj.name
                and self.phone == obj.phone
                and self.house == obj.house
                and self.flat == obj.flat)

    def __repr__(self):
        return "<User id=%s name='%s', phone='%s', house=%s, flat=%s>"\
            % (self.id, self.name, self.phone, repr(self.house), self.flat)

    def __str__(self):
        return "name: %s\nphone: %s\nhouse: %s\nflat: %s"\
            % (self.name, self.phone, str(self.house), self.flat)
