def shipping(total):
    if total>=50000:
        charge=0
    else:
        charge=100

    final_price=total+charge
    print("SHIPPING DETAILS")
    print("CART PRICE : ",total)
    print("SHIPPING CHARGE:",charge)
    print("FINAL PRICE:",final_price)