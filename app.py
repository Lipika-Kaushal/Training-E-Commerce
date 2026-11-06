import os
import secrets
import sqlite3
from contextlib import closing
from functools import wraps

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from database import DATABASE_PATH, initialize_database


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


def get_products():
    with closing(sqlite3.connect(DATABASE_PATH)) as con:
        return con.execute(
            "SELECT id, name, price FROM products ORDER BY id"
        ).fetchall()


def get_cart_items():
    quantities = session.get("cart", {})
    products = {product[0]: product for product in get_products()}
    items = []
    for product_id, quantity in quantities.items():
        product = products.get(int(product_id))
        if product is not None:
            items.append(
                {
                    "id": product[0],
                    "name": product[1],
                    "price": product[2],
                    "quantity": quantity,
                    "subtotal": product[2] * quantity,
                }
            )
    return items


@app.template_filter("inr")
def format_inr(amount):
    return f"₹{amount:,.0f}"


@app.context_processor
def inject_cart_count():
    cart = session.get("cart", {})
    return {"cart_count": sum(cart.values())}


@app.route("/", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("shop"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        with closing(sqlite3.connect(DATABASE_PATH)) as con:
            user = con.execute(
                "SELECT username FROM users WHERE username=? AND password=? LIMIT 1",
                (username, password),
            ).fetchone()
        if user:
            session.clear()
            session["username"] = user[0]
            session["cart"] = {}
            return redirect(url_for("shop"))
        flash("That username and password don't match. Please try again.", "error")

    return render_template("login.html")


@app.get("/shop")
@login_required
def shop():
    return render_template("shop.html", products=get_products())


@app.post("/cart/add")
@login_required
def add_to_cart():
    try:
        product_id = int(request.form.get("product_id", ""))
        quantity = int(request.form.get("quantity", "1"))
    except ValueError:
        flash("Choose a valid product and quantity.", "error")
        return redirect(url_for("shop"))

    product = next((p for p in get_products() if p[0] == product_id), None)
    if product is None or quantity < 1 or quantity > 99:
        flash("Choose a valid product and a quantity from 1 to 99.", "error")
        return redirect(url_for("shop"))

    cart = session.get("cart", {})
    cart[str(product_id)] = min(cart.get(str(product_id), 0) + quantity, 99)
    session["cart"] = cart
    flash(f"{product[1]} added to your bag.", "success")
    return redirect(url_for("shop"))


@app.get("/cart")
@login_required
def cart():
    items = get_cart_items()
    total = sum(item["subtotal"] for item in items)
    shipping = 0 if total >= 50000 else 100
    return render_template(
        "cart.html",
        items=items,
        total=total,
        shipping=shipping,
        grand_total=total + shipping,
    )


@app.post("/cart/update/<int:product_id>")
@login_required
def update_cart(product_id):
    try:
        quantity = int(request.form.get("quantity", ""))
    except ValueError:
        flash("Enter a valid quantity.", "error")
        return redirect(url_for("cart"))

    cart = session.get("cart", {})
    key = str(product_id)
    if key not in cart:
        flash("That item is not in your bag.", "error")
    elif quantity < 0 or quantity > 99:
        flash("Quantity must be between 0 and 99.", "error")
    elif quantity == 0:
        cart.pop(key)
        session["cart"] = cart
        flash("Item removed from your bag.", "success")
    else:
        cart[key] = quantity
        session["cart"] = cart
        flash("Your bag has been updated.", "success")
    return redirect(url_for("cart"))


@app.post("/checkout")
@login_required
def checkout():
    items = get_cart_items()
    if not items:
        flash("Your bag is empty. Add something lovely first.", "error")
        return redirect(url_for("shop"))

    total = sum(item["subtotal"] for item in items)
    shipping = 0 if total >= 50000 else 100
    grand_total = total + shipping
    with closing(sqlite3.connect(DATABASE_PATH)) as con:
        with con:
            con.executemany(
                """
                INSERT INTO orders (username, product, quantity, total)
                VALUES (?, ?, ?, ?)
                """,
                [
                    (session["username"], item["name"], item["quantity"], item["subtotal"])
                    for item in items
                ],
            )

    session["cart"] = {}
    return render_template(
        "confirmation.html",
        items=items,
        total=total,
        shipping=shipping,
        grand_total=grand_total,
    )


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    initialize_database()
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
