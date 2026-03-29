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

def push_products():
    if not os.path.exists('products.json'):
        print("products.json not found!")
        return

    with open('products.json', 'r') as f:
        products = json.load(f)

    print(f"Loaded {len(products)} products. Pushing to Supabase...")

    # Push products to the 'products' table
    # Using POST to insert rows
    response = requests.post(f"{URL}/rest/v1/products", headers=headers, json=products)

    if response.status_code in (200, 201):
        print("✅ Successfully pushed data to Supabase!")
    else:
        print(f"❌ Failed to push data. Status Code: {response.status_code}")
        print("Response:", response.text)
        print("\nNote: Please make sure the 'products' table is created in your Supabase dashboard.")
        print("You also need to temporarily disable Row Level Security (RLS) or add a policy to allow INSERTS.")

if __name__ == "__main__":
    push_products()
