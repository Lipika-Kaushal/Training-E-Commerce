import sqlite3
from contextlib import closing

from database import DATABASE_PATH


def get_products():
    with closing(sqlite3.connect(DATABASE_PATH)) as con:
        return con.execute(
            "SELECT id, name, price FROM products ORDER BY id"
        ).fetchall()

def show_products():
    print("Product Page Version 1")


def test_product_branch():
    print("This code was added from feature-cart-page")