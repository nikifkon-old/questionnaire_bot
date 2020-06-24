from tbot.datatypes import House, User


class TestHouse:
    def test_from_string(self):
        string = "123_street_area"
        house = House.from_string(string)
        assert house.number == 123
        assert house.street == "street"
        assert house.area == "area"

    def test_from_turple(self):
        trp = (1, "street", 123, "area")
        house = House.from_turple(trp)
        assert house.id == 1
        assert house.street == "street"
        assert house.number == 123
        assert house.area == "area"

    def test_eq(self, house):
        assert house == house

    def test_repr(self, house):
        repr(house)

    def test_str(self, house):
        str(house)


class TestUser:
    def test_from_turple(self, house):
        trp = (1, "John", "+123445679", house.id, None)
        user = User.from_turple(trp)
        assert user.id == 1
        assert user.name == "John"
        assert user.phone == "+123445679"
        assert user.house.id == house.id
        assert user.flat is None

    def test_eq(self, user):
        assert user == user

    def test_repr(self, user):
        repr(user)

    def test_str(self, user):
        str(user)

    def test_repr__blank_flat(self, user):
        user.flat = None
        repr(user)

    def test_str__blank_flat(self, user):
        user.flat = None
        str(user)
