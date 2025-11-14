"""
Load CSVs into an SQLite database named ecom.db
Creates tables and imports CSV data.
"""
import sqlite3
import os
import csv

ROOT = os.path.join(os.path.dirname(__file__), '..')
DATADIR = os.path.join(ROOT, 'data')
DBPATH = os.path.join(ROOT, 'ecom.db')

TABLES = {
    'customers': ('customers.csv', ['customer_id','name','email','phone','created_at']),
    'products': ('products.csv', ['product_id','title','category','price','sku']),
    'shipping_addresses': ('shipping_addresses.csv', ['address_id','customer_id','address','city','state','postal_code','country']),
    'orders': ('orders.csv', ['order_id','customer_id','order_date','total_amount','shipping_address_id']),
    'order_items': ('order_items.csv', ['order_id','product_id','quantity','unit_price','line_total'])
}

def create_tables(conn):
    cur = conn.cursor()
    cur.executescript("""
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS customers (
      customer_id INTEGER PRIMARY KEY,
      name TEXT,
      email TEXT,
      phone TEXT,
      created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS products (
      product_id INTEGER PRIMARY KEY,
      title TEXT,
      category TEXT,
      price REAL,
      sku TEXT
    );
    CREATE TABLE IF NOT EXISTS shipping_addresses (
      address_id INTEGER PRIMARY KEY,
      customer_id INTEGER,
      address TEXT,
      city TEXT,
      state TEXT,
      postal_code TEXT,
      country TEXT,
      FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );
    CREATE TABLE IF NOT EXISTS orders (
      order_id INTEGER PRIMARY KEY,
      customer_id INTEGER,
      order_date TEXT,
      total_amount REAL,
      shipping_address_id INTEGER,
      FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
      FOREIGN KEY(shipping_address_id) REFERENCES shipping_addresses(address_id)
    );
    CREATE TABLE IF NOT EXISTS order_items (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      order_id INTEGER,
      product_id INTEGER,
      quantity INTEGER,
      unit_price REAL,
      line_total REAL,
      FOREIGN KEY(order_id) REFERENCES orders(order_id),
      FOREIGN KEY(product_id) REFERENCES products(product_id)
    );
    """)
    conn.commit()

def import_csv(conn, table_name, csv_file, columns):
    path = os.path.join(DATADIR, csv_file)
    if not os.path.exists(path):
        print("Missing CSV:", path)
        return
    cur = conn.cursor()
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = []
        for r in reader:
            rows.append([r[col] for col in columns])
    placeholders = ','.join(['?']*len(columns))
    sql = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
    cur.executemany(sql, rows)
    conn.commit()
    print(f"Imported {len(rows)} rows into {table_name}")

def main():
    if not os.path.exists(DATADIR):
        print("Data folder not found. Run generate_data.py first.")
        return
    if os.path.exists(DBPATH):
        print("Removing old DB:", DBPATH)
        os.remove(DBPATH)
    conn = sqlite3.connect(DBPATH)
    create_tables(conn)
    for table, (fname, cols) in TABLES.items():
        import_csv(conn, table, fname, cols)
    conn.close()
    print("Database created at", DBPATH)

if __name__ == '__main__':
    main()
