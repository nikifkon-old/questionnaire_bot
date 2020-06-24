def test_save_user_info(db, user):
    db.save_user(user)


def _get_or_create_house(db, house):
    data, created = db._get_or_create_house(house)
    assert created is True
    data, created = db._get_or_create_house(house)
    assert created is False


def test_insert_user(db, user):
    house_id = 1
    db._insert_user(user, house_id)
    user_from_db, exist = db.get_user_if_exist(user.id)
    assert exist is True


def test_insert_user__blank_flat(db, user):
    user.flat = None
    house_id = 1
    db._insert_user(user, house_id)
    user_from_db, exist = db.get_user_if_exist(user.id)
    assert exist is True


def test_update_user(db, user):
    house_id = 1
    db._insert_user(user, house_id)
    user.name = "New name"
    user.phone = "New phone"
    user.flat = "New flat"
    db._update_user(user, house_id)
    user_from_db, exist = db.get_user_if_exist(user.id)
    assert exist is True


def test_update_user__blank_flat(db, user):
    house_id = 1
    db._insert_user(user, house_id)
    user.name = "New name"
    user.phone = "New phone"
    user.flat
    db._update_user(user, house_id)
    user_from_db, exist = db.get_user_if_exist(user.id)
    assert exist is True


def test_get_house_by_id(db, house):
    data, created = db._get_or_create_house(house)
    data2 = db._get_houser_by_id(data.id)
    assert data2.id == data.id


def test_get_user_if_exist(db, user, house):
    data, created = db._get_or_create_house(house)
    assert created is True
    house_id = 1
    db._insert_user(user, house_id)
    user_from_db, exist = db.get_user_if_exist(user.id)
    assert exist is True
    assert user_from_db.id == user.id  # FIXME
