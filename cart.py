from products import get_products
import numpy as np
import sqlite3
def shopping_cart(username):
    cart={}
    products=get_products()
    while True:
        pid=int(input("Enter Product ID(0 to stop)"))
        if pid==0:
            break
        qty=int(input("Enter Quantity:"))
        if pid not in [p[0] for p in products] or qty<=0:
            print("Inva;id product or quantity!")
            continue
        cart[pid]=cart.get(pid,0)+qty
    total=0
    print("SHOPPING CART :")

    con=sqlite3.connect("ecommerce.db")
    cur=con.cursor()

    for pid,qty in cart.items():
        for p in products:
            if p[0]==pid:
                name=p[1]
                price=p[2]
                amount=np.multiply(price,qty)
                total=total+amount
                print("PRODUCTS:")
                print("PRICE:")
                print("QUANTITY:")
                print("FINAL PRICE:",price,"x",qty,"=",amount)

                cur.execute("""
                INSERT INTO orders VALUES(?,?,?,?)
                """,(username,name,qty,amount))
    con.commit()
    con.close()

