"""
This module contains the functions to interact with the SQLite database.
"""

import sqlite3
from sqlite3 import Connection as SqlConn


def create_connection(db_file: str) -> SqlConn:
    """
    Creates a connection to the specified database.
    """
    conn = sqlite3.connect(db_file)
    return conn


def create_tables(conn: SqlConn, sql_query: str):
    """
    Executes the specifiend SQL file to create database tables.
    """
    conn.executescript(sql_query)
