import sqlite3
def login():
    username=input("Enter Username: ")
    password=input("Enter Password: ")
    con=sqlite3.connect("ecommerce.db")
    cur=con.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",(username,password)
    )
    user=cur.fetchone()
    con.close()
    if user:
        print("Login Successfull!")
        return username
    else:
        print("Invalid Login!")
        return None