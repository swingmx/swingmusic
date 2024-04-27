import json
from app.models.user import User
from app.utils.auth import encode_password
from app.db.sqlite.utils import SQLiteManager


class SQLiteAuthMethods:
    """
    Methods for authenticating users.
    """

    @staticmethod
    def insert_user(user: dict[str, str]):
        """
        Insert a user into the database.

        :param user: A dict with the username, password and roles.
        """
        sql = """INSERT INTO users(
        username,
        password,
        roles
        ) VALUES(:username, :password, :roles)
        """

        user_tuple = tuple(user.values())

        with SQLiteManager(userdata_db=True) as cur:
            cur = cur.execute(sql, user_tuple)
            userid = cur.lastrowid
            return userid
            # if userid:
            #     # sleep
            #     user = SQLiteAuthMethods.get_user_by_id(userid).todict_simplified()
            #     cur.close()
            #     return user

        raise Exception(f"Failed to insert user: {user}")

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
        return SQLiteAuthMethods.insert_user(user)

    @staticmethod
    def insert_guest_user():
        """
        Inserts the default guest user.
        """
        user = {
            "username": "guest",
            "password": encode_password("guest"),
            "roles": json.dumps(["guest"]),
        }

        return SQLiteAuthMethods.insert_user(user)

    @staticmethod
    def update_user(user: dict[str, str]):
        """
        Update a user in the database.

        :param user: A dict with the username, password and roles.
        """
        # get all user dict keys
        keys = list(user.keys())
        sql = f"""UPDATE users SET
        {', '.join([f"{key} = :{key}" for key in keys if key != 'id'])}
        WHERE id = :id
        """

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, user)
            cur.close()

        return SQLiteAuthMethods.get_user_by_id(user["id"]).todict()

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

    @staticmethod
    def get_user_by_id(userid: int):
        """
        Get a user by id.
        """
        sql = "SELECT * FROM users WHERE id = ?"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (userid,))

            data = cur.fetchone()
            cur.close()

            if data is not None:
                return User(*data)

            return None

    @staticmethod
    def delete_user_by_username(username: str):
        """
        Delete a user by username.
        """
        sql = "DELETE FROM users WHERE username = ?"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (username,))
            cur.close()
