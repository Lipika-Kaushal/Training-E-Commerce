import sqlite3
def get_products():
    con=sqlite3.connect("ecommerce.db")
    cur=con.cursor()
    cur.execute("SELECT * FROM products")
    data=cur.fetchall()
    con.close()
    return data