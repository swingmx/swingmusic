import json
from app.models.user import User
from app.utils.auth import encode_password
from app.db.sqlite.utils import SQLiteManager


class SQLiteAuthMethods:
    """
    Methods for authenticating users.
    """

    @staticmethod
    def insert_default_user():
        """
        Inserts the default admin user.
        """
        user = {
            "username": "admin",
            "password": encode_password("admin"),
            "roles": json.dumps(["admin"]),
        }
        user_tuple = tuple(user.values())

        sql = """INSERT INTO users(
        username,
        password,
        roles
        ) VALUES(:username, :password, :roles)
        """

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, user_tuple)
            cur.close()

    @staticmethod
    def insert_guest_user():
        """
        Inserts the default guest user.
        """
        user = {
            "username": "guest",
            "password": encode_password("guest"),
            "firstname": "Guest",
            "lastname": "User",
            "roles": json.dumps(["guest"]),
        }
        user_tuple = tuple(user.values())

        sql = """INSERT INTO users(
        username,
        password,
        firstname,
        lastname,
        roles
        ) VALUES(:username, :password, :firstname, :lastname, :roles)
        """

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, user_tuple)
            cur.close()

    @staticmethod
    def get_all_users():
        """
        Check if there are any users in the database.
        """
        sql = "SELECT * FROM users"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql)

            data = cur.fetchall()
            cur.close()

            return [User(*user) for user in data]

    @staticmethod
    def get_user_by_username(username: str):
        """
        Get a user by username.
        """
        sql = "SELECT * FROM users WHERE username = ?"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (username,))

            data = cur.fetchone()
            cur.close()

            if data is not None:
                return User(*data)

            return None