import sqlite3
def get_products():
    con=sqlite3.connect("ecommerce.db")
    cur=con.cursor()
    cur.execute("SELECT * FROM products")
    data=cur.fetchall()
    con.close()
    return data

def show_products():
    print("Product Page Version 1")


def test_product_branch():
    print("This code was added from feature-catalogue-page")


