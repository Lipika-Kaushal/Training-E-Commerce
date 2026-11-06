from database import initialize_database
from user import login
from catalog import display_catalog
from cart import shopping_cart
from shipping import shipping
from analytics import analysis


def main():
    initialize_database()
    username = login()

    if username:
        print("\nWELCOME", username)
        display_catalog()
        total = shopping_cart(username)
        shipping(total)
        print("\nThank you for shopping!")
        analysis()


if __name__ == "__main__":
    main()
