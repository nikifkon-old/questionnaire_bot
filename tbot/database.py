import sqlite3
import logging

from tbot.datatypes import User, House


logger = logging.getLogger(__file__)


class DB():
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def save_user(self, user: User):
        with self.connection:
            house, created = self._get_or_create_house(user.house)
            _, exist = self.get_user_if_exist(user.id)
            if exist:
                self._update_user(user, house.id)
            else:
                self._insert_user(user, house.id)

    def get_user_if_exist(self, id: int) -> (User, bool):
        with self.connection:
            self.cursor.execute(
                """SELECT *
                FROM users
                WHERE id = ?;
                """,
                (id,))
            result = self.cursor.fetchone()
            if result is not None:
                user = User.from_turple(result)
                user.house = self._get_houser_by_id(user.house.id)
                return user, True
            else:
                return None, False

    def _get_houser_by_id(self, id: int):
        with self.connection:
            self.cursor.execute(
                """SELECT *
                FROM houses
                WHERE id = ?;
                """, (id,))
            row = self.cursor.fetchone()
            if row is None:
                return None
            else:
                return House.from_turple(row)

    def _get_or_create_house(self, house: House) -> (House, bool):
        with self.connection:
            self.cursor.execute(
                """SELECT *
                FROM houses
                WHERE street = ?
                    AND house_number = ?;
                """,
                (house.street, house.number))
            row = self.cursor.fetchone()
            created = False
            if row is None:
                self.cursor.execute(
                    """INSERT INTO houses
                    (street, house_number, area)
                    VALUES
                    (?, ?, ?)
                    """,
                    (house.street, house.number, house.area))
                self.cursor.execute(
                    """SELECT *
                    FROM houses
                    WHERE street = ?
                        AND house_number = ?;
                    """,
                    (house.street, house.number))
                row = self.cursor.fetchone()
                created = True

            return House.from_turple(row), created

    def _update_user(self, user: User, house_id: int):
        with self.connection:
            self.cursor.execute(
                """UPDATE users
                SET name = ?,
                    phone = ?,
                    house_id = ?,
                    flat = ?
                WHERE id = ?
                """,
                (user.name, user.phone, house_id, user.flat, user.id)
            )
            logger.debug("%s updated" % user)

    def _insert_user(self, user: User, house_id: int):
        with self.connection:
            self.cursor.execute(
                """INSERT INTO users
                (id, name, phone, house_id, flat)
                VALUES
                (?, ?, ?, ?, ?)
                """,
                (user.id, user.name, user.phone, house_id, user.flat,)
            )
            logger.debug("%s insert into database" % user)

    def close(self):
        self.connection.close()
