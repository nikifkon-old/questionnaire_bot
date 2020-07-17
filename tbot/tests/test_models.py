from tbot import schemas
from tbot.models import User


def merge(d1, d2):
    c = d1.copy()
    for key, value in d2.items():
        if isinstance(value, dict):
            c[key] = merge(d1[key], value)
        else:
            c[key] = d2[key]
    return c


def test_str(create_event):
    expected = """
Горячая вода будет отключена - Scheduled work
2020-06-30 12:00:00 - 2020-06-30 15:00:00
В связи с заменой труб, водоснобжение в доме номер. 100 на улице Ленинкая будет недоступно 30.06 в период с 12:00 до 15:00.
Приносим свои извенения за предостваленные неудабства.
house
"""
    assert expected == create_event.post


def test_from_schema(session, user_data):
    init_base_schema = schemas.BaseUser(**user_data)
    user = User.from_schema(init_base_schema)
    session.add(user)
    session.commit()

    result_schema = schemas.User.from_orm(user)
    assert init_base_schema == result_schema.to_base()


def test_update_from_schema(session, create_user):
    old_data = schemas.User.from_orm(create_user).dict()

    new_data = {
        "id": create_user.id,
        "name": "new name",
        "house": {
            "area": {
                "name": "new area"
            }
        }
    }
    data = merge(old_data, new_data)
    new_data_schema = schemas.User(**new_data)
    create_user.update_from_schema(new_data_schema)
    session.add(create_user)
    session.commit()

    assert schemas.User(**data) == schemas.User.from_orm(create_user)
