from user import login
from catalog import display_catalog
from cart import shopping_cart
from shipping import shipping
from analytics import analysis
#userlogin
username=login()

if username:
    print("\nWELCOME",username)
    display_catalog()
    #cart
    total=shopping_cart(username)
    #shipping
    shipping(total)
    print("\n Thankyou for Shopping!")

    #analytics
    analysis()
