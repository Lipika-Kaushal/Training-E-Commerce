import sqlite3
from contextlib import closing

from database import DATABASE_PATH


def login():
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    with closing(sqlite3.connect(DATABASE_PATH)) as con:
        user = con.execute(
            "SELECT 1 FROM users WHERE username=? AND password=? LIMIT 1",
            (username, password)
        ).fetchone()
    if user:
        print("Login Successful!")
        return username
    else:
        print("Invalid Login!")
        return None
