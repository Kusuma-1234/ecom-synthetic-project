"""
Generate synthetic e-commerce CSV files:
- customers.csv
- products.csv
- orders.csv
- order_items.csv
- shipping_addresses.csv
"""
import csv
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()

OUTDIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(OUTDIR, exist_ok=True)

NUM_CUSTOMERS = 100
NUM_PRODUCTS = 50
NUM_ORDERS = 200
MAX_ITEMS_PER_ORDER = 5

def write_csv(path, headers, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print("Wrote:", path)

def generate_customers():
    rows = []
    for cid in range(1, NUM_CUSTOMERS+1):
        name = fake.name()
        email = f"user{cid}@{fake.free_email_domain()}"
        phone = fake.phone_number()
        created = fake.date_between(start_date='-2y', end_date='today').isoformat()
        rows.append([cid, name, email, phone, created])
    write_csv(os.path.join(OUTDIR, 'customers.csv'),
              ['customer_id','name','email','phone','created_at'], rows)

def generate_products():
    rows = []
    categories = ['Electronics','Home','Clothing','Sports','Books','Toys']
    for pid in range(1, NUM_PRODUCTS+1):
        title = f"{fake.word().title()} {random.choice(['Pro','Plus','Max',''])}".strip()
        category = random.choice(categories)
        price = round(random.uniform(5, 500),2)
        sku = f"SKU-{pid:04d}"
        rows.append([pid, title, category, price, sku])
    write_csv(os.path.join(OUTDIR, 'products.csv'),
              ['product_id','title','category','price','sku'], rows)

def generate_shipping_addresses():
    rows = []
    for aid in range(1, NUM_CUSTOMERS+1):
        cid = aid
        addr = fake.street_address()
        city = fake.city()
        state = fake.state()
        postal = fake.postcode()
        country = fake.country()
        rows.append([aid, cid, addr, city, state, postal, country])
    write_csv(os.path.join(OUTDIR, 'shipping_addresses.csv'),
              ['address_id','customer_id','address','city','state','postal_code','country'], rows)

def generate_orders_and_items():
    orders = []
    items = []
    order_id = 1
    for _ in range(NUM_ORDERS):
        cust = random.randint(1, NUM_CUSTOMERS)
        created = fake.date_time_between(start_date='-1y', end_date='now')
        num_items = random.randint(1, MAX_ITEMS_PER_ORDER)
        total = 0.0
        for i in range(num_items):
            pid = random.randint(1, NUM_PRODUCTS)
            qty = random.randint(1, 3)
            price = round(random.uniform(5, 500),2)  # naive price (you can join against products)
            subtotal = qty * price
            items.append([order_id, pid, qty, price, subtotal])
            total += subtotal
        shipping_id = cust  # simple mapping
        orders.append([order_id, cust, created.isoformat(), round(total,2), shipping_id])
        order_id += 1

    write_csv(os.path.join(OUTDIR, 'orders.csv'),
              ['order_id','customer_id','order_date','total_amount','shipping_address_id'], orders)
    write_csv(os.path.join(OUTDIR, 'order_items.csv'),
              ['order_id','product_id','quantity','unit_price','line_total'], items)

def main():
    generate_customers()
    generate_products()
    generate_shipping_addresses()
    generate_orders_and_items()
    print("Data generation complete. CSVs saved to:", OUTDIR)

if __name__ == '__main__':
    main()
