import os
import sqlite3
from sqlite3 import Error as SqlError

from app.imgserver import APP_DIR

db_path = os.path.join(APP_DIR, "alice.sqlite")
cwd = os.path.dirname(os.path.abspath(__file__))
schema_path = os.path.join(cwd, "schemas")


def get_path(filepath: str):
    return os.path.join(schema_path, filepath)


def get_schemas() -> dict:
    """
    Returns a list of all the schemas in the schema directory
    """
    return [get_path(f) for f in os.listdir(schema_path)]


def create_connection(path: str) -> sqlite3.Connection:
    """
    Create a database connection to a SQLite database

    :param path: path to the database file
    :return: Connection object or None
    """

    conn = None

    try:
        conn = sqlite3.connect(path)
    except SqlError as e:
        print(e)

    return conn


def close_connection(conn: sqlite3.Connection) -> None:
    """
    Close the connection to the database

    :param conn: Connection object
    :return: None
    """

    conn.close()


def create_schema(conn: sqlite3.Connection, schema_path: str) -> None:
    """
    Create the database schema

    :param conn: Connection object
    :param schema_path: Path to the schema file
    :return: None
    """
    print("Creating schema")
    with open(schema_path, "r") as f:
        schema = f.read()

        try:
            conn.executescript(schema)
        except SqlError as e:
            print(e)


def run():
    conn = create_connection(db_path)

    if conn is not None:
        for schema in get_schemas():
            create_schema(conn, schema)

        close_connection(conn)
