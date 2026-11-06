import sqlite3
from contextlib import closing
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().with_name("ecommerce.db")


def initialize_database():
    users = [
        ("u1", "p123"),
        ("u2", "p123"),
        ("u3", "p123"),
        ("u4", "p123"),
        ("u5", "p123"),
    ]
    products = [
        (1, "Laptop", 50000),
        (2, "Mobile", 20000),
        (3, "Keyboard", 1000),
        (4, "Mouse", 500),
        (5, "Headphones", 2000),
    ]

    with closing(sqlite3.connect(DATABASE_PATH)) as con:
        with con:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    password TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    price INTEGER
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS orders(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    product TEXT NOT NULL,
                    quantity INTEGER NOT NULL CHECK(quantity > 0),
                    total INTEGER NOT NULL
                )
            """)
            cur.executemany(
                """
                INSERT INTO users (username, password)
                SELECT ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM users WHERE username = ?
                )
                """,
                [(username, password, username) for username, password in users],
            )
            cur.executemany(
                "INSERT OR IGNORE INTO products (id, name, price) VALUES (?, ?, ?)",
                products,
            )


if __name__ == "__main__":
    initialize_database()
    print("DATABASE CREATED")
