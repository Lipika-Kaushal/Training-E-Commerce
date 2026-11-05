import sqlite3
con=sqlite3.connect("ecommerce.db")
cur=con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    username TEXT,password TEXT
    )
    """)

cur.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY,
    name TEXT,
    price INTEGER
    )
""")

users=[
    (1,'u1','p123'),
    (2,'u2','p123'),
    (3,'u3','p123'),
    (4,'u4','p123'),
    (5,'u5','p123')
]

products=[
    (1,'Laptop',50000),
    (2,'Mobile',20000),
    (3,'Keyboard',1000),
    (4,'Mouse',500),
    (5,'Headphones',2000)
]

cur.executemany(
    "INSERT OR IGNORE INTO users VALUES(?,?,?)",users
)
cur.executemany(
    "INSERT OR IGNORE INTO products VALUES(?,?,?)",products
)

cur.execute(
        "SELECT * FROM users"
    )
con.commit()
con.close()

print("DATABASE CREATED")
