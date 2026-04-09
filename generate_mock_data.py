from faker import Faker
import psycopg2
import random

fake = Faker()

conn = psycopg2.connect(
    host="localhost",
    database="legacy_db",
    user="tanmay",
    password=""
)

cur = conn.cursor()

# -------------------------------
# 1. Insert Customers (3000)
# -------------------------------
print("Inserting customers...")
for _ in range(3000):
    cur.execute(
        """
        INSERT INTO cust_mast (cust_name, city, signup_date)
        VALUES (%s, %s, %s)
        """,
        (
            fake.name(),
            fake.city(),
            fake.date_between(start_date='-3y', end_date='today')
        )
    )

conn.commit()

# -------------------------------
# 2. Insert Products (100)
# -------------------------------
print("Inserting products...")
categories = ["Electronics", "Furniture", "Clothing", "Grocery"]

for _ in range(100):
    cur.execute(
        """
        INSERT INTO prod_cat (prod_name, category, price)
        VALUES (%s, %s, %s)
        """,
        (
            fake.word().capitalize(),
            random.choice(categories),
            round(random.uniform(100, 100000), 2)
        )
    )

conn.commit()

# -------------------------------
# 3. Insert Orders (7000)
# -------------------------------
print("Inserting orders...")
for _ in range(7000):
    cur.execute(
        """
        INSERT INTO ord_hist (cust_id, prod_id, qty, ord_date)
        VALUES (%s, %s, %s, %s)
        """,
        (
            random.randint(1, 3000),
            random.randint(1, 100),
            random.randint(1, 5),
            fake.date_between(start_date='-2y', end_date='today')
        )
    )

conn.commit()

cur.close()
conn.close()

print("Data generation complete!")