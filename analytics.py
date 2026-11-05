import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analysis():
    con=sqlite3.connect("ecommerce.db")
    df=pd.read_sql_query(
        "SELECT * FROOM orders",con
    )
    con.close()
    print("Purchase Data")
    print(df)

    if df.empty:
        print("No purchases yet!")
        return
    
    #most purchased products
    sales=df.groupby('product')['quantity'].sum()

    print("\nMost Purchased Products")
    print(sales.sort_values(ascending=False))

    sns.barplot(x=sales.index,y=sales.values)

    plt.title("Most Purchased Products")
    plt.xlabel("Products")
    plt.ylabel("Quantity Sold")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


    #purchased by users
    user_sales=df.groupby('username')['quantity'].sum()
    sns.barplot(x=user_sales.index,y=user_sales.values)
    plt.title("Purchases by Users")
    plt.xlabel("Users")
    plt.ylabel("Quantity Purchased")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


    #user product heatmap
    pivot=df.pivot_table(
        index='username',
        columns='product',
        values='quantity',
        aggfunc='sum',
        fill_value=0
    )

    sns.heatmap(pivot,annot=True,cmap='Blues')

    plt.title("User Product Purchase Patterns")
    plt.tight_layout()
    plt.show()

    