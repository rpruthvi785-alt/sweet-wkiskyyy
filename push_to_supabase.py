import requests
import json
import sqlite3

URL = "https://ojhenudsmcvuiobpcqsv.supabase.co"
KEY = "sb_publishable_jtGvrWNZ5moIkQj1HwoWQQ_W5nFMfjE"

headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def test_connection():
    # Try fetching from 'products'
    resp = requests.get(f"{URL}/rest/v1/products?limit=1", headers=headers)
    print("Products table:", resp.status_code, resp.text)

if __name__ == "__main__":
    test_connection()
