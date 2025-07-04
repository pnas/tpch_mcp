import os
import psycopg2
from psycopg2 import Error
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker()

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    """Establishes and returns a database connection."""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set.")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Error as e:
        print(f"Error connecting to the database: {e}")
        raise

def generate_region_data(num_rows=20):
    """Generates data for the REGION table."""
    data = []
    for i in range(num_rows):
        r_regionkey = i
        r_name = fake.word().upper()[:25]
        r_comment = fake.sentence(nb_words=20)[:152]
        data.append((r_regionkey, r_name, r_comment))
    return data

def generate_nation_data(num_rows=20, region_keys=None):
    """Generates data for the NATION table."""
    if region_keys is None:
        # Fallback if region_keys are not provided, though they should be from generated region data
        region_keys = list(range(20)) # Assuming 20 regions were generated

    data = []
    for i in range(num_rows):
        n_nationkey = i
        n_name = fake.country()[:25]
        n_regionkey = random.choice(region_keys) # Link to existing region keys
        n_comment = fake.sentence(nb_words=20)[:152]
        data.append((n_nationkey, n_name, n_regionkey, n_comment))
    return data

def generate_part_data(num_rows=20):
    """Generates data for the PART table."""
    data = []
    for i in range(num_rows):
        p_partkey = i
        p_name = fake.sentence(nb_words=5)[:55]
        p_mfgr = fake.company()[:25]
        p_brand = fake.word().upper()[:10]
        p_type = f"{fake.word().upper()}{fake.word().upper()}"[:25]
        p_size = random.randint(1, 50)
        p_container = random.choice(["SM CASE", "LG BOX", "MED BAG", "JUMBO PKG"])[:10]
        p_retailprice = round(random.uniform(10.0, 1000.0), 2)
        p_comment = fake.sentence(nb_words=10)[:23]
        data.append((p_partkey, p_name, p_mfgr, p_brand, p_type, p_size, p_container, p_retailprice, p_comment))
    return data

def generate_supplier_data(num_rows=20, nation_keys=None):
    """
    Generates data for the SUPPLIER table.
    Requires nation_keys from the NATION table.
    """
    if nation_keys is None:
        nation_keys = list(range(20)) # Assuming 20 nations were generated

    data = []
    for i in range(num_rows):
        s_suppkey = i
        s_name = fake.company()[:25]
        s_address = fake.address().replace("\n", ", ")[:40]
        s_nationkey = random.choice(nation_keys)
        s_phone = fake.phone_number()[:15]
        s_acctbal = round(random.uniform(100.0, 10000.0), 2)
        s_comment = fake.sentence(nb_words=20)[:101]
        data.append((s_suppkey, s_name, s_address, s_nationkey, s_phone, s_acctbal, s_comment))
    return data

def generate_partsupp_data(num_rows=20, part_keys=None, supp_keys=None):
    """
    Generates data for the PARTSUPP table.
    Requires part_keys from PART and supp_keys from SUPPLIER.
    """
    if part_keys is None:
        part_keys = list(range(20))
    if supp_keys is None:
        supp_keys = list(range(20))

    data = []
    # Ensure unique combinations for primary key (ps_partkey, ps_suppkey)
    generated_combinations = set()
    for i in range(num_rows):
        while True:
            ps_partkey = random.choice(part_keys)
            ps_suppkey = random.choice(supp_keys)
            if (ps_partkey, ps_suppkey) not in generated_combinations:
                generated_combinations.add((ps_partkey, ps_suppkey))
                break
        
        ps_availqty = random.randint(1, 1000)
        ps_supplycost = round(random.uniform(1.0, 1000.0), 2)
        ps_comment = fake.sentence(nb_words=20)[:199]
        data.append((ps_partkey, ps_suppkey, ps_availqty, ps_supplycost, ps_comment))
    return data

def generate_customer_data(num_rows=20, nation_keys=None):
    """
    Generates data for the CUSTOMER table.
    Requires nation_keys from the NATION table.
    """
    if nation_keys is None:
        nation_keys = list(range(20))

    data = []
    for i in range(num_rows):
        c_custkey = i
        c_name = fake.name()[:25]
        c_address = fake.address().replace("\n", ", ")[:40]
        c_nationkey = random.choice(nation_keys)
        c_phone = fake.phone_number()[:15]
        c_acctbal = round(random.uniform(-1000.0, 10000.0), 2)
        c_mktsegment = random.choice(["AUTOMOBILE", "BUILDING", "FURNITURE", "MACHINERY", "HOUSEHOLD"])[:10]
        c_comment = fake.sentence(nb_words=20)[:117]
        data.append((c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment))
    return data

def generate_orders_data(num_rows=20, cust_keys=None):
    """
    Generates data for the ORDERS table.
    Requires cust_keys from the CUSTOMER table.
    """
    if cust_keys is None:
        cust_keys = list(range(20))

    data = []
    for i in range(num_rows):
        o_orderkey = i
        o_custkey = random.choice(cust_keys)
        o_orderstatus = random.choice(["O", "F", "P"]) # Open, Finished, Pending
        o_totalprice = round(random.uniform(100.0, 100000.0), 2)
        o_orderdate = fake.date_between(start_date="-5y", end_date="today")
        o_orderpriority = random.choice(["1-URGENT", "2-HIGH", "3-MEDIUM", "4-NOT SPECIFIED", "5-LOW"])[:15]
        o_clerk = fake.name()[:15]
        o_shippriority = 0 # Always 0 in TPC-H
        o_comment = fake.sentence(nb_words=20)[:79]
        data.append((o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment))
    return data

