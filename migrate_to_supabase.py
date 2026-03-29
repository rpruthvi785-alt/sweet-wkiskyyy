import sqlite3
import requests
import json
import os

URL = "https://ojhenudsmcvuiobpcqsv.supabase.co"
KEY = "sb_publishable_jtGvrWNZ5moIkQj1HwoWQQ_W5nFMfjE"

headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

DB_FILE = 'bakery.db'

def get_db_connection():
    if not os.path.exists(DB_FILE):
        return None
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def migrate_table(table_name):
    conn = get_db_connection()
    if not conn:
        print(f"Db {DB_FILE} not found!")
        return
        
    try:
        rows = conn.execute(f'SELECT * FROM {table_name}').fetchall()
    except Exception as e:
        print(f"Warning: Failed to read local table {table_name}. {e}")
        return
        
    records = []
    for r in rows:
        d = dict(r)
        if 'id' in d:
            del d['id'] # Remove local ID to let Supabase generate its own sequence correctly
        records.append(d)
    conn.close()

    if not records:
        print(f"No records found in local table '{table_name}'.")
        return

    print(f"Migrating {len(records)} records for '{table_name}'...")
    
    # We send records in chunks if there are many, but usually bakery.db doesn't have > 1000
    response = requests.post(f"{URL}/rest/v1/{table_name}", headers=headers, json=records)

    if response.status_code in (200, 201):
        print(f"SUCCESS: Successfully pushed '{table_name}' data to Supabase!")
    else:
        print(f"ERROR: Failed to push '{table_name}' data. Status: {response.status_code}")
        print(response.text)
        print("NOTE: Make sure the table exists in Supabase and RLS is temporarily disabled or allows inserts!")

if __name__ == "__main__":
    print("-" * 50)
    print("Starting migration to Supabase...")
    print("-" * 50)
    # The order matters slightly but there are no strict foreign keys yet.
    migrate_table("users")
    migrate_table("products")
    migrate_table("orders")
    print("-" * 50)
    print("Done!")
