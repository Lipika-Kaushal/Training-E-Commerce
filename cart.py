import sqlite3
from contextlib import closing

from database import DATABASE_PATH
from products import get_products


def shopping_cart(username):
    products = {product[0]: product for product in get_products()}
    cart = {}
    while True:
        try:
            product_id = int(input("Enter Product ID (0 to stop): "))
        except ValueError:
            print("Please enter a valid product ID.")
            continue
        if product_id == 0:
            break
        if product_id not in products:
            print("Invalid product ID!")
            continue
        try:
            quantity = int(input("Enter Quantity: "))
        except ValueError:
            print("Please enter a valid quantity.")
            continue
        if quantity <= 0:
            print("Quantity must be greater than zero.")
            continue
        cart[product_id] = cart.get(product_id, 0) + quantity

    total = 0
    print("SHOPPING CART:")
    with closing(sqlite3.connect(DATABASE_PATH)) as con:
        with con:
            for product_id, quantity in cart.items():
                _, name, price = products[product_id]
                amount = price * quantity
                total += amount
                print(
                    f"{name}: Rs. {price} x {quantity} = Rs. {amount}"
                )
                con.execute(
                    """
                    INSERT INTO orders (username, product, quantity, total)
                    VALUES (?, ?, ?, ?)
                    """,
                    (username, name, quantity, amount),
                )

    print(f"Cart total: Rs. {total}")
    return total