def generate_lineitem_data(num_rows=20, order_keys=None, part_supp_keys=None):
    """
    Generates data for the LINEITEM table.
    Requires order_keys from ORDERS and part_supp_keys (tuples of (partkey, suppkey)) from PARTSUPP.
    """
    if order_keys is None:
        order_keys = list(range(20))
    if part_supp_keys is None:
        # Assuming part_supp_keys are (partkey, suppkey) tuples
        part_supp_keys = [(i, i) for i in range(20)] # Placeholder

    data = []
    for i in range(num_rows):
        l_orderkey = random.choice(order_keys)
        l_linenumber = i + 1 # Unique per orderkey
        
        # Ensure part_supp_key is valid
        if part_supp_keys:
            l_partkey, l_suppkey = random.choice(part_supp_keys)
        else:
            l_partkey = random.randint(0, 19) # Fallback
            l_suppkey = random.randint(0, 19) # Fallback

        l_quantity = round(random.uniform(1.0, 50.0), 2)
        l_extendedprice = round(random.uniform(100.0, 5000.0), 2)
        l_discount = round(random.uniform(0.0, 0.10), 2)
        l_tax = round(random.uniform(0.01, 0.08), 2)
        l_returnflag = random.choice(["R", "A", "N"]) # Returned, Approved, None
        l_linestatus = random.choice(["O", "F"]) # Open, Finished
        
        ship_date = fake.date_between(start_date="-2y", end_date="today")
        commit_date = ship_date + timedelta(days=random.randint(1, 30))
        receipt_date = commit_date + timedelta(days=random.randint(1, 30))

        l_shipinstruct = random.choice(["DELIVER IN PERSON", "COLLECT COD", "NONE", "TAKE BACK RETURN"])[:25]
        l_shipmode = random.choice(["AIR", "RAIL", "TRUCK", "SHIP"])[:10]
        l_comment = fake.sentence(nb_words=10)[:44]
        data.append((l_orderkey, l_partkey, l_suppkey, l_linenumber, l_quantity, l_extendedprice, l_discount, l_tax, l_returnflag, l_linestatus, ship_date, commit_date, receipt_date, l_shipinstruct, l_shipmode, l_comment))
    return data

def insert_data(conn, table_name, columns, data):
    """Inserts generated data into the specified table."""
    if not data:
        print(f"No data to insert for {table_name}.")
        return

    cursor = conn.cursor()
    placeholders = ", ".join(["%s"] * len(columns))
    column_names = ", ".join(columns)
    insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;" # ON CONFLICT DO NOTHING for primary keys

    try:
        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"Successfully inserted {len(data)} rows into {table_name}.")
    except Error as e:
        conn.rollback()
        print(f"Error inserting data into {table_name}: {e}")
    finally:
        cursor.close()

def main():
    conn = None
    try:
        conn = get_db_connection()

        # Generate and insert data for each table in dependency order
        print("Generating and inserting REGION data...")
        region_data = generate_region_data()
        insert_data(conn, "region", ["r_regionkey", "r_name", "r_comment"], region_data)
        region_keys = [row[0] for row in region_data]

        print("Generating and inserting NATION data...")
        nation_data = generate_nation_data(region_keys=region_keys)
        insert_data(conn, "nation", ["n_nationkey", "n_name", "n_regionkey", "n_comment"], nation_data)
        nation_keys = [row[0] for row in nation_data]

        print("Generating and inserting PART data...")
        part_data = generate_part_data()
        insert_data(conn, "part", ["p_partkey", "p_name", "p_mfgr", "p_brand", "p_type", "p_size", "p_container", "p_retailprice", "p_comment"], part_data)
        part_keys = [row[0] for row in part_data]

        print("Generating and inserting SUPPLIER data...")
        supplier_data = generate_supplier_data(nation_keys=nation_keys)
        insert_data(conn, "supplier", ["s_suppkey", "s_name", "s_address", "s_nationkey", "s_phone", "s_acctbal", "s_comment"], supplier_data)
        supplier_keys = [row[0] for row in supplier_data]

        print("Generating and inserting PARTSUPP data...")
        partsupp_data = generate_partsupp_data(part_keys=part_keys, supp_keys=supplier_keys)
        insert_data(conn, "partsupp", ["ps_partkey", "ps_suppkey", "ps_availqty", "ps_supplycost", "ps_comment"], partsupp_data)
        part_supp_keys = [(row[0], row[1]) for row in partsupp_data]

        print("Generating and inserting CUSTOMER data...")
        customer_data = generate_customer_data(nation_keys=nation_keys)
        insert_data(conn, "customer", ["c_custkey", "c_name", "c_address", "c_nationkey", "c_phone", "c_acctbal", "c_mktsegment", "c_comment"], customer_data)
        customer_keys = [row[0] for row in customer_data]

        print("Generating and inserting ORDERS data...")
        orders_data = generate_orders_data(cust_keys=customer_keys)
        insert_data(conn, "orders", ["o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice", "o_orderdate", "o_orderpriority", "o_clerk", "o_shippriority", "o_comment"], orders_data)
        order_keys = [row[0] for row in orders_data]

        print("Generating and inserting LINEITEM data...")
        lineitem_data = generate_lineitem_data(order_keys=order_keys, part_supp_keys=part_supp_keys)
        insert_data(conn, "lineitem", ["l_orderkey", "l_partkey", "l_suppkey", "l_linenumber", "l_quantity", "l_extendedprice", "l_discount", "l_tax", "l_returnflag", "l_linestatus", "l_shipdate", "l_commitdate", "l_receiptdate", "l_shipinstruct", "l_shipmode", "l_comment"], lineitem_data)

        print("Data generation and insertion complete.")

    except Exception as e:
        print(f"An error occurred during data generation: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()
