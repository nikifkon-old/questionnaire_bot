import os

import pytest

from tbot.database import DB
from tbot.datatypes import User, House


class TestDB(DB):
    @classmethod
    def setup(cls, db_file):
        database = cls(db_file)
        with open("create.sql") as file:
            create_script = file.read()
        for statement in create_script.split(";"):
            database.cursor.execute(statement)
        return database

    def clear(self):
        self.cursor.execute("DELETE FROM users")
        self.cursor.execute("DELETE FROM houses")
        self.cursor.execute("DELETE FROM events")

    def drop(self):
        self.close()
        os.remove(self.db_file)


@pytest.fixture(scope="session")
def session_db():
    database = TestDB.setup("test.db")
    yield database
    database.drop()


@pytest.fixture(scope="function")
def db(session_db):
    yield session_db
    session_db.clear()


@pytest.fixture
def house():
    return House(number=123, street="Lenina", area="Leniscij")


@pytest.fixture
def user(house):
    return User(id=100500, name="John", phone="+12345678901", house=house,
                flat=1)
