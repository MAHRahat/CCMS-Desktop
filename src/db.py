import os
import sqlite3
from pathlib import Path
from sqlite3 import Error

from src.ccms_constants import APP_DIR

DB_NAME = "ccms_desktop.db"
CREATE_TBL_AUTH = """
                CREATE TABLE IF NOT EXISTS auth (
                kee text PRIMARY KEY UNIQUE,
                value text
                )
                """

INSERT_TBL_AUTH = """
                INSERT INTO auth (kee, value)
                values (?, ?)
                """

SELECT_TBL_AUTH = """
                SELECT value FROM auth
                WHERE kee = 'token'
                """

DELETE_TBL_AUTH = """
                DELETE FROM auth
                """


def db_create_connection():
    """
    Creates a connection to a local SQLite database.
    :return: connection if successful, None otherwise.
    """
    conn = None
    user_home_dir = str(Path.home())
    db_dir = os.path.join(user_home_dir, APP_DIR, "db")
    Path(db_dir).mkdir(parents=True, exist_ok=True)
    try:
        conn = sqlite3.connect(os.path.join(db_dir, DB_NAME))
    except Error as err:
        print(str(err))
    return conn


def db_create_auth_table(conn):
    """
    Creates a table to store authentication token.
    :param conn: connection to the local SQLite database
    :return: None
    """
    try:
        cursor = conn.cursor()
        cursor.execute(CREATE_TBL_AUTH)
    except Error as err:
        print(str(err))


def db_insert_auth_table(conn, kee, value):
    """
    Creates a record in the authentication table. Actually it is used to store authentication token.
    :param conn: connection to the local SQLite database
    :param kee: 1st field
    :param value: 2nd field
    :return: None
    """
    try:
        cursor = conn.cursor()
        cursor.execute(INSERT_TBL_AUTH, (kee, value))
        conn.commit()
    except Error as err:
        print(str(err))


def db_select_auth_table(conn):
    """
    Reads a record from the authentication table. Actually it is used to read the stored authorization token.
    :param conn: connection to the local SQLite database
    :return: Authorization token, if successful; None otherwise
    """
    auth_token = None
    try:
        cursor = conn.cursor()
        cursor.execute(SELECT_TBL_AUTH)
        conn.commit()
        rows = cursor.fetchall()
        if len(rows) > 0:
            row = rows[0]
            auth_token = row[0]
    except Error as err:
        print(str(err))
    return auth_token


def db_delete_auth_table(conn):
    """
    Deletes stored data in the authentication table.
    :param conn: connection to the local SQLite database
    :return: None
    """
    try:
        cursor = conn.cursor()
        cursor.execute(DELETE_TBL_AUTH)
        conn.commit()
    except Error as err:
        print(str(err))
