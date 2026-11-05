from products import get_products
def display_catalog():
    print("PRODUCT CATALOG")
    products=get_products()
    for p in products:
        print(p[0],p[1],"Rs.",p[2])